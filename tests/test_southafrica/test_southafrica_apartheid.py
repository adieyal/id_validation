from itertools import chain
import pytest

from id_validation.validate_southafrica import (
    CITIZENSHIP_TYPE,
    GENDER,
    RACE,
    ApartheidSouthAfricaValidator,
    SouthAfricaValidationError,
    SouthAfricaValidator,
)
from id_validation import ValidationError


@pytest.fixture
def validator() -> SouthAfricaValidator:
    return ApartheidSouthAfricaValidator()


@pytest.fixture
def invalid_race_id_numbers() -> list[str]:
    return [
        "7106245929085",
    ]


@pytest.fixture
def invalid_citizenship_id_numbers() -> list[str]:
    return [
        "7106245929285",
        "7106245929385",
        "7106245929485",
        "7106245929585",
        "7106245929685",
        "7106245929785",
        "7106245929885",
        "7106245929985",
    ]

@pytest.fixture
def invalid_id_numbers(invalid_date_id_numbers, invalid_race_id_numbers, invalid_citizenship_id_numbers, invalid_checksum_id_numbers) -> list[str]:
    return chain(invalid_date_id_numbers, invalid_race_id_numbers, invalid_citizenship_id_numbers, invalid_checksum_id_numbers)


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


# @pytest.fixture
# def invalid_id_numbers(
#     invalid_date_id_numbers, invalid_citizenship_numbers, invalid_checksum_numbers
# ):
#     return invalid_date_id_numbers + invalid_citizenship_numbers + invalid_checksum_numbers


class TestApartheidSouthAfricaValidator:
    def test_reject_invalid_strings(self, validator, invalid_str_id_numbers):
        for s in invalid_str_id_numbers:
            assert not validator._validate_str(s)

    def test_reject_invalid_dob(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_date_id_numbers: list[str],
    ):
        for idno in invalid_date_id_numbers:
            assert not validator._validate_dob(idno)

    def test_reject_invalid_race(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_race_id_numbers: list[str],
    ):
        for idno in invalid_race_id_numbers:
            assert not validator._validate_race(idno)

    def test_reject_invalid_citizenship(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_citizenship_id_numbers: list[str],
    ):
        for idno in invalid_citizenship_id_numbers:
            assert not validator._validate_citizenship(idno)

    def test_reject_invalid_checksum(
        self,
        validator: ApartheidSouthAfricaValidator,
        invalid_checksum_id_numbers: list[str],
    ):
       
        for idno in invalid_checksum_id_numbers:
            assert not validator._validate_checksum(idno)

    def test_reject_invalid_id_numbers(self, validator, invalid_id_numbers):
        for idno in invalid_id_numbers:
            assert not validator.validate(idno)

    def test_extract_dob(
        self,
        validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_id_numbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                validator.extract_dob(idno)

        for idno in valid_id_numbers:
            dob = validator.extract_dob(idno)
            assert dob.month == int(idno[2:4])
            assert dob.day == int(idno[4:6])

    def test_extract_gender(self, validator: ApartheidSouthAfricaValidator, invalid_id_numbers):
        for idno in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_gender(idno)

        for gender in list(GENDER):
            idno = validator.generate_idno(gender=gender)
            extracted_gender = validator.extract_gender(idno)
            assert extracted_gender == gender

    def test_extract_race(self, validator: ApartheidSouthAfricaValidator, invalid_id_numbers, valid_id_numbers):
        for idno in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_race(idno)

        for race in list(RACE):
            idno = validator.generate_idno(race=race)
            extracted_race = validator.extract_race(idno)
            assert extracted_race == race

    def test_extract_citizenship(self, validator: ApartheidSouthAfricaValidator, invalid_id_numbers):
        for idno in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_race(idno)

        for citizenship_type in list(CITIZENSHIP_TYPE):
            idno = validator.generate_idno(citizenship=citizenship_type)
            extracted_citizenship = validator.extract_citizenship(idno)
            assert extracted_citizenship == citizenship_type

    def test_extract_data(self, validator: ApartheidSouthAfricaValidator, invalid_id_numbers: list[str], valid_id_numbers: list[str]):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                validator.extract_data(idno)

        for race in list(RACE):
            for citizenship in list(CITIZENSHIP_TYPE):
                for gender in list(GENDER):

                    idno = validator.generate_idno(race=race, gender=gender, citizenship=citizenship)
                    data = validator.extract_data(idno)
                    assert "race" in data and data["race"] == race
                    assert "dob" in data and data["dob"] == validator.extract_dob(idno)
                    assert "gender" in data and data["gender"] == gender
                    assert "citizenship" in data and data["citizenship"] == citizenship
                    assert "checksum" in data and data["checksum"] == validator.extract_checksum(idno)
