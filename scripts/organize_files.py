"""File organizer utility.

This script organizes files in a target directory by grouping them into
subfolders based on their file extensions. It is designed to be modular,
with reusable functions, logging, and error handling to make future
enhancements straightforward.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Dict, Iterable


def configure_logger(verbose: bool = False) -> logging.Logger:
    """Create and configure a logger for the organizer.

    The logger writes to stdout and can be switched between INFO and DEBUG
    verbosity. Handlers are only added once to avoid duplicate log output when
    the module is reused.
    """

    logger = logging.getLogger("file_organizer")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False
    return logger


def determine_category(path: Path) -> str:
    """Return a folder name for the file based on its suffix.

    Files with no suffix are grouped under "no_extension" to keep the target
    directory organized.
    """

    suffix = path.suffix.lower().lstrip(".")
    return suffix if suffix else "no_extension"


def ensure_target_directory(target: Path) -> Path:
    """Validate that the provided path exists and is a directory."""

    if not target.exists():
        raise FileNotFoundError(f"Directory not found: {target}")
    if not target.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {target}")
    return target


def iter_files(directory: Path) -> Iterable[Path]:
    """Yield files in the given directory, skipping subdirectories."""

    for entry in directory.iterdir():
        if entry.is_file():
            yield entry


def move_file_to_category(file_path: Path, category_dir: Path, logger: logging.Logger) -> None:
    """Move a file into its category directory with collision avoidance."""

    category_dir.mkdir(parents=True, exist_ok=True)
    destination = category_dir / file_path.name
    counter = 1
    while destination.exists():
        destination = category_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
        counter += 1

    try:
        file_path.rename(destination)
        logger.info("Moved %s -> %s", file_path, destination)
    except OSError as error:
        logger.error("Failed to move %s: %s", file_path, error)
        raise


def organize_files(target_directory: Path, logger: logging.Logger) -> Dict[str, int]:
    """Organize files in ``target_directory`` by extension.

    Returns a dictionary mapping category names to the number of files moved.
    """

    counts: Dict[str, int] = {}
    for file_path in iter_files(target_directory):
        category = determine_category(file_path)
        category_dir = target_directory / category
        move_file_to_category(file_path, category_dir, logger)
        counts[category] = counts.get(category, 0) + 1

    if not counts:
        logger.info("No files to organize in %s", target_directory)
    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Organize files in a directory by grouping them into subfolders "
            "named after their file extensions."
        )
    )
    parser.add_argument(
        "directory",
        metavar="DIRECTORY",
        type=Path,
        help="Path to the directory containing files to organize",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = configure_logger(verbose=args.verbose)
    try:
        target_dir = ensure_target_directory(args.directory)
        logger.debug("Target directory resolved to %s", target_dir)
        organize_files(target_dir, logger)
    except Exception as error:  # noqa: BLE001
        logger.error("Organization failed: %s", error)


if __name__ == "__main__":
    main()
