from __future__ import annotations

import logging
import re

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID

_BOTSWANA_RE = re.compile(r"^\d{9}$")
_VALID_GENDER_DIGITS = {"1", "2"}

logger = logging.getLogger(__name__)


@register("BW")
class BotswanaValidator(BaseValidator):
    """Botswana National ID validator.

    Warning: This validator has not been validated against official documentation,
    only using anecdotal information available online.
    """

    country_code = "BW"

    def __init__(self) -> None:
        logger.warning(
            "The BotswanaValidator has not been validated against official "
            "documentation but only using anecdotal information available online."
        )

    def normalize(self, id_number: str) -> str:
        return id_number.strip()

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)

        if not _BOTSWANA_RE.fullmatch(v):
            raise ValidationError("Invalid Botswana ID format")

        gender_digit = v[4]
        if gender_digit not in _VALID_GENDER_DIGITS:
            raise ValidationError("Invalid gender digit")

        gender = "M" if gender_digit == "1" else "F"

        return ParsedID(
            country_code="BW",
            id_number=v,
            id_type="NATIONAL_ID",
            gender=gender,
            extra={"gender_digit": gender_digit},
        )
