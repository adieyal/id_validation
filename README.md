A library for validating national id numbers and extracting any embedded data from them.

Supports multiple countries; each validator can validate format/checksum and (where applicable) extract embedded data (DOB, gender, region codes, etc.).

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

    BE - Belgium (NRN)
    BG - Bulgaria (EGN)
    CZ - Czech Republic (rodné číslo)
    DK - Denmark (CPR)
    EE - Estonia (isikukood)
    FI - Finland (HETU)
    FR - France (NIR / Numéro de sécurité sociale)
    IT - Italy (Codice Fiscale)
    LT - Lithuania (Asmens kodas)
    LV - Latvia (personas kods)
    NO - Norway (Fødselsnummer)
    PL - Poland (PESEL)
    RO - Romania (CNP)
    SK - Slovakia (rodné číslo)
    ES - Spain (DNI/NIE)
    SE - Sweden (Personnummer)
    TR - Turkey (T.C. Kimlik No)

    BR - Brazil (CPF)
    CL - Chile (RUT/RUN)
    HR - Croatia (OIB)
    MX - Mexico (CURP)
    NL - Netherlands (BSN)
    PT - Portugal (NIF)
    SI - Slovenia (EMŠO)

## Supported countries & extracted fields

| Code | Country / ID | Extracted fields (when valid) |
|---|---|---|
| BW | Botswana | `gender` |
| NG | Nigeria | *(none – format only)* |
| ZA | South Africa (post-apartheid) | `dob`, `gender`, `checksum`, `citizenship` |
| ZA_OLD | South Africa (apartheid-era) | `dob`, `gender`, `checksum`, `citizenship`, `race` |
| ZW | Zimbabwe | `registration_region`, `district`, `sequence_number` |
| BE | Belgium (NRN) | `dob`, `gender`, `sequence`, `checksum` |
| BG | Bulgaria (EGN) | `dob`, `gender`, `birth_order`, `checksum` |
| CZ | Czech Republic (rodné číslo) | `dob`, `gender`, `century`, `month_raw`, `special_series`, `extension`, `checksum` |
| DK | Denmark (CPR) | `dob`, `gender`, `century`, `sequence`, `checksum_valid` *(lenient by default)* |
| EE | Estonia (isikukood) | `dob`, `gender`, `serial`, `checksum` |
| FI | Finland (HETU) | `dob`, `gender`, `century`, `individual_number`, `checksum` |
| FR | France (NIR) | `dob` *(month-level; day not encoded)*, `gender`, `department`, `commune`, `order`, `key`, `year`, `month` |
| IT | Italy (Codice Fiscale) | `dob`, `gender`, `municipality_code`, `checksum` |
| LT | Lithuania (Asmens kodas) | `dob`, `gender`, `century`, `serial`, `checksum` |
| LV | Latvia (personas kods) | `dob` *(legacy only)*, `century`, `century_digit`, `serial` *(legacy only)* |
| NO | Norway (fødselsnummer) | `dob`, `gender`, `individual_number`, `control_digits` |
| PL | Poland (PESEL) | `dob`, `gender`, `serial`, `checksum` |
| RO | Romania (CNP) | `dob`, `gender`, `county_code`, `county_name` *(best-effort)*, `serial`, `checksum` |
| SK | Slovakia (rodné číslo) | `dob`, `gender`, `century`, `month_raw`, `special_series`, `extension`, `checksum` |
| ES | Spain (DNI/NIE) | `type` (DNI/NIE), plus `number`, `letter` (and `prefix` for NIE) |
| SE | Sweden (personnummer) | `dob`, `gender`, `coordination_number`, `individual_number`, `checksum` |
| TR | Turkey (TCKN) | `checksum10`, `checksum11` *(no DOB/gender encoded)* |
| BR | Brazil (CPF) | `check_digits` |
| CL | Chile (RUT/RUN) | `number`, `dv` |
| HR | Croatia (OIB) | `checksum` |
| MX | Mexico (CURP) | `dob`, `gender`, `state_code`, `state_name`, `homonym`, `checksum` |
| NL | Netherlands (BSN) | *(none)* |
| PT | Portugal (NIF) | `checksum` |
| SI | Slovenia (EMŠO) | `dob`, `gender`, `region_code`, `serial`, `checksum` |

## References
See `docs/references/*.md` for per-country reference links and implementation notes.


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
