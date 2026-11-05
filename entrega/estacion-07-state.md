# Verificación del ciclo de vida

Las cuatro clases de estado existentes ya coincidían con las reglas y mensajes
de la guía. No se reescribieron para aparentar una implementación nueva.
El trabajo de esta estación incorpora las pruebas P01-P11, las doce
combinaciones de estado y operación y negativas adicionales.

| Estado | confirmar | cancelar | finalizar |
|---|---|---|---|
| Pendiente | Confirmada | Cancelada | Rechazo |
| Confirmada | Rechazo | Cancelada | Finalizada |
| Cancelada | Rechazo | Rechazo | Rechazo |
| Finalizada | Rechazo | Rechazo | Rechazo |

Las transiciones rechazadas deben conservar el estado y el número de eventos.
CambiarEstado permanece interno al paquete para ajustarse a la guía.
