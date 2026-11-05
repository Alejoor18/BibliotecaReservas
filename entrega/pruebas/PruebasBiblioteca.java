import biblioteca.*;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/** Pruebas de aceptación nativas. No requiere -ea ni bibliotecas externas. */
public class PruebasBiblioteca {
    private static final List<Resultado> RESULTADOS = new ArrayList<>();
    private static ByteArrayOutputStream capturaActual;
    private static final String FALTANTES = "Faltan datos obligatorios de la reserva.";
    private static final String DATOS_INVALIDOS = "Fecha, duración o cantidad de personas inválida.";

    @FunctionalInterface
    private interface Caso { void ejecutar() throws Exception; }

    private record Evento(Reserva reserva, String anterior, String nuevo) { }
    private record Resultado(String id, String descripcion, boolean correcto,
                             String salida, String error) { }

    private static final class ObservadorMedido implements ObservadorReserva {
        private final ObservadorReserva delegado;
        private final List<Evento> eventos = new ArrayList<>();
        ObservadorMedido(ObservadorReserva delegado) { this.delegado = delegado; }
        @Override public void actualizar(Reserva reserva, String anterior, String nuevo) {
            eventos.add(new Evento(reserva, anterior, nuevo));
            delegado.actualizar(reserva, anterior, nuevo);
        }
    }

    private static final class Escenario {
        final RepositorioReservasMemoria repositorio = new RepositorioReservasMemoria();
        final ObservadorMedido estudiante = new ObservadorMedido(new NotificadorEstudiante());
        final ObservadorMedido registro = new ObservadorMedido(new RegistroEventos());
        final ReservaFacade fachada = new ReservaFacade(new RepositorioSalasMemoria(),
                repositorio, List.of(estudiante, registro));
        Optional<Reserva> solicitar(int personas, EstrategiaSeleccionSala estrategia) {
            return fachada.realizarReserva(new Estudiante("E01", "Laura"),
                    LocalDate.now().plusDays(7), LocalTime.of(14, 0), 2, personas, estrategia);
        }
        Reserva confirmar() { return solicitar(4, new SeleccionPorCapacidad()).orElseThrow(); }
        void comprobarEventos(int cantidad) {
            comprobar(estudiante.eventos.size() == cantidad, "Eventos del notificador: " + cantidad);
            comprobar(registro.eventos.size() == cantidad, "Eventos del registro: " + cantidad);
            comprobar(estudiante.eventos.equals(registro.eventos), "Ambos observadores reciben los mismos eventos");
        }
    }

    private static ReservaBuilder builder() {
        return new ReservaBuilder().estudiante(new Estudiante("E01", "Laura"))
                .fecha(LocalDate.now().plusDays(7)).horaInicio(LocalTime.of(14, 0))
                .duracionHoras(2).cantidadPersonas(4).sala(new Sala("B", "Sala B", 4));
    }

    private static void comprobar(boolean condicion, String detalle) {
        if (!condicion) throw new AssertionError(detalle);
    }

    private static <T extends Throwable> T rechaza(Class<T> tipo, String mensaje, Runnable accion) {
        try { accion.run(); }
        catch (Throwable error) {
            comprobar(tipo.isInstance(error), "Excepción esperada " + tipo.getSimpleName()
                    + "; observada " + error.getClass().getSimpleName());
            comprobar(mensaje.equals(error.getMessage()), "Mensaje esperado: " + mensaje
                    + "; observado: " + error.getMessage());
            System.out.println("Rechazo observado: " + error.getClass().getSimpleName()
                    + ": " + error.getMessage());
            return tipo.cast(error);
        }
        throw new AssertionError("La operación no rechazó la entrada o transición inválida");
    }

