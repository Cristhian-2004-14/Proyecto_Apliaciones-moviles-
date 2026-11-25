"""Informe APA 7 de Brasas del Oriente.

Primera página deliberadamente en blanco para portada manual del estudiante.
"""
from pathlib import Path

from PIL import Image
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ROOT = Path(r"C:\Users\Usuario\Desktop\actividad_1")
DESKTOP = Path(r"C:\Users\Usuario\Desktop")
OUT = ROOT / "entregables" / "Documentacion_Final_Consolidada"
ASSETS = ROOT / "informe" / "capturas_apa7"
DATE = "25 de noviembre de 2026"

SOURCE_IMAGES = {
    "inicio": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.31.jpeg",
    "catalogo": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.32.jpeg",
    "voz": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.32 (1).jpeg",
    "carrito": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.32 (2).jpeg",
    "pedidos": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.33 (1).jpeg",
    "comprobante": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.33 (3).jpeg",
    "reserva": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.36 (2).jpeg",
    "estado_reserva": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.34 (1).jpeg",
    "ubicacion": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.36 (1).jpeg",
}


def prepare_images():
    ASSETS.mkdir(parents=True, exist_ok=True)
    images = {}
    for key, source in SOURCE_IMAGES.items():
        target = ASSETS / f"{key}.jpg"
        with Image.open(source) as image:
            image.convert("RGB").save(target, "JPEG", quality=87, optimize=True)
        images[key] = target
    return images


def set_cell_shading(cell, color="F2F2F2"):
    props = cell._tc.get_or_add_tcPr()
    element = OxmlElement("w:shd")
    element.set(qn("w:fill"), color)
    props.append(element)


def set_cell_borders(table):
    props = table._tbl.tblPr
    borders = props.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        props.append(borders)
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge = borders.find(qn(f"w:{side}"))
        if edge is None:
            edge = OxmlElement(f"w:{side}")
            borders.append(edge)
        edge.set(qn("w:val"), "single")
        edge.set(qn("w:sz"), "4")
        edge.set(qn("w:color"), "BFBFBF")


def add_toc_field(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = ' TOC \\o "1-2" \\h \\z \\u '
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Actualice el índice en Word con Ctrl+A y F9."
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, placeholder, end])


