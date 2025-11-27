param(
    [string]$TargetRoot = "D:\Photos",
    [string[]]$SourceRoots = @("C:\"),
    [switch]$WhatIf
)

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
$excludeDirs = @(
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData",
    $TargetRoot
)

function Assert-DriveReady {
    param([string]$Path)
    $driveLetter = ([System.IO.Path]::GetPathRoot($Path)).TrimEnd('\\')
    $driveInfo = [System.IO.DriveInfo]::GetDrives() | Where-Object { $_.Name.TrimEnd('\\') -eq $driveLetter }
    if (-not $driveInfo -or -not $driveInfo.IsReady) {
        throw "Destination drive '$driveLetter' is not available. Insert the microSD card and try again."
    }
}

function Ensure-Folder {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Get-UniquePath {
    param([string]$Path)
    $directory = Split-Path $Path -Parent
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($Path)
    $extension = [System.IO.Path]::GetExtension($Path)
    $candidate = $Path
    $suffix = 1
    while (Test-Path $candidate) {
        $candidate = Join-Path $directory "$baseName ($suffix)$extension"
        $suffix++
    }
    return $candidate
}

Assert-DriveReady -Path $TargetRoot

# Ensure root and log file exist
Ensure-Folder -Path $TargetRoot
$logFile = Join-Path $TargetRoot "PhotoMigrationLog.txt"
New-Item -ItemType File -Path $logFile -Force | Out-Null

# Counters for summary
$totalMoved = 0
$totalSkipped = 0
$totalFailed = 0
$typeCounts = @{}

# Create main structure
foreach ($type in $mediaTypes.Keys) {
    $typeFolder = Join-Path $TargetRoot "By Media Type\$type"
    Ensure-Folder -Path $typeFolder
    $typeCounts[$type] = 0
}

Write-Host "Scanning and moving files... This may take a while."

# Collect all files first for progress tracking
$allFiles = @()
foreach ($type in $mediaTypes.Keys) {
    foreach ($ext in $mediaTypes[$type]) {
        foreach ($root in $SourceRoots) {
            $allFiles += Get-ChildItem -Path $root -Include $ext -Recurse -ErrorAction SilentlyContinue |
                Where-Object { $excludeDirs -notcontains $_.DirectoryName }
        }
    }
}

$allFiles = $allFiles | Sort-Object FullName -Unique
$totalToProcess = $allFiles.Count
$processed = 0

foreach ($file in $allFiles) {
    try {
        $type = ($mediaTypes.Keys | Where-Object { $file.Extension -match $_ })
        if (-not $type) {
            $totalSkipped++
            Add-Content -Path $logFile -Value "Skipped (unknown type): $($file.FullName)"
            continue
        }

        $year = $file.CreationTime.Year
        $yearFolder = Join-Path $TargetRoot "By Media Type\$type\$year"
        Ensure-Folder -Path $yearFolder

        $destPath = Join-Path $yearFolder $file.Name
        $destPath = Get-UniquePath -Path $destPath

        Move-Item -LiteralPath $file.FullName -Destination $destPath -Force -WhatIf:$WhatIf

        # Update counters
        $totalMoved++
        $typeCounts[$type]++

        # Log the action
        Add-Content -Path $logFile -Value "Moved: $($file.FullName) -> $destPath"
    } catch {
        $totalFailed++
        Add-Content -Path $logFile -Value "Failed: $($file.FullName) - Error: $($_.Exception.Message)"
    }

    # Update progress
    $processed++
    $percent = if ($totalToProcess -eq 0) { 100 } else { ($processed / $totalToProcess) * 100 }
    Write-Progress -Activity "Moving Photos" -Status "$processed of $totalToProcess" -PercentComplete $percent
}

# Summary report
Write-Host "`nSummary Report:"
Write-Host "--------------------------------"
Write-Host "Total files moved: $totalMoved"
Write-Host "Total skipped: $totalSkipped"
Write-Host "Total failed: $totalFailed"
foreach ($type in $typeCounts.Keys) {
    Write-Host "$type: $($typeCounts[$type]) files"
}
Write-Host "--------------------------------"
Write-Host "Log file saved at: $logFile"
Write-Host "Use -WhatIf to preview changes without moving files."
