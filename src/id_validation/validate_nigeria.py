from __future__ import annotations

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


@register("NG")
class NigeriaValidator(BaseValidator):
    """Nigeria National Identification Number (NIN) validator.

    The NIN is an 11-digit number. This validator only checks format;
    no checksum algorithm is publicly documented.
    """

    country_code = "NG"

    def normalize(self, id_number: str) -> str:
        return id_number.strip()

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)

        if len(v) != 11 or not v.isdigit():
            raise ValidationError("Invalid NIN format: must be 11 digits")

        return ParsedID(
            country_code="NG",
            id_number=v,
            id_type="NIN",
        )
