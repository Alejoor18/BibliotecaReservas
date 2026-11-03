
package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;

public class Reserva {
    private final Estudiante estudiante;
    private final Sala sala;
    private final LocalDate fecha;
    private final LocalTime hora;
    private final int participantes;

    private Reserva(Builder builder) {
        this.estudiante = builder.estudiante;
        this.sala = builder.sala;
        this.fecha = builder.fecha;
        this.hora = builder.hora;
        this.participantes = builder.participantes;
    }

    public static class Builder {
        private Estudiante estudiante;
        private Sala sala;
        private LocalDate fecha;
        private LocalTime hora;
        private int participantes;

        public Builder estudiante(Estudiante estudiante) {
            this.estudiante = estudiante;
            return this;
        }

        public Builder sala(Sala sala) {
            this.sala = sala;
            return this;
        }

        public Builder fecha(LocalDate fecha) {
            this.fecha = fecha;
            return this;
        }

        public Builder hora(LocalTime hora) {
            this.hora = hora;
            return this;
        }

        public Builder participantes(int participantes) {
            this.participantes = participantes;
            return this;
        }

        public Reserva build() {
            if (estudiante == null || sala == null ||
                    fecha == null || hora == null) {
                throw new IllegalArgumentException(
                        "Faltan datos obligatorios");
            }

            if (participantes <= 0 ||
                    participantes > sala.getCapacidad()) {
                throw new IllegalArgumentException(
                        "Cantidad de participantes no valida");
            }

            return new Reserva(this);
        }
    }

    @Override
    public String toString() {
        return "Reserva: " + estudiante.getNombre()
                + " | " + sala.getNombre()
                + " | Fecha: " + fecha
                + " | Hora: " + hora
                + " | Participantes: " + participantes;
    }
}
