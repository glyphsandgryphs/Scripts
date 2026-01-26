"""Rename media files in a directory to a normalized YYYY-MM-description format."""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


def _derive_description(name: str) -> str:
    stem = Path(name).stem
    no_numbers = re.sub(r"\d+", "", stem)
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", no_numbers)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized.lower() or "file"


def _derive_year_month(name: str, fallback_path: Path) -> str:
    stem = Path(name).stem
    match = re.search(r"(19|20)\d{2}[-_]?([01]\d)", stem)
    if match:
        year = match.group(0)[:4]
        month = match.group(2)
        if "01" <= month <= "12":
            return f"{year}-{month}"

    stats = fallback_path.stat()
    return dt.datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m")


def _format_new_name(path: Path) -> Tuple[str, str, str]:
    date_str = _derive_year_month(path.name, path)
    description = _derive_description(path.name)
    suffix = path.suffix.lower()
    base = f"{date_str}-{description}"
    return base, suffix, f"{base}{suffix}"


def rename_files(directory: Path, dry_run: bool = False) -> List[Tuple[Path, Path]]:
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    renames: List[Tuple[Path, Path]] = []
    for entry in directory.iterdir():
        if not entry.is_file():
            continue

        base, suffix, candidate_name = _format_new_name(entry)
        target = directory / candidate_name
        counter = 1
        while target.exists() and target != entry:
            target = directory / f"{base}-{counter}{suffix}"
            counter += 1

        renames.append((entry, target))
        if not dry_run and target != entry:
            entry.rename(target)
    return renames


def _parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rename media files in a directory to the format "
            "YYYY-MM-description.ext based on file modified time."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Directory containing files to rename (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned renames without applying changes",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = _parse_args(argv)
    renames = rename_files(args.path, dry_run=args.dry_run)

    for src, dest in renames:
        if args.dry_run:
            print(f"Would rename {src.name} -> {dest.name}")
        else:
            if src == dest:
                print(f"Leaving {src.name} unchanged")
            else:
                print(f"Renamed {src.name} -> {dest.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
