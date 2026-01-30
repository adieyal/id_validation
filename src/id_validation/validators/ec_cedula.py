from __future__ import annotations

import re

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


_CED_RE = re.compile(r"^(\d{10})$")

_PROVINCES: dict[str, str] = {
    "01": "Azuay",
    "02": "Bolívar",
    "03": "Cañar",
    "04": "Carchi",
    "05": "Cotopaxi",
    "06": "Chimborazo",
    "07": "El Oro",
    "08": "Esmeraldas",
    "09": "Guayas",
    "10": "Imbabura",
    "11": "Loja",
    "12": "Los Ríos",
    "13": "Manabí",
    "14": "Morona Santiago",
    "15": "Napo",
    "16": "Pastaza",
    "17": "Pichincha",
    "18": "Tungurahua",
    "19": "Zamora Chinchipe",
    "20": "Galápagos",
    "21": "Sucumbíos",
    "22": "Orellana",
    "23": "Santo Domingo de los Tsáchilas",
    "24": "Santa Elena",
}


def _cedula_check_digit(first9: str) -> int:
    # Modulo 10 algorithm for natural persons (3rd digit 0-5)
    coeffs = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    s = 0
    for d, c in zip(first9, coeffs):
        v = int(d) * c
        if v >= 10:
            v -= 9
        s += v
    return (10 - (s % 10)) % 10


@register("EC")
class EcuadorCedulaValidator(BaseValidator):
    """Ecuador cédula de identidad (natural persons, 10 digits)."""

    country_code = "EC"

    def normalize(self, id_number: str) -> str:
        return re.sub(r"\s+", "", id_number.strip())

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        if not _CED_RE.match(v):
            raise ValidationError("Invalid cédula format")

        province = v[0:2]
        third = int(v[2])
        if province not in _PROVINCES:
            raise ValidationError("Invalid province code")
        if third >= 6:
            raise ValidationError("Unsupported cédula type (third digit)")

        expected = _cedula_check_digit(v[:9])
        if int(v[9]) != expected:
            raise ValidationError("Invalid checksum")

        extra = {
            "province_code": province,
            "province_name": _PROVINCES[province],
            "third_digit": third,
            "serial": v[3:9],
            "checksum": expected,
        }
        return ParsedID(country_code="EC", id_number=v, id_type="CEDULA", extra=extra)
