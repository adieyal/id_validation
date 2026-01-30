from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..validate import ValidationError, Validator


@dataclass(frozen=True)
class ParsedID:
    """Common structured output for parsed identity numbers.

    Not all fields apply to all countries.
    """

    country_code: str
    id_number: str
    id_type: Optional[str] = None

    # Common decoded fields
    dob: Any | None = None  # typically datetime.date
    gender: str | None = None  # 'M'|'F' or other country-specific

    # Additional decoded metadata (region codes, municipality codes, etc.)
    extra: Dict[str, Any] | None = None


class BaseValidator(Validator):
    country_code: str = ""

    def normalize(self, id_number: str) -> str:
        return id_number.strip()

    def validate(self, id_number: str) -> bool:
        try:
            self.parse(id_number)
            return True
        except ValidationError:
            return False

    def parse(self, id_number: str) -> ParsedID:
        raise NotImplementedError

    def extract_data(self, id_number: str) -> dict[str, Any]:
        """Backwards-compatible API: returns a dict (existing tests use this pattern)."""
        parsed = self.parse(id_number)
        data: dict[str, Any] = {}
        if parsed.dob is not None:
            data["dob"] = parsed.dob
        if parsed.gender is not None:
            data["gender"] = parsed.gender
        if parsed.id_type is not None:
            data["type"] = parsed.id_type
        if parsed.extra:
            data.update(parsed.extra)
        return data
