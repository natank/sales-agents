"""Unit tests for src/agents_def.py — pure-logic pieces (no live API calls)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from agents_def import parse_picker_output


class TestParsePickerOutput:
    def test_parses_well_formed_output(self):
        raw = "Best Email: The Concise\nReasoning: Buyers value efficiency here."
        chosen, reasoning = parse_picker_output(raw)
        assert chosen == "The Concise"
        assert reasoning == "Buyers value efficiency here."

    def test_case_insensitive_labels(self):
        raw = "BEST EMAIL: The Witty\nREASONING: Humor lands with this audience."
        chosen, reasoning = parse_picker_output(raw)
        assert chosen == "The Witty"
        assert reasoning == "Humor lands with this audience."

    def test_missing_reasoning_falls_back_to_full_output(self):
        raw = "Best Email: The Professional"
        chosen, reasoning = parse_picker_output(raw)
        assert chosen == "The Professional"
        assert reasoning == raw

    def test_no_best_email_line_raises(self):
        with pytest.raises(RuntimeError, match="Could not parse"):
            parse_picker_output("I like all three equally.")

    def test_strips_surrounding_whitespace(self):
        raw = "  \nBest Email: The Concise\nReasoning: Efficient.\n  "
        chosen, reasoning = parse_picker_output(raw)
        assert chosen == "The Concise"
        assert reasoning == "Efficient."
