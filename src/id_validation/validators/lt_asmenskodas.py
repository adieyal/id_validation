from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_LT_RE = re.compile(r"^(\d{11})$")

# Lithuanian personal code (Asmens kodas) checksum weights
_W1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
_W2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]


def _lt_checksum(digits: list[int]) -> int:
    """Return checksum digit for first 10 digits."""
    s1 = sum(d * w for d, w in zip(digits[:10], _W1))
    r1 = s1 % 11
    if r1 != 10:
        return r1

    s2 = sum(d * w for d, w in zip(digits[:10], _W2))
    r2 = s2 % 11
    if r2 != 10:
        return r2

    return 0


def _century_and_gender(first_digit: int) -> tuple[int, str]:
    # 1/2 => 1800-1899, 3/4 => 1900-1999, 5/6 => 2000-2099
    if first_digit in (1, 2):
        century = 1800
    elif first_digit in (3, 4):
        century = 1900
    elif first_digit in (5, 6):
        century = 2000
    else:
        raise ValidationError("Invalid first digit (century/gender)")

    gender = "M" if first_digit % 2 == 1 else "F"
    return century, gender


@register("LT")
class LithuaniaAsmensKodasValidator(BaseValidator):
    """Lithuania personal code (Asmens kodas).

    Format: GYYMMDDSSSC
    - G: gender + century marker (1..6)
    - YYMMDD: date of birth
    - SSS: serial/individual number
    - C: checksum
    """

    country_code = "LT"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _LT_RE.match(v):
            raise ValidationError("Invalid LT personal code format")

        digits = [int(ch) for ch in v]
        century, gender = _century_and_gender(digits[0])

        yy = int(v[1:3])
        mm = int(v[3:5])
        dd = int(v[5:7])
        year = century + yy
        try:
            dob = _dt.date(year, mm, dd)
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        expected = _lt_checksum(digits)
        if digits[10] != expected:
            raise ValidationError("Invalid checksum")

        extra: dict[str, Any] = {
            "century": century,
            "serial": int(v[7:10]),
            "checksum": digits[10],
        }
        return ParsedID(country_code="LT", id_number=v, id_type="ASMENS_KODAS", dob=dob, gender=gender, extra=extra)
