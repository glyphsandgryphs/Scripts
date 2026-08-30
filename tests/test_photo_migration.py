import logging
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest

from scripts.photo_migration import MigrationResult, destination_for, migrate_photos


def create_media_file(tmp_path: Path, name: str, year: int) -> Path:
    file_path = tmp_path / name
    file_path.write_bytes(b"data")
    dt = datetime(year, 1, 2, 12, 0, 0)
    timestamp = dt.timestamp()
    os.utime(file_path, (timestamp, timestamp))
    return file_path


def test_migrate_moves_files_into_year_and_extension(tmp_path: Path):
    source = tmp_path / "source"
    destination = tmp_path / "dest"
    source.mkdir()

    photo = create_media_file(source, "holiday.JPG", 2021)

    logger = logging.getLogger("migrate_move")
    logger.addHandler(logging.NullHandler())

    result = migrate_photos([source], destination, logger=logger)

    target = destination / "2021" / "jpg" / photo.name
    assert target.exists()
    assert not photo.exists()
    assert result == MigrationResult(
        moved=1, copied=0, skipped=0, by_extension=Counter({".jpg": 1})
    )


def test_filename_collisions_are_disambiguated(tmp_path: Path):
    source_a = tmp_path / "a"
    source_b = tmp_path / "b"
    destination = tmp_path / "dest"
    source_a.mkdir()
    source_b.mkdir()

    create_media_file(source_a, "shared.png", 2022)
    create_media_file(source_b, "shared.png", 2022)

    logger = logging.getLogger("collision")
    logger.addHandler(logging.NullHandler())

    result = migrate_photos([source_a, source_b], destination, logger=logger)

    base = destination / "2022" / "png"
    assert (base / "shared.png").exists()
    assert any(path.name.startswith("shared_") for path in base.iterdir())
    assert result.moved == 2


def test_copy_mode_preserves_source_files(tmp_path: Path):
    source = tmp_path / "src"
    destination = tmp_path / "dest"
    source.mkdir()

    photo = create_media_file(source, "keep.jpeg", 2020)

    logger = logging.getLogger("copy")
    logger.addHandler(logging.NullHandler())

    result = migrate_photos([source], destination, copy_only=True, logger=logger)

    copied_path = destination / "2020" / "jpeg" / photo.name
    assert copied_path.exists()
    assert photo.exists()
    assert result.copied == 1
    assert result.moved == 0


def test_destination_for_handles_missing_extension(tmp_path: Path):
    destination = tmp_path / "dest"
    file_without_ext = create_media_file(tmp_path, "noext", 2019)

    dest_path = destination_for(file_without_ext, destination)

    assert dest_path.parent.name == "other"
    assert dest_path.parent.parent.name == "2019"
