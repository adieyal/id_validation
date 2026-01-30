from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


_HETU_RE = re.compile(r"^(\d{2})(\d{2})(\d{2})([+\-A])(\d{3})([0-9A-Y])$")

# Official checksum table (0-30)
_HETU_CHECK_CHARS = "0123456789ABCDEFHJKLMNPRSTUVWXY"


@register("FI")
class FinlandHETUValidator(BaseValidator):
    """Finland personal identity code (HETU / henkilötunnus)."""

    country_code = "FI"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().upper().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _HETU_RE.match(v)
        if not m:
            raise ValidationError("Invalid HETU format")

        dd, mm, yy, century_char, individual, check = m.groups()

        if century_char == "+":
            century = 1800
        elif century_char == "-":
            century = 1900
        elif century_char == "A":
            century = 2000
        else:
            raise ValidationError("Invalid century character")

        year = century + int(yy)
        try:
            dob = _dt.date(year, int(mm), int(dd))
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        number = int(dd + mm + yy + individual)
        expected = _HETU_CHECK_CHARS[number % 31]
        if check != expected:
            raise ValidationError("Invalid checksum")

        gender = "M" if int(individual) % 2 == 1 else "F"

        extra: dict[str, Any] = {
            "century": century,
            "individual_number": int(individual),
            "checksum": check,
        }
        return ParsedID(country_code="FI", id_number=v, id_type="HETU", dob=dob, gender=gender, extra=extra)
