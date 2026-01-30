# Slovakia (SK) — Rodné číslo

## Official / authority sources
- Ministry of the Interior of the Slovak Republic: https://www.minv.sk/

## Implementation notes
- Normalizes by removing `/`.
- Accepts:
  - 9-digit legacy numbers (no checksum).
  - 10-digit numbers with a mod-11 check digit.
- DOB decoding uses the same month modifiers as commonly described for rodné číslo:
  - +50 female, +20 special series, +70 female+special.
- Century is inferred (best-effort) for 10-digit numbers using a current-year pivot.

## Non-official
- Wikipedia overview: https://en.wikipedia.org/wiki/National_identification_number#Slovakia
