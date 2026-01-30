# Norway — Fødselsnummer

## Authority reference
TODO: add an accessible official source (Skatteetaten pages appear JS-heavy and are not extracted well via `web_fetch` from this environment).

Suggested authority pages to capture when accessible:
- Skatteetaten / National Population Register section on identity numbers.

## Notes (used by this library)
- Format: `DDMMYYIIIKK` (11 digits)
  - `DDMMYY` date of birth
  - `III` individual number (also used for century inference)
  - `KK` control digits computed via Mod-11 with published weight vectors.
