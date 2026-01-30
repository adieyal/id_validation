import datetime as dt
import pytest

from id_validation.validate_belgium import BelgiumNRNValidator
from id_validation.validate import ValidationError


def checksum97(base: int) -> int:
    r = base % 97
    return 97 - r if r != 0 else 97


def make_nrn(year: int, month: int, day: int, seq: int) -> str:
    yy = year % 100
    base9 = int(f"{yy:02d}{month:02d}{day:02d}{seq:03d}")
    if year >= 2000:
        cc = checksum97(2_000_000_000 + base9)
    else:
        cc = checksum97(base9)
    return f"{base9:09d}{cc:02d}"


def test_belgium_nrn_valid_parse_1900s():
    v = BelgiumNRNValidator()
    nrn = make_nrn(1978, 5, 2, 123)
    parsed = v.parse(nrn)
    assert parsed.dob == dt.date(1978, 5, 2)
    assert parsed.gender == "M"


def test_belgium_nrn_valid_parse_2000s():
    v = BelgiumNRNValidator()
    nrn = make_nrn(2003, 12, 31, 124)
    parsed = v.parse(nrn)
    assert parsed.dob == dt.date(2003, 12, 31)
    assert parsed.gender == "F"


def test_belgium_nrn_invalid_checksum():
    v = BelgiumNRNValidator()
    nrn = make_nrn(1978, 5, 2, 123)
    bad = nrn[:-2] + "00"
    with pytest.raises(ValidationError):
        v.parse(bad)
