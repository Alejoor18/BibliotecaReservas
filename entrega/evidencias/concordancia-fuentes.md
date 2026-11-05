# Concordancia de fuentes con la guía

Se inspeccionaron visualmente las quince capturas originales y el recorrido del video. Se contrastaron las firmas, datos, algoritmos, textos y orden del flujo de los veinte tipos auxiliares. El Main final se cotejó adicionalmente por sus 413 tokens contra una transcripción visual independiente; se ignoraron únicamente espacios y saltos de línea. No se exige igualdad de bytes ni formato. Esta revisión estática no sustituye los logs de compilación y pruebas.

El informe revision-guia.md conserva el detalle de lectura y del video. Los hashes de esta revisión están en concordancia-fuentes.json.

| Archivo | Captura de origen | Comprobación |
|---|---|---|
| Main.java | 11–12 | Concordante |
| Estudiante.java | 03 | Concordante |
| Sala.java | 03 | Concordante |
| Reserva.java | 04–05 y 09 | Concordante |
| ReservaBuilder.java | 05 | Concordante |
| EstrategiaSeleccionSala.java | 06 | Concordante |
| SeleccionPorCapacidad.java | 06 | Concordante |
| SeleccionSalaPreferida.java | 06 | Concordante |
| RepositorioSalas.java | 07 | Concordante |
| RepositorioReservas.java | 07 | Concordante |
| RepositorioSalasMemoria.java | 07 | Concordante |
| RepositorioReservasMemoria.java | 08 | Concordante |
| ReservaFacade.java | 08 y 10 | Concordante |
| ObservadorReserva.java | 09 | Concordante |
| NotificadorEstudiante.java | 09 | Concordante |
| RegistroEventos.java | 09 | Concordante |
| EstadoReserva.java | 10 | Concordante |
| Pendiente.java | 10 | Concordante |
| Confirmada.java | 10–11 | Concordante |
| Cancelada.java | 11 | Concordante |
| Finalizada.java | 11 | Concordante |

## Controles estáticos

- OK: 21 nombres de archivo exactos
- OK: Paquete biblioteca en todos los archivos
- OK: Main final igual a transcripción visual por tokens
- OK: Código UUID y ausencia de codigo manual
- OK: horaInicio y getNombreEstado
- OK: cambiarEstado interno y sin getter estado
- OK: Observer itera copia y métodos alta/baja
- OK: Texto literal Evento registrado
- OK: Ausencia de anotaciones ajenas a captura11

## Resultado de la revisión manual

Las salas son A/2, B/4, C/6 y D/8, y su representación coincide con la captura. Builder comprueba obligatorios, fecha pasada, valores no positivos y capacidad; genera R- y ocho caracteres UUID. Strategy conserva capacidad mínima y preferencia sin distinguir mayúsculas. Los repositorios y la fachada siguen sus contratos: consultar, seleccionar, construir, suscribir, guardar, confirmar y devolver. La falta de sala retorna vacío sin construir ni guardar. Observer conserva ambos mensajes exactos y notifica desde cambiarEstado. State mantiene las cuatro transiciones permitidas y los ocho mensajes de rechazo.

No se añadieron GUI, BD, persistencia, control de solapamientos, restricciones horarias ni operaciones ajenas a la guía. Las limitaciones de robustez propias del ejemplo (UUID truncado, confianza dentro del paquete y fallo de un observador) se documentan sin alterar el código académico.
