"""Utility to move or copy photos to a microSD card (drive D by default).

The script scans source folders for common photo extensions and migrates them
into a destination structured by year and extension. A log file is written to
help trace all file moves or copies.
"""
from __future__ import annotations

import argparse
import logging
import shutil
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Sequence, Set

DEFAULT_EXTENSIONS: Set[str] = {
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".gif",
    ".bmp",
    ".tiff",
}

DEFAULT_SOURCES: Sequence[str] = (
    r"C:\\Users\\Public\\Pictures",
    r"C:\\Users\\Public\\DCIM",
)

DEFAULT_DESTINATION = Path(r"D:\\Photos")


@dataclass
class MigrationResult:
    moved: int
    copied: int
    skipped: int
    by_extension: Counter[str]


class MigrationError(Exception):
    """Custom exception for migration failures."""


def iter_media_files(sources: Sequence[Path], extensions: Set[str]) -> Iterator[Path]:
    """Yield all files under the given sources that match allowed extensions.

    Args:
        sources: Directories to search.
        extensions: Lowercase extensions (including the leading period).
    """

    for root in sources:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in extensions:
                yield path


def ensure_unique_path(dest_path: Path) -> Path:
    """Return a non-colliding path by appending a numeric suffix if needed."""

    candidate = dest_path
    counter = 1
    while candidate.exists():
        candidate = dest_path.with_name(f"{dest_path.stem}_{counter}{dest_path.suffix}")
        counter += 1
    return candidate


def destination_for(source: Path, destination_root: Path) -> Path:
    """Build the destination path based on year and extension."""

    try:
        year = datetime.fromtimestamp(source.stat().st_mtime).year
    except OSError as exc:
        raise MigrationError(f"Unable to read timestamp for {source}") from exc

    extension_folder = source.suffix.lower().lstrip(".") or "other"
    return destination_root / str(year) / extension_folder / source.name


def migrate_photos(
    sources: Sequence[Path],
    destination_root: Path,
    *,
    copy_only: bool = False,
    dry_run: bool = False,
    extensions: Set[str] | None = None,
    logger: logging.Logger | None = None,
) -> MigrationResult:
    """Move or copy photos from sources into the destination root.

    The function preserves the original filename, creating a unique variant when
    collisions are detected. Files are organized into `<destination>/<year>/<extension>`.
    """

    exts = {ext.lower() for ext in (extensions or DEFAULT_EXTENSIONS)}
    destination_root.mkdir(parents=True, exist_ok=True)

    log = logger or logging.getLogger(__name__)

    moved = copied = skipped = 0
    by_extension: Counter[str] = Counter()

    for file_path in iter_media_files(sources, exts):
        if destination_root in file_path.parents:
            skipped += 1
            log.debug("Skipping %s because it is already under destination", file_path)
            continue

        dest_path = ensure_unique_path(destination_for(file_path, destination_root))
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        action = shutil.copy2 if copy_only else shutil.move
        verb = "Copying" if copy_only else "Moving"

        log.info("%s %s -> %s", verb, file_path, dest_path)
        if not dry_run:
            action(file_path, dest_path)

        if copy_only:
            copied += 1
        else:
            moved += 1
        by_extension[file_path.suffix.lower()] += 1

    return MigrationResult(moved=moved, copied=copied, skipped=skipped, by_extension=by_extension)


def setup_logging(log_path: Path, verbose: bool = False) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("photo_migration")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(console_handler)

    return logger


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Move or copy photos to drive D:.")
    parser.add_argument(
        "--sources",
        nargs="+",
        default=list(DEFAULT_SOURCES),
        help="One or more source directories to scan for photos.",
    )
    parser.add_argument(
        "--destination",
        default=str(DEFAULT_DESTINATION),
        help="Destination root (defaults to D:\\Photos).",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of moving them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List actions without performing any file operations.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging to the console.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> MigrationResult:
    args = parse_args(argv)
    destination_root = Path(args.destination)
    sources = [Path(src) for src in args.sources]

    log_file = destination_root / "photo_migration.log"
    logger = setup_logging(log_file, verbose=args.verbose)

    logger.info("Scanning sources: %s", ", ".join(str(src) for src in sources))
    result = migrate_photos(
        sources,
        destination_root,
        copy_only=args.copy,
        dry_run=args.dry_run,
        extensions=DEFAULT_EXTENSIONS,
        logger=logger,
    )

    logger.info(
        "Completed: moved=%s copied=%s skipped=%s", result.moved, result.copied, result.skipped
    )
    for ext, count in sorted(result.by_extension.items()):
        logger.info("%s: %s files", ext, count)

    return result


if __name__ == "__main__":
    main()
