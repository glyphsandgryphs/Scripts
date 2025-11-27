# Scripts

This repository contains runnable utility scripts. Start with `scripts/sample_tool.py`, a command-line example that shows how to parse arguments, emit structured logs, and optionally mirror output to a log file or uppercase the generated greetings. See [`docs/scripts.md`](docs/scripts.md) for usage details and invocation examples.
This repository contains runnable utility scripts. Start with `scripts/sample_tool.py`, a command-line example that shows how to parse arguments and emit structured logs. See [`docs/scripts.md`](docs/scripts.md) for usage details.
A small sample script for summarizing numeric input and accompanying tests powered by `pytest`.

## Sample script

Run the script directly to see summary statistics (count, total, average):

```bash
python sample_script.py 1 2 3 4.5
```

Expected output:

```
Count: 4
Total: 10.50
Average: 2.62
```

## Installation

Create a virtual environment and install dependencies from `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running tests (CI-friendly)

Execute the full test suite with `pytest` (suitable for CI pipelines):

```bash
python -m pytest
```

To run a specific test module:

```bash
python -m pytest tests/test_sample_script.py
```

The test suite covers both the library function and the CLI output for the sample script, including helpful error handling for invalid numeric input.
# Scripts Repository

This repository contains utility scripts and documentation.

## File organizer
- Location: `scripts/organize_files.py`
- Purpose: Organize files inside a target directory into subfolders named after their file extensions.
- Usage: `python scripts/organize_files.py <directory> [--verbose]`

See [STATUS.md](STATUS.md) for a summary of the current state and recommendations for next steps.

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
