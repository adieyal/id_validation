import datetime as dt

from id_validation import ValidatorFactory


def test_nl_bsn_valid_and_invalid():
    v = ValidatorFactory.get_validator("NL")
    assert v.validate("123456782")
    assert v.validate("087880532")

    assert not v.validate("123456781")
    assert not v.validate("000000000")


def test_pt_nif_valid_and_invalid():
    v = ValidatorFactory.get_validator("PT")
    assert v.validate("501964843")

    assert not v.validate("501964844")


def test_si_emso_valid_and_invalid():
    v = ValidatorFactory.get_validator("SI")

    emso = "0101004500009"  # 2004-01-01, region 50, serial 000
    assert v.validate(emso)
    data = v.extract_data(emso)
    assert data["dob"] == dt.date(2004, 1, 1)
    assert data["gender"] == "M"
    assert data["region_code"] == 50

    assert not v.validate(emso[:-1] + "0")


def test_hr_oib_valid_and_invalid():
    v = ValidatorFactory.get_validator("HR")
    assert v.validate("33392005961")
    assert not v.validate("33392005962")
