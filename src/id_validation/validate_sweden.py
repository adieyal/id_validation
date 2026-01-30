from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


# Accept 10-digit with separator or 12-digit without.
# Examples: YYMMDD-XXXX, YYMMDD+XXXX, YYYYMMDDXXXX
_SSN_RE = re.compile(r"^(?:(\d{2})(\d{2})(\d{2})[-+]?|(\d{4})(\d{2})(\d{2}))(?:(\d{3})(\d))$")


def _luhn_check_digit(num: str) -> int:
    total = 0
    for i, ch in enumerate(num):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - (total % 10)) % 10


@register("SE")
class SwedenPersonnummerValidator(BaseValidator):
    """Sweden personal identity number (personnummer).

    Implements checksum (Luhn) on the 9-digit string YYMMDDNNN and compares with last digit.
    """

    country_code = "SE"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().upper().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)

        # Capture separator if present
        sep = None
        if len(v) in (11, 12) and ("-" in v or "+" in v):
            sep = "+" if "+" in v else "-"

        # Strip separator
        w = v.replace("-", "").replace("+", "")

        if len(w) == 10:
            yy = int(w[0:2])
            mm = int(w[2:4])
            dd = int(w[4:6])
            nnn = w[6:9]
            c = int(w[9])
            year = self._infer_century(yy, sep)
        elif len(w) == 12:
            year = int(w[0:4])
            mm = int(w[4:6])
            dd = int(w[6:8])
            nnn = w[8:11]
            c = int(w[11])
            yy = year % 100
        else:
            raise ValidationError("Invalid personnummer length")

        # Coordination number: day + 60
        is_coordination = dd > 60
        real_day = dd - 60 if is_coordination else dd

        try:
            dob = _dt.date(year, mm, real_day)
        except ValueError as e:
            raise ValidationError("Invalid date") from e

        expected = _luhn_check_digit(f"{yy:02d}{mm:02d}{dd:02d}{nnn}")
        if expected != c:
            raise ValidationError("Invalid checksum")

        gender = "M" if int(nnn[-1]) % 2 == 1 else "F"
        extra: dict[str, Any] = {
            "coordination_number": is_coordination,
            "individual_number": int(nnn),
            "checksum": c,
        }

        return ParsedID(country_code="SE", id_number=v, id_type="PERSONNUMMER", dob=dob, gender=gender, extra=extra)

    def _infer_century(self, yy: int, sep: str | None) -> int:
        today = _dt.date.today()
        current_yy = today.year % 100

        if sep == "+":
            # Person is 100+ years old; use previous century compared to '-' logic.
            base = today.year - 100
            century = base - (base % 100)
            # choose century such that year <= base year
            year = century + yy
            if year > base:
                year -= 100
            return year

        # '-' or unspecified: within last 100 years
        century = today.year - (today.year % 100)
        year = century + yy
        if yy > current_yy:
            year -= 100
        return year