    private static void caso(String id, String descripcion, Caso accion) {
        PrintStream consola = System.out;
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        capturaActual = bytes;
        String error = "";
        boolean correcto = true;
        try (PrintStream captura = new PrintStream(bytes, true, StandardCharsets.UTF_8)) {
            System.setOut(captura);
            try { accion.ejecutar(); }
            catch (Throwable fallo) {
                correcto = false;
                error = fallo.getClass().getSimpleName() + ": " + fallo.getMessage();
                fallo.printStackTrace(captura);
            } finally { System.setOut(consola); }
        }
        String salida = bytes.toString(StandardCharsets.UTF_8);
        RESULTADOS.add(new Resultado(id, descripcion, correcto, salida, error));
        consola.println("[" + (correcto ? "PASS" : "FAIL") + "] " + id + " | " + descripcion);
        consola.print(salida);
        if (!error.isEmpty()) consola.println(error);
    }

    private static void pruebasOficiales() {
        caso("P01", "Construcción con todos los datos y código generado", () -> {
            Reserva r = builder().build();
            comprobar(r.getNombreEstado().equals("Pendiente"), "Estado inicial Pendiente");
            comprobar(r.getCodigo().matches("R-[0-9A-F]{8}"), "Código R- y ocho dígitos hexadecimales");
            comprobar(r.getEstudiante().getIdentificador().equals("E01"), "Estudiante conservado");
            comprobar(r.getFecha().equals(LocalDate.now().plusDays(7)), "Fecha conservada");
            comprobar(r.getHoraInicio().equals(LocalTime.of(14, 0)), "Hora conservada");
            comprobar(r.getDuracionHoras() == 2 && r.getCantidadPersonas() == 4, "Duración y personas");
            comprobar(r.getSala().getCodigo().equals("B"), "Sala conservada");
            System.out.println(r);
        });
        caso("P02", "Construcción sin estudiante rechazada con mensaje claro", () ->
                rechaza(IllegalStateException.class, FALTANTES, () -> builder().estudiante(null).build()));
        caso("P03", "Capacidad para cuatro personas selecciona Sala B", () -> {
            Sala sala = new SeleccionPorCapacidad().seleccionar(new RepositorioSalasMemoria().obtenerDisponibles(), 4).orElseThrow();
            comprobar(sala.getCodigo().equals("B"), "Menor capacidad suficiente es B");
            System.out.println(sala);
        });
        caso("P04", "Preferida C para cuatro personas selecciona Sala C", () -> {
            Sala sala = new SeleccionSalaPreferida("C").seleccionar(new RepositorioSalasMemoria().obtenerDisponibles(), 4).orElseThrow();
            comprobar(sala.getCodigo().equals("C"), "Código C seleccionado");
            System.out.println(sala);
        });
        caso("P05", "Preferida B para siete personas no selecciona sala", () -> {
            Optional<Sala> sala = new SeleccionSalaPreferida("B").seleccionar(new RepositorioSalasMemoria().obtenerDisponibles(), 7);
            comprobar(sala.isEmpty(), "B no tiene capacidad suficiente");
            System.out.println("Selección observada: " + sala);
        });
        caso("P06", "La fachada registra y confirma la misma reserva", () -> {
            Escenario e = new Escenario();
            Reserva r = e.confirmar();
            comprobar(e.repositorio.obtenerTodas().size() == 1, "Una reserva registrada");
            comprobar(e.repositorio.obtenerTodas().get(0) == r, "Se devuelve el objeto registrado");
            comprobar(r.getNombreEstado().equals("Confirmada"), "Confirmada al devolver el resultado");
            System.out.println("Reservas registradas: " + e.repositorio.obtenerTodas().size());
            System.out.println(r);
        });
        caso("P07", "Confirmación notifica a los dos observadores reales", () -> {
            Escenario e = new Escenario();
            Reserva r = e.confirmar();
            e.comprobarEventos(1);
            Evento evento = e.estudiante.eventos.get(0);
            comprobar(evento.reserva() == r && evento.anterior().equals("Pendiente")
                    && evento.nuevo().equals("Confirmada"), "Evento Pendiente -> Confirmada");
            String salidaReal = capturaActual.toString(StandardCharsets.UTF_8);
            comprobar(salidaReal.contains("Notificación a Laura: su reserva " + r.getCodigo()
                    + " cambió de Pendiente a Confirmada."), "Salida real de NotificadorEstudiante");
            comprobar(salidaReal.contains("Evento registrado: " + r.getCodigo()
                    + " cambió de Pendiente a Confirmada."), "Salida real de RegistroEventos");
            System.out.println("NotificadorEstudiante: 1 evento; RegistroEventos: 1 evento.");
        });
        caso("P08", "Cancelar una confirmada cambia el estado y notifica", () -> {
            Escenario e = new Escenario();
            Reserva r = e.confirmar();
            r.cancelar();
            comprobar(r.getNombreEstado().equals("Cancelada"), "Estado Cancelada");
            e.comprobarEventos(2);
            Evento evento = e.estudiante.eventos.get(1);
            comprobar(evento.anterior().equals("Confirmada") && evento.nuevo().equals("Cancelada"), "Evento Confirmada -> Cancelada");
            System.out.println("Tras cancelar: " + r.getNombreEstado() + "; eventos acumulados por observador: 2.");
        });
        caso("P09", "Confirmar cancelada se rechaza sin nuevas notificaciones", () -> {
            Escenario e = new Escenario();
            Reserva r = e.confirmar();
            r.cancelar();
            e.comprobarEventos(2);
            System.out.println("Inicio del intento inválido; eventos por observador antes: 2.");
            rechaza(IllegalStateException.class, "No se puede confirmar una reserva cancelada.", r::confirmar);
            comprobar(r.getNombreEstado().equals("Cancelada"), "El rechazo conserva Cancelada");
            e.comprobarEventos(2);
            comprobar(e.repositorio.obtenerTodas().size() == 1, "El rechazo no duplica el registro");
            System.out.println("Eventos por observador después: 2; diferencia: 0.");
        });
        caso("P10", "Diez personas no crean ni registran reserva", () -> {
            Escenario e = new Escenario();
            Optional<Reserva> reserva = e.solicitar(10, new SeleccionPorCapacidad());
            comprobar(reserva.isEmpty(), "Resultado vacío");
            comprobar(e.repositorio.obtenerTodas().isEmpty(), "Cero reservas registradas");
            e.comprobarEventos(0);
            System.out.println("Resultado: " + reserva + "; registros: 0; eventos: 0.");
        });
        caso("P11", "Finalizar confirmada cambia el estado y notifica", () -> {
            Escenario e = new Escenario();
            Reserva r = e.confirmar();
            r.finalizar();
            comprobar(r.getNombreEstado().equals("Finalizada"), "Estado Finalizada");
            e.comprobarEventos(2);
            Evento evento = e.estudiante.eventos.get(1);
            comprobar(evento.anterior().equals("Confirmada") && evento.nuevo().equals("Finalizada"), "Evento Confirmada -> Finalizada");
            System.out.println("Tras finalizar: " + r.getNombreEstado() + "; eventos acumulados por observador: 2.");
        });
    }

