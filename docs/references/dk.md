# Denmark (DK) — CPR

## Official / authority sources
- CPR administration portal: https://cpr.dk/

## Implementation notes
- Supported format: `DDMMYY-SSSS` (hyphen optional).
- Date of birth is derived from `DDMMYY` plus a century rule based on the first digit of the serial (`SSSS`).
- Gender is derived from the parity of the last digit (odd = male, even = female).
- **Checksum**: Denmark historically used a mod-11 checksum, but it is not guaranteed for all issued CPR numbers (there are valid CPR numbers that fail the checksum). For this reason the library defaults to *lenient* checksum handling and exposes `strict_checksum=True` if you want to enforce mod-11.

## Non-official (used for algorithm descriptions)
- Wikipedia (overview + checksum weights): https://en.wikipedia.org/wiki/Personal_identification_number_(Denmark)
