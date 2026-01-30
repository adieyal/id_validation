# Italy — Codice Fiscale

## Authority reference
TODO: add an accessible official source (Agenzia delle Entrate pages returned 404 from this environment; likely moved).

## Notes (used by this library)
- Format: 16 alphanumeric characters.
- Encodes surname/name, year, month letter, day+gender, municipality code.
- The last character is a checksum derived from odd/even-position character mappings.
- This implementation validates checksum and extracts:
  - `dob`
  - `gender`
  - `municipality_code` (not decoded to a name).
