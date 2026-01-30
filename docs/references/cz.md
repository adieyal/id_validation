# Czech Republic (CZ) — Rodné číslo

## Official / authority sources
- Ministry of the Interior (MVČR): https://www.mvcr.cz/

## Implementation notes
- Normalizes by removing `/`.
- Accepts:
  - 9-digit legacy numbers (no checksum).
  - 10-digit numbers with a mod-11 check digit.
- DOB decoding:
  - `YYMMDD` with month modifiers: +50 female, +20 special series, +70 female+special.
  - Century is inferred (best-effort) for 10-digit numbers using a current-year pivot.

## Non-official
- Wikipedia overview: https://en.wikipedia.org/wiki/National_identification_number#Czech_Republic
