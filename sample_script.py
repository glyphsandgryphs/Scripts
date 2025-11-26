"""Simple sample script that summarizes numeric input."""
from __future__ import annotations

from dataclasses import dataclass
import sys
from typing import Iterable, List


@dataclass
class Summary:
    count: int
    total: float
    average: float


def summarize_numbers(values: Iterable[float]) -> Summary:
    """Return count, total, and average for an iterable of numbers.

    The function is intentionally small to demonstrate testability for the sample script.
    """
    numbers: List[float] = [float(v) for v in values]
    count = len(numbers)
    total = sum(numbers)
    average = total / count if count else 0.0
    return Summary(count=count, total=total, average=average)


def _format_summary(summary: Summary) -> str:
    return (
        f"Count: {summary.count}\n"
        f"Total: {summary.total:.2f}\n"
        f"Average: {summary.average:.2f}"
    )


def _parse_args(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description="Summarize numeric input")
    parser.add_argument(
        "numbers", nargs="*", help="Numbers to summarize", default=[]
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    try:
        summary = summarize_numbers(args.numbers)
    except ValueError as exc:  # pragma: no cover - exercised via CLI test
        print(f"Invalid numeric input: {exc}", file=sys.stderr)
        return 2

    print(_format_summary(summary))
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
