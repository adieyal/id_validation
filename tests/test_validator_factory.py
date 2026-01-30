import pytest

from id_validation import ValidatorFactory
from id_validation.validate_botswana import BotswanaValidator
from id_validation.validate_southafrica import (
    ApartheidSouthAfricaValidator,
    PostApartheidSouthAfricaValidator,
)
from id_validation.validate_zimbabwe import ZimbabweValidator
from id_validation.validate_nigeria import NigeriaValidator


@pytest.fixture
def validator_factory() -> type[ValidatorFactory]:
    return ValidatorFactory


class TestValidatorFactory:
    def test_get_bw_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("BW"), BotswanaValidator)

    def test_get_ng_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("NG"), NigeriaValidator)

    def test_get_za_validator(self, validator_factory):
        assert isinstance(
            validator_factory.get_validator("ZA"), PostApartheidSouthAfricaValidator
        )

    def test_get_za_old_validator(self, validator_factory):
        assert isinstance(
            validator_factory.get_validator("ZA_OLD"), ApartheidSouthAfricaValidator
        )

    def test_get_zw_validator(self, validator_factory):
        assert isinstance(validator_factory.get_validator("ZW"), ZimbabweValidator)
