"""Tests for Nigeria National ID validator."""

import pytest

from id_validation.validate import ValidationError
from id_validation.validate_nigeria import NigeriaValidator


@pytest.fixture
def validator() -> NigeriaValidator:
    return NigeriaValidator()


@pytest.fixture
def invalid_format_id_numbers() -> list[str]:
    return [
        "",
        "123456789",  # too short
        "342343243243244324",  # too long
        "3432dfdsf",  # non-digit
    ]


@pytest.fixture
def valid_id_numbers() -> list[str]:
    return [
        "45743234565",
        "37965436742",
        "34235768854",
    ]


class TestNigeriaValidator:
    def test_validate_accepts_valid_ids(
        self,
        validator: NigeriaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            assert validator.validate(idno), f"Expected {idno} to be valid"

    def test_validate_rejects_invalid_format(
        self,
        validator: NigeriaValidator,
        invalid_format_id_numbers: list[str],
    ) -> None:
        for idno in invalid_format_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid"

    def test_extract_data_raises_on_invalid(
        self,
        validator: NigeriaValidator,
        invalid_format_id_numbers: list[str],
    ) -> None:
        for idno in invalid_format_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_data(idno)

    def test_extract_data_valid(
        self,
        validator: NigeriaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        """Nigeria NIN doesn't encode data, so extract_data returns minimal info."""
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            # Nigeria validator returns empty dict (no encoded data)
            assert isinstance(data, dict)
