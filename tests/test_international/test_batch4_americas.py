import datetime as dt

import pytest

from id_validation import ValidatorFactory


def test_br_cpf_valid_and_invalid():
    v = ValidatorFactory.get_validator("BR")
    assert v.validate("529.982.247-25")
    assert v.validate("11144477735")

    assert not v.validate("111.111.111-11")  # repeated digits
    assert not v.validate("52998224724")  # bad check digit


def test_cl_rut_valid_and_invalid():
    v = ValidatorFactory.get_validator("CL")
    assert v.validate("76.086.428-5")
    assert v.validate("60803000-K")

    assert not v.validate("76086428-6")
    assert not v.validate("12.345.678-9")


def test_mx_curp_multiple_scenarios():
    v = ValidatorFactory.get_validator("MX")

    # 1990-01-01 (17th is digit => 1900s)
    curp_1990 = "GODE900101HDFRRN08"
    assert v.validate(curp_1990)
    data = v.extract_data(curp_1990)
    assert data["dob"] == dt.date(1990, 1, 1)
    assert data["gender"] == "M"
    assert data["state_code"] == "DF"

    # 2004-01-01 (17th is letter => 2000s)
    curp_2004 = "BADD040101MDFCCCA5"
    assert v.validate(curp_2004)
    data2 = v.extract_data(curp_2004)
    assert data2["dob"] == dt.date(2004, 1, 1)
    assert data2["gender"] == "F"

    # invalid checksum
    assert not v.validate(curp_1990[:-1] + "9")

    # invalid DOB (2003-02-29 doesn't exist, but checksum is correct)
    assert not v.validate("BADD030229MDFCCCA5")
