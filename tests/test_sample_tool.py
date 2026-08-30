import subprocess
import sys
from pathlib import Path

from scripts import sample_tool


def test_positive_int_accepts_positive_values() -> None:
    assert sample_tool.positive_int("3") == 3


def test_positive_int_rejects_non_positive_values() -> None:
    try:
        sample_tool.positive_int("0")
    except Exception as exc:
        assert "positive integer" in str(exc)
    else:
        raise AssertionError("Expected an argparse validation error")


def test_format_greetings_uppercase() -> None:
    assert sample_tool.format_greetings("Ada", 2, uppercase=True) == [
        "HELLO, ADA!",
        "HELLO, ADA!",
    ]


def test_cli_writes_log_file(tmp_path: Path) -> None:
    log_path = tmp_path / "sample.log"

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/sample_tool.py",
            "--name",
            "Ada",
            "--count",
            "2",
            "--uppercase",
            "--log-file",
            str(log_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert log_path.exists()
    log_contents = log_path.read_text(encoding="utf-8")
    assert "HELLO, ADA!" in log_contents
