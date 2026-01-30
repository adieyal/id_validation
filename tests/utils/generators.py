"""Test utilities for generating valid ID numbers.

These generators are for testing purposes only and should not be used
in production code.
"""

from __future__ import annotations

import datetime as _dt
import random
from enum import Enum, auto


class Gender(Enum):
    MALE = auto()
    FEMALE = auto()


class CitizenshipType(Enum):
    CITIZEN = 0
    PERMANENT_RESIDENT = 1


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


def _luhn_checksum(id_number: str) -> int:
    """Generate Luhn checksum digit."""
    digits = [int(d) for d in id_number]
    odd_digits = digits[-2::-2]
    even_digits = digits[-1::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return (10 - (checksum % 10)) % 10


def generate_south_africa_id(
    dob: _dt.datetime | None = None,
    gender: Gender | None = None,
    citizenship: CitizenshipType | None = None,
) -> str:
    """Generate a valid post-apartheid South African ID number.

    Args:
        dob: Date of birth (random if not provided)
        gender: Gender (random if not provided)
        citizenship: Citizenship type (random if not provided)

    Returns:
        A valid 13-digit South African ID number
    """
    start_date = _dt.datetime(1900, 1, 1)
    end_date = _dt.datetime.now()

    if dob is None:
        timestamp = start_date.timestamp() + random.random() * (end_date.timestamp() - start_date.timestamp())
        dob = _dt.datetime.fromtimestamp(timestamp)

    if gender is None:
        gender = random.choice(list(Gender))

    if citizenship is None:
        citizenship = random.choice(list(CitizenshipType))

    gender_digit = random.randint(0, 4) if gender == Gender.FEMALE else random.randint(5, 9)
    sequence = "".join(str(i) for i in random.sample(range(10), 3))

    idno = dob.strftime("%y%m%d") + str(gender_digit) + sequence + str(citizenship.value) + random.choice("78")
    idno += str(_luhn_checksum(idno))

    return idno


def generate_apartheid_south_africa_id(
    dob: _dt.datetime | None = None,
    gender: Gender | None = None,
    race: Race | None = None,
    citizenship: CitizenshipType | None = None,
) -> str:
    """Generate a valid apartheid-era South African ID number.

    Args:
        dob: Date of birth (random if not provided)
        gender: Gender (random if not provided)
        race: Race classification (random if not provided)
        citizenship: Citizenship type (random if not provided)

    Returns:
        A valid 13-digit apartheid-era South African ID number
    """
    start_date = _dt.datetime(1900, 1, 1)
    end_date = _dt.datetime.now()

    if dob is None:
        timestamp = start_date.timestamp() + random.random() * (end_date.timestamp() - start_date.timestamp())
        dob = _dt.datetime.fromtimestamp(timestamp)

    if gender is None:
        gender = random.choice(list(Gender))

    if race is None:
        race = random.choice(list(Race))

    if citizenship is None:
        citizenship = random.choice(list(CitizenshipType))

    gender_digit = random.randint(0, 4) if gender == Gender.FEMALE else random.randint(5, 9)
    sequence = "".join(str(i) for i in random.sample(range(10), 3))

    idno = dob.strftime("%y%m%d") + str(gender_digit) + sequence + str(citizenship.value) + str(race.value)
    idno += str(_luhn_checksum(idno))

    return idno
