from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_BSN_RE = re.compile(r"^(\d{9})$")


def _elfproef(digits: list[int]) -> bool:
    # "11-proef" / "elfproef": weights 9..2 and -1 for last digit
    weights = [9, 8, 7, 6, 5, 4, 3, 2, -1]
    return sum(d * w for d, w in zip(digits, weights)) % 11 == 0


@register("NL")
class NetherlandsBSNValidator(BaseValidator):
    """Netherlands BSN (Burgerservicenummer)."""

    country_code = "NL"

    def normalize(self, id_number: str) -> str:
        return re.sub(r"\s+", "", id_number.strip())

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _BSN_RE.match(v)
        if not m:
            raise ValidationError("Invalid BSN format")

        if v == "000000000":
            raise ValidationError("Invalid BSN")

        digits = [int(ch) for ch in v]
        if not _elfproef(digits):
            raise ValidationError("Invalid checksum")

        return ParsedID(country_code="NL", id_number=v, id_type="BSN")
