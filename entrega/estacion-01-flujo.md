# Flujo y responsabilidades

La solicitud contiene estudiante, fecha, hora, duración, personas y criterio.
La disponibilidad es una lista fija: no representa una agenda real.

```mermaid
flowchart TD
 A[Estudiante solicita reserva] --> B[Facade consulta salas]
 B --> C[Strategy selecciona por capacidad o preferencia]
 C --> D{¿Existe sala adecuada?}
 D -- No --> E[Optional vacío y mensaje sin crear reserva]
 D -- Sí --> F[Builder valida y construye Pendiente]
 F --> G[Facade suscribe observadores y registra]
 G --> H[State confirma]
 H --> I[Observer notifica al estudiante y registra evento]
 I --> J{Operación posterior}
 J -- Cancelar --> K[State valida y cancela]
 J -- Finalizar --> L[State valida y finaliza]
 K --> M[Notifica cambio válido]
 L --> M
 J -- No permitida --> N[Excepción sin cambio ni notificación]
```

Responsabilidades separadas: Main configura dependencias; Strategy selecciona;
Builder construye y valida; repositorios proporcionan salas y guardan reservas;
Facade coordina el caso de uso; State controla transiciones; Observer comunica
cambios. Una clase Main que hiciera todo tendría muchas razones para cambiar.

Las ocho ramas se crean en esta sesión por organización solicitada por el
estudiante. No se atribuye a la guía una obligación de usar ocho ramas.
