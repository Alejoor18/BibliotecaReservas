package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.UUID;

public class ReservaBuilder {
    private Estudiante estudiante;
    private LocalDate fecha;
    private LocalTime horaInicio;
    private int duracionHoras;
    private int cantidadPersonas;
    private Sala sala;

    public ReservaBuilder estudiante(Estudiante valor) {
        this.estudiante = valor; return this;
    }
    public ReservaBuilder fecha(LocalDate valor) {
        this.fecha = valor; return this;
    }
    public ReservaBuilder horaInicio(LocalTime valor) {
        this.horaInicio = valor; return this;
    }
    public ReservaBuilder duracionHoras(int valor) {
        this.duracionHoras = valor; return this;
    }
    public ReservaBuilder cantidadPersonas(int valor) {
        this.cantidadPersonas = valor; return this;
    }
    public ReservaBuilder sala(Sala valor) {
        this.sala = valor; return this;
    }

    public Reserva build() {
        if (estudiante == null || fecha == null || horaInicio == null || sala == null) {
            throw new IllegalStateException("Faltan datos obligatorios de la reserva.");
        }
        if (fecha.isBefore(LocalDate.now()) || duracionHoras <= 0
                || cantidadPersonas <= 0) {
            throw new IllegalStateException("Fecha, duración o cantidad de personas inválida.");
        }
        if (sala.getCapacidad() < cantidadPersonas) {
            throw new IllegalStateException("La sala no tiene capacidad suficiente.");
        }
        String codigo = "R-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
        return new Reserva(codigo, estudiante, fecha, horaInicio,
                duracionHoras, cantidadPersonas, sala);
    }
}
