
package biblioteca;

public class Sala {
    private final String codigo;
    private final String nombre;
    private final int capacidad;

    public Sala(String codigo, String nombre, int capacidad) {
        if (codigo == null || codigo.isBlank()
                || nombre == null || nombre.isBlank()) {
            throw new IllegalArgumentException(
                    "Los identificadores de sala son inválidos.");
        }
        this.codigo = codigo;
        this.nombre = nombre;
        this.capacidad = capacidad;
    }

    public String getCodigo() {
        return codigo;
    }

    public String getNombre() {
        return nombre;
    }

    public int getCapacidad() {
        return capacidad;
    }
}
