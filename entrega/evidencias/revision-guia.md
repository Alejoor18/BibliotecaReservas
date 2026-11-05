# Verificación de la guía original y del video

Fecha de revisión: 4 de noviembre de 2026 (America/Bogota). Las comprobaciones describen material efectivamente inspeccionado.

## Alcance y fuentes

Se leyó completo `03_PROMPT_Y_PLAN/PROMPT_MAESTRO_CODEX.md` y se inspeccionaron visualmente, una por una, las quince imágenes `01_GUIA_CAPTURAS/pagina_01.png` a `pagina_15.png`. Se ampliaron 09, 12 y 14 para resolver código y preguntas. El índice orientativo no coincide exactamente con los archivos: el Main final completo está en pagina_12.png, la validación 8.1 y P01–P06 en pagina_13.png, y P07–P11/preguntas en pagina_14.png.

El MP4 original se decodificó íntegramente con FFmpeg obtenido mediante una instalación temporal de imageio-ffmpeg fuera del repositorio. La primera instalación fue bloqueada por red del sandbox; la repetición con aprobación automática fue aceptada. No se cambió el proyecto. VLC pudo leer duración pero su filtro scene no produjo imágenes; no se utilizó como evidencia visual. La extracción con FFmpeg sí finalizó con código 0.

Video: 50.17 segundos; H.264 High 1280×720, 30 fps; audio AAC estéreo 48 kHz. Se extrajeron 50 fotogramas a un fotograma por segundo, `video-frames/segundo-01.png` a `segundo-50.png`. Se revisaron las cinco hojas `contacto-1.png` a `contacto-5.png`, que abarcan todos los fotogramas. El recorrido enseña las mismas quince páginas, desde la portada hasta las limitaciones finales; OBS aparece al comienzo y al final. No se observó instrucción adicional de ramas. El análisis de todo el audio dio mean_volume=-91.0 dB y max_volume=-91.0 dB, con las 4 810 752 muestras en ese nivel: pista silenciosa, sin narración identificable. No se afirma haber oído una explicación docente.

Las ocho estaciones son exigencia de la guía. Ocho ramas y sus nombres constituyen una organización solicitada en el prompt del estudiante; no se atribuyen al profesor.

## Inventario visual por archivo de captura

| Captura | Contenido verificado |
|---|---|
| 01 | Título, asignatura, JDK17+, consola individual sin BD, cinco patrones, salas A2/B4/C6/D8. |
| 02 | Reglas funcionales, 21 archivos, estación1 con decisión de sala adecuada. |
| 03 | Fin flujo, Estudiante y Sala exactos; Main inicial comienza. |
| 04 | Main inicial A–D y Reserva base, campos, getters y State. |
| 05 | Reserva.toString y Builder completo, validaciones y UUID. |
| 06 | Fin prueba Builder, Strategy y tres clases. |
| 07 | Pruebas Strategy, interfaces repositorios y RepositorioSalasMemoria. |
| 08 | RepositorioReservasMemoria y ReservaFacade inicial. |
| 09 | Observer: interfaz, notificador, registro y ampliación Reserva. |
| 10 | Constructor Facade con observadores, registro antes de guardar y confirmar, State. |
| 11 | Estados terminales, pruebas State e imports Main final. |
| 12 | Main final completo y nota de disponibilidad simulada. |
| 13 | Validación8.1, SOLID, antipatrones, P01–P06. |
| 14 | P07–P11, entregables, criterios, preguntas14–22, recomendaciones. |
| 15 | Fin recomendaciones y limitaciones expresas. |

## Reglas y código literal relevante

### Estación 1

Flujo oficial: el estudiante registra datos; el sistema consulta salas; la estrategia selecciona; Builder construye y valida; Facade registra y coordina confirmación; State valida; Observer comunica; el estudiante puede cancelar o finalizar según estado. La decisión «¿hay una sala adecuada?» termina sin reserva confirmada cuando no hay capacidad. Deben explicarse al menos cinco responsabilidades fuera de Main.

### Sala

```java
if (codigo == null || codigo.isBlank() || nombre == null || nombre.isBlank()
        || capacidad <= 0) {
    throw new IllegalArgumentException("Datos de sala inválidos.");
}
```

```java
@Override
public String toString() {
    return nombre + " (" + codigo + ", capacidad: " + capacidad + ")";
}
```

Estudiante tiene identificador/nombre privados finales, comprobación de null/isBlank, IllegalArgumentException("Identificador y nombre son obligatorios.") y getters.

### Reserva

