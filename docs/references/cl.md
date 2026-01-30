# Chile (CL) — RUT / RUN

## Official / authority sources
- Servicio de Impuestos Internos (SII): https://www.sii.cl/

## Implementation notes
- Supported format: base number (7–8 digits) plus verifier digit (0–9 or `K`). Common formatting with dots and hyphen is accepted.
- **Checksum**: mod 11 with multipliers 2..7 cyclic, resulting verifier digit in `{0..9,K}`.
- No DOB/gender are encoded.

## Non-official (used for algorithm descriptions)
- Wikipedia (RUT checksum overview): https://en.wikipedia.org/wiki/Rol_%C3%9Anico_Tributario
