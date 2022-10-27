from id_validation.validate import ValidationError
class NigeriaValidator:
    def _validate_str(self, id_number: str) -> bool:
        return len(id_number) == 11 and id_number.isdigit()

    def validate(self, id_number: str) -> bool:
        return self._validate_str(id_number)

    def extract_data(self, id_number: str) -> bool:
        if not self.validate(id_number):
            raise ValidationError("Invalid ID number")
        
        return {}