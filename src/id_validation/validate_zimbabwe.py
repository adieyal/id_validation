from .validate import ValidationError
import re

"""
Source: Zimbabwe 2018 Elections Biometric Voters' Roll Analysis
https://www.slideshare.net/povonews/zimbabwe-2018-biometric-voters-roll-analysis-pachedu
"""
region_lookup = {
    "02": "Beitbridge",
    "03": "Mberengwa",
    "04": "Bikita",
    "05": "Bindura",
    "06": "Binga",
    "07": "Buhera",
    "08": "Bulawayo",
    "10": "Unknown", # (Undetermined) (believed: Mhondoro- "11": "Ngezi)    ",
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
    "46": "Unknown", # (Undetermined) (believed: Mbire)
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

class ZimbabweValidator:
    _lookup = {
        1: "A", 2: "B", 3: "C", 4: "D",
        5: "E", 6: "F", 7: "G", 8: "H",
        9: "J", 10: "K", 11: "L", 12: "M",
        13: "N", 14: "P", 15: "Q", 16: "R",
        17: "S", 18: "T", 19: "V", 20: "W",
        21: "X", 22: "Y", 23: "Z",
    }

    def _get_region(self, region_id: str) -> str:
        """
        Returns the region name for the given region id
        """
        try:
            return region_lookup[region_id]
        except IndexError:
            raise ValidationError(f"Invalid region code: {region_id}")

    def _checksum(self, id_number: str) -> bool:
        """
        Validates the checksum digit of the given id number using mod 23
        """
        registration_code, sequence_number, check_letter, _ = self._extract_parts(id_number)
        check_number = int(registration_code + sequence_number)
        mod = check_number % 23

        return check_letter == ZimbabweValidator._lookup[mod]

    def _clean_id_number(self, id_number: str) -> str:
        return id_number.replace("-", "").replace(" ", "")

    def _validate_str(self, id_number: str) -> str:
        clean = self._clean_id_number(id_number)
        allowed_letters = "".join(ZimbabweValidator._lookup.values())
        re_validate = re.compile(r"^\d{2}\d{6,7}[{%s}]\d{2}$" % allowed_letters)

        return re_validate.match(clean) is not None

    def _extract_parts(self, id_number: str) -> list[str]:
        registration_code = id_number[0:2]
        sequence_number = id_number[2:-3]
        check_letter = id_number[-3]
        district_code = id_number[-2:]

        return registration_code, sequence_number, check_letter, district_code


    def validate(self, id_number: str) -> bool:
        """
        Verify the region codes as well as use the modulus 23 validation
        """
        cleaned_id_number = self._clean_id_number(id_number)
        if not self._validate_str(cleaned_id_number):
            return False

        registration_code, _, _, district_code = self._extract_parts(cleaned_id_number)

        try:
            _ = self._get_region(registration_code)
            _ = self._get_region(district_code)
        except ValidationError:
            return False

        return self._checksum(cleaned_id_number)

    def extract_data(self, id_number: str) -> dict[str, str]:
        is_valid = self.validate(id_number)
        if not is_valid:
            raise ValidationError("Invalid ID number")
        
        cleaned_id_number = self._clean_id_number(id_number)
        registration_code, sequence_number, _, district_code = self._extract_parts(cleaned_id_number)

        return {
            "registration_region": self._get_region(registration_code),
            "district": self._get_region(district_code),
            "sequence_number": sequence_number
        }



