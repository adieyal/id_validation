from id_validation.validate_botswana import BotswanaValidator
from .validate import Validator, ValidationError
from .validate_zimbabwe import ZimbabweValidator
from .validate_southafrica import PostApartheidSouthAfricaValidator, ApartheidSouthAfricaValidator
from .validate_botswana import BotswanaValidator
from .validate_nigeria import NigeriaValidator

VERSION = "0.5.0"

__all__ = ["ValidatorFactory"]

validators = {
    "BW": BotswanaValidator,
    "NG": NigeriaValidator,
    "ZA": PostApartheidSouthAfricaValidator,
    "ZA_OLD": ApartheidSouthAfricaValidator,
    "ZW": ZimbabweValidator,
}

class ValidatorFactory:
    @staticmethod
    def get_validator(country_code: str, *args, **kwargs) -> Validator:
        if country_code not in validators:
            raise ValueError("No validator for country code: " + country_code)
        return validators[country_code](*args, **kwargs)
