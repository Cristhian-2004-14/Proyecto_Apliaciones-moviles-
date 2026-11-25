from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r"C:\Users\Usuario\Desktop\actividad_1")
OUT = ROOT / "entregables" / "informe_avance_brasas_apa7_sin_caratula.docx"
EVIDENCE = ROOT / "evidencias" / "pantalla_emulador.png"

def set_font(run, size=12, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic

def set_spacing(paragraph, before=0, after=0, line=2.0):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line

def text(doc, content, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=True, italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    set_spacing(p)
    if first_indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    r = p.add_run(content)
    set_font(r, italic=italic)
    return p

def heading(doc, content, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    set_spacing(p, before=12, after=6, line=2.0)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(content)
    set_font(r, 12, bold=True)
    return p

def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.append(fld)
    set_font(run)

def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

def set_cell(cell, value, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_spacing(p, line=1.15)
    r = p.add_run(value)
    set_font(r, 11, bold=bold)
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = OxmlElement("w:tcMar")
    for side in ("top", "start", "bottom", "end"):
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), "100")
        m.set(qn("w:type"), "dxa")
        margins.append(m)
    tc_pr.append(margins)

def add_caption(doc, label):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_spacing(p, before=3, after=4, line=1.15)
    r = p.add_run(label)
    set_font(r, 11, italic=True)
    return p

doc = Document()
section = doc.sections[0]
section.top_margin = Inches(1)
section.bottom_margin = Inches(1)
section.left_margin = Inches(1)
section.right_margin = Inches(1)

styles = doc.styles
for name in ["Normal", "Title", "Heading 1", "Heading 2"]:
    style = styles[name]
    style.font.name = "Times New Roman"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    style.font.size = Pt(12)

header = section.header.paragraphs[0]
add_page_number(header)

# Page 1 - title and summary, no cover page.
p = doc.add_paragraph(style="Title")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_spacing(p, before=0, after=18, line=2.0)
r = p.add_run("Informe de avance del MVP móvil Brasas del Oriente")
set_font(r, 12, bold=True)

heading(doc, "Resumen")
text(doc, "Este informe presenta el avance de Brasas del Oriente, un MVP móvil desarrollado en Flutter para una churrasquería local de Santa Cruz de la Sierra. El sistema ofrece una pantalla de bienvenida, un menú digital con búsqueda y filtros, formularios para consultas y reservas, y una pantalla de ubicación y horarios. La integración con Supabase está preparada mediante configuración, servicios y scripts SQL. Las pruebas de análisis y navegación fueron aprobadas; la ejecución completa en Android y la conexión real con Supabase permanecen pendientes de verificación. El alcance no incluye pagos ni autenticación.", first_indent=False)
text(doc, "Palabras clave: Flutter, aplicación móvil, churrasquería, Supabase, MVP.", first_indent=False, italic=True)

# Page 2 - index.
page_break(doc)
heading(doc, "Índice")
for item, page in [
    ("Introducción", "3"),
    ("Objetivo del proyecto", "3"),
    ("Tecnología seleccionada", "4"),
    ("Desarrollo del MVP", "5"),
    ("Evidencias y validaciones", "6"),
    ("Limitaciones y trabajo pendiente", "7"),
    ("Conclusiones", "7"),
    ("Referencias", "8"),
]:
    p = doc.add_paragraph()
    set_spacing(p, after=3, line=1.5)
    r = p.add_run(f"{item} {' .' * 22} {page}")
    set_font(r)

# Page 3.
page_break(doc)
heading(doc, "Introducción")
text(doc, "Los pequeños negocios gastronómicos suelen difundir su oferta y recibir consultas mediante redes sociales y mensajería. Para este caso académico, Brasas del Oriente requiere una aplicación inicial que facilite la exploración del menú y la recepción de solicitudes. El proyecto se diseñó como un producto mínimo viable, por lo que prioriza funciones concretas y deja fuera procesos que requieren una validación adicional, como pagos, autenticación y confirmación automática de disponibilidad.")
heading(doc, "Objetivo del proyecto")
text(doc, "Desarrollar un MVP multiplataforma que permita al usuario conocer el menú de la churrasquería, enviar una consulta, solicitar una reserva y revisar la ubicación y los horarios del negocio.")
heading(doc, "Alcance")
text(doc, "El alcance incluye la interfaz móvil, la navegación entre pantallas, la búsqueda y el filtrado del menú, la validación de formularios y una capa de servicios preparada para Supabase. Los datos locales y los precios son demostrativos. El proyecto no implementa pagos, pedidos, autenticación ni una confirmación definitiva de reservas.")

# Page 4.
page_break(doc)
heading(doc, "Tecnología seleccionada")
text(doc, "Se compararon Flutter, React Native y el desarrollo nativo separado para Android e iOS. La matriz ponderada consideró costo inicial y mantenimiento, rendimiento previsto, comunidad y ecosistema, compatibilidad Android e iOS y curva de aprendizaje. La operación aplicada fue peso por calificación dividido entre cinco.")
p = doc.add_paragraph()
set_spacing(p, before=6, after=3, line=1.15)
r = p.add_run("Tabla 1\nResultados de la matriz ponderada")
set_font(r, 12, italic=True)
table = doc.add_table(rows=4, cols=2)
table.style = "Table Grid"
table.autofit = False
table.columns[0].width = Inches(4.5)
table.columns[1].width = Inches(2.0)
for cell, value in zip(table.rows[0].cells, ["Alternativa", "Puntaje de 100"]): set_cell(cell, value, bold=True)
for row, values in zip(table.rows[1:], [("Flutter", "91"), ("React Native", "83"), ("Nativo Android e iOS", "66")]):
    for cell, value in zip(row.cells, values): set_cell(cell, value)
text(doc, "Flutter obtuvo la puntuación más alta para este caso porque permite mantener una base de código común y una interfaz consistente en Android e iOS. La elección no reemplaza las pruebas de rendimiento en dispositivos reales ni la revisión de paquetes antes de incorporar nuevas funciones (Flutter, s. f.-a; Flutter, s. f.-b).", first_indent=False)

# Page 5.
page_break(doc)
heading(doc, "Desarrollo del MVP")
text(doc, "La aplicación se desarrolló con Flutter y Material 3. La pantalla inicial dirige al usuario al menú digital, a la reserva de mesa, a la consulta y a la información de ubicación y horarios. El catálogo usa una lista dinámica, un campo de búsqueda y filtros por categoría. Cuando no se configura Supabase, el proyecto muestra datos locales para que el flujo de interfaz continúe disponible.")
heading(doc, "Formularios y validaciones", level=2)
text(doc, "El formulario de reserva solicita nombre, teléfono boliviano, fecha, hora y cantidad de personas. El sistema evita el envío de campos incompletos y rechaza fechas u horas pasadas. La reserva solo se registra en Supabase cuando la configuración pública de la aplicación está disponible. El formulario de consulta aplica validaciones equivalentes para evitar registros vacíos o incompletos.")
heading(doc, "Arquitectura", level=2)
text(doc, "La estructura separa las pantallas, los servicios, los modelos y la configuración. Las pantallas presentan la interfaz; los servicios concentran las consultas y escrituras; los modelos representan los datos; y los scripts de Supabase definen tablas, datos semilla y reglas de acceso a nivel de fila. Esta organización permite sustituir los datos demostrativos por datos remotos sin reescribir la interfaz.")

# Page 6 - evidence image under half page.
page_break(doc)
heading(doc, "Evidencias y validaciones")
text(doc, "La Figura 1 muestra la pantalla de bienvenida disponible como evidencia visual del prototipo. La imagen se mantiene compacta y no representa una prueba de ejecución Android. Para esa verificación se requiere un dispositivo físico o un emulador configurado.")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_spacing(p, before=6, after=0, line=1.0)
p.add_run().add_picture(str(EVIDENCE), width=Inches(1.45))
add_caption(doc, "Figura 1\nPantalla de bienvenida del prototipo")
text(doc, "Las validaciones registradas indican que flutter analyze finalizó sin incidencias y que flutter test aprobó una prueba de navegación. En cambio, no se verificó una ejecución Android porque el JDK del entorno estaba incompleto y no existía un emulador Android configurado. Por esta razón, el informe distingue entre las pruebas aprobadas y las evidencias pendientes.", first_indent=False)

# Page 7.
page_break(doc)
heading(doc, "Limitaciones y trabajo pendiente")
text(doc, "La principal limitación actual es de entorno. Para completar la validación se debe instalar o reparar un JDK 17 o superior, configurar Flutter con esa ruta y crear un dispositivo virtual Android o conectar un teléfono con depuración USB. Después se debe ejecutar la aplicación, verificar la navegación y conservar una captura auténtica del resultado.")
text(doc, "También se debe ejecutar la configuración de Supabase con la URL y la clave pública en tiempo de ejecución. La clave secreta o service_role no debe incorporarse al cliente Flutter. Una vez que la conexión esté validada, el equipo podrá comprobar la lectura remota del catálogo y el registro de consultas y reservas.")
heading(doc, "Conclusiones")
text(doc, "Brasas del Oriente cuenta con un avance funcional de MVP que cubre las interacciones principales del usuario: conocer la oferta, realizar una consulta y solicitar una reserva. Flutter resultó adecuado para el alcance académico por su base de código compartida. El siguiente hito consiste en validar el flujo completo en Android y con Supabase antes de ampliar el alcance del sistema.")

# Page 8.
page_break(doc)
heading(doc, "Referencias")
refs = [
    "Apple. (s. f.). SwiftUI. Recuperado el 8 de noviembre de 2026, de https://developer.apple.com/swiftui/",
    "Corti, N. (2024, 25 de junio). Use a framework to build React Native apps. React Native. https://reactnative.dev/blog/2024/06/25/use-a-framework-to-build-react-native-apps",
    "Flutter. (s. f.-a). FAQ. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/resources/faq",
    "Flutter. (s. f.-b). Flutter performance profiling. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/perf/ui-performance",
    "Google. (s. f.). Develop for Android. https://developer.android.com/develop",
    "Meta. (s. f.). Platform-specific code. React Native. https://reactnative.dev/docs/platform-specific-code.html",
]
for ref in refs:
    p = doc.add_paragraph()
    set_spacing(p, after=0, line=2.0)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    r = p.add_run(ref)
    set_font(r)

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(OUT)
