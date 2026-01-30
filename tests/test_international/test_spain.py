import pytest

from id_validation.validate_spain import SpainDNINIEValidator
from id_validation.validate import ValidationError


LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


def make_dni(num: int) -> str:
    return f"{num:08d}{LETTERS[num % 23]}"


def make_nie(prefix: str, digits7: int) -> str:
    pmap = {"X": "0", "Y": "1", "Z": "2"}
    num = int(pmap[prefix] + f"{digits7:07d}")
    return f"{prefix}{digits7:07d}{LETTERS[num % 23]}"


def test_spain_dni_valid():
    v = SpainDNINIEValidator()
    dni = make_dni(12345678)
    assert v.validate(dni) is True
    parsed = v.parse(dni)
    assert parsed.id_type == "DNI"


def test_spain_nie_valid():
    v = SpainDNINIEValidator()
    nie = make_nie("X", 1234567)
    parsed = v.parse(nie)
    assert parsed.id_type == "NIE"


def test_spain_invalid_letter():
    v = SpainDNINIEValidator()
    dni = make_dni(12345678)
    bad = dni[:-1] + ("A" if dni[-1] != "A" else "B")
    with pytest.raises(ValidationError):
        v.parse(bad)
