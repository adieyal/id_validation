A library for validating national id numbers and extracting any embedded data from them.

Currenty only South Africa and Zimbabwe are implemented but more countries will be added over time

# Installation

    pip install id-validation
    
# Usage

    from id_validation import ValidatorFactory
    validator = ValidatorFactory.get_validator("ZW")

    # Use the validate method to test whether a number is valid or not according to country-specific rules
    assert validator.validate("50-025544-Q-12")

    # The extract data method returns any data that might be encoded into the id number. This is country specific.
    data = validator.extract_data("50-025544-Q-12")
    assert data["registration_region"] == "Mutasa"
    assert data["district"] == "Chivi"
    assert data["sequence_number"] == "025544"

# Countries
The following codes are available:

    BW - Botswana
    NG - Nigeria
    ZA - South Africa
    ZA_OLD - South African (Apartheid-era). See the note below for more information
    ZW - Zimbabwe


## Botswana (BW)
Note - the validation logic has been implemented from anecdotal information available online and not against official documentation.

```
>>> import id_validation
>>> from id_validation import ValidatorFactory
>>> validator = ValidatorFactory.get_validator("BW")
>>> validator.validate("379219515")
True
>>> validator.extract_data("379219515")
{'gender': 'Male'}
```

## Nigeria
Nigerian id numbers consist of 11 randomly selected digits. Find the regulations <a href="images/MandatoryNIN_Gazetted.pdf">here</a>.

```
>>> import id_validation
>>> from id_validation import ValidatorFactory
>>> validator = ValidatorFactory.get_validator("NG")
>>> validator.validate("35765421356")
True
```

## South Africa (ZA)
South African ids contain the following information:
- Date of birth
- Gender
- Citizenship (citizen or permanent resident)

```
>>> import id_validation
>>> from id_validation import ValidatorFactory
>>> validator = ValidatorFactory.get_validator("ZA")
>>> validator.validate("7106245929185")
True
>>> validator.extract_data("7106245929185")
{'dob': datetime.datetime(1971, 6, 24, 0, 0), 'gender': <GENDER.MALE: 1>, 'checksum': 5, 'citizenship': <CITIZENSHIP_TYPE.PERMANENT_RESIDENT: 1>}
```

## South Africa - Apartheid-era (ZA_OLD)
Apartheid-era South African ids contain the following information:
- Date of birth
- Gender
- Race

```
>>> import id_validation
>>> from id_validation import ValidatorFactory
>>> validator = ValidatorFactory.get_validator("ZA_OLD")
>>> validator.validate("7106245929185")
True
>>> validator.extract_data("7106245929185")
{'dob': datetime.datetime(1971, 6, 24, 0, 0), 'gender': <GENDER.MALE: 1>, 'checksum': 5, 'race': <RACE.CAPE_COLOURED: 1>}
```

### Note
These id numbers were used during the Apartheid-era. They encoded the race of the ID holder. The 1986 Identification Act removed this identifier and all id numbers were changed to the more modern version which only encodes citizenship. This validator is included for completeness. I have never seen an old id number in any dataset I have ever worked with, so avoid using it unless you are sure that your ids are pre-1986. More information can be found [here](https://web.archive.org/web/20220705233321/https://www.thoughtco.com/south-african-apartheid-era-identity-numbers-4070233)

<img src="images/apartheid_id.jpg"/>

## Zimbabwe (ZW)
Zimbabwe IDs contain the following information:
- Registration region
- Father's district

```
>>> import id_validation
>>> from id_validation import ValidatorFactory
>>> validator = ValidatorFactory.get_validator("ZW")
>>> validator.validate("50-025544-Q-12")
True
>>> validator.extract_data("50-025544-Q-12")
{'registration_region': 'Mutasa', 'district': 'Chivi', 'sequence_number': '025544'}
```
