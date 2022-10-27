import pytest

from id_validation.validate_southafrica import (
    CITIZENSHIP_TYPE,
    GENDER,
    PostApartheidSouthAfricaValidator,
    SouthAfricaValidationError,
    SouthAfricaValidator,
)
from id_validation.validate import ValidationError

idnumbers = list[str]


class DummyValidator(SouthAfricaValidator):
    def validate(self, id_number: str) -> bool:
        return super().validate(id_number)

    def extract_data(self, id_number: str) -> dict[str, str]:
        return super().extract_data(id_number)


@pytest.fixture
def post_apartheid_validator() -> SouthAfricaValidator:
    return PostApartheidSouthAfricaValidator()


@pytest.fixture
def dummy_validator() -> SouthAfricaValidator:
    return DummyValidator()


@pytest.fixture
def valid_id_numbers():
    return ["7106245929185", "7405095437186", "7710165556082", "6403056005085"]


@pytest.fixture
def invalid_citizenship_id_numbers():
    return ["7106245929485", "7405095437386", "7710165556282"]


@pytest.fixture
def invalid_id_numbers(
    invalid_date_numbers, invalid_citizenship_numbers, invalid_checksum_numbers
):
    return invalid_date_numbers + invalid_citizenship_numbers + invalid_checksum_numbers


@pytest.fixture
def citizen_id_numbers():
    return [
        "0604059596071",
        "0210079107087",
        "0701303437084",
        "6811228928077",
        "1010174953073",
    ]


@pytest.fixture
def permanent_resident_id_numbers():
    return [
        "9805302690170",
        "5601292418175",
        "3507318786176",
        "0910142906189",
        "4005115587177",
    ]


@pytest.fixture
def invalid_id_numbers(
    invalid_date_id_numbers, invalid_citizenship_id_numbers, invalid_checksum_id_numbers
):
    return (
        invalid_date_id_numbers
        + invalid_citizenship_id_numbers
        + invalid_checksum_id_numbers
    )