Campos: codigo, estudiante, fecha, horaInicio, duracionHoras, cantidadPersonas, sala y estado. El constructor tiene acceso de paquete. Todos los datos son final salvo estado. El inicial es `new Pendiente()`.

Getters: getCodigo, getEstudiante, getFecha, getHoraInicio, getDuracionHoras, getCantidadPersonas, getSala y `getNombreEstado()`. La guía no muestra un getter público que devuelva EstadoReserva.

`confirmar()`, `cancelar()` y `finalizar()` delegan al estado. `cambiarEstado` tiene acceso de paquete.

```java
@Override
public String toString() {
    return "Reserva " + codigo + " | " + estudiante.getNombre()
            + " | " + fecha + " " + horaInicio + " | " + sala
            + " | Estado: " + getNombreEstado();
}
```

Observer añade `private final List<ObservadorReserva> observadores = new ArrayList<>();`. `agregarObservador` ignora null; `retirarObservador` elimina; `cambiarEstado` obtiene nombre anterior, asigna estado, obtiene nombre actual y recorre `List.copyOf(observadores)` para llamar actualizar.

### Builder

Métodos fluidos: estudiante(Estudiante valor), fecha(LocalDate valor), horaInicio(LocalTime valor), duracionHoras(int valor), cantidadPersonas(int valor), sala(Sala valor). No código manual.

```java
public Reserva build() {
    if (estudiante == null || fecha == null || horaInicio == null || sala == null) {
        throw new IllegalStateException("Faltan datos obligatorios de la reserva.");
    }
    if (fecha.isBefore(LocalDate.now()) || duracionHoras <= 0
            || cantidadPersonas <= 0) {
        throw new IllegalStateException("Fecha, duración o cantidad de personas inválida.");
    }
    if (sala.getCapacidad() < cantidadPersonas) {
        throw new IllegalStateException("La sala no tiene capacidad suficiente.");
    }
    String codigo = "R-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    return new Reserva(codigo, estudiante, fecha, horaInicio,
            duracionHoras, cantidadPersonas, sala);
}
```

### Repositorios y Facade

RepositorioSalas: `List<Sala> obtenerDisponibles();`.
RepositorioReservas: `void guardar(Reserva reserva);`.
RepositorioSalasMemoria carga List.of con A/Sala A/2, B/Sala B/4, C/Sala C/6, D/Sala D/8.
RepositorioReservasMemoria guarda en ArrayList y obtenerTodas devuelve `Collections.unmodifiableList(reservas)`.

Facade recibe interfaces de repositorios. Después de Observer recibe además List<ObservadorReserva>, guardada como `java.util.List.copyOf(observadores)`. realizarReserva recibe estudiante, fecha, hora, duracion, personas, estrategia; obtiene disponibles; selecciona; si Optional vacío imprime `No hay una sala disponible que cumpla la solicitud.` y retorna Optional.empty(). Construye con Builder; ejecuta `observadores.forEach(reserva::agregarObservador);`; guarda; confirma; retorna Optional.of(reserva). No notifica antes de suscribir.

### Observer y textos

Interfaz: `void actualizar(Reserva reserva, String estadoAnterior, String estadoNuevo);`.

NotificadorEstudiante:
```java
System.out.println("Notificación a "
        + reserva.getEstudiante().getNombre()
        + ": su reserva " + reserva.getCodigo()
        + " cambió de " + anterior + " a " + nuevo + ".");
```

RegistroEventos:
```java
System.out.println("Evento registrado: " + reserva.getCodigo()
        + " cambió de " + anterior + " a " + nuevo + ".");
```

### State

Permitidas: Pendiente→Confirmada, Pendiente→Cancelada, Confirmada→Cancelada, Confirmada→Finalizada. Las clases terminales rechazan todas las operaciones. Textos comprobados:

- Pendiente finalizar: No se puede finalizar una reserva pendiente.
- Confirmada confirmar: La reserva ya está confirmada.
- Cancelada confirmar: No se puede confirmar una reserva cancelada.
- Cancelada cancelar: La reserva ya está cancelada.
- Cancelada finalizar: No se puede finalizar una reserva cancelada.
- Finalizada confirmar: No se puede confirmar una reserva finalizada.
- Finalizada cancelar: No se puede cancelar una reserva finalizada.
- Finalizada finalizar: La reserva ya está finalizada.

Todos estos rechazos son IllegalStateException. No deben generar evento, pues solo cambiarEstado notifica.

## Main final transcrito de imagen 12 y contrastado con recorrido del video

