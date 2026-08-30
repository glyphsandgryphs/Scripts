<#
Cross-platform folder organizer (PowerShell).

Mirrors the behavior of `scripts/apply_structure.py` for Windows-first
workflows. Creates a predictable folder skeleton, routes files into category
folders based on extension, and renames them to a clean, portable format.

Example:
    pwsh scripts/apply_structure.ps1 -Roots "C:\\Sync", "D:\\External"
    pwsh scripts/apply_structure.ps1 -Roots "$HOME/OneDrive" -DryRun
#>
param(
    [Parameter(Mandatory = $true)]
    [string[]]$Roots,

    [switch]$DryRun
)

$CategoryMap = [ordered]@{
    "01_Documents" = @("pdf", "doc", "docx", "txt", "md", "rtf", "odt", "ppt", "pptx")
    "02_Data"      = @("csv", "xlsx", "xls", "json", "xml", "parquet")
    "03_Code"      = @("py", "js", "ts", "html", "css", "yaml", "yml", "json5", "sh", "ps1", "bat")
    "04_Images"    = @("jpg", "jpeg", "png", "gif", "svg", "heic", "bmp", "tif", "tiff", "webp")
    "05_Audio"     = @("mp3", "wav", "flac", "aac", "ogg", "m4a")
    "06_Video"     = @("mp4", "mov", "avi", "mkv", "webm")
    "07_Archives"  = @("zip", "tar", "gz", "rar", "7z")
    "08_Backups"   = @("bak", "tmp")
    "99_Misc"      = @()
}

$Skeleton = @(
    "00_Inbox",
    "10_Projects",
    "20_Archive",
    "30_Reference",
    "40_Exports"
)

function Sanitize-Stem {
    param([string]$Stem)
    $clean = $Stem.ToLower().Trim()
    $clean = -join ($clean.ToCharArray() | ForEach-Object {
        if ($_ -match '[a-z0-9._-]') { $_ } else { '_' }
    })
    $clean = ($clean -replace '_{2,}', '_').Trim('._')
    if ([string]::IsNullOrWhiteSpace($clean)) { $clean = 'unnamed' }
    if ($clean.Length -gt 80) { $clean = $clean.Substring(0,80).Trim('._') }
    return $clean
}

function Ensure-Directories {
    param([string]$Root)
    foreach ($folder in $CategoryMap.Keys + $Skeleton) {
        $target = Join-Path -Path $Root -ChildPath $folder
        if (-not (Test-Path -LiteralPath $target)) {
            New-Item -ItemType Directory -Path $target | Out-Null
        }
    }
}

function Determine-Category {
    param([System.IO.FileInfo]$File)
    $suffix = $File.Extension.TrimStart('.').ToLower()
    foreach ($entry in $CategoryMap.GetEnumerator()) {
        if ($entry.Value -contains $suffix) { return $entry.Key }
    }
    return '99_Misc'
}

function Move-FileSafe {
    param(
        [System.IO.FileInfo]$File,
        [string]$DestinationDir
    )
    $sanitized = Sanitize-Stem $File.BaseName
    $target = Join-Path -Path $DestinationDir -ChildPath "$sanitized$($File.Extension.ToLower())"
    $counter = 1
    while ((Test-Path -LiteralPath $target) -and ($target -ne $File.FullName)) {
        $target = Join-Path -Path $DestinationDir -ChildPath "$sanitized_$counter$($File.Extension.ToLower())"
        $counter += 1
    }
    if ($DryRun) {
        Write-Host "[dry-run] Would move $($File.FullName) -> $target"
    } else {
        if (-not (Test-Path -LiteralPath $DestinationDir)) {
            New-Item -ItemType Directory -Path $DestinationDir | Out-Null
        }
        Move-Item -LiteralPath $File.FullName -Destination $target
        Write-Host "Moved $($File.FullName) -> $target"
    }
}

function Test-InManagedFolder {
    param(
        [System.IO.FileInfo]$File,
        [System.IO.DirectoryInfo]$RootDirectory
    )

    $directory = $File.Directory
    while ($null -ne $directory -and $directory.FullName -ne $RootDirectory.FullName) {
        if ($CategoryMap.Contains($directory.Name) -or $Skeleton -contains $directory.Name) {
            return $true
        }
        $directory = $directory.Parent
    }
    return $false
}

foreach ($root in $Roots) {
    Write-Host "Processing root: $root"
    if (-not (Test-Path -LiteralPath $root -PathType Container)) {
        Write-Warning "Skipping $root (not found or not a directory)"
        continue
    }

    $rootDirectory = Get-Item -LiteralPath $root
    if (-not $DryRun) {
        Ensure-Directories -Root $rootDirectory.FullName
    }
    $moved = @{}
    $skipped = 0

    Get-ChildItem -LiteralPath $rootDirectory.FullName -Recurse -File | ForEach-Object {
        $file = $_
        if (Test-InManagedFolder -File $file -RootDirectory $rootDirectory) {
            Write-Verbose "Skipping already categorized file $($file.FullName)"
            $skipped += 1
            return
        }
        $category = Determine-Category -File $file
        $destDir = Join-Path -Path $rootDirectory.FullName -ChildPath $category
        Move-FileSafe -File $file -DestinationDir $destDir
        if ($moved.ContainsKey($category)) { $moved[$category] += 1 } else { $moved[$category] = 1 }
    }

    Write-Host "Summary for $root -> moved: $($moved | Out-String), skipped: $skipped"
}