class TestSouthAfricaValidator:
    def test_clean_idnunber(self, dummy_validator: SouthAfricaValidator):
        assert "7106245929185" == dummy_validator._clean_id_number(
            "7106245 929 185    "
        )
        with pytest.raises(ValidationError):
            dummy_validator._clean_id_number("7106245 929 185d    ")

    def test_correct_length(self, dummy_validator: SouthAfricaValidator):
        invalid_id = "324343"
        valid_id_number = "9202204720082"

        assert not dummy_validator._validate_str(invalid_id)
        assert dummy_validator._validate_str(valid_id_number)

    def test_invalid_dob(
        self,
        dummy_validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_date_id_numbers,
    ):
        for idno in invalid_date_id_numbers:
            assert not dummy_validator._validate_dob(idno)

        for idno in valid_id_numbers:
            assert dummy_validator._validate_dob(idno)

    def test_checksum(self, dummy_validator: SouthAfricaValidator, valid_id_numbers):
        for idno in valid_id_numbers:
            check_digit = int(idno[-1])
            for i in range(10):
                test_idno = idno[:-1] + str(i)
                if i == check_digit:
                    assert dummy_validator._validate_checksum(test_idno)
                else:
                    assert not dummy_validator._validate_checksum(test_idno)

    def _test_validate(
        self,
        validator: SouthAfricaValidator,
        valid_id_numbers: idnumbers,
        invalid_id_numbers: idnumbers,
        invalid_date_id_numbers: idnumbers,
        invalid_checksum_id_numbers: idnumbers,
    ):
        for idno in valid_id_numbers:
            assert dummy_validator.validate(idno)

        for idno in invalid_id_numbers:
            assert not dummy_validator.validate(idno)

        for idno in invalid_date_id_numbers:
            assert not dummy_validator.validate(idno)

        for idno in invalid_checksum_id_numbers:
            assert not dummy_validator.validate(idno)

    def test_validate(
        self,
        dummy_validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_date_id_numbers,
        invalid_checksum_id_numbers,
    ):
        for idno in valid_id_numbers:
            assert dummy_validator.validate(idno)

        for idno in invalid_date_id_numbers:
            assert not dummy_validator.validate(idno)

        for idno in invalid_checksum_id_numbers:
            assert not dummy_validator.validate(idno)

    def test_generate_checksum(
        self, dummy_validator: SouthAfricaValidator, valid_id_numbers
    ):
        for idno in valid_id_numbers:
            assert int(idno[-1]) == dummy_validator.generate_checksum(idno[:-1])

    def test_extract_dob(
        self,
        dummy_validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_id_numbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                dummy_validator.extract_dob(idno)

        for idno in valid_id_numbers:
            dob = dummy_validator.extract_dob(idno)
            assert dob.month == int(idno[2:4])
            assert dob.day == int(idno[4:6])

        dob = dummy_validator.extract_dob("1604032983684")
        assert dob.year == 2016

        dob = dummy_validator.extract_dob("9804038760381")
        assert dob.year == 1998

        dob = dummy_validator.extract_dob("2704035759385")
        assert dob.year == 1927

        dob = dummy_validator.extract_dob("2104030613580")
        assert dob.year == 2021

    def test_extract_gender(
        self,
        dummy_validator: SouthAfricaValidator,
        invalid_id_numbers: idnumbers,
        male_id_numbers: idnumbers,
        female_id_numbers: idnumbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                dummy_validator.extract_gender(idno)

        for idno in male_id_numbers:
            gender = dummy_validator.extract_gender(idno)
            assert gender == GENDER.MALE

        for idno in female_id_numbers:
            gender = dummy_validator.extract_gender(idno)
            assert gender == GENDER.FEMALE

    def test_extract_checksum(
        self,
        dummy_validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_id_numbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                dummy_validator.extract_checksum(idno)

        for idno in valid_id_numbers:
            checksum = dummy_validator.extract_checksum(idno)
            assert checksum == int(idno[-1])

    def test_extract_data(
        self,
        dummy_validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_id_numbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                dummy_validator.extract_data(idno)

        for idno in valid_id_numbers:
            dob = dummy_validator.extract_dob(idno)
            gender = dummy_validator.extract_gender(idno)
            checksum = dummy_validator.extract_checksum(idno)
            data = dummy_validator.extract_data(idno)

            assert "dob" in data and data["dob"] == dob
            assert "gender" in data and data["gender"] == gender
            assert "checksum" in data and data["checksum"] == checksum


class TestPostApartheidValidator:
    def test_citizenship(
        self,
        post_apartheid_validator: SouthAfricaValidator,
        valid_id_numbers,
        invalid_citizenship_id_numbers,
    ):
        for idno in invalid_citizenship_id_numbers:
            assert not post_apartheid_validator._validate_citizenship(idno)

        for idno in valid_id_numbers:
            assert post_apartheid_validator._validate_citizenship(idno)

    def test_validate(
        self,
        post_apartheid_validator: PostApartheidSouthAfricaValidator,
        valid_id_numbers: idnumbers,
        invalid_citizenship_id_numbers: idnumbers,
    ):
        for idno in valid_id_numbers:
            assert post_apartheid_validator.validate(idno)

        for idno in invalid_citizenship_id_numbers:
            assert not post_apartheid_validator.validate(idno)

    def test_extract_citizenship(
        self,
        post_apartheid_validator: PostApartheidSouthAfricaValidator,
        invalid_id_numbers: idnumbers,
        citizen_id_numbers: idnumbers,
        permanent_resident_id_numbers: idnumbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                post_apartheid_validator.extract_citizenship(idno)

        for idno in citizen_id_numbers:
            citizenship = post_apartheid_validator.extract_citizenship(idno)
            assert citizenship == CITIZENSHIP_TYPE.CITIZEN

        for idno in permanent_resident_id_numbers:
            citizenship = post_apartheid_validator.extract_citizenship(idno)
            assert citizenship == CITIZENSHIP_TYPE.PERMANENT_RESIDENT

    def test_extract_data(
        self,
        post_apartheid_validator: PostApartheidSouthAfricaValidator,
        invalid_id_numbers: idnumbers,
        valid_id_numbers: idnumbers,
    ):
        for idno in invalid_id_numbers:
            with pytest.raises(SouthAfricaValidationError):
                post_apartheid_validator.extract_data(idno)

        for idno in valid_id_numbers:
            data = post_apartheid_validator.extract_data(idno)
            assert "dob" in data and data[
                "dob"
            ] == post_apartheid_validator.extract_dob(idno)
            assert "gender" in data and data[
                "gender"
            ] == post_apartheid_validator.extract_gender(idno)
            assert "checksum" in data and data[
                "checksum"
            ] == post_apartheid_validator.extract_checksum(idno)
            assert "citizenship" in data and data[
                "citizenship"
            ] == post_apartheid_validator.extract_citizenship(idno)
