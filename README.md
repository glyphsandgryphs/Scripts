# Scripts Repository

This repository contains utility scripts plus lightweight documentation and tests.

## Sample CLI tool

- Location: `scripts/sample_tool.py`
- Purpose: Provide a representative script that demonstrates robust argument parsing, validated input, and structured logging (console + optional file output).
- Usage docs: [`docs/scripts.md`](docs/scripts.md)

Quick example:

```bash
python scripts/sample_tool.py --name Ada --count 3 --verbose --uppercase --log-file logs/sample.log
```

## File organizer

- Location: `scripts/organize_files.py`
- Purpose: Organize files inside a target directory into subfolders named after their file extensions.
- Usage: `python scripts/organize_files.py <directory> [--verbose]`

## Photo migration to microSD (drive D:)

- Location: `scripts/photo_migration.py`
- Purpose: Move or copy common photo formats onto a microSD card mounted at drive `D:`.

### Usage

```bash
# Move photos from the default Windows picture folders to D:\Photos
python scripts/photo_migration.py

# Copy instead of move, with verbose console output
python scripts/photo_migration.py --copy --verbose

# Provide explicit source folders and a custom destination
python scripts/photo_migration.py --sources C:\Users\You\Pictures D:\DCIM --destination D:\Backup\Photos
```

The script organizes media into `<destination>/<year>/<extension>/` and writes a
`photo_migration.log` file inside the destination for traceability.

## OneDrive photo migration to external drive (drive E:)

- Location: `scripts/onedrive_photo_migration.py`
- Purpose: Move or copy photos from OneDrive to an external drive mounted at `E:`.

### Usage

```bash
# Move photos from detected OneDrive roots to E:\Photos
python scripts/onedrive_photo_migration.py

# Copy instead of move, with verbose console output
python scripts/onedrive_photo_migration.py --copy --verbose

# Provide explicit source folders and a custom destination
python scripts/onedrive_photo_migration.py --sources C:\Users\You\OneDrive --destination E:\Backup\Photos
```

The script writes `onedrive_photo_migration.log` inside the destination for traceability.

See [STATUS.md](STATUS.md) for a summary of the current state and recommendations for next steps.
