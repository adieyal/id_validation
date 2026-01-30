import datetime as dt
import pytest

from id_validation.validate_norway import NorwayFodselsnummerValidator
from id_validation.validate import ValidationError


def mod11_control(digits, weights):
    s = sum(d * w for d, w in zip(digits, weights))
    r = s % 11
    k = 11 - r
    if k == 11:
        return 0
    if k == 10:
        return None
    return k


def make_fnr(dd, mm, yy, individ):
    first9 = f"{dd:02d}{mm:02d}{yy:02d}{individ:03d}"
    digits = [int(c) for c in first9]
    k1 = mod11_control(digits, [3, 7, 6, 1, 8, 9, 4, 5, 2])
    if k1 is None:
        raise ValueError("cannot generate")
    digits10 = digits + [k1]
    k2 = mod11_control(digits10, [5, 4, 3, 2, 7, 6, 5, 4, 3, 2])
    if k2 is None:
        raise ValueError("cannot generate")
    return first9 + str(k1) + str(k2)


def test_norway_fodselsnummer_valid_parse():
    v = NorwayFodselsnummerValidator()
    # 1 Jan 1999 -> yy=99, individ within 000-499 => 1900+yy
    fnr = make_fnr(1, 1, 99, 123)
    parsed = v.parse(fnr)
    assert parsed.dob == dt.date(1999, 1, 1)
    assert parsed.gender == "M"


def test_norway_fodselsnummer_invalid_control_digit():
    v = NorwayFodselsnummerValidator()
    fnr = make_fnr(1, 1, 99, 123)
    bad = fnr[:-1] + ("0" if fnr[-1] != "0" else "1")
    with pytest.raises(ValidationError):
        v.parse(bad)
