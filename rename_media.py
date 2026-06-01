"""Rename media files in a directory to a uniform pattern.

Usage:
    python rename_media.py /path/to/media --dry-run

The new file names follow the pattern ``YYYY-MM-description.ext`` where
``YYYY`` and ``MM`` come from the file's modification time and
``description`` is derived from the original filename with numbers
removed. Existing files are never overwritten; a numeric suffix is
appended when needed to avoid collisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import argparse
import os
import re
from pathlib import Path
from typing import Iterable, List, Tuple


@dataclass
class RenamePlan:
    """Represents a planned rename operation."""

    source: Path
    target: Path


_DIGIT_PATTERN = re.compile(r"\d+")
_NON_ALNUM_PATTERN = re.compile(r"[^A-Za-z0-9]+")


def _normalize_description(name: str) -> str:
    """Return a sanitized description from a filename stem.

    Numbers are removed and remaining characters are collapsed into
    hyphen-separated segments. Returns "file" when the name contains no
    letters after normalization.
    """

    without_digits = _DIGIT_PATTERN.sub("", name)
    cleaned = _NON_ALNUM_PATTERN.sub("-", without_digits).strip("-")
    normalized = cleaned.lower() or "file"
    return normalized


def _build_target_name(path: Path) -> str:
    """Build the target filename (without directory) for ``path``."""

    timestamp = datetime.fromtimestamp(path.stat().st_mtime)
    prefix = timestamp.strftime("%Y-%m")
    description = _normalize_description(path.stem)
    return f"{prefix}-{description}{path.suffix}"


def _resolve_target(path: Path, directory: Path, reserved: set[str]) -> Path:
    """Return a collision-free target path inside ``directory``."""

    base_name = _build_target_name(path)
    candidate = directory / base_name
    counter = 1

    while (
        (candidate.exists() and candidate.resolve() != path.resolve())
        or candidate.name in reserved
    ):
        candidate = directory / f"{Path(base_name).stem}-{counter}{path.suffix}"
        counter += 1

    return candidate


def plan_renames(directory: Path) -> List[RenamePlan]:
    """Create rename plans for all files directly in ``directory``."""

    if not directory.is_dir():
        raise NotADirectoryError(directory)

    plans: List[RenamePlan] = []
    reserved: set[str] = set()

    for entry in sorted(directory.iterdir(), key=lambda p: p.name):
        if not entry.is_file():
            continue
        target = _resolve_target(entry, directory, reserved)
        reserved.add(target.name)
        if target != entry:
            plans.append(RenamePlan(source=entry, target=target))

    return plans


def apply_plans(plans: Iterable[RenamePlan], dry_run: bool = False) -> List[Tuple[Path, Path]]:
    """Apply rename plans and return a list of executed operations."""

    operations: List[Tuple[Path, Path]] = []
    for plan in plans:
        operations.append((plan.source, plan.target))
        if not dry_run:
            plan.source.rename(plan.target)
    return operations


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rename media files in a directory")
    parser.add_argument("directory", type=Path, help="Directory containing media files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned renames without applying changes",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        plans = plan_renames(args.directory)
    except NotADirectoryError:
        print(f"{args.directory} is not a directory", file=os.sys.stderr)
        return 2

    operations = apply_plans(plans, dry_run=args.dry_run)

    if not operations:
        print("No files to rename.")
        return 0

    for source, target in operations:
        action = "DRY RUN" if args.dry_run else "RENAMED"
        print(f"{action}: {source.name} -> {target.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
