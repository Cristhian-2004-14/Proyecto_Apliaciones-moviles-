"""Agrega páginas editables para capturas a documentos de MVP y pruebas.

No modifica el Protocolo UAT ni el Acta de Conformidad.
"""

from pathlib import Path
import sys
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(r"C:\Users\Usuario\Desktop\actividad_1")
OUT = ROOT / "entregables"
COLOR = "9A542B"
GRAY = "E6E0DC"


def shade(cell, color: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color)
    tc_pr.append(shd)


def border(cell, color="B9A89D"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        tag = qn(f"w:{edge}")
        element = borders.find(tag)
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "dashed")
        element.set(qn("w:sz"), "10")
        element.set(qn("w:color"), color)


def page_break(doc):
    doc.add_page_break()


def heading(doc, title, intro):
    p = doc.add_paragraph()
    p.style = "Heading 1"
    run = p.add_run(title)
    run.font.color.rgb = RGBColor(0, 0, 0)
    p = doc.add_paragraph(intro)
    p.paragraph_format.space_after = Pt(12)


def placeholder(doc, number, title, instruction, height=2.7):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"Figura pendiente {number}. {title}")
    r.bold = True
    r.font.size = Pt(11)
    note = doc.add_paragraph(f"Qué pegar aquí: {instruction}")
    note.paragraph_format.space_after = Pt(6)
    note.runs[0].font.size = Pt(10)
    note.runs[0].font.color.rgb = RGBColor(89, 78, 72)
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    shade(cell, "FAF7F5")
    border(cell)
    row = table.rows[0]
    row.height = Inches(height)
    row.height_rule = 1
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run("PEGAR CAPTURA DE PANTALLA AQUÍ")
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(154, 84, 43)
    cap = doc.add_paragraph("Nota. Origen: captura propia tomada durante la prueba de la aplicación Brasas del Oriente, 2026.")
    cap.paragraph_format.space_after = Pt(14)
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)


def add_manual_evidence(path: Path):
    doc = Document(path)
    page_break(doc)
    heading(doc, "Espacios para capturas del MVP", "Inserte las evidencias al finalizar la prueba de cada flujo. Evite mostrar contraseñas, datos bancarios, QR funcionales o información personal de terceros.")
    items = [
        ("M1", "Catálogo con fotos reales", "Menú digital con al menos cuatro productos, foto, nombre, precio y botón para agregar al carrito."),
        ("M2", "Búsqueda por voz", "Menú digital mientras aparece Escuchando o el texto reconocido y el catálogo queda filtrado."),
        ("M3", "Pedido y estado", "Carrito con total y, después, Mis pedidos donde se observe En espera, Confirmado o Rechazado."),
        ("M4", "Reserva del cliente", "Reserva creada y la pantalla Mis pedidos y reservas con el estado mostrado."),
        ("M5", "Funciones del dueño", "Mi cuenta del dueño con accesos a fotos, gestión de reservas y verificación de pagos."),
        ("M6", "Pago QR y comprobante", "Pantalla Pago por QR o Adjuntar comprobante. Oculte número de cuenta, código de operación y QR real antes de entregar."),
    ]
    for i, (code, title, instruction) in enumerate(items):
        placeholder(doc, code, title, instruction, 2.45)
        if i in (1, 3):
            page_break(doc)
    doc.save(path)


def add_test_evidence(path: Path):
    doc = Document(path)
    page_break(doc)
    heading(doc, "Registro visual de pruebas del MVP", "Complete este anexo solo después de ejecutar cada prueba. Marque el resultado en la guía correspondiente y pegue una evidencia por caso. El Protocolo UAT y el Acta de Conformidad se mantienen sin cambios.")
    items = [
        ("P01", "Inicio y navegación", "Pantalla principal con los accesos del MVP."),
        ("P02", "Catálogo y filtro", "Menú digital con categorías o texto de búsqueda aplicado."),
        ("P03", "Consulta enviada", "Formulario completo y mensaje de confirmación de la consulta."),
        ("P04", "Búsqueda por voz", "Permiso concedido, estado de escucha o resultado reconocido."),
        ("P05", "Carrito y pedido", "Productos, cantidades, total y confirmación del pedido."),
        ("P06", "Reserva", "Reserva creada desde cliente con estado En espera."),
        ("P07", "Fotos administradas", "Pantalla Fotos de productos con una foto cargada."),
        ("P08", "Gestión de reservas", "Panel del dueño aceptando o denegando una reserva."),
        ("P09", "Pago QR", "Monto, instrucciones y carga del comprobante. Oculte datos bancarios."),
        ("P10", "Verificación de pago", "Panel del dueño comparando datos y confirmando o rechazando el pago."),
    ]
    for i, (code, title, instruction) in enumerate(items):
        # Una prueba por página evita que la captura o su nota queden partidas.
        placeholder(doc, code, title, instruction, 4.1)
        if i < len(items) - 1:
            page_break(doc)
    doc.save(path)


