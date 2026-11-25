from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image

ROOT = Path(r"C:\Users\Usuario\Desktop\actividad_1")
OUT = ROOT / "entregables" / "informe_avance_brasas_apa7_extenso_con_capturas.pdf"
WELCOME = ROOT / "evidencias" / "captura_bienvenida_presentacion.png"
HOME = ROOT / "evidencias" / "captura_menu_principal.png"
CONSULT = ROOT / "evidencias" / "captura_consulta.png"
RESERVE = ROOT / "evidencias" / "captura_reserva.png"
W, H = letter; M = inch
base = dict(fontName="Times-Roman", fontSize=12, leading=24, textColor=colors.black)
ss = getSampleStyleSheet()
title = ParagraphStyle("title", parent=ss["Normal"], alignment=TA_CENTER, spaceAfter=18, **base)
h1 = ParagraphStyle("h1", parent=ss["Normal"], alignment=TA_CENTER, spaceBefore=10, spaceAfter=6, fontName="Times-Bold", fontSize=12, leading=24, textColor=colors.black)
h2 = ParagraphStyle("h2", parent=ss["Normal"], alignment=TA_LEFT, spaceBefore=10, spaceAfter=6, fontName="Times-Bold", fontSize=12, leading=24, textColor=colors.black)
body = ParagraphStyle("body", parent=ss["Normal"], firstLineIndent=0.5*inch, spaceAfter=0, **base)
plain = ParagraphStyle("plain", parent=ss["Normal"], spaceAfter=0, **base)
toc = ParagraphStyle("toc", parent=ss["Normal"], fontName="Times-Roman", fontSize=12, leading=18, spaceAfter=3)
caption = ParagraphStyle("caption", parent=ss["Normal"], alignment=TA_CENTER, fontName="Times-Italic", fontSize=11, leading=13, spaceBefore=2, spaceAfter=5)
refs = ParagraphStyle("refs", parent=ss["Normal"], leftIndent=0.5*inch, firstLineIndent=-0.5*inch, **base)
tablecap = ParagraphStyle("tablecap", parent=ss["Normal"], fontName="Times-Italic", fontSize=12, leading=18, spaceBefore=6, spaceAfter=3)
def P(t, st=body): return Paragraph(t, st)
def page(canvas, doc):
    canvas.saveState(); canvas.setFont("Times-Roman",12); canvas.drawRightString(W-M,H-.55*inch,str(doc.page)); canvas.restoreState()
def figure(path, label):
    i = Image(str(path), width=1.55*inch, height=3.36*inch); i.hAlign="CENTER"
    return [i, P(label,caption)]
story=[]

# 1
story += [P("Informe de avance del MVP móvil Brasas del Oriente",title),P("Resumen",h1),P("Este informe describe el avance de Brasas del Oriente, un producto mínimo viable desarrollado para la asignatura de Aplicaciones Móviles I. El proyecto propone una aplicación Flutter para una churrasquería local de Santa Cruz de la Sierra. El MVP integra una pantalla de bienvenida, un menú digital con búsqueda y filtros, formularios para consultas y reservas, y una sección de ubicación y horarios. La solución también incorpora una capa de servicios y una configuración preparada para Supabase. Se verificaron el análisis estático y una prueba automatizada de navegación. La ejecución final en Android y la conexión real con Supabase continúan pendientes de una validación de entorno.",plain),P("<i>Palabras clave:</i> Flutter, aplicación móvil, catálogo digital, reserva, Supabase.",plain),PageBreak()]

# 2 index
story += [P("Índice",h1)]
for n,pag in [("Introducción",3),("Planteamiento del problema",3),("Objetivos y alcance",4),("Metodología y selección tecnológica",5),("Diseño de la solución",6),("Evidencia de interfaz de bienvenida",7),("Evidencia de menú principal",8),("Evidencia de formulario de consulta",9),("Evidencia de formulario de reserva",10),("Formularios y datos",11),("Pruebas y validaciones",12),("Limitaciones y trabajo futuro",13),("Conclusiones",13),("Referencias",14)]: story.append(P(f"{n} {'.'*52} {pag}",toc))
story.append(PageBreak())

