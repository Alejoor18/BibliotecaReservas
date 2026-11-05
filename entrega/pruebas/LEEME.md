# Pruebas nativas de BibliotecaReservas

Los archivos de esta carpeta se integran en `entrega/pruebas`, fuera de los 21 fuentes oficiales de `src/main/java/biblioteca`. No utilizan dependencias externas, JUnit ni la opción `-ea`: las comprobaciones fallan explícitamente con `AssertionError` y el proceso devuelve código 1 si algún caso falla.

Ejecutar desde PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\entrega\pruebas\ejecutar-pruebas.ps1 -JavaHome "C:\Users\aleja\.jdks\ms-17.0.21.0.2"
```

Con PowerShell 7 también puede utilizar `pwsh`. Si el script se ejecuta desde otra ubicación, indique `-ProjectRoot` con la carpeta que contiene `pom.xml`. `-OutputDirectory` permite elegir otra carpeta de evidencias. Por defecto se usa `entrega/evidencias` y se compila en una nueva carpeta temporal para no depender de clases antiguas de `target`.

El harness cubre 45 casos: P01–P11, las 12 combinaciones de cuatro estados y tres operaciones (T01–T12), y 22 casos adicionales (V01–V22). P07–P11 emplean observadores medidos que delegan en los dos observadores reales de producción. Se comprueban cantidad, reserva y contenido de los eventos; P09 verifica que el rechazo conserve tanto el estado como el número de notificaciones.

El runner escribe exclusivamente resultados de ejecuciones realizadas: `compilacion.log`, `pruebas.log`, `ejecucion-main.log`, `resultados-pruebas.json`, `comandos-ejecutados.log` y `entorno-ejecucion.json`. Este último registra versiones, códigos de salida, reloj real UTC/Bogotá y hashes SHA-256 de los fuentes compilados. Son logs de consola y datos de ejecución; no son capturas de la interfaz de IntelliJ.

La elección de fechas usa `LocalDate.now()` como la guía. Las evidencias deben conservar su fecha real de ejecución, aunque difiera de la fecha de preparación del informe. Los códigos de reserva se generan con UUID y cambiarán entre ejecuciones.
