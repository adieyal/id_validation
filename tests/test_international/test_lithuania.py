import datetime as dt
import pytest

from id_validation.validate import ValidationError
from id_validation.validators.lt_asmenskodas import LithuaniaAsmensKodasValidator


def lt_checksum(first10: str) -> int:
    digits = [int(c) for c in first10]
    w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    w2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    r1 = sum(d * w for d, w in zip(digits, w1)) % 11
    if r1 != 10:
        return r1
    r2 = sum(d * w for d, w in zip(digits, w2)) % 11
    if r2 != 10:
        return r2
    return 0


def make_lt(g: int, dob: dt.date, serial: int) -> str:
    first10 = f"{g}{dob:%y%m%d}{serial:03d}"
    return first10 + str(lt_checksum(first10))


def test_lt_valid_parse_gender_and_dob():
    v = LithuaniaAsmensKodasValidator()
    idno = make_lt(5, dt.date(2001, 12, 31), 7)  # 5 => male, 2000s
    parsed = v.parse(idno)
    assert parsed.dob == dt.date(2001, 12, 31)
    assert parsed.gender == "M"
    assert parsed.extra["serial"] == 7
    assert v.validate(idno) is True


def test_lt_invalid_checksum():
    v = LithuaniaAsmensKodasValidator()
    idno = make_lt(3, dt.date(1988, 1, 15), 123)
    bad = idno[:-1] + ("0" if idno[-1] != "0" else "1")
    with pytest.raises(ValidationError):
        v.parse(bad)


def test_lt_invalid_date():
    v = LithuaniaAsmensKodasValidator()
    # Month 13 should fail
    with pytest.raises(ValidationError):
        v.parse("399133112345")
