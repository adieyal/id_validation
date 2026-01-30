# Brazil (BR) — CPF

## Official / authority sources
- Receita Federal (CPF services entry point): https://www.gov.br/receitafederal/pt-br/assuntos/cadastro-cpf

## Implementation notes
- Supported format: 11 digits (punctuation like `000.000.000-00` is accepted and normalized).
- **Checksum**: two check digits derived via mod 11 over the first 9 and first 10 digits.
- All-equal digit sequences (e.g. `00000000000`) are rejected.
- No DOB/gender are encoded.

## Non-official (used for algorithm descriptions)
- Wikipedia (CPF overview and checksum): https://en.wikipedia.org/wiki/Cadastro_de_Pessoas_F%C3%ADsicas
