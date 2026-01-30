import datetime as dt
import pytest

from id_validation.validate_italy import ItalyCodiceFiscaleValidator
from id_validation.validate import ValidationError


def cf_check_char(cf15: str) -> str:
    odd_values = {
        **{str(i): v for i, v in enumerate([1, 0, 5, 7, 9, 13, 15, 17, 19, 21])},
        **dict(
            A=1,
            B=0,
            C=5,
            D=7,
            E=9,
            F=13,
            G=15,
            H=17,
            I=19,
            J=21,
            K=2,
            L=4,
            M=18,
            N=20,
            O=11,
            P=3,
            Q=6,
            R=8,
            S=12,
            T=14,
            U=16,
            V=10,
            W=22,
            X=25,
            Y=24,
            Z=23,
        ),
    }
    even_values = {**{str(i): i for i in range(10)}, **{chr(ord('A') + i): i for i in range(26)}}
    check_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    total = 0
    for idx, ch in enumerate(cf15, start=1):
        total += odd_values[ch] if idx % 2 == 1 else even_values[ch]
    return check_chars[total % 26]


def test_italy_codice_fiscale_valid_parse():
    v = ItalyCodiceFiscaleValidator()
    # Construct a syntactically-valid CF with known DOB and dummy municipality code.
    # Surname+name part doesn't affect DOB parsing.
    cf15 = "RSSMRA85M01H501"  # 1985-08? Actually month code M=8, day 01, municipality H501
    cf = cf15 + cf_check_char(cf15)
    parsed = v.parse(cf)
    assert parsed.gender == "M"
    assert parsed.dob.month == 8 and parsed.dob.day == 1
    assert parsed.extra["municipality_code"] == "H501"


def test_italy_codice_fiscale_invalid_checksum():
    v = ItalyCodiceFiscaleValidator()
    cf15 = "RSSMRA85M01H501"
    cf = cf15 + cf_check_char(cf15)
    bad = cf[:-1] + ("A" if cf[-1] != "A" else "B")
    with pytest.raises(ValidationError):
        v.parse(bad)
