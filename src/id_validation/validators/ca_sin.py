from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_SIN_RE = re.compile(r"^(\d{9})$")


def _luhn_ok(number: str) -> bool:
    digits = [int(c) for c in number]
    s = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return s % 10 == 0


@register("CA")
class CanadaSINValidator(BaseValidator):
    """Canada SIN (Social Insurance Number)."""

    country_code = "CA"

    def normalize(self, id_number: str) -> str:
        # Accept spaces/hyphens
        v = id_number.strip()
        v = re.sub(r"[^0-9]", "", v)
        return v

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _SIN_RE.match(v):
            raise ValidationError("Invalid SIN format")
        if not _luhn_ok(v):
            raise ValidationError("Invalid checksum")
        return ParsedID(country_code="CA", id_number=v, id_type="SIN")
