package biblioteca;

public class Cancelada implements EstadoReserva {

    public String nombre() {
        return "Cancelada";
    }

    public void confirmar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede confirmar una reserva cancelada.");
    }

    public void cancelar(Reserva reserva) {
        throw new IllegalStateException(
                "La reserva ya está cancelada.");
    }

    public void finalizar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede finalizar una reserva cancelada.");
    }
}
