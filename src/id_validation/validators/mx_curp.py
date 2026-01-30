from __future__ import annotations

import datetime as _dt
import re
from typing import Any

from ..registry import register
from ..validate import ValidationError
from .base import BaseValidator, ParsedID


# CURP format (18 chars):
#  1-4  letters
#  5-10 YYMMDD
#  11   gender: H (hombre) / M (mujer)
#  12-13 state code
#  14-16 internal consonants
#  17   homonym disambiguator (0-9 for 1900-1999; A-Z for 2000-2099)
#  18   check digit
_CURP_RE = re.compile(r"^([A-Z][AEIOUX][A-Z]{2})(\d{2})(\d{2})(\d{2})([HM])([A-Z]{2})([A-Z]{3})([0-9A-Z])(\d)$")


_STATE_CODES: dict[str, str] = {
    "AS": "Aguascalientes",
    "BC": "Baja California",
    "BS": "Baja California Sur",
    "CC": "Campeche",
    "CL": "Coahuila",
    "CM": "Colima",
    "CS": "Chiapas",
    "CH": "Chihuahua",
    "DF": "Ciudad de México",  # historically Distrito Federal
    "DG": "Durango",
    "GT": "Guanajuato",
    "GR": "Guerrero",
    "HG": "Hidalgo",
    "JC": "Jalisco",
    "MC": "México",
    "MN": "Michoacán",
    "MS": "Morelos",
    "NT": "Nayarit",
    "NL": "Nuevo León",
    "OC": "Oaxaca",
    "PL": "Puebla",
    "QT": "Querétaro",
    "QR": "Quintana Roo",
    "SP": "San Luis Potosí",
    "SL": "Sinaloa",
    "SR": "Sonora",
    "TC": "Tabasco",
    "TS": "Tamaulipas",
    "TL": "Tlaxcala",
    "VZ": "Veracruz",
    "YN": "Yucatán",
    "ZS": "Zacatecas",
    "NE": "Nacido en el Extranjero",
}


# Mapping for check digit calculation.
# Source commonly published by RENAPO/SEGOB documentation.
_CHAR_VALUES = {ch: i for i, ch in enumerate("0123456789ABCDEFGHIJKLMN\u00d1OPQRSTUVWXYZ")}


def _curp_check_digit(first_17: str) -> int:
    # Sum(value(char_i) * (18 - i)) for i=1..17, then (10 - (sum % 10)) % 10
    s = 0
    for i, ch in enumerate(first_17, start=1):
        if ch not in _CHAR_VALUES:
            raise ValidationError("Invalid character for checksum")
        s += _CHAR_VALUES[ch] * (18 - i)
    return (10 - (s % 10)) % 10


def _decode_year(yy: int, homonym: str) -> int:
    # Homonym character (position 17) differentiates century:
    #  - digit: 1900-1999
    #  - letter: 2000-2099
    if homonym.isdigit():
        return 1900 + yy
    return 2000 + yy


@register("MX")
class MexicoCURPValidator(BaseValidator):
    """Mexico CURP (Clave \u00danica de Registro de Poblaci\u00f3n)."""

    country_code = "MX"

    def normalize(self, id_number: str) -> str:
        return re.sub(r"\s+", "", id_number.strip()).upper()

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)
        m = _CURP_RE.match(v)
        if not m:
            raise ValidationError("Invalid CURP format")

        yy = int(m.group(2))
        mm = int(m.group(3))
        dd = int(m.group(4))
        gender_raw = m.group(5)
        state = m.group(6)
        homonym = m.group(8)
        check_digit = int(m.group(9))

        if state not in _STATE_CODES:
            raise ValidationError("Invalid state code")

        year = _decode_year(yy, homonym)
        try:
            dob = _dt.date(year, mm, dd)
        except ValueError as e:
            raise ValidationError("Invalid date of birth") from e

        expected = _curp_check_digit(v[:17])
        if check_digit != expected:
            raise ValidationError("Invalid checksum")

        gender = "M" if gender_raw == "H" else "F"

        extra: dict[str, Any] = {
            "state_code": state,
            "state_name": _STATE_CODES[state],
            "homonym": homonym,
            "checksum": expected,
        }
        return ParsedID(country_code="MX", id_number=v, id_type="CURP", dob=dob, gender=gender, extra=extra)
