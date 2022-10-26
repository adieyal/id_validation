from .validate import Validator
from .validate_zimbabwe import ZimbabweValidator
from .validate_southafrica import PostApartheidSouthAfricaValidator, ApartheidSouthAfricaValidator

VERSION = "0.3.4"

__all__ = ["ValidatorFactory"]

validators = {
    "ZA": PostApartheidSouthAfricaValidator,
    "ZA_OLD": ApartheidSouthAfricaValidator,
    "ZW": ZimbabweValidator
}

class ValidatorFactory:
    @staticmethod
    def get_validator(country_code: str, *args, **kwargs) -> Validator:
        if country_code not in validators:
            raise ValueError("No validator for country code: " + country_code)
        return validators[country_code](*args, **kwargs)
