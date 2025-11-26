"""Simple sample script that summarizes numeric input."""
from __future__ import annotations

from typing import Iterable, List


def summarize_numbers(values: Iterable[float]) -> dict:
    """Return count, total, and average for an iterable of numbers.

    The function is intentionally small to demonstrate testability for the sample script.
    """
    numbers: List[float] = [float(v) for v in values]
    count = len(numbers)
    total = sum(numbers)
    average = total / count if count else 0.0
    return {"count": count, "total": total, "average": average}


def _format_summary(summary: dict) -> str:
    return (
        f"Count: {summary['count']}\n"
        f"Total: {summary['total']}\n"
        f"Average: {summary['average']:.2f}"
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize numeric input")
    parser.add_argument(
        "numbers", type=float, nargs="*", help="Numbers to summarize", default=[]
    )
    args = parser.parse_args()

    summary = summarize_numbers(args.numbers)
    print(_format_summary(summary))


if __name__ == "__main__":
    main()
