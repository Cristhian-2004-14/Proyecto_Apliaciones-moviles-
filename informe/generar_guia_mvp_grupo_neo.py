from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "entregables" / "Guia_MVP_Grupo_Neo.docx"

BROWN = "241711"
ORANGE = "D56B25"
PALE = "FFF4ED"
GRAY = "F2F2F2"
BORDER = "D9D9D9"


TESTS = [
    {
        "id": "P01",
        "name": "Ingreso y navegación principal",
        "purpose": "Comprobar que la aplicación abre y que cada módulo visible responde.",
        "pre": "Aplicación instalada y dispositivo con conexión a internet.",
        "steps": [
            "Abrir Brasas del Oriente.",
            "Revisar que aparezcan Ver menú, Mi pedido, Mi cuenta, Reservar mesa, Enviar consulta y Ubicación y horarios.",
            "Abrir cada módulo y regresar usando la flecha superior.",
        ],
        "expected": "La pantalla principal carga sin cierres ni textos superpuestos. Cada módulo abre su pantalla correcta y el botón Atrás devuelve al inicio.",
    },
    {
        "id": "P02",
        "name": "Catálogo con fotos y filtros",
        "purpose": "Verificar que el menú muestra información, fotografías y categorías coherentes.",
        "pre": "Conexión disponible y catálogo con fotografías cargadas por el dueño.",
        "steps": [
            "Entrar en Ver menú.",
            "Confirmar que al menos cinco productos muestran nombre, descripción, precio y foto.",
            "Elegir Bebidas, Acompañamientos y luego Todos.",
            "Desplazarse hasta el final de la lista.",
        ],
        "expected": "Cada filtro deja visibles solo los productos de su categoría. Las imágenes y datos corresponden al producto. La lista se desplaza sin tarjetas cortadas ni mensajes de error.",
    },
    {
        "id": "P03",
        "name": "Búsqueda escrita de productos",
        "purpose": "Comprobar el filtrado del catálogo por nombre o descripción.",
        "pre": "Estar en Menú digital.",
        "steps": [
            "Tocar Buscar en el menú.",
            "Escribir limonada.",
            "Comprobar los resultados.",
            "Borrar el texto y buscar una palabra inexistente, por ejemplo xyz123.",
        ],
        "expected": "Al buscar limonada se muestra Limonada de hierbabuena. Con xyz123 se informa que no hay coincidencias o se presenta una lista vacía sin bloquear la aplicación.",
    },
    {
        "id": "P04",
        "name": "Búsqueda por voz y permiso de micrófono",
        "purpose": "Validar reconocimiento de voz, filtrado y manejo del permiso RECORD_AUDIO.",
        "pre": "Dispositivo Android físico, internet activo y micrófono disponible.",
        "steps": [
            "En Menú digital, tocar el ícono de micrófono.",
            "Cuando Android solicite permiso, elegir Permitir.",
            "Decir limonada y esperar a que finalice la escucha.",
            "Repetir el intento negando el permiso, si el dispositivo permite restablecerlo desde Ajustes.",
        ],
        "expected": "Con permiso concedido, el texto reconocido aparece en la búsqueda y el catálogo se filtra. Con permiso negado, se muestra un aviso claro y la aplicación continúa operativa mediante la búsqueda escrita.",
    },
    {
        "id": "P05",
        "name": "Carrito y cantidades",
        "purpose": "Confirmar que el carrito conserva productos, cantidades y total correcto.",
        "pre": "Estar en Menú digital.",
        "steps": [
            "Agregar Limonada de hierbabuena una vez y Lomo fino una vez.",
            "Abrir el ícono del carrito o Mi pedido.",
            "Aumentar una unidad de limonada y disminuir una unidad de lomo fino.",
            "Revisar el total y eliminar el último producto si corresponde.",
        ],
        "expected": "Las cantidades nunca son negativas. El total cambia al modificar cada cantidad y el artículo eliminado deja de contarse en el pedido.",
    },
    {
        "id": "P06",
        "name": "Confirmación de pedido",
        "purpose": "Validar el registro de un pedido con datos básicos del cliente.",
        "pre": "Tener al menos un producto en Mi pedido y conexión a Supabase.",
        "steps": [
            "Tocar Confirmar pedido.",
            "Probar enviar el formulario vacío para revisar las validaciones.",
            "Ingresar un nombre de prueba y un teléfono boliviano de prueba autorizado.",
            "Confirmar el pedido una sola vez y esperar la respuesta.",
        ],
        "expected": "Los campos inválidos no se envían. Con datos válidos, se crea un pedido una sola vez, se muestra confirmación y el detalle coincide con el carrito.",
    },
    {
        "id": "P07",
        "name": "Cuenta y permisos del dueño",
        "purpose": "Comprobar que las funciones administrativas solo son visibles para el dueño.",
        "pre": "Contar con una cuenta de prueba autorizada como dueño. No anotar ni compartir credenciales en esta guía.",
        "steps": [
            "Abrir Mi cuenta e iniciar sesión con la cuenta de prueba autorizada.",
            "Confirmar que el perfil muestra Rol Dueño.",
            "Revisar que aparezcan las opciones de fotos, configuración QR y verificación de pagos.",
            "Cerrar sesión y verificar que esas opciones ya no estén disponibles para un cliente.",
        ],
        "expected": "Las acciones administrativas aparecen solo para el dueño autenticado. Al cerrar sesión o usar una cuenta cliente, no se puede acceder a esas acciones.",
    },
    {
        "id": "P08",
        "name": "Carga y actualización de foto de producto",
        "purpose": "Verificar Storage, permisos del dueño y actualización del catálogo.",
        "pre": "Sesión de dueño activa; usar una foto JPG o PNG de prueba sin datos personales.",
        "steps": [
            "En Mi cuenta, tocar Gestionar fotos de productos.",
            "Elegir un producto y seleccionar una foto de prueba desde el teléfono.",
            "Esperar el mensaje de carga exitosa.",
            "Volver al catálogo y localizar ese producto.",
        ],
        "expected": "La foto se carga sin error y se visualiza en el panel. El catálogo muestra la nueva imagen del producto después de actualizar o volver a abrir la pantalla.",
    },
    {
        "id": "P09",
        "name": "Consulta y servicios de ubicación",
        "purpose": "Comprobar formularios, clima y enlaces a servicios externos.",
        "pre": "Conexión a internet. Para llamadas, WhatsApp o mapas no es necesario completar acciones externas; basta revisar que se solicite abrir la aplicación correspondiente.",
        "steps": [
            "Entrar en Enviar consulta, completar nombre, teléfono y mensaje de prueba, y enviar.",
            "Confirmar el mensaje de éxito.",
            "Abrir Ubicación y horarios y esperar la tarjeta de clima.",
            "Probar Ver mapa o Cómo llegar y volver a la app sin completar una llamada o mensaje real.",
        ],
        "expected": "La consulta muestra confirmación. La pantalla de ubicación muestra datos del negocio y clima o un mensaje de reintento si falla la conexión. Los botones solicitan abrir el servicio externo correcto.",
    },
    {
        "id": "P10",
        "name": "Pago QR y comprobante en revisión manual",
        "purpose": "Validar el flujo documental sin realizar una transferencia real.",
        "pre": "Usar solamente un pedido de prueba y un comprobante ficticio permitido por el equipo. No escanear, publicar ni compartir datos bancarios, QR reales o comprobantes de terceros.",
        "steps": [
            "Desde el pedido de prueba, abrir Pago por QR.",
            "Revisar que el total mostrado coincida con el pedido.",
            "Abrir Adjuntar comprobante y seleccionar una imagen de prueba JPG o PNG menor a 5 MB.",
            "Enviar el comprobante y, con cuenta de dueño, abrir Verificación de pagos.",
        ],
        "expected": "El pago queda en revisión manual; no debe marcarse como PAGADO automáticamente. El dueño puede ver la solicitud y solo confirma el pago después de constatar el abono real en la banca autorizada.",
    },
]


