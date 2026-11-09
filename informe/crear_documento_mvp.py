from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

root = Path(r"C:\Users\Usuario\Desktop\actividad_1")
out = root / "informe" / "informe_mvp_churrasqueria_apa7_final.docx"
shots = [
    Path(r"C:\Users\Usuario\AppData\Local\Temp\codex-clipboard-286ac6dd-c613-46a7-ad38-c51f635e3be2.png"),
    Path(r"C:\Users\Usuario\AppData\Local\Temp\codex-clipboard-05328f03-4211-439c-a639-d2b6ded85166.png"),
    Path(r"C:\Users\Usuario\AppData\Local\Temp\codex-clipboard-4397ae4d-bea3-47ea-89ff-72a7663e169d.png"),
]

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(.7); sec.bottom_margin = Inches(.7)
sec.left_margin = Inches(.8); sec.right_margin = Inches(.8)
styles = doc.styles
styles['Normal'].font.name = 'Times New Roman'; styles['Normal'].font.size = Pt(12); styles['Normal'].font.color.rgb = RGBColor(0, 0, 0)
styles['Normal'].paragraph_format.line_spacing = 2
styles['Normal'].paragraph_format.space_after = Pt(0)
for name in ['Heading 1', 'Heading 2']:
    styles[name].font.name = 'Times New Roman'; styles[name].font.color.rgb = RGBColor(0, 0, 0)
    styles[name].font.size = Pt(12); styles[name].font.bold = True

title = doc.add_paragraph(); title.style = 'Title'; title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('Informe de implementación del MVP\nBrasas del Oriente'); r.font.color.rgb = RGBColor(0,0,0); r.font.name = 'Times New Roman'; r.font.size = Pt(12)
p = doc.add_paragraph('Aplicaciones Móviles I · Santa Cruz de la Sierra, Bolivia\nFecha: 8 de noviembre de 2026')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_heading('1. Objetivo', 1)
doc.add_paragraph('Desarrollar un prototipo móvil navegable para una churrasquería local, denominado Brasas del Oriente. El MVP concentra tres historias de usuario: consultar el menú digital, solicitar una reserva y consultar ubicación y horarios. La solución no incluye pagos, autenticación, base de datos ni gestión administrativa.')

doc.add_heading('2. Tecnologías y entorno', 1)
doc.add_paragraph('La aplicación se desarrolló con Flutter 3.44.2 y Dart 3.12.2. La prueba se realizó en un emulador Android 17 (API 37). El entorno utiliza Android SDK 36.1.0 y OpenJDK Temurin 17.0.21. Las licencias Android fueron aceptadas antes de compilar.')

doc.add_heading('3. Funcionalidades implementadas', 1)
table = doc.add_table(rows=1, cols=3); table.alignment = WD_TABLE_ALIGNMENT.CENTER; table.style = 'Table Grid'
for cell, text in zip(table.rows[0].cells, ['Historia', 'Implementación', 'Estado']):
    cell.text = text; cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for run in cell.paragraphs[0].runs: run.font.color.rgb = RGBColor(0, 0, 0); run.font.name = 'Times New Roman'; run.font.size = Pt(12)
for row in [
    ('HU-01 Menú digital', 'Categorías, filtros, tarjetas locales, descripciones y precios demostrativos en Bs.', 'Funcional'),
    ('HU-02 Reservar mesa', 'Formulario con validación, DatePicker sin fechas pasadas, TimePicker y resumen local.', 'Funcional'),
    ('HU-03 Ubicación y horarios', 'Dirección, horarios, contacto y enlaces a Google Maps y WhatsApp.', 'Funcional'),
]:
    cells = table.add_row().cells
    for cell, text in zip(cells, row):
        cell.text = text
        for run in cell.paragraphs[0].runs: run.font.color.rgb = RGBColor(0, 0, 0); run.font.name = 'Times New Roman'; run.font.size = Pt(12)

doc.add_heading('4. Diseño y navegación', 1)
doc.add_paragraph('Se utilizó una interfaz de tonos oscuros y cálidos asociados a la parrilla, con botones grandes, tarjetas y espaciado adaptable. El flujo es: bienvenida → pantalla principal → menú, reserva o ubicación. Cada pantalla incluye una barra superior para regresar al inicio.')

doc.add_heading('5. Evidencias de ejecución', 1)
captions = [
    'Figura 1\nDiagnóstico del entorno Android con SDK, Java y licencias aceptadas.',
    'Figura 2\nPantalla de bienvenida de Brasas del Oriente ejecutada en el emulador.',
    'Figura 3\nPantalla principal con los tres accesos del MVP.',
]
for image, caption in zip(shots, captions):
    if image.exists():
        par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.add_run().add_picture(str(image), width=Inches(5.8))
        cap = doc.add_paragraph(caption); cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        cap.runs[0].bold = True

doc.add_heading('6. Validación', 1)
doc.add_paragraph('Se ejecutaron dart format, flutter analyze y flutter test. El análisis no reportó incidencias y la prueba de widget aprobó la navegación desde la bienvenida hacia la pantalla principal. También se generó e instaló el APK de depuración en el emulador Android.')

doc.add_heading('7. Elementos demostrativos y limitaciones', 1)
doc.add_paragraph('Los productos, precios, dirección, teléfono y horarios son datos demostrativos centralizados en el código. La reserva es una simulación local: muestra un resumen y no confirma disponibilidad real. Los enlaces externos dependen de que el dispositivo cuente con Google Maps o WhatsApp.')

doc.add_heading('8. Conclusión', 1)
doc.add_paragraph('El MVP permite demostrar las tres historias de usuario prioritarias de una churrasquería sin depender de servicios externos. La estructura permite incorporar posteriormente persistencia de datos, confirmación de reservas y contenido real del restaurante.')
doc.add_heading('9. Repositorio del proyecto', 1)
doc.add_paragraph('El código fuente, las evidencias y los documentos del proyecto se encuentran disponibles en el siguiente repositorio de GitHub: https://github.com/Cristhian-2004-14/Proyecto_Apliaciones-moviles-.git')
doc.save(out)
print(out)
