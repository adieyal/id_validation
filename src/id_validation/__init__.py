from typing import TypedDict

from typing_extensions import Unpack

from .validate import Validator, ValidationError
from .registry import VALIDATORS, get as _get_validator_type


class ValidatorOptions(TypedDict, total=False):
    """Options that can be passed to validators."""

    strict_checksum: bool  # Used by DK (Denmark) CPR validator

# Import validators (side-effect: register with registry)
from .validate_botswana import BotswanaValidator
from .validate_nigeria import NigeriaValidator
from .validate_southafrica import ApartheidSouthAfricaValidator, PostApartheidSouthAfricaValidator
from .validate_zimbabwe import ZimbabweValidator

from .validate_finland import FinlandHETUValidator
from .validate_sweden import SwedenPersonnummerValidator
from .validate_norway import NorwayFodselsnummerValidator
from .validate_belgium import BelgiumNRNValidator
from .validate_france import FranceNIRValidator
from .validate_italy import ItalyCodiceFiscaleValidator
from .validate_spain import SpainDNINIEValidator

# Additional international validators (src/id_validation/validators/*)
from .validators.pl_pesel import PolandPESELValidator
from .validators.ro_cnp import RomaniaCNPValidator
from .validators.bg_egn import BulgariaEGNValidator
from .validators.ee_isikukood import EstoniaIsikukoodValidator
from .validators.tr_tckn import TurkeyTCKNValidator
from .validators.lt_asmenskodas import LithuaniaAsmensKodasValidator
from .validators.lv_personas_kods import LatviaPersonasKodsValidator
from .validators.cz_rodne_cislo import CzechRodneCisloValidator
from .validators.sk_rodne_cislo import SlovakiaRodneCisloValidator
from .validators.dk_cpr import DenmarkCPRValidator

from .validators.mx_curp import MexicoCURPValidator
from .validators.nl_bsn import NetherlandsBSNValidator
from .validators.pt_nif import PortugalNIFValidator
from .validators.si_emso import SloveniaEMSOValidator
from .validators.hr_oib import CroatiaOIBValidator
from .validators.br_cpf import BrazilCPFValidator
from .validators.cl_rut import ChileRUTValidator

from .validators.ca_sin import CanadaSINValidator
from .validators.ar_cuit_cuil import ArgentinaCUITCUILValidator
from .validators.co_nit import ColombiaNITValidator
from .validators.ec_cedula import EcuadorCedulaValidator

VERSION = "0.6.0"

__all__ = ["ValidatorFactory", "VALIDATORS", "ValidationError", "Validator"]


class ValidatorFactory:
    @staticmethod
    def get_validator(country_code: str, **kwargs: Unpack[ValidatorOptions]) -> Validator:
        """Get a validator instance for the given country code.

        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., "US", "FI", "DK")
            **kwargs: Validator-specific options (e.g., strict_checksum for DK)

        Returns:
            Validator instance for the specified country
        """
        cls = _get_validator_type(country_code)
        return cls(**kwargs)
