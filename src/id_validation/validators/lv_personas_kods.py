from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_LV_RE = re.compile(r"^(\d{6})-?(\d{5})$")


def _try_parse_legacy(digits11: str) -> tuple[_dt.date | None, dict[str, Any]]:
    """Attempt to parse legacy Latvian personal code with embedded DOB.

    Legacy format (commonly encountered in datasets): DDMMYY-XXXXX
    The first digit after the hyphen is generally used as a century indicator.

    This implementation validates *format* and *date*.
    A checksum/key has existed historically, but authoritative public documentation
    is harder to source; checksum validation is intentionally not enforced here.
    """
    dd = int(digits11[0:2])
    mm = int(digits11[2:4])
    yy = int(digits11[4:6])
    century_digit = int(digits11[6])

    century_map = {0: 1800, 1: 1900, 2: 2000}
    if century_digit not in century_map:
        return None, {}

    year = century_map[century_digit] + yy
    try:
        dob = _dt.date(year, mm, dd)
    except ValueError:
        return None, {}

    extra: dict[str, Any] = {
        "century": century_map[century_digit],
        "century_digit": century_digit,
        "serial": int(digits11[7:11]),
        "checksum": None,
    }
    return dob, extra


@register("LV")
class LatviaPersonasKodsValidator(BaseValidator):
    """Latvia personal code (personas kods).

    Supports:
    - Legacy: DDMMYY-XXXXX (hyphen optional) with DOB derivable.
    - Modern: 11 digits without DOB encoding (DOB/gender not derivable).

    Note: This validator validates format and (when applicable) DOB. It does not
    enforce a checksum for LV at this time.
    """

    country_code = "LV"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)

        # Legacy (date-encoded)
        m = _LV_RE.match(v)
        if m:
            digits11 = m.group(1) + m.group(2)
            dob, extra = _try_parse_legacy(digits11)
            if dob is not None:
                return ParsedID(
                    country_code="LV",
                    id_number=digits11,
                    id_type="PERSONAS_KODS",
                    dob=dob,
                    gender=None,
                    extra=extra,
                )

            # Not a valid legacy-encoded DOB => treat as modern/randomized code
            return ParsedID(country_code="LV", id_number=digits11, id_type="PERSONAS_KODS", dob=None, gender=None, extra={"date_encoded": False})

        # Modern (randomized) format: 11 digits
        if re.fullmatch(r"\d{11}", v):
            return ParsedID(country_code="LV", id_number=v, id_type="PERSONAS_KODS", dob=None, gender=None, extra={"date_encoded": False})

        raise ValidationError("Invalid LV personal code format")
