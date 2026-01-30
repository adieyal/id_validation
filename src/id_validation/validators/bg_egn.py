from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_EGN_RE = re.compile(r"^(\d{10})$")

# Weights for first 9 digits.
_EGN_WEIGHTS = [2, 4, 8, 5, 10, 9, 7, 3, 6]


def _decode_egn_dob(yy: int, mm: int, dd: int) -> _dt.date:
    # Month encoding:
    # 1900-1999: 01-12
    # 1800-1899: month + 20
    # 2000-2099: month + 40
    if 1 <= mm <= 12:
        century = 1900
        real_month = mm
    elif 21 <= mm <= 32:
        century = 1800
        real_month = mm - 20
    elif 41 <= mm <= 52:
        century = 2000
        real_month = mm - 40
    else:
        raise ValidationError("Invalid month/century encoding")

    year = century + yy
    try:
        return _dt.date(year, real_month, dd)
    except ValueError as e:
        raise ValidationError("Invalid date of birth") from e


def _egn_checksum(first_9: list[int]) -> int:
    s = sum(d * w for d, w in zip(first_9, _EGN_WEIGHTS))
    r = s % 11
    return 0 if r == 10 else r


@register("BG")
class BulgariaEGNValidator(BaseValidator):
    """Bulgaria EGN (Единен граждански номер)."""

    country_code = "BG"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _EGN_RE.match(v):
            raise ValidationError("Invalid EGN format")

        digits = [int(ch) for ch in v]
        expected = _egn_checksum(digits[:9])
        if digits[9] != expected:
            raise ValidationError("Invalid checksum")

        yy = int(v[0:2])
        mm = int(v[2:4])
        dd = int(v[4:6])
        dob = _decode_egn_dob(yy, mm, dd)

        birth_order = int(v[6:9])
        # The last digit of the three-digit birth order is even for males, odd for females.
        gender = "M" if (birth_order % 2 == 0) else "F"

        extra: dict[str, Any] = {
            "birth_order": birth_order,
            "checksum": digits[9],
        }

        return ParsedID(country_code="BG", id_number=v, id_type="EGN", dob=dob, gender=gender, extra=extra)
