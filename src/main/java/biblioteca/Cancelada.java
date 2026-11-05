
package biblioteca;

public class Cancelada implements EstadoReserva {

    @Override
    public String nombre() {
        return "Cancelada";
    }

    @Override
    public void confirmar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede confirmar una reserva cancelada.");
    }

    @Override
    public void cancelar(Reserva reserva) {
        throw new IllegalStateException(
                "La reserva ya está cancelada.");
    }

    @Override
    public void finalizar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede finalizar una reserva cancelada.");
    }
}
