package biblioteca;
public class RegistroEventos implements ObservadorReserva {
    @Override
    public void actualizar(Reserva reserva, String anterior, String nuevo) {
        System.out.println("Evento registrado: " + reserva.getCodigo()
            + " cambió de " + anterior + " a " + nuevo + ".");
    }
}