    private static void transiciones() {
        String[] estados = {"Pendiente", "Confirmada", "Cancelada", "Finalizada"};
        String[] acciones = {"confirmar", "cancelar", "finalizar"};
        String[][] destinos = {{"Confirmada", "Cancelada", null},
                {null, "Cancelada", "Finalizada"}, {null, null, null}, {null, null, null}};
        String[][] mensajes = {{null, null, "No se puede finalizar una reserva pendiente."},
                {"La reserva ya está confirmada.", null, null},
                {"No se puede confirmar una reserva cancelada.", "La reserva ya está cancelada.", "No se puede finalizar una reserva cancelada."},
                {"No se puede confirmar una reserva finalizada.", "No se puede cancelar una reserva finalizada.", "La reserva ya está finalizada."}};
        for (int s = 0; s < estados.length; s++) {
            for (int a = 0; a < acciones.length; a++) {
                final int estado = s, accion = a;
                String id = String.format("T%02d", s * 3 + a + 1);
                caso(id, estados[s] + " / " + acciones[a], () -> {
                    Reserva r = builder().build();
                    ObservadorMedido primero = new ObservadorMedido(new NotificadorEstudiante());
                    ObservadorMedido segundo = new ObservadorMedido(new RegistroEventos());
                    r.agregarObservador(primero);
                    r.agregarObservador(segundo);
                    if (estado == 1 || estado == 3) r.confirmar();
                    if (estado == 2) r.cancelar();
                    if (estado == 3) r.finalizar();
                    int antes = primero.eventos.size();
                    Runnable operacion = switch (accion) {
                        case 0 -> r::confirmar;
                        case 1 -> r::cancelar;
                        default -> r::finalizar;
                    };
                    if (destinos[estado][accion] == null) {
                        rechaza(IllegalStateException.class, mensajes[estado][accion], operacion);
                        comprobar(r.getNombreEstado().equals(estados[estado]), "Se conserva estado tras rechazo");
                        comprobar(primero.eventos.size() == antes && segundo.eventos.size() == antes, "Sin eventos nuevos en rechazo");
                    } else {
                        operacion.run();
                        comprobar(r.getNombreEstado().equals(destinos[estado][accion]), "Destino permitido");
                        comprobar(primero.eventos.size() == antes + 1 && segundo.eventos.size() == antes + 1, "Un evento nuevo por observador");
                    }
                    System.out.println("Estado observado: " + r.getNombreEstado() + "; eventos nuevos por observador: " + (primero.eventos.size() - antes));
                });
            }
        }
    }

