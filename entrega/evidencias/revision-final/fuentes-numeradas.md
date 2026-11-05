## Cancelada

```java
  1: package biblioteca;
  2: 
  3: public class Cancelada implements EstadoReserva {
  4: 
  5:     public String nombre() {
  6:         return "Cancelada";
  7:     }
  8: 
  9:     public void confirmar(Reserva reserva) {
 10:         throw new IllegalStateException(
 11:                 "No se puede confirmar una reserva cancelada.");
 12:     }
 13: 
 14:     public void cancelar(Reserva reserva) {
 15:         throw new IllegalStateException(
 16:                 "La reserva ya está cancelada.");
 17:     }
 18: 
 19:     public void finalizar(Reserva reserva) {
 20:         throw new IllegalStateException(
 21:                 "No se puede finalizar una reserva cancelada.");
 22:     }
 23: }
```

## Confirmada

```java
  1: 
  2: package biblioteca;
  3: 
  4: public class Confirmada implements EstadoReserva {
  5: 
  6:     public String nombre() {
  7:         return "Confirmada";
  8:     }
  9: 
 10:     public void confirmar(Reserva reserva) {
 11:         throw new IllegalStateException(
 12:                 "La reserva ya está confirmada.");
 13:     }
 14: 
 15:     public void cancelar(Reserva reserva) {
 16:         reserva.cambiarEstado(new Cancelada());
 17:     }
 18: 
 19:     public void finalizar(Reserva reserva) {
 20:         reserva.cambiarEstado(new Finalizada());
 21:     }
 22: }
```

## EstadoReserva

```java
  1: 
  2: package biblioteca;
  3: 
  4: public interface EstadoReserva {
  5:     String nombre();
  6:     void confirmar(Reserva reserva);
  7:     void cancelar(Reserva reserva);
  8:     void finalizar(Reserva reserva);
  9: }
```

## EstrategiaSeleccionSala

```java
  1: 
  2: package biblioteca;
  3: 
  4: import java.util.List;
  5: import java.util.Optional;
  6: 
  7: public interface EstrategiaSeleccionSala {
  8:     Optional<Sala> seleccionar(List<Sala> disponibles, int cantidadPersonas);
  9: }
```

## Estudiante

```java
  1: 
  2: package biblioteca;
  3: 
  4: public class Estudiante {
  5:     private final String identificador;
  6:     private final String nombre;
  7: 
  8:     public Estudiante(String identificador, String nombre) {
  9:         if (identificador == null || identificador.isBlank()
 10:                 || nombre == null || nombre.isBlank()) {
 11:             throw new IllegalArgumentException(
 12:                     "Identificador y nombre son obligatorios.");
 13:         }
 14:         this.identificador = identificador;
 15:         this.nombre = nombre;
 16:     }
 17: 
 18:     public String getIdentificador() {
 19:         return identificador;
 20:     }
 21: 
 22:     public String getNombre() {
 23:         return nombre;
 24:     }
 25: }
```

## Finalizada

```java
  1: package biblioteca;
  2: 
  3: public class Finalizada implements EstadoReserva {
  4: 
  5:     public String nombre() {
  6:         return "Finalizada";
  7:     }
  8: 
  9:     public void confirmar(Reserva reserva) {
 10:         throw new IllegalStateException(
 11:                 "No se puede confirmar una reserva finalizada.");
 12:     }
 13: 
 14:     public void cancelar(Reserva reserva) {
 15:         throw new IllegalStateException(
 16:                 "No se puede cancelar una reserva finalizada.");
 17:     }
 18: 
 19:     public void finalizar(Reserva reserva) {
 20:         throw new IllegalStateException(
 21:                 "La reserva ya está finalizada.");
 22:     }
 23: }
```

## Main

