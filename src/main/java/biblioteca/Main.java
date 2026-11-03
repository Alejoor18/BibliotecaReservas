
package biblioteca;

import java.time.LocalDate;
import java.time.LocalTime;

public class Main {

    public static void main(String[] args) {

        Estudiante estudiante =
                new Estudiante("1001", "Alejandro");

        Sala sala = new Sala("B", "Sala B", 4);

        Reserva reserva = new Reserva.Builder()
                .estudiante(estudiante)
                .sala(sala)
                .fecha(LocalDate.of(2026, 11, 5))
                .hora(LocalTime.of(10, 0))
                .participantes(3)
                .build();

        System.out.println("=== SISTEMA DE BIBLIOTECA ===");
        System.out.println(reserva);
    }
}
