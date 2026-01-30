import datetime as dt
import pytest

from id_validation.validate import ValidationError
from id_validation.validators.dk_cpr import DenmarkCPRValidator


def cpr_checksum_ok(cpr10: str) -> bool:
    weights = [4, 3, 2, 7, 6, 5, 4, 3, 2, 1]
    s = sum(int(d) * w for d, w in zip(cpr10, weights))
    return s % 11 == 0


def find_valid_cpr_for_date(ddmmyy: str, serial_first_digit: int) -> str:
    # brute-force within the serial range for a mod-11 passing number
    for n in range(serial_first_digit * 1000, (serial_first_digit + 1) * 1000):
        cpr10 = ddmmyy + f"{n:04d}"
        if cpr_checksum_ok(cpr10):
            return cpr10
    raise RuntimeError("No CPR found")


def test_dk_lenient_checksum_by_default():
    v = DenmarkCPRValidator()
    # 010203 + serial starting with 4 => year 2003 (per century rule)
    parsed = v.parse("010203-4123")
    assert parsed.dob == dt.date(2003, 2, 1)
    assert parsed.gender in ("M", "F")
    assert "checksum_valid" in parsed.extra


def test_dk_strict_checksum_enforced():
    v = DenmarkCPRValidator(strict_checksum=True)
    cpr10 = find_valid_cpr_for_date("010203", 4)
    parsed = v.parse(cpr10)
    assert parsed.dob == dt.date(2003, 2, 1)
    assert parsed.extra["checksum_valid"] is True


def test_dk_invalid_date_rejected():
    v = DenmarkCPRValidator()
    with pytest.raises(ValidationError):
        v.parse("321399-1234")
