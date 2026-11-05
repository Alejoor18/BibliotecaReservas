
package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;

public class ReservaBuilder {

    private String codigo;
    private Estudiante estudiante;
    private LocalDate fecha;
    private LocalTime horarioInicio;
    private int duracionHoras;
    private int cantidadPersonas;
    private Sala sala;

    public ReservaBuilder codigo(String codigo) {
        this.codigo = codigo;
        return this;
    }

    public ReservaBuilder estudiante(Estudiante estudiante) {
        this.estudiante = estudiante;
        return this;
    }

    public ReservaBuilder fecha(LocalDate fecha) {
        this.fecha = fecha;
        return this;
    }

    public ReservaBuilder horarioInicio(LocalTime horarioInicio) {
        this.horarioInicio = horarioInicio;
        return this;
    }

    public ReservaBuilder duracionHoras(int duracionHoras) {
        this.duracionHoras = duracionHoras;
        return this;
    }

    public ReservaBuilder cantidadPersonas(int cantidadPersonas) {
        this.cantidadPersonas = cantidadPersonas;
        return this;
    }

    public ReservaBuilder sala(Sala sala) {
        this.sala = sala;
        return this;
    }

    public Reserva build() {
        if (codigo == null || codigo.isBlank()
                || estudiante == null || fecha == null
                || horarioInicio == null || sala == null) {
            throw new IllegalArgumentException(
                    "Faltan datos obligatorios de la reserva.");
        }

        if (duracionHoras <= 0 || cantidadPersonas <= 0
                || cantidadPersonas > sala.getCapacidad()) {
            throw new IllegalArgumentException(
                    "Duración o cantidad de personas inválida.");
        }

        return new Reserva(codigo, estudiante, fecha,
                horarioInicio, duracionHoras, cantidadPersonas, sala);
    }
}
