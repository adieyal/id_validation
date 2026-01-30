from __future__ import annotations

import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_TCKN_RE = re.compile(r"^(\d{11})$")


def _tckn_check_digit_10(d: list[int]) -> int:
    # d: 11 digits, use first 9
    odd_sum = d[0] + d[2] + d[4] + d[6] + d[8]
    even_sum = d[1] + d[3] + d[5] + d[7]
    return ((odd_sum * 7) - even_sum) % 10


def _tckn_check_digit_11(d: list[int]) -> int:
    return sum(d[:10]) % 10


@register("TR")
class TurkeyTCKNValidator(BaseValidator):
    """Turkey Republic Identification Number (T.C. Kimlik No)."""

    country_code = "TR"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _TCKN_RE.match(v):
            raise ValidationError("Invalid TCKN format")

        digits = [int(ch) for ch in v]
        if digits[0] == 0:
            raise ValidationError("Invalid TCKN: first digit cannot be 0")

        if digits[9] != _tckn_check_digit_10(digits):
            raise ValidationError("Invalid checksum (10th digit)")

        if digits[10] != _tckn_check_digit_11(digits):
            raise ValidationError("Invalid checksum (11th digit)")

        extra: dict[str, Any] = {
            "checksum10": digits[9],
            "checksum11": digits[10],
        }
        return ParsedID(country_code="TR", id_number=v, id_type="TCKN", extra=extra)
