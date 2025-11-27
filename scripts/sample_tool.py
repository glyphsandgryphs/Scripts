"""Sample command-line tool with argument parsing and structured logging.

Usage examples:
    python scripts/sample_tool.py --name Ada --count 3 --verbose
    python scripts/sample_tool.py --name Ada --count 3 --log-file logs/run.log

The script prints a greeting message multiple times and demonstrates how to
control logging verbosity and output destinations from the command line.
"""
Sample command-line tool with argument parsing and structured logging.

Usage examples:
    python scripts/sample_tool.py --name Ada --count 3 --verbose

The script prints a greeting message multiple times and demonstrates
how to control logging verbosity from the command line.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import List, Sequence


def positive_int(value: str) -> int:
    """Return a validated positive integer parsed from ``value``.

    Raises ``argparse.ArgumentTypeError`` if validation fails so argparse can
    surface a helpful error to the user.
    """

    try:
        parsed = int(value)
    except ValueError as exc:  # pragma: no cover - defensive
        raise argparse.ArgumentTypeError("count must be an integer") from exc

    if parsed < 1:
        raise argparse.ArgumentTypeError("count must be a positive integer")
    return parsed
from typing import List


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sample tool demonstrating argument parsing and logging",
    )
    parser.add_argument(
        "--name",
        default="World",
        help="Name to include in the greeting message",
    )
    parser.add_argument(
        "--count",
        type=positive_int,
        default=1,
        help="Number of greetings to print (must be positive)",
    )
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Output greetings in uppercase for emphasis",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Optional file path to also write logs to",
        type=int,
        default=1,
        help="Number of greetings to print",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging for troubleshooting",
    )
    return parser


def configure_logging(verbose: bool, log_file: Path | None) -> None:
    """Configure console logging and optional file logging."""

    level = logging.DEBUG if verbose else logging.INFO
    handlers: List[logging.Handler] = [logging.StreamHandler()]

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers,
    )


def format_greetings(name: str, count: int, uppercase: bool = False) -> List[str]:
    """Generate greeting messages with optional uppercase formatting."""

    greetings = [f"Hello, {name}!" for _ in range(count)]
    if uppercase:
        return [greeting.upper() for greeting in greetings]
    return greetings


def emit_greetings(greetings: Sequence[str]) -> None:
    """Log each greeting line to the configured handlers."""

    for greeting in greetings:
        logging.info(greeting)
def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def generate_greetings(name: str, count: int) -> List[str]:
    if count < 1:
        raise ValueError("count must be a positive integer")
    return [f"Hello, {name}!" for _ in range(count)]


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    configure_logging(args.verbose, args.log_file)
    logging.debug("Parsed arguments: %s", args)

    greetings = format_greetings(args.name, args.count, uppercase=args.uppercase)
    emit_greetings(greetings)
    configure_logging(args.verbose)
    logging.debug("Parsed arguments: %s", args)

    greetings = generate_greetings(args.name, args.count)
    for greeting in greetings:
        logging.info(greeting)


if __name__ == "__main__":
    main()
