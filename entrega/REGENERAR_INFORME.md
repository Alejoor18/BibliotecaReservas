# Regenerar el informe

El PDF se generó con Python y ReportLab, con fuentes Markdown y diagramas Mermaid editables.
No se requiere instalar estas bibliotecas para ejecutar la aplicación Java ni sus pruebas.
Para regenerar el informe, con reportlab y Pillow disponibles:

```powershell
python entrega/generar_informe.py --datos entrega/datos_doc.json --resultados entrega/evidencias/resultados-pruebas.json --repo . --main-log entrega/evidencias/ejecucion-main.log --test-log entrega/evidencias/pruebas.log
```

El generador exige resultados reales P01-P11 aprobados y vuelve a leer el historial Git.
El historial del documento tiene un corte anterior al commit del propio PDF para evitar autorreferencia.
Los logs completos y hashes se entregan en evidencias. Son registros de procesos reales,
no capturas de pantalla de IntelliJ ni imágenes fabricadas.
