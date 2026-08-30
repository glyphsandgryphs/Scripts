# Root folder
$targetRoot = "D:\Photos"
$logFile = "$targetRoot\PhotoMigrationLog.txt"

# Ensure root and log file exist
if (!(Test-Path $targetRoot)) {
    New-Item -ItemType Directory -Path $targetRoot | Out-Null
}
New-Item -ItemType File -Path $logFile -Force | Out-Null

# Media types and extensions
$mediaTypes = @{
    "JPG"   = @("*.jpg","*.jpeg")
    "PNG"   = @("*.png")
    "HEIC"  = @("*.heic")
    "GIF"   = @("*.gif")
    "BMP"   = @("*.bmp")
    "TIFF"  = @("*.tiff")
}

# Folders to exclude
$excludeDirs = @("C:\Windows", "C:\Program Files", "C:\Program Files (x86)", "C:\ProgramData")

# Counters for summary
$totalFiles = 0
$typeCounts = @{}

# Create main structure
foreach ($type in $mediaTypes.Keys) {
    $typeFolder = Join-Path $targetRoot "By Media Type\$type"
    if (!(Test-Path $typeFolder)) {
        New-Item -ItemType Directory -Path $typeFolder | Out-Null
    }
    $typeCounts[$type] = 0
}

Write-Host "Scanning and copying files... Please wait."

# Collect all files first for progress tracking
$allFiles = @()
foreach ($type in $mediaTypes.Keys) {
    foreach ($ext in $mediaTypes[$type]) {
        $allFiles += Get-ChildItem -Path "C:\" -Include $ext -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $excludeDirs -notcontains $_.DirectoryName }
    }
}

$totalToProcess = $allFiles.Count
$processed = 0

# Copy files with progress
foreach ($file in $allFiles) {
    try {
        $type = ($mediaTypes.Keys | Where-Object { $file.Extension -match $_ })
        $year = $file.CreationTime.Year
        $yearFolder = Join-Path $targetRoot "By Media Type\$type\$year"
        if (!(Test-Path $yearFolder)) {
            New-Item -ItemType Directory -Path $yearFolder | Out-Null
        }
        $destPath = Join-Path $yearFolder $file.Name
        Copy-Item $file.FullName -Destination $destPath -Force

        # Update counters
        $totalFiles++
        $typeCounts[$type]++

        # Log the action
        Add-Content -Path $logFile -Value "Copied: $($file.FullName) -> $destPath"
    } catch {
        Add-Content -Path $logFile -Value "Failed: $($file.FullName) - Error: $($_.Exception.Message)"
    }

    # Update progress
    $processed++
    Write-Progress -Activity "Copying Photos" -Status "$processed of $totalToProcess" -PercentComplete (($processed / $totalToProcess) * 100)
}

# Summary report
Write-Host "`nSummary Report:"
Write-Host "--------------------------------"
Write-Host "Total files copied: $totalFiles"
foreach ($type in $typeCounts.Keys) {
    Write-Host "$type: $($typeCounts[$type]) files"
}
Write-Host "--------------------------------"
Write-Host "Log file saved at: $logFile"
