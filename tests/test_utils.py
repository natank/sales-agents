"""Unit tests for src/utils.py — validation and formatting helpers."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from utils import (
    format_email_output,
    format_picker_output,
    validate_prospect_input,
)


class TestValidateProspectInput:
    def test_valid_input_returns_true(self):
        assert (
            validate_prospect_input("Acme", "Finance", "Manual work", "Automate it")
            is True
        )

    def test_missing_field_raises(self):
        with pytest.raises(ValueError, match="company"):
            validate_prospect_input("", "Finance", "Manual work", "Automate it")

    def test_blank_field_raises(self):
        with pytest.raises(ValueError, match="pain_point"):
            validate_prospect_input("Acme", "Finance", "   ", "Automate it")

    def test_multiple_missing_fields_listed(self):
        with pytest.raises(ValueError) as exc_info:
            validate_prospect_input("", "", "Manual work", "Automate it")
        assert "company" in str(exc_info.value)
        assert "industry" in str(exc_info.value)


class TestFormatEmailOutput:
    def test_includes_agent_name_and_email_text(self):
        output = format_email_output("professional", "Subject: Hi\n\nBody text")
        assert "The Professional" in output
        assert "Subject: Hi" in output
        assert "Body text" in output

    def test_unknown_agent_key_falls_back_to_key(self):
        output = format_email_output("mystery", "some text")
        assert "mystery" in output


class TestFormatPickerOutput:
    def test_includes_chosen_agent_and_reasoning(self):
        output = format_picker_output("The Concise", "Buyers value efficiency.")
        assert "The Concise" in output
        assert "Buyers value efficiency." in output

    def test_handles_missing_chosen_agent(self):
        output = format_picker_output(None, "picker failed")
        assert "unavailable" in output.lower()
        assert "picker failed" in output
