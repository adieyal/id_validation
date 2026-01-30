# Portugal (PT) — NIF

## Official / authority sources
- Autoridade Tributária e Aduaneira (Portal das Finanças): https://www.portaldasfinancas.gov.pt/

## Implementation notes
- Supported format: 9 digits.
- **Checksum**: mod 11 over the first 8 digits with weights `9..2`.
- The first digit(s) can indicate NIF category (individual/company/etc). This library does not currently enforce prefix/category rules.

## Non-official (used for algorithm descriptions)
- Wikipedia (checksum description): https://en.wikipedia.org/wiki/VAT_identification_number#Portugal
