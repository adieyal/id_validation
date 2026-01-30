from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


_NRN_RE = re.compile(r"^(\d{2})(\d{2})(\d{2})(\d{3})(\d{2})$")


def _checksum97(base: int) -> int:
    r = base % 97
    return 97 - r if r != 0 else 97


@register("BE")
class BelgiumNRNValidator(BaseValidator):
    """Belgian National Register Number (NRN / Rijksregisternummer).

    Format: YYMMDDXXXCC where CC is checksum.
    For people born in/after 2000, checksum is computed on 2_000_000_000 + YYMMDDXXX.
    """

    country_code = "BE"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "").replace("-", "").replace(".", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _NRN_RE.match(v)
        if not m:
            raise ValidationError("Invalid NRN format")

        yy, mm, dd, seq, cc = m.groups()
        base9 = int(yy + mm + dd + seq)
        checksum = int(cc)

        # Determine which century by matching checksum.
        expected_1900 = _checksum97(base9)
        expected_2000 = _checksum97(2_000_000_000 + base9)

        if checksum == expected_1900:
            year = 1900 + int(yy)
        elif checksum == expected_2000:
            year = 2000 + int(yy)
        else:
            raise ValidationError("Invalid checksum")

        try:
            dob = _dt.date(year, int(mm), int(dd))
        except ValueError as e:
            raise ValidationError("Invalid date") from e

        gender = "M" if int(seq) % 2 == 1 else "F"
        extra: dict[str, Any] = {
            "sequence": int(seq),
            "checksum": checksum,
        }
        return ParsedID(country_code="BE", id_number=v, id_type="NRN", dob=dob, gender=gender, extra=extra)