def configure(doc):
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 2
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.first_line_indent = Inches(0.5)
    for style_name in ("Heading 1", "Heading 2"):
        style = doc.styles[style_name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        style.font.size = Pt(12)
        style.font.bold = True
        style.font.color.rgb = None
        style.paragraph_format.line_spacing = 2
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(0)
        style.paragraph_format.first_line_indent = Inches(0)
    doc.styles["Heading 1"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.styles["Heading 2"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    doc.core_properties.title = "Informe final del proyecto Brasas del Oriente"
    doc.core_properties.author = "Equipo de desarrollo del proyecto"


def title(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.line_spacing = 2
    paragraph.paragraph_format.first_line_indent = Inches(0)
    run = paragraph.add_run(text)
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)


def body(doc, text):
    paragraph = doc.add_paragraph(text)
    paragraph.paragraph_format.line_spacing = 2
    paragraph.paragraph_format.first_line_indent = Inches(0.5)
    return paragraph


def heading(doc, text, level=1):
    return doc.add_paragraph(text, style=f"Heading {level}")


def table(doc, headers, rows, widths=None):
    result = doc.add_table(rows=1, cols=len(headers))
    result.alignment = WD_TABLE_ALIGNMENT.CENTER
    result.style = "Table Grid"
    set_cell_borders(result)
    for i, header in enumerate(headers):
        cell = result.rows[0].cells[i]
        cell.text = header
        set_cell_shading(cell, "D9EAD3")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
    for index, row in enumerate(rows):
        cells = result.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = value
            cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if index % 2:
                set_cell_shading(cells[i], "FAFAFA")
            for paragraph in cells[i].paragraphs:
                paragraph.paragraph_format.line_spacing = 1.15
                paragraph.paragraph_format.first_line_indent = Inches(0)
                for run in paragraph.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)
    if widths:
        for row in result.rows:
            for cell, width in zip(row.cells, widths):
                cell.width = Inches(width)
    doc.add_paragraph()
    return result


def figures(doc, entries):
    layout = doc.add_table(rows=1, cols=len(entries))
    layout.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell, (number, caption, image_path) in zip(layout.rows[0].cells, entries):
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.add_run().add_picture(str(image_path), width=Inches(1.55))
        c = cell.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraph_format.first_line_indent = Inches(0)
        c.add_run(f"Figura {number}. ").bold = True
        title_run = c.add_run(caption)
        title_run.italic = True
        note = cell.add_paragraph("Nota. Captura propia de las pruebas del proyecto.")
        note.alignment = WD_ALIGN_PARAGRAPH.CENTER
        note.paragraph_format.first_line_indent = Inches(0)
        for run in note.runs:
            run.italic = True
            run.font.size = Pt(9)
    doc.add_paragraph()


def create_report():
    images = prepare_images()
    doc = Document()
    configure(doc)
    # Hoja 1 vacía destinada a portada manual.
    doc.add_page_break()
    heading(doc, "Índice")
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.first_line_indent = Inches(0)
    add_toc_field(paragraph)
    doc.add_page_break()
    title(doc, "Informe final del proyecto Brasas del Oriente")
    body(doc, "Este informe documenta el desarrollo, la configuración, la validación y los resultados del producto mínimo viable Brasas del Oriente. El proyecto se elaboró como una aplicación móvil para centralizar el catálogo, los pedidos, las reservas, las consultas, la información de ubicación y las funciones operativas del dueño. El documento organiza el alcance alcanzado, las decisiones de implementación y la evidencia utilizada para la aceptación del sistema.")
    heading(doc, "Descripción del proyecto")
    body(doc, "Brasas del Oriente es una aplicación móvil desarrollada con Flutter para apoyar la atención de una churrasquería en Santa Cruz de la Sierra. La solución digital permite que una persona cliente consulte la oferta sin depender de mensajes dispersos y que una persona dueña gestione las solicitudes relacionadas con la operación cotidiana.")
    heading(doc, "Objetivo general")
    body(doc, "Construir un producto mínimo viable que permita a los clientes explorar el menú, solicitar pedidos o reservas y revisar sus estados, mientras el dueño administra fotografías, reservas y comprobantes de pago desde una vista autorizada.")
    heading(doc, "Objetivos específicos")
    table(doc, ["Código", "Objetivo específico"], [
        ("OE 01", "Digitalizar la consulta del menú mediante categorías, precios, descripciones e imágenes."),
        ("OE 02", "Permitir la construcción y el registro de pedidos desde un carrito."),
        ("OE 03", "Registrar reservas y comunicar los estados en espera, confirmado o rechazado."),
        ("OE 04", "Apoyar la revisión de pagos mediante comprobantes adjuntos y contraste manual."),
        ("OE 05", "Brindar al dueño herramientas básicas de gestión de contenido y solicitudes."),
    ], [1.0, 5.5])
    heading(doc, "Alcance del producto mínimo viable")
    body(doc, "El alcance se concentró en un recorrido de cliente y un recorrido de dueño. El cliente puede navegar por el catálogo, usar búsqueda escrita o por voz, agregar productos al carrito, registrar un pedido, adjuntar un comprobante de demostración, solicitar una reserva, enviar una consulta y revisar datos de ubicación. El dueño puede administrar fotos, gestionar reservas y revisar pagos con una decisión explícita de confirmar o rechazar.")
    table(doc, ["Rol", "Necesidad", "Función entregada"], [
        ("Cliente", "Conocer la oferta", "Catálogo, categorías, fotos, precios y búsqueda."),
        ("Cliente", "Solicitar atención", "Carrito, pedido, comprobante, reserva y consulta."),
        ("Cliente", "Conocer resultados", "Historial de pedidos y reservas con estados."),
        ("Dueño", "Gestionar operación", "Fotos, reservas y comprobantes en revisión."),
    ], [1.0, 2.0, 3.5])
    figures(doc, [("1", "Catálogo del menú digital", images["catalogo"]), ("2", "Historial de pedidos", images["pedidos"])])
    heading(doc, "Requisitos funcionales")
    table(doc, ["Código", "Requisito", "Resultado esperado"], [
        ("RF 01", "Mostrar catálogo", "Productos, categorías, imágenes, precios y descripciones visibles."),
        ("RF 02", "Buscar productos", "Filtro escrito y búsqueda por voz cuando el permiso está disponible."),
        ("RF 03", "Gestionar carrito", "Agregar, quitar, calcular cantidades y total."),
        ("RF 04", "Registrar pedido", "Solicitud persistente con estado inicial en espera."),
        ("RF 05", "Registrar reserva", "Fecha, hora, personas y estado inicial en espera."),
        ("RF 06", "Mostrar historial", "Estados de pedidos y reservas visibles al cliente."),
        ("RF 07", "Gestionar operación", "El dueño acepta o deniega reservas y revisa pagos."),
        ("RF 08", "Gestionar fotos", "El dueño puede cargar o reemplazar imágenes de productos."),
    ], [0.7, 2.4, 3.4])
    heading(doc, "Requisitos no funcionales")
    body(doc, "El sistema se desarrolló para ejecutarse en Android mediante una APK de Flutter. Requiere conectividad para los servicios de Supabase, clima y mapas, y solicita permisos de micrófono solamente cuando se usa búsqueda por voz. La persistencia se delega a Supabase para que pedidos, reservas, perfiles y archivos puedan recuperarse después de navegar o reiniciar la aplicación.")
    table(doc, ["Categoría", "Aplicación en el proyecto"], [
        ("Usabilidad", "Etiquetas claras, botones visibles y mensajes de estado en los recorridos principales."),
        ("Seguridad", "Autenticación, perfiles, roles y políticas de seguridad por fila."),
        ("Compatibilidad", "Ejecución en emulador y dispositivos Android compatibles con Flutter."),
        ("Mantenibilidad", "Separación entre pantallas, servicios y modelos del proyecto."),
    ], [1.5, 5.0])
    heading(doc, "Historias de usuario")
    table(doc, ["Código", "Historia", "Criterio de aceptación"], [
        ("HU C01", "Como cliente quiero ver el menú para conocer productos y precios.", "Puedo ver categorías, productos y datos de cada producto."),
        ("HU C02", "Como cliente quiero armar un pedido para solicitar productos.", "El carrito calcula el total y permite registrar el pedido."),
        ("HU C03", "Como cliente quiero revisar estados para conocer el resultado.", "Veo pedido en espera, confirmado o rechazado."),
        ("HU C04", "Como cliente quiero reservar una mesa para solicitar disponibilidad.", "La reserva se almacena y muestra su estado."),
        ("HU D01", "Como dueño quiero gestionar reservas para atender solicitudes.", "Puedo aceptar o denegar las reservas pendientes."),
        ("HU D02", "Como dueño quiero revisar pagos para contrastar comprobantes.", "Puedo confirmar o rechazar después de revisar el abono."),
    ], [0.8, 3.1, 2.6])
    heading(doc, "Tecnologías e integraciones")
    body(doc, "Flutter se utilizó para la interfaz móvil, la navegación, los formularios y la gestión del carrito. Supabase se utilizó para la autenticación, los perfiles, la base de datos, las políticas de seguridad y el almacenamiento de archivos. Supabase Storage concentra fotos de productos, portada y comprobantes. Como servicios complementarios se emplean Open Meteo para clima, OpenStreetMap para ubicación y reconocimiento de voz provisto por el dispositivo.")
    table(doc, ["Tecnología", "Responsabilidad"], [
        ("Flutter", "Interfaz, navegación, validaciones y visualización de estados."),
        ("Supabase Auth", "Registro, inicio de sesión e identidad del usuario."),
        ("Supabase Database", "Perfiles, productos, pedidos, reservas y estados."),
        ("Supabase Storage", "Imágenes de productos y comprobantes adjuntos."),
        ("Servicios externos", "Clima, mapa y asistencia de búsqueda por voz."),
    ], [2.0, 4.5])
    heading(doc, "Arquitectura funcional")
    body(doc, "La capa de presentación reúne las pantallas que utiliza cada rol. La capa de lógica controla el carrito, los cálculos, las validaciones de formularios y las transiciones de estado. La capa de datos comunica la aplicación con Supabase. Esta estructura permite que la aplicación muestre información actualizada sin mezclar la interfaz con el acceso directo a la base de datos.")
    table(doc, ["Capa", "Responsabilidad", "Resultado"], [
        ("Presentación", "Pantallas, botones, formularios y mensajes.", "Interacción móvil clara."),
        ("Lógica", "Carrito, totales, validaciones y cambios de estado.", "Flujos coherentes."),
        ("Datos", "Autenticación, consultas, archivos y persistencia.", "Información recuperable."),
        ("Servicios", "Clima, mapa y reconocimiento de voz.", "Información contextual."),
    ], [1.2, 3.4, 1.9])
    heading(doc, "Modelo de datos y estados")
    body(doc, "La información se vincula a una cuenta autenticada mediante el perfil del usuario. Un pedido tiene detalles de producto, monto y estado; el pago asociado puede quedar en revisión manual, pagado o rechazado. Una reserva tiene fecha, hora, cantidad de personas y estado. La aplicación comunica En espera, Confirmado y Rechazado en el historial del cliente para que pueda conocer el avance de la solicitud.")
    table(doc, ["Entidad", "Propósito", "Relación"], [
        ("Perfil", "Identificar usuario y rol.", "Relaciona pedidos y reservas."),
        ("Producto", "Representar ítems del menú.", "Se incluye en el detalle de pedido."),
        ("Pedido", "Registrar solicitud y total.", "Contiene detalles y pago."),
        ("Reserva", "Registrar solicitud de mesa.", "Pertenece a un usuario."),
        ("Comprobante", "Aportar evidencia documental.", "Se relaciona con un pedido."),
    ], [1.4, 2.75, 2.35])
    figures(doc, [("3", "Búsqueda por voz", images["voz"]), ("4", "Carrito de compra", images["carrito"])])
    heading(doc, "Seguridad y roles")
    body(doc, "La aplicación separa las capacidades de cliente y dueño. Una cuenta creada desde el registro obtiene el comportamiento de cliente; la asignación de dueño se realiza de manera autorizada. Las políticas de seguridad por fila limitan la lectura y modificación de datos, de modo que la persona cliente ve sus propios pedidos y reservas, mientras que el dueño accede a las operaciones administrativas necesarias.")
    body(doc, "Las claves de configuración de Supabase se aplican durante la compilación o la ejecución de la aplicación. No forman parte del informe, de las capturas ni de los archivos que se comparten públicamente. Este criterio reduce el riesgo de que información de configuración se use fuera del contexto del proyecto.")
    heading(doc, "Gestión de fotografías")
    body(doc, "El dueño puede administrar fotografías de productos desde su cuenta. Las imágenes se cargan a un bucket de Supabase Storage y la referencia guardada permite que el catálogo muestre el contenido actualizado. Durante la versión final se validó el bucket requerido y se corrigió la actualización de estado posterior a la carga de una imagen para evitar errores asíncronos en Flutter.")
    heading(doc, "Pago QR con revisión manual")
    body(doc, "La alternativa de pago implementada muestra el monto exacto de un pedido, permite adjuntar una imagen de comprobante y envía el resultado a revisión manual. La pantalla de verificación presenta datos comparativos disponibles, como monto esperado, destino, fecha o referencia, para facilitar la revisión del dueño.")
    body(doc, "No se integró una pasarela bancaria oficial porque dicha integración requiere un contrato con la entidad financiera, credenciales empresariales, controles de seguridad y autorización operativa. Además, una lectura OCR o una imagen no certifica por sí sola que el dinero ingresó. Por ese motivo, el dueño confirma el estado solamente después de constatar el movimiento real.")
    figures(doc, [("5", "Adjuntar comprobante", images["comprobante"]), ("6", "Estado de reserva", images["estado_reserva"])])
    heading(doc, "Recorrido de cliente")
    body(doc, "El recorrido principal empieza al abrir la aplicación y entrar a la churrasquería. El cliente puede abrir el menú, filtrar por categoría o buscar un producto, agregar productos al carrito y revisar el total. Después completa sus datos de contacto para registrar el pedido. El sistema lo muestra inicialmente en espera mientras el negocio revisa el pedido y el comprobante adjunto.")
    body(doc, "El cliente también puede solicitar una reserva. Para ello registra su nombre, teléfono, fecha, hora y número de personas. La reserva inicia en espera y, luego de la decisión del dueño, el historial muestra si fue confirmada o rechazada. Ubicación y horarios complementan el recorrido con información de contacto, clima y acciones de mapa.")
    heading(doc, "Recorrido de dueño")
    body(doc, "El dueño inicia sesión con la cuenta autorizada y accede a Mi cuenta. Desde allí puede entrar al panel operativo, gestionar fotografías, revisar las reservas registradas y revisar los comprobantes de pago. Las listas priorizan las solicitudes pendientes y muestran acciones explícitas para aceptar, denegar, confirmar o rechazar.")
    body(doc, "Para una reserva, el dueño consulta fecha, hora y cantidad de personas antes de tomar una decisión. Para un pago, contrasta el monto del pedido con la información disponible del comprobante y registra la confirmación o el rechazo. El resultado se persiste y posteriormente es visible para la cuenta cliente en el historial.")
    figures(doc, [("7", "Formulario de reserva", images["reserva"]), ("8", "Ubicación y horarios", images["ubicacion"])])
    heading(doc, "Pruebas realizadas")
    body(doc, "La calidad del MVP se revisó con análisis estático, pruebas automatizadas disponibles y recorridos manuales. flutter analyze permite identificar problemas de código antes de ejecutar la aplicación. flutter test cubre los casos implementados en el repositorio. Los recorridos manuales validan lo que la persona usuaria observa en Android y confirman la persistencia de la información entre las pantallas.")
    table(doc, ["Tipo", "Propósito", "Resultado esperado"], [
        ("Análisis estático", "Revisar problemas en código Dart.", "Sin incidencias críticas."),
        ("Pruebas automatizadas", "Validar lógica y widgets disponibles.", "Casos ejecutados correctamente."),
        ("Pruebas funcionales", "Recorrer módulos del MVP.", "Resultado coherente en interfaz y datos."),
        ("UAT", "Aceptar el flujo completo de cliente y dueño.", "Sin defectos bloqueantes."),
    ], [1.45, 2.55, 2.85])
    heading(doc, "Resultados de pruebas")
    table(doc, ["Módulo", "Resultado validado", "Evidencia"], [
        ("Catálogo", "Productos, fotos, precios, categorías y búsqueda.", "Capturas del menú digital."),
        ("Carrito", "Cantidades, total y confirmación de pedido.", "Captura del carrito."),
        ("Pedidos", "Estados En espera, Confirmado y Rechazado.", "Historial del cliente."),
        ("Reservas", "Solicitud y estado posterior a gestión.", "Formulario e historial."),
        ("Comprobantes", "Archivo seleccionado y enviado a revisión.", "Pantalla de adjuntar."),
        ("Ubicación", "Horario, contacto, clima y acciones.", "Pantalla informativa."),
    ], [1.4, 3.5, 1.95])
    heading(doc, "Pruebas de aceptación UAT")
    body(doc, "El protocolo UAT complementario presenta una guía de aceptación completa. El recorrido contiene doce pasos: iniciar la aplicación, explorar el catálogo, probar voz, construir el carrito, registrar el pedido, adjuntar un comprobante de demostración, revisar el pago como dueño, consultar el estado del pedido, crear una reserva, gestionarla como dueño, actualizar fotos y consultar la información final. El acta permite registrar resultado, observaciones, nombre de la persona revisora y firma.")
    heading(doc, "Bitácora de evolución")
    table(doc, ["Actividad", "Resultado de la versión final"], [
        ("Configuración", "Conexión entre Flutter, Supabase Auth, base de datos y Storage."),
        ("Autenticación", "Inicio de sesión, registro y perfiles con roles diferenciados."),
        ("Fotografías", "Carga de imágenes de productos y actualización del catálogo."),
        ("Estados", "Historial con pedidos en espera, confirmados o rechazados."),
        ("Reservas", "Gestión por dueño y visibilidad del resultado para cliente."),
        ("Pagos", "Comprobante con contraste de campos para revisión manual."),
        ("Interfaz", "Corrección de desbordes visuales en productos del menú."),
    ], [2.0, 4.8])
    heading(doc, "Despliegue de la aplicación")
    body(doc, "Para pruebas locales se ejecuta la aplicación desde Android Studio o la terminal con Flutter, seleccionando un emulador o teléfono con depuración USB. Para compartir una copia se genera una APK de depuración o de distribución. La compilación debe recibir la configuración pública de Supabase definida para el proyecto; sin ella, la autenticación, los datos y el almacenamiento no podrán conectarse.")
    table(doc, ["Elemento", "Mínimo", "Recomendado"], [
        ("Dispositivo", "Android compatible con Flutter.", "Android actualizado."),
        ("Memoria", "Capacidad para instalar la APK.", "4 GB de RAM o más."),
        ("Conectividad", "Internet para servicios remotos.", "Wi-Fi o datos estables."),
        ("Permisos", "Archivos y micrófono cuando se usan.", "Permisos concedidos en UAT."),
    ], [1.4, 2.55, 2.85])
    heading(doc, "Limitaciones y mejoras futuras")
    body(doc, "El producto se entrega como un MVP académico. Las funciones de voz, clima y mapas dependen de conectividad, permisos y disponibilidad de servicios externos. El pago por QR conserva revisión manual y no sustituye una pasarela financiera certificada. Para una siguiente fase se recomienda integrar notificaciones, trazabilidad de auditoría, pasarela autorizada, panel de métricas, mayor cobertura de pruebas y evaluaciones con más usuarios.")
    heading(doc, "Conclusiones")
    body(doc, "Brasas del Oriente integra en una misma aplicación las funciones principales de consulta, pedido, reserva, seguimiento y administración básica. El cliente obtiene un recorrido claro para conocer la oferta y solicitar atención. El dueño dispone de acciones diferenciadas para gestionar el contenido, las reservas y la revisión de pagos. La persistencia de datos y la visualización de estados permiten que ambas partes conozcan el avance de cada operación.")
    body(doc, "La solución cumple el alcance definido para un MVP y establece una base técnica para ampliaciones posteriores. La aceptación definitiva se apoya en el protocolo UAT y el registro de pruebas que acompañan este informe. La revisión manual de pagos es una decisión responsable para el alcance actual porque evita que un comprobante documental sea tomado como confirmación bancaria automática.")
    heading(doc, "Referencias")
    for reference in [
        "Flutter. (2026). Flutter documentation. https://docs.flutter.dev/",
        "Open Meteo. (2026). Weather API. https://open-meteo.com/",
        "OpenStreetMap. (2026). OpenStreetMap. https://www.openstreetmap.org/",
        "Supabase. (2026). Supabase documentation. https://supabase.com/docs",
    ]:
        paragraph = doc.add_paragraph(reference)
        paragraph.paragraph_format.first_line_indent = Inches(-0.5)
        paragraph.paragraph_format.left_indent = Inches(0.5)
        paragraph.paragraph_format.line_spacing = 2
    doc.add_page_break()
    heading(doc, "Anexo A Evidencias del catálogo y del carrito")
    figures(doc, [("A1", "Catálogo de productos", images["catalogo"]), ("A2", "Carrito y total", images["carrito"])])
    heading(doc, "Anexo B Evidencias de estados y comprobantes")
    figures(doc, [("B1", "Historial de pedidos", images["pedidos"]), ("B2", "Carga de comprobante", images["comprobante"])])
    heading(doc, "Anexo C Evidencias de reservas e información")
    figures(doc, [("C1", "Reserva de mesa", images["reserva"]), ("C2", "Ubicación y horarios", images["ubicacion"])])
    path = OUT / "03_Informe_Final_Brasas_del_Oriente_APA7.docx"
    doc.save(path)
    return path


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(create_report())
