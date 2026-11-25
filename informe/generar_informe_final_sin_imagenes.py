from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "entregables" / "Informe_final_Brasas_del_Oriente_QA_UAT.docx"


def font(run, size=12, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def field(run, instruction, placeholder="1"):
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    code = OxmlElement("w:instrText")
    code.set(qn("xml:space"), "preserve")
    code.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    value = OxmlElement("w:t")
    value.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, code, separate, value, end])


def set_cell_shading(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color)
    tc_pr.append(shd)


def set_cell_borders(cell, color="D9D9D9"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        border = borders.find(tag)
        if border is None:
            border = OxmlElement(f"w:{edge}")
            borders.append(border)
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "6")
        border.set(qn("w:color"), color)


def set_cell_margins(cell, top=90, start=100, bottom=90, end=100):
    tc_pr = cell._tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tag = OxmlElement("w:tblHeader")
    tag.set(qn("w:val"), "true")
    tr_pr.append(tag)


def paragraph(doc, text="", style="Normal", before=0, after=0, first_line=0, align=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 2
    if first_line:
        p.paragraph_format.first_line_indent = Inches(first_line)
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    font(run)
    return p


def heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before = Pt(14 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 2
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    font(run, bold=True)
    return p


def bullet(doc, text):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.line_spacing = 2
    run = p.add_run("• " + text)
    font(run)


def number(doc, n, text):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.line_spacing = 2
    run = p.add_run(f"{n}. {text}")
    font(run)


def table(doc, headers, rows, widths, font_size=10):
    result = doc.add_table(rows=1, cols=len(headers))
    result.alignment = WD_TABLE_ALIGNMENT.CENTER
    result.style = "Table Grid"
    repeat_header(result.rows[0])
    for index, value in enumerate(headers):
        cell = result.rows[0].cells[index]
        cell.width = Inches(widths[index])
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_shading(cell, "303030")
        set_cell_borders(cell)
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(value)
        font(r, size=font_size, bold=True)
        r.font.color.rgb = RGBColor(255, 255, 255)
    for row_number, row in enumerate(rows):
        cells = result.add_row().cells
        for index, value in enumerate(row):
            cell = cells[index]
            cell.width = Inches(widths[index])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_borders(cell)
            set_cell_margins(cell)
            if row_number % 2:
                set_cell_shading(cell, "F2F2F2")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(value))
            font(r, size=font_size)
    paragraph(doc, "", after=4)


def reference(doc, text):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.line_spacing = 2
    font(p.add_run(text))


def evidence_placeholder(doc, title, description):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5
    title_run = p.add_run(f"Evidencia pendiente: {title}. ")
    font(title_run, bold=True)
    font(p.add_run(description), italic=True)


def configure_document(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.5)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 2
    normal.paragraph_format.space_after = Pt(0)
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        style = styles[name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.size = Pt(12)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    header.paragraph_format.line_spacing = 1
    r = header.add_run()
    font(r)
    field(r, " PAGE ")

    settings = doc.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def landscape_section(doc):
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(11)
    section.page_height = Inches(8.5)
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)
    return section


def portrait_section(doc):
    section = doc.add_section(WD_SECTION.NEW_PAGE)
    section.orientation = WD_ORIENT.PORTRAIT
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    return section


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    configure_document(doc)

    # Portada APA 7.
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph(style="Normal")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2
    font(p.add_run("Informe final de desarrollo y validación de Brasas del Oriente"), bold=True)
    for line in [
        "Estudiante: ______________________________",
        "Universidad Privada Domingo Savio",
        "Aplicaciones Móviles I",
        "Docente: ______________________________",
        "24 de noviembre de 2026",
    ]:
        paragraph(doc, line, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # Índice funcional actualizable en Word.
    p = paragraph(doc, "Índice", align=WD_ALIGN_PARAGRAPH.CENTER)
    p.runs[0].bold = True
    toc = doc.add_paragraph()
    toc.paragraph_format.line_spacing = 1.5
    r = toc.add_run()
    font(r)
    field(r, ' TOC \\o "1-3" \\h \\z \\u ', "Actualice el índice en Word con Ctrl+A y F9.")
    paragraph(doc, "Nota. Este índice se actualiza automáticamente al abrir el documento en Word. Si no se actualiza, seleccione todo el documento con Ctrl+A y presione F9.", before=12)
    doc.add_page_break()

    heading(doc, "Introducción")
    paragraph(doc, "Brasas del Oriente es una aplicación móvil académica desarrollada con Flutter para una churrasquería de Santa Cruz de la Sierra. El proyecto integra un catálogo de productos, consultas, reservas, pedidos, cuentas con roles, servicios de ubicación y herramientas de administración para el dueño. El objetivo de la solución es centralizar interacciones que habitualmente se realizan por mensajes o medios no estructurados y convertirlas en registros consultables desde una aplicación móvil.", first_line=0.5)
    paragraph(doc, "La última versión incorpora fotografías reales de productos administradas desde Supabase Storage, búsqueda por voz, historial de pedidos y reservas para el cliente, gestión de reservas para el dueño y un flujo complementario de pago mediante QR bancario con comprobante y revisión manual. El informe describe el alcance real de cada integración, los controles aplicados, las pruebas automatizadas preparadas y las evidencias visuales que se incorporarán en la versión final.", first_line=0.5)

    heading(doc, "Planteamiento del problema")
    paragraph(doc, "La atención de un restaurante depende de información actualizada sobre su menú, disponibilidad de mesas, consultas y pedidos. Cuando esa información se distribuye por distintos canales, se vuelve más difícil para el cliente encontrar productos y para el negocio dar seguimiento a las solicitudes. También se limita la capacidad del dueño para actualizar fotografías y controlar quién puede cambiar información pública.", first_line=0.5)
    paragraph(doc, "El problema abordado consiste en construir una aplicación que permita a los clientes consultar un catálogo y registrar acciones básicas, mientras el dueño dispone de controles diferenciados para administrar contenido, pedidos, pagos documentales y reservas. La solución debe integrar servicios externos sin exponer credenciales sensibles en el dispositivo móvil.", first_line=0.5)

    heading(doc, "Objetivos")
    heading(doc, "Objetivo general", 2)
    paragraph(doc, "Desarrollar una aplicación móvil con Flutter para Brasas del Oriente que gestione el catálogo, la interacción básica con clientes y los procesos de administración del negocio mediante Supabase y servicios externos.", first_line=0.5)
    heading(doc, "Objetivos específicos", 2)
    for item in [
        "Presentar un catálogo filtrable con nombre, descripción, precio y fotografías reales de productos.",
        "Permitir el registro de consultas, reservas, pedidos y detalle de productos solicitados.",
        "Implementar autenticación y autorización con los roles cliente y dueño.",
        "Permitir al dueño administrar fotografías de portada y fotografías de productos almacenadas en la nube.",
        "Incorporar una búsqueda por voz que respete el permiso de micrófono en Android.",
        "Mostrar al cliente el historial de sus pedidos, pagos y reservas, y permitir al dueño confirmar o rechazar reservas.",
        "Implementar un flujo QR documental que requiera comprobante y constatación manual antes de declarar un pago como aprobado.",
    ]:
        bullet(doc, item)

    heading(doc, "Alcance del proyecto")
    paragraph(doc, "La aplicación se orienta a un escenario demostrativo académico. Incluye las pantallas y servicios necesarios para explorar productos, usar el carrito, registrar una consulta, solicitar una reserva, crear un pedido, consultar información del negocio y administrar funciones según el rol. El catálogo y los datos se almacenan en Supabase; los recursos de imagen se administran mediante Storage. La versión no pretende reemplazar un sistema bancario ni una pasarela comercial certificada.", first_line=0.5)
    table(doc, ["Módulo", "Usuario principal", "Resultado esperado"], [
        ["Catálogo", "Cliente", "Consulta de productos por categoría, texto o voz."],
        ["Carrito y pedido", "Cliente", "Cálculo de cantidades y registro persistente del pedido."],
        ["Reservas", "Cliente y dueño", "Solicitud, consulta de estado y confirmación o rechazo."],
        ["Fotos", "Dueño", "Carga o reemplazo de portada y fotografías de productos."],
        ["Pagos QR", "Cliente y dueño", "Comprobante privado y verificación manual del abono."],
        ["Ubicación", "Cliente", "Horarios, contacto, clima, ruta y mapa."],
    ], [1.35, 1.45, 3.7])

    heading(doc, "Metodología de desarrollo")
    paragraph(doc, "Se utilizó un enfoque incremental. Primero se definieron las pantallas, modelos de datos y validaciones. Luego se integró Supabase para autenticación, base de datos, funciones remotas y Storage. Finalmente se añadieron las integraciones complementarias de voz, fotografías, OCR, QR, historial y gestión de reservas. Cada etapa se validó con recorridos funcionales y, al cierre, se preparó una suite de pruebas automatizadas para revisar la lógica independiente de la interfaz.", first_line=0.5)

    heading(doc, "Arquitectura técnica")
    paragraph(doc, "Flutter y Dart se utilizaron para la interfaz móvil y la navegación. Supabase aporta Auth, PostgreSQL, políticas de seguridad por fila, funciones RPC y Storage. La aplicación utiliza servicios externos para clima, mapa y reconocimiento de voz; el OCR se ejecuta localmente sobre el comprobante que el cliente selecciona. Esta separación permite que las operaciones sensibles, como crear un pedido o resolver un pago, estén controladas por la base de datos o por el rol del usuario.", first_line=0.5)
    table(doc, ["Tecnología", "Aplicación", "Control o aporte"], [
        ["Flutter y Dart", "Interfaz, estado de pantallas, formularios y navegación.", "Código multiplataforma y componentes reutilizables."],
        ["Supabase Auth", "Registro e inicio de sesión.", "Identidad autenticada y perfil con rol."],
        ["PostgreSQL y RPC", "Pedidos, detalles, reservas, pagos y auditoría.", "Reglas de negocio y operaciones sensibles."],
        ["Supabase Storage", "Fotos, QR y comprobantes.", "Buckets y políticas diferenciadas por tipo de archivo."],
        ["speech_to_text", "Filtro de catálogo por voz.", "Reconocimiento dependiente de permiso y disponibilidad."],
        ["ML Kit", "Lectura documental de comprobantes.", "Extracción local de texto como apoyo."],
        ["Open Meteo y OpenStreetMap", "Clima, mapa, ruta y contacto.", "Servicios externos sin claves bancarias ni privadas."],
    ], [1.4, 2.45, 2.65])

    heading(doc, "Desarrollo funcional")
    heading(doc, "Catálogo con fotos reales y filtrado", 2)
    paragraph(doc, "El menú digital muestra productos organizados por rubro. Cada tarjeta utiliza el nombre, la descripción, el precio y la ruta de imagen asociada al producto. El diseño se ajustó para que el botón de agregar no produzca desbordamiento visual cuando existen descripciones de varias líneas. El catálogo admite filtros por categoría y búsqueda textual.", first_line=0.5)
    evidence_placeholder(doc, "Catálogo con fotografías reales", "Insertar captura del menú digital donde se vean al menos cuatro productos, precios, fotos reales y el botón para agregar al carrito.")

    heading(doc, "Búsqueda por voz", 2)
    paragraph(doc, "El botón de micrófono inicia el servicio de reconocimiento de voz y coloca el texto reconocido en el filtro del catálogo. El sistema muestra el estado de escucha y permite detenerlo. La integración requiere el permiso RECORD_AUDIO y contempla errores por permiso denegado, servicio no disponible o falta de conectividad. El comportamiento se debe evidenciar en un teléfono real.", first_line=0.5)
    evidence_placeholder(doc, "Búsqueda por voz", "Insertar captura de la pantalla Menú digital mientras se muestra Escuchando o Reconocido y el catálogo filtrado.")

    heading(doc, "Cuentas y roles", 2)
    paragraph(doc, "Las cuentas se gestionan con Supabase Auth. El perfil se guarda en la tabla perfiles y define el rol cliente o dueño. El cliente visualiza funciones de consulta, reserva, pedido e historial propio. El dueño recibe accesos adicionales para administrar fotografías, configurar QR, revisar pagos, consultar pedidos y gestionar reservas. La interfaz restringe las opciones visibles y las políticas RLS limitan el acceso a nivel de datos.", first_line=0.5)
    evidence_placeholder(doc, "Panel de cuenta del dueño", "Insertar captura de Mi cuenta donde se vean los accesos del rol dueño.")

    heading(doc, "Consultas, carrito y pedidos", 2)
    paragraph(doc, "El formulario de consulta valida nombre, teléfono y un mensaje mínimo antes de registrar la solicitud. El carrito suma productos repetidos, disminuye cantidades y calcula el total. Al confirmar el pedido, la aplicación solicita los datos necesarios y utiliza la función crear_pedido para registrar el encabezado y el detalle de los productos. El registro mantiene el pedido asociado al usuario autenticado cuando corresponde.", first_line=0.5)
    evidence_placeholder(doc, "Pedido y consulta", "Insertar una captura de la consulta enviada y otra de Mi pedido con productos, cantidades, total y acción de confirmar.")

    heading(doc, "Reservas e historial del cliente", 2)
    paragraph(doc, "Una reserva nueva se asocia al usuario autenticado y recibe inicialmente el estado solicitada. Para el usuario final el estado se presenta como En espera. Desde Mi cuenta, la pantalla Mis pedidos y reservas muestra los pedidos de la cuenta activa, el estado del pago asociado y las reservas realizadas. Los estados de reserva se comunican con texto e icono: En espera, Confirmada o Rechazada.", first_line=0.5)
    paragraph(doc, "En el rol dueño, la pantalla Gestionar reservas lista las solicitudes, muestra la información del cliente y permite aceptar o denegar la reserva después de una confirmación explícita. La actualización se persiste en Supabase y el cliente puede consultar el nuevo estado al actualizar su historial. Esta separación evita que un cliente visualice reservas pertenecientes a otra cuenta.", first_line=0.5)
    evidence_placeholder(doc, "Historial y gestión de reservas", "Insertar tres capturas: reserva En espera desde cliente, reserva Confirmada o Rechazada desde cliente y pantalla Gestionar reservas del dueño.")

    heading(doc, "Ubicación clima y contacto", 2)
    paragraph(doc, "La sección Ubicación y horarios presenta dirección, horario, contacto y accesos a llamadas, WhatsApp, rutas y mapa. El clima se consulta desde Open Meteo, se transforma desde JSON a un modelo tipado y presenta estados de carga, error y reintento. El mapa utiliza OpenStreetMap, con lo que se evita incluir una clave privada de Google Maps en el cliente móvil.", first_line=0.5)
    evidence_placeholder(doc, "Ubicación y mapa", "Insertar captura de ubicación con tarjeta de clima y captura del mapa del negocio.")

    heading(doc, "Pago QR comprobante y verificación manual")
    heading(doc, "Alcance implementado", 2)
    paragraph(doc, "El dueño configura una imagen QR autorizada y datos de referencia en Supabase. Al iniciar un pago, el cliente observa el importe exacto del pedido, escanea el QR desde su aplicación bancaria y adjunta una imagen JPG o PNG del comprobante. El comprobante se guarda en un bucket privado asociado al pago y se calcula un hash SHA 256 para apoyar la detección de reutilización.", first_line=0.5)
    paragraph(doc, "El OCR se ejecuta localmente para extraer datos visibles, como banco, monto, fecha, beneficiario, cuenta destino y código de operación. La lectura no acredita por sí sola que el dinero haya ingresado. Por esta razón, el dueño debe revisar el abono en la banca móvil y recién entonces marcar el pago como PAGADO o RECHAZADO. El cliente visualiza el estado desde su historial.", first_line=0.5)
    evidence_placeholder(doc, "Flujo de pago QR", "Insertar captura de Pago por QR, Adjuntar comprobante, Verificación de pagos del dueño y detalle de pago aprobado o rechazado.")

    heading(doc, "SIP y motivo de la alternativa adoptada", 2)
    paragraph(doc, "Se evaluó SIP como una posible vía para una cobranza interoperable. Sin embargo, una cuenta para generar QR desde un portal web no equivale a disponer de una API de producción para integrarla desde Flutter. Para una pasarela real se requerirían documentación oficial, ambiente de pruebas, credenciales de aplicación, contratos, mecanismos de firma, certificados, endpoints autorizados y un canal de notificación de transacciones.", first_line=0.5)
    paragraph(doc, "Tampoco sería seguro colocar usuarios, contraseñas o secretos bancarios dentro de una aplicación móvil. En una integración de producción, la aplicación debería solicitar el pago a un backend propio; ese backend calcularía el monto desde el pedido guardado, solicitaría la orden de cobro al proveedor y validaría un webhook o consulta firmada antes de marcar el pago como aprobado. Debido a que esos requisitos no estaban disponibles dentro del alcance académico, se implementó la alternativa QR con comprobante y constatación manual.", first_line=0.5)
    table(doc, ["Aspecto", "Alternativa QR implementada", "Pasarela SIP de producción"], [
        ["Generación", "QR autorizado configurable por el dueño.", "Orden o QR dinámico emitido por API."],
        ["Confirmación", "Revisión del dueño en banca móvil.", "Webhook o consulta validada en backend."],
        ["Fuente de verdad", "Constatación bancaria humana y auditoría.", "Estado transaccional firmado por el proveedor."],
        ["Secretos", "No se guardan secretos bancarios en Flutter.", "Secretos protegidos en infraestructura de backend."],
        ["Uso actual", "Prototipo académico funcional con revisión manual.", "Operación comercial con habilitación y contrato."],
    ], [1.3, 2.55, 2.65])

    heading(doc, "Seguridad privacidad y controles")
    paragraph(doc, "Las claves de Supabase se suministran durante la ejecución mediante variables de compilación. La aplicación no debe almacenar ni publicar una clave service_role. Supabase Row Level Security restringe la consulta y modificación de datos según el usuario y su rol. Las fotos de catálogo pueden ser públicas; los comprobantes de pago deben permanecer en almacenamiento privado y ser accesibles solo para el cliente asociado o el dueño.", first_line=0.5)
    paragraph(doc, "Los comprobantes pueden contener información personal y bancaria. Por ese motivo, las capturas de evidencias académicas deben ocultar números de cuenta, códigos de operación, QR funcionales y datos que permitan utilizar la cuenta fuera de la demostración. La documentación final describirá el flujo sin publicar credenciales ni datos sensibles.", first_line=0.5)

    heading(doc, "Plan y registro de pruebas de software")
    heading(doc, "Introducción", 2)
    paragraph(doc, "Este plan valida el producto mínimo viable de Brasas del Oriente: catálogo con fotos, búsqueda y filtros, carrito, pedidos, consultas, reservas, historial del cliente, rol dueño y ubicación. La búsqueda por voz se incluye porque está implementada en el catálogo. El QR documental, OCR y SIP quedan fuera del MVP, ya que el repositorio los define como funcionalidad extra y no realizan una transacción bancaria automática.", first_line=0.5)
    heading(doc, "Objetivos alcance y entorno", 2)
    table(doc, ["Aspecto", "Definición"], [
        ["Objetivo", "Comprobar recorridos esenciales, validaciones y control de acceso sin inventar resultados."],
        ["Alcance", "Catálogo, voz, carrito, pedido, consulta, reserva, historial, rol dueño, gestión de reservas y ubicación."],
        ["Entorno", "Flutter Android; Supabase configurado por dart define; Open Meteo, OpenStreetMap, Storage y micrófono."],
        ["Datos", "Cuentas, productos, pedidos y reservas de prueba. No utilizar movimientos ni comprobantes bancarios reales."],
    ], [1.45, 5.05])
    heading(doc, "Metodología y criterios", 2)
    paragraph(doc, "Se combinan análisis estático, pruebas unitarias y recorridos manuales. El repositorio contiene 18 pruebas unitarias declaradas. Se intentó ejecutar flutter test durante la preparación de este informe, pero no se obtuvo una salida final verificable dentro del tiempo de observación; por ello ningún caso se registra como aprobado sin evidencia de terminal. Un caso es aprobado si cumple el resultado esperado, fallido si bloquea el recorrido o entrega datos incorrectos, y pendiente si aún no se ejecutó.", first_line=0.5)
    landscape_section(doc)
    heading(doc, "Matriz de casos de prueba del MVP")
    table(doc, ["ID", "Funcionalidad", "Precondiciones", "Procedimiento", "Datos de entrada", "Resultado esperado", "Resultado obtenido", "Estado", "Evidencia"], [
        ["PT-01", "Catálogo y fotos", "Productos disponibles.", "Abrir menú y revisar tarjetas.", "Sin datos.", "Datos, precios y fotos sin desbordamiento.", "Pendiente de ejecución manual.", "Pendiente", "Captura menú."],
        ["PT-02", "Filtro y texto", "Menú abierto.", "Filtrar y escribir limonada.", "Categoría y texto.", "Solo se muestran coincidencias.", "Pendiente de ejecución manual.", "Pendiente", "Captura filtro."],
        ["PT-03", "Voz y permiso", "Micrófono disponible o denegado.", "Pulsar micrófono; permitir o negar.", "Voz: limonada.", "Filtra por voz o informa permiso requerido.", "Pendiente de ejecución manual.", "Pendiente", "Captura o video."],
        ["PT-04", "Carrito y pedido", "Productos disponibles.", "Agregar, cambiar cantidad y confirmar.", "Nombre y teléfono de prueba.", "Total correcto y pedido registrado.", "Pendiente de ejecución manual.", "Pendiente", "Captura pedido."],
        ["PT-05", "Error de pedido", "Confirmar pedido abierto.", "Enviar formulario incompleto.", "Campos vacíos o inválidos.", "Validación impide el envío.", "Prueba unitaria declarada; ejecución pendiente.", "Pendiente", "Salida test."],
        ["PT-06", "Consulta", "Supabase configurado.", "Enviar consulta válida.", "Datos de prueba.", "Se registra y confirma envío.", "Pendiente de ejecución manual.", "Pendiente", "Captura consulta."],
        ["PT-07", "Reserva", "Cliente autenticado.", "Crear futura; intentar fecha pasada.", "Fechas de prueba.", "Futura EN ESPERA; pasada rechazada.", "Pendiente de ejecución manual.", "Pendiente", "Capturas."],
        ["PT-08", "Historial", "Pedido o reserva del cliente.", "Abrir Mis pedidos y reservas.", "Cuenta cliente.", "Solo muestra registros propios y estados claros.", "Pendiente de ejecución manual.", "Pendiente", "Captura historial."],
        ["PT-09", "Rol dueño", "Dueño y reserva EN ESPERA.", "Confirmar o rechazar reserva.", "Reserva de prueba.", "El estado cambia y se refleja al cliente.", "Pendiente de ejecución manual.", "Pendiente", "Antes y después."],
        ["PT-10", "Ubicación", "Internet disponible.", "Abrir ubicación, clima y mapa.", "Sin datos.", "Muestra datos o reintento controlado; mapa abre.", "Pendiente de ejecución manual.", "Pendiente", "Captura ubicación."],
    ], [0.45, 0.9, 1.05, 1.35, 0.9, 1.35, 1.3, 0.7, 0.85], font_size=8)
    portrait_section(doc)
    heading(doc, "Registro de incidencias", 2)
    paragraph(doc, "No existen incidencias declaradas como corregidas sin una ejecución reproducible. Esta tabla se completa durante la prueba manual.", first_line=0.5)
    table(doc, ["ID", "Descripción", "Severidad", "Estado", "Evidencia o responsable"], [
        ["INC-01", "Pendiente de registrar durante la ejecución.", "Por definir", "Abierta o cerrada", "____________________________"],
        ["INC-02", "Pendiente de registrar durante la ejecución.", "Por definir", "Abierta o cerrada", "____________________________"],
    ], [0.7, 2.45, 1.0, 1.1, 1.25])
    heading(doc, "Conclusiones de las pruebas", 2)
    paragraph(doc, "La suite de 18 pruebas unitarias y los diez casos funcionales documentados constituyen la base de control de calidad del MVP. La ejecución automática y las evidencias manuales permanecen pendientes hasta obtener salida de terminal y capturas verificables. Este informe no atribuye resultados, incidencias resueltas ni aprobaciones que no hayan sido demostradas.", first_line=0.5)

    heading(doc, "Protocolo de pruebas de aceptación del usuario UAT y acta de conformidad")
    heading(doc, "Datos generales objetivo y acceso", 2)
    table(doc, ["Campo", "Valor"], [
        ["Proyecto", "Brasas del Oriente."],
        ["Versión", "1.0.0+1."],
        ["Cliente evaluador", "Grupo Neo."],
        ["Responsable del desarrollo", "________________________________."],
        ["Acceso", "Aplicación instalada por el equipo y cuentas de prueba entregadas en canal privado."],
    ], [1.8, 4.7])
    paragraph(doc, "El cliente prueba únicamente el alcance del MVP: catálogo, búsqueda, pedido, consulta, reserva, historial, respuesta del dueño y ubicación. Debe contar con internet, teléfono Android o emulador, datos de prueba y permiso de micrófono solo para la búsqueda por voz. No se prueban pagos reales ni el QR adicional.", first_line=0.5)
    table(doc, ["ID", "Funcionalidad", "Instrucciones", "Resultado esperado", "Conformidad", "Observaciones"], [
        ["UAT-01", "Catálogo", "Abra Ver menú y revise productos.", "Productos con datos y fotos.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-02", "Buscar", "Filtre y busque por texto o voz.", "Resultados relacionados o aviso de permiso.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-03", "Pedido", "Agregue productos y confirme con datos de prueba.", "Total correcto y pedido registrado.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-04", "Consulta", "Envíe una consulta de prueba.", "Confirma el envío.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-05", "Reserva", "Cree una reserva futura.", "Se registra EN ESPERA.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-06", "Historial", "Abra Mis pedidos y reservas.", "Muestra registros y estados propios.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-07", "Dueño", "Confirme o rechace una reserva.", "Cambio visible al cliente.", "[ ] Conforme\n[ ] No conforme", "____________"],
        ["UAT-08", "Ubicación", "Abra ubicación y luego el mapa.", "Datos visibles y mapa accesible.", "[ ] Conforme\n[ ] No conforme", "____________"],
    ], [0.65, 1.0, 1.45, 1.5, 0.95, 0.95], font_size=8.5)
    heading(doc, "Resultado general y acta de entrega", 2)
    paragraph(doc, "Resultado: [ ] Aceptación total    [ ] Aceptación con observaciones    [ ] Rechazo", first_line=0.0)
    paragraph(doc, "El cliente declara haber revisado el alcance del MVP. Las observaciones pendientes se anotan antes de firmar. Esta acta no certifica pagos, operaciones bancarias ni funcionalidades adicionales.", first_line=0.5)
    paragraph(doc, "Observaciones o condiciones pendientes: ________________________________________________________________\n____________________________________________________________________________________________________", first_line=0.0)
    paragraph(doc, "Nombre y firma del cliente: ___________________________________     Fecha: ____ / ____ / 2026", before=18)
    paragraph(doc, "Nombre y firma del responsable del desarrollo: __________________________     Fecha: ____ / ____ / 2026", before=18)

    heading(doc, "Bitácora de asistencia y apoyo técnico")
    paragraph(doc, "Durante el desarrollo se utilizó Codex IA como herramienta de apoyo técnico. Su participación consistió en orientar el diagnóstico, proponer estructura de tareas, revisar código, generar borradores de documentación, explicar comandos y ayudar a organizar pruebas. Las decisiones de alcance, la configuración de Supabase, la selección de evidencias, la validación en dispositivo y la responsabilidad sobre la entrega permanecen en el equipo del proyecto.", first_line=0.5)
    table(doc, ["Etapa", "Asistencia recibida", "Resultado incorporado"], [
        ["Planificación", "Organización de tareas por módulos y priorización de requisitos.", "División del trabajo para catálogo, cuentas, fotos, voz y pagos."],
        ["Supabase", "Revisión de tablas, políticas RLS, Storage y scripts SQL.", "Estructura para roles, imágenes, pedidos, pagos e historial."],
        ["Interfaz Flutter", "Diagnóstico de errores de renderizado y revisión de pantallas.", "Tarjetas del catálogo ajustadas y nuevos apartados de historial y reservas."],
        ["Integraciones", "Guía para voz, OCR, QR documental y servicios externos.", "Búsqueda por voz, fotos reales y flujo de comprobantes."],
        ["Calidad", "Propuesta de pruebas unitarias, análisis estático y guía UAT.", "Script de validación y 18 pruebas automatizadas preparadas."],
        ["Documentación", "Estructuración del guion, presentación, informe y anexos.", "Borradores editables con espacios para evidencias."],
    ], [1.25, 2.7, 2.55])

    heading(doc, "Resultados esperados y limitaciones")
    paragraph(doc, "El resultado esperado es una aplicación demostrativa que permita completar recorridos de cliente y dueño con información persistente. La validación final dependerá de ejecutar los scripts SQL en la instancia correcta de Supabase, iniciar la aplicación con la URL y clave publicable correctas, aprobar permisos necesarios y registrar las evidencias desde un dispositivo real. Los estados de pago continuarán siendo manuales hasta contar con una API bancaria y un backend de producción autorizados.", first_line=0.5)
    paragraph(doc, "Las imágenes y capturas aún no se incorporan en esta versión inicial. Esta decisión evita utilizar evidencia incompleta o imágenes que puedan contener datos sensibles. El anexo de evidencias define de forma precisa qué capturas se necesitarán para completar la entrega.", first_line=0.5)

    heading(doc, "Conclusiones")
    paragraph(doc, "Brasas del Oriente consolida las funciones principales de una aplicación de atención gastronómica: catálogo, consultas, reservas, pedidos, cuentas, ubicación y administración diferenciada. La incorporación de fotografías reales y búsqueda por voz mejora el descubrimiento de productos, mientras que Supabase permite almacenar datos y aplicar controles por rol sin exponer privilegios administrativos al cliente.", first_line=0.5)
    paragraph(doc, "La incorporación del historial de pedidos y reservas mejora la trazabilidad para el cliente. A la vez, la gestión de reservas del dueño permite convertir una solicitud pendiente en una decisión visible para la cuenta que la creó. Esta funcionalidad complementa el panel de pedidos y evita depender solo de comunicación externa para confirmar disponibilidad.", first_line=0.5)
    paragraph(doc, "La alternativa de pago QR implementada es válida como flujo académico controlado porque no simula una confirmación bancaria automática. El comprobante y el OCR aportan información de apoyo, pero el estado PAGADO depende de la revisión humana. Una futura integración SIP o equivalente debe construirse únicamente con una API autorizada, un backend seguro y mecanismos verificables de conciliación.", first_line=0.5)

    heading(doc, "Referencias")
    for item in [
        "Android Developers. (n.d.). Manifest.permission. https://developer.android.com/reference/android/Manifest.permission",
        "Flutter. (n.d.). Flutter documentation. https://docs.flutter.dev/",
        "Google. (n.d.). Recognize text in images with ML Kit on Android. https://developers.google.com/ml-kit/vision/text-recognition/v2/android",
        "Open Meteo. (n.d.). Weather API. https://open-meteo.com/en/docs",
        "OpenStreetMap contributors. (n.d.). OpenStreetMap. https://www.openstreetmap.org/",
        "Supabase. (n.d.-a). Auth. https://supabase.com/docs/guides/auth",
        "Supabase. (n.d.-b). Row Level Security. https://supabase.com/docs/guides/database/postgres/row-level-security",
        "Supabase. (n.d.-c). Storage access control. https://supabase.com/docs/guides/storage/security/access-control",
        "speech_to_text. (n.d.). Flutter package documentation. https://pub.dev/packages/speech_to_text",
    ]:
        reference(doc, item)

    doc.add_page_break()
    heading(doc, "Anexos")
    heading(doc, "Anexo A Archivos relevantes", 2)
    table(doc, ["Archivo", "Finalidad"], [
        ["supabase 09_fotos_productos.sql", "Añade ruta de imagen a productos y políticas de actualización por dueño."],
        ["supabase 08_pagos_qr.sql", "Crea configuración QR, pagos, comprobantes, auditoría y funciones de revisión."],
        ["supabase 10_historial_cliente_y_gestion_reservas.sql", "Asocia reservas al usuario, incorpora estados y habilita historial y gestión."],
        ["herramientas ejecutar_pruebas.ps1", "Ejecuta flutter analyze y flutter test antes de las pruebas manuales."],
        ["test estados_historial_test.dart", "Valida estados de reservas y pago aprobado."],
        ["test flujo_core_test.dart y validacion_entrega_test.dart", "Valida carrito, QR, pedido sin pago y formularios."],
    ], [2.85, 3.65])

    heading(doc, "Anexo B Evidencias visuales solicitadas", 2)
    paragraph(doc, "Para completar la versión final con figuras, se requieren capturas originales, sin recortes que oculten el contexto de la pantalla y sin datos bancarios visibles. Cada figura llevará una nota con su origen: Captura propia de la aplicación Brasas del Oriente, 2026.", first_line=0.5)
    table(doc, ["Figura", "Captura requerida", "Qué debe demostrar"], [
        ["Figura 1", "Catálogo con fotos reales.", "Productos, fotos, precio y botón de agregar sin desbordamiento."],
        ["Figura 2", "Búsqueda por voz.", "Estado Escuchando o Reconocido y catálogo filtrado."],
        ["Figura 3", "Cuenta del dueño.", "Accesos de administración visibles por rol."],
        ["Figura 4", "Gestión de fotos.", "Fotos cargadas o acción de reemplazar producto."],
        ["Figura 5", "Reserva del cliente.", "Estados En espera, Confirmada o Rechazada."],
        ["Figura 6", "Gestión de reservas.", "Botones para confirmar o rechazar desde el dueño."],
        ["Figura 7", "Pago QR y comprobante.", "Flujo QR sin exponer QR utilizable, cuenta ni códigos reales."],
        ["Figura 8", "Verificación de pagos.", "Revisión manual desde el panel del dueño."],
        ["Figura 9", "Ubicación y clima.", "Tarjeta de clima, contacto y acceso a mapa."],
        ["Figura 10", "Pruebas automáticas.", "Terminal con flutter analyze y flutter test aprobados."],
    ], [0.75, 2.35, 3.4])

    heading(doc, "Anexo C Comandos de validación", 2)
    for command in [
        "flutter pub get",
        "dart format lib test",
        "powershell -ExecutionPolicy Bypass -File .\\herramientas\\ejecutar_pruebas.ps1",
        "flutter run --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(command)
        font(r, size=10)
        r.font.name = "Courier New"
        r._element.rPr.rFonts.set(qn("w:ascii"), "Courier New")
        r._element.rPr.rFonts.set(qn("w:hAnsi"), "Courier New")

    doc.core_properties.title = "Informe final Brasas del Oriente"
    doc.core_properties.subject = "Desarrollo y validación de aplicación móvil"
    doc.core_properties.author = ""
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
