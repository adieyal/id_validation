A library for validating national id numbers and extracting any embedded data from them.

Currenty only Zimbabwe is implemented but more countries will be added over time

*Usage*

```
    from id_validation import validators
    validator_class = validators["ZW"]
    validator = validator_class()

    # Use the validate method to test whether a number is valid or not according to country-specific rules
    assert validator.validate("50-025544-Q-12")

    # The extract data method returns any data that might be encoded into the id number. This is country specific.
    data = validator.extract_data("50-025544-Q-12")
    assert data["registration_region"] == "Mutasa"
    assert data["distict"] == "Chivi"
    assert data["sequence_number"] == "025544"
```