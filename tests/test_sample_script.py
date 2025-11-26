import subprocess
import sys

import sample_script


def test_summarize_numbers_basic():
    summary = sample_script.summarize_numbers([1, 2, 3, 4])
    assert summary == {"count": 4, "total": 10.0, "average": 2.5}


def test_summarize_numbers_empty():
    summary = sample_script.summarize_numbers([])
    assert summary == {"count": 0, "total": 0.0, "average": 0.0}


def test_cli_output():
    completed = subprocess.run(
        [sys.executable, "sample_script.py", "5", "15"], capture_output=True, check=True, text=True
    )
    output = completed.stdout.strip()
    assert "Count: 2" in output
    assert "Total: 20.0" in output
    assert "Average: 10.00" in output
