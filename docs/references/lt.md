# Lithuania (LT) — Asmens kodas (personal code)

## Official / authority sources
- State Enterprise Centre of Registers (Registrų centras): https://www.registrucentras.lt/

## Implementation notes
- Supported format: `GYYMMDDSSSC` (11 digits).
- `G` encodes gender and century: 1/2=1800s, 3/4=1900s, 5/6=2000s (odd=male, even=female).
- DOB is decoded from `YYMMDD` with the inferred century.
- Checksum implemented using the commonly published two-pass mod-11 scheme.

## Non-official (used for algorithm details)
- Wikipedia: https://en.wikipedia.org/wiki/National_identification_number#Lithuania
