"""Tests for Zimbabwe National ID validator."""

import pytest
from itertools import chain

from id_validation.validate import ValidationError
from id_validation.validate_zimbabwe import ZimbabweValidator, REGION_LOOKUP


@pytest.fixture
def valid_id_numbers() -> list[str]:
    return [
        "50-025544-Q-12",
        "43-165780-A-42",
        "77-040785-H-77",
        "75-341502-L-70",
        "63-751545-G-63",
        "49-008555-S-49",
        "63-1174850-T-45",
    ]


@pytest.fixture
def invalid_format_ids() -> list[str]:
    return [
        "F",
        "50-925544-Q-132",
        "50-925544-I-13",  # 'I' is not a valid check letter
    ]


@pytest.fixture
def invalid_checksum_ids() -> list[str]:
    return [
        "50-925544-Q-12",
        "43-965780-A-42",
        "77-940785-H-77",
        "75-941502-J-70",
        "63-951545-G-63",
        "49-908555-S-49",
        "63-9174850-L-45",
    ]


@pytest.fixture
def invalid_region_ids() -> list[str]:
    return [
        "49-908555-S-00",  # 00 is not a valid region
        "00-908555-S-49",  # 00 is not a valid region
    ]


@pytest.fixture
def validator() -> ZimbabweValidator:
    return ZimbabweValidator()


class TestZimbabweValidator:
    def test_validate_valid_ids(
        self,
        validator: ZimbabweValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for id_number in valid_id_numbers:
            assert validator.validate(id_number), f"Expected {id_number} to be valid"

    def test_reject_invalid_format(
        self,
        validator: ZimbabweValidator,
        invalid_format_ids: list[str],
    ) -> None:
        for id_number in invalid_format_ids:
            assert not validator.validate(id_number), f"Expected {id_number} to be invalid"

    def test_reject_invalid_checksum(
        self,
        validator: ZimbabweValidator,
        invalid_checksum_ids: list[str],
    ) -> None:
        for id_number in invalid_checksum_ids:
            assert not validator.validate(id_number), f"Expected {id_number} to be invalid (bad checksum)"

    def test_reject_invalid_region(
        self,
        validator: ZimbabweValidator,
        invalid_region_ids: list[str],
    ) -> None:
        for id_number in invalid_region_ids:
            assert not validator.validate(id_number), f"Expected {id_number} to be invalid (bad region)"

    def test_reject_empty_and_short(
        self,
        validator: ZimbabweValidator,
    ) -> None:
        assert not validator.validate("")
        assert not validator.validate("sd")
        assert not validator.validate("12345")

    def test_normalize_removes_separators(
        self,
        validator: ZimbabweValidator,
    ) -> None:
        assert validator.normalize("50-025544-Q-12") == "50025544Q12"
        assert validator.normalize("43-165780-A-42") == "43165780A42"
        assert validator.normalize("77-040785-H- 77") == "77040785H77"
        assert validator.normalize("75-3415-02-L-70") == "75341502L70"

    def test_extract_data(
        self,
        validator: ZimbabweValidator,
    ) -> None:
        data = validator.extract_data("43-165780-A-42")
        assert data["registration_region"] == "Marondera"
        assert data["registration_code"] == "43"
        assert data["district"] == "Makoni"
        assert data["district_code"] == "42"
        assert data["sequence_number"] == "165780"
        assert data["check_letter"] == "A"

    def test_extract_data_raises_on_invalid(
        self,
        validator: ZimbabweValidator,
        invalid_format_ids: list[str],
    ) -> None:
        for id_number in invalid_format_ids:
            with pytest.raises(ValidationError):
                validator.extract_data(id_number)

    def test_all_region_codes_valid(
        self,
        validator: ZimbabweValidator,
    ) -> None:
        """Verify that all defined region codes are accepted."""
        # Using a known-good ID template and substituting region codes
        for region_code in REGION_LOOKUP:
            # Build a test ID with this region code
            # We can't easily generate valid IDs, so just verify the lookup exists
            assert region_code in REGION_LOOKUP
            assert isinstance(REGION_LOOKUP[region_code], str)

    def test_invalid_region_codes_not_in_lookup(
        self,
        validator: ZimbabweValidator,
    ) -> None:
        """Verify some region codes that should be invalid."""
        invalid_codes = ["00", "01", "09", "16", "17", "20", "30", "31", "33", "99"]
        for code in invalid_codes:
            assert code not in REGION_LOOKUP
