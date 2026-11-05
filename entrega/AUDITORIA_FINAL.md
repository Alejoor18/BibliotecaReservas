# Auditoría final estricta de BibliotecaReservas

Autor académico confirmado: Alejandro Ospina Rodríguez. Fecha: 5 de noviembre de 2026.

## Dictamen

**CUMPLE CON OBSERVACIONES.** El código de aplicación coincide con la guía en nombres, paquete, atributos/tipos, constructores, firmas, accesos, validaciones, mensajes, dependencias y comportamiento. La nueva ejecución aprueba 45/45 y Maven compila tras la corrección mínima del POM. Las ocho ramas tienen diffs reales, existen en remoto y son ancestros de master. Las observaciones documentales y límites probatorios se detallan al final: este dictamen no equivale a aprobar todas las capturas pendientes.

La comparación es manual contra las 15 imágenes, página por página, apoyada por firmas, fuentes numeradas y hashes; no es una prueba de igualdad OCR de todos los tokens. COINCIDE significa concordancia del código, ignorando espaciado y saltos de línea. Main conserva además los 413 tokens cotejados con la transcripción visual independiente.

## Comparación de los 21 archivos

Las páginas son nombres pagina_XX.png, no numeración editorial del PDF. Los rangos de líneas corresponden a los archivos locales completos. El cotejo comprende todos los criterios indicados, no solo existencia de clases. Ningún fuente Java fue modificado durante esta revisión; los 21 hashes coinciden con el registro tomado al comenzar.