def create_test_evidence_workbook(path: Path):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    heading(doc, "Registro de evidencias de pruebas del MVP", "Use un espacio por cada una de las diez pruebas de la Guía MVP Grupo Neo. Escriba el resultado en la guía y pegue aquí la captura correspondiente. No incorpore contraseñas, QR funcionales, números de cuenta ni datos personales de terceros.")
    items = [
        ("P01", "Inicio y navegación", "Pantalla principal con los accesos del MVP."),
        ("P02", "Catálogo y filtro", "Menú digital con categorías o texto de búsqueda aplicado."),
        ("P03", "Consulta enviada", "Formulario completo y mensaje de confirmación de la consulta."),
        ("P04", "Búsqueda por voz", "Permiso concedido, estado de escucha o resultado reconocido."),
        ("P05", "Carrito y pedido", "Productos, cantidades, total y confirmación del pedido."),
        ("P06", "Reserva", "Reserva creada desde cliente con estado En espera."),
        ("P07", "Fotos administradas", "Pantalla Fotos de productos con una foto cargada."),
        ("P08", "Gestión de reservas", "Panel del dueño aceptando o denegando una reserva."),
        ("P09", "Pago QR", "Monto, instrucciones y carga del comprobante. Oculte datos bancarios."),
        ("P10", "Verificación de pago", "Panel del dueño comparando datos y confirmando o rechazando el pago."),
    ]
    for i, (code, title, instruction) in enumerate(items):
        if i:
            page_break(doc)
        placeholder(doc, code, title, instruction, 4.6)
    # Mantiene materializado el último cuadro al abrirlo o exportarlo en Word.
    doc.add_paragraph()
    doc.core_properties.title = "Registro de evidencias de pruebas del MVP"
    doc.save(path)


def add_report_evidence(path: Path):
    doc = Document(path)
    page_break(doc)
    heading(doc, "Anexo de capturas pendientes", "Use estas áreas para completar la evidencia del informe de pruebas. Cada captura debe corresponder al resultado indicado en la sección de pruebas y MVP.")
    placeholder(doc, "A1", "Prueba automática", "Terminal con la ejecución de flutter test o flutter analyze y resultado final visible.", 2.25)
    placeholder(doc, "A2", "Flujo principal del cliente", "Catálogo, carrito o historial de pedido con estado visible.", 2.25)
    placeholder(doc, "A3", "Flujo principal del dueño", "Gestión de reservas, fotos o verificación de pago desde la cuenta del dueño.", 2.25)
    doc.save(path)


def main():
    # MVP manual and guide/test documents only. UAT protocol intentionally excluded.
    targets = set(sys.argv[1:]) or {"manual", "guia", "informe", "registro"}
    if "manual" in targets:
        add_manual_evidence(ROOT / "documentación técnica" / "Manual_de_uso_MVP.docx")
    if "guia" in targets:
        add_test_evidence(OUT / "Guia_MVP_Grupo_Neo.docx")
    if "informe" in targets:
        add_report_evidence(OUT / "Informe_final_Brasas_del_Oriente_QA_UAT.docx")
    if "registro" in targets:
        create_test_evidence_workbook(OUT / "Registro_de_evidencias_pruebas_MVP.docx")
    print("Actualizados: Manual_de_uso_MVP, Guia_MVP_Grupo_Neo e Informe_final_Brasas_del_Oriente_QA_UAT")


if __name__ == "__main__":
    main()
