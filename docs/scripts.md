# Scripts

This repository includes a sample command-line tool that demonstrates argument parsing and logging.

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
