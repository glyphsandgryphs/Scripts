import logging
from pathlib import Path

import pytest

from scripts.apply_structure import (
    DEFAULT_CATEGORY_MAP,
    apply_rules,
    determine_category,
    sanitize_stem,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("My Report FINAL", "my_report_final"),
        ("   Spaces   and---Chars  ", "spaces_and---chars"),
        ("äccêntß", "accent"),
        ("", "unnamed"),
    ],
)
def test_sanitize_stem_normalizes_names(raw: str, expected: str) -> None:
    assert sanitize_stem(raw) == expected


def test_determine_category_prefers_known_extension(tmp_path: Path) -> None:
    file_path = tmp_path / "example.csv"
    file_path.write_text("data")
    assert determine_category(file_path, DEFAULT_CATEGORY_MAP) == "02_Data"


def test_apply_rules_moves_and_renames_files(tmp_path: Path) -> None:
    messy_name = tmp_path / "Docs" / "My Report (Final).PDF"
    messy_name.parent.mkdir(parents=True)
    messy_name.write_text("sample")
    stray = tmp_path / "photo 1.JPG"
    stray.write_text("binary")

    logger = logging.getLogger("test")
    logger.addHandler(logging.NullHandler())

    plan = apply_rules(tmp_path, logger, DEFAULT_CATEGORY_MAP, dry_run=False)

    documents_dir = tmp_path / "01_Documents"
    images_dir = tmp_path / "04_Images"

    moved_docs = list(documents_dir.glob("*.pdf"))
    moved_images = list(images_dir.glob("*.jpg"))

    assert moved_docs and moved_docs[0].name == "my_report_final.pdf"
    assert moved_images and moved_images[0].name == "photo_1.jpg"
    assert plan.moved["01_Documents"] == 1
    assert plan.moved["04_Images"] == 1
    assert plan.skipped == 0
