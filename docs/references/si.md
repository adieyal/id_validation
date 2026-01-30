# Slovenia (SI) — EMŠO

## Official / authority sources
- eUprava (Slovenian government portal; EMŠO overview entry point): https://e-uprava.gov.si/

> Note: A stable, specific official URL describing the checksum rules was not available in this environment.

## Implementation notes
- Supported format: 13 digits.
- Decoded fields:
  - `dob`: `DDMMYYY` (with `YYY` interpreted as a 3-digit year; library uses a practical century heuristic for modern IDs)
  - `gender`: derived from the 3-digit serial (`000-499` → male, `500-999` → female)
  - `region_code`: digits 8–9
- **Checksum**: mod 11 with weights `7,6,5,4,3,2,7,6,5,4,3,2`; check digit rules follow the EMŠO/JMBG system.

## Non-official (used for algorithm descriptions)
- Wikipedia / JMBG checksum description (same structure as EMŠO): https://en.wikipedia.org/wiki/Unique_Master_Citizen_Number
