import os
from pathlib import Path

import pytest

from scripts.onedrive_photo_migration import (
    default_onedrive_sources,
    resolve_sources,
)


def test_default_onedrive_sources_prefers_env_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    consumer = tmp_path / "OneDriveConsumer"
    commercial = tmp_path / "OneDriveBusiness"
    consumer.mkdir()
    commercial.mkdir()

    monkeypatch.setenv("OneDriveConsumer", str(consumer))
    monkeypatch.setenv("OneDriveCommercial", str(commercial))
    monkeypatch.delenv("OneDrive", raising=False)
    monkeypatch.delenv("USERPROFILE", raising=False)
    monkeypatch.delenv("HOME", raising=False)

    sources = default_onedrive_sources(os.environ)

    assert sources == [consumer, commercial]


def test_default_onedrive_sources_falls_back_to_userprofile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    home = tmp_path / "user"
    (home / "OneDrive").mkdir(parents=True)

    monkeypatch.delenv("OneDrive", raising=False)
    monkeypatch.delenv("OneDriveConsumer", raising=False)
    monkeypatch.delenv("OneDriveCommercial", raising=False)
    monkeypatch.setenv("USERPROFILE", str(home))

    sources = default_onedrive_sources(os.environ)

    assert sources == [home / "OneDrive"]


def test_resolve_sources_uses_cli_sources(tmp_path: Path):
    source = tmp_path / "custom"
    sources = resolve_sources([str(source)], os.environ)

    assert sources == [source]
