# France — NIR / Numéro de sécurité sociale

## Authority reference
- Service-Public.fr (Direction de l'information légale et administrative, Premier ministre): **Que signifie le numéro de Sécurité sociale ?**
  - https://www.service-public.gouv.fr/particuliers/vosdroits/F33078

## Notes (used by this library)
- The NIR is composed of **13 digits** plus a **2-digit control key**.
- Encoded information described by Service-Public includes:
  - Sex (1=male, 2=female)
  - Year and month of birth
  - Birth location codes (department + INSEE commune code) or foreign birth codes
  - Serial/order number
- This implementation:
  - Validates the 2-digit key using: `key = 97 - (numeric_body % 97)`.
  - Supports Corsica department codes `2A` and `2B` for key computation using the common substitutions (`2A→19`, `2B→18`).
  - Returns a `dob` with day set to `1` (NIR encodes month/year only).
