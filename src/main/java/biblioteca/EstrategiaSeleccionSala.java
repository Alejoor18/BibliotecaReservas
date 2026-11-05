
package biblioteca;

import java.util.List;
import java.util.Optional;

public interface EstrategiaSeleccionSala {
    Optional<Sala> seleccionar(List<Sala> disponibles, int cantidadPersonas);
}
