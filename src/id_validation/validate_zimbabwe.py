from __future__ import annotations

import re

from .registry import register
from .validate import ValidationError
from .validators.base import BaseValidator, ParsedID

# Source: Zimbabwe 2018 Elections Biometric Voters' Roll Analysis
# https://www.slideshare.net/povonews/zimbabwe-2018-biometric-voters-roll-analysis-pachedu
_REGION_LOOKUP: dict[str, str] = {
    "02": "Beitbridge",
    "03": "Mberengwa",
    "04": "Bikita",
    "05": "Bindura",
    "06": "Binga",
    "07": "Buhera",
    "08": "Bulawayo",
    "10": "Unknown",  # (Undetermined) (believed: Mhondoro-Ngezi)
    "11": "Muzarabani",
    "12": "Chivi",
    "13": "Chipinge",
    "14": "Chiredzi",
    "15": "Mazowe",
    "18": "Chikomba",
    "19": "Umzingwane",
    "21": "Insiza",
    "22": "Masvingo",
    "23": "Gokwe South",
    "24": "Kadoma",
    "25": "Goromonzi",
    "26": "Gokwe North",
    "27": "Gutu",
    "28": "Gwanda",
    "29": "Gweru",
    "32": "Chegutu",
    "34": "Nyanga",
    "35": "Bubi",
    "37": "Kariba",
    "38": "Hurungwe",
    "39": "Matobo",
    "41": "Lupane",
    "42": "Makoni",
    "43": "Marondera",
    "44": "Chimanimani",
    "45": "Mt. Darwin",
    "46": "Unknown",  # (Undetermined) (believed: Mbire)
    "47": "Murehwa",
    "48": "Mutoko",
    "49": "Mudzi",
    "50": "Mutasa",
    "53": "Nkayi",
    "54": "Mwenezi",
    "56": "Bulilimamangwe",
    "58": "Kwekwe",
    "59": "Seke",
    "61": "Rushinga",
    "63": "Harare",
    "66": "Shurugwi",
    "67": "Zvishavane",
    "68": "Shamva",
    "70": "Makonde",
    "71": "Guruve",
    "73": "Tsholotsho",
    "75": "Mutare",
    "77": "Chirumanzu",
    "79": "Hwange",
    "80": "Hwedza",
    "83": "Zaka",
    "84": "Umguza",
    "85": "U.M.P. (Uzumba, Maramba, Pfungwe)",
    "86": "Zvimba",
}

# Check letter lookup for mod-23 checksum
_CHECK_LETTER_LOOKUP: dict[int, str] = {
    1: "A", 2: "B", 3: "C", 4: "D",
    5: "E", 6: "F", 7: "G", 8: "H",
    9: "J", 10: "K", 11: "L", 12: "M",
    13: "N", 14: "P", 15: "Q", 16: "R",
    17: "S", 18: "T", 19: "V", 20: "W",
    21: "X", 22: "Y", 23: "Z",
}

_ALLOWED_LETTERS = "".join(_CHECK_LETTER_LOOKUP.values())
_ZW_RE = re.compile(rf"^\d{{2}}\d{{6,7}}[{_ALLOWED_LETTERS}]\d{{2}}$")

# Backwards compatibility export
REGION_LOOKUP = _REGION_LOOKUP


def _extract_parts(id_number: str) -> tuple[str, str, str, str]:
    """Extract parts from a cleaned Zimbabwe ID number."""
    registration_code = id_number[0:2]
    sequence_number = id_number[2:-3]
    check_letter = id_number[-3]
    district_code = id_number[-2:]
    return registration_code, sequence_number, check_letter, district_code


def _validate_checksum(id_number: str) -> bool:
    """Validate the checksum digit using mod 23."""
    registration_code, sequence_number, check_letter, _ = _extract_parts(id_number)
    check_number = int(registration_code + sequence_number)
    mod = check_number % 23
    expected = _CHECK_LETTER_LOOKUP.get(mod)
    return check_letter == expected


@register("ZW")
class ZimbabweValidator(BaseValidator):
    """Zimbabwe National ID validator.

    Validates region codes and uses modulus 23 checksum validation.
    """

    country_code = "ZW"

    def normalize(self, id_number: str) -> str:
        return id_number.replace("-", "").replace(" ", "").strip()

    def parse(self, id_number: str) -> ParsedID:
        v = self.normalize(id_number)

        if not _ZW_RE.match(v):
            raise ValidationError("Invalid Zimbabwe ID format")

        registration_code, sequence_number, check_letter, district_code = _extract_parts(v)

        if registration_code not in _REGION_LOOKUP:
            raise ValidationError(f"Invalid registration region code: {registration_code}")

        if district_code not in _REGION_LOOKUP:
            raise ValidationError(f"Invalid district code: {district_code}")

        if not _validate_checksum(v):
            raise ValidationError("Invalid checksum")

        return ParsedID(
            country_code="ZW",
            id_number=v,
            id_type="NATIONAL_ID",
            extra={
                "registration_region": _REGION_LOOKUP[registration_code],
                "registration_code": registration_code,
                "district": _REGION_LOOKUP[district_code],
                "district_code": district_code,
                "sequence_number": sequence_number,
                "check_letter": check_letter,
            },
        )
