from id_validation import ValidatorFactory

from id_validation.validators.cz_rodne_cislo import CzechRodneCisloValidator
from id_validation.validators.dk_cpr import DenmarkCPRValidator
from id_validation.validators.lt_asmenskodas import LithuaniaAsmensKodasValidator
from id_validation.validators.lv_personas_kods import LatviaPersonasKodsValidator
from id_validation.validators.sk_rodne_cislo import SlovakiaRodneCisloValidator


def test_factory_registration_new_eu_batch():
    assert isinstance(ValidatorFactory.get_validator("LT"), LithuaniaAsmensKodasValidator)
    assert isinstance(ValidatorFactory.get_validator("LV"), LatviaPersonasKodsValidator)
    assert isinstance(ValidatorFactory.get_validator("CZ"), CzechRodneCisloValidator)
    assert isinstance(ValidatorFactory.get_validator("SK"), SlovakiaRodneCisloValidator)
    assert isinstance(ValidatorFactory.get_validator("DK"), DenmarkCPRValidator)
