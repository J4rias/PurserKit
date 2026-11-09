# Mapeo Stellar → CARF (borrador)

🌐 [English](stellar-carf-mapping.md) · **Español**

| Operación / evento Stellar | Categoría CARF (para un usuario del RCASP) | Fuente de datos | Notas |
|---|---|---|---|
| `payment` entrante / saliente | `CryptoTransferIn` (505 si viene de un VASP conocido, si no 509) / `CryptoTransferOut` (601/606) + `TransferWallet` si el destino no es un VASP conocido | Horizon `/payments`; evento CAP-67 `transfer` | Requiere registro de direcciones de VASP (SEP-1 `ACCOUNTS`). Pagos desde/hacia el emisor = mint/burn |
| `path_payment_strict_send/receive` | A sí mismo: `CryptoToCryptoOut` + `CryptoToCryptoIn`; a tercero: swap + `TransferOut` | Horizon op | La separación swap/transferencia es interpretación |
| Fills de `manage_sell/buy_offer` | `CryptoToCryptoOut` + `CryptoToCryptoIn` | Horizon `/trades` | |
| `create_account` | Quien fondea: `TransferOut` (+`TransferWallet`); cuenta nueva: `TransferIn` | Horizon op | |
| `account_merge` | `TransferOut` (XLM) | Horizon `/effects` | |
| Claimable balances | Out al crear / In al reclamar; airdrops = CARF501 | Horizon effects; CAP-67 | Momento ambiguo |
| `clawback` | `TransferOut` 605/606 | Horizon op; CAP-67 | Marcar |
| LP deposit/withdraw | Intercambio cripto-cripto por participación del pool | Horizon | Fuera del MVP |
| Fee de red | Se neta ("net of fees") | `fee_charged` | |
| SAC `transfer/mint/burn/clawback` (Soroban) | Como pagos / mint (p. ej. 503) / burn | RPC `getEvents`; Token Transfer Processor | |
| Blend / Soroswap / DeFindex | Swap, préstamo (402/602), colateral (404/507/604) | Eventos de contrato | Fuera del MVP |
| Depósito SEP-24/6 (fiat→cripto) | `CryptoFiatIn` + transferencia a la wallet del usuario | Anchor Platform `sep24_transaction` (`amount_in`, `amount_out`, `amount_fee`, `stellar_transaction_id`) | El lado fiat solo existe en el anchor |
| Retiro SEP-24/6 (cripto→fiat) | `TransferIn` + `CryptoFiatOut` | Igual | |
| SEP-31 | Depende del rol | `sep31_transaction` (`sender_id`, `receiver_id`) | Pregunta legal: quién es el usuario |
| Cotización SEP-38 | Fuente de precio prioritaria | `exchange_quote` | |
