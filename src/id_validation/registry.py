from __future__ import annotations

from .validate import Validator


VALIDATORS: dict[str, type[Validator]] = {}


def register(country_code: str):
    """Class decorator to register a validator for use by ValidatorFactory."""

    def _decorator(cls: type[Validator]) -> type[Validator]:
        VALIDATORS[country_code] = cls
        return cls

    return _decorator


def get(country_code: str) -> type[Validator]:
    if country_code not in VALIDATORS:
        raise ValueError("No validator for country code: " + country_code)
    return VALIDATORS[country_code]
