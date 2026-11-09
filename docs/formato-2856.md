# Formato 2856 — Report of operations with digital assets (third-party information)

🌐 **English** · [Español](formato-2856.es.md)

Source: Resolution 000233 of 2025 of DIAN (Dirección de Impuestos y Aduanas Nacionales, Colombia's tax and customs authority), art. 1.3.12.21 and Technical Annex T3.73. Applies from tax year 2026 (filed in 2027, on the *exógena* calendar).

## Reporting entities
Digital-asset service providers resident or domiciled in Colombia, with operations in the country, whose gross income in the year exceeds 1,400 UVT (item 21 of art. 1.3.1.1).

## What is reported
Per user, accumulated and annualised: conversions between legal-tender currency and digital assets.

| Field (XML attribute) | Content |
|---|---|
| `nidusu`, names/`razusu`, `dirusu`, `paisusu` | User's identification, name or company name, address and country |
| `cuentausu`, `seudousu` | Account or wallet number and name/pseudonym (alphanumeric; "1" when there is no wallet) |
| `saldoini`, `saldofin` | Opening and closing balance (positive integers; the annex does not allow zero) |
| `tope` | Operation type: 1 Purchase · 2 Sale · 3 Exchange for goods or services · 4 Exchange for other digital assets · 5 Donations and/or rewards |
| `valtot` | Total value for the year in COP at fair market value at the time of each operation (integer) |
| `totunid` | Units traded (2 decimals) |
| `nactivo` | Asset ticker as listed on CoinMarketCap (max. 7 characters) |
| `nidcp`… `paiscp`, `cuentacp`, `seudocp` | Counterparty: identification, name, address, country, account and pseudonym |
| `…psav`, `dirpsav` | Service provider intermediating for the counterparty |

Foreign parties: TIN of the country of residence with document type 42; if none exists, 444444001 onwards with type 43.

## File
- XML 1.0, **ISO-8859-1** encoding, root `mas`, header `Cab` (Ano, CodCpt 1 insert / 2 replace, Formato 2856, Version 1, NumEnvio, FecEnvio, FecInicial, FecFinal, ValorTotal, CantReg) and `operacionesdigitales` records.
- File name: `Dmuisca_ccmmmmmvvaaaacccccccc.xml` (cc 01/02, mmmmm 02856, vv 01, aaaa filing year, cccccccc sequence number).
- Maximum 5,000 records per file; `nidusu` is the unique key per year.

## Mapping from the PurserKit data model
| Normalised event | `tope` |
|---|---|
| Fiat → asset deposit (SEP-24/6 deposit, CryptoFiatIn) | 1 Purchase |
| Asset → fiat withdrawal (SEP-24/6 withdraw, CryptoFiatOut) | 2 Sale |
| Payment for goods or services with assets | 3 |
| Swap / path payment / trade (CryptoToCrypto) | 4 |
| Airdrop, reward, mint to a user (CARF501/502/503) | 5 |

Open points: treatment of zero balances; memos and federated addresses (they do not match the alphanumeric pattern); the 2027 *exógena* deadlines are not yet published.
