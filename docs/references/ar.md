# Argentina (AR) — CUIT / CUIL

## Official / authority sources
- AFIP (Administración Federal de Ingresos Públicos) portal: https://www.afip.gob.ar/

## Implementation notes
- Supported format: 11 digits (hyphens accepted and normalized from `XX-XXXXXXXX-X`).
- Extracted fields:
  - `prefix` (first 2 digits)
  - `dni` (middle 8 digits)
  - `category` (best-effort: individual/company/unknown)
- **Checksum**: mod 11 using weights `5,4,3,2,7,6,5,4,3,2` and special-case mapping for results 10→9 and 11→0.

## Non-official (used for algorithm descriptions)
- Wikipedia (CUIT checksum overview): https://en.wikipedia.org/wiki/Clave_%C3%9Anica_de_Identificaci%C3%B3n_Tributaria