```java
  1: package biblioteca;
  2: 
  3: import java.time.LocalDate;
  4: import java.time.LocalTime;
  5: import java.util.List;
  6: 
  7: public class Main {
  8:     public static void main(String[] args) {
  9:         RepositorioSalas salas = new RepositorioSalasMemoria();
 10:         RepositorioReservasMemoria reservas = new RepositorioReservasMemoria();
 11:         List<ObservadorReserva> observadores = List.of(
 12:             new NotificadorEstudiante(),
 13:             new RegistroEventos()
 14:         );
 15:         ReservaFacade fachada = new ReservaFacade(salas, reservas, observadores);
 16:         Estudiante laura = new Estudiante("E001", "Laura");
 17: 
 18:         System.out.println("--- ESCENARIO PRINCIPAL ---");
 19:         Reserva reserva = fachada.realizarReserva(
 20:             laura,
 21:             LocalDate.now().plusDays(7),
 22:             LocalTime.of(14, 0),
 23:             2,
 24:             4,
 25:             new SeleccionPorCapacidad()
 26:         ).orElseThrow();
 27:         System.out.println(reserva);
 28: 
 29:         System.out.println("\nLaura cancela la reserva:");
 30:         reserva.cancelar();
 31:         System.out.println(reserva);
 32: 
 33:         System.out.println("\nIntento inválido: confirmar una reserva cancelada:");
 34:         try {
 35:             reserva.confirmar();
 36:         } catch (IllegalStateException ex) {
 37:             System.out.println("Operación rechazada: " + ex.getMessage());
 38:         }
 39: 
 40:         System.out.println("\n--- PRUEBA DE SALA PREFERIDA ---");
 41:         fachada.realizarReserva(
 42:             new Estudiante("E002", "Andrés"),
 43:             LocalDate.now().plusDays(8),
 44:             LocalTime.of(10, 0),
 45:             2,
 46:             4,
 47:             new SeleccionSalaPreferida("C")
 48:         ).ifPresent(System.out::println);
 49: 
 50:         System.out.println("\n--- PRUEBA SIN SALA ADECUADA ---");
 51:         fachada.realizarReserva(
 52:             new Estudiante("E003", "Camila"),
 53:             LocalDate.now().plusDays(9),
 54:             LocalTime.of(9, 0),
 55:             2,
 56:             10,
 57:             new SeleccionPorCapacidad()
 58:         );
 59: 
 60:         System.out.println("\n--- PRUEBA DE FINALIZACIÓN ---");
 61:         Reserva otra = fachada.realizarReserva(
 62:             new Estudiante("E004", "Samuel"),
 63:             LocalDate.now().plusDays(10),
 64:             LocalTime.of(11, 0),
 65:             1,
 66:             2,
 67:             new SeleccionPorCapacidad()
 68:         ).orElseThrow();
 69:         otra.finalizar();
 70:         System.out.println(otra);
 71:     }
 72: }
```

## NotificadorEstudiante

```java
  1: package biblioteca;
  2: public class NotificadorEstudiante implements ObservadorReserva {
  3:     @Override
  4:     public void actualizar(Reserva reserva, String anterior, String nuevo) {
  5:         System.out.println("Notificación a "
  6:             + reserva.getEstudiante().getNombre()
  7:             + ": su reserva " + reserva.getCodigo()
  8:             + " cambió de " + anterior + " a " + nuevo + ".");
  9:     }
 10: }
```

## ObservadorReserva

```java
  1: package biblioteca;
  2: public interface ObservadorReserva {
  3:     void actualizar(Reserva reserva, String estadoAnterior, String estadoNuevo);
  4: }
```

## Pendiente

```java
  1: 
  2: package biblioteca;
  3: 
  4: public class Pendiente implements EstadoReserva {
  5: 
  6:     public String nombre() {
  7:         return "Pendiente";
  8:     }
  9: 
 10:     public void confirmar(Reserva reserva) {
 11:         reserva.cambiarEstado(new Confirmada());
 12:     }
 13: 
 14:     public void cancelar(Reserva reserva) {
 15:         reserva.cambiarEstado(new Cancelada());
 16:     }
 17: 
 18:     public void finalizar(Reserva reserva) {
 19:         throw new IllegalStateException(
 20:                 "No se puede finalizar una reserva pendiente.");
 21:     }
 22: }
```

