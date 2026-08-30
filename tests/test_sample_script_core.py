"""Basic tests for sample_script core behavior."""

import sample_script


def test_summarize_numbers_core_behavior():
    summary = sample_script.summarize_numbers([2, 4, 6])

    assert summary.count == 3
    assert summary.total == 12.0
    assert summary.average == 4.0
