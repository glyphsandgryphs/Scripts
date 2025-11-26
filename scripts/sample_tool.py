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

    configure_logging(args.verbose)
    logging.debug("Parsed arguments: %s", args)

    greetings = generate_greetings(args.name, args.count)
    for greeting in greetings:
        logging.info(greeting)


if __name__ == "__main__":
    main()
