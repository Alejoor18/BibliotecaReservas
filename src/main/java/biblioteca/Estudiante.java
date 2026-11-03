package biblioteca;

public class Estudiante {

    private String identificador;
    private String nombre;

    public Estudiante(String identificador, String nombre) {
        this.identificador = identificador;
        this.nombre = nombre;
    }

    public String getIdentificador() {
        return identificador;
    }

    public String getNombre() {
        return nombre;
    }
}