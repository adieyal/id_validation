import datetime as dt
import pytest

from id_validation.validate import ValidationError
from id_validation.validators.lv_personas_kods import LatviaPersonasKodsValidator


def test_lv_legacy_parse_dob():
    v = LatviaPersonasKodsValidator()
    parsed = v.parse("010203-11234")  # 01-02-1903 (century digit 1)
    assert parsed.dob == dt.date(1903, 2, 1)
    assert parsed.extra["century"] == 1900
    assert parsed.extra["serial"] == 1234


def test_lv_modern_no_dob():
    v = LatviaPersonasKodsValidator()
    parsed = v.parse("12345678901")
    assert parsed.dob is None
    assert parsed.extra["date_encoded"] is False


def test_lv_invalid_format():
    v = LatviaPersonasKodsValidator()
    with pytest.raises(ValidationError):
        v.parse("ABC")
