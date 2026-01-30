import pytest

from id_validation.validate_france import FranceNIRValidator
from id_validation.validate import ValidationError


def make_nir(sex: str, yy: int, mm: int, dept: str, commune: str, order: str) -> str:
    dept_u = dept.upper()
    dept_num = {"2A": "19", "2B": "18"}.get(dept_u, dept_u)
    body = f"{sex}{yy:02d}{mm:02d}{dept_num}{commune}{order}"
    key = 97 - (int(body) % 97)
    if key == 97:
        key = 0
    # return with original dept formatting if Corsica
    body_display = f"{sex}{yy:02d}{mm:02d}{dept_u}{commune}{order}"
    return body_display + f"{key:02d}"


def test_france_nir_valid_parse_corsica_2a():
    v = FranceNIRValidator()
    nir = make_nir("1", 85, 7, "2A", "001", "123")
    parsed = v.parse(nir)
    assert parsed.gender == "M"
    assert parsed.extra["department"] == "2A"


def test_france_nir_invalid_key():
    v = FranceNIRValidator()
    nir = make_nir("2", 90, 12, "75", "001", "001")
    bad = nir[:-2] + "00"
    with pytest.raises(ValidationError):
        v.parse(bad)
