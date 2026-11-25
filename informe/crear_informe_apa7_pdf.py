from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether

ROOT = Path(r"C:\Users\Usuario\Desktop\actividad_1")
OUT = ROOT / "entregables" / "informe_avance_brasas_apa7_sin_caratula.pdf"
EVIDENCE = ROOT / "evidencias" / "pantalla_emulador.png"

PAGE_W, PAGE_H = letter
MARGIN = inch

styles = getSampleStyleSheet()
base = dict(fontName="Times-Roman", fontSize=12, leading=24, textColor=colors.black)
title = ParagraphStyle("TitleAPA", parent=styles["Normal"], alignment=TA_CENTER, spaceAfter=18, **base)
h1 = ParagraphStyle("HeadingAPA", parent=styles["Normal"], alignment=TA_CENTER, spaceBefore=12, spaceAfter=6, fontName="Times-Bold", fontSize=12, leading=24, textColor=colors.black)
h2 = ParagraphStyle("Heading2APA", parent=styles["Normal"], alignment=TA_LEFT, spaceBefore=12, spaceAfter=6, fontName="Times-Bold", fontSize=12, leading=24, textColor=colors.black)
body = ParagraphStyle("BodyAPA", parent=styles["Normal"], firstLineIndent=0.5*inch, spaceAfter=0, **base)
body_noindent = ParagraphStyle("BodyNoIndent", parent=styles["Normal"], spaceAfter=0, **base)
keyword = ParagraphStyle("Keywords", parent=styles["Normal"], spaceAfter=0, fontName="Times-Italic", fontSize=12, leading=24, textColor=colors.black)
toc = ParagraphStyle("TOC", parent=styles["Normal"], spaceAfter=3, fontName="Times-Roman", fontSize=12, leading=18, textColor=colors.black)
caption = ParagraphStyle("Caption", parent=styles["Normal"], alignment=TA_CENTER, spaceBefore=2, spaceAfter=4, fontName="Times-Italic", fontSize=11, leading=13, textColor=colors.black)
ref = ParagraphStyle("References", parent=styles["Normal"], leftIndent=0.5*inch, firstLineIndent=-0.5*inch, spaceAfter=0, **base)
table_caption = ParagraphStyle("TableCaption", parent=styles["Normal"], fontName="Times-Italic", fontSize=12, leading=18, spaceBefore=6, spaceAfter=3, textColor=colors.black)

def P(value, style=body): return Paragraph(value, style)
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 12)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.55*inch, str(doc.page))
    canvas.restoreState()

story = []
# Page 1
story += [P("Informe de avance del MVP móvil Brasas del Oriente", title), P("Resumen", h1)]
story += [P("Este informe presenta el avance de Brasas del Oriente, un MVP móvil desarrollado en Flutter para una churrasquería local de Santa Cruz de la Sierra. El sistema ofrece una pantalla de bienvenida, un menú digital con búsqueda y filtros, formularios para consultas y reservas, y una pantalla de ubicación y horarios. La integración con Supabase está preparada mediante configuración, servicios y scripts SQL. Las pruebas de análisis y navegación fueron aprobadas; la ejecución completa en Android y la conexión real con Supabase permanecen pendientes de verificación. El alcance no incluye pagos ni autenticación.", body_noindent)]
story += [P("<i>Palabras clave:</i> Flutter, aplicación móvil, churrasquería, Supabase, MVP.", keyword), PageBreak()]

# Page 2
story += [P("Índice", h1)]
for name, page in [("Introducción",3),("Objetivo del proyecto",3),("Tecnología seleccionada",4),("Desarrollo del MVP",5),("Evidencias y validaciones",6),("Limitaciones y trabajo pendiente",7),("Conclusiones",7),("Referencias",8)]:
    story.append(P(f"{name} {'.' * 52} {page}", toc))
story.append(PageBreak())

# Page 3
story += [P("Introducción", h1), P("Los pequeños negocios gastronómicos suelen difundir su oferta y recibir consultas mediante redes sociales y mensajería. Para este caso académico, Brasas del Oriente requiere una aplicación inicial que facilite la exploración del menú y la recepción de solicitudes. El proyecto se diseñó como un producto mínimo viable, por lo que prioriza funciones concretas y deja fuera procesos que requieren una validación adicional, como pagos, autenticación y confirmación automática de disponibilidad."), P("Objetivo del proyecto", h1), P("Desarrollar un MVP multiplataforma que permita al usuario conocer el menú de la churrasquería, enviar una consulta, solicitar una reserva y revisar la ubicación y los horarios del negocio."), P("Alcance", h1), P("El alcance incluye la interfaz móvil, la navegación entre pantallas, la búsqueda y el filtrado del menú, la validación de formularios y una capa de servicios preparada para Supabase. Los datos locales y los precios son demostrativos. El proyecto no implementa pagos, pedidos, autenticación ni una confirmación definitiva de reservas."), PageBreak()]