## RegistroEventos

```java
  1: package biblioteca;
  2: public class RegistroEventos implements ObservadorReserva {
  3:     @Override
  4:     public void actualizar(Reserva reserva, String anterior, String nuevo) {
  5:         System.out.println("Evento registrado: " + reserva.getCodigo()
  6:             + " cambió de " + anterior + " a " + nuevo + ".");
  7:     }
  8: }
```

## RepositorioReservas

```java
  1: package biblioteca;
  2: public interface RepositorioReservas {
  3:     void guardar(Reserva reserva);
  4: }
```

## RepositorioReservasMemoria

```java
  1: package biblioteca;
  2: import java.util.ArrayList;
  3: import java.util.Collections;
  4: import java.util.List;
  5: public class RepositorioReservasMemoria implements RepositorioReservas {
  6:     private final List<Reserva> reservas = new ArrayList<>();
  7:     @Override
  8:     public void guardar(Reserva reserva) {
  9:         reservas.add(reserva);
 10:     }
 11:     public List<Reserva> obtenerTodas() {
 12:         return Collections.unmodifiableList(reservas);
 13:     }
 14: }
```

## RepositorioSalas

```java
  1: package biblioteca;
  2: import java.util.List;
  3: public interface RepositorioSalas {
  4:     List<Sala> obtenerDisponibles();
  5: }
```

## RepositorioSalasMemoria

```java
  1: package biblioteca;
  2: import java.util.List;
  3: public class RepositorioSalasMemoria implements RepositorioSalas {
  4:     private final List<Sala> salas = List.of(
  5:         new Sala("A", "Sala A", 2), new Sala("B", "Sala B", 4),
  6:         new Sala("C", "Sala C", 6), new Sala("D", "Sala D", 8)
  7:     );
  8:     @Override
  9:     public List<Sala> obtenerDisponibles() {
 10:         return salas;
 11:     }
 12: }
```

## Reserva

```java
  1: package biblioteca;
  2: 
  3: import java.time.LocalDate;
  4: import java.time.LocalTime;
  5: import java.util.ArrayList;
  6: import java.util.List;
  7: 
  8: public class Reserva {
  9:     private final String codigo;
 10:     private final Estudiante estudiante;
 11:     private final LocalDate fecha;
 12:     private final LocalTime horaInicio;
 13:     private final int duracionHoras;
 14:     private final int cantidadPersonas;
 15:     private final Sala sala;
 16:     private EstadoReserva estado;
 17:     private final List<ObservadorReserva> observadores = new ArrayList<>();
 18: 
 19:     Reserva(String codigo, Estudiante estudiante, LocalDate fecha,
 20:             LocalTime horaInicio, int duracionHoras, int cantidadPersonas, Sala sala) {
 21:         this.codigo = codigo;
 22:         this.estudiante = estudiante;
 23:         this.fecha = fecha;
 24:         this.horaInicio = horaInicio;
 25:         this.duracionHoras = duracionHoras;
 26:         this.cantidadPersonas = cantidadPersonas;
 27:         this.sala = sala;
 28:         this.estado = new Pendiente();
 29:     }
 30: 
 31:     public String getCodigo() { return codigo; }
 32:     public Estudiante getEstudiante() { return estudiante; }
 33:     public LocalDate getFecha() { return fecha; }
 34:     public LocalTime getHoraInicio() { return horaInicio; }
 35:     public int getDuracionHoras() { return duracionHoras; }
 36:     public int getCantidadPersonas() { return cantidadPersonas; }
 37:     public Sala getSala() { return sala; }
 38:     public String getNombreEstado() { return estado.nombre(); }
 39: 
 40:     public void confirmar() { estado.confirmar(this); }
 41:     public void cancelar() { estado.cancelar(this); }
 42:     public void finalizar() { estado.finalizar(this); }
 43: 
 44:     public void agregarObservador(ObservadorReserva observador) {
 45:         if (observador != null) observadores.add(observador);
 46:     }
 47: 
 48:     public void retirarObservador(ObservadorReserva observador) {
 49:         observadores.remove(observador);
 50:     }
 51: 
 52:     void cambiarEstado(EstadoReserva nuevoEstado) {
 53:         String anterior = estado.nombre();
 54:         this.estado = nuevoEstado;
 55:         String actual = estado.nombre();
 56:         for (ObservadorReserva observador : List.copyOf(observadores)) {
 57:             observador.actualizar(this, anterior, actual);
 58:         }
 59:     }
 60: 
 61:     @Override
 62:     public String toString() {
 63:         return "Reserva " + codigo + " | " + estudiante.getNombre()
 64:                 + " | " + fecha + " " + horaInicio + " | " + sala
 65:                 + " | Estado: " + getNombreEstado();
 66:     }
 67: }
```

