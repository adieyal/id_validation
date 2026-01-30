import datetime as dt
import pytest

from id_validation.validate_sweden import SwedenPersonnummerValidator
from id_validation.validate import ValidationError


def luhn_digit(num: str) -> int:
    total = 0
    for i, ch in enumerate(num):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - (total % 10)) % 10


def make_pnr_10(yy, mm, dd, nnn: str) -> str:
    base = f"{yy:02d}{mm:02d}{dd:02d}{nnn}"
    return base + str(luhn_digit(base))


def test_sweden_personnummer_valid_parse():
    v = SwedenPersonnummerValidator()
    # 12 Oct 1985 (heuristic century), male because nnn last digit odd
    body10 = make_pnr_10(85, 10, 12, "123")
    formatted = body10[:6] + "-" + body10[6:]
    parsed = v.parse(formatted)
    assert parsed.dob.month == 10 and parsed.dob.day == 12
    assert parsed.gender == "M"


def test_sweden_personnummer_invalid_checksum():
    v = SwedenPersonnummerValidator()
    body10 = make_pnr_10(85, 10, 12, "123")
    bad = body10[:-1] + ("0" if body10[-1] != "0" else "1")
    with pytest.raises(ValidationError):
        v.parse(bad)
