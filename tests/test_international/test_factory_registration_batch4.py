from id_validation import ValidatorFactory

from id_validation.validators.br_cpf import BrazilCPFValidator
from id_validation.validators.cl_rut import ChileRUTValidator
from id_validation.validators.hr_oib import CroatiaOIBValidator
from id_validation.validators.mx_curp import MexicoCURPValidator
from id_validation.validators.nl_bsn import NetherlandsBSNValidator
from id_validation.validators.pt_nif import PortugalNIFValidator
from id_validation.validators.si_emso import SloveniaEMSOValidator


def test_factory_registration_batch4():
    assert isinstance(ValidatorFactory.get_validator("MX"), MexicoCURPValidator)
    assert isinstance(ValidatorFactory.get_validator("NL"), NetherlandsBSNValidator)
    assert isinstance(ValidatorFactory.get_validator("PT"), PortugalNIFValidator)
    assert isinstance(ValidatorFactory.get_validator("SI"), SloveniaEMSOValidator)
    assert isinstance(ValidatorFactory.get_validator("HR"), CroatiaOIBValidator)
    assert isinstance(ValidatorFactory.get_validator("BR"), BrazilCPFValidator)
    assert isinstance(ValidatorFactory.get_validator("CL"), ChileRUTValidator)
