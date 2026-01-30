from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


_CF_RE = re.compile(r"^[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]$")

_MONTH_MAP = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "H": 6,
    "L": 7,
    "M": 8,
    "P": 9,
    "R": 10,
    "S": 11,
    "T": 12,
}

_ODD_VALUES = {
    **{str(i): v for i, v in enumerate([1, 0, 5, 7, 9, 13, 15, 17, 19, 21])},
    **dict(
        A=1,
        B=0,
        C=5,
        D=7,
        E=9,
        F=13,
        G=15,
        H=17,
        I=19,
        J=21,
        K=2,
        L=4,
        M=18,
        N=20,
        O=11,
        P=3,
        Q=6,
        R=8,
        S=12,
        T=14,
        U=16,
        V=10,
        W=22,
        X=25,
        Y=24,
        Z=23,
    ),
}

_EVEN_VALUES = {**{str(i): i for i in range(10)}, **{chr(ord('A') + i): i for i in range(26)}}

_CHECK_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _cf_check_char(cf15: str) -> str:
    total = 0
    for idx, ch in enumerate(cf15, start=1):
        if idx % 2 == 1:  # odd positions (1-indexed)
            total += _ODD_VALUES[ch]
        else:
            total += _EVEN_VALUES[ch]
    return _CHECK_CHARS[total % 26]


@register("IT")
class ItalyCodiceFiscaleValidator(BaseValidator):
    """Italy Codice Fiscale (tax code) validator.

    Implements checksum and extracts: dob (year/month/day) and gender.
    Municipality code is returned but not decoded (requires external table).
    """

    country_code = "IT"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().upper().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        cf = self.normalize(id_number)
        if not _CF_RE.match(cf):
            raise ValidationError("Invalid codice fiscale format")

        expected = _cf_check_char(cf[:15])
        if cf[15] != expected:
            raise ValidationError("Invalid checksum")

        yy = int(cf[6:8])
        month_ch = cf[8]
        day_code = int(cf[9:11])
        comune = cf[11:15]

        if month_ch not in _MONTH_MAP:
            raise ValidationError("Invalid month code")
        month = _MONTH_MAP[month_ch]

        gender = "F" if day_code > 40 else "M"
        day = day_code - 40 if day_code > 40 else day_code

        # Infer century heuristically.
        today = _dt.date.today()
        current_yy = today.year % 100
        year = (today.year - (today.year % 100)) + yy
        if yy > current_yy:
            year -= 100

        try:
            dob = _dt.date(year, month, day)
        except ValueError as e:
            raise ValidationError("Invalid date") from e

        extra: dict[str, Any] = {
            "municipality_code": comune,
            "checksum": cf[15],
        }
        return ParsedID(country_code="IT", id_number=cf, id_type="CODICE_FISCALE", dob=dob, gender=gender, extra=extra)
