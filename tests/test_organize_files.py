"""Tests for the file organizer utility."""
from __future__ import annotations

import logging
from pathlib import Path

import pytest

from scripts.organize_files import (
    configure_logger,
    determine_category,
    ensure_target_directory,
    organize_files,
)


def _make_logger() -> logging.Logger:
    logger = configure_logger(verbose=True)
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    return logger


def test_determine_category_handles_missing_suffix():
    assert determine_category(Path("filename")) == "no_extension"
    assert determine_category(Path("report.TXT")) == "txt"


def test_organize_files_moves_by_extension(tmp_path: Path):
    file_txt = tmp_path / "notes.txt"
    file_png = tmp_path / "image.png"
    file_no_ext = tmp_path / "README"

    for path in (file_txt, file_png, file_no_ext):
        path.write_text("content")

    logger = _make_logger()
    counts = organize_files(tmp_path, logger)

    assert counts == {"txt": 1, "png": 1, "no_extension": 1}
    assert (tmp_path / "txt" / file_txt.name).exists()
    assert (tmp_path / "png" / file_png.name).exists()
    assert (tmp_path / "no_extension" / file_no_ext.name).exists()


def test_organize_files_renames_on_collision(tmp_path: Path):
    category_dir = tmp_path / "txt"
    existing = category_dir / "duplicate.txt"
    category_dir.mkdir()
    existing.write_text("existing")

    colliding_source = tmp_path / "duplicate.txt"
    colliding_source.write_text("new file")

    logger = _make_logger()
    counts = organize_files(tmp_path, logger)

    renamed_path = category_dir / "duplicate_1.txt"
    assert renamed_path.exists()
    assert renamed_path.read_text() == "new file"
    assert counts == {"txt": 1}


def test_ensure_target_directory_rejects_invalid_paths(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")

    with pytest.raises(FileNotFoundError):
        ensure_target_directory(tmp_path / "missing")

    with pytest.raises(NotADirectoryError):
        ensure_target_directory(file_path)
