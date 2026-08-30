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


def test_dry_run_does_not_modify_the_root(tmp_path: Path) -> None:
    source = tmp_path / "My Report.PDF"
    source.write_text("sample")
    logger = logging.getLogger("test-dry-run")
    logger.addHandler(logging.NullHandler())

    plan = apply_rules(tmp_path, logger, DEFAULT_CATEGORY_MAP, dry_run=True)

    assert source.exists()
    assert not (tmp_path / "01_Documents").exists()
    assert not (tmp_path / "00_Inbox").exists()
    assert plan.moved == {"01_Documents": 1}


def test_nested_files_in_managed_folders_are_skipped(tmp_path: Path) -> None:
    nested = tmp_path / "10_Projects" / "client" / "notes.txt"
    nested.parent.mkdir(parents=True)
    nested.write_text("keep in project")
    logger = logging.getLogger("test-managed-folders")
    logger.addHandler(logging.NullHandler())

    plan = apply_rules(tmp_path, logger, DEFAULT_CATEGORY_MAP)

    assert nested.exists()
    assert plan.moved == {}
    assert plan.skipped == 1


def test_missing_root_is_not_created(tmp_path: Path) -> None:
    missing = tmp_path / "missing"
    logger = logging.getLogger("test-missing-root")
    logger.addHandler(logging.NullHandler())

    with pytest.raises(FileNotFoundError):
        apply_rules(missing, logger, DEFAULT_CATEGORY_MAP)

    assert not missing.exists()
