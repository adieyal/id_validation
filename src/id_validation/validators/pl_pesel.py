from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_PESEL_RE = re.compile(r"^(\d{11})$")

# Weights for first 10 digits
_PESEL_WEIGHTS = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]


def _decode_pesel_dob(yy: int, mm: int, dd: int) -> _dt.date:
    # Century encoded in month:
    # 1900-1999: 01-12
    # 2000-2099: 21-32 (month + 20)
    # 2100-2199: 41-52 (month + 40)
    # 2200-2299: 61-72 (month + 60)
    # 1800-1899: 81-92 (month + 80)
    if 1 <= mm <= 12:
        century = 1900
        real_month = mm
    elif 21 <= mm <= 32:
        century = 2000
        real_month = mm - 20
    elif 41 <= mm <= 52:
        century = 2100
        real_month = mm - 40
    elif 61 <= mm <= 72:
        century = 2200
        real_month = mm - 60
    elif 81 <= mm <= 92:
        century = 1800
        real_month = mm - 80
    else:
        raise ValidationError("Invalid month/century encoding")

    year = century + yy
    try:
        return _dt.date(year, real_month, dd)
    except ValueError as e:
        raise ValidationError("Invalid date of birth") from e


def _pesel_checksum(first_10_digits: list[int]) -> int:
    s = sum(d * w for d, w in zip(first_10_digits, _PESEL_WEIGHTS))
    return (10 - (s % 10)) % 10


@register("PL")
class PolandPESELValidator(BaseValidator):
    """Poland PESEL (Powszechny Elektroniczny System Ewidencji Ludności)."""

    country_code = "PL"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _PESEL_RE.match(v)
        if not m:
            raise ValidationError("Invalid PESEL format")

        digits = [int(ch) for ch in v]
        expected = _pesel_checksum(digits[:10])
        if digits[10] != expected:
            raise ValidationError("Invalid checksum")

        yy = int(v[0:2])
        mm = int(v[2:4])
        dd = int(v[4:6])
        dob = _decode_pesel_dob(yy, mm, dd)

        gender_digit = digits[9]
        gender = "M" if gender_digit % 2 == 1 else "F"

        extra: dict[str, Any] = {
            "serial": int(v[6:10]),
            "checksum": digits[10],
        }
        return ParsedID(country_code="PL", id_number=v, id_type="PESEL", dob=dob, gender=gender, extra=extra)
