from typing import Protocol

class Validator(Protocol):
    def validate(self, id_number: str) -> bool:
        """Validates the given id number using a country-specific verification method."""

    def extract_data(self, id_number: str) -> dict[str, str]:
        """Extracts any data encoded in the id number. This will be different for every country."""

class ValidationError(Exception):
    pass
