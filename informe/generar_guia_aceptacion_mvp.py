from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "entregables" / "Guia_de_validacion_y_aceptacion_MVP_Grupo_Neo_final.docx"


def set_font(run, size=12, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def page_field(run):
    for tag, text in (("begin", None), ("instrText", " PAGE "), ("separate", None), ("t", "1"), ("end", None)):
        node = OxmlElement(f"w:{'fldChar' if tag in ('begin', 'separate', 'end') else tag}")
        if tag in ("begin", "separate", "end"):
            node.set(qn("w:fldCharType"), tag)
        elif tag == "instrText":
            node.set(qn("xml:space"), "preserve")
            node.text = text
        else:
            node.text = text
        run._r.append(node)


def shade(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    node = OxmlElement("w:shd")
    node.set(qn("w:fill"), color)
    tc_pr.append(node)


def borders(cell, color="D9D9D9"):
    tc_pr = cell._tc.get_or_add_tcPr()
    node = tc_pr.first_child_found_in("w:tcBorders")
    if node is None:
        node = OxmlElement("w:tcBorders")
        tc_pr.append(node)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge_node = node.find(qn(f"w:{edge}"))
        if edge_node is None:
            edge_node = OxmlElement(f"w:{edge}")
            node.append(edge_node)
        edge_node.set(qn("w:val"), "single")
        edge_node.set(qn("w:sz"), "6")
        edge_node.set(qn("w:color"), color)


def margins(cell, top=100, start=120, bottom=100, end=120):
    tc_pr = cell._tc.get_or_add_tcPr()
    node = tc_pr.first_child_found_in("w:tcMar")
    if node is None:
        node = OxmlElement("w:tcMar")
        tc_pr.append(node)
    for side, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        side_node = node.find(qn(f"w:{side}"))
        if side_node is None:
            side_node = OxmlElement(f"w:{side}")
            node.append(side_node)
        side_node.set(qn("w:w"), str(value))
        side_node.set(qn("w:type"), "dxa")


def normal_paragraph(doc, text="", before=0, after=0, first=0, align=None):
    p = doc.add_paragraph(style="Normal")
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.5
    if first:
        p.paragraph_format.first_line_indent = Inches(first)
    if align is not None:
        p.alignment = align
    set_font(p.add_run(text))
    return p


def title(doc, text):
    p = doc.add_paragraph(style="Normal")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.5
    set_font(p.add_run(text), bold=True)
    return p


def heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(text), bold=True)
    return p


def record_table(doc, entries):
    table = doc.add_table(rows=0, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for label, value in entries:
        row = table.add_row()
        left, right = row.cells
        left.width = Inches(1.45)
        right.width = Inches(5.05)
        for cell in (left, right):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            borders(cell)
            margins(cell)
        shade(left, "EAEAEA")
        lp = left.paragraphs[0]
        lp.paragraph_format.line_spacing = 1.15
        set_font(lp.add_run(label), size=10, bold=True)
        rp = right.paragraphs[0]
        rp.paragraph_format.line_spacing = 1.15
        set_font(rp.add_run(value), size=10)
    normal_paragraph(doc, "", after=3)


def checklist(doc, items):
    for item in items:
        p = doc.add_paragraph(style="Normal")
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        p.paragraph_format.line_spacing = 1.35
        set_font(p.add_run("[ ] " + item), size=11)


def configure(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.85)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)
    styles = doc.styles
    for style_name in ("Normal", "Title", "Heading 1", "Heading 2"):
        style = styles[style_name]
        style.font.name = "Times New Roman"
        style._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        style._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        style.font.color.rgb = RGBColor(0, 0, 0)
    styles["Normal"].font.size = Pt(12)
    styles["Title"].font.size = Pt(16)
    styles["Heading 1"].font.size = Pt(13)
    styles["Heading 2"].font.size = Pt(12)
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_font(header.add_run("Brasas del Oriente | Guía MVP"), size=9)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(footer.add_run("Página "), size=9)
    page_field(footer.add_run())


CASES = [
    ("UAT-01", "Acceso y navegación principal", "Confirmar que el usuario puede reconocer y recorrer las funciones centrales del MVP.", "1. Abra la aplicación. 2. Revise las opciones de la pantalla principal. 3. Entre y vuelva desde Menú, Mi pedido, Mi cuenta, Reservar mesa, Enviar consulta y Ubicación.", "La pantalla inicial carga sin errores y cada opción abre su pantalla correspondiente. El botón Atrás permite regresar sin cerrar inesperadamente la aplicación."),
    ("UAT-02", "Catálogo con fotos reales y filtros", "Comprobar que el catálogo presenta información útil y fotografías asociadas a los productos.", "1. Abra Ver menú. 2. Revise al menos cinco productos. 3. Seleccione una categoría. 4. Quite el filtro. 5. Desplácese por el listado.", "Cada producto muestra nombre, descripción, precio y fotografía disponible. El filtro muestra solo la categoría elegida. No aparecen franjas rojas ni mensajes de desbordamiento."),
    ("UAT-03", "Búsqueda por voz", "Validar que una búsqueda hablada filtra el catálogo cuando el permiso está concedido.", "1. En el menú, pulse el micrófono. 2. Conceda el permiso de micrófono si el sistema lo solicita. 3. Diga el nombre de un producto, por ejemplo limonada. 4. Detenga la escucha.", "El texto reconocido se coloca en el campo de búsqueda y se muestran los productos relacionados. Si se niega el permiso, la aplicación informa el caso sin cerrarse."),
    ("UAT-04", "Carrito y creación de pedido", "Confirmar el recorrido de compra básico del cliente.", "1. Agregue dos productos desde el menú. 2. Abra Mi pedido. 3. Modifique una cantidad. 4. Revise el total. 5. Confirme el pedido con nombre y teléfono de prueba.", "Las cantidades y el total se actualizan de forma correcta. Al confirmar, se registra el pedido y aparece una confirmación comprensible para el cliente."),
    ("UAT-05", "Consulta y reserva", "Comprobar que las solicitudes no comerciales se guardan y pueden continuar su flujo.", "1. Abra Enviar consulta, complete datos de prueba y envíe. 2. Abra Reservar mesa, complete los datos de prueba y cree la reserva. 3. Regrese a Mi cuenta.", "La consulta informa que fue enviada. La reserva se crea con estado EN ESPERA y queda disponible para la gestión del dueño."),
    ("UAT-06", "Historial del cliente", "Validar la visibilidad de pedidos, pagos y reservas creados por la cuenta del cliente.", "1. Inicie sesión como cliente. 2. Abra Mi cuenta. 3. Seleccione Mis pedidos y reservas. 4. Revise las secciones de pedidos, reservas y pagos.", "El historial carga los registros del cliente autenticado. Las reservas reflejan EN ESPERA, CONFIRMADA o RECHAZADA según la decisión del dueño. Los pagos muestran su estado disponible."),
    ("UAT-07", "Funciones del dueño", "Verificar que los accesos administrativos están restringidos al rol dueño.", "1. Inicie sesión como dueño. 2. Abra Mi cuenta. 3. Revise los botones de panel, fotos, reservas y pagos. 4. Cierre sesión e ingrese como cliente.", "Las opciones administrativas aparecen únicamente para el dueño. La cuenta cliente no puede acceder a gestión de fotos, reservas ni verificación de pagos."),
    ("UAT-08", "Gestión de reservas", "Confirmar que el dueño puede responder las reservas y que el cliente recibe el nuevo estado.", "1. Como dueño, abra Gestionar reservas. 2. Seleccione una reserva EN ESPERA. 3. Confirme o rechace. 4. Como cliente, abra el historial y actualice la vista.", "La reserva cambia a CONFIRMADA o RECHAZADA. El cambio se conserva al volver a abrir la aplicación y es visible para el cliente correcto."),
    ("UAT-09", "Pago QR y comprobante", "Validar el flujo documental de pago sin afirmar una transferencia bancaria automática.", "1. Cree o abra un pedido. 2. Seleccione Pago por QR. 3. Revise el total. 4. Adjunte una imagen de comprobante de prueba. 5. Como dueño, abra Verificación de pagos y confirme o rechace el abono.", "La aplicación muestra el QR configurado, permite adjuntar JPG o PNG y deja el estado en REVISIÓN MANUAL. El dueño puede confirmar o rechazar; el cliente visualiza el resultado. No se realiza un cobro bancario automático."),
    ("UAT-10", "Ubicación clima y respuesta ante error", "Comprobar los servicios externos principales y su manejo de fallas.", "1. Abra Ubicación y horarios. 2. Revise ubicación, horario y clima. 3. Abra el mapa. 4. Para una prueba controlada, niegue el permiso del micrófono o desactive momentáneamente la conexión antes de reintentar una función externa.", "La información de contacto y ubicación es visible, el mapa se abre y el clima se consulta cuando hay conexión. En ausencia de permiso o red se muestra un mensaje de error o reintento, sin bloquear la aplicación."),
]


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    configure(doc)

    for _ in range(5):
        doc.add_paragraph()
    title(doc, "Guía de validación y aceptación del MVP de Brasas del Oriente")
    normal_paragraph(doc, "Documento de presentación y prueba para Grupo Neo", before=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    normal_paragraph(doc, "Propósito: validar el recorrido principal y las funciones esenciales antes de la entrega del sistema.", before=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    for line in ("Proyecto: Brasas del Oriente", "Fecha de prueba: ____ / ____ / 2026", "Responsable del cliente: ______________________________", "Responsable del equipo: ______________________________"):
        normal_paragraph(doc, line, before=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    heading(doc, "1. Propósito y alcance")
    normal_paragraph(doc, "Esta guía permite a Grupo Neo comprobar el MVP de Brasas del Oriente mediante diez pruebas guiadas. El alcance se concentra en los recorridos que dan valor inmediato: explorar el menú, buscar un producto, crear un pedido o una reserva, consultar el historial, administrar solicitudes desde el rol dueño y revisar el flujo documental de pago QR.", first=0.4)
    normal_paragraph(doc, "La prueba no autoriza movimientos bancarios reales. Para el caso de pago QR se debe usar una captura de comprobante de demostración o material autorizado por el equipo. La confirmación final del pago se mantiene manual porque no existe una pasarela bancaria integrada.", first=0.4)
    heading(doc, "2. Preparación antes de iniciar")
    checklist(doc, [
        "Usar un teléfono Android o emulador con la versión actual de la aplicación instalada.",
        "Conectar el dispositivo a internet para Supabase, clima, Storage y mapa.",
        "Disponer de una cuenta de cliente y una cuenta de dueño creadas por el equipo.",
        "Permitir el micrófono solo para la prueba UAT-03.",
        "Usar datos de prueba para nombre, teléfono, pedidos, reservas y comprobantes.",
        "Tomar una captura cuando un resultado no coincida con lo esperado.",
    ])
    heading(doc, "3. Registro de resultados")
    normal_paragraph(doc, "Para cada caso marque un único resultado y describa las observaciones. Un caso Aprobado cumple todos sus criterios; Observado funciona parcialmente o requiere ajuste menor; No aprobado impide completar el recorrido o muestra información incorrecta.", first=0.4)
    record_table(doc, [
        ("Estado", "[ ] Aprobado     [ ] Observado     [ ] No aprobado"),
        ("Resultado", "Describa brevemente lo ocurrido: ________________________________________________"),
        ("Evidencia", "Nombre de captura, video o fecha de prueba: _______________________________________"),
        ("Observación", "________________________________________________________________________________"),
    ])

    heading(doc, "4. Casos de prueba del recorrido principal")
    for index, (case_id, name, objective, steps, expected) in enumerate(CASES, start=1):
        heading(doc, f"{case_id}  {name}", 2)
        record_table(doc, [
            ("Objetivo", objective),
            ("Pasos", steps),
            ("Resultado esperado", expected),
            ("Estado", "[ ] Aprobado     [ ] Observado     [ ] No aprobado"),
            ("Resultado obtenido", "________________________________________________________________________________"),
            ("Evidencia u observación", "________________________________________________________________________________"),
        ])
        if index in (2, 4, 6, 8):
            doc.add_page_break()

    heading(doc, "5. Cierre y aceptación")
    normal_paragraph(doc, "Al concluir las pruebas, el representante de Grupo Neo debe registrar el resultado general. La firma confirma que se revisó el MVP en el ambiente de demostración descrito en esta guía; no sustituye una certificación bancaria ni una auditoría de seguridad de producción.", first=0.4)
    record_table(doc, [
        ("Resultado general", "[ ] Aceptado     [ ] Aceptado con observaciones     [ ] No aceptado"),
        ("Observaciones finales", "________________________________________________________________________________\n________________________________________________________________________________\n________________________________________________________________________________"),
        ("Compromiso de corrección", "________________________________________________________________________________"),
    ])
    normal_paragraph(doc, "Firma del representante de Grupo Neo: ______________________________________", before=24)
    normal_paragraph(doc, "Nombre completo: __________________________________    Fecha: ____ / ____ / 2026", before=10)
    normal_paragraph(doc, "Firma del responsable del equipo: _________________________________________", before=24)
    normal_paragraph(doc, "Nombre completo: __________________________________    Fecha: ____ / ____ / 2026", before=10)

    doc.core_properties.title = "Guía de validación y aceptación del MVP de Brasas del Oriente"
    doc.core_properties.subject = "Pruebas UAT y acta de aceptación"
    doc.core_properties.author = ""
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
