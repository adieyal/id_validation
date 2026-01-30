from __future__ import annotations

import re
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


_DNI_RE = re.compile(r"^(\d{8})([A-Z])$")
_NIE_RE = re.compile(r"^([XYZ])(\d{7})([A-Z])$")

_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


@register("ES")
class SpainDNINIEValidator(BaseValidator):
    """Spain DNI (Documento Nacional de Identidad) / NIE validator.

    DNI: 8 digits + letter where letter = digits % 23.
    NIE: X/Y/Z + 7 digits + letter; X=0,Y=1,Z=2 prefixed for modulo.
    """

    country_code = "ES"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().upper().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)

        m = _DNI_RE.match(v)
        if m:
            num_s, letter = m.groups()
            num = int(num_s)
            expected = _LETTERS[num % 23]
            if letter != expected:
                raise ValidationError("Invalid DNI letter")
            extra: dict[str, Any] = {"number": num, "letter": letter}
            return ParsedID(country_code="ES", id_number=v, id_type="DNI", extra=extra)

        m = _NIE_RE.match(v)
        if m:
            prefix, digits7, letter = m.groups()
            prefix_map = {"X": "0", "Y": "1", "Z": "2"}
            num = int(prefix_map[prefix] + digits7)
            expected = _LETTERS[num % 23]
            if letter != expected:
                raise ValidationError("Invalid NIE letter")
            extra = {"prefix": prefix, "number": num, "letter": letter}
            return ParsedID(country_code="ES", id_number=v, id_type="NIE", extra=extra)

        raise ValidationError("Invalid DNI/NIE format")
