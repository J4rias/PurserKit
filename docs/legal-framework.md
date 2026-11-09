# Legal framework

🌐 **English** · [Español](legal-framework.es.md)

Summary of the reporting obligations that DIAN (Dirección de Impuestos y Aduanas Nacionales, Colombia's tax and customs authority) and UIAF (Unidad de Información y Análisis Financiero, Colombia's financial intelligence unit) impose on crypto-asset service providers.

## DIAN — Resolution 000240 of 24 Dec 2025 (CARF)
- Adds articles 1.6.11.1–1.6.11.11 to Resolution 227/2025. Annex T6.16 (due diligence) and Annex T6.17 (CARF XML v1.5).
- Reporting entity: anyone who, as a business, provides crypto-asset exchange or transfer services to customers and has a nexus with Colombia.
- Users resident in Colombia and in any other jurisdiction are reported; one XML file per jurisdiction; nil report (CARF703) when there is nothing to report.
- Rules: `SendingEntityIN` = 9-digit NIT (Colombian tax ID) without check digit; `MessageRefId` of 22 characters; `DocRefId` of 28; amounts with 2 decimals; UTF-8.
- Prerequisites: RUT (tax registry) responsibility 67 (and 22 for the legal representative); electronic signature.
- Deadline: last business day of May of the following year → **31 May 2027** for tax year 2026. Records kept for 5 years.
- Penalties (art. 1.6.11.9): when the report is not filed, is filed late, or its content has errors or does not match what was requested, the penalties of article 651 of the Tax Code apply, up to 7,500 UVT.

## DIAN — Formato 2856, third-party information (Resolution 000233 of 30 Oct 2025, art. 1.3.12.21, Annex T3.73)
- Reporting entities: digital-asset service providers with operations in Colombia and gross income above 1,400 UVT.
- Annual report, accumulated per user, of fiat↔digital-asset conversions (operation types 1–5), balances, value in COP, units, CoinMarketCap ticker, counterparty and its provider.
- ISO-8859-1 XML, root `mas`, header `Cab`, ≤5,000 records per file, file name `Dmuisca_ccmmmmmvvaaaacccccccc.xml`; XSD included in the annex.
- Tax year 2026 onwards (filed in 2027, on the *exógena* calendar).

## UIAF — Resolution 314 of 15 Dec 2021 (in force from 1 Jul 2022 under Resolution 84/2022)
- Suspicious-operation reports (ROS) immediately, through the SIREL web form.
- Monthly, days 1–20: transactions (individual ≥ USD 150; multiple ≥ USD 450 per customer per month), customers, and nil reports.
- Annex 3 in force (Nov 2022): pipe-delimited TXT, ANSI CP1252, file `TPSVSSTTTCCCMMAA`, 26 fields (includes transaction hash; value in COP at the TRM rate).
- Annex 2 in force (Jun 2022): file `CPSVSSTTTCCCMMAA`, 12 fields.

## Limits of this toolkit
It produces drafts for the reporting entity (or its statutory auditor or lawyer) to review and file. It does not file reports, does not hold assets, and is not tax or legal advice. It is designed to run inside the provider's own infrastructure (personal data, Law 1581 of 2012).

Note: this document is a reference summary and does not constitute legal advice.