## ReservaBuilder

```java
  1: package biblioteca;
  2: 
  3: import java.time.LocalDate;
  4: import java.time.LocalTime;
  5: import java.util.UUID;
  6: 
  7: public class ReservaBuilder {
  8:     private Estudiante estudiante;
  9:     private LocalDate fecha;
 10:     private LocalTime horaInicio;
 11:     private int duracionHoras;
 12:     private int cantidadPersonas;
 13:     private Sala sala;
 14: 
 15:     public ReservaBuilder estudiante(Estudiante valor) {
 16:         this.estudiante = valor; return this;
 17:     }
 18:     public ReservaBuilder fecha(LocalDate valor) {
 19:         this.fecha = valor; return this;
 20:     }
 21:     public ReservaBuilder horaInicio(LocalTime valor) {
 22:         this.horaInicio = valor; return this;
 23:     }
 24:     public ReservaBuilder duracionHoras(int valor) {
 25:         this.duracionHoras = valor; return this;
 26:     }
 27:     public ReservaBuilder cantidadPersonas(int valor) {
 28:         this.cantidadPersonas = valor; return this;
 29:     }
 30:     public ReservaBuilder sala(Sala valor) {
 31:         this.sala = valor; return this;
 32:     }
 33: 
 34:     public Reserva build() {
 35:         if (estudiante == null || fecha == null || horaInicio == null || sala == null) {
 36:             throw new IllegalStateException("Faltan datos obligatorios de la reserva.");
 37:         }
 38:         if (fecha.isBefore(LocalDate.now()) || duracionHoras <= 0
 39:                 || cantidadPersonas <= 0) {
 40:             throw new IllegalStateException("Fecha, duración o cantidad de personas inválida.");
 41:         }
 42:         if (sala.getCapacidad() < cantidadPersonas) {
 43:             throw new IllegalStateException("La sala no tiene capacidad suficiente.");
 44:         }
 45:         String codigo = "R-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
 46:         return new Reserva(codigo, estudiante, fecha, horaInicio,
 47:                 duracionHoras, cantidadPersonas, sala);
 48:     }
 49: }
```

## ReservaFacade

