package biblioteca;
public class NotificadorEstudiante implements ObservadorReserva {
    @Override
    public void actualizar(Reserva reserva, String anterior, String nuevo) {
        System.out.println("Notificación a "
            + reserva.getEstudiante().getNombre()
            + ": su reserva " + reserva.getCodigo()
            + " cambió de " + anterior + " a " + nuevo + ".");
    }
}
