from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_NIF_RE = re.compile(r"^(\d{9})$")


def _nif_check_digit(first_8: list[int]) -> int:
    # Mod 11 with weights 9..2
    weights = list(range(9, 1, -1))
    s = sum(d * w for d, w in zip(first_8, weights))
    r = 11 - (s % 11)
    return 0 if r >= 10 else r


@register("PT")
class PortugalNIFValidator(BaseValidator):
    """Portugal NIF (Número de Identificação Fiscal)."""

    country_code = "PT"

    def normalize(self, id_number: str) -> str:
        return re.sub(r"\s+", "", id_number.strip())

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _NIF_RE.match(v):
            raise ValidationError("Invalid NIF format")

        digits = [int(ch) for ch in v]
        expected = _nif_check_digit(digits[:8])
        if digits[8] != expected:
            raise ValidationError("Invalid checksum")

        # Type/prefix rules exist (first digit/first 2 digits), but are not universally enforced.
        return ParsedID(country_code="PT", id_number=v, id_type="NIF", extra={"checksum": expected})
