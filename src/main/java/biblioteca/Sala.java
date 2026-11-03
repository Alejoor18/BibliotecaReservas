
package biblioteca;

public class Sala {

    private String codigo;
    private String nombre;
    private int capacidad;

    public Sala(String codigo, String nombre, int capacidad) {
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

    @Override
    public String toString() {
        return nombre + " (" + codigo +
                ") - Capacidad: " + capacidad;
    }
}
