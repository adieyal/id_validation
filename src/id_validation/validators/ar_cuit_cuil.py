from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_AR_RE = re.compile(r"^(\d{11})$")

# Common prefix categories (not exhaustive; used for best-effort type hinting)
_INDIVIDUAL_PREFIXES = {"20", "23", "24", "27"}
_COMPANY_PREFIXES = {"30", "33", "34"}

_WEIGHTS = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]


def _check_digit(first10: str) -> int:
    s = sum(int(d) * w for d, w in zip(first10, _WEIGHTS))
    r = 11 - (s % 11)
    if r == 11:
        return 0
    if r == 10:
        return 9
    return r


@register("AR")
class ArgentinaCUITCUILValidator(BaseValidator):
    """Argentina CUIT/CUIL.

    Both CUIT and CUIL share the same 11-digit structure and checksum.
    """

    country_code = "AR"

    def normalize(self, id_number: str) -> str:
        # Accept hyphenated forms: XX-XXXXXXXX-X
        v = id_number.strip()
        v = re.sub(r"[^0-9]", "", v)
        return v

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _AR_RE.match(v):
            raise ValidationError("Invalid CUIT/CUIL format")

        prefix = v[0:2]
        dni = v[2:10]
        expected = _check_digit(v[:10])
        if int(v[10]) != expected:
            raise ValidationError("Invalid checksum")

        # Best-effort type hint based on prefix.
        if prefix in _COMPANY_PREFIXES:
            id_type = "CUIT"
            category = "company"
        elif prefix in _INDIVIDUAL_PREFIXES:
            # Individuals commonly have CUIL, but CUIT also exists.
            id_type = "CUIL"
            category = "individual"
        else:
            id_type = "CUIT/CUIL"
            category = "unknown"

        return ParsedID(
            country_code="AR",
            id_number=v,
            id_type=id_type,
            extra={
                "prefix": prefix,
                "dni": dni,
                "category": category,
                "checksum": expected,
            },
        )
