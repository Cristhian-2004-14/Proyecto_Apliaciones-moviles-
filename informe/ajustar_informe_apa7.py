"""Ajusta el informe final ya generado sin alterar su contenido técnico.

Reduce las evidencias visuales para que ninguna exceda media página e
incorpora los rótulos de tablas requeridos por el estilo APA 7.
"""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


SOURCE = Path(__file__).resolve().parents[1] / "entregables" / "Informe_final_APA7_Brasas_del_Oriente.docx"
REPORT = Path(__file__).resolve().parents[1] / "entregables" / "Informe_final_APA7_Brasas_del_Oriente_Ajustado.docx"

TABLES = [
    ("Tabla 1", "Componentes y controles de la arquitectura de la aplicación."),
    ("Tabla 2", "Comparación entre el flujo QR implementado y una pasarela SIP directa."),
    ("Tabla 3", "Resultados de las pruebas funcionales y automatizadas."),
    ("Tabla A1", "Scripts y configuración relevante para reproducir las integraciones."),
]


def set_run_font(run, size=12, *, bold=False, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def new_paragraph(doc, text, *, bold=False, italic=False, size=12):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 2
    run = paragraph.add_run(text)
    set_run_font(run, size, bold=bold, italic=italic)
    return paragraph


def insert_after(paragraph, anchor):
    anchor.addnext(paragraph._p)


def enable_toc_update(doc):
    """Pide a Word actualizar los campos del índice al abrir el documento."""
    settings = doc.settings.element
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    settings.append(update)


def main():
    doc = Document(SOURCE)

    # APA 7 para trabajos estudiantiles utiliza márgenes de una pulgada.
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Las capturas verticales se limitan a 3.55 pulgadas de alto, dejando
    # espacio suficiente para título y leyenda dentro de media página.
    for shape in doc.inline_shapes:
        if shape.height > Inches(3.55):
            ratio = shape.width / shape.height
            shape.height = Inches(3.55)
            shape.width = int(shape.height * ratio)

    # Evita duplicar rótulos si el ajuste se ejecuta más de una vez.
    existing = {p.text.strip() for p in doc.paragraphs}
    for table, (label, title) in zip(doc.tables, TABLES):
        if label in existing:
            continue
        label_p = new_paragraph(doc, label, bold=True)
        title_p = new_paragraph(doc, title, italic=True)
        label_p.paragraph_format.space_before = Pt(12)
        title_p.paragraph_format.space_before = Pt(0)
        table._element.addprevious(title_p._p)
        table._element.addprevious(label_p._p)

        note_p = new_paragraph(doc, "Nota. Elaboración propia.", italic=True, size=10)
        note_p.paragraph_format.line_spacing = 1
        note_p.paragraph_format.space_before = Pt(3)
        insert_after(note_p, table._element)

    enable_toc_update(doc)
    doc.save(REPORT)
    print(REPORT)


if __name__ == "__main__":
    main()
