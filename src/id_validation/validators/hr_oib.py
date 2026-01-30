from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_OIB_RE = re.compile(r"^(\d{11})$")


def _iso_7064_mod_11_10_check_digit(first_10: list[int]) -> int:
    # ISO 7064 Mod 11,10 (used by Croatian OIB)
    p = 10
    for d in first_10:
        p = (p + d) % 10
        if p == 0:
            p = 10
        p = (p * 2) % 11
    k = 11 - p
    if k == 10 or k == 11:
        k = 0
    return k


@register("HR")
class CroatiaOIBValidator(BaseValidator):
    """Croatia OIB (Osobni identifikacijski broj)."""

    country_code = "HR"

    def normalize(self, id_number: str) -> str:
        return re.sub(r"\s+", "", id_number.strip())

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _OIB_RE.match(v):
            raise ValidationError("Invalid OIB format")

        digits = [int(ch) for ch in v]
        expected = _iso_7064_mod_11_10_check_digit(digits[:10])
        if digits[10] != expected:
            raise ValidationError("Invalid checksum")

        return ParsedID(country_code="HR", id_number=v, id_type="OIB", extra={"checksum": expected})
