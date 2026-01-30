from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_CPR_RE = re.compile(r"^(\d{6})-?(\d{4})$")

# Mod-11 checksum weights for all 10 digits
_CPR_WEIGHTS = [4, 3, 2, 7, 6, 5, 4, 3, 2, 1]


def _cpr_century(yy: int, serial_first: int) -> int:
    """Infer century from CPR rules (best-effort).

    Mapping (common published rule set):
    - serial_first 0-3 => 1900-1999
    - serial_first 4-5 => 1900-1999 (yy 37-99) or 2000-2036 (yy 00-36)
    - serial_first 6-9 => 1800-1899 (yy 37-99) or 2000-2036 (yy 00-36)
    """
    if 0 <= serial_first <= 3:
        return 1900
    if 4 <= serial_first <= 5:
        return 2000 if yy <= 36 else 1900
    if 6 <= serial_first <= 9:
        return 2000 if yy <= 36 else 1800
    raise ValidationError("Invalid serial/century digit")


def _cpr_checksum_ok(digits: list[int]) -> bool:
    s = sum(d * w for d, w in zip(digits, _CPR_WEIGHTS))
    return s % 11 == 0


@register("DK")
class DenmarkCPRValidator(BaseValidator):
    """Denmark CPR number.

    Format: DDMMYY-SSSS (hyphen optional)

    - DOB is encoded as DDMMYY plus a century rule based on the first serial digit.
    - Gender is encoded by parity of the last digit (odd=male, even=female).

    Checksum note:
    Denmark historically used a mod-11 checksum, but the modulus rule is no longer
    guaranteed for all issued numbers. Therefore checksum validation is **optional**.

    Use strict_checksum=True to enforce mod-11 for datasets where it's expected.
    """

    country_code = "DK"

    def __init__(self, strict_checksum: bool = False):
        self.strict_checksum = strict_checksum

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _CPR_RE.match(v)
        if not m:
            raise ValidationError("Invalid CPR format")

        dd = int(m.group(1)[0:2])
        mm = int(m.group(1)[2:4])
        yy = int(m.group(1)[4:6])
        serial = m.group(2)

        serial_first = int(serial[0])
        century = _cpr_century(yy, serial_first)
        year = century + yy
        try:
            dob = _dt.date(year, mm, dd)
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        digits = [int(ch) for ch in (m.group(1) + serial)]
        checksum_valid = _cpr_checksum_ok(digits)
        if self.strict_checksum and not checksum_valid:
            raise ValidationError("Invalid checksum")

        gender = "M" if digits[-1] % 2 == 1 else "F"

        extra: dict[str, Any] = {
            "century": century,
            "sequence": int(serial),
            "checksum_valid": checksum_valid,
        }
        return ParsedID(country_code="DK", id_number=(m.group(1) + serial), id_type="CPR", dob=dob, gender=gender, extra=extra)
