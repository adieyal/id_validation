from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_ISIKUKOOD_RE = re.compile(r"^(\d{11})$")


def _isikukood_checksum(digits: list[int]) -> int:
    # Two-stage mod 11 checksum.
    weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    weights2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]

    s1 = sum(d * w for d, w in zip(digits[:10], weights1))
    r1 = s1 % 11
    if r1 < 10:
        return r1

    s2 = sum(d * w for d, w in zip(digits[:10], weights2))
    r2 = s2 % 11
    if r2 < 10:
        return r2

    return 0


def _century_gender_from_first(first: int) -> tuple[int, str]:
    # 1/2: 1800-1899 (M/F)
    # 3/4: 1900-1999 (M/F)
    # 5/6: 2000-2099 (M/F)
    # 7/8: 2100-2199 (M/F)
    mapping = {
        1: (1800, "M"),
        2: (1800, "F"),
        3: (1900, "M"),
        4: (1900, "F"),
        5: (2000, "M"),
        6: (2000, "F"),
        7: (2100, "M"),
        8: (2100, "F"),
    }
    if first not in mapping:
        raise ValidationError("Invalid first digit")
    return mapping[first]


@register("EE")
class EstoniaIsikukoodValidator(BaseValidator):
    """Estonia personal identification code (isikukood)."""

    country_code = "EE"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _ISIKUKOOD_RE.match(v):
            raise ValidationError("Invalid isikukood format")

        digits = [int(ch) for ch in v]
        expected = _isikukood_checksum(digits)
        if digits[10] != expected:
            raise ValidationError("Invalid checksum")

        century, gender = _century_gender_from_first(digits[0])
        yy = int(v[1:3])
        mm = int(v[3:5])
        dd = int(v[5:7])

        year = century + yy
        try:
            dob = _dt.date(year, mm, dd)
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        serial = int(v[7:10])
        extra: dict[str, Any] = {
            "serial": serial,
            "checksum": digits[10],
        }
        return ParsedID(country_code="EE", id_number=v, id_type="ISIKUKOOD", dob=dob, gender=gender, extra=extra)
