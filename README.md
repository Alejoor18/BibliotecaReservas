# BibliotecaReservas

Prototipo académico de consola en Java 17. Implementa Builder, Strategy,
Facade, Observer y State con 21 archivos en el paquete biblioteca. Sin
dependencias de aplicación externas, interfaz gráfica ni base de datos.

## Ejecución en Windows

Desde PowerShell, en la raíz del proyecto:

```powershell
powershell -ExecutionPolicy Bypass -File .\ejecutar.ps1
```

El script usa el JDK 17 instalado en .jdks del usuario si está disponible,
o JAVA_HOME. Para indicar otro JDK 17 o superior:

```powershell
powershell -ExecutionPolicy Bypass -File .\ejecutar.ps1 -JavaHome "C:\ruta\al\jdk-17"
```

No cambia JAVA_HOME ni el PATH del sistema y compila en una carpeta temporal.
La demostración ejecuta los cuatro escenarios oficiales y termina; no pide
datos por teclado. Fechas relativas y códigos UUID cambian entre ejecuciones.

En IntelliJ: abrir pom.xml, seleccionar SDK17 y ejecutar biblioteca.Main.
El IDE incluye Maven. La terminal de este computador tenía Java8 en PATH,
por lo que ejecutar simplemente java podía fallar aunque el IDE usara Java17.

## Pruebas reproducibles

```powershell
powershell -ExecutionPolicy Bypass -File .\entrega\pruebas\ejecutar-pruebas.ps1
```

45 casos sin frameworks: P01-P11, 12 combinaciones de State y 22 negativas
o comprobaciones adicionales. El runner falla si alguna prueba falla y guarda
logs, resultados JSON, comandos y hashes de fuentes en entrega/evidencias.
Puede recibir -JavaHome y -OutputDirectory para conservar evidencia previa.

## Maven

Con Maven y JAVA_HOME configurados hacia JDK17 o superior:

```powershell
mvn clean package
java -cp target/BibliotecaReservas-1.0-SNAPSHOT.jar biblioteca.Main
```

El arnés nativo se ejecuta con el comando anterior; no se presenta mvn test
como si ejecutara esas45 pruebas. No hay Maven Wrapper ni JAR con manifiesto
Main-Class. La primera compilación Maven puede descargar sus plugins.

## Entrega y alcance

entrega contiene el informe académico PDF, su fuente Markdown y generador,
diagramas, pruebas, evidencias reales y trazabilidad Git por estaciones.
El material de entrada está excluido de Git y de la distribución.

Las salas A2, B4, C6 y D8 forman una lista fija. Una sala puede aparecer en
múltiples reservas: no hay agenda, bloqueo por horario ni persistencia entre
ejecuciones. La simulación de notificación y registro imprime en consola;
no envía mensajes externos. El código reproduce las reglas del laboratorio.
