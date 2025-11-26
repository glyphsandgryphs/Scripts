# Scripts

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
