from id_validation import ValidatorFactory

from id_validation.validators.ar_cuit_cuil import ArgentinaCUITCUILValidator
from id_validation.validators.ca_sin import CanadaSINValidator
from id_validation.validators.co_nit import ColombiaNITValidator
from id_validation.validators.ec_cedula import EcuadorCedulaValidator


def test_factory_registration_batch5():
    assert isinstance(ValidatorFactory.get_validator("CA"), CanadaSINValidator)
    assert isinstance(ValidatorFactory.get_validator("AR"), ArgentinaCUITCUILValidator)
    assert isinstance(ValidatorFactory.get_validator("CO"), ColombiaNITValidator)
    assert isinstance(ValidatorFactory.get_validator("EC"), EcuadorCedulaValidator)
