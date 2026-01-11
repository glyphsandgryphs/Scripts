"""Move or copy photos from OneDrive to an external drive (E by default)."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable, List, Mapping, Sequence

from scripts.photo_migration import DEFAULT_EXTENSIONS, migrate_photos, setup_logging

DEFAULT_DESTINATION = Path(r"E:\Photos")


def default_onedrive_sources(env: Mapping[str, str] | None = None) -> List[Path]:
    env = env or os.environ
    candidates: List[Path] = []

    for key in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial"):
        value = env.get(key)
        if value:
            candidates.append(Path(value))

    home = env.get("USERPROFILE") or env.get("HOME")
    if home:
        candidates.append(Path(home) / "OneDrive")

    unique: List[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if path.exists():
            unique.append(path)

    return unique


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move or copy photos from OneDrive to drive E:."
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        default=None,
        help="Optional OneDrive source folders. Defaults to OneDrive roots if omitted.",
    )
    parser.add_argument(
        "--destination",
        default=str(DEFAULT_DESTINATION),
        help="Destination root (defaults to E:\\Photos).",
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


def resolve_sources(cli_sources: Iterable[str] | None, env: Mapping[str, str]) -> List[Path]:
    if cli_sources:
        return [Path(src) for src in cli_sources]

    return default_onedrive_sources(env)


def main(argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    args = parse_args(argv)
    runtime_env = env or os.environ
    sources = resolve_sources(args.sources, runtime_env)

    if not sources:
        raise SystemExit(
            "No OneDrive folders were found. Provide --sources to specify the folders to scan."
        )

    destination_root = Path(args.destination)
    log_file = destination_root / "onedrive_photo_migration.log"
    logger = setup_logging(log_file, verbose=args.verbose)

    logger.info("Scanning OneDrive sources: %s", ", ".join(str(src) for src in sources))
    result = migrate_photos(
        sources,
        destination_root,
        copy_only=args.copy,
        dry_run=args.dry_run,
        extensions=DEFAULT_EXTENSIONS,
        logger=logger,
    )

    logger.info(
        "Completed: moved=%s copied=%s skipped=%s",
        result.moved,
        result.copied,
        result.skipped,
    )
    for ext, count in sorted(result.by_extension.items()):
        logger.info("%s: %s files", ext, count)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
