"""Tests for post-apartheid South African ID validator."""

import datetime as dt

import pytest

from id_validation.validate_southafrica import (
    PostApartheidSouthAfricaValidator,
    SouthAfricaValidationError,
)
from id_validation import ValidationError


@pytest.fixture
def validator() -> PostApartheidSouthAfricaValidator:
    return PostApartheidSouthAfricaValidator()


@pytest.fixture
def valid_id_numbers() -> list[str]:
    return ["7106245929185", "7405095437186", "7710165556082", "6403056005085"]


@pytest.fixture
def citizen_id_numbers() -> list[str]:
    return [
        "0604059596071",
        "0210079107087",
        "0701303437084",
        "6811228928077",
        "1010174953073",
    ]


@pytest.fixture
def permanent_resident_id_numbers() -> list[str]:
    return [
        "9805302690170",
        "5601292418175",
        "3507318786176",
        "0910142906189",
        "4005115587177",
    ]


@pytest.fixture
def invalid_citizenship_id_numbers() -> list[str]:
    return ["7106245929485", "7405095437386", "7710165556282"]


class TestPostApartheidSouthAfricaValidator:
    def test_validate_valid_ids(
        self,
        validator: PostApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            assert validator.validate(idno), f"Expected {idno} to be valid"

    def test_validate_with_spaces(
        self,
        validator: PostApartheidSouthAfricaValidator,
    ) -> None:
        # Should handle whitespace in input
        assert validator.validate("7106245 929 185    ")
        assert validator.validate("  7405095437186  ")

    def test_reject_invalid_format(
        self,
        validator: PostApartheidSouthAfricaValidator,
        invalid_str_id_numbers: list[str],
    ) -> None:
        for idno in invalid_str_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid"

    def test_reject_invalid_date(
        self,
        validator: PostApartheidSouthAfricaValidator,
        invalid_date_id_numbers: list[str],
    ) -> None:
        for idno in invalid_date_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad date)"

    def test_reject_invalid_checksum(
        self,
        validator: PostApartheidSouthAfricaValidator,
        invalid_checksum_id_numbers: list[str],
    ) -> None:
        for idno in invalid_checksum_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad checksum)"

    def test_reject_invalid_citizenship(
        self,
        validator: PostApartheidSouthAfricaValidator,
        invalid_citizenship_id_numbers: list[str],
    ) -> None:
        for idno in invalid_citizenship_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad citizenship)"

    def test_extract_data_valid(
        self,
        validator: PostApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            assert "dob" in data
            assert "gender" in data
            assert "checksum" in data
            assert "citizenship" in data

    def test_extract_data_invalid_raises(
        self,
        validator: PostApartheidSouthAfricaValidator,
        invalid_str_id_numbers: list[str],
    ) -> None:
        for idno in invalid_str_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_data(idno)

    def test_extract_dob(
        self,
        validator: PostApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            dob = data["dob"]
            assert isinstance(dob, dt.date)
            assert dob.month == int(idno[2:4])
            assert dob.day == int(idno[4:6])

    def test_extract_dob_century_inference(
        self,
        validator: PostApartheidSouthAfricaValidator,
    ) -> None:
        # Year 06 -> 2006 (less than current year's last 2 digits)
        data = validator.extract_data("0604059596071")  # From citizen_id_numbers fixture
        assert data["dob"].year == 2006

        # Year 98 -> 1998 (greater than current year's last 2 digits)
        data = validator.extract_data("9805302690170")  # From permanent_resident fixture
        assert data["dob"].year == 1998

        # Year 71 -> 1971 (greater than current year's last 2 digits)
        data = validator.extract_data("7106245929185")  # From valid_id_numbers fixture
        assert data["dob"].year == 1971

        # Year 21 -> 2021 (less than current year's last 2 digits)
        data = validator.extract_data("2104030613085")  # Generated valid ID
        assert data["dob"].year == 2021

    def test_extract_gender(
        self,
        validator: PostApartheidSouthAfricaValidator,
        male_id_numbers: list[str],
        female_id_numbers: list[str],
    ) -> None:
        for idno in male_id_numbers:
            data = validator.extract_data(idno)
            assert data["gender"] == "M"

        for idno in female_id_numbers:
            data = validator.extract_data(idno)
            assert data["gender"] == "F"

    def test_extract_citizenship(
        self,
        validator: PostApartheidSouthAfricaValidator,
        citizen_id_numbers: list[str],
        permanent_resident_id_numbers: list[str],
    ) -> None:
        for idno in citizen_id_numbers:
            data = validator.extract_data(idno)
            assert data["citizenship"] == "CITIZEN"
            assert data["citizenship_code"] == 0

        for idno in permanent_resident_id_numbers:
            data = validator.extract_data(idno)
            assert data["citizenship"] == "PERMANENT_RESIDENT"
            assert data["citizenship_code"] == 1

    def test_extract_checksum(
        self,
        validator: PostApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            assert data["checksum"] == int(idno[-1])

    def test_checksum_validation(
        self,
        validator: PostApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        """Test that only the correct checksum digit validates."""
        for idno in valid_id_numbers:
            check_digit = int(idno[-1])
            for i in range(10):
                test_idno = idno[:-1] + str(i)
                if i == check_digit:
                    assert validator.validate(test_idno)
                else:
                    assert not validator.validate(test_idno)
