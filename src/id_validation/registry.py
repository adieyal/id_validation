from __future__ import annotations

from typing import Dict, Type

from .validate import Validator


VALIDATORS: Dict[str, Type[Validator]] = {}


def register(country_code: str):
    """Class decorator to register a validator for use by ValidatorFactory."""

    def _decorator(cls: Type[Validator]):
        VALIDATORS[country_code] = cls
        return cls

    return _decorator


def get(country_code: str) -> Type[Validator]:
    if country_code not in VALIDATORS:
        raise ValueError("No validator for country code: " + country_code)
    return VALIDATORS[country_code]
