# Formato 2856 — Reporte de operaciones con activos digitales (exógena)

🌐 [English](formato-2856.md) · **Español**

Fuente: Resolución 000233 de 2025 de la DIAN (Dirección de Impuestos y Aduanas Nacionales, la autoridad tributaria y aduanera de Colombia), art. 1.3.12.21 y Anexo T3.73. Aplica desde el año gravable 2026 (se presenta en 2027, en los plazos de exógena).

## Obligados
Proveedores de servicios de activos digitales residentes o domiciliados en Colombia, con operaciones en el país, con ingresos brutos superiores a 1.400 UVT en el año (num. 21 del art. 1.3.1.1).

## Qué se reporta
Por usuario, acumulado y anualizado: operaciones de conversión moneda de curso legal ↔ activos digitales.

| Campo (atributo XML) | Contenido |
|---|---|
| `nidusu`, nombres/`razusu`, `dirusu`, `paisusu` | Identificación, nombre o razón social, dirección y país del usuario |
| `cuentausu`, `seudousu` | Número y nombre/seudónimo de la cuenta o billetera (alfanumérico; "1" si no hay billetera) |
| `saldoini`, `saldofin` | Saldo inicial y final (enteros positivos; el anexo no permite cero) |
| `tope` | Tipo de operación: 1 Compra · 2 Venta · 3 Intercambio por bienes o servicios · 4 Intercambio con otros activos digitales · 5 Donaciones y/o recompensas |
| `valtot` | Valor total del año en COP al valor justo de mercado al momento de la operación (entero) |
| `totunid` | Unidades transadas (2 decimales) |
| `nactivo` | Sigla del activo según CoinMarketCap (máx. 7 caracteres) |
| `nidcp`… `paiscp`, `cuentacp`, `seudocp` | Contraparte: identificación, nombre, dirección, país, cuenta y seudónimo |
| `…psav`, `dirpsav` | Proveedor que intermedia a la contraparte |

Extranjeros: TIN del país de residencia con tipo de documento 42; si no existe, 444444001 en adelante con tipo 43.

## Archivo
- XML 1.0, codificación **ISO-8859-1**, raíz `mas`, encabezado `Cab` (Ano, CodCpt 1 inserción / 2 reemplazo, Formato 2856, Version 1, NumEnvio, FecEnvio, FecInicial, FecFinal, ValorTotal, CantReg) y registros `operacionesdigitales`.
- Nombre: `Dmuisca_ccmmmmmvvaaaacccccccc.xml` (cc 01/02, mmmmm 02856, vv 01, aaaa año de envío, cccccccc consecutivo).
- Máximo 5.000 registros por archivo; `nidusu` es llave única por año.

## Mapeo desde el modelo de datos de PurserKit
| Evento normalizado | `tope` |
|---|---|
| Depósito fiat → activo (SEP-24/6 deposit, CryptoFiatIn) | 1 Compra |
| Retiro activo → fiat (SEP-24/6 withdraw, CryptoFiatOut) | 2 Venta |
| Pago de bienes o servicios con activos | 3 |
| Swap / path payment / trade (CryptoToCrypto) | 4 |
| Airdrop, recompensa, mint a usuario (CARF501/502/503) | 5 |

Puntos abiertos: tratamiento de saldos en cero; memos y direcciones federadas (no cumplen el patrón alfanumérico); plazos de exógena 2027 aún no publicados.