```java
  1: package biblioteca;
  2: import java.time.LocalDate;
  3: import java.time.LocalTime;
  4: import java.util.Optional;
  5: public class ReservaFacade {
  6:     private final RepositorioSalas repositorioSalas;
  7:     private final RepositorioReservas repositorioReservas;
  8:     private final java.util.List<ObservadorReserva> observadores;
  9:     public ReservaFacade(RepositorioSalas repositorioSalas,
 10:                          RepositorioReservas repositorioReservas,
 11:                          java.util.List<ObservadorReserva> observadores) {
 12:         this.repositorioSalas = repositorioSalas;
 13:         this.repositorioReservas = repositorioReservas;
 14:         this.observadores = java.util.List.copyOf(observadores);
 15:     }
 16:     public Optional<Reserva> realizarReserva(
 17:             Estudiante estudiante, LocalDate fecha, LocalTime hora,
 18:             int duracion, int personas, EstrategiaSeleccionSala estrategia) {
 19:         var disponibles = repositorioSalas.obtenerDisponibles();
 20:         Optional<Sala> sala = estrategia.seleccionar(disponibles, personas);
 21:         if (sala.isEmpty()) {
 22:             System.out.println("No hay una sala disponible que cumpla la solicitud.");
 23:             return Optional.empty();
 24:         }
 25:         Reserva reserva = new ReservaBuilder()
 26:             .estudiante(estudiante)
 27:             .fecha(fecha)
 28:             .horaInicio(hora)
 29:             .duracionHoras(duracion)
 30:             .cantidadPersonas(personas)
 31:             .sala(sala.get())
 32:             .build();
 33:         observadores.forEach(reserva::agregarObservador);
 34:         repositorioReservas.guardar(reserva);
 35:         reserva.confirmar();
 36:         return Optional.of(reserva);
 37:     }
 38: }
```

## Sala

```java
  1: package biblioteca;
  2: 
  3: public class Sala {
  4:     private final String codigo;
  5:     private final String nombre;
  6:     private final int capacidad;
  7: 
  8:     public Sala(String codigo, String nombre, int capacidad) {
  9:         if (codigo == null || codigo.isBlank() || nombre == null || nombre.isBlank()
 10:                 || capacidad <= 0) {
 11:             throw new IllegalArgumentException("Datos de sala inválidos.");
 12:         }
 13:         this.codigo = codigo;
 14:         this.nombre = nombre;
 15:         this.capacidad = capacidad;
 16:     }
 17: 
 18:     public String getCodigo() { return codigo; }
 19:     public String getNombre() { return nombre; }
 20:     public int getCapacidad() { return capacidad; }
 21: 
 22:     @Override
 23:     public String toString() {
 24:         return nombre + " (" + codigo + ", capacidad: " + capacidad + ")";
 25:     }
 26: }
```

## SeleccionPorCapacidad

```java
  1: 
  2: package biblioteca;
  3: 
  4: import java.util.Comparator;
  5: import java.util.List;
  6: import java.util.Optional;
  7: 
  8: public class SeleccionPorCapacidad implements EstrategiaSeleccionSala {
  9: 
 10:     @Override
 11:     public Optional<Sala> seleccionar(
 12:             List<Sala> disponibles, int cantidadPersonas) {
 13: 
 14:         return disponibles.stream()
 15:                 .filter(sala -> sala.getCapacidad() >= cantidadPersonas)
 16:                 .min(Comparator.comparingInt(Sala::getCapacidad));
 17:     }
 18: }
```

## SeleccionSalaPreferida

```java
  1: 
  2: package biblioteca;
  3: 
  4: import java.util.List;
  5: import java.util.Optional;
  6: 
  7: public class SeleccionSalaPreferida implements EstrategiaSeleccionSala {
  8: 
  9:     private final String codigoPreferido;
 10: 
 11:     public SeleccionSalaPreferida(String codigoPreferido) {
 12:         if (codigoPreferido == null || codigoPreferido.isBlank()) {
 13:             throw new IllegalArgumentException(
 14:                     "Debe indicar la sala preferida.");
 15:         }
 16:         this.codigoPreferido = codigoPreferido;
 17:     }
 18: 
 19:     @Override
 20:     public Optional<Sala> seleccionar(
 21:             List<Sala> disponibles, int cantidadPersonas) {
 22: 
 23:         return disponibles.stream()
 24:                 .filter(sala -> sala.getCodigo().equalsIgnoreCase(codigoPreferido))
 25:                 .filter(sala -> sala.getCapacidad() >= cantidadPersonas)
 26:                 .findFirst();
 27:     }
 28: }
```
