import pytest
from id_validation.validate_botswana import BotswanaValidator

from id_validation.validate_southafrica import ApartheidSouthAfricaValidator, PostApartheidSouthAfricaValidator, SouthAfricaValidator
from id_validation.validate_zimbabwe import ZimbabweValidator

@pytest.fixture
def validator_factory():
    from id_validation import ValidatorFactory
    return ValidatorFactory


class TestValidatorFactory:
    def test_get_za_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("ZA"), PostApartheidSouthAfricaValidator)

    def test_get_za_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("ZA_OLD"), ApartheidSouthAfricaValidator)

    def test_get_bw_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("BW"), BotswanaValidator)

    def test_get_zw_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("ZW"), ZimbabweValidator)
