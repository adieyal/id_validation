# Colombia (CO) — NIT

## Official / authority sources
- DIAN (Dirección de Impuestos y Aduanas Nacionales) portal: https://www.dian.gov.co/

## Implementation notes
- Supported format: base digits + verifier digit (DV), accepting `NNNNNNNNN-D` or `NNNNNNNNND`.
- Extracted fields: `base`, `dv`.
- **Checksum**: mod 11 with DIAN weights (right-to-left): `71,67,59,53,47,43,41,37,29,23,19,17,13,7,3`.

## Non-official (used for algorithm descriptions)
- Wikipedia (NIT and DV overview): https://en.wikipedia.org/wiki/National_Tax_Number
