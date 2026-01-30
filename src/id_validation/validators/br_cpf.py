from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_CPF_RE = re.compile(r"^(\d{11})$")


def _calc_check_digit(digits: list[int], weights: list[int]) -> int:
    s = sum(d * w for d, w in zip(digits, weights))
    r = 11 - (s % 11)
    return 0 if r >= 10 else r


@register("BR")
class BrazilCPFValidator(BaseValidator):
    """Brazil CPF (Cadastro de Pessoas Físicas)."""

    country_code = "BR"

    def normalize(self, id_number: str) -> str:
        # Accept common formatting: 000.000.000-00
        v = id_number.strip()
        v = re.sub(r"[^0-9]", "", v)
        return v

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _CPF_RE.match(v):
            raise ValidationError("Invalid CPF format")

        digits = [int(ch) for ch in v]
        if len(set(digits)) == 1:
            # Disallow obvious invalid CPFs like 00000000000, 11111111111, ...
            raise ValidationError("Invalid CPF")

        d1 = _calc_check_digit(digits[:9], list(range(10, 1, -1)))
        d2 = _calc_check_digit(digits[:10], list(range(11, 1, -1)))
        if digits[9] != d1 or digits[10] != d2:
            raise ValidationError("Invalid checksum")

        return ParsedID(country_code="BR", id_number=v, id_type="CPF", extra={"check_digits": (d1, d2)})
