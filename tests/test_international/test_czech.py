import datetime as dt
import pytest

from id_validation.validate import ValidationError
from id_validation.validators.cz_rodne_cislo import CzechRodneCisloValidator


def make_rc10(date: dt.date, extension: int, female: bool = False, special: bool = False) -> str:
    yy = date.year % 100
    mm = date.month + (50 if female else 0) + (20 if special else 0)
    dd = date.day
    base9 = f"{yy:02d}{mm:02d}{dd:02d}{extension:03d}"
    check = int(base9) % 11
    if check == 10:
        check = 0
    return base9 + str(check)


def test_cz_valid_10_digit_male():
    v = CzechRodneCisloValidator()
    idno = make_rc10(dt.date(2001, 1, 1), 123, female=False)
    parsed = v.parse(idno)
    assert parsed.dob == dt.date(2001, 1, 1)
    assert parsed.gender == "M"
    assert parsed.extra["checksum"] == int(idno[-1])


def test_cz_valid_10_digit_female_and_special_series():
    v = CzechRodneCisloValidator()
    idno = make_rc10(dt.date(2004, 12, 31), 7, female=True, special=True)
    parsed = v.parse(idno)
    assert parsed.dob == dt.date(2004, 12, 31)
    assert parsed.gender == "F"
    assert parsed.extra.get("special_series") is True


def test_cz_invalid_checksum():
    v = CzechRodneCisloValidator()
    idno = make_rc10(dt.date(2001, 1, 1), 123)
    bad = idno[:-1] + ("0" if idno[-1] != "0" else "1")
    with pytest.raises(ValidationError):
        v.parse(bad)
