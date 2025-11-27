"""Cross-platform folder organizer and renamer.

This utility applies a consistent folder structure and filename convention
across multiple target roots (local PCs, synced cloud folders, external
drives, etc.). Files are routed into category folders based on extension,
renamed with a predictable pattern, and created directories are ensured on
each run.
"""
from __future__ import annotations

import argparse
import logging
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping

# Default category mapping organized by extension.
DEFAULT_CATEGORY_MAP: Mapping[str, List[str]] = {
    "01_Documents": [
        "pdf",
        "doc",
        "docx",
        "txt",
        "md",
        "rtf",
        "odt",
        "ppt",
        "pptx",
    ],
    "02_Data": ["csv", "xlsx", "xls", "json", "xml", "parquet"],
    "03_Code": ["py", "js", "ts", "html", "css", "yaml", "yml", "json5", "sh", "ps1", "bat"],
    "04_Images": ["jpg", "jpeg", "png", "gif", "svg", "heic", "bmp", "tif", "tiff", "webp"],
    "05_Audio": ["mp3", "wav", "flac", "aac", "ogg", "m4a"],
    "06_Video": ["mp4", "mov", "avi", "mkv", "webm"],
    "07_Archives": ["zip", "tar", "gz", "rar", "7z"],
    "08_Backups": ["bak", "tmp"],
    "99_Misc": [],
}

SKELETON_FOLDERS: List[str] = [
    "00_Inbox",
    "10_Projects",
    "20_Archive",
    "30_Reference",
    "40_Exports",
]

INVALID_CHARACTERS = re.compile(r"[^A-Za-z0-9._-]+")
MULTIPLE_SEPARATORS = re.compile(r"_{2,}")


@dataclass
class PlanResult:
    """Summary of operations performed for a root directory."""

    moved: Dict[str, int]
    skipped: int


def configure_logger(verbose: bool = False) -> logging.Logger:
    """Configure a module-scoped logger."""

    logger = logging.getLogger("structure_applier")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False
    return logger


def sanitize_stem(stem: str) -> str:
    """Normalize a filename stem into a predictable, portable format."""

    normalized = unicodedata.normalize("NFKD", stem)
    ascii_only = normalized.encode("ascii", "ignore").decode()
    cleaned = INVALID_CHARACTERS.sub("_", ascii_only.strip().lower())
    cleaned = MULTIPLE_SEPARATORS.sub("_", cleaned).strip("._")
    if not cleaned:
        return "unnamed"
    if len(cleaned) > 80:
        cleaned = cleaned[:80].rstrip("._")
    return cleaned


def determine_category(path: Path, category_map: Mapping[str, List[str]]) -> str:
    suffix = path.suffix.lower().lstrip(".")
    for category, extensions in category_map.items():
        if suffix in extensions:
            return category
    return "99_Misc"


def ensure_directories(root: Path, category_map: Mapping[str, List[str]]) -> None:
    for folder in list(category_map.keys()) + SKELETON_FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)


def iter_files(root: Path) -> Iterable[Path]:
    """Yield files recursively while skipping generated category folders."""

    for path in list(root.rglob("*")):
        if path.is_dir():
            continue
        yield path


def move_file(file_path: Path, destination_dir: Path, logger: logging.Logger, dry_run: bool = False) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    sanitized = sanitize_stem(file_path.stem)
    destination = destination_dir / f"{sanitized}{file_path.suffix.lower()}"
    counter = 1
    while destination.exists() and destination != file_path:
        destination = destination_dir / f"{sanitized}_{counter}{file_path.suffix.lower()}"
        counter += 1
    if dry_run:
        logger.info("[dry-run] Would move %s -> %s", file_path, destination)
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    file_path.rename(destination)
    logger.info("Moved %s -> %s", file_path, destination)
    return destination


def apply_rules(root: Path, logger: logging.Logger, category_map: Mapping[str, List[str]], dry_run: bool = False) -> PlanResult:
    ensure_directories(root, category_map)
    moved: Dict[str, int] = {}
    skipped = 0

    for file_path in iter_files(root):
        # Skip files already inside a managed category to avoid churn
        if file_path.parent.name in category_map:
            logger.debug("Skipping already categorized file %s", file_path)
            skipped += 1
            continue

        category = determine_category(file_path, category_map)
        destination_dir = root / category
        move_file(file_path, destination_dir, logger, dry_run=dry_run)
        moved[category] = moved.get(category, 0) + 1

    if not moved:
        logger.info("No files required changes under %s", root)
    return PlanResult(moved=moved, skipped=skipped)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Apply folder structure and naming conventions to multiple roots. "
            "Useful for local PCs, synced cloud folders, and external drives."
        )
    )
    parser.add_argument(
        "roots",
        metavar="ROOT",
        type=Path,
        nargs="+",
        help="One or more root directories to organize",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving or renaming files",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = configure_logger(verbose=args.verbose)

    for root in args.roots:
        logger.info("Processing root: %s", root)
        try:
            plan = apply_rules(root, logger, DEFAULT_CATEGORY_MAP, dry_run=args.dry_run)
            logger.info("Summary for %s: %s", root, plan)
        except Exception as error:  # noqa: BLE001
            logger.error("Failed to organize %s: %s", root, error)


if __name__ == "__main__":
    main()