    private static void validacionesAdicionales() {
        caso("V01", "Builder rechaza fecha ausente", () -> rechaza(IllegalStateException.class, FALTANTES, () -> builder().fecha(null).build()));
        caso("V02", "Builder rechaza hora ausente", () -> rechaza(IllegalStateException.class, FALTANTES, () -> builder().horaInicio(null).build()));
        caso("V03", "Builder rechaza sala ausente", () -> rechaza(IllegalStateException.class, FALTANTES, () -> builder().sala(null).build()));
        caso("V04", "Builder rechaza fecha pasada", () -> rechaza(IllegalStateException.class, DATOS_INVALIDOS, () -> builder().fecha(LocalDate.now().minusDays(1)).build()));
        caso("V05", "Builder rechaza duración cero", () -> rechaza(IllegalStateException.class, DATOS_INVALIDOS, () -> builder().duracionHoras(0).build()));
        caso("V06", "Builder rechaza duración negativa", () -> rechaza(IllegalStateException.class, DATOS_INVALIDOS, () -> builder().duracionHoras(-1).build()));
        caso("V07", "Builder rechaza cero personas", () -> rechaza(IllegalStateException.class, DATOS_INVALIDOS, () -> builder().cantidadPersonas(0).build()));
        caso("V08", "Builder rechaza personas negativas", () -> rechaza(IllegalStateException.class, DATOS_INVALIDOS, () -> builder().cantidadPersonas(-1).build()));
        caso("V09", "Builder rechaza exceso de capacidad", () -> rechaza(IllegalStateException.class, "La sala no tiene capacidad suficiente.", () -> builder().cantidadPersonas(5).build()));
        caso("V10", "Sala rechaza capacidad cero", () -> rechaza(IllegalArgumentException.class, "Datos de sala inválidos.", () -> new Sala("X", "Sala X", 0)));
        caso("V11", "Sala rechaza capacidad negativa", () -> rechaza(IllegalArgumentException.class, "Datos de sala inválidos.", () -> new Sala("X", "Sala X", -1)));
        caso("V12", "Estudiante rechaza identificador nulo y nombre blanco", () -> {
            rechaza(IllegalArgumentException.class, "Identificador y nombre son obligatorios.", () -> new Estudiante(null, "Laura"));
            rechaza(IllegalArgumentException.class, "Identificador y nombre son obligatorios.", () -> new Estudiante("E01", " "));
        });
        caso("V13", "Sala rechaza código blanco y nombre nulo", () -> {
            rechaza(IllegalArgumentException.class, "Datos de sala inválidos.", () -> new Sala(" ", "Sala X", 2));
            rechaza(IllegalArgumentException.class, "Datos de sala inválidos.", () -> new Sala("X", null, 2));
        });
        caso("V14", "Preferida rechaza código nulo o blanco", () -> {
            rechaza(IllegalArgumentException.class, "Debe indicar la sala preferida.", () -> new SeleccionSalaPreferida(null));
            rechaza(IllegalArgumentException.class, "Debe indicar la sala preferida.", () -> new SeleccionSalaPreferida(" "));
        });
        caso("V15", "Preferida compara código sin distinguir mayúsculas", () -> {
            comprobar(new SeleccionSalaPreferida("c").seleccionar(new RepositorioSalasMemoria().obtenerDisponibles(), 4).orElseThrow().getCodigo().equals("C"), "c selecciona C");
            System.out.println("Código solicitado: c; seleccionado: C.");
        });
        caso("V16", "Una lista de salas vacía no produce selección", () -> {
            comprobar(new SeleccionPorCapacidad().seleccionar(List.of(), 4).isEmpty(), "Capacidad sobre lista vacía");
            comprobar(new SeleccionSalaPreferida("C").seleccionar(List.of(), 4).isEmpty(), "Preferida sobre lista vacía");
            System.out.println("Ambas estrategias devolvieron Optional.empty.");
        });
        caso("V17", "Repositorio expone una vista inmodificable", () -> {
            Escenario e = new Escenario();
            List<Reserva> vista = e.repositorio.obtenerTodas();
            Reserva r = e.confirmar();
            comprobar(vista.size() == 1 && vista.get(0) == r, "La vista refleja el registro posterior");
            try { vista.clear(); throw new AssertionError("La vista permitió modificar el repositorio"); }
            catch (UnsupportedOperationException esperado) { System.out.println("clear() rechazado con UnsupportedOperationException."); }
            comprobar(e.repositorio.obtenerTodas().size() == 1, "El registro se conserva");
        });
        caso("V18", "Retirar observadores durante notificación usa copia estable", () -> {
            Reserva r = builder().build();
            List<String> eventos = new ArrayList<>();
            ObservadorReserva segundo = (reserva, anterior, nuevo) -> eventos.add("segundo:" + nuevo);
            ObservadorReserva primero = (reserva, anterior, nuevo) -> {
                eventos.add("primero:" + nuevo);
                reserva.retirarObservador(segundo);
            };
            r.agregarObservador(null);
            r.agregarObservador(primero);
            r.agregarObservador(segundo);
            r.confirmar();
            comprobar(eventos.equals(List.of("primero:Confirmada", "segundo:Confirmada")), "Ambos reciben el evento en curso");
            r.cancelar();
            comprobar(eventos.equals(List.of("primero:Confirmada", "segundo:Confirmada", "primero:Cancelada")), "El retirado no recibe el siguiente evento");
            System.out.println("Eventos observados: " + eventos);
        });
        caso("V19", "El cambio de estado interno no es público", () -> {
            var metodo = Reserva.class.getDeclaredMethod("cambiarEstado", EstadoReserva.class);
            comprobar(!Modifier.isPublic(metodo.getModifiers()) && !Modifier.isProtected(metodo.getModifiers())
                    && !Modifier.isPrivate(metodo.getModifiers()), "Acceso de paquete según guía");
            System.out.println("cambiarEstado tiene acceso de paquete.");
        });
        caso("V20", "Disponibilidad simulada permite reutilizar sala en varias reservas", () -> {
            Escenario e = new Escenario();
            Reserva a = e.confirmar(), b = e.confirmar();
            comprobar(a.getSala().getCodigo().equals("B") && b.getSala().getCodigo().equals("B"), "B seleccionada para ambas");
            comprobar(e.repositorio.obtenerTodas().size() == 2, "Dos registros en memoria");
            System.out.println("Dos reservas para B en el mismo horario, conforme al alcance simulado.");
        });
        caso("V21", "Datos inválidos no se guardan ni notifican en Facade", () -> {
            Escenario e = new Escenario();
            rechaza(IllegalStateException.class, FALTANTES, () -> e.fachada.realizarReserva(null,
                    LocalDate.now().plusDays(7), LocalTime.of(14, 0), 2, 4, new SeleccionPorCapacidad()));
            comprobar(e.repositorio.obtenerTodas().isEmpty(), "No se registra al fallar Builder");
            e.comprobarEventos(0);
            System.out.println("Registros: 0; eventos: 0.");
        });
        caso("V22", "Sala y Reserva incluyen la sala legible en consola", () -> {
            Sala sala = new Sala("B", "Sala B", 4);
            comprobar(sala.toString().equals("Sala B (B, capacidad: 4)"), "toString Sala según guía");
            Reserva r = builder().build();
            comprobar(r.toString().contains(" | Sala B (B, capacidad: 4) | Estado: Pendiente"), "Reserva incluye sala y estado");
            System.out.println(r);
        });
    }

