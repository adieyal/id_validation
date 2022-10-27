from itertools import chain
from xml.dom import ValidationErr

import pytest
from id_validation.validate import ValidationError
from id_validation.validate_botswana import BotswanaValidator


@pytest.fixture
def valid_male_id_numbers():
    return [
        "106513015",
    ]

@pytest.fixture
def valid_female_id_numbers():
    return [
        "106523015",
    ]

@pytest.fixture
def valid_id_numbers(valid_male_id_numbers, valid_female_id_numbers):
    return chain(valid_male_id_numbers, valid_female_id_numbers, [
        "106513015    ",
        "    417812414",
        "379219515",
        "095324303",
    ])

@pytest.fixture
def invalid_str_id_numbers():
    return [
        "",
        "23434",
        "43534534234243",
        "123456d89",
    ]

@pytest.fixture
def invalid_gender_id_numbers():
    return [
        "106533015",
        "417842414",
        "379259515",
        "095364303",
        "106573015",
        "417882414",
        "379299515",
    ]

@pytest.fixture
def invalid_id_numbers(invalid_str_id_numbers, invalid_gender_id_numbers):
    return chain(invalid_str_id_numbers, invalid_gender_id_numbers)

@pytest.fixture
def validator():
    return BotswanaValidator()

class TestBotswanaValidator:
    def test_rejects_invalid_strings(self, validator, invalid_str_id_numbers):
        for s in invalid_str_id_numbers:
            assert not validator._validate_str(s)

    def test_accepts_valid_strings(self, validator, valid_id_numbers):
        for s in valid_id_numbers:
            assert validator._validate_str(s)

    def test_rejects_invalid_gender(self, validator, invalid_str_id_numbers, invalid_gender_id_numbers):
        for s in invalid_str_id_numbers:
            assert not validator._validate_gender(s)

        for s in invalid_gender_id_numbers:
            assert not validator._validate_gender(s)

    def test_accepts_valid_gender(self, validator, valid_id_numbers):
        for s in valid_id_numbers:
            assert validator._validate_gender(s)

    def test_validate_rejects_invalid_id_numbers(self, validator, invalid_id_numbers):
        for s in invalid_id_numbers:
            assert not validator.validate(s)

    def test_validate_accepts_valid_id_numbers(self, validator, valid_id_numbers):
        for s in valid_id_numbers:
            assert validator.validate(s)

    def test_extract_gender_from_invalid_id_numbers(self, validator, invalid_id_numbers):
        for s in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator._extract_gender(s)

    def test_extract_gender_from_valid_id_numbers(self, validator, valid_male_id_numbers, valid_female_id_numbers):
        for s in valid_male_id_numbers:
            assert validator._extract_gender(s) == BotswanaValidator.GENDER.MALE

        for s in valid_female_id_numbers:
            assert validator._extract_gender(s) == BotswanaValidator.GENDER.FEMALE 

    def test_extract_data_with_invalid(self, validator, invalid_id_numbers):
        for s in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_data(s)

    def test_extract_date_with_valid_id_numbers(self, validator, valid_male_id_numbers, valid_female_id_numbers):
        for s in valid_male_id_numbers:
            data = validator.extract_data(s)
            assert "gender" in data and data["gender"] == BotswanaValidator.GENDER.MALE

        for s in valid_female_id_numbers:
            data = validator.extract_data(s)
            assert "gender" in data and data["gender"] == BotswanaValidator.GENDER.FEMALE
