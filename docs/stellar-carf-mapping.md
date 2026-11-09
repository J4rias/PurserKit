# Stellar → CARF mapping (draft)

🌐 **English** · [Español](stellar-carf-mapping.es.md)

| Stellar operation / event | CARF category (for a user of the reporting provider) | Data source | Notes |
|---|---|---|---|
| Incoming / outgoing `payment` | `CryptoTransferIn` (505 if from a known VASP, otherwise 509) / `CryptoTransferOut` (601/606) + `TransferWallet` when the destination is not a known VASP | Horizon `/payments`; CAP-67 `transfer` event | Requires a VASP address registry (SEP-1 `ACCOUNTS`). Payments from/to the issuer = mint/burn |
| `path_payment_strict_send/receive` | To self: `CryptoToCryptoOut` + `CryptoToCryptoIn`; to a third party: swap + `TransferOut` | Horizon operation | Splitting swap and transfer is an interpretation |
| `manage_sell/buy_offer` fills | `CryptoToCryptoOut` + `CryptoToCryptoIn` | Horizon `/trades` | |
| `create_account` | Funder: `TransferOut` (+`TransferWallet`); new account: `TransferIn` | Horizon operation | |
| `account_merge` | `TransferOut` (XLM) | Horizon `/effects` | |
| Claimable balances | Out on creation / In on claim; airdrops = CARF501 | Horizon effects; CAP-67 | Timing is ambiguous |
| `clawback` | `TransferOut` 605/606 | Horizon operation; CAP-67 | Flag it |
| Liquidity-pool deposit/withdraw | Crypto-to-crypto exchange for pool shares | Horizon | Out of MVP scope |
| Network fee | Netted out ("net of fees") | `fee_charged` | |
| SAC `transfer/mint/burn/clawback` (Soroban) | As payments / mint (e.g. 503) / burn | RPC `getEvents`; Token Transfer Processor | |
| Blend / Soroswap / DeFindex | Swap, loan (402/602), collateral (404/507/604) | Contract events | Out of MVP scope |
| SEP-24/6 deposit (fiat→crypto) | `CryptoFiatIn` + transfer to the user's wallet | Anchor Platform `sep24_transaction` (`amount_in`, `amount_out`, `amount_fee`, `stellar_transaction_id`) | The fiat leg exists only at the anchor |
| SEP-24/6 withdrawal (crypto→fiat) | `TransferIn` + `CryptoFiatOut` | Same | |
| SEP-31 | Depends on the role | `sep31_transaction` (`sender_id`, `receiver_id`) | Legal question: who is the user |
| SEP-38 quote | Preferred price source | `exchange_quote` | |
