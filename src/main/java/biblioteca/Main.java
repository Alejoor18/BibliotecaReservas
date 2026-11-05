package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;

public class Main {
    public static void main(String[] args) {
        Reserva reserva = new ReservaBuilder()
            .estudiante(new Estudiante("E001", "Laura"))
            .fecha(LocalDate.now().plusDays(7))
            .horaInicio(LocalTime.of(14, 0))
            .duracionHoras(2)
            .cantidadPersonas(4)
            .sala(new Sala("B", "Sala B", 4))
            .build();
        System.out.println(reserva);
    }
}
