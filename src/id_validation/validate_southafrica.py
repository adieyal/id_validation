from __future__ import annotations

import datetime as _dt
from enum import Enum
from typing import Any

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID


class SouthAfricaValidationError(ValidationError):
    pass


class Race(Enum):
    """Apartheid-era race classification codes."""

    WHITE = 0
    CAPE_COLOURED = 1
    MALAY = 2
    GRIQUA = 3
    CHINESE = 4
    INDIAN = 5
    OTHER_ASIATIC = 6
    OTHER_COLOURED = 7
    BLACK = 9


class CitizenshipType(Enum):
    """Citizenship status codes."""

    CITIZEN = 0
    PERMANENT_RESIDENT = 1


_VALID_CITIZENSHIP_VALUES = {c.value for c in CitizenshipType}
_VALID_RACE_VALUES = {r.value for r in Race}


def _luhn_checksum(id_number: str) -> int:
    """Generate Luhn checksum digit for a 12-digit ID prefix."""
    digits = [int(d) for d in id_number]
    odd_digits = digits[-2::-2]
    even_digits = digits[-1::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return (10 - (checksum % 10)) % 10


def _validate_luhn(id_number: str) -> bool:
    """Validate the Luhn checksum of a 13-digit ID number."""
    check_digit = int(id_number[-1])
    return check_digit == _luhn_checksum(id_number[:-1])


def _parse_dob(id_number: str) -> _dt.date:
    """Parse date of birth from ID number (first 6 digits: YYMMDD)."""
    year_2d = int(id_number[0:2])
    month = int(id_number[2:4])
    day = int(id_number[4:6])

    # Y2K handling: years less than current 2-digit year are 2000s
    current_year_2d = _dt.date.today().year % 100
    year = 2000 + year_2d if year_2d < current_year_2d else 1900 + year_2d

    try:
        return _dt.date(year, month, day)
    except ValueError as e:
        raise SouthAfricaValidationError("Invalid date of birth") from e


def _parse_gender(id_number: str) -> str:
    """Parse gender from ID number (digit 7: 0-4=F, 5-9=M)."""
    gender_digit = int(id_number[6])
    return "F" if gender_digit < 5 else "M"


def _base_parse(id_number: str) -> tuple[str, _dt.date, str, int]:
    """Common parsing for all South African ID types.

    Returns: (normalized_id, dob, gender, checksum)
    """
    v = id_number.strip().replace(" ", "")

    if len(v) != 13 or not v.isdigit():
        raise SouthAfricaValidationError("Invalid ID format: must be 13 digits")

    if not _validate_luhn(v):
        raise SouthAfricaValidationError("Invalid checksum")

    dob = _parse_dob(v)
    gender = _parse_gender(v)
    checksum = int(v[-1])

    return v, dob, gender, checksum


@register("ZA")
class PostApartheidSouthAfricaValidator(BaseValidator):
    """Post-apartheid South African ID validator.

    Validates 13-digit ID numbers issued after 1986 that include
    citizenship status but not race classification.
    """

    country_code = "ZA"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v, dob, gender, checksum = _base_parse(id_number)

        citizenship_digit = int(v[10])
        if citizenship_digit not in _VALID_CITIZENSHIP_VALUES:
            raise SouthAfricaValidationError("Invalid citizenship digit")

        citizenship = CitizenshipType(citizenship_digit)

        return ParsedID(
            country_code="ZA",
            id_number=v,
            id_type="NATIONAL_ID",
            dob=dob,
            gender=gender,
            extra={
                "citizenship": citizenship.name,
                "citizenship_code": citizenship_digit,
                "checksum": checksum,
            },
        )


@register("ZA_OLD")
class ApartheidSouthAfricaValidator(BaseValidator):
    """Apartheid-era South African ID validator.

    Validates 13-digit ID numbers that include both race classification
    and citizenship status, as used during the apartheid era.
    """

    country_code = "ZA_OLD"

    def normalize(self, id_number: str) -> str:
        return id_number.strip().replace(" ", "")

    def parse(self, id_number: str) -> ParsedID:
        v, dob, gender, checksum = _base_parse(id_number)

        citizenship_digit = int(v[10])
        race_digit = int(v[11])

        if race_digit not in _VALID_RACE_VALUES:
            raise SouthAfricaValidationError("Invalid race digit")

        race = Race(race_digit)
        citizenship = CitizenshipType(citizenship_digit) if citizenship_digit in _VALID_CITIZENSHIP_VALUES else None

        extra: dict[str, Any] = {
            "race": race.name,
            "race_code": race_digit,
            "checksum": checksum,
        }

        if citizenship is not None:
            extra["citizenship"] = citizenship.name
            extra["citizenship_code"] = citizenship_digit

        return ParsedID(
            country_code="ZA_OLD",
            id_number=v,
            id_type="NATIONAL_ID",
            dob=dob,
            gender=gender,
            extra=extra,
        )


# Re-export for backwards compatibility
RACE = Race
CITIZENSHIP_TYPE = CitizenshipType
