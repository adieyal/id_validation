import logging
import re
from enum import Enum

from id_validation.validate import ValidationError

re_valid_id = re.compile(r"\d{9}")
logger = logging.getLogger(__name__)
   
class BotswanaValidator:

    class GENDER(Enum):
        MALE = "1"
        FEMALE = "2"

    def __init__(self):
        logger.warning("The BotswanaValidator has not been validated against the official documentation but only using anecdotal information available online.")    

    def _clean(self, s: str) -> str:
        return s.strip()

    def _validate_str(self, s: str) -> bool:
        s = self._clean(s)
        return re_valid_id.fullmatch(s) is not None

    def _validate_gender(self, s: str) -> bool:
        s = self._clean(s)
        if not self._validate_str(s):
            return False

        try:
            gender_digit = self._extract_gender_digit(s)
            return BotswanaValidator.GENDER(gender_digit) in BotswanaValidator.GENDER.__members__.values()
        except ValueError:
            return False

    def validate(self, s: str) -> bool:
        if not self._validate_str(s):
            return False

        if not self._validate_gender(s):
            return False

        return True

    def _extract_gender_digit(self, s: str) -> str:
        return s[4]

    def _extract_gender(self, s: str) -> GENDER:
        if not self.validate(s):
            raise ValidationError("Invalid ID number")
        gender_digit = self._extract_gender_digit(s)
        return BotswanaValidator.GENDER(gender_digit)

    def extract_data(self, s):
        if not self.validate(s):
            raise ValidationError("Invalid ID number")

        return {
            "gender": self._extract_gender(s)
        }