def set_run_font(run, size=11, bold=False, color=None):
    run.font.name = "Aptos"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def shade(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), color)


def borders(cell, color=BORDER):
    tc_pr = cell._tc.get_or_add_tcPr()
    existing = tc_pr.first_child_found_in("w:tcBorders")
    if existing is not None:
        tc_pr.remove(existing)
    element = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = OxmlElement(f"w:{edge}")
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), "6")
        tag.set(qn("w:color"), color)
        element.append(tag)
    tc_pr.append(element)


def cell_margins(cell, top=100, start=110, bottom=100, end=110):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    mar = tc_pr.first_child_found_in("w:tcMar")
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tc_pr.append(mar)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = mar.find(qn(f"w:{side}"))
        if node is None:
            node = OxmlElement(f"w:{side}")
            mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def table_cell(cell, text, header=False, size=10):
    shade(cell, BROWN if header else "FFFFFF")
    borders(cell)
    cell_margins(cell)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.1
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if header else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    set_run_font(r, size=size, bold=header, color="FFFFFF" if header else None)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before = Pt(18 if level == 1 else 12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, 15 if level == 1 else 12, bold=True, color=BROWN)
    return p


def add_body(doc, text, *, bold_lead=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.15
    if bold_lead and text.startswith(bold_lead):
        r = p.add_run(bold_lead)
        set_run_font(r, 11, bold=True)
        r = p.add_run(text[len(bold_lead):])
        set_run_font(r, 11)
    else:
        r = p.add_run(text)
        set_run_font(r, 11)
    return p


def add_numbered_steps(doc, steps):
    for n, step in enumerate(steps, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.28)
        p.paragraph_format.first_line_indent = Inches(-0.20)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(f"{n}. ")
        set_run_font(r, 11, bold=True, color=ORANGE)
        r = p.add_run(step)
        set_run_font(r, 11)


def add_test(doc, test):
    add_heading(doc, f"{test['id']}  {test['name']}", 1)
    add_body(doc, test["purpose"], bold_lead=None)

    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(1.05)
    table.columns[1].width = Inches(5.85)
    table_cell(table.cell(0, 0), "Antes de iniciar", header=True)
    table_cell(table.cell(0, 1), test["pre"], header=False)
    table_cell(table.cell(1, 0), "Resultado esperado", header=True)
    table_cell(table.cell(1, 1), test["expected"], header=False)

    add_body(doc, "Pasos para realizar la prueba", bold_lead="Pasos para realizar la prueba")
    add_numbered_steps(doc, test["steps"])

    result = doc.add_table(rows=2, cols=4)
    result.alignment = WD_TABLE_ALIGNMENT.CENTER
    result.autofit = False
    headers = ["Estado", "Resultado observado", "Evidencia", "Error o comentario"]
    widths = [0.8, 2.15, 1.4, 2.55]
    for col, (text, width) in enumerate(zip(headers, widths)):
        result.columns[col].width = Inches(width)
        table_cell(result.cell(0, col), text, header=True, size=9)
        table_cell(result.cell(1, col), "", header=False, size=10)
    result.rows[1].height = Inches(0.54)
    add_body(doc, "Registrar Pasa, Falla o Observado. Si falla, anotar en qué paso ocurrió, qué se esperaba, qué ocurrió realmente y adjuntar una captura o video corto sin datos sensibles.")


def add_page_number(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Página ")
    set_run_font(r, 9, color="666666")
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    p._p.append(fld)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    add_page_number(section)

    styles = doc.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"]._element.rPr.rFonts.set(qn("w:ascii"), "Aptos")
    styles["Normal"]._element.rPr.rFonts.set(qn("w:hAnsi"), "Aptos")
    styles["Normal"].font.size = Pt(11)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_before = Pt(18)
    title.paragraph_format.space_after = Pt(6)
    r = title.add_run("Guía de pruebas MVP para Grupo Neo")
    set_run_font(r, 23, bold=True, color=BROWN)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(20)
    r = subtitle.add_run("Brasas del Oriente  |  Pruebas de aceptación de la aplicación")
    set_run_font(r, 11, color=ORANGE)

    add_body(doc, "Esta guía permite al Grupo Neo recorrer las funciones principales de la aplicación y documentar hallazgos de forma comparable. Completen las diez pruebas en orden, registren el resultado en la tabla de cada prueba y reporten los fallos con evidencia.")

    add_heading(doc, "Antes de comenzar", 1)
    for item in [
        "Instalen la versión de prueba más reciente de Brasas del Oriente en un teléfono Android físico.",
        "Usen una conexión Wi-Fi o datos móviles estable. Indiquen si una falla ocurrió sin conexión.",
        "Para pruebas de dueño, soliciten al equipo una cuenta de prueba autorizada. No escriban credenciales en el documento, capturas ni chat.",
        "No realicen pagos reales, llamadas reales ni mensajes reales. Para el flujo QR usen solamente pedidos y comprobantes de prueba autorizados.",
        "Antes de iniciar, anoten: probador, modelo del dispositivo, versión de Android, fecha y versión de la aplicación.",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.1
        set_run_font(p.add_run(item), 11)

    add_heading(doc, "Datos del probador", 1)
    data = doc.add_table(rows=3, cols=4)
    data.alignment = WD_TABLE_ALIGNMENT.CENTER
    labels = [("Nombre", "", "Fecha", ""), ("Modelo del teléfono", "", "Android", ""), ("Versión de la app", "", "Conexión", "Wi-Fi / Datos / Sin conexión")]
    for row, values in enumerate(labels):
        for col, value in enumerate(values):
            table_cell(data.cell(row, col), value, header=col in (0, 2), size=10)

    add_heading(doc, "Cómo reportar un error", 1)
    add_body(doc, "Un reporte útil debe incluir el identificador de la prueba, el paso exacto, el resultado observado y evidencia. Ejemplo: P04, paso 3, se concedió permiso, se dijo limonada, pero el catálogo no se filtró; adjunto video de 10 segundos. Eviten capturas con claves, cuentas, QR reales, comprobantes reales o datos personales.")

    for test in TESTS:
        doc.add_page_break()
        add_test(doc, test)

    doc.add_page_break()
    add_heading(doc, "Cierre de la validación", 1)
    add_body(doc, "Cuando terminen, entreguen esta guía con los estados completados y una carpeta de evidencias nombradas por prueba, por ejemplo P04_voz_falla.mp4 o P08_foto_exitosa.png. El equipo revisará primero los casos Falla y Observado, reproducirá el recorrido y definirá la corrección o la mejora correspondiente.")
    add_body(doc, "Resultado general:  ☐ Aprobado para demo  ☐ Aprobado con observaciones  ☐ Requiere correcciones")
    add_body(doc, "Responsable de la validación: ______________________________    Fecha: __________________")

    doc.core_properties.title = "Guía de pruebas MVP para Grupo Neo"
    doc.core_properties.subject = "Pruebas de aceptación Brasas del Oriente"
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
