# Netherlands (NL) — BSN

## Official / authority sources
- Rijksoverheid (what is a BSN): https://www.rijksoverheid.nl/onderwerpen/paspoort-en-identiteitskaart/vraag-en-antwoord/wat-is-een-burgerservicenummer-bsn

## Implementation notes
- Supported format: 9 digits.
- **Checksum**: Dutch "11-proef" (elfproef) with weights `9,8,7,6,5,4,3,2,-1` (mod 11).
- No DOB/gender are encoded.

## Non-official (used for algorithm descriptions)
- Wikipedia (11-proef summary): https://en.wikipedia.org/wiki/Burgerservicenummer