# 3
story += [P("Introducción",h1),P("La digitalización de pequeños negocios gastronómicos requiere herramientas que sean fáciles de usar para el cliente y viables para un equipo académico con tiempo y recursos limitados. En el caso de Brasas del Oriente, el propósito es concentrar en una aplicación móvil la información que normalmente se dispersa entre redes sociales, mensajes y publicaciones individuales. El usuario debe poder identificar la propuesta del negocio, revisar su oferta y encontrar un canal para iniciar una consulta o solicitar una mesa."),P("Planteamiento del problema",h1),P("La atención basada únicamente en mensajes puede dificultar la consulta de precios, horarios o disponibilidad. Un menú digital ordenado reduce preguntas repetitivas y permite al usuario explorar las opciones antes de comunicarse. Además, un formulario de reserva reúne los datos mínimos que el negocio necesita para revisar una solicitud. El problema no se aborda como una solución comercial terminada, sino como un primer producto funcional que valida el recorrido principal del usuario."),P("Justificación",h1),P("Flutter permite construir este primer producto desde una sola base de código. La elección resulta pertinente para un prototipo académico porque facilita el mantenimiento de una interfaz coherente y permite concentrar el esfuerzo en las funciones de catálogo, consulta y reserva. La implementación también deja una base para conectar información remota cuando la configuración de backend esté lista."),PageBreak()]

# 4
story += [P("Objetivos y alcance",h1),P("El objetivo general consiste en desarrollar un MVP multiplataforma que permita conocer el menú de una churrasquería, enviar una consulta, solicitar una reserva y revisar su ubicación y horarios."),P("Objetivos específicos",h2),P("Los objetivos específicos fueron diseñar una navegación clara entre pantallas, implementar un catálogo con búsqueda y filtros, crear formularios con validación local, estructurar una capa de servicios para el acceso a datos y preparar scripts de Supabase con tablas, datos semilla y reglas de seguridad."),P("Alcance funcional",h2),P("El alcance incluye la pantalla de bienvenida, la pantalla inicial, el menú digital, la consulta, la solicitud de reserva y la ubicación. El catálogo puede operar con datos demostrativos si no se configura Supabase. La reserva solicita nombre, teléfono, fecha, hora y cantidad de personas. La consulta recoge la información necesaria para que el negocio pueda responder posteriormente."),P("Exclusiones",h2),P("El proyecto no incorpora pagos, autenticación, pedidos con carrito, confirmación automática de disponibilidad ni una administración para personal del restaurante. Estas funciones demandan reglas de negocio, seguridad y pruebas adicionales que exceden el objetivo del MVP actual."),PageBreak()]

