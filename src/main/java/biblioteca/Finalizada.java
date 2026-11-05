
package biblioteca;

public class Finalizada implements EstadoReserva {

    @Override
    public String nombre() {
        return "Finalizada";
    }

    @Override
    public void confirmar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede confirmar una reserva finalizada.");
    }

    @Override
    public void cancelar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede cancelar una reserva finalizada.");
    }

    @Override
    public void finalizar(Reserva reserva) {
        throw new IllegalStateException(
                "La reserva ya está finalizada.");
    }
}
