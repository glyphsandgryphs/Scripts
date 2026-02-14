# Scripts Repository

This repository contains utility scripts for file organization, media migration, and a small testable sample CLI.

## Included scripts

- `scripts/sample_tool.py`: sample command-line tool with argument parsing and structured logs.
- `scripts/organize_files.py`: organizes files into extension-based folders.
- `scripts/photo_migration.py`: moves/copies photos to a destination organized by year and extension.
- `scripts/onedrive_photo_migration.py`: moves/copies OneDrive photos to an external destination.
- `sample_script.py`: simple numeric summarizer used as a testing example.

## Install dependencies

This project uses `pytest` for tests.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the sample script

```bash
python sample_script.py 1 2 3 4.5
```

Example output:

```text
Count: 4
Total: 10.50
Average: 2.62
```

## Run tests (CI-friendly)

Use `pytest` in non-interactive mode so CI can fail fast on test failures:

```bash
python -m pytest -q
```

Run only the sample script tests:

```bash
python -m pytest -q tests/test_sample_script.py
```

These tests validate the sample script's core behavior (summary calculations and CLI behavior), including invalid input handling.

## Additional documentation

- [`docs/scripts.md`](docs/scripts.md)
- [`STATUS.md`](STATUS.md)
