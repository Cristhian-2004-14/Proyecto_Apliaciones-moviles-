"""Prepara la versión de entrega con índice, notas de evidencia y primera hoja en blanco."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "entregables" / "Informe_final_APA7_Brasas_del_Oriente_Ajustado.docx"
OUT = ROOT / "entregables" / "Informe_final_APA7_Brasas_del_Oriente_Entrega.docx"

FIGURE_NOTES = {
    "Figura 1.": "Nota. Origen: captura propia tomada en la aplicación. Muestra el panel que permite al dueño cargar o reemplazar fotografías reales del catálogo.",
    "Figura 2.": "Nota. Origen: captura propia tomada en la aplicación. Muestra las opciones protegidas que se habilitan únicamente para el rol dueño.",
    "Figura 3.": "Nota. Origen: captura propia tomada en la aplicación. Muestra el formulario de consulta y el mensaje que confirma su registro.",
    "Figura 4.": "Nota. Origen: captura propia tomada en la aplicación. Muestra la selección de un comprobante y la advertencia sobre el alcance documental del OCR.",
    "Figura A1.": "Nota. Origen: captura propia tomada en la aplicación. Muestra la pantalla principal y sus módulos de acceso.",
    "Figura A2.": "Nota. Origen: captura propia tomada en la aplicación. Muestra productos con fotos cargadas y administrables por el dueño.",
    "Figura A3.": "Nota. Origen: captura propia tomada en la aplicación. Muestra una consulta registrada correctamente.",
    "Figura A4.": "Nota. Origen: captura propia tomada en la aplicación. Muestra el flujo para adjuntar un comprobante sin afirmar una confirmación bancaria automática.",
}

TABLE_NOTES = [
    "Nota. Origen: elaboración propia a partir de la implementación. Muestra los componentes de Flutter, Supabase y los controles aplicados.",
    "Nota. Origen: elaboración propia. Muestra la diferencia entre la alternativa QR con revisión manual y una pasarela SIP directa teórica.",
    "Nota. Origen: elaboración propia a partir de las pruebas ejecutadas. Muestra los casos validados y sus resultados observados.",
    "Nota. Origen: elaboración propia a partir del repositorio. Muestra los scripts y archivos necesarios para reproducir las integraciones.",
]


def set_run_font(run, size=10, *, italic=False):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    run._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    run.font.size = Pt(size)
    run.italic = italic


def note_paragraph(doc, text):
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1
    run = paragraph.add_run(text)
    set_run_font(run, 10, italic=True)
    return paragraph


def insert_after(paragraph, anchor):
    anchor.addnext(paragraph._p)


def first_body_paragraph_with_text(doc, target):
    for paragraph in doc.paragraphs:
        if paragraph.text.strip() == target:
            return paragraph
    raise ValueError(f"No se encontró el apartado: {target}")


def page_break_element():
    p = OxmlElement("w:p")
    r = OxmlElement("w:r")
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    r.append(br)
    p.append(r)
    return p


def set_text(paragraph, text):
    paragraph.clear()
    run = paragraph.add_run(text)
    set_run_font(run, 10, italic=True)
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(8)
    paragraph.paragraph_format.line_spacing = 1


def enable_toc_update(doc):
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings.element.append(update)


def main():
    doc = Document(SOURCE)
    index = first_body_paragraph_with_text(doc, "Índice")
    body = doc._element.body

    # Elimina portada y resumen: deja una primera hoja en blanco y el índice
    # inicia en la segunda hoja.
    index_element = index._p
    for child in list(body):
        if child is index_element:
            break
        body.remove(child)
    body.insert(0, page_break_element())

    # Añade notas explicativas bajo las leyendas de evidencia.
    for paragraph in list(doc.paragraphs):
        text = paragraph.text.strip()
        for label, note in FIGURE_NOTES.items():
            if text.startswith(label):
                added = note_paragraph(doc, note)
                insert_after(added, paragraph._p)
                break

    # Sustituye la nota genérica de cada tabla por una que explica su origen y
    # el contenido evidenciado.
    generic_notes = [p for p in doc.paragraphs if p.text.strip() == "Nota. Elaboración propia."]
    for paragraph, note in zip(generic_notes, TABLE_NOTES):
        set_text(paragraph, note)

    enable_toc_update(doc)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
