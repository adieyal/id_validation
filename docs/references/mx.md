# Mexico (MX) — CURP

## Official / authority sources
- Government portal (CURP): https://www.gob.mx/curp/
- RENAPO (Registro Nacional de Población) portal: https://www.gob.mx/segob%7Crenapo

> Note: RENAPO/SEGOB pages sometimes change URLs; these are the official entry points.

## Implementation notes
- Supported format: 18 alphanumeric characters (case-insensitive; normalized to uppercase).
- Date of birth is decoded from `YYMMDD` plus a *century heuristic* based on the 17th character (homonym disambiguator):
  - digit (`0-9`) → 1900–1999
  - letter (`A-Z`) → 2000–2099
- Gender is decoded from position 11: `H` → `M`, `M` → `F` (library outputs `M`/`F`).
- State code is decoded from positions 12–13.
- **Checksum**: calculated from the first 17 characters using the published character-value table and a mod-10 check digit.

## Non-official (used for algorithm descriptions / tables)
- Wikipedia (format and check digit overview): https://en.wikipedia.org/wiki/Unique_Population_Registry_Code
