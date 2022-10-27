import pytest

from id_validation.validate_nigeria import NigeriaValidator
from id_validation.validate import ValidationError

@pytest.fixture
def validator():
    return NigeriaValidator()

@pytest.fixture
def invalid_str_id_numbers():
    return [
        "",
        "123456789",
        "342343243243244324",
        "3432dfdsf",
    ]

@pytest.fixture
def valid_id_numbers():
    return [
        "45743234565",
        "37965436742",
        "34235768854",
    ]

@pytest.fixture
def invalid_id_numbers(invalid_str_id_numbers):
    return invalid_str_id_numbers

class TestNigeriaValidator:
    def test_reject_invalid_strings(self, validator, invalid_str_id_numbers):
        for s in invalid_str_id_numbers:
            assert not validator._validate_str(s)

    def test_validation(self, validator, valid_id_numbers, invalid_id_numbers):
        for idno in invalid_id_numbers:
            assert not validator.validate(idno)

        for idno in valid_id_numbers:
            assert validator.validate(idno)

    def test_extract_data(self, validator, valid_id_numbers, invalid_id_numbers):
        for idno in invalid_id_numbers:
            with pytest.raises(ValidationError):
                validator.extract_data(idno)
            
        for idno in valid_id_numbers:
            data = validator.extract_data(idno)
            assert len(data) == 0