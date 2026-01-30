# Finland — HETU (henkilötunnus / personal identity code)

## Authority reference
TODO: add an accessible official source (DVV pages are currently behind a bot-check (HTTP 403) from this environment).

Suggested authority pages to capture when accessible:
- Digital and Population Data Services Agency (DVV): https://dvv.fi/en/personal-identity-code

## Notes (used by this library)
- Format: `DDMMYYCZZZQ`
  - `C` century sign: `+` (1800s), `-` (1900s), `A` (2000s)
  - `ZZZ` individual number (odd=male, even=female)
  - `Q` check character from modulo-31 table.
