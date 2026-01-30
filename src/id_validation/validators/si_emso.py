from __future__ import annotations

import datetime as _dt
import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_EMSO_RE = re.compile(r"^(\d{13})$")

_WEIGHTS = [7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]


def _emso_checksum(first_12: list[int]) -> int:
    s = sum(d * w for d, w in zip(first_12, _WEIGHTS))
    r = 11 - (s % 11)
    if r == 11:
        return 0
    if r == 10:
        # 10 is not a valid check digit in this system
        raise ValidationError("Invalid checksum")
    return r


def _decode_year(yyy: int) -> int:
    # EMŠO uses a 3-digit year within a limited range; modern usage is mainly 19xx and 20xx.
    # Heuristic: if yyy is <= current year's last-3-digits, treat as 2000+yyy, else 1000+yyy.
    cutoff = _dt.date.today().year % 1000
    if yyy <= cutoff:
        return 2000 + yyy
    return 1000 + yyy


@register("SI")
class SloveniaEMSOValidator(BaseValidator):
    """Slovenia EMŠO (Enotna matična številka občana).

    EMŠO is structurally the same as the former Yugoslav JMBG.
    """

    country_code = "SI"

    def normalize(self, id_number: str) -> str:
        return re.sub(r"\s+", "", id_number.strip())

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _EMSO_RE.match(v):
            raise ValidationError("Invalid EMŠO format")

        digits = [int(ch) for ch in v]

        dd = int(v[0:2])
        mm = int(v[2:4])
        yyy = int(v[4:7])
        year = _decode_year(yyy)
        try:
            dob = _dt.date(year, mm, dd)
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        region_code = int(v[7:9])
        serial = int(v[9:12])
        gender = "M" if serial < 500 else "F"

        expected = _emso_checksum(digits[:12])
        if digits[12] != expected:
            raise ValidationError("Invalid checksum")

        extra = {
            "region_code": region_code,
            "serial": serial,
            "checksum": expected,
        }
        return ParsedID(country_code="SI", id_number=v, id_type="EMSO", dob=dob, gender=gender, extra=extra)
