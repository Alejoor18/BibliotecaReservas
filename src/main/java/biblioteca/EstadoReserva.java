
package biblioteca;

public interface EstadoReserva {
    String nombre();
    void confirmar(Reserva reserva);
    void cancelar(Reserva reserva);
    void finalizar(Reserva reserva);
}