```java
package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        RepositorioSalas salas = new RepositorioSalasMemoria();
        RepositorioReservasMemoria reservas = new RepositorioReservasMemoria();

        List<ObservadorReserva> observadores = List.of(
                new NotificadorEstudiante(),
                new RegistroEventos()
        );

        ReservaFacade fachada = new ReservaFacade(salas, reservas, observadores);

        Estudiante laura = new Estudiante("E001", "Laura");

        System.out.println("--- ESCENARIO PRINCIPAL ---");
        Reserva reserva = fachada.realizarReserva(
                laura,
                LocalDate.now().plusDays(7),
                LocalTime.of(14, 0),
                2,
                4,
                new SeleccionPorCapacidad()
        ).orElseThrow();

        System.out.println(reserva);
        System.out.println("\nLaura cancela la reserva:");
        reserva.cancelar();
        System.out.println(reserva);

        System.out.println("\nIntento inválido: confirmar una reserva cancelada:");
        try {
            reserva.confirmar();
        } catch (IllegalStateException ex) {
            System.out.println("Operación rechazada: " + ex.getMessage());
        }

        System.out.println("\n--- PRUEBA DE SALA PREFERIDA ---");
        fachada.realizarReserva(
                new Estudiante("E002", "Andrés"),
                LocalDate.now().plusDays(8),
                LocalTime.of(10, 0),
                2,
                4,
                new SeleccionSalaPreferida("C")
        ).ifPresent(System.out::println);

        System.out.println("\n--- PRUEBA SIN SALA ADECUADA ---");
        fachada.realizarReserva(
                new Estudiante("E003", "Camila"),
                LocalDate.now().plusDays(9),
                LocalTime.of(9, 0),
                2,
                10,
                new SeleccionPorCapacidad()
        );

        System.out.println("\n--- PRUEBA DE FINALIZACIÓN ---");
        Reserva otra = fachada.realizarReserva(
                new Estudiante("E004", "Samuel"),
                LocalDate.now().plusDays(10),
                LocalTime.of(11, 0),
                1,
                2,
                new SeleccionPorCapacidad()
        ).orElseThrow();
        otra.finalizar();
        System.out.println(otra);
    }
}
```

Las fechas ya son relativas en la guía. No hace falta alterar el ejemplo por calendario actual.

## Documentación, pruebas y límites exigidos

La guía exige PDF individual, flujo, clases actualizadas, explicación de los cinco patrones, evidencias legibles P01–P11, matriz con clases y conclusión técnica individual. El prompt agrega fuentes editables, portada sin inventar datos, SOLID y antipatrones, respuestas14–22 y trazabilidad Git auténtica.

P01 válida; P02 falta estudiante; P03 cuatro personas→B; P04 preferida C/cantidad4→C; P05 preferida B/cantidad7→vacío; P06 registra y confirma; P07 ambos observadores reciben Confirmada; P08 cancela y notifica; P09 rechaza confirmar cancelada sin notificar; P10 diez personas no crea reserva; P11 finaliza y notifica. También rechazos de transiciones State.

Preguntas literales de reflexión:
14. ¿Qué responsabilidades separó y qué problema habría tenido una clase única que hiciera todo?
15. ¿Qué ventaja ofrece Builder frente a un constructor con numerosos parámetros?
16. ¿Cómo permite Strategy incorporar otro criterio de selección sin modificar la fachada?
17. ¿Qué complejidad oculta Facade y qué dependencia evita que Main conozca?
18. ¿Cómo se desacoplan Reserva y los mecanismos concretos de notificación con Observer?
19. ¿Qué ventaja aporta State frente a modificar directamente una variable String?
20. Mencione dos principios SOLID que se evidencian en su solución y señale las clases involucradas.
21. Identifique un antipatrón que evitó y explique qué decisión concreta tomó para evitarlo.
22. ¿Qué limitación tiene la disponibilidad simulada y qué componente modificaría para consultar una fuente real?

Antipatrones enumerados: God Object, Long Parameter List, Primitive Obsession, Shotgun Surgery, Tight Coupling, Duplicate Code, Swallowing Exceptions y Premature Optimization.

Criterios: análisis15%; diagramas20%; cinco patrones35%; pruebas/evidencias20%; organización/explicación técnica10%.

Limitaciones expresas: consola, disponibilidad en lista fija, misma sala puede figurar en varias reservas; sin calendario real, sin control de solapamientos ni persistencia entre ejecuciones. No agregar GUI/BD/agenda real para esta entrega.
