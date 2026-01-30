# Belgium — National Register Number (NRN / Rijksregisternummer)

## Authority reference
TODO: add an accessible official source (belgium.be and IBZ/NRN pages encountered bot-check/captcha or 404 from this environment).

## Notes (used by this library)
- Format: `YYMMDDXXXCC` (11 digits)
  - `YYMMDD` date of birth
  - `XXX` sequence number (odd=male, even=female)
  - `CC` checksum computed as `97 - (base % 97)`.
- For births in/after 2000, checksum is computed using the base number prefixed with `2` (i.e. `2_000_000_000 + YYMMDDXXX`).