| Archivo | Capturas | Líneas cotejadas | Resultado | Evidencia |
|---|---|---|---|---|
| Cancelada.java | 11 | 1–23 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#cancelada); SHA256 en concordancia21.json |
| Confirmada.java | 10-11 | 1–22 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#confirmada); SHA256 en concordancia21.json |
| EstadoReserva.java | 10 | 1–9 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#estadoreserva); SHA256 en concordancia21.json |
| EstrategiaSeleccionSala.java | 06 | 1–9 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#estrategiaseleccionsala); SHA256 en concordancia21.json |
| Estudiante.java | 03 | 1–25 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#estudiante); SHA256 en concordancia21.json |
| Finalizada.java | 11 | 1–23 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#finalizada); SHA256 en concordancia21.json |
| Main.java | 11-12 | 1–72 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#main); SHA256 en concordancia21.json |
| NotificadorEstudiante.java | 09 | 1–10 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#notificadorestudiante); SHA256 en concordancia21.json |
| ObservadorReserva.java | 09 | 1–4 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#observadorreserva); SHA256 en concordancia21.json |
| Pendiente.java | 10 | 1–22 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#pendiente); SHA256 en concordancia21.json |
| RegistroEventos.java | 09 | 1–8 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#registroeventos); SHA256 en concordancia21.json |
| RepositorioReservas.java | 07 | 1–4 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#repositorioreservas); SHA256 en concordancia21.json |
| RepositorioReservasMemoria.java | 08 | 1–14 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#repositorioreservasmemoria); SHA256 en concordancia21.json |
| RepositorioSalas.java | 07 | 1–5 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#repositoriosalas); SHA256 en concordancia21.json |
| RepositorioSalasMemoria.java | 07 | 1–12 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#repositoriosalasmemoria); SHA256 en concordancia21.json |
| Reserva.java | 04-05,09 | 1–67 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#reserva); SHA256 en concordancia21.json |
| ReservaBuilder.java | 05 | 1–49 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#reservabuilder); SHA256 en concordancia21.json |
| ReservaFacade.java | 08,10 | 1–38 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#reservafacade); SHA256 en concordancia21.json |
| Sala.java | 03 | 1–26 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#sala); SHA256 en concordancia21.json |
| SeleccionPorCapacidad.java | 06 | 1–18 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#seleccionporcapacidad); SHA256 en concordancia21.json |
| SeleccionSalaPreferida.java | 06 | 1–28 | COINCIDE | [Fuente numerada](evidencias/revision-final/fuentes-numeradas.md#seleccionsalapreferida); SHA256 en concordancia21.json |

## Git y GitHub

Origin y HEAD remoto verifican https://github.com/Alejoor18/BibliotecaReservas y master. Los comandos exigidos se ejecutaron de nuevo y están íntegros en evidencias/revision-final/git, incluidos fetch con prune, status, ramas, grafo, autores/fechas, remote y diff con origin/master.

| Rama | Commit | Cambio real de estación | Diff frente a etapa anterior | Integración y remoto |
|---|---|---|---|---|
| codex/estacion-01 | `4b8a602` | Flujo y comparación inicial; exclusión de entradas | 3 archivos; [diff](evidencias/revision-final/git/e1-diff.log) | merge-base=4b8a602; ancestro, código 0; remoto idéntico |
| codex/estacion-02 | `82036bc` | Sala validada y Main inicial A-D | 3 archivos; [diff](evidencias/revision-final/git/e2-diff.log) | merge-base=82036bc; ancestro, código 0; remoto idéntico |
| codex/estacion-03 | `c291577` | API/validaciones de Reserva y Builder | 4 archivos; [diff](evidencias/revision-final/git/e3-diff.log) | merge-base=c291577; ancestro, código 0; remoto idéntico |
| codex/estacion-04 | `8b92663` | Demostración real de las tres selecciones Strategy | 2 archivos; [diff](evidencias/revision-final/git/e4-diff.log) | merge-base=8b92663; ancestro, código 0; remoto idéntico |
| codex/estacion-05 | `8a88ed0` | Cuatro repositorios y Facade | 7 archivos; [diff](evidencias/revision-final/git/e5-diff.log) | merge-base=8a88ed0; ancestro, código 0; remoto idéntico |
| codex/estacion-06 | `b1ff249` | Observer y suscripción antes de confirmar | 7 archivos; [diff](evidencias/revision-final/git/e6-diff.log) | merge-base=b1ff249; ancestro, código 0; remoto idéntico |
| codex/estacion-07 | `e1765c5` | Arnés P01-P11 y matriz de State ya existente | 12 archivos; [diff](evidencias/revision-final/git/e7-diff.log) | merge-base=e1765c5; ancestro, código 0; remoto idéntico |
| codex/estacion-08 | `dd1322f` | Main final de los cuatro estudiantes y su ejecución | 2 archivos; [diff](evidencias/revision-final/git/e8-diff.log) | merge-base=dd1322f; ancestro, código 0; remoto idéntico |

Corte previo a esta corrección: `9fcecd5229f5913a087e5506d71109899fe00200`. master y origin/master estaban idénticos (divergencia 0/0). `git diff origin/master --` muestra exclusivamente la eliminación de la línea vacía del POM; los documentos nuevos aún sin seguimiento no aparecen en ese diff, pero sí en status. No se presenta ese estado de trabajo como limpio. Después del único commit final se vuelve a comprobar limpieza y sincronización; el comprobante posterior se incorpora al ZIP y se informa al cerrar la tarea, evitando una referencia circular al commit del propio informe.

Se examinaron 14 commits alcanzables con git show y diff-tree: ninguno tiene diff vacío. El original `5d8bbbef779e0215bd2339afb9d9378632ec1217` sigue siendo ancestro de master y su objeto no se alteró. Las ramas son puntos de control de un desarrollo lineal integrado por avance rápido, no ocho desarrollos paralelos independientes. Esto conserva todos los commits sin squash ni force push. La estación 7 añadió pruebas; las reglas State ya existían y no se atribuyen falsamente a ese commit.

Los autores y fechas se conservan tal como figuran en los objetos Git (autores.log y commit-*.log). La identidad Git AlejandrOspinaForja corresponde a la configuración preexistente, distinta del nombre académico de portada. Las fechas de la sesión cruzan del 4 al 5 de noviembre y las fechas ISO documentan la zona. Los diffs y la ascendencia demuestran cambios reales; Git por sí solo no puede probar la intención subjetiva del autor ni certificar su identidad civil. No se alteraron autores, fechas ni commits previos.

## Nueva ejecución funcional

La ejecución que sustenta este informe es `2026-11-05T07:00:26.291529600Z` UTC, Java `17.0.21.0.2`. Los logs anteriores se conservan como históricos y no se presentan como esta nueva corrida. El arnés y los fuentes se compilaron de nuevo.

| Grupo | Casos | Resultado |
|---|---:|---|
| Obligatorios P01–P11 | 11 | 11 PASS |
| Matriz de cuatro estados por tres operaciones | 12 | 12 PASS |
| Validaciones y verificaciones adicionales V01–V22 | 22 | 22 PASS |
| Total | 45 | 45 PASS, 0 FAIL |

Son **45 casos en total**, no 45 adicionales a los once obligatorios. Cada caso contiene varias aserciones. El proceso de compilación, pruebas y Main terminó con código 0 según validacion45/entorno-ejecucion.json. Main ejecutó selección B/C, cancelación válida, rechazo de reconfirmar, ausencia de sala para diez y finalización. Maven clean package produjo BUILD SUCCESS; maven-package.log conserva la salida nueva.

| Prueba | Resultado | Observación real |
|---|---|---|
| P01 | PASS | Construcción con todos los datos y código generado |
| P02 | PASS | Construcción sin estudiante rechazada con mensaje claro |
| P03 | PASS | Capacidad para cuatro personas selecciona Sala B |
| P04 | PASS | Preferida C para cuatro personas selecciona Sala C |
| P05 | PASS | Preferida B para siete personas no selecciona sala |
| P06 | PASS | La fachada registra y confirma la misma reserva |
| P07 | PASS | Confirmación notifica a los dos observadores reales |
| P08 | PASS | Cancelar una confirmada cambia el estado y notifica |
| P09 | PASS | Confirmar cancelada se rechaza sin nuevas notificaciones |
| P10 | PASS | Diez personas no crean ni registran reserva |
| P11 | PASS | Finalizar confirmada cambia el estado y notifica |

Las salidas completas por caso están en validacion45/resultados-pruebas.json y pruebas.log. P07 comprueba textos exactos y un evento en cada observador real. P09 registra dos eventos previos en cada observador y dos después del intento rechazado: diferencia cero. T01–T12 cubren todas las operaciones, comprobando estado y eventos, y V21 verifica ausencia de registro al fallar Builder. V17 y V18 comprueban vista inmodificable y copia estable de suscriptores.

## Diferencia comprobada y corrección mínima

`pom.xml`, línea 1: existía una línea vacía antes de `<?xml ...?>`, también presente en el commit auditado. Una nueva invocación de Maven produjo Non-parseable POM, processing instruction can not have PITarget with reserved xml name, línea 2. Se retiró exclusivamente ese salto inicial. No se cambiaron versiones, dependencias ni funcionalidades. Los logs históricos BUILD SUCCESS no bastaban para acreditar el estado actual; la compilación nueva posterior a esta corrección sí lo acredita. Los 21 fuentes y el arnés original siguen intactos.

## Documentación y límites de comprobación

Se cotejaron las dos vistas de clases (21 tipos), flujo, matriz, cinco patrones, SOLID, ocho antipatrones y respuestas 14–22. Describen la lista fija, persistencia solo en memoria y notificaciones en consola que realmente existen. No se añade agenda real, base de datos ni GUI a la aplicación. Los repositorios y observadores reciben dependencias por contrato; el acceso interno a cambiarEstado confía en las clases del paquete, como la guía. No se afirma aislamiento ante código malicioso dentro del paquete ni entrega externa de mensajes.

Por la nueva prioridad del usuario, **no se cambia la presentación del PDF** hasta cerrar esta auditoría. El PDF previo todavía requiere incorporar el nombre completo y completar las capturas visuales P01–P11 y de Git. Hay registros auténticos de ejecución y Git, pero no se afirma disponer de las trece capturas gráficas solicitadas. El auxiliar provisional de captura no se incluye como cambio de aplicación ni sustituye las pruebas originales. El video se había inspeccionado en la fase previa; en esta revisión se releen las 15 imágenes y no se afirma haber reproducido otra vez el video.

Estas observaciones impiden marcar CUMPLE sin reservas para la entrega académica completa, aunque el código y las ocho ramas superan la auditoría técnica. No se ha inferido una exigencia docente de ocho nombres de rama: su organización responde a la solicitud del estudiante.

## Detalle independiente de la revisión visual, patrones y estaciones

# Auditoría final de concordancia con la guía

Se revisaron visualmente las quince capturas originales y se leyeron los 21 archivos Java actuales. No se encontró una diferencia funcional, de API, visibilidad o mensaje que justifique cambiar el código de aplicación. El Main final conserva los 413 tokens de la transcripción visual independiente, ignorando únicamente espacios y saltos de línea.

Esta auditoría es de solo lectura. No reescribe código ni historial y no presenta los registros anteriores como una nueva ejecución. El video ya se había inspeccionado en la revisión previa documentada en revision-guia.md; no se volvió a reproducir en esta auditoría.

## Archivos cotejados

| Archivo | Captura de origen | Resultado |
|---|---|---|
| Main.java | 11-12 | Concordante |
| Estudiante.java | 03 | Concordante |
| Sala.java | 03 | Concordante |
| Reserva.java | 04-05 y 09 | Concordante |
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
| Confirmada.java | 10-11 | Concordante |
| Cancelada.java | 11 | Concordante |
| Finalizada.java | 11 | Concordante |

El cotejo manual de los veinte tipos auxiliares incluyó campos, constructores, métodos, algoritmos, mensajes y orden de coordinación. No se afirma igualdad de bytes ni formato tipográfico con las capturas. Los hashes SHA256 del código revisado acompañan este informe en auditoria-final.json.

## Cinco patrones

| Patrón | Realización comprobada | Pruebas relacionadas |
|---|---|---|
| Builder | ReservaBuilder valida obligatorios, fecha, duración, personas y capacidad; genera R- más ocho caracteres UUID y crea Reserva Pendiente. | P01-P02, V01-V11 |
| Strategy | EstrategiaSeleccionSala y las dos implementaciones mantienen selección mínima suficiente o preferencia por código sin distinguir mayúsculas. | P03-P05, P10, V15-V16 |
| Facade | Consulta, selecciona, construye, suscribe, guarda, confirma y retorna; Optional vacío evita registro cuando no hay sala. | P06, P10, V21 |
| Observer | Reserva depende del contrato, permite alta y baja, recorre copia de la lista y avisa a NotificadorEstudiante y RegistroEventos desde cambiarEstado. | P07-P09, P11, V18 |
| State | Pendiente, Confirmada, Cancelada y Finalizada aplican exactamente las cuatro transiciones permitidas y los ocho rechazos de la guía. | P08-P09, P11, T01-T12 |

## Ocho estaciones y trazabilidad

| Estación | Evidencia actual o histórica comprobada |
|---|---|
| 1 Flujo | entrega/estacion-01-flujo.md y diagrama final; commit 4b8a602. |
| 2 Dominio | Estudiante y Sala; Main inicial y salida A-D conservados en 82036bc y estacion-02.log. |
| 3 Builder | Reserva y ReservaBuilder; c291577 y evidencia de etapa. |
| 4 Strategy | Tres tipos y las pruebas de capacidad/preferencia; 8b92663. |
| 5 Repositorios y Facade | Cuatro tipos de repositorio y fachada; 8a88ed0. |
| 6 Observer | Tres tipos y ampliaciones de Reserva y Facade; b1ff249. |
| 7 State | Cinco tipos presentes; reglas ya implementadas y matriz nativa incorporada en e1765c5, sin simular una implementación nueva. |
| 8 Integración | Main final de Laura, Andrés, Camila y Samuel; dd1322f. |

Las ocho ramas son una organización solicitada por el estudiante. La guía y el video previamente revisado no acreditan que el profesor exigiera ocho ramas con nombres concretos.

## Diagramas

Las dos vistas de clases reúnen exactamente los 21 tipos, sin clases inventadas. Se comprobaron relaciones de repositorios, construcción, estrategias, estado y observación. El flujo coincide con la secuencia de Facade y diferencia ausencia de sala y rechazo sin evento. Las fuentes Mermaid y sus imágenes reflejan el alcance simulado; esta auditoría coteja su contenido, no ejecuta un nuevo renderizador Mermaid.

## Matriz P01 a P11

| ID | Requisito de guía y aserción inspeccionada |
|---|---|
| P01 | Reserva válida y Pendiente con los datos conservados y código R-XXXXXXXX. |
| P02 | Falta estudiante: IllegalStateException con mensaje exacto. |
| P03 | Cuatro personas por capacidad: B. |
| P04 | Preferida C para cuatro: C. |
| P05 | Preferida B para siete: vacío. |
| P06 | Se guarda y devuelve la misma reserva Confirmada. |
| P07 | Los dos observadores reales reciben Pendiente a Confirmada y producen sus textos exactos. |
| P08 | Confirmada a Cancelada: un evento nuevo por observador. |
| P09 | Confirmar Cancelada: excepción, estado intacto y diferencia de eventos cero. |
| P10 | Diez personas: sin reserva, registro ni eventos. |
| P11 | Confirmada a Finalizada: un evento nuevo por observador. |

Los registros previos inspeccionados corresponden a 2026-11-05T04:38:06.649138700Z: 45 casos aprobados y cero fallidos. La revisión final debe ejecutar nuevamente Maven y el arnés, como ha solicitado el estudiante.

## Resultado y correcciones documentales necesarias

No se recomienda cambiar ninguno de los 21 fuentes Java: las limitaciones de lista fija, ausencia de persistencia y solapamientos, UUID truncado y confianza dentro del paquete pertenecen al ejemplo académico. Las modificaciones pendientes de esta entrega se concentran en la portada con el nombre confirmado Alejandro Ospina Rodríguez, capturas auténticas y legibles P01-P11, comparación visual P07/P09, evidencias reales de ramas e historial y regeneración del PDF y ZIP. No deben inventarse docente, universidad, capturas de IntelliJ ni commits.
