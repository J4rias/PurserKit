# Marco legal

🌐 [English](legal-framework.md) · **Español**

Resumen de las obligaciones de reporte que la DIAN (Dirección de Impuestos y Aduanas Nacionales, la autoridad tributaria y aduanera de Colombia) y la UIAF (Unidad de Información y Análisis Financiero, la unidad de inteligencia financiera de Colombia) imponen a los proveedores de servicios de criptoactivos.

## DIAN — Res. 000240 de 24-dic-2025 (CARF)
- Agrega arts. 1.6.11.1–1.6.11.11 a la Res. 227/2025. Anexo T6.16 (debida diligencia) y T6.17 (CARF XML v1.5).
- Obligado: quien, como negocio, presta servicios de intercambio o transferencia de criptoactivos para clientes, con nexo en Colombia.
- Se reportan usuarios residentes en Colombia y en cualquier otra jurisdicción; un archivo XML por jurisdicción; reporte en cero (CARF703) si no hay datos.
- Reglas: `SendingEntityIN` = NIT de 9 dígitos sin DV; `MessageRefId` de 22 caracteres; `DocRefId` de 28; montos con 2 decimales; UTF-8.
- Requisitos: RUT responsabilidad 67 (y 22 para el representante legal); firma electrónica.
- Plazo: último día hábil de mayo del año siguiente → **31-may-2027** para el año 2026. Conservación 5 años.
- Sanción (art. 1.6.11.9): cuando no se presente, se presente tarde, o el contenido tenga errores o no corresponda a lo solicitado, aplican las sanciones del art. 651 del ET, hasta 7.500 UVT.

## DIAN — Formato 2856 exógena (Res. 000233 de 30-oct-2025, art. 1.3.12.21, Anexo T3.73)
- Obligados: proveedores de servicios de activos digitales con operaciones en Colombia e ingresos brutos > 1.400 UVT.
- Reporte anual acumulado por usuario de conversiones fiat↔activos digitales (tipos 1–5), saldos, valor en COP, unidades, sigla CoinMarketCap, contraparte y su proveedor.
- XML ISO-8859-1, raíz `mas`, encabezado `Cab`, ≤5.000 registros por archivo, nombre `Dmuisca_ccmmmmmvvaaaacccccccc.xml`; XSD incluido en el anexo.
- Año gravable 2026 en adelante (se presenta en 2027, plazos de exógena).

## UIAF — Res. 314 de 15-dic-2021 (inicio 1-jul-2022 por Res. 84/2022)
- ROS inmediato (formulario web SIREL).
- Mensual, días 1–20: transacciones (individuales ≥ USD 150; múltiples ≥ USD 450 por cliente/mes), clientes, ausencias.
- Anexo 3 vigente (nov-2022): TXT `|`, ANSI CP1252, archivo `TPSVSSTTTCCCMMAA`, 26 campos (incluye hash; valor en COP a TCRM).
- Anexo 2 vigente (jun-2022): archivo `CPSVSSTTTCCCMMAA`, 12 campos.

## Límites de esta herramienta
Genera borradores para que el obligado (o su revisor fiscal/abogado) los revise y presente. No presenta reportes, no custodia activos, no es asesoría tributaria ni legal. Pensada para ejecutarse en la infraestructura del propio proveedor (datos personales, Ley 1581/2012).

Nota: este documento es un resumen de referencia y no constituye asesoría legal.
