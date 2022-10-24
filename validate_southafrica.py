from datetime import datetime
import random
from typing import Protocol
from enum import Enum, auto
import re
from abc import ABC, abstractmethod
from typing import Any

from .validate import ValidationError

class SouthAfricaValidationError(ValidationError):
    pass

re_validate = re.compile(r"^\d{13}$")

class RACE(Enum):
    WHITE = 0
    CAPE_COLOURED = 1
    MALAY = 2
    GRIQUA = 3
    CHINESE = 4
    INDIAN = 5
    OTHER_ASIATIC = 6
    OTHER_COLOURED = 7
    BLACK = 9

class CITIZENSHIP_TYPE(Enum):
    CITIZEN = 0
    PERMANENT_RESIDENT = 1

class GENDER(Enum):
    MALE = auto()
    FEMALE = auto()

class SouthAfricaValidator(ABC):
    def _clean_id_number(self, id_number: str) -> str:
        v = id_number.strip().replace(" ", "")
        if not self._validate_str(v):
            raise ValidationError("Invalid id number")

        return v

    def _validate_str(self, id_number: str) -> bool:
        if not re_validate.match(id_number):
            return False
        return True

    def _add_millenium(self, year_2digits: int) -> int:
        """
        This deals with the y2k problem in id numbers by adding the millenium to the year.
        Any id number with a year greater than the current year is from the previous millenium.
        This approach is problematic for dates of birth over 100 years ago. I haven't 
        found a legal reference to resolve this issue but this seems to be the approach
        used by most other implementations.
        
        """
        current_year_2digits = datetime.now().year % 100
        if year_2digits < current_year_2digits:
            return year_2digits + 2000
        else:
            return year_2digits + 1900

    def _validate_dob(self, id_number: str) -> bool:
        """Validates the date of birth part of the id number."""
        day = int(id_number[4:6])
        month = int(id_number[2:4])
        year = int(id_number[0:2])
        year = self._add_millenium(year)

        try:
            dt = datetime(year, month, day)
        except ValueError:
            return False

        return True
   

    # check the checksum of the idnumber using the luhn algorithm
    def _validate_checksum(self, id_number: str) -> bool:
        """
        Validates the checksum digit of the given id number using the Luhn algorithm.
        """
        # https://en.wikipedia.org/wiki/Luhn_algorithm
        check_digit = int(id_number[-1])
        return check_digit == self.generate_checksum(id_number[:-1])
        
        
    def generate_checksum(self, id_number: str) -> int:
        digits = list(map(int, str(id_number)))
        odd_digits = digits[-2::-2]
        even_digits = digits[-1::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(divmod(d * 2, 10))
        return (10 - (checksum % 10)) % 10

    @abstractmethod
    def validate(self, id_number: str) -> bool:
        if not self._validate_str(id_number):
            return False

        if not self._validate_dob(id_number):
            return False

        if not self._validate_checksum(id_number):
            return False

        return True

    def extract_dob(self, id_number: str) -> datetime:
        if not self.validate(id_number):
            raise SouthAfricaValidationError("Invalid ID number")

        day = int(id_number[4:6])
        month = int(id_number[2:4])
        year = int(id_number[0:2])

        year = self._add_millenium(year)

        return datetime(year, month, day)

    def extract_gender(self, id_number: str) -> GENDER:
        if not self.validate(id_number):
            raise SouthAfricaValidationError("Invalid ID number")

        digit = id_number[6]
        if digit in "01234":
            return GENDER.FEMALE
        else:
            return GENDER.MALE

    def extract_checksum(self, id_number: str) -> int:
        if not self.validate(id_number):
            raise SouthAfricaValidationError("Invalid ID number")

        return int(id_number[-1])

    @abstractmethod
    def extract_data(self, id_number: str) -> dict[str, Any]:

        if not self.validate(id_number):
            raise SouthAfricaValidationError("Invalid ID number")

        return {
            "dob": self.extract_dob(id_number),
            "gender": self.extract_gender(id_number),
            "checksum": self.extract_checksum(id_number),
        }

  

class PostApartheidSouthAfricaValidator(SouthAfricaValidator):
    def _validate_citizenship(self, id_number: str) -> bool:
        citizenship = int(id_number[10:11])
        return citizenship in [CITIZENSHIP_TYPE.CITIZEN.value, CITIZENSHIP_TYPE.PERMANENT_RESIDENT.value]

    def validate(self, id_number: str) -> bool:
        if not super().validate(id_number):
            return False

        if not self._validate_citizenship(id_number):
            return False
        return True

    def generate_idno(self, dob: datetime=None, gender: GENDER|None=None, citizenship: CITIZENSHIP_TYPE|None=None):
        start_date = datetime(1900, 1, 1)
        end_date = datetime.now()
        # generate a random date
        if dob is None:
            dob = datetime.fromtimestamp(start_date.timestamp() + random.random() * (end_date.timestamp() - start_date.timestamp()))

        if gender is None:
            gender = random.choice(list(GENDER))

        if citizenship is None:
            citizenship = random.choice(list(CITIZENSHIP_TYPE))

        if gender == GENDER.FEMALE:
            gender_digit = random.randint(0, 4)
        else:
            gender_digit = random.randint(5, 9)

        sequence = "".join(str(i) for i in random.sample(range(10), 3))

        idno = dob.strftime("%y%m%d") + str(gender_digit) + sequence + str(citizenship.value) + random.choice("78")
        idno += str(self.generate_checksum(idno))

        return idno

    def extract_citizenship(self, id_number: str) -> CITIZENSHIP_TYPE:
        if not self.validate(id_number):
            raise SouthAfricaValidationError("Invalid ID number")

        citizenship = int(id_number[10])
        return CITIZENSHIP_TYPE(citizenship)

    def extract_data(self, id_number: str) -> dict[str, Any]:
        data = super().extract_data(id_number)
        data["citizenship"] = self.extract_citizenship(id_number)
        return data
            

class ApartheidSouthAfricaValidator(SouthAfricaValidator):
    def _validate_race(self, id_number: str) -> bool:
        race = int(id_number[10])
        
        return race in [
            RACE.WHITE.value,
            RACE.CAPE_COLOURED.value,
            RACE.GRIQUA.value,
            RACE.MALAY.value,
            RACE.CHINESE.value,
            RACE.INDIAN.value,
            RACE.OTHER_ASIATIC.value,
            RACE.OTHER_COLOURED.value,
            RACE.BLACK.value
        ]

    def validate(self, id_number: str) -> bool:
        if not super().validate(id_number):
            return False

        if not self._validate_race(id_number):
            return False

        return True

    def extract_race(self, id_number: str) -> RACE:
        if not self.validate(id_number):
            raise ValidationError("Invalid ID number")

        race_digit = int(id_number[10])
        return RACE(race_digit)

    def extract_data(self, id_number: str) -> dict[str, Any]:
        data = super().extract_data(id_number)
        data["race"] = self.extract_race(id_number)
        return data

    def generate_idno(self, dob: datetime=None, gender: GENDER|None=None, race: RACE|None=None):
        start_date = datetime(1900, 1, 1)
        end_date = datetime.now()

        if dob is None:
            dob = datetime.fromtimestamp(start_date.timestamp() + random.random() * (end_date.timestamp() - start_date.timestamp()))

        if gender is None:
            gender = random.choice(list(GENDER))

        if race is None:
            race = random.choice(list(RACE))

        if gender == GENDER.FEMALE:
            gender_digit = random.randint(0, 4)
        else:
            gender_digit = random.randint(5, 9)

        sequence = "".join(str(i) for i in random.sample(range(10), 3))

        idno = dob.strftime("%y%m%d") + str(gender_digit) + sequence + str(race.value) + random.choice("78")
        idno += str(self.generate_checksum(idno))

        return idno
