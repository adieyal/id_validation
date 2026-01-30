from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


# Allow 2A/2B department for Corsica in the 13-char body.
_NIR_RE = re.compile(r"^([12])\s*(\d{2})\s*(\d{2})\s*([0-9AB]{2})\s*(\d{3})\s*(\d{3})\s*(\d{2})$")


def _nir_numeric_body(sex: str, yy: str, mm: str, dept: str, commune: str, order: str) -> int:
    dept = dept.upper()
    if dept == "2A":
        dept_num = "19"
    elif dept == "2B":
        dept_num = "18"
    else:
        dept_num = dept

    if not dept_num.isdigit():
        raise ValidationError("Invalid department code")

    body = f"{sex}{yy}{mm}{dept_num}{commune}{order}"
    return int(body)


@register("FR")
class FranceNIRValidator(BaseValidator):
    """France NIR (Numéro d'inscription au répertoire), a.k.a. INSEE number.

    Format: 13-char body + 2-digit key.
    Key = 97 - (numeric_body % 97)
    For Corsica, 2A->19 and 2B->18 for key calculation.
    """

    country_code = "FR"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().upper().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        raw = id_number.strip().upper()
        m = _NIR_RE.match(raw)
        if not m:
            # Try compact form as well
            compact = self.normalize(id_number)
            m = re.match(r"^([12])(\d{2})(\d{2})([0-9AB]{2})(\d{3})(\d{3})(\d{2})$", compact)
        if not m:
            raise ValidationError("Invalid NIR format")

        sex, yy, mm, dept, commune, order, key_s = m.groups()
        key = int(key_s)

        # Month may have special values in some cases; implement strict 01-12 for now.
        month = int(mm)
        if month < 1 or month > 12:
            raise ValidationError("Invalid month")

        body_num = _nir_numeric_body(sex, yy, mm, dept, commune, order)
        expected_key = 97 - (body_num % 97)
        if expected_key == 97:
            expected_key = 0

        if key != expected_key:
            raise ValidationError("Invalid key")

        # Year: infer century (heuristic). NIR encodes 2-digit year only.
        today = _dt.date.today()
        current_yy = today.year % 100
        year = (today.year - (today.year % 100)) + int(yy)
        if int(yy) > current_yy:
            year -= 100

        # Use day=1 since NIR does not include day.
        dob = _dt.date(year, month, 1)

        gender = "M" if sex == "1" else "F"
        extra: dict[str, Any] = {
            "department": dept,
            "commune": commune,
            "order": order,
            "key": key,
            "year": year,
            "month": month,
        }
        return ParsedID(country_code="FR", id_number=self.normalize(id_number), id_type="NIR", dob=dob, gender=gender, extra=extra)