# 5
story += [P("Metodología y selección tecnológica",h1),P("Se utilizó una comparación ponderada para escoger el framework. Las alternativas fueron Flutter, React Native y desarrollo nativo separado para Android e iOS. Los criterios fueron costo inicial y de mantenimiento, rendimiento previsto, comunidad y ecosistema, compatibilidad Android e iOS y curva de aprendizaje. Cada criterio se calificó en una escala de uno a cinco y se ponderó de acuerdo con las necesidades del caso."),P("Tabla 1<br/>Resultados de la matriz ponderada",tablecap)]
t=Table([["Alternativa","Puntaje de 100"],["Flutter","91"],["React Native","83"],["Nativo Android e iOS","66"]],colWidths=[4.5*inch,2*inch])
t.setStyle(TableStyle([("FONTNAME",(0,0),(-1,-1),"Times-Roman"),("FONTNAME",(0,0),(-1,0),"Times-Bold"),("FONTSIZE",(0,0),(-1,-1),11),("GRID",(0,0),(-1,-1),.5,colors.HexColor("#D9D9D9")),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EAEAEA")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [t,Spacer(1,10),P("Flutter obtuvo el resultado más alto. La principal razón es la posibilidad de mantener una sola base de código para Android e iOS sin renunciar a una interfaz consistente. React Native representa una alternativa válida, especialmente si el equipo domina JavaScript y React. El enfoque nativo puede ser conveniente cuando se requieren integraciones muy específicas por plataforma, aunque demanda mayor mantenimiento. La matriz orienta la decisión del proyecto y no representa un benchmark de rendimiento en dispositivos reales (Flutter, s. f.-a; Meta, s. f.)."),PageBreak()]

# 6
story += [P("Diseño de la solución",h1),P("La solución se organiza en cuatro grupos principales. Las pantallas presentan la experiencia del usuario. Los widgets reutilizables concentran elementos visuales como tarjetas y bloques informativos. Los servicios gestionan la lectura del catálogo y la escritura de reservas o consultas. Los modelos representan los datos que se muestran o se almacenan. Finalmente, la configuración de Supabase establece cómo se conectaría la aplicación con los datos remotos."),P("Flujo de navegación",h2),P("El recorrido comienza en la pantalla de bienvenida. Después de ingresar, el usuario llega a una pantalla con accesos directos. Desde allí puede abrir el menú digital, iniciar una solicitud de reserva, enviar una consulta o revisar la ubicación y los horarios. Esta secuencia evita que el usuario deba buscar funciones en menús complejos y mantiene visibles las acciones más importantes."),P("Diseño visual",h2),P("La interfaz usa una paleta cálida asociada a la parrilla y al ambiente de la churrasquería. El contraste entre fondos claros, texto oscuro y botones en color naranja prioriza la legibilidad. El proyecto utiliza Material 3 para mantener componentes de interacción consistentes, como campos de texto, botones, tarjetas y mensajes de validación."),PageBreak()]

# 7 Figure welcome
story += [P("Evidencia de interfaz de bienvenida",h1),P("La Figura 1 corresponde a una captura incluida en la presentación del proyecto. Muestra la identidad visual inicial, el nombre del negocio, el mensaje descriptivo y el botón de acceso. Esta pantalla funciona como el primer contacto del usuario con la aplicación y permite establecer la transición hacia las opciones principales.")]
story += figure(WELCOME,"Figura 1<br/>Captura de la pantalla de bienvenida del prototipo")
story += [P("La captura se incluye como evidencia de interfaz y ocupa menos de media página. No se utiliza para afirmar una validación completa en Android; la evidencia técnica de esa ejecución requiere un entorno funcional y una captura obtenida durante la prueba correspondiente.",plain),PageBreak()]

# 8 home
story += [P("Evidencia de menú principal",h1),P("La Figura 2 muestra la pantalla principal disponible en la presentación. El usuario encuentra accesos directos a Ver menú, Reservar mesa y Ubicación y horarios. La jerarquía visual ubica el banner del negocio en la parte superior y presenta las acciones como tarjetas de tamaño cómodo para la interacción táctil.")]
story += figure(HOME,"Figura 2<br/>Captura de la pantalla principal del prototipo")
story += [P("La pantalla también comunica que los datos y precios son demostrativos para fines académicos. Esta aclaración evita presentar la información del prototipo como una oferta comercial vigente y mantiene coherencia con el alcance establecido en el informe.",plain),PageBreak()]

# 9
story += [P("Evidencia de formulario de consulta",h1),P("La Figura 3 muestra el formulario destinado a registrar consultas. La interfaz solicita el nombre, el teléfono boliviano y un mensaje. El botón de envío permanece visible al final de la pantalla, de manera que el usuario puede completar el recorrido sin cambiar de sección. La captura también evidencia el mensaje de confirmación mostrado después de procesar una consulta." )]
story += figure(CONSULT,"Figura 3<br/>Captura del formulario de consulta y mensaje de confirmación")
story += [P("Esta evidencia respalda la separación entre consultas generales y solicitudes de mesa. El formulario contribuye a que el negocio reciba datos mínimos para responder, mientras que las validaciones reducen el riesgo de registros vacíos o incompletos.",plain),PageBreak()]

# 10
story += [P("Evidencia de formulario de reserva",h1),P("La Figura 4 corresponde al flujo de reserva. La pantalla solicita el nombre del cliente, teléfono, fecha, hora y cantidad de personas. El texto de apoyo aclara que la confirmación final depende de la disponibilidad del restaurante. Esta condición es importante porque el MVP registra una solicitud y no promete una reserva definitiva sin revisión posterior." )]
story += figure(RESERVE,"Figura 4<br/>Captura del formulario de reserva con datos de prueba")
story += [P("La captura contiene datos de prueba utilizados para mostrar el comportamiento del formulario. La aplicación valida el formato del teléfono y exige que la fecha y la hora sean futuras. Por ello, la interfaz comunica tanto la solicitud como el límite operativo de la funcionalidad.",plain),PageBreak()]

# 11
story += [P("Formularios y datos",h1),P("El formulario de reserva solicita nombre, teléfono boliviano, fecha, hora y cantidad de personas. Antes de enviar la solicitud, la aplicación comprueba que los campos requeridos estén completos, que el número telefónico tenga el formato esperado y que la fecha y hora seleccionadas sean futuras. Si existe un error, se muestra un mensaje claro para orientar la corrección."),P("Gestión de consultas",h2),P("La pantalla de consulta ofrece un canal para preguntas que no se resuelven en el menú. La validación evita que se envíen registros vacíos o incompletos. Esta función separa las consultas generales de las solicitudes de reserva, lo cual favorece una organización posterior de la información cuando el backend esté conectado."),P("Integración con Supabase",h2),P("El repositorio incluye scripts para crear tablas, aplicar reglas de seguridad de acceso por fila y cargar datos semilla. La aplicación recibe la URL y la clave pública mediante variables de ejecución. La clave secreta o service_role no se almacena en el cliente móvil. Mientras la configuración no exista, el catálogo utiliza datos locales, de modo que el diseño y la navegación se pueden evaluar sin exponer credenciales."),PageBreak()]

# 12
story += [P("Pruebas y validaciones",h1),P("Las validaciones registradas se orientaron a comprobar la calidad del código y el recorrido básico de navegación. El comando flutter analyze no reportó incidencias. El comando flutter test aprobó una prueba que verifica la navegación desde el botón principal hacia la pantalla de negocios destacados. Estas pruebas aportan evidencia sobre la estructura del proyecto, pero no sustituyen una prueba manual completa en un dispositivo móvil."),P("Tabla 2<br/>Resultados documentados de verificación",tablecap)]
t2=Table([["Verificación","Resultado"],["dart format lib test","Correcto; sin cambios pendientes"],["flutter analyze","Correcto; sin incidencias"],["flutter test","Correcto; una prueba aprobada"],["Dispositivo Android","Pendiente; no había emulador configurado"]],colWidths=[2.6*inch,3.9*inch])
t2.setStyle(TableStyle([("FONTNAME",(0,0),(-1,-1),"Times-Roman"),("FONTNAME",(0,0),(-1,0),"Times-Bold"),("FONTSIZE",(0,0),(-1,-1),11),("GRID",(0,0),(-1,-1),.5,colors.HexColor("#D9D9D9")),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EAEAEA")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [t2,Spacer(1,10),P("El resultado permite afirmar que el código fue formateado, analizado y probado en el alcance indicado. No permite afirmar que el flujo completo fue ejecutado en Android ni que se conectó con Supabase en producción. Mantener esta distinción ayuda a comunicar el avance con precisión.",plain),PageBreak()]

# 13
story += [P("Limitaciones y trabajo futuro",h1),P("La principal limitación es el entorno de ejecución Android. El diagnóstico documentó un problema con la instalación de Java y la ausencia de un dispositivo Android o AVD configurado. Para continuar se debe instalar o reparar un JDK 17 o superior, indicar la ruta correcta a Flutter y crear un emulador o conectar un teléfono con depuración USB. Después se debe ejecutar el proyecto y guardar una captura auténtica de cada flujo validado."),P("También se debe realizar la configuración de Supabase con valores públicos de ejecución y ejecutar los scripts SQL en el orden documentado. La siguiente verificación debe comprobar la carga remota del catálogo, el registro de una consulta y el envío de una solicitud de reserva. Una fase posterior podría evaluar autenticación, pagos y confirmación de disponibilidad, siempre que se definan reglas de seguridad y criterios de prueba."),P("Conclusiones",h1),P("Brasas del Oriente presenta un avance funcional alineado con el objetivo de un MVP académico. La aplicación ya estructura el acceso al menú, las consultas, las reservas y la información del negocio. Flutter fue una elección adecuada para el alcance propuesto, porque facilita una interfaz común y un desarrollo centralizado. El siguiente hito es transformar las pantallas y pruebas locales en una demostración verificada en Android y con datos reales de Supabase."),PageBreak()]

# 14
story += [P("Referencias",h1)]
for item in ["Apple. (s. f.). <i>SwiftUI</i>. Recuperado el 8 de noviembre de 2026, de https://developer.apple.com/swiftui/","Corti, N. (2024, 25 de junio). <i>Use a framework to build React Native apps</i>. React Native. https://reactnative.dev/blog/2024/06/25/use-a-framework-to-build-react-native-apps","Flutter. (s. f.-a). <i>FAQ</i>. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/resources/faq","Flutter. (s. f.-b). <i>Flutter performance profiling</i>. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/perf/ui-performance","Google. (s. f.). <i>Develop for Android</i>. https://developer.android.com/develop","Meta. (s. f.). <i>Platform-specific code</i>. React Native. https://reactnative.dev/docs/platform-specific-code.html"]: story.append(P(item,refs))

OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=letter,leftMargin=M,rightMargin=M,topMargin=.85*inch,bottomMargin=.8*inch).build(story,onFirstPage=page,onLaterPages=page)
print(OUT)
