package biblioteca;
import java.time.LocalDate;
import java.time.LocalTime;
public class Main {
    public static void main(String[] args) {
        RepositorioReservasMemoria reservas = new RepositorioReservasMemoria();
        ReservaFacade fachada = new ReservaFacade(new RepositorioSalasMemoria(), reservas,
            java.util.List.of(new NotificadorEstudiante(), new RegistroEventos()));
        Reserva reserva = fachada.realizarReserva(new Estudiante("E001", "Laura"),
            LocalDate.now().plusDays(7), LocalTime.of(14, 0), 2, 4,
            new SeleccionPorCapacidad()).orElseThrow();
        System.out.println(reserva);
        System.out.println("Reservas registradas: " + reservas.obtenerTodas().size());
    }
}
