# Scripts

This repository includes a few small, runnable utilities with accompanying tests.

## `sample_script.py`

- Summarizes numeric input (count, total, average).
- Emits a helpful error message for invalid numbers.

### Usage

```
python sample_script.py 1 2 3 4.5
```

## `scripts/sample_tool.py`

- Prints a greeting message the specified number of times.
- Supports a `--verbose` flag to enable debug logging.
- Raises an error if the requested count is less than one.

### Usage

```
python scripts/sample_tool.py --name Ada --count 3 --verbose
```

Arguments:
- `--name`: Name to include in the greeting (default: `World`).
- `--count`: Number of greetings to print (default: `1`).
- `--verbose`: Enable debug logging.

## `scripts/organize_files.py`

- Organizes files in a target directory into subfolders based on extension.
- Names files with numeric suffixes when collisions are detected.

### Usage

```
python scripts/organize_files.py /path/to/dir --verbose
```

Arguments:
- `DIRECTORY`: Path to the folder containing files to organize.
- `--verbose`: Enable debug-level logging to observe each move.
