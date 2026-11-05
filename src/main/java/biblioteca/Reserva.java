
package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;

public class Reserva {
    private final String codigo;
    private final Estudiante estudiante;
    private final LocalDate fecha;
    private final LocalTime horarioInicio;
    private final int duracionHoras;
    private final int cantidadPersonas;
    private final Sala sala;
    private EstadoReserva estado;

    Reserva(String codigo, Estudiante estudiante,
            LocalDate fecha, LocalTime horarioInicio,
            int duracionHoras, int cantidadPersonas, Sala sala) {
        this.codigo = codigo;
        this.estudiante = estudiante;
        this.fecha = fecha;
        this.horarioInicio = horarioInicio;
        this.duracionHoras = duracionHoras;
        this.cantidadPersonas = cantidadPersonas;
        this.sala = sala;
        this.estado = new Pendiente();
    }

    public String getCodigo() {
        return codigo;
    }

    public Estudiante getEstudiante() {
        return estudiante;
    }

    public LocalDate getFecha() {
        return fecha;
    }

    public LocalTime getHorarioInicio() {
        return horarioInicio;
    }

    public int getDuracionHoras() {
        return duracionHoras;
    }

    public int getCantidadPersonas() {
        return cantidadPersonas;
    }

    public Sala getSala() {
        return sala;
    }

    public EstadoReserva getEstado() {
        return estado;
    }

    public void cambiarEstado(EstadoReserva nuevoEstado) {
        this.estado = nuevoEstado;
    }

    public void confirmar() {
        estado.confirmar(this);
    }

    public void cancelar() {
        estado.cancelar(this);
    }

    public void finalizar() {
        estado.finalizar(this);
    }


    @Override
    public String toString() {
        return "Reserva " + codigo + " | " + estudiante.getNombre()
                + " | " + fecha + " " + horarioInicio
                + " | Estado: " + estado.nombre();
    }
}
