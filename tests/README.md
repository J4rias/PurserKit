🌐 **English** · [Español](README.es.md)

Planned test cases (phase 1): new report (CARF701), correction/deletion (CARF702, OECD2/OECD3), nil report (CARF703), natural-person user, entity with controlling persons, every `TransferType` (CARF501–509, 601–606), `TransferWallet`, RRPT, `AltValuation`, multiple jurisdictions (one file per jurisdiction).

Formato 2856 (third-party information): `Cab` header (insert and replace), one record per user with each operation type (1–5), natural-person and legal-entity user and counterparty, foreign counterparty without TIN (444444001… with type 43), operation without a wallet (`cuentausu` = 1), partitioning into 5,000-record files, `Dmuisca_…` file name, ISO-8859-1 encoding, validation against the Annex T3.73 XSD.
