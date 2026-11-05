
package biblioteca;

public class Pendiente implements EstadoReserva {

    public String nombre() {
        return "Pendiente";
    }

    public void confirmar(Reserva reserva) {
        reserva.cambiarEstado(new Confirmada());
    }

    public void cancelar(Reserva reserva) {
        reserva.cambiarEstado(new Cancelada());
    }

    public void finalizar(Reserva reserva) {
        throw new IllegalStateException(
                "No se puede finalizar una reserva pendiente.");
    }
}
