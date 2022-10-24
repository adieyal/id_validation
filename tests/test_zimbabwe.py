import pytest

from ..validate_zimbabwe import ZimbabweValidator, region_lookup

@pytest.fixture
def valid_id_numbers():
    return [
        "50-025544-Q-12",
        "43-165780-A-42",
        "77-040785-H-77",
        "75-341502-L-70",
        "63-751545-G-63",
        "49-008555-S-49",
        "63-1174850-T-45",
    ]

@pytest.fixture
def invalid_id_numbers():
    return [
        "50-925544-Q-12",
        "43-965780-A-42",
        "77-940785-H-77",
        "75-941502-J-70",
        "63-951545-G-63",
        "49-908555-S-49",
        "63-9174850-L-45",
    ]

class TestZimbabweValidator:
    def test_accepts_valid_registration_codes(self):
        validator = ZimbabweValidator()
        for registration_code in region_lookup:
            try:
                validator._get_region(registration_code)
            except Exception:
                raise AssertionError(f"Incorrectly rejected {registration_code}")
        
    def test_rejects_invalid_registration_codes(self):
        validator = ZimbabweValidator()
        for i in range(100):
            registration_code = str(i).zfill(2)
            if registration_code not in region_lookup:
                try:
                    validator._get_region(registration_code)
                    raise AssertionError(f"Incorrectly accepted {registration_code}")
                except Exception:
                    pass 

    def test_checksum_with_valid_id_numbers(self, valid_id_numbers):
        validator = ZimbabweValidator()
        for id_number in valid_id_numbers:
            clean_id_number = validator._clean_id_number(id_number)
            assert validator._checksum(clean_id_number)

    def test_checksum_with_invalid_id_numbers(self, invalid_id_numbers):
        validator = ZimbabweValidator()
        for id_number in invalid_id_numbers:
            clean_id_number = validator._clean_id_number(id_number)
            assert not validator._checksum(clean_id_number)

    def test_cleans_id_numbers(self):
        validator = ZimbabweValidator()
        assert validator._clean_id_number("50-025544-Q-12") == "50025544Q12"
        assert validator._clean_id_number("43-165780-A-42") == "43165780A42"
        assert validator._clean_id_number("77-040785-H- 77") == "77040785H77"
        assert validator._clean_id_number("75-3415-02-L-70") == "75341502L70"

    def test_extract_parts(self):
        validator = ZimbabweValidator()
        assert validator._extract_parts("50025544Q12") == ("50", "025544", "Q", "12")
        assert validator._extract_parts("43165780A42") == ("43", "165780", "A", "42")
        assert validator._extract_parts("77040785H77") == ("77", "040785", "H", "77")

    def test_validate_with_valid_idnumbers(self, valid_id_numbers):
        validator = ZimbabweValidator()
        for id_number in valid_id_numbers:
            assert validator.validate(id_number)

    def test_validate_with_invalid_idnumbers(self, invalid_id_numbers):
        validator = ZimbabweValidator()
        for id_number in invalid_id_numbers:
                assert not validator.validate(id_number)

    def test_extract_data(self, valid_id_numbers):
        validator = ZimbabweValidator()
        data = validator.extract_data("43-165780-A-42")
        assert data["registration_region"] == validator._get_region("43")
        assert data["district"] == validator._get_region("42")
        assert data["sequence_number"] == "165780"