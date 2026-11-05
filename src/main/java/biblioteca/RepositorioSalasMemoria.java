package biblioteca;
import java.util.List;
public class RepositorioSalasMemoria implements RepositorioSalas {
    private final List<Sala> salas = List.of(
        new Sala("A", "Sala A", 2), new Sala("B", "Sala B", 4),
        new Sala("C", "Sala C", 6), new Sala("D", "Sala D", 8)
    );
    @Override
    public List<Sala> obtenerDisponibles() {
        return salas;
    }
}
