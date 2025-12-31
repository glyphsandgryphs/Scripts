import os
from datetime import datetime
from pathlib import Path

import pytest

import rename_media


def set_mtime(path: Path, dt: datetime) -> None:
    ts = dt.timestamp()
    os.utime(path, (ts, ts))


def test_plan_renames_creates_expected_names(tmp_path: Path) -> None:
    first = tmp_path / "IMG_1234_beach.jpg"
    second = tmp_path / "20230101-party-night.png"
    third = tmp_path / "README.txt"  # ensure non-media-like names still processed

    for file in (first, second, third):
        file.write_text("data")

    set_mtime(first, datetime(2024, 7, 4, 12, 0, 0))
    set_mtime(second, datetime(2023, 1, 1, 8, 30, 0))
    set_mtime(third, datetime(2022, 12, 25, 23, 59, 59))

    plans = rename_media.plan_renames(tmp_path)
    mapping = {plan.source.name: plan.target.name for plan in plans}

    assert mapping["IMG_1234_beach.jpg"] == "2024-07-img-beach.jpg"
    assert mapping["20230101-party-night.png"] == "2023-01-party-night.png"
    assert mapping["README.txt"] == "2022-12-readme.txt"


def test_apply_plans_renames_files(tmp_path: Path) -> None:
    file_path = tmp_path / "photo001-sunset.JPG"
    file_path.write_text("content")
    set_mtime(file_path, datetime(2020, 2, 2, 18, 0, 0))

    plans = rename_media.plan_renames(tmp_path)
    operations = rename_media.apply_plans(plans)

    assert (tmp_path / "2020-02-photo-sunset.JPG").exists()
    assert not file_path.exists()
    assert operations == [(plan.source, plan.target) for plan in plans]


def test_collision_adds_suffix(tmp_path: Path) -> None:
    original = tmp_path / "video1.mov"
    duplicate = tmp_path / "video2.mov"

    original.write_text("a")
    duplicate.write_text("b")

    set_mtime(original, datetime(2022, 5, 1, 10, 0, 0))
    set_mtime(duplicate, datetime(2022, 5, 1, 10, 0, 0))

    plans = rename_media.plan_renames(tmp_path)
    targets = {plan.target.name for plan in plans}

    assert "2022-05-video.mov" in targets
    assert any(name.startswith("2022-05-video-") for name in targets)


def test_dry_run_does_not_change_files(tmp_path: Path) -> None:
    file_path = tmp_path / "notes123.txt"
    file_path.write_text("keep")
    set_mtime(file_path, datetime(2021, 11, 11, 11, 11, 11))

    plans = rename_media.plan_renames(tmp_path)
    rename_media.apply_plans(plans, dry_run=True)

    assert file_path.exists()
    assert (tmp_path / "2021-11-notes.txt").exists() is False
