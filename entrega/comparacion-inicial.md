# Comparación del punto de partida con la guía

| Exigido | Existente | Diferencia | Corrección por estación |
|---|---|---|---|
| 21 archivos en biblioteca | 13 archivos | Faltan 8 | E5 repositorios y Facade; E6 Observer |
| Sala válida y legible | Valida solo código y nombre | Capacidad no validada, sin toString | E2 |
| Builder con UUID y horaInicio | Código manual y horarioInicio | Sin validación de fecha pasada | E3 |
| Reserva getNombreEstado y cambio interno | getEstado y setter público | API distinta y transición eludible | E3, E6 |
| Dos estrategias | Ya implementadas | Falta evidencia reproducible | E4 |
| Repositorios y Facade | Ausentes | No registra ni confirma un flujo | E5 |
| Observer | Ausente | Sin notificaciones | E6 |
| Cuatro estados | Ya implementados | Falta matriz ejecutada completa | E7 |
| Main final Laura, Andrés, Camila, Samuel | Demostración directa de Alejandro | No integra patrones | E8 |
| Pruebas P01-P11 y PDF | Sin pruebas; borrador incompleto | Entrega pendiente | E7, E8 y documentación final |
| Java 17 | POM correcto; terminal usa Java 8 | PATH y JAVA_HOME no coinciden | Scripts con JDK explícito |

El punto de partida y su índice Git se copiaron completos fuera del repositorio.
El commit original se conserva; el avance sin confirmar se guardó como un
checkpoint auténtico antes de corregirlo. Los recursos de entrada se conservan
localmente, ignorados por Git y excluidos de la distribución final.
