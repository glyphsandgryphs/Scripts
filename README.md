# Scripts

This repository contains runnable utility scripts with accompanying tests. Start with `scripts/sample_tool.py`, a command-line example that shows how to parse arguments and emit structured logs. See [`docs/scripts.md`](docs/scripts.md) for usage details.
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
# Included utilities

- `sample_script.py`: Summarize numeric input (count, total, average) with CLI validation.
- `scripts/sample_tool.py`: Demonstrate argument parsing and structured logging.
- `scripts/organize_files.py`: Organize files inside a target directory into extension-named folders with collision handling.

See [STATUS.md](STATUS.md) for a summary of the current state and recommendations for next steps.
