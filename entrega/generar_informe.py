"""Genera el informe académico a partir del código y evidencias locales reales.

Dependencias de autoría: ReportLab y Pillow del runtime de Codex.
El proyecto Java y su verificación no dependen de estas bibliotecas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from html import escape
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether

BASE = Path(__file__).resolve().parent
FONT = Path('C:/Windows/Fonts/arial.ttf')
BOLD = Path('C:/Windows/Fonts/arialbd.ttf')
MONO = Path('C:/Windows/Fonts/consola.ttf')

FLOW = '''flowchart TD
  S([Inicio]) --> D[Estudiante registra solicitud]
  D --> F[ReservaFacade consulta RepositorioSalas]
  F --> E[Strategy busca una sala suficiente]
  E --> Q{¿Hay sala adecuada?}
  Q -- No --> N[Devuelve Optional.empty sin guardar ni confirmar]
  Q -- Sí --> B[Builder valida datos y crea Reserva Pendiente]
  B --> O[Facade registra observadores]
  O --> G[RepositorioReservas guarda la reserva]
  G --> C[Facade solicita confirmar]
  C --> ST[State acepta Pendiente a Confirmada]
  ST --> NT[Observer notifica estudiante y registro]
  NT --> A{Operación posterior}
  A -- Cancelar --> CA[State pasa a Cancelada y notifica]
  A -- Finalizar --> FI[State pasa a Finalizada y notifica]
  A -- Inválida --> RE[IllegalStateException sin evento]
  N --> Z([Fin])
  CA --> Z
  FI --> Z
  RE --> Z
'''

UML1 = '''classDiagram
  class Main { +main(String[] args) void }
  class ReservaFacade { -RepositorioSalas repositorioSalas\n-RepositorioReservas repositorioReservas\n-List~ObservadorReserva~ observadores\n+realizarReserva(...) Optional~Reserva~ }
  class RepositorioSalas { <<interface>>\n+obtenerDisponibles() List~Sala~ }
  class RepositorioReservas { <<interface>>\n+guardar(Reserva) void }
  class RepositorioSalasMemoria { -List~Sala~ salas\n+obtenerDisponibles() List~Sala~ }
  class RepositorioReservasMemoria { -List~Reserva~ reservas\n+guardar(Reserva) void\n+obtenerTodas() List~Reserva~ }
  class EstrategiaSeleccionSala { <<interface>>\n+seleccionar(List~Sala~, int) Optional~Sala~ }
  class SeleccionPorCapacidad { +seleccionar(List~Sala~, int) Optional~Sala~ }
  class SeleccionSalaPreferida { -String codigoPreferido\n+seleccionar(List~Sala~, int) Optional~Sala~ }
  class ReservaBuilder { -Estudiante estudiante\n-LocalDate fecha\n-LocalTime horaInicio\n-int duracionHoras\n-int cantidadPersonas\n-Sala sala\n+build() Reserva }
  class Reserva { -String codigo\n-LocalDate fecha\n-LocalTime horaInicio\n-int duracionHoras\n-int cantidadPersonas\n+getNombreEstado() String }
  class Estudiante { -String identificador\n-String nombre }
  class Sala { -String codigo\n-String nombre\n-int capacidad }
  Main --> ReservaFacade : configura y usa
  ReservaFacade --> RepositorioSalas : consulta
  ReservaFacade --> RepositorioReservas : guarda
  RepositorioSalasMemoria ..|> RepositorioSalas
  RepositorioReservasMemoria ..|> RepositorioReservas
  RepositorioSalasMemoria o-- Sala
  RepositorioReservasMemoria o-- Reserva
  ReservaFacade ..> EstrategiaSeleccionSala : recibe en cada solicitud
  SeleccionPorCapacidad ..|> EstrategiaSeleccionSala
  SeleccionSalaPreferida ..|> EstrategiaSeleccionSala
  ReservaFacade ..> ReservaBuilder : usa
  ReservaBuilder ..> Reserva : crea
  Reserva --> Estudiante : estudiante
  Reserva --> Sala : sala
'''

UML2 = '''classDiagram
  class Reserva { -EstadoReserva estado\n-List~ObservadorReserva~ observadores\n+confirmar() void\n+cancelar() void\n+finalizar() void\n+agregarObservador(ObservadorReserva) void\n+retirarObservador(ObservadorReserva) void\n~cambiarEstado(EstadoReserva) void }
  class EstadoReserva { <<interface>>\n+nombre() String\n+confirmar(Reserva) void\n+cancelar(Reserva) void\n+finalizar(Reserva) void }
  class Pendiente
  class Confirmada
  class Cancelada
  class Finalizada
  class ObservadorReserva { <<interface>>\n+actualizar(Reserva, String, String) void }
  class NotificadorEstudiante { +actualizar(Reserva, String, String) void }
  class RegistroEventos { +actualizar(Reserva, String, String) void }
  Reserva --> EstadoReserva : delega
  Pendiente ..|> EstadoReserva
  Confirmada ..|> EstadoReserva
  Cancelada ..|> EstadoReserva
  Finalizada ..|> EstadoReserva
  Reserva o-- ObservadorReserva : suscriptores
  NotificadorEstudiante ..|> ObservadorReserva
  RegistroEventos ..|> ObservadorReserva
  EstadoReserva ..> Reserva : cambia estado válido
'''

def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def diagram(path, kind):
    """Diagramas originales de código, con texto a resolución de impresión."""
    scale = 3
    w, h = (1000, 1140) if kind == 'flujo' else (1100, 820)
    offset_y=40 if kind=='flujo' else 0
    im = PILImage.new('RGB', (w*scale,h*scale),'white')
    draw = ImageDraw.Draw(im)
    def line(points, dash=False):
        pts=[(int(x*scale),int((y+offset_y)*scale)) for x,y in points]
        draw.line(pts,fill='#566370',width=2*scale)
    def arrow(points, label='', dashed=False):
        line(points)
        x,y=points[-1]; px,py=points[-2]
        if abs(x-px)>abs(y-py):
            sign=1 if x>px else -1
            head=[(x,y),(x-sign*8,y-5),(x-sign*8,y+5)]
        else:
            sign=1 if y>py else -1
            head=[(x,y),(x-5,y-sign*8),(x+5,y-sign*8)]
        draw.polygon([(int(a*scale),int((b+offset_y)*scale)) for a,b in head],fill='#566370')
        if label:
            if len(points)==2:
                xx=(points[0][0]+points[1][0])/2
                yy=(points[0][1]+points[1][1])/2
            else:
                xx,yy=points[len(points)//2]
            if len(points)==2 and abs(points[1][0]-points[0][0])>abs(points[1][1]-points[0][1]):
                draw.text((xx*scale,(yy+offset_y-4)*scale),label,anchor='mb',font=font(14*scale),fill='#333333')
            else:
                draw.text((xx*scale+4*scale,(yy+offset_y)*scale-19*scale),label,font=font(14*scale),fill='#333333')
    def box(x,y,bw,bh,title,body='',interface=False):
        rect=(x*scale,(y+offset_y)*scale,(x+bw)*scale,(y+bh+offset_y)*scale)
        draw.rounded_rectangle(rect,radius=5*scale,fill='#f4f7f9',outline='#526473',width=2*scale)
        parts=title.split('\n')
        ty=y+8
        if interface:
            draw.text(((x+bw/2)*scale,(ty+offset_y)*scale),'«interface»',anchor='mt',font=font(12*scale),fill='#333333')
            ty+=14
        for s in parts:
            title_size=18
            while draw.textlength(s,font=font(title_size*scale,True))>(bw-16)*scale:
                title_size-=1
            draw.text(((x+bw/2)*scale,(ty+offset_y)*scale),s,anchor='mt',font=font(title_size*scale,True),fill='black'); ty+=16
        if body:
            line([(x,ty+3),(x+bw,ty+3)])
            for s in body.split('\n'):
                ty+=16
                draw.text(((x+9)*scale,(ty+offset_y)*scale),s,font=font(16*scale),fill='#222222')
    if kind=='flujo':
        # El orden exacto de la fachada se preserva y el rechazo no genera evento.
        draw.ellipse((420*scale,5*scale,580*scale,35*scale),fill='#e7eef3',outline='#526473',width=2*scale)
        draw.text((500*scale,20*scale),'Inicio',anchor='mm',font=font(14*scale,True),fill='black')
        arrow([(500,-5),(500,15)])
        box(290,15,420,45,'Estudiante registra solicitud')
        box(290,85,420,50,'Facade consulta las salas disponibles')
        box(290,160,420,50,'Strategy selecciona por capacidad o código')
        arrow([(500,60),(500,85)]); arrow([(500,135),(500,160)])
        dia=[(500,235),(660,285),(500,335),(340,285)]
        draw.polygon([(x*scale,(y+offset_y)*scale) for x,y in dia],fill='#e7eef3',outline='#526473',width=2*scale)
        draw.text((500*scale,(280+offset_y)*scale),'¿Hay sala adecuada?',anchor='mm',font=font(16*scale,True),fill='black')
        arrow([(500,210),(500,235)])
        box(25,370,220,80,'No crear reserva','Optional.empty()\nNo guardar ni confirmar')
        arrow([(340,285),(135,285),(135,370)],'No')
        box(290,370,420,70,'Builder valida y construye','Estado inicial Pendiente')
        arrow([(500,335),(500,370)],'Sí')
        box(290,465,420,55,'Facade suscribe los dos observadores')
        box(290,545,420,55,'Repositorio guarda la reserva')
        box(290,625,420,55,'State confirma la reserva')
        box(290,705,420,65,'Observer comunica el cambio válido','NotificadorEstudiante y RegistroEventos')
        for a,b in [(440,465),(520,545),(600,625),(680,705)]: arrow([(500,a),(500,b)])
        box(20,835,290,85,'Cancelar o finalizar','State valida el cambio\nObserver notifica si es válido')
        box(375,835,290,85,'Operación inválida','IllegalStateException\nSin notificaciones')
        box(730,835,250,85,'Sin operación posterior','Se devuelve la reserva\ncon su estado actual')
        arrow([(500,770),(500,800),(165,800),(165,835)])
        arrow([(500,770),(500,835)])
        arrow([(500,770),(500,800),(855,800),(855,835)])
        for xx in [165,520,855]:arrow([(xx,920),(xx,1000),(500,1000),(500,1010)])
        arrow([(135,450),(5,450),(5,1000),(500,1000),(500,1010)])
        draw.ellipse((420*scale,1050*scale,580*scale,1090*scale),fill='#e7eef3',outline='#526473',width=2*scale)
        draw.text((500*scale,1070*scale),'Fin',anchor='mm',font=font(14*scale,True),fill='black')
        draw.text((500*scale,1120*scale),'La disponibilidad es simulada y no consulta un calendario.',anchor='mm',font=font(14*scale),fill='#333333')
    elif kind=='creacion':
        box(440,10,220,58,'Main','+ main(args)')
        box(385,105,330,90,'ReservaFacade','- repositorios y observadores\n+ realizarReserva(...)')
        box(15,245,270,80,'RepositorioSalas','+ obtenerDisponibles()',True)
        box(15,380,270,90,'RepositorioSalasMemoria','- salas A B C D\n+ obtenerDisponibles()')
        box(815,245,270,80,'RepositorioReservas','+ guardar(reserva)',True)
        box(815,380,270,90,'RepositorioReservasMemoria','- reservas\n+ obtenerTodas()')
        box(380,250,340,88,'EstrategiaSeleccionSala','+ seleccionar(salas, personas)',True)
        box(335,390,205,70,'SeleccionPorCapacidad','+ seleccionar(...)')
        box(560,390,240,70,'SeleccionSalaPreferida','- codigoPreferido')
        box(390,520,320,100,'ReservaBuilder','- estudiante fecha horaInicio sala\n- duracionHoras cantidadPersonas\n+ build()')
        box(415,675,270,100,'Reserva','- codigo fecha horaInicio\n- duracionHoras cantidadPersonas\n+ getNombreEstado()')
        box(15,675,280,100,'Estudiante','- identificador\n- nombre')
        box(810,675,275,100,'Sala','- codigo nombre\n- capacidad')
        arrow([(550,68),(550,105)],'usa')
        arrow([(385,150),(150,150),(150,245)],'consulta')
        arrow([(715,150),(950,150),(950,245)],'guarda')
        arrow([(550,195),(550,250)],'recibe')
        arrow([(150,380),(150,325)],'implementa')
        arrow([(950,380),(950,325)],'implementa')
        arrow([(435,390),(435,338)],'implementa')
        arrow([(680,390),(680,338)],'implementa')
        arrow([(715,185),(805,185),(805,490),(550,490),(550,520)],'usa')
        arrow([(550,620),(550,675)],'crea')
        arrow([(415,735),(295,735)],'estudiante')
        arrow([(685,735),(810,735)],'sala')
    else:
        box(380,20,340,190,'Reserva','- estado: EstadoReserva\n- observadores: List\n+ confirmar() cancelar() finalizar()\n+ agregarObservador(...)\n+ retirarObservador(...)\n~ cambiarEstado(...)')
        box(20,280,390,115,'EstadoReserva','+ nombre()\n+ confirmar(Reserva)\n+ cancelar(Reserva) finalizar(Reserva)',True)
        box(685,280,395,100,'ObservadorReserva','+ actualizar(reserva, anterior, nuevo)',True)
        box(10,500,195,90,'Pendiente','confirma o cancela\nrechaza finalizar')
        box(225,500,195,90,'Confirmada','cancela o finaliza\nrechaza confirmar')
        box(10,675,195,80,'Cancelada','estado terminal')
        box(225,675,195,80,'Finalizada','estado terminal')
        box(600,500,245,90,'NotificadorEstudiante','+ actualizar(...)\nmensaje al estudiante')
        box(865,500,220,90,'RegistroEventos','+ actualizar(...)\nregistro en consola')
        arrow([(420,210),(420,245),(215,245),(215,280)],'delega')
        arrow([(680,210),(680,245),(880,245),(880,280)],'0..* suscriptores')
        arrow([(105,500),(105,395)],'implementa')
        arrow([(320,500),(320,395)],'implementa')
        arrow([(105,675),(105,625),(465,625),(465,420),(370,420),(370,395)],'implementa')
        arrow([(320,675),(320,650),(490,650),(490,400),(395,400)],'implementa')
        arrow([(720,500),(720,425),(800,425),(800,380)],'implementa')
        arrow([(970,500),(970,380)],'implementa')
        draw.text((730*scale,685*scale),'Cada cambio válido publica un evento.',anchor='mm',font=font(16*scale,True),fill='black')
        draw.text((730*scale,720*scale),'El rechazo conserva el estado y no publica.',anchor='mm',font=font(14*scale),fill='#333333')
    im.save(path)

def git(repo,*args):
    # Confianza limitada al repositorio solicitado, sin cambiar la configuración global.
    out=subprocess.run(['git','--no-optional-locks','-c','safe.directory='+repo.resolve().as_posix(),'-C',str(repo),*args],capture_output=True,text=True,encoding='utf-8')
    if out.returncode: raise RuntimeError(out.stderr)
    return out.stdout.strip()

def build_pages(meta, tests, mainlog, testlog, commits):
    pages=[]
    def page(title, *items): pages.append((title,list(items)))
    def p(s): return ('p',s)
    def h(s): return ('h',s)
    def table(headers,rows,widths=None): return ('table',(headers,rows,widths))
    def image(name,width,height): return ('image',(name,width,height))
    def code(s): return ('code',s)

    page('Sistema de reservas de biblioteca',
        ('subtitle','Identificación e implementación de patrones de diseño'),
        ('cover','Informe académico del laboratorio individual'),
        ('cover','Análisis y diseño de sistemas de información'),
        ('cover','4 de noviembre de 2026'),
        ('space',60),
        p('El prototipo de consola coordina solicitudes de reserva de salas mediante Builder, Strategy, Facade, Observer y State. La solución separa la construcción de objetos, la selección de salas, el almacenamiento temporal, el control de estados y las notificaciones.'),
        p('Este informe explica el diseño, relaciona los requisitos con sus clases y registra los resultados de ejecución del código final. La aplicación se implementa en Java 17, sin frameworks ni dependencias externas de ejecución.'),
        p('La disponibilidad se simula con cuatro salas fijas. No existe agenda real, bloqueo por horarios ni persistencia entre ejecuciones. El cumplimiento del laboratorio debe evaluarse dentro de ese alcance.'))

    page('1 Propósito y reglas del caso',
        p('El objetivo es registrar una solicitud, seleccionar una sala suficiente, construir la reserva, guardarla y confirmarla. Después se puede cancelar o finalizar según el estado. Cada transición válida comunica el cambio al estudiante y al registro de eventos; una operación rechazada no genera un evento.'),
        table(['Sala','Código','Capacidad'],[['Sala A','A','2 personas'],['Sala B','B','4 personas'],['Sala C','C','6 personas'],['Sala D','D','8 personas']],[2.9,1.2,2.8]),
        h('Datos y validaciones'),
        p('Una solicitud contiene estudiante, fecha, hora de inicio, duración en horas, cantidad de personas y criterio de selección. Estudiante exige identificador y nombre no vacíos. Sala exige código, nombre y capacidad positiva. Builder rechaza datos obligatorios ausentes, fechas anteriores al día de ejecución, duración o cantidad no positivas y capacidad insuficiente.'),
        p('La selección por capacidad utiliza la sala más pequeña que alcanza para el grupo. La selección por preferencia exige que el código solicitado exista y tenga capacidad suficiente. Si no se encuentra sala, la fachada devuelve Optional.empty y no registra ni confirma una reserva.'),
        h('Responsabilidades separadas'),
        table(['Responsabilidad','Clases principales'],[['Configurar dependencias y presentar escenarios','Main'],['Representar datos de estudiante y sala','Estudiante y Sala'],['Construir y validar la reserva','ReservaBuilder'],['Elegir una sala','EstrategiaSeleccionSala y estrategias concretas'],['Consultar salas y guardar reservas','Repositorios y sus implementaciones en memoria'],['Coordinar el caso de uso','ReservaFacade'],['Validar transiciones del ciclo de vida','EstadoReserva y sus cuatro estados'],['Comunicar cambios a suscriptores','ObservadorReserva y observadores concretos']],[3.1,3.8]),
        p('Concentrar estas tareas en Main produciría una clase con demasiados motivos de cambio: variar una estrategia, modificar una validación o añadir un observador obligaría a editar el mismo punto de entrada.'))

    page('2 Flujo de la reserva',
        p('La fachada ejecuta la secuencia de coordinación. La rama sin sala termina antes de construir o guardar. En la rama exitosa, los observadores se suscriben antes de la confirmación para recibir el primer evento.'),
        image('flujo.png',16.5,18.81),
        p('Figura 1. Flujo del caso de uso y de sus operaciones posteriores. Cancelar o finalizar requiere un estado que permita la operación; los estados terminales rechazan nuevas transiciones.'))

    page('3 Clases para creación y selección',
        p('La primera vista muestra los datos, la construcción, las estrategias y los repositorios. Las flechas rotuladas implementa representan realización de interfaces; las demás indican uso o asociación. Main ensambla las dependencias concretas y la fachada consume contratos.'),
        image('clases_creacion.png',17.0,12.67),
        table(['Relación','Interpretación'],[['ReservaFacade → repositorios','Consulta y guarda mediante interfaces inyectadas por constructor.'],['ReservaFacade → estrategia','El algoritmo se recibe en cada llamada a realizarReserva.'],['ReservaBuilder → Reserva','Construye una reserva válida y genera su código.'],['Reserva → Estudiante y Sala','Una reserva conserva sus referencias y datos de solicitud.'],['Repositorios de memoria → listas','Las salas son fijas y las reservas solo viven en el proceso.']],[3.2,3.7]),
        p('Figura 2. Vista de creación y selección. La vista siguiente completa los 21 tipos públicos del paquete biblioteca.'))

    page('4 Clases para estados y observación',
        p('Reserva mantiene un estado y una lista de observadores. Los métodos públicos confirmar, cancelar y finalizar delegan el comportamiento. El método cambiarEstado tiene acceso de paquete y centraliza la publicación del evento.'),
        image('clases_ciclo.png',17.0,12.67),
        table(['Asociación','Multiplicidad y efecto'],[['Reserva → EstadoReserva','Un estado actual por reserva; empieza en Pendiente.'],['Reserva → ObservadorReserva','De cero a muchos suscriptores registrados.'],['EstadoReserva → Reserva','Una transición permitida solicita el nuevo estado.'],['NotificadorEstudiante y RegistroEventos','Implementan el mismo contrato y producen mensajes en consola.']],[3.2,3.7]),
        p('Figura 3. Vista de ciclo de vida. El símbolo ~ indica acceso de paquete. Las interfaces son contratos, no implementaciones de almacenamiento o notificación.'))

    page('5 Builder Strategy y Facade',
        h('Builder'),
        p('ReservaBuilder concentra las validaciones de construcción y permite expresar cada dato mediante un método con nombre. El cliente encadena estudiante, fecha, horaInicio, duracionHoras, cantidadPersonas y sala, y finaliza con build. Así se reduce el riesgo de intercambiar parámetros del mismo tipo en un constructor largo.'),
        p('build valida obligatorios, reglas temporales y valores positivos, y después comprueba la capacidad. Genera el código R- seguido de los primeros ocho caracteres del UUID en mayúsculas. Reserva nace en Pendiente; el constructor de paquete evita exponer la construcción posicional fuera de biblioteca.'),
        h('Strategy'),
        p('EstrategiaSeleccionSala define seleccionar(List<Sala>, int), que devuelve Optional<Sala>. SeleccionPorCapacidad filtra las salas suficientes y utiliza el mínimo de capacidad. SeleccionSalaPreferida busca un código sin distinguir mayúsculas y también exige capacidad suficiente.'),
        p('Las estrategias reciben la lista disponible y no consultan almacenamiento por su cuenta. Una nueva política puede implementar la misma interfaz y entregarse a la fachada sin añadir condiciones por tipo en Main o ReservaFacade.'),
        h('Facade'),
        p('ReservaFacade presenta realizarReserva como operación de alto nivel. Recibe repositorios y observadores por constructor. Consulta salas, aplica la estrategia, devuelve vacío si no encuentra una adecuada, utiliza Builder, registra observadores, guarda y confirma. El cliente no necesita repetir esa secuencia ni conocer el orden de sus pasos.'),
        p('RepositorioSalas y RepositorioReservas separan los contratos de las listas en memoria. RepositorioSalasMemoria conserva A–D mediante List.of. RepositorioReservasMemoria almacena las reservas y expone obtenerTodas como vista inmodificable, aunque el contenido puede crecer cuando el repositorio guarda otra reserva.'),
        h('Límites de estas decisiones'),
        p('El código conserva el alcance de la guía: no hay transacción, búsqueda de duplicados ni control concurrente. El UUID truncado reduce la probabilidad de colisión, pero no garantiza unicidad absoluta. En una aplicación real habría que definir identidad y consistencia del almacenamiento.'))

    page('6 Observer y State',
        h('Observer'),
        p('ObservadorReserva declara actualizar(Reserva, estadoAnterior, estadoNuevo). NotificadorEstudiante presenta el aviso dirigido al estudiante y RegistroEventos escribe el cambio en consola. Reserva depende de la interfaz; no crea ni conoce clases concretas de notificación.'),
        p('agregarObservador incorpora suscriptores no nulos y retirarObservador los elimina. cambiarEstado obtiene el nombre anterior, actualiza el estado y recorre List.copyOf(observadores). La copia permite que una suscripción cambie durante la notificación sin alterar la iteración en curso.'),
        h('State'),
        p('EstadoReserva contiene nombre, confirmar, cancelar y finalizar. Cada estado concreto decide qué solicitudes acepta. Reserva delega esas operaciones en su estado; no mantiene una cadena condicional central que compare textos.'),
        table(['Estado actual','Confirmar','Cancelar','Finalizar'],[['Pendiente','Confirmada','Cancelada','Rechazo'],['Confirmada','Rechazo','Cancelada','Finalizada'],['Cancelada','Rechazo','Rechazo','Rechazo'],['Finalizada','Rechazo','Rechazo','Rechazo']],[1.8,1.7,1.7,1.7]),
        p('Cancelada y Finalizada son terminales. El rechazo lanza IllegalStateException antes de cambiarEstado; por ello conserva el estado y no envía notificaciones. Una confirmación válida produce dos mensajes cuando están suscritos los dos observadores de Main.'),
        h('Encapsulamiento y alcance'),
        p('Cambiar el acceso de cambiarEstado de público a paquete evita invocaciones directas desde otros paquetes. Las propias clases de biblioteca aún pueden utilizarlo, por lo que el cliente debe respetar las operaciones públicas del dominio. El prototipo no impone restricciones horarias ni duración máxima y tampoco define un tratamiento de fallos de observadores.'))

    page('7 SOLID y antipatrones',
        table(['Principio','Aplicación en este código'],[['Responsabilidad única','Builder valida construcción; Strategy selecciona; repositorios almacenan; State decide transiciones; Observer comunica.'],['Abierto y cerrado','Una nueva estrategia u observador implementa un contrato existente sin alterar la coordinación.'],['Sustitución de Liskov','Las estrategias devuelven una sala suficiente o vacío. Los estados respetan el contrato y expresan operaciones inválidas mediante excepciones.'],['Segregación de interfaces','Los contratos de selección, consulta, guardado, estado y observación son pequeños y específicos.'],['Inversión de dependencias','ReservaFacade recibe interfaces de repositorio; Reserva colabora con EstadoReserva y ObservadorReserva.']],[2.0,4.9]),
        h('Decisiones que evitan antipatrones'),
        p('God Object se evita al distribuir responsabilidades y dejar en Main la configuración y los ejemplos. Builder atiende Long Parameter List al nombrar los datos de construcción. State reduce Primitive Obsession: el comportamiento del ciclo de vida se representa con objetos, no con una cadena modificable desde cualquier lugar.'),
        p('Strategy reduce Shotgun Surgery: agregar un criterio no obliga a editar muchas clases ni un switch central. Observer y la inyección de repositorios reducen Tight Coupling: Reserva no instancia NotificadorEstudiante y la fachada no decide el almacenamiento concreto.'),
        p('Para evitar Duplicate Code, no se copian las validaciones de negocio en Main. Selección y construcción cumplen funciones distintas: la estrategia busca una candidata y Builder protege la creación incluso cuando se usa por separado. Swallowing Exceptions se evita al presentar los rechazos con su mensaje, en lugar de capturar excepciones para ignorarlas.'),
        p('Premature Optimization se evita manteniendo el alcance solicitado: no se agrega base de datos, interfaz gráfica, variables globales para reservas ni dependencias externas de ejecución. La sencillez permite observar cada patrón con una responsabilidad concreta.'))

    expected=[
        ('P01','Construcción con todos los datos','ReservaBuilder y Reserva','Builder'),
        ('P02','Falta estudiante','ReservaBuilder','Builder'),
        ('P03','Capacidad para cuatro selecciona B','SeleccionPorCapacidad','Strategy'),
        ('P04','Preferida C para cuatro selecciona C','SeleccionSalaPreferida','Strategy'),
        ('P05','Preferida B para siete devuelve vacío','SeleccionSalaPreferida','Strategy'),
        ('P06','Se guarda y confirma una reserva','ReservaFacade y repositorio','Facade'),
        ('P07','Ambos observadores reciben confirmación','Reserva y observadores','Observer y State'),
        ('P08','Cancelar confirmada cambia y notifica','Confirmada y observadores','State y Observer'),
        ('P09','Reconfirmar cancelada rechaza sin evento','Cancelada y Reserva','State'),
        ('P10','Diez personas no crea reserva','Strategy y ReservaFacade','Strategy y Facade'),
        ('P11','Finalizar confirmada cambia y notifica','Confirmada y observadores','State y Observer')]
    results={str(x.get('id','')):x for x in tests}
    rows=[]
    for id,desc,cls,pat in expected:
        result=results.get(id,{})
        status=result.get('estado',result.get('status',result.get('resultado','VERIFICAR')))
        rows.append([id,desc,cls+'\n'+pat,str(status)])
    page('8 Matriz de trazabilidad y resultados',
        p('Cada escenario vincula un requisito observable, las clases responsables y el patrón que lo sostiene. Los resultados corresponden a la ejecución del arnés nativo y no a las capturas históricas del proyecto.'),
        table(['ID','Escenario y requisito','Clases y patrón','Resultado'],rows,[0.55,2.4,2.8,1.15]),
        p('La verificación adicional incluye datos obligatorios, fechas pasadas, valores no positivos, capacidad insuficiente y las doce combinaciones de cuatro estados por tres operaciones. También se comprueba que un rechazo no altere el estado ni produzca notificaciones.'),
        p(meta.get('resumen_pruebas','')))

    page('9 Evidencias reales de ejecución',
        p('Los fragmentos siguientes se extraen de los logs generados al compilar y ejecutar. Se presentan como texto de consola, no como capturas gráficas. Los archivos completos acompañan la entrega para permitir su revisión y repetición.'),
        h('Aplicación principal'),
        code('\n'.join(mainlog.splitlines()[:30])),
        h('Comprobaciones del arnés'),
        code('\n'.join([ln for ln in testlog.splitlines() if ln.startswith('[PASS]')][:11])),
        p('Los códigos de reserva se generan de nuevo en cada ejecución. Las fechas del Main final usan LocalDate.now().plusDays(...), tal como aparece en la guía; por ello pueden diferir entre logs ejecutados en días distintos.'))

    observed=[]
    for id,desc,cls,pat in expected:
        raw=results[id].get('salidaReal','')
        lines=[ln for ln in raw.splitlines() if ln.strip()]
        selected=lines[-2:] if id=='P06' else [ln for ln in lines if ln.startswith('Rechazo observado:')]+lines[-1:] if id=='P09' else lines[-1:]
        observed.append([id,'\n'.join(selected)])
    page('10 Evidencias de P01 a P11',
        p('Se transcriben las observaciones finales producidas por cada prueba. Los mensajes de notificación y las aserciones completas se conservan en el log y en resultados-pruebas.json. Estos registros permiten distinguir una transición válida de un rechazo sin eventos nuevos.'),
        table(['ID','Salida real observada'],observed,[0.6,6.3]),
        p('En P07, P08 y P11 el conteo se realiza por observador: un evento para NotificadorEstudiante y otro para RegistroEventos por cada transición válida. P09 compara el conteo anterior y posterior al intento rechazado. P10 verifica también que el repositorio permanezca vacío.'))

    page('11 Correcciones y ejecución reproducible',
        table(['Exigido','Existente al revisar','Corrección aplicada'],[['Sala válida y legible','Sin validación de capacidad ni toString','Capacidad positiva y representación de la guía.'],['Builder fiel a la guía','Código manual, horarioInicio y fecha pasada aceptada','Código UUID, horaInicio y rechazo de fechas pasadas.'],['Reserva y eventos','Cambio público sin observadores','Acceso de paquete, getNombreEstado y notificación por copia.'],['Facade y repositorios','Ocho tipos ausentes entre estas capas y Observer','Contratos, listas de memoria, fachada y suscriptores.'],['Main de estación 8','Una reserva fija en Pendiente','Cuatro escenarios con confirmación, cancelación, rechazo y finalización.'],['Pruebas y documentación','Sin pruebas finales ni informe completo','Arnés nativo, logs, diagramas y este informe.']],[1.9,2.4,2.6]),
        h('Entorno comprobado'),
        p(meta.get('entorno','JDK 17 en Windows; compilación UTF-8. La aplicación no necesita bibliotecas externas.')),
        p('En IntelliJ IDEA se abre pom.xml, se selecciona un SDK 17 o superior y se ejecuta biblioteca.Main. La terminal debe utilizar el mismo JDK: un Java 8 en el PATH no puede ejecutar clases compiladas para Java 17.'),
        h('Comandos'),
        code(meta.get('comandos','Consultar README.md y el script de pruebas incluidos en la entrega.')),
        p('La carpeta src/main/java/biblioteca conserva exclusivamente los 21 archivos oficiales. El arnés y los scripts de verificación están fuera de esa carpeta para distinguir el programa académico de sus herramientas de prueba.'))

    page('12 Reflexión individual preguntas 14 a 18',
        h('14 Responsabilidades separadas'),
        p('Se separaron representación de datos, validación de construcción, selección, almacenamiento, coordinación, estados y notificación. Una clase única tendría que cambiar por todos esos motivos y sería difícil probar un criterio de selección sin ejecutar también almacenamiento y consola. La distribución permite probar Strategy con una lista pequeña y State con una reserva aislada.'),
        h('15 Ventaja de Builder'),
        p('Los nombres horaInicio, duracionHoras y cantidadPersonas hacen visible qué significa cada valor. Un constructor con varios enteros y referencias facilita intercambios accidentales. build establece un punto común para rechazar un objeto incompleto antes de ponerlo en circulación.'),
        h('16 Extensión de Strategy'),
        p('Para seleccionar por otro criterio se implementa EstrategiaSeleccionSala y se entrega una instancia a realizarReserva. La fachada continúa invocando seleccionar y manejando Optional. No necesita conocer el nombre de la nueva clase ni agregar un caso condicional.'),
        h('17 Complejidad oculta por Facade'),
        p('ReservaFacade oculta el orden de consultar, seleccionar, validar y construir, suscribir observadores, guardar y confirmar. Main solo configura dependencias y solicita el caso de uso. Así evita depender de cada paso interno y de su secuencia, aunque conserva las decisiones de configuración del ejemplo.'),
        h('18 Desacoplamiento mediante Observer'),
        p('Reserva conoce ObservadorReserva y llama actualizar con el cambio de estado. Cada suscriptor decide cómo presentar ese evento. La lista y la interfaz son los mecanismos de desacoplamiento: incorporar un tercer observador no obliga a importar su clase concreta en Reserva.'))

    page('13 Reflexión individual preguntas 19 a 22',
        h('19 Ventaja de State'),
        p('State agrupa las reglas del ciclo de vida con el estado que las aplica. Cancelada y Finalizada rechazan todas las operaciones de transición; Confirmada permite cancelar y finalizar. Una variable String por sí sola no impide asignaciones arbitrarias ni concentra esas reglas. Los nombres se utilizan para mostrar el estado, no para decidir el comportamiento.'),
        h('20 Dos principios SOLID'),
        p('Responsabilidad única aparece en ReservaBuilder y SeleccionPorCapacidad: el primero construye y valida; la segunda elige una candidata. Inversión de dependencias aparece en ReservaFacade, que recibe RepositorioSalas y RepositorioReservas, y en Reserva, que mantiene contratos de estado y observación. Estas relaciones permiten cambiar implementaciones concretas sin trasladar sus detalles al consumidor.'),
        h('21 Un antipatrón evitado'),
        p('Se evitó God Object al impedir que Main concentre el sistema. La decisión concreta fue asignar la coordinación a ReservaFacade, las reglas de transición a los estados y los avisos a observadores. Main conserva un papel explícito de ensamblaje y demostración, lo que permite repetir los escenarios sin duplicar la lógica de negocio.'),
        h('22 Límite de la disponibilidad simulada'),
        p('RepositorioSalasMemoria devuelve la misma lista fija sin filtrar por fecha y hora. Dos solicitudes pueden recibir la misma sala aunque sus horarios coincidan. Para consultar una fuente real se sustituiría la implementación del repositorio; además habría que evolucionar su contrato para recibir el intervalo, definir solapamientos y realizar la asignación de forma atómica. Cambiar solo la lista por una consulta sin controlar concurrencia no resolvería una doble reserva.'),
        h('Conclusión técnica'),
        p('Los cinco patrones hacen visible una división de responsabilidades que facilita comprender y comprobar el prototipo. Las dificultades técnicas principales son coordinar la suscripción antes del primer cambio de estado y garantizar que un rechazo no envíe eventos. La fachada y la centralización de notificaciones resuelven esas necesidades dentro del alcance del laboratorio.'),
        p('Una mejora futura razonable es incorporar un servicio de disponibilidad por intervalo y un repositorio persistente con control de concurrencia. También convendría utilizar identificadores completos y definir qué ocurre si un observador falla. Estas mejoras requieren requisitos adicionales y no se presentan como funcionalidades ya implementadas.'))

    commitrows=[]
    for ln in commits.splitlines():
        fields=ln.split('|',2)
        if len(fields)==3: commitrows.append(fields)
    page('14 Trazabilidad de Git y referencias',
        p('Se conservó el historial previo y se organizó el trabajo nuevo por estaciones, según la solicitud del estudiante. Las ocho estaciones de la guía no se interpretan como una obligación académica de tener ocho ramas específicas. Los commits describen cambios reales y no reconstruyen fechas o avances anteriores.'),
        table(['Commit','Referencia de etapa','Cambio registrado'],commitrows,[1.05,1.85,4.0]),
        p(meta.get('estado_git','El detalle de ramas, integración y publicación se registra en los archivos de evidencia Git de la entrega. Este informe cita los commits existentes antes de guardar su propia versión para evitar una referencia circular al hash del documento.')),
        h('Cómo verificar el historial'),
        code('git status --short\ngit branch -a -vv\ngit log --oneline --graph --decorate --all\ngit remote -v'),
        h('Referencias utilizadas'),
        p('Guía práctica. Identificación e implementación de patrones de diseño en un sistema de reservas de biblioteca. Asignatura Análisis y diseño de sistemas de información. Capturas originales pagina_01.png a pagina_15.png y recorrido de referencia en video.'),
        p('Código fuente y evidencias de BibliotecaReservas, repositorio https://github.com/Alejoor18/BibliotecaReservas. Las capturas previas de IntelliJ y el borrador se utilizaron como contexto histórico, no como evidencia de las pruebas finales.'))
    return pages

def paragraph(text,style):
    text=text.replace('\u2013','-').replace('\u2014','-').replace('\u2011','-')
    encoded=escape(text).replace('\n','<br/>')
    encoded=re.sub(r'https://github\.com/Alejoor18/BibliotecaReservas',r'<link href="https://github.com/Alejoor18/BibliotecaReservas">https://github.com/Alejoor18/BibliotecaReservas</link>',encoded)
    return Paragraph(encoded,style)

def write_pdf(pages,out):
    pdfmetrics.registerFont(TTFont('ArialReport',str(FONT)))
    pdfmetrics.registerFont(TTFont('ArialReportBold',str(BOLD)))
    pdfmetrics.registerFont(TTFont('ConsolasReport',str(MONO)))
    styles={
      'title':ParagraphStyle('T',fontName='ArialReportBold',fontSize=20,leading=25,spaceAfter=18,textColor=colors.black),
      'p':ParagraphStyle('P',fontName='ArialReport',fontSize=10.2,leading=14.5,spaceAfter=10,alignment=TA_JUSTIFY),
      'h':ParagraphStyle('H',fontName='ArialReportBold',fontSize=11.7,leading=15,spaceBefore=12,spaceAfter=7,textColor=colors.black),
      'cell':ParagraphStyle('C',fontName='ArialReport',fontSize=8.5,leading=11.3,spaceAfter=0),
      'header':ParagraphStyle('CH',fontName='ArialReportBold',fontSize=8.6,leading=11.5,textColor=colors.white),
      'code':ParagraphStyle('Code',fontName='ConsolasReport',fontSize=7.4,leading=10,spaceAfter=9,wordWrap='CJK'),
      'subtitle':ParagraphStyle('Sub',fontName='ArialReportBold',fontSize=14,leading=20,spaceAfter=25,textColor=colors.black),
      'cover':ParagraphStyle('Cover',fontName='ArialReport',fontSize=12,leading=18,spaceAfter=13)}
    story=[]
    for i,(title,items) in enumerate(pages):
        if i: story.append(PageBreak())
        if i==0: story.append(Spacer(1,2.2*cm))
        story.append(paragraph(title,styles['title']))
        for kind,data in items:
            if kind in styles: story.append(paragraph(data,styles[kind]))
            elif kind=='space': story.append(Spacer(1,data))
            elif kind=='image':
                name,w,h=data; story.append(Image(str(BASE/'diagramas'/name),width=w*cm,height=h*cm)); story.append(Spacer(1,9))
            elif kind=='table':
                headers,rows,widths=data
                body=[[paragraph(t,styles['header']) for t in headers]]+[[paragraph(str(t),styles['cell']) for t in row] for row in rows]
                widths=[w/6.9*17*cm for w in widths] if widths else None
                tb=Table(body,colWidths=widths,repeatRows=1,hAlign='LEFT')
                tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#243e53')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f1f4f6')]),('GRID',(0,0),(-1,-1),.45,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
                story.append(tb); story.append(Spacer(1,12))
    def footer(c,d):
        c.setFont('ArialReport',8)
        c.setFillColor(colors.HexColor('#666666'))
        c.drawString(2*cm,1.2*cm,'BibliotecaReservas  |  Informe académico')
        c.drawRightString(A4[0]-2*cm,1.2*cm,str(d.page))
    doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=2*cm,rightMargin=2*cm,topMargin=1.8*cm,bottomMargin=1.9*cm,title='Sistema de reservas de biblioteca',author='BibliotecaReservas')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)

def write_md(pages,out):
    lines=[]
    for title,items in pages:
        lines+=['# '+title,'']
        for kind,data in items:
            if kind in ['p','subtitle','cover']:lines+=[data,'']
            elif kind=='h':lines+=['## '+data,'']
            elif kind=='code':lines+=['```text',data,'```','']
            elif kind=='image':lines+=['!['+data[0]+'](diagramas/'+data[0]+')','']
            elif kind=='table':
                headers,rows,_=data
                lines+=['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']
                for row in rows:lines+=['| '+' | '.join(str(x).replace('\n','; ') for x in row)+' |']
                lines+=['']
    out.write_text('\n'.join(lines),encoding='utf-8')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--datos',type=Path,required=True)
    parser.add_argument('--resultados',type=Path,required=True)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--main-log',type=Path,required=True)
    parser.add_argument('--test-log',type=Path,required=True)
    args=parser.parse_args()
    meta=json.loads(args.datos.read_text(encoding='utf-8-sig'))
    testdata=json.loads(args.resultados.read_text(encoding='utf-8-sig'))
    if testdata['fallidas']!=0:raise ValueError('Existen pruebas fallidas')
    tests=[{**case,'estado':case['resultado']} for case in testdata['casos'] if re.fullmatch(r'P\d\d',case['id'])]
    meta.setdefault('resumen_pruebas',f"Se ejecutaron {testdata['total']} casos: {testdata['aprobadas']} aprobados y {testdata['fallidas']} fallidos. Fecha UTC de ejecución: {testdata['ejecutadoUtc']}.")
    if {str(t['id']) for t in tests}!={f'P{i:02}' for i in range(1,12)}:raise ValueError('Se requieren once resultados reales P01-P11')
    if any(str(t.get('estado','')).upper() not in ['OK','PASS','CORRECTA','CORRECTO'] for t in tests):raise ValueError('Revisar pruebas antes de finalizar')
    mainlog=args.main_log.read_text(encoding='utf-8-sig')
    testlog=args.test_log.read_text(encoding='utf-8-sig')
    if not mainlog.strip() or not testlog.strip():raise ValueError('Los logs no pueden estar vacíos')
    refs=git(args.repo,'for-each-ref','--format=%(objectname:short)|%(refname:short)','refs/heads').splitlines()
    byhash={}
    for ref in refs:
        sha,name=ref.split('|',1);byhash.setdefault(sha,[]).append(name.replace('codex/',''))
    commitlines=[]
    for ln in git(args.repo,'log','--no-merges','--reverse','--format=%h|%s').splitlines():
        sha,subject=ln.split('|',1)
        names=', '.join(byhash.get(sha,[])) or 'historial conservado'
        commitlines.append(sha+'|'+names+'|'+subject)
    pages=build_pages(meta,tests,mainlog,testlog,'\n'.join(commitlines))
    (BASE/'diagramas').mkdir(exist_ok=True)
    for name,content in [('flujo',FLOW),('clases_creacion',UML1),('clases_ciclo',UML2)]:
        (BASE/'diagramas'/f'{name}.mmd').write_text(content.replace('\\n','\n'),encoding='utf-8')
        diagram(BASE/'diagramas'/f'{name}.png','flujo' if name=='flujo' else 'creacion' if name=='clases_creacion' else 'ciclo')
    write_pdf(pages,BASE/'Informe_BibliotecaReservas.pdf')
    write_md(pages,BASE/'Informe_BibliotecaReservas.md')
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.glob('Informe_BibliotecaReservas.*')}
    (BASE/'manifest-documentos.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'paginas_disenadas':len(pages),'archivos':manifest},ensure_ascii=False))

if __name__=='__main__':main()
