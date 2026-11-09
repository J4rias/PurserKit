🌐 [English](README.md) · **Español**

Casos de prueba previstos (entregable 1): nuevo (CARF701), corrección/eliminación (CARF702, OECD2/OECD3), reporte en cero (CARF703), usuario persona natural, entidad con personas controlantes, cada `TransferType` (CARF501–509, 601–606), `TransferWallet`, RRPT, `AltValuation`, múltiples jurisdicciones (un archivo por jurisdicción).

Formato 2856 (exógena): encabezado `Cab` (inserción y reemplazo), registro por usuario con cada tipo de operación (1–5), usuario y contraparte persona natural y jurídica, contraparte extranjera sin TIN (444444001… con tipo 43), operación sin billetera (`cuentausu` = 1), partición en archivos de 5.000 registros, nombre `Dmuisca_…`, codificación ISO-8859-1, validación contra el XSD del Anexo T3.73.
