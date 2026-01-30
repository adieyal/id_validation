# Sweden — Personnummer (personal identity number)

## Authority reference
- Skatteverket (Swedish Tax Agency): **Personnummer – Personnumrets uppbyggnad**
  - https://www.skatteverket.se/privat/folkbokforing/personnummer.4.3810a01c150939e893f18c29.html

## Notes (used by this library)
- Structure: `YYMMDD-NNNK` (or `YYMMDD+NNNK` when the person turns 100), where:
  - `YYMMDD` = date of birth
  - `NNN` = birth number (last digit odd = male, even = female)
  - `K` = control digit calculated from birth date + birth number
- This implementation:
  - Supports `YYMMDD-XXXX`, `YYMMDD+XXXX`, and `YYYYMMDDXXXX` inputs.
  - Implements checksum verification using the commonly used Luhn method on `YYMMDDNNN`.
