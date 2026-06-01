# Scripts Repository

This repository contains utility scripts plus lightweight documentation and tests.

This repository contains runnable utility scripts with accompanying tests. Start with `scripts/sample_tool.py`, a command-line example that shows how to parse arguments and emit structured logs. See [`docs/scripts.md`](docs/scripts.md) for usage details.
This repository contains runnable utility scripts. Start with `scripts/sample_tool.py`, a command-line example that shows how to parse arguments, emit structured logs, and optionally mirror output to a log file or uppercase the generated greetings. See [`docs/scripts.md`](docs/scripts.md) for usage details and invocation examples.
This repository contains runnable utility scripts. Start with `scripts/sample_tool.py`, a command-line example that shows how to parse arguments and emit structured logs. See [`docs/scripts.md`](docs/scripts.md) for usage details.
A small sample script for summarizing numeric input and accompanying tests powered by `pytest`.

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

The test suite covers both the library function and the CLI output for the sample script, including helpful error handling for invalid numeric input.
# Included utilities

- `sample_script.py`: Summarize numeric input (count, total, average) with CLI validation.
- `scripts/sample_tool.py`: Demonstrate argument parsing and structured logging.
- `scripts/organize_files.py`: Organize files inside a target directory into extension-named folders with collision handling.

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

The script writes `onedrive_photo_migration.log` inside the destination for traceability.

See [STATUS.md](STATUS.md) for a summary of the current state and recommendations for next steps.
- [`docs/scripts.md`](docs/scripts.md)
- [`STATUS.md`](STATUS.md)
