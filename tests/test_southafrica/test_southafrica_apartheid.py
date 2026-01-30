"""Tests for apartheid-era South African ID validator."""

import datetime as dt

import pytest

from id_validation.validate_southafrica import (
    ApartheidSouthAfricaValidator,
    SouthAfricaValidationError,
    Race,
    CitizenshipType,
)
from id_validation import ValidationError

from tests.utils import (
    Gender as GenGender,
    Race as GenRace,
    CitizenshipType as GenCitizenship,
    generate_apartheid_south_africa_id,
)


@pytest.fixture
def validator() -> ApartheidSouthAfricaValidator:
    return ApartheidSouthAfricaValidator()


@pytest.fixture
def valid_id_numbers() -> list[str]:
    return [
        "4102068120179",
        "3211037218146",
        "5612254513028",
        "5110260243193",
        "7707306076145",
        "3304130204160",
        "1511300891012",
        "9109071856157",
        "5606265491091",
        "1710214031000",
    ]


@pytest.fixture
def invalid_race_id_numbers() -> list[str]:
    # Race digit 8 is not valid
    return ["7106245929085"]


class TestApartheidSouthAfricaValidator:
    def test_validate_valid_ids(
        self,
        validator: ApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            assert validator.validate(idno), f"Expected {idno} to be valid"

    def test_reject_invalid_format(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_str_id_numbers: list[str],
    ) -> None:
        for idno in invalid_str_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid"

    def test_reject_invalid_date(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_date_id_numbers: list[str],
    ) -> None:
        for idno in invalid_date_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad date)"

    def test_reject_invalid_checksum(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_checksum_id_numbers: list[str],
    ) -> None:
        for idno in invalid_checksum_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad checksum)"

    def test_reject_invalid_race(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_race_id_numbers: list[str],
    ) -> None:
        for idno in invalid_race_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad race digit)"

    def test_extract_data_valid(
        self,
        validator: ApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            assert "dob" in data
            assert "gender" in data
            assert "checksum" in data
            assert "race" in data

    def test_extract_data_invalid_raises(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_str_id_numbers: list[str],
    ) -> None:
        for idno in invalid_str_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_data(idno)

    def test_extract_dob(
        self,
        validator: ApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            dob = data["dob"]
            assert isinstance(dob, dt.date)
            assert dob.month == int(idno[2:4])
            assert dob.day == int(idno[4:6])

    def test_extract_gender_generated(
        self,
        validator: ApartheidSouthAfricaValidator,
    ) -> None:
        """Test gender extraction using generated IDs."""
        for gender in list(GenGender):
            idno = generate_apartheid_south_africa_id(gender=gender)
            data = validator.extract_data(idno)
            expected = "M" if gender == GenGender.MALE else "F"
            assert data["gender"] == expected

    def test_extract_gender_from_fixtures(
        self,
        validator: ApartheidSouthAfricaValidator,
        male_id_numbers: list[str],
        female_id_numbers: list[str],
    ) -> None:
        for idno in male_id_numbers:
            # Only test if valid under apartheid rules (may have invalid race digit)
            if validator.validate(idno):
                data = validator.extract_data(idno)
                assert data["gender"] == "M"

        for idno in female_id_numbers:
            if validator.validate(idno):
                data = validator.extract_data(idno)
                assert data["gender"] == "F"

    def test_extract_race_generated(
        self,
        validator: ApartheidSouthAfricaValidator,
    ) -> None:
        """Test race extraction using generated IDs."""
        for race in list(GenRace):
            idno = generate_apartheid_south_africa_id(race=race)
            data = validator.extract_data(idno)
            assert data["race"] == race.name
            assert data["race_code"] == race.value

    def test_extract_citizenship_generated(
        self,
        validator: ApartheidSouthAfricaValidator,
    ) -> None:
        """Test citizenship extraction using generated IDs."""
        for citizenship in list(GenCitizenship):
            idno = generate_apartheid_south_africa_id(citizenship=citizenship)
            data = validator.extract_data(idno)
            assert data["citizenship"] == citizenship.name
            assert data["citizenship_code"] == citizenship.value

    def test_extract_checksum(
        self,
        validator: ApartheidSouthAfricaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            assert data["checksum"] == int(idno[-1])

    def test_full_extraction_generated(
        self,
        validator: ApartheidSouthAfricaValidator,
    ) -> None:
        """Test full data extraction using generated IDs with all combinations."""
        # Test a sampling of combinations to avoid combinatorial explosion
        test_cases = [
            (GenRace.WHITE, GenGender.MALE, GenCitizenship.CITIZEN),
            (GenRace.BLACK, GenGender.FEMALE, GenCitizenship.PERMANENT_RESIDENT),
            (GenRace.INDIAN, GenGender.MALE, GenCitizenship.CITIZEN),
            (GenRace.CAPE_COLOURED, GenGender.FEMALE, GenCitizenship.CITIZEN),
        ]

        for race, gender, citizenship in test_cases:
            idno = generate_apartheid_south_africa_id(
                race=race, gender=gender, citizenship=citizenship
            )
            data = validator.extract_data(idno)

            assert data["race"] == race.name
            assert data["gender"] == ("M" if gender == GenGender.MALE else "F")
            assert data["citizenship"] == citizenship.name
            assert "dob" in data
            assert "checksum" in data
