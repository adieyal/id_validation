# Ecuador (EC) — Cédula

## Official / authority sources
- Registro Civil (Ecuador) portal: https://www.registrocivil.gob.ec/

## Implementation notes
- Supported format: 10 digits (**natural persons cédula only**).
- Extracted fields:
  - `province_code` (first two digits)
  - `province_name`
  - `third_digit`
  - `serial`
- Validation rules implemented:
  - province code must be `01..24`
  - third digit must be `0..5` (natural persons)
- **Checksum**: modulo 10 with coefficients `2,1,2,1,2,1,2,1,2` (subtract 9 when product >= 10).

## Non-official (used for algorithm descriptions)
- Wikipedia / community descriptions of the modulo-10 algorithm (reference only): https://en.wikipedia.org/wiki/National_identification_number#Ecuador
