"""Tests for Botswana National ID validator."""

from itertools import chain

import pytest

from id_validation.validate import ValidationError
from id_validation.validate_botswana import BotswanaValidator


@pytest.fixture
def valid_male_id_numbers() -> list[str]:
    return ["106513015"]


@pytest.fixture
def valid_female_id_numbers() -> list[str]:
    return ["106523015"]


@pytest.fixture
def valid_id_numbers(valid_male_id_numbers, valid_female_id_numbers) -> list[str]:
    return list(
        chain(
            valid_male_id_numbers,
            valid_female_id_numbers,
            [
                "106513015    ",
                "    417812414",
                "379219515",
                "095324303",
            ],
        )
    )


@pytest.fixture
def invalid_format_id_numbers() -> list[str]:
    return [
        "",
        "23434",
        "43534534234243",
        "123456d89",
    ]


@pytest.fixture
def invalid_gender_id_numbers() -> list[str]:
    # Gender digit (position 5) must be 1 or 2
    return [
        "106533015",  # gender digit 3
        "417842414",  # gender digit 4
        "379259515",  # gender digit 5
        "095364303",  # gender digit 6
        "106573015",  # gender digit 7
        "417882414",  # gender digit 8
        "379299515",  # gender digit 9
    ]


@pytest.fixture
def invalid_id_numbers(invalid_format_id_numbers, invalid_gender_id_numbers) -> list[str]:
    return list(chain(invalid_format_id_numbers, invalid_gender_id_numbers))


@pytest.fixture
def validator() -> BotswanaValidator:
    return BotswanaValidator()


class TestBotswanaValidator:
    def test_validate_accepts_valid_ids(
        self,
        validator: BotswanaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            assert validator.validate(idno), f"Expected {idno} to be valid"

    def test_validate_rejects_invalid_format(
        self,
        validator: BotswanaValidator,
        invalid_format_id_numbers: list[str],
    ) -> None:
        for idno in invalid_format_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid"

    def test_validate_rejects_invalid_gender(
        self,
        validator: BotswanaValidator,
        invalid_gender_id_numbers: list[str],
    ) -> None:
        for idno in invalid_gender_id_numbers:
            assert not validator.validate(idno), f"Expected {idno} to be invalid (bad gender)"

    def test_extract_data_raises_on_invalid(
        self,
        validator: BotswanaValidator,
        invalid_id_numbers: list[str],
    ) -> None:
        for idno in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_data(idno)

    def test_extract_gender_male(
        self,
        validator: BotswanaValidator,
        valid_male_id_numbers: list[str],
    ) -> None:
        for idno in valid_male_id_numbers:
            data = validator.extract_data(idno)
            assert data["gender"] == "M"

    def test_extract_gender_female(
        self,
        validator: BotswanaValidator,
        valid_female_id_numbers: list[str],
    ) -> None:
        for idno in valid_female_id_numbers:
            data = validator.extract_data(idno)
            assert data["gender"] == "F"

    def test_extract_data_contains_expected_fields(
        self,
        validator: BotswanaValidator,
        valid_id_numbers: list[str],
    ) -> None:
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            assert "gender" in data
            assert "gender_digit" in data
            assert data["gender"] in ("M", "F")
