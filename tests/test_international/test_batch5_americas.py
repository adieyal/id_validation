import pytest

from id_validation import ValidatorFactory


def test_ca_sin_valid_and_invalid():
    v = ValidatorFactory.get_validator("CA")
    assert v.validate("046 454 286")
    assert v.validate("046-454-286")

    assert not v.validate("046454287")
    assert not v.validate("123")


def test_ar_cuit_cuil_valid_and_invalid_with_types():
    v = ValidatorFactory.get_validator("AR")

    cuil = "20-12345678-6"
    assert v.validate(cuil)
    data = v.extract_data(cuil)
    assert data["prefix"] == "20"
    assert data["dni"] == "12345678"
    assert data["category"] == "individual"

    cuit_company = "30-12345678-1"
    assert v.validate(cuit_company)
    data2 = v.extract_data(cuit_company)
    assert data2["prefix"] == "30"
    assert data2["category"] == "company"

    assert not v.validate("20-12345678-0")


def test_co_nit_valid_and_invalid():
    v = ValidatorFactory.get_validator("CO")

    assert v.validate("900373913-4")
    assert v.validate("9003739134")

    assert not v.validate("900373913-5")
    assert not v.validate("900373913")  # missing DV


def test_ec_cedula_valid_and_invalid_extracts_province():
    v = ValidatorFactory.get_validator("EC")

    ced = "1712345675"
    assert v.validate(ced)
    data = v.extract_data(ced)
    assert data["province_code"] == "17"
    assert data["province_name"] == "Pichincha"
    assert data["third_digit"] == 1

    assert not v.validate("0012345678")  # invalid province
    assert not v.validate("1712345676")  # bad checksum
    assert not v.validate("1762345675")  # unsupported third digit (>=6)
