import datetime as dt
import pytest

from id_validation.validate import ValidationError
from id_validation.validators.sk_rodne_cislo import SlovakiaRodneCisloValidator


def make_rc10(date: dt.date, extension: int, female: bool = False, special: bool = False) -> str:
    yy = date.year % 100
    mm = date.month + (50 if female else 0) + (20 if special else 0)
    dd = date.day
    base9 = f"{yy:02d}{mm:02d}{dd:02d}{extension:03d}"
    check = int(base9) % 11
    if check == 10:
        check = 0
    return base9 + str(check)


def test_sk_valid_10_digit_female():
    v = SlovakiaRodneCisloValidator()
    idno = make_rc10(dt.date(1999, 5, 20), 555, female=True)
    parsed = v.parse(idno)
    assert parsed.dob == dt.date(1999, 5, 20)
    assert parsed.gender == "F"


def test_sk_invalid_date():
    v = SlovakiaRodneCisloValidator()
    # Month 00 should fail
    with pytest.raises(ValidationError):
        v.parse("9900001230")
