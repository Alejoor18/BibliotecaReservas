package biblioteca;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Optional;
public class ReservaFacade {
    private final RepositorioSalas repositorioSalas;
    private final RepositorioReservas repositorioReservas;
    public ReservaFacade(RepositorioSalas repositorioSalas,
                         RepositorioReservas repositorioReservas) {
        this.repositorioSalas = repositorioSalas;
        this.repositorioReservas = repositorioReservas;
    }
    public Optional<Reserva> realizarReserva(
            Estudiante estudiante, LocalDate fecha, LocalTime hora,
            int duracion, int personas, EstrategiaSeleccionSala estrategia) {
        var disponibles = repositorioSalas.obtenerDisponibles();
        Optional<Sala> sala = estrategia.seleccionar(disponibles, personas);
        if (sala.isEmpty()) {
            System.out.println("No hay una sala disponible que cumpla la solicitud.");
            return Optional.empty();
        }
        Reserva reserva = new ReservaBuilder()
            .estudiante(estudiante)
            .fecha(fecha)
            .horaInicio(hora)
            .duracionHoras(duracion)
            .cantidadPersonas(personas)
            .sala(sala.get())
            .build();
        repositorioReservas.guardar(reserva);
        reserva.confirmar();
        return Optional.of(reserva);
    }
}
