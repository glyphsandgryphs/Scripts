# Scripts

This repository includes a sample command-line tool that demonstrates argument parsing and logging, including optional uppercase output and writing logs to a file.

## `scripts/sample_tool.py`

- Prints a greeting message the specified number of times.
- Supports a `--verbose` flag to enable debug logging.
- Raises an error if the requested count is less than one.
- Accepts `--uppercase` to emphasize the greetings.
- Writes logs to both the console and an optional `--log-file` path.

### Usage

```bash
# Basic run with default settings
python scripts/sample_tool.py --name Ada --count 3

# Enable debug logging and uppercase output, also writing logs to a file
python scripts/sample_tool.py --name Ada --count 3 --verbose --uppercase --log-file logs/sample.log
```

Arguments:
- `--name`: Name to include in the greeting (default: `World`).
- `--count`: Number of greetings to print; must be positive (default: `1`).
- `--uppercase`: Output greetings in uppercase.
- `--log-file`: Path to an optional log file to mirror the console output.
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
