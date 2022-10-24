A library for validating national id numbers and extracting any embedded data from them.

Currenty only South Africa and Zimbabwe are implemented but more countries will be added over time

# Installation

    pip install id-validation
    
# Usage

```
    from id_validation import ValidatorFactory
    validator = ValidatorFactory.get_validator("ZW")

    # Use the validate method to test whether a number is valid or not according to country-specific rules
    assert validator.validate("50-025544-Q-12")

    # The extract data method returns any data that might be encoded into the id number. This is country specific.
    data = validator.extract_data("50-025544-Q-12")
    assert data["registration_region"] == "Mutasa"
    assert data["district"] == "Chivi"
    assert data["sequence_number"] == "025544"
```

# Countries
The following codes are available:

    ZA - South Africa
    ZA_OLD - South African (Apartheid-era). See the note below for more information
    ZW - Zimbabwe

## South Africa (Apartheid-era)
These id numbers were used during the Apartheid-era. They encoded the race of the ID holder. The 1986 Identification Act removed this identifier and all id numbers were changed to the more modern version which only encodes citizenship. This validator is included for completeness. I have never seen an old id number in any dataset I have ever worked with, so avoid using it unless you are sure that your ids are pre-1986. More information can be found [here](https://web.archive.org/web/20220705233321/https://www.thoughtco.com/south-african-apartheid-era-identity-numbers-4070233)