    private static String json(String valor) {
        StringBuilder salida = new StringBuilder("\"");
        for (char c : valor.toCharArray()) {
            switch (c) {
                case '\\' -> salida.append("\\\\");
                case '"' -> salida.append("\\\"");
                case '\n' -> salida.append("\\n");
                case '\r' -> salida.append("\\r");
                case '\t' -> salida.append("\\t");
                default -> { if (c < 32) salida.append(String.format("\\u%04x", (int) c)); else salida.append(c); }
            }
        }
        return salida.append('"').toString();
    }

    public static void main(String[] args) throws Exception {
        pruebasOficiales();
        transiciones();
        validacionesAdicionales();
        long aprobadas = RESULTADOS.stream().filter(Resultado::correcto).count();
        System.out.println("RESUMEN: " + aprobadas + "/" + RESULTADOS.size() + " casos correctos.");
        if (args.length > 0) {
            StringBuilder datos = new StringBuilder("{\n  \"ejecutadoUtc\": ").append(json(Instant.now().toString()))
                    .append(",\n  \"javaVersion\": ").append(json(System.getProperty("java.version")))
                    .append(",\n  \"total\": ").append(RESULTADOS.size()).append(",\n  \"aprobadas\": ").append(aprobadas)
                    .append(",\n  \"fallidas\": ").append(RESULTADOS.size() - aprobadas).append(",\n  \"casos\": [\n");
            for (int i = 0; i < RESULTADOS.size(); i++) {
                Resultado r = RESULTADOS.get(i);
                if (i > 0) datos.append(",\n");
                datos.append("    {\"id\": ").append(json(r.id())).append(", \"descripcion\": ").append(json(r.descripcion()))
                        .append(", \"resultado\": ").append(json(r.correcto() ? "PASS" : "FAIL"))
                        .append(", \"salidaReal\": ").append(json(r.salida())).append(", \"error\": ").append(json(r.error())).append('}');
            }
            datos.append("\n  ]\n}\n");
            Path destino = Path.of(args[0]);
            if (destino.getParent() != null) Files.createDirectories(destino.getParent());
            Files.writeString(destino, datos, StandardCharsets.UTF_8);
        }
        if (aprobadas != RESULTADOS.size()) System.exit(1);
    }
}
