from pathlib import Path
from datetime import date
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "entregables" / "Informe_final_APA7_Brasas_del_Oriente.docx"
IMAGES = {
    "inicio": Path(r"C:\Users\Usuario\Videos\WhatsApp Image 2026-11-23 at 00.17.48.jpeg"),
    "dueno": Path(r"C:\Users\Usuario\Videos\WhatsApp Image 2026-11-23 at 00.17.47.jpeg"),
    "fotos": Path(r"C:\Users\Usuario\Videos\WhatsApp Image 2026-11-23 at 00.20.12.jpeg"),
    "consulta": Path(r"C:\Users\Usuario\Videos\WhatsApp Image 2026-11-22 at 23.44.28 (1).jpeg"),
    "comprobante": Path(r"C:\Users\Usuario\Videos\WhatsApp Image 2026-11-23 at 00.23.01 (1).jpeg"),
}


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=110, start=110, bottom=110, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_cell_border(cell, color="D9D9D9", size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        element = borders.find(tag)
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), color)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_keep_with_next(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    keep = OxmlElement("w:keepNext")
    p_pr.append(keep)


def add_field(run, instruction):
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])


def toc_field(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = ' TOC \\o "1-3" \\h \\z \\u '
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    fallback = OxmlElement("w:t")
    fallback.text = "Actualice este campo en Word con Ctrl+A y F9."
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, fallback, end])


def update_fields_on_open(doc):
    settings = doc.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def remove_paragraph_borders(paragraph_or_style):
    """Remove Word's inherited blue Title border in all renderers."""
    element = paragraph_or_style._p if hasattr(paragraph_or_style, "_p") else paragraph_or_style._element
    p_pr = element.get_or_add_pPr()
    for border in list(p_pr.findall(qn("w:pBdr"))):
        p_pr.remove(border)


