import os
import time
from pathlib import Path

import rename_media


def _touch_with_time(path: Path, year: int, month: int, day: int):
    path.touch()
    timestamp = time.mktime((year, month, day, 12, 0, 0, 0, 1, -1))
    os.utime(path, (timestamp, timestamp))


def test_derive_description_removes_numbers_and_normalizes():
    assert rename_media._derive_description("IMG_20220101_Beach123.JPG") == "img-beach"
    assert rename_media._derive_description("1234-__--!!.png") == "file"


def test_rename_files_basic(tmp_path: Path):
    file_path = tmp_path / "IMG_20220101_beach.jpg"
    _touch_with_time(file_path, 2022, 3, 15)

    renames = rename_media.rename_files(tmp_path)

    assert renames[0][0] == file_path
    expected = tmp_path / "2022-03-img-beach.jpg"
    assert renames[0][1] == expected
    assert expected.exists()


def test_rename_files_handles_collisions(tmp_path: Path):
    first = tmp_path / "photo1.jpg"
    second = tmp_path / "photo2.jpg"
    for f in (first, second):
        _touch_with_time(f, 2021, 6, 1)

    renames = rename_media.rename_files(tmp_path)

    renamed_targets = {new.name for _, new in renames}
    assert "2021-06-photo.jpg" in renamed_targets
    assert "2021-06-photo-1.jpg" in renamed_targets


def test_dry_run_does_not_rename(tmp_path: Path):
    file_path = tmp_path / "202304vacation.png"
    _touch_with_time(file_path, 2023, 4, 2)

    renames = rename_media.rename_files(tmp_path, dry_run=True)

    assert renames[0][0] == file_path
    assert renames[0][1].name == "2023-04-vacation.png"
    assert (tmp_path / "202304vacation.png").exists()
