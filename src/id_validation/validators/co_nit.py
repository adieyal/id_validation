from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


# Accept either: NNNNNNNNN-DV or NNNNNNNNNDV (DV is 0-9)
_NIT_RE = re.compile(r"^(\d{1,15})(?:-(\d))?$")

# DIAN mod-11 weights (applied from right to left)
_WEIGHTS = [71, 67, 59, 53, 47, 43, 41, 37, 29, 23, 19, 17, 13, 7, 3]


def _nit_dv(base: str) -> int:
    # Multiply digits (right-to-left) by corresponding weights (from the end of _WEIGHTS)
    if not base.isdigit():
        raise ValidationError("Invalid NIT")
    if len(base) > len(_WEIGHTS):
        raise ValidationError("NIT too long")

    s = 0
    # align weights to length
    weights = _WEIGHTS[-len(base) :]
    for d, w in zip(base, weights):
        s += int(d) * w

    r = s % 11
    if r in (0, 1):
        return r
    return 11 - r


@register("CO")
class ColombiaNITValidator(BaseValidator):
    """Colombia NIT (Número de Identificación Tributaria)."""

    country_code = "CO"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        base: str
        dv_str: str | None

        if "-" in v:
            m = _NIT_RE.match(v)
            if not m:
                raise ValidationError("Invalid NIT format")
            base = m.group(1)
            dv_str = m.group(2)
        else:
            # If no hyphen, treat the last digit as DV.
            if not v.isdigit() or len(v) < 2:
                raise ValidationError("Invalid NIT format")
            base, dv_str = v[:-1], v[-1]

        if dv_str is None:
            raise ValidationError("Missing check digit")

        expected = _nit_dv(base)
        if int(dv_str) != expected:
            raise ValidationError("Invalid checksum")

        return ParsedID(
            country_code="CO",
            id_number=f"{base}-{dv_str}",
            id_type="NIT",
            extra={"base": base, "dv": int(dv_str), "checksum": expected},
        )