def set_run_font(run, size=12, bold=None, italic=None):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def add_text(doc, text, style="Normal", before=0, after=0, indent=0, first=0, align=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.first_line_indent = Inches(first)
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_run_font(r)
    return p


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 2
    r = p.add_run(text)
    set_run_font(r, size={1: 12, 2: 12, 3: 12}.get(level, 12), bold=True)
    if level >= 2:
        # Keep a visible separation from the following paragraph in Word.
        r.add_break(WD_BREAK.LINE)
    # Do not inherit Word's run-in behavior from built-in heading styles.
    # Standard paragraph separation is more reliable for this APA report.
    return p


def add_spacer(doc, points=6):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(points)
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 2
    r = p.add_run("• " + text)
    set_run_font(r)
    return p


def add_numbered(doc, text, n):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 2
    r = p.add_run(f"{n}. {text}")
    set_run_font(r)
    return p


def add_caption(doc, label, description):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(9)
    p.paragraph_format.line_spacing = 2
    r1 = p.add_run(label + ". ")
    set_run_font(r1, 12, bold=True)
    r2 = p.add_run(description)
    set_run_font(r2, 12, italic=True)
    return p


def add_figure(doc, image_key, label, description, width=3.1):
    image = IMAGES[image_key]
    if not image.exists():
        return
    image_to_insert = image
    try:
        with Image.open(image) as source:
            source.verify()
    except Exception:
        return
    # Algunas capturas de WhatsApp usan variantes JPEG que python-docx no
    # reconoce directamente. Se normalizan a PNG sin alterar la evidencia.
    normalized = ROOT / ".qa_informe_final" / f"{image_key}.png"
    normalized.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(image) as source:
        source.convert("RGB").save(normalized, "PNG")
    image_to_insert = normalized
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(str(image_to_insert), width=Inches(width))
    add_caption(doc, label, description)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    header_cells = table.rows[0].cells
    set_repeat_table_header(table.rows[0])
    for i, header in enumerate(headers):
        cell = header_cells[i]
        if widths:
            cell.width = Inches(widths[i])
        set_cell_shading(cell, "1F1F1F")
        set_cell_border(cell)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(header)
        set_run_font(r, size=10, bold=True)
        r.font.color.rgb = RGBColor(255, 255, 255)
    for idx, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cell = cells[i]
            if widths:
                cell.width = Inches(widths[i])
            set_cell_border(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if idx % 2:
                set_cell_shading(cell, "F4F4F4")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(value))
            set_run_font(r, size=10)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_reference(doc, text):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 2
    r = p.add_run(text)
    set_run_font(r)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1.25)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 2
    normal.paragraph_format.space_after = Pt(0)
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        st = styles[name]
        st.font.name = "Times New Roman"
        st._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        st._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        st.font.color.rgb = RGBColor(0, 0, 0)
    styles["Title"].font.size = Pt(12)
    styles["Title"].font.bold = True
    remove_paragraph_borders(styles["Title"])
    for name in ("Heading 1", "Heading 2", "Heading 3"):
        styles[name].font.size = Pt(12)
        styles[name].font.bold = True

    section.different_odd_and_even_pages = True
    section.header_distance = Inches(0.5)
    for header in (section.header, section.even_page_header):
        p = header.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.line_spacing = 1
        nr = p.add_run()
        set_run_font(nr, 12)
        add_field(nr, " PAGE ")

    # Title page
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2
    r = p.add_run("Informe técnico de desarrollo y validación de la aplicación móvil Brasas del Oriente")
    set_run_font(r, 12, bold=True)
    remove_paragraph_borders(p)
    for line in [
        "Estudiante: ______________________________",
        "Universidad Privada Domingo Savio",
        "Aplicaciones Móviles I",
        "Docente: ______________________________",
        "23 de noviembre de 2026",
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 2
        r = p.add_run(line)
        set_run_font(r)
    doc.add_page_break()

    # Abstract
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2
    r = p.add_run("Resumen")
    set_run_font(r, 12, bold=True)
    add_text(doc, "Este informe documenta el desarrollo y la validación de Brasas del Oriente, una aplicación móvil creada con Flutter para una churrasquería de Santa Cruz de la Sierra. La solución reúne catálogo digital, fotos reales de productos, búsqueda por voz, consultas, reservas, carrito, pedidos, cuentas con roles y servicios de ubicación. Supabase se utiliza para autenticación, base de datos, funciones remotas y almacenamiento de imágenes con políticas de acceso. En la última versión se incorporaron la administración de fotografías por parte del dueño, el reconocimiento de voz para filtrar el catálogo y un flujo complementario de pago mediante un código QR bancario configurable. El cliente adjunta un comprobante y el dueño verifica el abono antes de marcar el pedido como pagado.")
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2
    p.paragraph_format.space_before = Pt(12)
    r1 = p.add_run("Palabras clave: ")
    set_run_font(r1, 12, italic=True)
    r2 = p.add_run("Flutter, Supabase, almacenamiento en la nube, búsqueda por voz, QR, OCR, pagos.")
    set_run_font(r2)
    doc.add_page_break()

    # TOC
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 2
    r = p.add_run("Índice")
    set_run_font(r, 12, bold=True)
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    toc_field(p)
    add_text(doc, "Nota. El índice es un campo automático de Word. Si no se actualiza al abrir el archivo, presione Ctrl+A y luego F9; seleccione “Actualizar toda la tabla”.", before=12)
    doc.add_page_break()

    add_heading(doc, "Introducción", 1)
    add_text(doc, "Los negocios gastronómicos requieren canales simples para presentar su oferta, recibir solicitudes y organizar pedidos. Brasas del Oriente se desarrolló como una aplicación móvil académica orientada a una churrasquería de Santa Cruz de la Sierra. El proyecto busca demostrar cómo una aplicación Flutter puede combinar una interfaz de cliente con servicios remotos, autenticación, almacenamiento de imágenes, geolocalización y comunicación externa.")
    add_text(doc, "El alcance de esta versión incorpora tanto los flujos básicos del restaurante como las integraciones solicitadas en la Actividad 4: fotografías reales en la nube y búsqueda por voz. De forma complementaria, se implementó una alternativa controlada de pago por QR bancario con comprobante y validación humana. Esta decisión permite preservar la honestidad técnica: una captura u OCR puede ayudar a organizar la revisión, pero no confirma por sí sola el ingreso de dinero en una cuenta bancaria.")

    add_heading(doc, "Planteamiento del problema", 1)
    add_text(doc, "Un menú estático o la comunicación por mensajes dificulta la actualización del catálogo, el registro ordenado de solicitudes y el seguimiento de pedidos. Además, un catálogo gastronómico necesita imágenes actuales y una forma de búsqueda accesible. Para el dueño, el reto es conservar control sobre qué información se publica y quién puede modificarla.")

    add_heading(doc, "Objetivos", 1)
    add_spacer(doc, 2)
    add_heading(doc, "Objetivo general", 2)
    add_text(doc, "Desarrollar una aplicación móvil en Flutter para gestionar la interacción básica entre clientes y la churrasquería Brasas del Oriente, integrando Supabase y servicios externos de manera controlada.")
    add_heading(doc, "Objetivos específicos", 2)
    for item in [
        "Mostrar un catálogo filtrable con datos, precios y fotografías reales de los productos.",
        "Permitir consultas, reservas, carrito y creación de pedidos mediante funciones de Supabase.",
        "Aplicar autenticación y autorización por roles de cliente y dueño.",
        "Permitir que el dueño cargue o reemplace fotografías de productos usando Supabase Storage.",
        "Incorporar búsqueda por voz con autorización explícita para el uso del micrófono.",
        "Ofrecer un flujo de pago QR complementario con comprobante, lectura OCR local y verificación manual.",
    ]:
        add_bullet(doc, item)

    add_heading(doc, "Metodología y arquitectura", 1)
    add_text(doc, "Se aplicó un enfoque incremental. Primero se construyeron las pantallas y modelos de datos; después se conectaron los servicios de Supabase y, finalmente, se añadieron las integraciones de imágenes, voz y pagos. La aplicación se desarrolló en Dart con Flutter y utiliza Material 3 para la interfaz.")
    doc.add_page_break()
    add_table(doc,
        ["Componente", "Uso en el proyecto", "Control principal"],
        [
            ["Flutter", "Interfaz móvil, navegación, formularios y estado de pantalla.", "Validaciones y pruebas automatizadas."],
            ["Supabase Auth", "Inicio de sesión y perfiles con rol de cliente o dueño.", "JWT y políticas según el usuario autenticado."],
            ["PostgreSQL y RPC", "Catálogo, consultas, reservas, pedidos, pagos y auditoría.", "RLS y funciones remotas para operaciones sensibles."],
            ["Supabase Storage", "Fotos de productos, portada, QR y comprobantes.", "Buckets y políticas de lectura o escritura por rol."],
            ["speech_to_text", "Transcripción para filtrar el catálogo por voz.", "Permiso RECORD_AUDIO y manejo de indisponibilidad."],
            ["Google ML Kit", "Lectura local de datos visibles en comprobantes.", "OCR como apoyo, no como confirmación bancaria."],
            ["Open-Meteo y OpenStreetMap", "Clima, ubicación y visualización de mapa.", "Consumo de servicios externos sin exponer claves privadas."],
        ],
        [1.18, 3.04, 2.28],
    )
    add_text(doc, "Supabase integra autenticación con políticas de seguridad por fila, por lo que el acceso desde el cliente se limita a la información permitida por el rol y la política definida (Supabase, 2026a, 2026b). El uso de Storage sigue el mismo modelo: por defecto, las cargas requieren políticas explícitas sobre los objetos almacenados (Supabase, 2026c).")

    add_heading(doc, "Desarrollo de la última versión", 1)
    add_heading(doc, "Catálogo con datos y fotos reales", 2)
    add_text(doc, "El catálogo consume productos almacenados en la tabla negocios, utilizada en este proyecto como catálogo de productos. Cada elemento contiene nombre, rubro, descripción, precio e imagen_path. La ruta de la imagen se resuelve desde el bucket negocios y se muestra en tarjetas reutilizables. El dueño puede entrar a Gestionar fotos de productos para cargar o reemplazar la fotografía asociada a cada producto.")
    add_text(doc, "Las imágenes se guardan bajo rutas de producto y el propietario debe estar autenticado para subir, actualizar o eliminar archivos. La política evita la escritura pública y mantiene la lectura del catálogo disponible para el usuario final. Esto cumple con el requisito de que el dueño cambie la foto de su negocio o productos sin exponer privilegios administrativos en la aplicación.")
    add_figure(doc, "fotos", "Figura 1", "Panel de administración de fotografías reales de productos. Captura propia de la aplicación.", width=3.0)

    add_heading(doc, "Búsqueda y filtrado por voz", 2)
    add_text(doc, "La pantalla Menú digital combina un campo de texto, categorías y un botón de micrófono. Al iniciar la escucha, el servicio de voz solicita disponibilidad y permiso; el texto reconocido se coloca en el filtro del catálogo. Así, una expresión como “limonada” reduce los resultados visibles a productos coincidentes. Android clasifica RECORD_AUDIO como permiso peligroso, por lo que la aplicación debe declararlo y solicitar la autorización del usuario antes de grabar audio (Android Developers, 2026a).")
    add_text(doc, "La integración contempla mensajes cuando el permiso es denegado, cuando el reconocimiento no está disponible o cuando el servicio no puede inicializarse. La prueba debe realizarse en un teléfono real, ya que el emulador puede no ofrecer captura de audio (Android Developers, 2026b).")

    add_heading(doc, "Cuentas, roles y administración", 2)
    add_text(doc, "La aplicación contempla los roles cliente y dueño. El cliente puede utilizar el catálogo, realizar solicitudes y asociar comprobantes a sus propios pedidos. El dueño recibe opciones adicionales: panel de pedidos, cambio de portada, gestión de fotos de productos, configuración de QR y verificación de pagos. Esta separación se valida tanto en la interfaz como mediante políticas RLS y funciones de la base de datos.")
    add_figure(doc, "dueno", "Figura 2", "Opciones exclusivas disponibles para el rol dueño. Captura propia de la aplicación.", width=3.0)
    doc.add_page_break()

    add_heading(doc, "Consultas, reservas y pedidos", 2)
    add_text(doc, "Los formularios validan los datos mínimos antes de enviarlos. Las consultas se registran en Supabase y muestran una confirmación al cliente. El carrito calcula cantidades y total; cuando se confirma un pedido, la función crear_pedido registra el encabezado y el detalle de los productos. Estas operaciones separan la lógica de creación de pedidos de la interfaz móvil.")
    add_figure(doc, "consulta", "Figura 3", "Formulario de consulta con mensaje de registro exitoso. Captura propia de la aplicación.", width=3.0)

    add_heading(doc, "Ubicación, clima y contacto", 2)
    add_text(doc, "La sección de ubicación presenta dirección, horarios y contacto. También consulta la API Open-Meteo para mostrar condiciones climáticas y maneja estados de carga o error. Los botones de llamada, WhatsApp, ruta y mapa conectan con aplicaciones o servicios externos. El mapa se muestra con OpenStreetMap, evitando incorporar una clave privada de Google en el cliente.")

    add_heading(doc, "Pago por QR y comprobante", 1)
    add_spacer(doc, 2)
    add_heading(doc, "Alcance de la solución implementada", 2)
    add_text(doc, "La versión actual utiliza un QR bancario configurado por el dueño. El QR y los datos de validación no se escriben en el código fuente; se guardan en Supabase para que el dueño pueda actualizarlos. Cuando el cliente inicia el pago, la aplicación obtiene el total calculado desde el pedido, muestra el QR activo y solicita que se transfiera exactamente el importe indicado.")
    add_text(doc, "Después de pagar, el cliente adjunta un comprobante JPG o PNG de hasta 5 MB. El archivo se guarda en un bucket privado asociado al pago y se calcula un hash SHA-256. El OCR se ejecuta en el dispositivo para extraer, cuando sea posible, datos como banco, monto, fecha, beneficiario, cuenta y código de operación. Google ML Kit reconoce texto en imágenes y su calidad depende de factores como resolución y enfoque de la imagen (Google, 2026).")
    add_text(doc, "El resultado del OCR se usa como ayuda documental. La aplicación compara los datos disponibles con el pedido y detecta reutilización por hash o código de operación; sin embargo, la transacción solo cambia a PAGADO cuando el dueño constata el abono en su banca móvil. Esta decisión evita afirmar una verificación bancaria inexistente.")
    add_figure(doc, "comprobante", "Figura 4", "Pantalla para seleccionar y enviar un comprobante de pago. Captura propia de la aplicación.", width=3.0)

    add_heading(doc, "Por qué no se utilizó SIP como pasarela directa", 2)
    add_text(doc, "SIP se consideró como una posible vía para generar y verificar cobros interoperables. No obstante, el equipo no recibió una API de producción, documentación de endpoints, ambiente de pruebas, credenciales de aplicación, certificados ni un mecanismo autorizado de notificación de pagos. El acceso proporcionado para generar un QR desde un portal web no equivale a tener una pasarela disponible para ser invocada desde una aplicación Flutter.")
    add_text(doc, "Una integración bancaria directa tampoco debe implementarse colocando usuarios, contraseñas, secretos o certificados dentro de la aplicación móvil. Las operaciones de creación, consulta y verificación deberían ejecutarse en un backend controlado por la empresa, porque la aplicación instalada puede ser inspeccionada o modificada. Por estas razones, para el alcance académico se eligió una alternativa operativa y explícitamente manual en la etapa final de confirmación.")

    add_heading(doc, "Requisitos y pasos teóricos para una integración SIP", 2)
    add_text(doc, "Los siguientes pasos describen un escenario de producción propuesto. No representan una integración SIP ya realizada ni sustituyen las condiciones que establezca la entidad financiera o el proveedor de la pasarela.")
    steps = [
        "Formalizar la relación comercial con la entidad o proveedor y solicitar el producto de cobranza por API, incluyendo responsables, cuenta beneficiaria y condiciones de operación.",
        "Recibir documentación técnica oficial, un ambiente sandbox, credenciales de cliente, certificados o mecanismos de firma, límites de consumo y el contrato de uso de datos.",
        "Crear un backend propio para generar la orden de cobro. El backend debe calcular el total a partir del pedido persistido y nunca aceptar como confiable el monto enviado por la aplicación.",
        "Solicitar al proveedor el QR dinámico o la orden de pago y registrar el identificador único, vencimiento, moneda e importe en la base de datos.",
        "Configurar un webhook HTTPS autenticado o un mecanismo de consulta de estado. El backend debe validar firma, origen, importe, moneda, identificador e idempotencia antes de actualizar el estado a PAGADO.",
        "Aplicar controles de seguridad: secretos en variables de entorno, rotación de credenciales, registros de auditoría, mínimo privilegio, protección de datos personales y monitoreo de errores o reintentos.",
        "Realizar pruebas de creación, pago, cancelación, expiración, duplicidad, reintento y conciliación; luego solicitar la habilitación formal de producción.",
    ]
    for i, step in enumerate(steps, 1):
        add_numbered(doc, step, i)
    add_text(doc, "La protección de la API debe apoyarse en autenticación, autorización, validación de eventos y auditoría. En el entorno del proyecto, Supabase recomienda habilitar RLS y otorgar privilegios mínimos a cada rol expuesto (Supabase, 2026a). El mismo principio se aplicaría a un backend de pagos.")

    add_heading(doc, "Comparación entre la alternativa implementada y una pasarela SIP", 2)
    add_table(doc,
        ["Aspecto", "Alternativa actual con QR", "Pasarela SIP directa"],
        [
            ["Generación de QR", "QR autorizado configurado por el dueño.", "QR dinámico u orden creada por API."],
            ["Monto", "Se muestra el total del pedido y se instruye pagar el importe exacto.", "Monto asociado criptográfica o transaccionalmente a una orden."],
            ["Confirmación", "Constatación manual del dueño en banca móvil.", "Webhook o consulta de estado validada en backend."],
            ["Comprobante", "Imagen privada con OCR documental y controles de duplicidad.", "Opcional para soporte; la fuente de verdad es la transacción."],
            ["Secretos", "No se usan claves de banca dentro de Flutter.", "Se resguardan en backend, nunca en cliente móvil."],
            ["Disponibilidad", "Funcional para un prototipo con revisión humana.", "Requiere contratación, aprobación técnica y operación del proveedor."],
        ],
        [1.25, 2.62, 2.63],
    )

    add_heading(doc, "Seguridad, privacidad y limitaciones", 1)
    add_text(doc, "Las credenciales de Supabase no se guardan en el repositorio: la aplicación recibe la URL y la clave publicable mediante variables de compilación. Las claves secretas o service_role no se usan en Flutter. Las fotos de productos son públicas porque pertenecen al catálogo; los comprobantes, en cambio, se guardan en un bucket privado y se entregan con URL firmada solamente a la persona vinculada al pago o al dueño.")
    add_text(doc, "La lectura OCR no equivale a una confirmación financiera. Un comprobante puede ser alterado, ilegible o corresponder a una operación distinta; por eso el estado final depende de la constatación bancaria manual. Esta limitación se conserva de manera intencional y se muestra al usuario antes de enviar el archivo.")
    add_text(doc, "Durante la toma de evidencia se observó una advertencia visual de desbordamiento inferior en algunas tarjetas del catálogo en una pantalla específica. Las fotos y filtros continuaron funcionales, pero el ajuste del alto o distribución de esos componentes debe incluirse como tarea de pulido antes de una publicación pública.")

    add_heading(doc, "Pruebas y resultados", 1)
    add_text(doc, "La validación se realizó mediante análisis estático, pruebas unitarias y recorridos funcionales en Android. El proyecto cuenta con pruebas para carrito, validadores, clima, OCR, modelo de imagen de producto y configuración QR. La ejecución de flutter analyze no reportó incidencias y flutter test completó 10 pruebas. También se generó un APK de depuración y se verificó una compilación Android con targetSdk 36.")
    add_table(doc,
        ["Caso", "Resultado esperado", "Resultado observado"],
        [
            ["Fotos de productos", "El dueño carga o reemplaza una imagen y el catálogo utiliza la ruta guardada.", "Cumplido: fotos reales registradas en el panel de productos."],
            ["Búsqueda por voz", "El micrófono reconoce una palabra y filtra el catálogo.", "Cumplido en dispositivo Android con permiso concedido."],
            ["Consulta", "El formulario valida y registra la solicitud.", "Cumplido: se muestra confirmación de envío."],
            ["Pago QR", "El cliente adjunta comprobante y el dueño revisa antes de pagar.", "Cumplido: flujo llega a revisión manual."],
            ["Pruebas automatizadas", "Análisis sin incidencias y pruebas aprobadas.", "Cumplido: 10 pruebas superadas."],
        ],
        [1.35, 2.62, 2.53],
    )

    add_heading(doc, "Conclusiones", 1)
    add_text(doc, "Brasas del Oriente integra en una sola aplicación los procesos principales de interacción de una churrasquería: catálogo, solicitudes, pedidos, cuentas y servicios de contacto. La última versión amplía el valor del catálogo al incorporar fotografías reales administradas por el dueño y un filtro por voz que mejora el acceso a los productos.")
    add_text(doc, "La arquitectura con Supabase permite aplicar autenticación, roles, RLS y Storage sin trasladar privilegios administrativos al cliente móvil. El flujo QR complementario demuestra una alternativa útil para el contexto académico: mantiene el importe del pedido, conserva evidencia documental, detecta inconsistencias y exige verificación humana antes de confirmar un pago.")
    add_text(doc, "No se debe presentar la solución QR actual como una pasarela SIP. Una integración bancaria directa requeriría formalización, API autorizada, backend seguro y una confirmación transaccional firmada. Como mejora futura, el proyecto puede migrar a esa arquitectura una vez que el proveedor habilite las condiciones técnicas y contractuales necesarias.")

    add_heading(doc, "Referencias", 1)
    refs = [
        "Android Developers. (2026a). Manifest.permission. https://developer.android.com/reference/android/Manifest.permission",
        "Android Developers. (2026b). MediaRecorder overview. https://developer.android.com/media/platform/mediarecorder",
        "Google. (2026). Recognize text in images with ML Kit on Android. https://developers.google.com/ml-kit/vision/text-recognition/v2/android",
        "Supabase. (2026a). Row Level Security. https://supabase.com/docs/guides/database/postgres/row-level-security",
        "Supabase. (2026b). Auth. https://supabase.com/docs/guides/auth",
        "Supabase. (2026c). Storage access control. https://supabase.com/docs/guides/storage/security/access-control",
        "Supabase. (2026d). Use Supabase with Flutter. https://supabase.com/docs/guides/getting-started/quickstarts/flutter",
    ]
    for ref in refs:
        add_reference(doc, ref)

    doc.add_page_break()
    add_heading(doc, "Anexos", 1)
    add_spacer(doc, 2)
    add_heading(doc, "Anexo A Evidencias funcionales", 2)
    add_text(doc, "Las siguientes capturas corresponden a los flujos implementados. Por privacidad, no se incorpora la imagen del QR bancario real ni datos de cuentas, beneficiarios, códigos de operación o comprobantes de terceros.")
    add_figure(doc, "inicio", "Figura A1", "Pantalla principal de Brasas del Oriente. Captura propia de la aplicación.", width=3.0)
    add_figure(doc, "fotos", "Figura A2", "Productos con fotografías almacenadas y administrables por el dueño. Captura propia de la aplicación.", width=3.0)
    add_figure(doc, "consulta", "Figura A3", "Evidencia de registro de una consulta. Captura propia de la aplicación.", width=3.0)
    add_figure(doc, "comprobante", "Figura A4", "Selección de comprobante con advertencia de alcance del OCR. Captura propia de la aplicación.", width=3.0)

    add_heading(doc, "Anexo B Scripts y configuración relevante", 2)
    add_table(doc,
        ["Archivo", "Finalidad", "Orden"],
        [
            ["07_storage_negocio.sql", "Crea la configuración del negocio, bucket negocios y políticas de Storage.", "Después de cuentas y roles."],
            ["09_fotos_productos.sql", "Agrega imagen_path a productos y restringe la actualización al dueño.", "Después de 07_storage_negocio.sql."],
            ["08_pagos_qr.sql", "Crea configuración QR, pagos, comprobantes privados, auditoría y funciones de revisión.", "Extra; después de pedidos y cuentas."],
            ["AndroidManifest.xml", "Declara RECORD_AUDIO para la búsqueda por voz.", "Se compila con la aplicación."],
        ],
        [1.65, 3.45, 1.4],
    )

    add_heading(doc, "Anexo C Comandos de validación", 2)
    for command in [
        "flutter pub get",
        "dart format lib test",
        "flutter analyze",
        "flutter test",
        "flutter build apk --debug --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(command)
        set_run_font(r, 10)
        r.font.name = "Courier New"
        r._element.rPr.rFonts.set(qn("w:ascii"), "Courier New")
        r._element.rPr.rFonts.set(qn("w:hAnsi"), "Courier New")

    update_fields_on_open(doc)
    doc.core_properties.title = "Informe técnico Brasas del Oriente"
    doc.core_properties.subject = "Desarrollo, evidencias, SIP y pago QR"
    doc.core_properties.author = ""
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
