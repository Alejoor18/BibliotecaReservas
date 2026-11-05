
package biblioteca;

import java.util.List;
import java.util.Optional;

public class SeleccionSalaPreferida implements EstrategiaSeleccionSala {

    private final String codigoPreferido;

    public SeleccionSalaPreferida(String codigoPreferido) {
        if (codigoPreferido == null || codigoPreferido.isBlank()) {
            throw new IllegalArgumentException(
                    "Debe indicar la sala preferida.");
        }
        this.codigoPreferido = codigoPreferido;
    }

    @Override
    public Optional<Sala> seleccionar(
            List<Sala> disponibles, int cantidadPersonas) {

        return disponibles.stream()
                .filter(sala -> sala.getCodigo().equalsIgnoreCase(codigoPreferido))
                .filter(sala -> sala.getCapacidad() >= cantidadPersonas)
                .findFirst();
    }
}
