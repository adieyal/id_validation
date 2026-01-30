# Spain — DNI / NIE

## Authority reference
TODO: add an accessible official source (Policía Nacional page returned 404 from this environment).

Suggested authority pages to capture when accessible:
- Policía Nacional / DNI and NIE info pages.

## Notes (used by this library)
- DNI: `NNNNNNNNL` where `L` is a control letter computed as `number % 23` mapped through a fixed table.
- NIE: `X|Y|Z` + 7 digits + control letter; for calculation `X→0`, `Y→1`, `Z→2` and then same modulo-23 letter table.
