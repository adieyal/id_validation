import datetime as dt
import pytest

from id_validation.validate_finland import FinlandHETUValidator
from id_validation.validate import ValidationError


def hetu(ddmmyy: str, century: str, individual: str) -> str:
    chars = "0123456789ABCDEFHJKLMNPRSTUVWXY"
    number = int(ddmmyy + individual)
    return f"{ddmmyy}{century}{individual}{chars[number % 31]}"


def test_finland_hetu_valid_and_parse():
    v = FinlandHETUValidator()
    idno = hetu("131052", "-", "308")  # 13 Oct 1952, female (even)
    parsed = v.parse(idno)
    assert parsed.dob == dt.date(1952, 10, 13)
    assert parsed.gender == "F"
    assert v.validate(idno) is True


def test_finland_hetu_invalid_checksum():
    v = FinlandHETUValidator()
    idno = hetu("131052", "-", "308")
    bad = idno[:-1] + ("0" if idno[-1] != "0" else "1")
    with pytest.raises(ValidationError):
        v.parse(bad)
