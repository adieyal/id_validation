from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Validator(Protocol):
    """Protocol for country-specific ID validators."""

    def validate(self, id_number: str) -> bool:
        """Validates the given id number using a country-specific verification method."""
        ...

    def extract_data(self, id_number: str) -> dict[str, Any]:
        """Extracts any data encoded in the id number. This will be different for every country."""
        ...


class ValidationError(Exception):
    pass