# Page 4
story += [P("Tecnología seleccionada", h1), P("Se compararon Flutter, React Native y el desarrollo nativo separado para Android e iOS. La matriz ponderada consideró costo inicial y mantenimiento, rendimiento previsto, comunidad y ecosistema, compatibilidad Android e iOS y curva de aprendizaje. La operación aplicada fue peso por calificación dividido entre cinco."), P("Tabla 1<br/>Resultados de la matriz ponderada", table_caption)]
tbl = Table([["Alternativa","Puntaje de 100"],["Flutter","91"],["React Native","83"],["Nativo Android e iOS","66"]], colWidths=[4.5*inch,2.0*inch])
tbl.setStyle(TableStyle([("FONTNAME",(0,0),(-1,-1),"Times-Roman"),("FONTNAME",(0,0),(-1,0),"Times-Bold"),("FONTSIZE",(0,0),(-1,-1),11),("LEADING",(0,0),(-1,-1),14),("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#D9D9D9")),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EAEAEA")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [tbl, Spacer(1,10), P("Flutter obtuvo la puntuación más alta para este caso porque permite mantener una base de código común y una interfaz consistente en Android e iOS. La elección no reemplaza las pruebas de rendimiento en dispositivos reales ni la revisión de paquetes antes de incorporar nuevas funciones (Flutter, s. f.-a; Flutter, s. f.-b).", body_noindent), PageBreak()]

# Page 5
story += [P("Desarrollo del MVP", h1), P("La aplicación se desarrolló con Flutter y Material 3. La pantalla inicial dirige al usuario al menú digital, a la reserva de mesa, a la consulta y a la información de ubicación y horarios. El catálogo usa una lista dinámica, un campo de búsqueda y filtros por categoría. Cuando no se configura Supabase, el proyecto muestra datos locales para que el flujo de interfaz continúe disponible."), P("Formularios y validaciones", h2), P("El formulario de reserva solicita nombre, teléfono boliviano, fecha, hora y cantidad de personas. El sistema evita el envío de campos incompletos y rechaza fechas u horas pasadas. La reserva solo se registra en Supabase cuando la configuración pública de la aplicación está disponible. El formulario de consulta aplica validaciones equivalentes para evitar registros vacíos o incompletos."), P("Arquitectura", h2), P("La estructura separa las pantallas, los servicios, los modelos y la configuración. Las pantallas presentan la interfaz; los servicios concentran las consultas y escrituras; los modelos representan los datos; y los scripts de Supabase definen tablas, datos semilla y reglas de acceso a nivel de fila. Esta organización permite sustituir los datos demostrativos por datos remotos sin reescribir la interfaz."), PageBreak()]

# Page 6
story += [P("Evidencias y validaciones", h1), P("La Figura 1 muestra la pantalla de bienvenida disponible como evidencia visual del prototipo. La imagen se mantiene compacta y no representa una prueba de ejecución Android. Para esa verificación se requiere un dispositivo físico o un emulador configurado.")]
img = Image(str(EVIDENCE), width=1.45*inch, height=3.14*inch)
img.hAlign = "CENTER"
story += [img, P("Figura 1<br/>Pantalla de bienvenida del prototipo", caption), P("Las validaciones registradas indican que flutter analyze finalizó sin incidencias y que flutter test aprobó una prueba de navegación. En cambio, no se verificó una ejecución Android porque el JDK del entorno estaba incompleto y no existía un emulador Android configurado. Por esta razón, el informe distingue entre las pruebas aprobadas y las evidencias pendientes.", body_noindent), PageBreak()]

# Page 7
story += [P("Limitaciones y trabajo pendiente", h1), P("La principal limitación actual es de entorno. Para completar la validación se debe instalar o reparar un JDK 17 o superior, configurar Flutter con esa ruta y crear un dispositivo virtual Android o conectar un teléfono con depuración USB. Después se debe ejecutar la aplicación, verificar la navegación y conservar una captura auténtica del resultado."), P("También se debe ejecutar la configuración de Supabase con la URL y la clave pública en tiempo de ejecución. La clave secreta o service_role no debe incorporarse al cliente Flutter. Una vez que la conexión esté validada, el equipo podrá comprobar la lectura remota del catálogo y el registro de consultas y reservas."), P("Conclusiones", h1), P("Brasas del Oriente cuenta con un avance funcional de MVP que cubre las interacciones principales del usuario: conocer la oferta, realizar una consulta y solicitar una reserva. Flutter resultó adecuado para el alcance académico por su base de código compartida. El siguiente hito consiste en validar el flujo completo en Android y con Supabase antes de ampliar el alcance del sistema."), PageBreak()]

# Page 8
story += [P("Referencias", h1)]
for item in [
    "Apple. (s. f.). <i>SwiftUI</i>. Recuperado el 8 de noviembre de 2026, de https://developer.apple.com/swiftui/",
    "Corti, N. (2024, 25 de junio). <i>Use a framework to build React Native apps</i>. React Native. https://reactnative.dev/blog/2024/06/25/use-a-framework-to-build-react-native-apps",
    "Flutter. (s. f.-a). <i>FAQ</i>. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/resources/faq",
    "Flutter. (s. f.-b). <i>Flutter performance profiling</i>. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/perf/ui-performance",
    "Google. (s. f.). <i>Develop for Android</i>. https://developer.android.com/develop",
    "Meta. (s. f.). <i>Platform-specific code</i>. React Native. https://reactnative.dev/docs/platform-specific-code.html",
]: story.append(P(item, ref))

OUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=MARGIN, leftMargin=MARGIN, topMargin=0.85*inch, bottomMargin=0.8*inch)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
