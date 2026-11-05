package biblioteca;
public interface ObservadorReserva {
    void actualizar(Reserva reserva, String estadoAnterior, String estadoNuevo);
}
