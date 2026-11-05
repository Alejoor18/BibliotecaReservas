package biblioteca;

public class Finalizada implements EstadoReserva {

    public String nombre() {
        return "Finalizada";
    }

    public void confirmar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede confirmar una reserva finalizada.");
    }

    public void cancelar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede cancelar una reserva finalizada.");
    }

    public void finalizar(Reserva reserva) {
        throw new IllegalStateException(
                "La reserva ya está finalizada.");
    }
}
