
package biblioteca;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

public class SeleccionPorCapacidad implements EstrategiaSeleccionSala {

    @Override
    public Optional<Sala> seleccionar(
            List<Sala> disponibles, int cantidadPersonas) {

        return disponibles.stream()
                .filter(sala -> sala.getCapacidad() >= cantidadPersonas)
                .min(Comparator.comparingInt(Sala::getCapacidad));
    }
}
