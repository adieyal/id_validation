from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_CNP_RE = re.compile(r"^(\d{13})$")

# Constant weights used by CNP checksum
_CNP_WEIGHTS = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]

# County (Judet) codes. This mapping is widely published; treat as best-effort.
_COUNTY_NAMES: dict[int, str] = {
    1: "Alba",
    2: "Arad",
    3: "Argeș",
    4: "Bacău",
    5: "Bihor",
    6: "Bistrița-Năsăud",
    7: "Botoșani",
    8: "Brașov",
    9: "Brăila",
    10: "Buzău",
    11: "Caraș-Severin",
    12: "Cluj",
    13: "Constanța",
    14: "Covasna",
    15: "Dâmbovița",
    16: "Dolj",
    17: "Galați",
    18: "Gorj",
    19: "Harghita",
    20: "Hunedoara",
    21: "Ialomița",
    22: "Iași",
    23: "Ilfov",
    24: "Maramureș",
    25: "Mehedinți",
    26: "Mureș",
    27: "Neamț",
    28: "Olt",
    29: "Prahova",
    30: "Satu Mare",
    31: "Sălaj",
    32: "Sibiu",
    33: "Suceava",
    34: "Teleorman",
    35: "Timiș",
    36: "Tulcea",
    37: "Vaslui",
    38: "Vâlcea",
    39: "Vrancea",
    40: "București",
    41: "București - Sector 1",
    42: "București - Sector 2",
    43: "București - Sector 3",
    44: "București - Sector 4",
    45: "București - Sector 5",
    46: "București - Sector 6",
    51: "Călărași",
    52: "Giurgiu",
}


def _cnp_checksum(first_12: list[int]) -> int:
    s = sum(d * w for d, w in zip(first_12, _CNP_WEIGHTS))
    r = s % 11
    return 1 if r == 10 else r


def _century_from_s(s: int) -> int:
    # S indicates sex and century.
    # Common interpretation:
    # 1/2 => 1900-1999
    # 3/4 => 1800-1899
    # 5/6 => 2000-2099
    # 7/8/9 => special cases (residents/foreigners) – often treated as 2000+.
    if s in (1, 2):
        return 1900
    if s in (3, 4):
        return 1800
    if s in (5, 6):
        return 2000
    if s in (7, 8, 9):
        return 2000
    raise ValidationError("Invalid S digit")


@register("RO")
class RomaniaCNPValidator(BaseValidator):
    """Romania CNP (Cod Numeric Personal)."""

    country_code = "RO"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _CNP_RE.match(v):
            raise ValidationError("Invalid CNP format")

        digits = [int(ch) for ch in v]
        if digits[0] == 0:
            raise ValidationError("Invalid S digit")

        expected = _cnp_checksum(digits[:12])
        if digits[12] != expected:
            raise ValidationError("Invalid checksum")

        s = digits[0]
        yy = int(v[1:3])
        mm = int(v[3:5])
        dd = int(v[5:7])
        century = _century_from_s(s)
        year = century + yy

        try:
            dob = _dt.date(year, mm, dd)
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        gender = "M" if s in (1, 3, 5, 7, 9) else "F"

        county_code = int(v[7:9])
        extra: dict[str, Any] = {
            "county_code": county_code,
            "county_name": _COUNTY_NAMES.get(county_code),
            "serial": int(v[9:12]),
            "checksum": digits[12],
        }

        return ParsedID(country_code="RO", id_number=v, id_type="CNP", dob=dob, gender=gender, extra=extra)
