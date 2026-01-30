# ID Validation Library

A Python library for validating national ID numbers and extracting embedded demographic data across 40+ countries.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Multi-Country Support**: Validates ID numbers from 40+ countries across Africa, Europe, and the Americas
- **Format Validation**: Verifies ID number structure and checksums according to country-specific rules
- **Data Extraction**: Extracts embedded information (date of birth, gender, region codes, etc.) where applicable
- **Type-Safe**: Full type hints and protocol-based design
- **Extensible**: Plugin architecture makes adding new validators straightforward

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Countries](#supported-countries)
- [API Reference](#api-reference)
- [Country-Specific Examples](#country-specific-examples)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

### From PyPI

```bash
pip install id-validation
```

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/adieyal/id_validation.git
cd id_validation

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
make install

# Or manually:
pip install -e ".[dev]"

# Verify installation
pytest
```

**Requirements**: Python 3.9 or higher

## Quick Start

```python
from id_validation import ValidatorFactory

# Get a validator for a specific country
validator = ValidatorFactory.get_validator("ZA")  # South Africa

# Validate an ID number
is_valid = validator.validate("7106245929185")
print(f"Valid: {is_valid}")  # Output: Valid: True

# Extract embedded data (when available)
data = validator.extract_data("7106245929185")
print(data)
# Output: {
#   'dob': datetime.datetime(1971, 6, 24, 0, 0),
#   'gender': <GENDER.MALE: 1>,
#   'citizenship': <CITIZENSHIP_TYPE.PERMANENT_RESIDENT: 1>,
#   'checksum': 5
# }
```

## Supported Countries

### Coverage by Region

| Region | Countries |
|--------|-----------|
| **Africa** | Botswana, Nigeria, South Africa, Zimbabwe |
| **Europe** | Belgium, Bulgaria, Croatia, Czech Republic, Denmark, Estonia, Finland, France, Italy, Latvia, Lithuania, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden, Turkey |
| **Americas** | Argentina, Brazil, Canada, Chile, Colombia, Ecuador, Mexico |

### Country Codes & Extracted Fields

| Code | Country / ID Type | Validation | Extracted Fields |
|------|-------------------|------------|------------------|
| **Africa** | | | |
| `BW` | Botswana | Format + Checksum | `gender` |
| `NG` | Nigeria | Format only | *(none)* |
| `ZA` | South Africa (post-apartheid) | Format + Checksum | `dob`, `gender`, `citizenship`, `checksum` |
| `ZA_OLD` | South Africa (apartheid-era)* | Format + Checksum | `dob`, `gender`, `race`, `checksum` |
| `ZW` | Zimbabwe | Format | `registration_region`, `district`, `sequence_number` |
| **Europe** | | | |
| `BE` | Belgium (NRN) | Format + Checksum | `dob`, `gender`, `sequence`, `checksum` |
| `BG` | Bulgaria (EGN) | Format + Checksum | `dob`, `gender`, `birth_order`, `checksum` |
| `CZ` | Czech Republic (rodné číslo) | Format + Checksum | `dob`, `gender`, `century`, `checksum` |
| `DK` | Denmark (CPR) | Format + Checksum (lenient) | `dob`, `gender`, `century`, `sequence` |
| `EE` | Estonia (isikukood) | Format + Checksum | `dob`, `gender`, `serial`, `checksum` |
| `FI` | Finland (HETU) | Format + Checksum | `dob`, `gender`, `century`, `individual_number`, `checksum` |
| `FR` | France (NIR / INSEE) | Format + Checksum | `dob`† , `gender`, `department`, `commune`, `order`, `key` |
| `HR` | Croatia (OIB) | Format + Checksum | `checksum` |
| `IT` | Italy (Codice Fiscale) | Format + Checksum | `dob`, `gender`, `municipality_code`, `checksum` |
| `LT` | Lithuania (Asmens kodas) | Format + Checksum | `dob`, `gender`, `century`, `serial`, `checksum` |
| `LV` | Latvia (personas kods) | Format | `dob`‡, `century`, `serial`‡ |
| `NL` | Netherlands (BSN) | Format + Checksum | *(none)* |
| `NO` | Norway (Fødselsnummer) | Format + Checksum | `dob`, `gender`, `individual_number`, `control_digits` |
| `PL` | Poland (PESEL) | Format + Checksum | `dob`, `gender`, `serial`, `checksum` |
| `PT` | Portugal (NIF) | Format + Checksum | `checksum` |
| `RO` | Romania (CNP) | Format + Checksum | `dob`, `gender`, `county_code`, `county_name`, `serial`, `checksum` |
| `SK` | Slovakia (rodné číslo) | Format + Checksum | `dob`, `gender`, `century`, `checksum` |
| `SI` | Slovenia (EMŠO) | Format + Checksum | `dob`, `gender`, `region_code`, `serial`, `checksum` |
| `ES` | Spain (DNI/NIE) | Format + Checksum | `type` (DNI/NIE), `number`, `letter` |
| `SE` | Sweden (Personnummer) | Format + Checksum | `dob`, `gender`, `coordination_number`, `individual_number`, `checksum` |
| `TR` | Turkey (T.C. Kimlik No) | Format + Checksum | `checksum10`, `checksum11` |
| **Americas** | | | |
| `AR` | Argentina (CUIT/CUIL) | Format + Checksum | `prefix`, `dni`, `category`, `checksum` |
| `BR` | Brazil (CPF) | Format + Checksum | `check_digits` |
| `CA` | Canada (SIN) | Format + Checksum | *(none)* |
| `CL` | Chile (RUT/RUN) | Format + Checksum | `number`, `dv` |
| `CO` | Colombia (NIT) | Format + Checksum | `base`, `dv`, `checksum` |
| `EC` | Ecuador (Cédula) | Format + Checksum | `province_code`, `province_name`, `serial`, `checksum` |
| `MX` | Mexico (CURP) | Format + Checksum | `dob`, `gender`, `state_code`, `state_name`, `homonym`, `checksum` |

**Notes:**
- \* `ZA_OLD`: Pre-1986 South African IDs (included for historical completeness; rarely encountered)
- † France: DOB extracted at month-level precision (day not encoded)
- ‡ Latvia: Legacy format only

## API Reference

### ValidatorFactory

Factory class for retrieving country-specific validators.

#### `get_validator(country_code: str) -> Validator`

Returns a validator instance for the specified country code.

**Parameters:**
- `country_code` (str): ISO 3166-1 alpha-2 country code (e.g., "ZA", "FI")

**Returns:**
- Validator instance

**Raises:**
- `ValueError`: If country code is not supported

**Example:**
```python
validator = ValidatorFactory.get_validator("FI")
```

### Validator Protocol

All validators implement the following interface:

#### `validate(id_number: str) -> bool`

Validates whether an ID number conforms to country-specific rules.

**Parameters:**
- `id_number` (str): The ID number to validate (format is country-specific)

**Returns:**
- `bool`: True if valid, False otherwise

**Example:**
```python
validator = ValidatorFactory.get_validator("NO")
is_valid = validator.validate("01010012345")  # Norway
```

#### `extract_data(id_number: str) -> dict[str, Any]`

Extracts embedded data from a valid ID number.

**Parameters:**
- `id_number` (str): A valid ID number

**Returns:**
- `dict[str, Any]`: Dictionary with extracted fields (varies by country)

**Raises:**
- `ValidationError`: If the ID number is invalid

**Example:**
```python
validator = ValidatorFactory.get_validator("MX")
data = validator.extract_data("CURP123456HDFLRN07")
# Returns: {'dob': datetime(...), 'gender': ..., 'state_code': 'DF', ...}
```

### ValidationError

Exception raised when an ID number fails validation.

```python
from id_validation import ValidationError

try:
    data = validator.extract_data("invalid-id")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Country-Specific Examples

### South Africa (ZA)

South African ID numbers encode date of birth, gender, and citizenship status.

```python
from id_validation import ValidatorFactory

validator = ValidatorFactory.get_validator("ZA")

# Validate
assert validator.validate("7106245929185") == True

# Extract data
data = validator.extract_data("7106245929185")
print(data)
# {
#   'dob': datetime.datetime(1971, 6, 24, 0, 0),
#   'gender': <GENDER.MALE: 1>,
#   'citizenship': <CITIZENSHIP_TYPE.PERMANENT_RESIDENT: 1>,
#   'checksum': 5
# }
```

### Zimbabwe (ZW)

Zimbabwe IDs contain registration region and district codes.

```python
validator = ValidatorFactory.get_validator("ZW")

assert validator.validate("50-025544-Q-12") == True

data = validator.extract_data("50-025544-Q-12")
# {
#   'registration_region': 'Mutasa',
#   'district': 'Chivi',
#   'sequence_number': '025544'
# }
```

### Mexico (MX)

Mexican CURP numbers include demographic and geographic information.

```python
validator = ValidatorFactory.get_validator("MX")

data = validator.extract_data("MEXA900101HDFLXN07")
# {
#   'dob': datetime.datetime(1990, 1, 1, 0, 0),
#   'gender': <GENDER.MALE: 1>,
#   'state_code': 'DF',
#   'state_name': 'Ciudad de México',
#   'homonym': '07',
#   'checksum': '7'
# }
```

### Finland (FI)

Finnish HETU numbers encode date of birth, century, and gender.

```python
validator = ValidatorFactory.get_validator("FI")

data = validator.extract_data("131052-308T")
# {
#   'dob': datetime.datetime(1952, 10, 13, 0, 0),
#   'century': '-',  # Born 1900-1999
#   'gender': <GENDER.MALE: 1>,
#   'individual_number': '308',
#   'checksum': 'T'
# }
```

### Nigeria (NG)

Nigerian National Identification Numbers (NIN) are 11-digit random numbers with no embedded data.

```python
validator = ValidatorFactory.get_validator("NG")

assert validator.validate("35765421356") == True
# Note: extract_data() returns empty dict (no encoded information)
```

**Caveat**: Botswana validation is implemented from publicly available information, not official documentation.

## Development

### Project Structure

```
id_validation/
├── src/id_validation/
│   ├── __init__.py          # Public API
│   ├── registry.py           # Plugin registry
│   ├── validate.py           # Base interfaces
│   ├── validate_*.py         # Country validators (top-level)
│   └── validators/           # Additional validators
│       ├── base.py
│       └── *.py              # Country-specific modules
├── tests/
│   ├── test_*.py             # Test files
│   ├── test_international/   # Regional test suites
│   ├── test_southafrica/
│   └── utils/
│       └── generators.py     # Test data generators
├── docs/
│   └── references/           # Per-country implementation notes
└── pyproject.toml
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific country tests
pytest tests/test_international/test_finland.py

# Run with coverage
pytest --cov=id_validation
```

### Adding a New Validator

1. Create a new validator module in `src/id_validation/validators/`
2. Implement the `Validator` protocol (or extend `BaseValidator`)
3. Register with `@register("COUNTRY_CODE")` decorator
4. Add tests in `tests/test_international/`
5. Document in `docs/references/`

Example:

```python
from id_validation.registry import register
from id_validation.validators.base import BaseValidator, ParsedID

@register("XX")
class ExampleValidator(BaseValidator):
    def parse(self, id_number: str) -> ParsedID:
        # Implement validation and parsing logic
        ...
```

### Build and Publish

```bash
# Build distribution packages
make build

# Check package metadata
make check

# Upload to PyPI
make publish
```

## References

Per-country implementation notes and official documentation links are available in `docs/references/*.md`.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-validator`)
3. Add tests for new functionality
4. Ensure all tests pass (`pytest`)
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This library aggregates validation rules from official government sources and public documentation. See `docs/references/` for specific citations.

---

**Maintainer**: Adi Eyal (adi@clearforest.io)
**Repository**: https://github.com/adieyal/id_validation/
