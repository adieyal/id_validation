from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_RUT_RE = re.compile(r"^(\d{7,8})([0-9K])$", re.IGNORECASE)


def _rut_dv(number: str) -> str:
    # Mod-11 with multipliers 2..7 cyclic from rightmost digit
    s = 0
    mul = 2
    for ch in reversed(number):
        s += int(ch) * mul
        mul += 1
        if mul > 7:
            mul = 2

    r = 11 - (s % 11)
    if r == 11:
        return "0"
    if r == 10:
        return "K"
    return str(r)


@register("CL")
class ChileRUTValidator(BaseValidator):
    """Chile RUT / RUN (Rol Único Tributario / Rol Único Nacional)."""

    country_code = "CL"

    def normalize(self, id_number: str) -> str:
        v = id_number.strip().upper()
        v = v.replace(".", "").replace("-", "")
        return v

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _RUT_RE.match(v)
        if not m:
            raise ValidationError("Invalid RUT format")

        num, dv = m.group(1), m.group(2).upper()
        expected = _rut_dv(num)
        if dv != expected:
            raise ValidationError("Invalid checksum")

        return ParsedID(country_code="CL", id_number=f"{num}{dv}", id_type="RUT", extra={"number": num, "dv": dv})
