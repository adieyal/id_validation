# Latvia (LV) — Personas kods (personal code)

## Official / authority sources
- Office of Citizenship and Migration Affairs (PMLP): https://www.pmlp.gov.lv/

## Implementation notes
- Supports both:
  - **Legacy** format: `DDMMYY-XXXXX` (hyphen optional) where DOB is embedded.
  - **Modern** format: 11 digits without DOB encoding (DOB/gender not derivable).
- For legacy numbers, DOB is parsed and validated. A historical checksum/key exists, but this library currently does **not** enforce it due to difficulty sourcing an authoritative public specification.

## Non-official
- Wikipedia overview: https://en.wikipedia.org/wiki/National_identification_number#Latvia
