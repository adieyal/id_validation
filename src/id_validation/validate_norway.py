from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


_FNR_RE = re.compile(r"^(\d{2})(\d{2})(\d{2})(\d{3})(\d{2})$")


def _mod11_control(digits: list[int], weights: list[int]) -> int | None:
    s = sum(d * w for d, w in zip(digits, weights))
    r = s % 11
    k = 11 - r
    if k == 11:
        return 0
    if k == 10:
        return None
    return k


@register("NO")
class NorwayFodselsnummerValidator(BaseValidator):
    """Norway fødselsnummer (national identity number) validator."""

    country_code = "NO"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _FNR_RE.match(v)
        if not m:
            raise ValidationError("Invalid fødselsnummer format")

        dd, mm, yy, individ_s, kk = m.groups()
        individ = int(individ_s)
        k1 = int(kk[0])
        k2 = int(kk[1])

        year = self._infer_year(int(yy), individ)
        try:
            dob = _dt.date(year, int(mm), int(dd))
        except ValueError as e:
            raise ValidationError("Invalid date") from e

        digits = [int(ch) for ch in v]
        k1_expected = _mod11_control(digits[:9], [3, 7, 6, 1, 8, 9, 4, 5, 2])
        if k1_expected is None or k1_expected != k1:
            raise ValidationError("Invalid control digit 1")

        k2_expected = _mod11_control(digits[:10], [5, 4, 3, 2, 7, 6, 5, 4, 3, 2])
        if k2_expected is None or k2_expected != k2:
            raise ValidationError("Invalid control digit 2")

        gender = "M" if individ % 2 == 1 else "F"
        extra: dict[str, Any] = {
            "individual_number": individ,
            "control_digits": (k1, k2),
        }
        return ParsedID(country_code="NO", id_number=v, id_type="FODSELSNUMMER", dob=dob, gender=gender, extra=extra)

    def _infer_year(self, yy: int, individ: int) -> int:
        # Century inference rules based on individ range.
        # Source: common Skatteetaten rules.
        if 0 <= individ <= 499:
            return 1900 + yy
        if 500 <= individ <= 749 and yy >= 54:
            return 1800 + yy
        if 900 <= individ <= 999 and yy >= 40:
            return 1900 + yy
        if 500 <= individ <= 999 and yy <= 39:
            return 2000 + yy
        raise ValidationError("Cannot infer century from individ/yy")
