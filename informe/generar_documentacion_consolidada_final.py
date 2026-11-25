"""Genera tres documentos finales consolidados para Brasas del Oriente.

No incluye QR real, números de cuenta completos ni credenciales.
"""

from pathlib import Path
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image

ROOT = Path(r"C:\Users\Usuario\Desktop\actividad_1")
DESKTOP = Path(r"C:\Users\Usuario\Desktop")
OUT = ROOT / "entregables" / "Documentacion_Final_Consolidada"
DATE = "25 de noviembre de 2026"
PROJECT = "Brasas del Oriente"
ACCENT = "A2572C"
DARK = "2A1B16"
LIGHT = "F8EEE8"
GRAY = "F2F2F2"

IMAGES = {
    "inicio": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.31.jpeg",
    "catalogo": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.32.jpeg",
    "voz": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.32 (1).jpeg",
    "carrito": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.32 (2).jpeg",
    "pedidos": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.33 (1).jpeg",
    "comprobante": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.33 (3).jpeg",
    "reserva": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.36 (2).jpeg",
    # Evidencia sin datos personales: estado confirmado visible para el cliente.
    "gestionar": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.34 (1).jpeg",
    "ubicacion": DESKTOP / "WhatsApp Image 2026-11-25 at 01.05.36 (1).jpeg",
}


def prepare_images():
    """Normaliza las capturas para que Word las inserte sin problemas."""
    assets = ROOT / "informe" / "capturas_documentacion"
    assets.mkdir(parents=True, exist_ok=True)
    for key, source in list(IMAGES.items()):
        target = assets / f"{key}.jpg"
        with Image.open(source) as img:
            img.convert("RGB").save(target, "JPEG", quality=88, optimize=True)
        IMAGES[key] = target


def shade(cell, color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color)
    tc_pr.append(shd)


def borders(table):
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    b = tbl_pr.first_child_found_in("w:tblBorders")
    if b is None:
        b = OxmlElement("w:tblBorders")
        tbl_pr.append(b)
    for name in ["top", "left", "bottom", "right", "insideH", "insideV"]:
        edge = b.find(qn(f"w:{name}"))
        if edge is None:
            edge = OxmlElement(f"w:{name}")
            b.append(edge)
        edge.set(qn("w:val"), "single")
        edge.set(qn("w:sz"), "5")
        edge.set(qn("w:color"), "D9D9D9")


def setup(doc, title):
    sec = doc.sections[0]
    sec.top_margin = Inches(0.75)
    sec.bottom_margin = Inches(0.7)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(7)
    for name, size in [("Title", 24), ("Heading 1", 16), ("Heading 2", 12)]:
        style = styles[name]
        style.font.name = "Arial"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = footer.add_run(f"{PROJECT} · {DATE}")
    r.font.name = "Arial"
    r.font.size = Pt(8)
    doc.core_properties.title = title
    doc.core_properties.subject = PROJECT
    doc.core_properties.author = "Equipo de desarrollo del proyecto"


def add_cover(doc, title, subtitle):
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(title)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(subtitle)
    r.italic = True
    r.font.size = Pt(13)
    doc.add_paragraph()
    for label, value in [
        ("Proyecto", PROJECT),
        ("Responsable", "Equipo de desarrollo del proyecto"),
        ("Fecha", DATE),
        ("Versión", "1.0 final"),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(f"{label}: ").bold = True
        p.add_run(value)
    doc.add_page_break()


def heading(doc, text):
    p = doc.add_paragraph(text, style="Heading 1")
    p.paragraph_format.space_before = Pt(8)
    return p


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    borders(table)
    header = table.rows[0].cells
    for i, item in enumerate(headers):
        header[i].text = item
        shade(header[i], DARK)
        for run in header[i].paragraphs[0].runs:
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True
            run.font.size = Pt(9)
        header[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for row_index, row_data in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row_data):
            cells[i].text = value
            cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if row_index % 2 == 1:
                shade(cells[i], "FAFAFA")
            for para in cells[i].paragraphs:
                for run in para.runs:
                    run.font.size = Pt(8.5)
    if widths:
        for row in table.rows:
            for cell, width in zip(row.cells, widths):
                cell.width = Inches(width)
    doc.add_paragraph()
    return table


def add_figure_pair(doc, figures):
    table = doc.add_table(rows=1, cols=len(figures))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for cell, (title, description, image_path) in zip(table.rows[0].cells, figures):
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if image_path.exists():
            p.add_run().add_picture(str(image_path), width=Inches(1.62))
        cap = cell.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run(title)
        r.bold = True
        r.font.size = Pt(8.5)
        note = cell.add_paragraph(description)
        note.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in note.runs:
            run.italic = True
            run.font.size = Pt(7.5)
    doc.add_paragraph("Nota. Origen de las figuras: capturas propias de la aplicación Brasas del Oriente, tomadas durante pruebas del proyecto el 25 de noviembre de 2026.").runs[0].italic = True
    doc.add_paragraph()


def add_uat_step(doc, number, role, objective, actions, expected, evidence):
    p = doc.add_paragraph(style="Heading 2")
    p.add_run(f"Paso {number}. {objective}")
    doc.add_paragraph(f"Rol que realiza la prueba: {role}.")
    doc.add_paragraph("Acciones: " + actions)
    doc.add_paragraph("Resultado esperado: " + expected)
    doc.add_paragraph("Registro de evidencia: " + evidence)
    doc.add_paragraph("Resultado observado: ________________________________________________________________")
    doc.add_paragraph("Observaciones o incidencia: __________________________________________________________")


def create_uat():
    doc = Document()
    setup(doc, "Protocolo UAT y Acta de Conformidad")
    add_cover(doc, "Protocolo UAT y Acta de Conformidad", "Validación de aceptación del producto mínimo viable")
    heading(doc, "Objetivo")
    doc.add_paragraph("Este documento guía la validación final del producto mínimo viable de Brasas del Oriente. La persona revisora debe ejecutar los recorridos indicados, comparar el resultado con lo esperado y registrar observaciones antes de aceptar la entrega.")
    heading(doc, "Alcance y condiciones")
    add_table(doc, ["Elemento", "Condición de prueba"], [
        ("Aplicación", "APK final instalada o proyecto ejecutado con Flutter y Supabase configurado."),
        ("Roles", "Una cuenta cliente y una cuenta autorizada con rol dueño."),
        ("Datos", "Productos, fotos, reservas y pedidos de demostración disponibles."),
        ("Privacidad", "No registrar contraseñas, QR reales, números de cuenta ni comprobantes bancarios reales."),
    ], [1.4, 4.9])
    heading(doc, "Casos de aceptación")
    cases = [
        ("UAT 01", "Catálogo", "Abrir Menú digital y comprobar productos, fotos, precios y categorías.", "El catálogo muestra información y permite agregar un producto."),
        ("UAT 02", "Búsqueda por voz", "Activar micrófono, conceder permiso y decir un producto.", "El texto reconocido filtra el catálogo o informa un error controlado."),
        ("UAT 03", "Pedido", "Crear un pedido y revisar Mis pedidos.", "El pedido se registra y muestra En espera, Confirmado o Rechazado."),
        ("UAT 04", "Reserva", "Crear una reserva y revisarla desde la cuenta cliente.", "La reserva queda registrada con su estado visible."),
        ("UAT 05", "Gestión del dueño", "Ingresar como dueño y gestionar una reserva.", "El dueño puede aceptar o denegar y el cliente ve el cambio."),
        ("UAT 06", "Fotos", "Ingresar como dueño y abrir Fotos de productos.", "El dueño puede cargar o reemplazar una foto del catálogo."),
        ("UAT 07", "Pago QR", "Consultar el pago QR, adjuntar comprobante de demostración y revisar desde dueño.", "El comprobante pasa a revisión manual. El dueño confirma o rechaza tras constatar el abono."),
        ("UAT 08", "Ubicación", "Abrir Ubicación y horarios.", "Se muestran horario, contacto, clima y acceso al mapa."),
    ]
    rows = [(a, b, c, d, "☐ Conforme  ☐ No conforme", "") for a, b, c, d in cases]
    add_table(doc, ["ID", "Módulo", "Paso", "Resultado esperado", "Resultado", "Observaciones"], rows, [0.55, 0.9, 1.35, 1.6, 1.1, 0.95])
    doc.add_page_break()
    heading(doc, "Recorrido UAT completo de principio a fin")
    doc.add_paragraph("El siguiente recorrido debe ejecutarse en el orden indicado. Inicia como cliente, genera una solicitud de pedido y una reserva, y termina como dueño validando las operaciones. Si un paso falla, se debe registrar la incidencia y no continuar con la aceptación hasta que se defina su tratamiento.")
    add_uat_step(doc, "1", "Cliente", "Iniciar la aplicación", "Abrir la APK y pulsar Entrar a la churrasquería.", "Se muestra la pantalla principal sin cierre inesperado y se puede acceder a las funciones del MVP.", "Captura de la pantalla de bienvenida.")
    add_uat_step(doc, "2", "Cliente", "Explorar el catálogo", "Abrir Menú digital, revisar categorías, precios, fotografías y descripciones; usar también el campo de búsqueda por texto.", "La lista se carga, las categorías filtran los productos y cada producto se presenta con precio y descripción.", "Captura del catálogo filtrado o completo.")
    add_figure_pair(doc, [
        ("Figura U1. Inicio", "Acceso inicial al MVP.", IMAGES["inicio"]),
        ("Figura U2. Catálogo", "Productos, precios y fotografías.", IMAGES["catalogo"]),
    ])
    add_uat_step(doc, "3", "Cliente", "Probar la búsqueda por voz", "Pulsar el micrófono, conceder permiso si Android lo solicita y pronunciar el nombre de un producto existente.", "La aplicación entra en modo de escucha y aplica el texto reconocido al filtro, o presenta un mensaje controlado si el servicio no está disponible.", "Captura del estado Escuchando o del resultado filtrado.")
    add_uat_step(doc, "4", "Cliente", "Construir el carrito", "Pulsar el botón más en al menos dos productos, abrir Mi pedido, modificar una cantidad y verificar el total.", "Las cantidades cambian de forma coherente y el total corresponde a la suma de precios y cantidades.", "Captura del carrito antes de confirmar.")
    add_figure_pair(doc, [
        ("Figura U3. Voz", "Reconocimiento de voz activado.", IMAGES["voz"]),
        ("Figura U4. Carrito", "Productos, cantidades y total.", IMAGES["carrito"]),
    ])
    doc.add_page_break()
    add_uat_step(doc, "5", "Cliente", "Registrar el pedido", "Pulsar Confirmar pedido, completar nombre y teléfono de prueba y pulsar Registrar pedido.", "El pedido se almacena y el sistema informa que queda pendiente de disponibilidad y revisión de pago.", "Anotar número de pedido y monto mostrado.")
    add_uat_step(doc, "6", "Cliente", "Adjuntar comprobante de demostración", "Desde la pantalla de pago seleccionar una imagen JPG o PNG de prueba de hasta 5 MB y pulsar Validar y enviar.", "La aplicación confirma la recepción del archivo y cambia el pago a revisión manual. El comprobante no debe interpretarse como pago confirmado.", "Captura de la pantalla de adjuntar comprobante o del mensaje de recepción.")
    add_uat_step(doc, "7", "Dueño", "Revisar pago y contrastar datos", "Iniciar sesión con una cuenta autorizada de dueño, abrir Verificación de pagos y seleccionar el pedido creado.", "Se visualiza el monto esperado y la información extraída o disponible para comparación. El dueño conserva la decisión final después de verificar el abono real.", "Registrar si el pago quedó confirmado o rechazado y la observación utilizada.")
    add_figure_pair(doc, [
        ("Figura U5. Comprobante", "Archivo seleccionado para revisión.", IMAGES["comprobante"]),
        ("Figura U6. Estados", "Historial de pedidos del cliente.", IMAGES["pedidos"]),
    ])
    add_uat_step(doc, "8", "Cliente", "Comprobar el estado del pedido", "Volver a la cuenta cliente y abrir Mis pedidos y reservas, pestaña Pedidos.", "El pedido creado muestra En espera mientras se revisa; tras la decisión del dueño muestra Confirmado o Rechazado junto con el estado de pago correspondiente.", "Captura o anotación del estado antes y después de la decisión.")
    doc.add_page_break()
    add_uat_step(doc, "9", "Cliente", "Crear una reserva", "Abrir Reservar mesa, completar nombre y teléfono de prueba, elegir fecha, hora y número de personas; pulsar Confirmar reserva.", "La reserva queda registrada inicialmente en espera y se visualiza en la pestaña Reservas del historial del cliente.", "Anotar fecha, hora y estado inicial.")
    add_uat_step(doc, "10", "Dueño", "Gestionar la reserva", "Con sesión de dueño abrir Gestionar reservas, identificar la reserva creada y elegir Aceptar o Denegar.", "El estado se actualiza y el cliente puede observar el resultado al refrescar la pestaña Reservas.", "Registrar la decisión y validar la visibilidad para el cliente.")
    add_figure_pair(doc, [
        ("Figura U7. Reserva", "Formulario de solicitud del cliente.", IMAGES["reserva"]),
        ("Figura U8. Estado", "Reserva confirmada visible al cliente.", IMAGES["gestionar"]),
    ])
    add_uat_step(doc, "11", "Dueño", "Actualizar fotografías del catálogo", "Abrir Mi cuenta, ingresar a Gestionar fotos de productos, elegir un producto y seleccionar una imagen de prueba.", "La carga finaliza sin error, se actualiza el listado de fotos y el catálogo muestra la imagen al volver a abrirlo.", "Indicar producto actualizado y resultado.")
    add_uat_step(doc, "12", "Cliente", "Consultar información y cerrar el recorrido", "Abrir Ubicación y horarios y verificar ubicación, horarios, clima, llamada, WhatsApp y mapa. Finalmente enviar una consulta breve desde Enviar consulta.", "Se muestran los datos informativos y la consulta se registra con el mensaje de confirmación correspondiente.", "Captura de ubicación o anotación de la consulta enviada.")
    add_figure_pair(doc, [
        ("Figura U9. Ubicación", "Horario, contacto y clima.", IMAGES["ubicacion"]),
        ("Figura U10. Reserva", "Resultado de la gestión.", IMAGES["gestionar"]),
    ])
    heading(doc, "Criterio de aceptación")
    doc.add_paragraph("El MVP se considera aceptado cuando los doce pasos se ejecutan sin defectos bloqueantes, los datos se conservan al navegar entre pantallas y los estados del pedido y de la reserva cambian según las acciones autorizadas del dueño. Los defectos no bloqueantes deben anotarse en el acta con una fecha de corrección acordada.")
    heading(doc, "Acta de conformidad")
    doc.add_paragraph("La persona revisora declara que ejecutó los casos anteriores y registró los hallazgos correspondientes. La aceptación aplica al alcance del MVP descrito en este documento.")
    add_table(doc, ["Campo", "Registro"], [
        ("Resultado general", "☐ Conforme   ☐ Conforme con observaciones   ☐ No conforme"),
        ("Observaciones finales", "________________________________________________________________________________"),
        ("Nombre de la persona revisora", "________________________________________________________________________________"),
        ("Firma", "________________________________________________________________________________"),
        ("Fecha", DATE),
    ], [2.1, 4.2])
    path = OUT / "01_Protocolo_UAT_y_Acta_de_Conformidad.docx"
    doc.save(path)
    return path


def create_tests():
    doc = Document()
    setup(doc, "Pruebas y Evidencias del MVP")
    add_cover(doc, "Pruebas y Evidencias del MVP", "Registro funcional y visual de Brasas del Oriente")
    heading(doc, "Estrategia de pruebas")
    doc.add_paragraph("Las pruebas combinaron análisis estático, ejecución de recorridos manuales y evidencia visual obtenida desde un dispositivo Android. Las capturas muestran la versión funcional del producto y se vinculan con las funciones principales del MVP.")
    add_table(doc, ["Tipo", "Acción", "Criterio"], [
        ("Análisis estático", "flutter analyze", "Sin incidencias críticas de análisis."),
        ("Pruebas automatizadas", "flutter test", "Casos unitarios y de widgets disponibles en el repositorio."),
        ("Pruebas manuales", "Recorridos de cliente y dueño", "El comportamiento coincide con el resultado esperado."),
    ], [1.3, 2.0, 3.1])
    heading(doc, "Resultados de pruebas funcionales")
    test_rows = [
        ("P01", "Inicio", "Pantalla de bienvenida y acceso a la churrasquería.", "Evidencia adjunta"),
        ("P02", "Catálogo", "Fotos reales, precios, categorías y productos.", "Evidencia adjunta"),
        ("P03", "Voz", "Reconocimiento de voz en el filtro del catálogo.", "Evidencia adjunta"),
        ("P04", "Carrito", "Cantidades, total y confirmación del pedido.", "Evidencia adjunta"),
        ("P05", "Pedidos", "Estados En espera, Confirmado y Rechazado.", "Evidencia adjunta"),
        ("P06", "Reservas", "Solicitud cliente y gestión por dueño.", "Evidencia adjunta"),
        ("P07", "Comprobante", "Selección y envío para revisión manual.", "Evidencia adjunta"),
        ("P08", "Ubicación", "Horario, clima, contacto y acciones de mapa.", "Evidencia adjunta"),
    ]
    add_table(doc, ["ID", "Módulo", "Resultado esperado", "Estado"], test_rows, [0.55, 1.05, 3.55, 1.25])
    heading(doc, "Criterios de ejecución")
    doc.add_paragraph("Cada caso se ejecutó con conectividad disponible, una instancia configurada de Supabase y datos de demostración. Se considera aprobado cuando la pantalla responde, los datos esperados quedan visibles después de navegar o actualizar y no se presentan cierres inesperados. Los resultados manuales se registran con evidencia visual cuando el paso tiene una interfaz verificable.")
    add_table(doc, ["Clasificación", "Descripción", "Tratamiento"], [
        ("Bloqueante", "Impide iniciar, registrar pedidos, crear reservas o acceder al rol autorizado.", "Corregir antes de la entrega."),
        ("Mayor", "Permite continuar, pero muestra datos incorrectos o altera el estado de una operación.", "Registrar y corregir con prioridad alta."),
        ("Menor", "Afecta apariencia, texto o comodidad sin comprometer el flujo principal.", "Registrar para mejora posterior."),
    ], [1.15, 3.55, 1.7])
    doc.add_page_break()
    heading(doc, "Detalle de casos funcionales")
    detailed = [
        ("PF 01", "Inicio", "Abrir la APK y entrar", "La pantalla de bienvenida conduce al inicio sin error", "Aprobado"),
        ("PF 02", "Catálogo", "Cargar categorías y productos", "Se muestran fotos, descripciones y precios", "Aprobado"),
        ("PF 03", "Filtro", "Buscar un producto por texto", "La lista reduce los resultados relacionados", "Aprobado"),
        ("PF 04", "Voz", "Activar micrófono y pronunciar un producto", "La búsqueda recibe el texto o maneja el error", "Aprobado"),
        ("PF 05", "Carrito", "Agregar, quitar y contar productos", "Cantidad y total se actualizan correctamente", "Aprobado"),
        ("PF 06", "Pedido", "Completar los datos y registrar", "Se crea un pedido pendiente", "Aprobado"),
        ("PF 07", "Historial", "Consultar pedidos del cliente", "Se muestran estados En espera, Confirmado y Rechazado", "Aprobado"),
        ("PF 08", "Comprobante", "Seleccionar un JPG o PNG de prueba", "El archivo pasa a revisión manual", "Aprobado"),
        ("PF 09", "Reserva", "Completar fecha, hora y personas", "La reserva inicia En espera", "Aprobado"),
        ("PF 10", "Gestión", "Aceptar o denegar una reserva como dueño", "El estado actualizado llega al cliente", "Aprobado"),
        ("PF 11", "Ubicación", "Consultar horario, contacto y clima", "La información y acciones están disponibles", "Aprobado"),
        ("PF 12", "Consulta", "Enviar mensaje desde el formulario", "Se confirma el registro de la consulta", "Aprobado"),
    ]
    add_table(doc, ["ID", "Módulo", "Acción", "Resultado esperado", "Estado"], detailed, [0.6, 1.0, 1.55, 2.65, 0.75])
    heading(doc, "Resultados de validación técnica")
    doc.add_paragraph("La validación técnica complementó los recorridos manuales con flutter analyze para revisar problemas estáticos y flutter test para los casos automatizados disponibles. Este nivel de prueba no sustituye la UAT, porque la UAT confirma que el recorrido tiene sentido para quien utiliza la aplicación; sin embargo, reduce el riesgo de fallas básicas antes de la demostración final.")
    heading(doc, "Evidencias visuales")
    add_figure_pair(doc, [
        ("Figura 1. Inicio", "Acceso inicial al servicio.", IMAGES["inicio"]),
        ("Figura 2. Catálogo", "Productos, precios y fotos reales.", IMAGES["catalogo"]),
    ])
    doc.add_page_break()
    heading(doc, "Trazabilidad de evidencias")
    add_table(doc, ["Evidencia", "Caso relacionado", "Qué demuestra"], [
        ("Figura 1", "PF 01", "Pantalla de entrada de la aplicación."),
        ("Figura 2", "PF 02", "Catálogo con productos y precios."),
        ("Figura 3", "PF 04", "Estado de escucha para búsqueda por voz."),
        ("Figura 4", "PF 05", "Carrito con cantidades y total calculado."),
        ("Figura 5", "PF 07", "Tres estados de pedido visibles para el cliente."),
        ("Figura 6", "PF 09", "Formulario de registro de reserva."),
        ("Figura 7", "PF 10", "Estado de reserva después de gestión."),
        ("Figura 8", "PF 08", "Carga de un comprobante para revisión manual."),
    ], [1.05, 1.45, 3.05])
    add_figure_pair(doc, [
        ("Figura 3. Búsqueda por voz", "Estado de escucha activo.", IMAGES["voz"]),
        ("Figura 4. Carrito", "Cantidades y total del pedido.", IMAGES["carrito"]),
    ])
    add_figure_pair(doc, [
        ("Figura 5. Estados de pedidos", "En espera, confirmado y rechazado.", IMAGES["pedidos"]),
        ("Figura 6. Reserva", "Formulario de solicitud de mesa.", IMAGES["reserva"]),
    ])
    add_figure_pair(doc, [
        ("Figura 7. Estado de reserva", "Resultado visible después de la gestión.", IMAGES["gestionar"]),
        ("Figura 8. Comprobante", "Carga de evidencia para revisión manual.", IMAGES["comprobante"]),
    ])
    heading(doc, "Conclusión de pruebas")
    doc.add_paragraph("La evidencia adjunta confirma los recorridos centrales del MVP. El flujo de pago mantiene revisión manual por seguridad: una imagen u OCR aporta información documental, pero el dueño confirma el pago únicamente después de verificar el abono real.")
    path = OUT / "02_Pruebas_y_Evidencias_MVP.docx"
    doc.save(path)
    return path


def create_report():
    doc = Document()
    setup(doc, "Informe Final Brasas del Oriente")
    # La primera hoja se conserva en blanco para la presentación institucional.
    doc.add_page_break()
    add_cover(doc, "Informe Final del Proyecto", "Desarrollo e integración del MVP Brasas del Oriente")
    heading(doc, "Índice")
    add_table(doc, ["Sección", "Contenido"], [
        ("1", "Descripción, objetivo y alcance del proyecto."),
        ("2", "Requisitos, roles e historias de usuario del MVP."),
        ("3", "Arquitectura, datos, seguridad e integraciones."),
        ("4", "Diseño de interfaz y recorridos de cliente y dueño."),
        ("5", "Pago QR con revisión manual y decisiones de implementación."),
        ("6", "Pruebas, UAT, bitácora, despliegue y resultados."),
        ("7", "Limitaciones, conclusiones, referencias y anexos."),
    ], [1.0, 5.2])
    doc.add_page_break()
    heading(doc, "Descripción del proyecto")
    doc.add_paragraph("Brasas del Oriente es una aplicación móvil desarrollada en Flutter para apoyar la atención de una churrasquería en Santa Cruz de la Sierra. El proyecto reúne un catálogo digital, pedidos, reservas, consultas, información de ubicación y un panel administrativo para el dueño.")
    heading(doc, "Objetivo")
    doc.add_paragraph("Construir un producto mínimo viable que permita al cliente consultar la oferta, realizar solicitudes y conocer el estado de sus operaciones, mientras el dueño administra contenido, reservas y pagos pendientes de revisión.")
    heading(doc, "Problema que atiende")
    doc.add_paragraph("La atención tradicional de un restaurante concentra consultas sobre precios, disponibilidad, pedidos y reservas en canales dispersos. El MVP organiza estas necesidades en una sola aplicación móvil. El cliente puede revisar la información antes de comunicarse con el negocio y el dueño obtiene una vista operativa para responder solicitudes y revisar comprobantes.")
    heading(doc, "Alcance del producto mínimo viable")
    add_table(doc, ["Rol", "Necesidad atendida", "Función implementada"], [
        ("Cliente", "Conocer productos y precios", "Catálogo por categorías, búsqueda por texto y voz, fotos y carrito."),
        ("Cliente", "Solicitar atención", "Pedido, reserva, consulta, ubicación y horarios."),
        ("Cliente", "Conocer el avance", "Historial con estados de pedido, pago y reserva."),
        ("Dueño", "Administrar operación", "Panel para fotos, reservas y verificación manual de pagos."),
    ], [1.0, 2.1, 2.95])
    heading(doc, "Desarrollo e integraciones")
    add_table(doc, ["Componente", "Aplicación en el proyecto"], [
        ("Flutter", "Interfaz móvil, navegación, formularios, carrito y visualización de estados."),
        ("Supabase", "Autenticación, perfiles, roles, base de datos, políticas RLS y almacenamiento de archivos."),
        ("Supabase Storage", "Fotos de portada, imágenes reales de productos y comprobantes de pago."),
        ("Servicios externos", "Open Meteo para clima, OpenStreetMap para ubicación y reconocimiento de voz para búsqueda."),
    ], [1.55, 4.9])
    heading(doc, "Funciones entregadas")
    doc.add_paragraph("El cliente puede explorar el catálogo, buscar por texto o voz, agregar productos al carrito, confirmar pedidos, crear reservas, enviar consultas, consultar ubicación y revisar el estado de pedidos y reservas. El dueño puede administrar fotografías, gestionar reservas y revisar comprobantes de pago.")
    add_figure_pair(doc, [
        ("Figura 1. Catálogo", "Menú con productos y fotos reales.", IMAGES["catalogo"]),
        ("Figura 2. Historial", "Estados visibles de los pedidos.", IMAGES["pedidos"]),
    ])
    doc.add_page_break()
    heading(doc, "Arquitectura funcional")
    doc.add_paragraph("La aplicación Flutter concentra la interfaz móvil y los recorridos de cada rol. Supabase aporta autenticación, perfiles, base de datos y almacenamiento. Las solicitudes del cliente se registran en tablas relacionadas con su identificador de usuario; las vistas del dueño consumen únicamente los datos necesarios para operar. La separación por roles evita que una cuenta cliente acceda a las acciones administrativas.")
    add_table(doc, ["Capa", "Responsabilidad", "Resultado observable"], [
        ("Presentación", "Pantallas, formularios, navegación y mensajes de validación.", "Experiencia móvil para cliente y dueño."),
        ("Lógica", "Carrito, cálculo de totales, cambio de estados y validaciones.", "Pedidos, reservas y pagos con seguimiento."),
        ("Datos", "Persistencia, autenticación, archivos y políticas de acceso.", "Información disponible tras recargar la aplicación."),
        ("Servicios", "Clima, mapa y reconocimiento de voz cuando están disponibles.", "Información contextual y búsqueda asistida."),
    ], [1.1, 3.05, 1.9])
    heading(doc, "Estados principales")
    doc.add_paragraph("El pedido inicia En espera mientras el negocio revisa la solicitud y el comprobante. Después de la revisión puede quedar Confirmado o Rechazado. De manera equivalente, una reserva comienza En espera y el dueño la acepta o la deniega según la disponibilidad. Mostrar estos estados en el historial evita que el cliente tenga que preguntar por canales externos.")
    add_figure_pair(doc, [
        ("Figura 3. Pedido", "Estados visibles en el historial.", IMAGES["pedidos"]),
        ("Figura 4. Reserva", "Solicitud de mesa desde el cliente.", IMAGES["reserva"]),
    ])
    heading(doc, "Roles y seguridad")
    doc.add_paragraph("La aplicación distingue los roles cliente y dueño. Supabase aplica autenticación y políticas de seguridad por fila para limitar la lectura y las acciones de cada cuenta. El cliente revisa únicamente sus propios pedidos y reservas, mientras el dueño accede a las funciones operativas autorizadas.")
    heading(doc, "Pago QR con revisión manual")
    doc.add_paragraph("Se implementó una alternativa de pago mediante QR fijo y comprobante adjunto. No se incorporó una pasarela bancaria o API de cobro porque ese proceso requiere contratación, credenciales empresariales, validaciones de seguridad y aprobación de la entidad financiera. La alternativa permite registrar el pedido, mostrar el monto exacto, adjuntar un comprobante y enviarlo a revisión manual. La confirmación final permanece a cargo del dueño después de constatar el abono bancario.")
    add_figure_pair(doc, [
        ("Figura 3. Comprobante", "Archivo listo para validar y enviar.", IMAGES["comprobante"]),
        ("Figura 4. Reserva", "Estado confirmado visible para el cliente.", IMAGES["gestionar"]),
    ])
    doc.add_page_break()
    heading(doc, "Decisiones de implementación")
    doc.add_paragraph("Se eligió Supabase porque concentra autenticación, base de datos, reglas de seguridad y almacenamiento, lo que permite que un MVP móvil mantenga datos persistentes sin construir un servidor propio. Para las fotografías de productos y comprobantes se utilizó almacenamiento de archivos. La aplicación muestra errores de configuración de forma visible para facilitar el diagnóstico durante las pruebas.")
    doc.add_paragraph("La verificación de pagos permanece manual de manera intencional. Aunque el sistema puede presentar campos comparativos como monto, destino, fecha o referencia disponible, una imagen o un resultado OCR no certifica por sí solo el abono. Integrar una pasarela bancaria oficial exige un contrato con la entidad, credenciales empresariales, cumplimiento de seguridad y una integración autorizada. Por ello, el dueño confirma únicamente después de revisar el movimiento real.")
    heading(doc, "Pruebas realizadas")
    doc.add_paragraph("La entrega fue revisada con análisis estático, pruebas automatizadas disponibles y recorridos manuales. Los recorridos cubrieron acceso inicial, catálogo, búsqueda por voz, carrito, registro de pedido, envío de comprobante, historial en los tres estados, reserva, gestión de reserva, fotografías, información de ubicación y consultas. Las evidencias se documentan en el registro de pruebas y el recorrido de aceptación se formaliza en el protocolo UAT.")
    add_table(doc, ["Tipo de validación", "Propósito", "Documento asociado"], [
        ("Análisis y pruebas automáticas", "Detectar errores de código antes de ejecutar la app.", "Pruebas y Evidencias del MVP."),
        ("Pruebas funcionales", "Comprobar resultados de módulos y estados.", "Pruebas y Evidencias del MVP."),
        ("UAT", "Validar la experiencia completa con una persona revisora.", "Protocolo UAT y Acta de Conformidad."),
    ], [1.65, 3.0, 1.4])
    heading(doc, "Bitácora de evolución de la versión final")
    add_table(doc, ["Actividad", "Resultado de la versión final"], [
        ("Configuración de Supabase", "Conexión de autenticación, datos y almacenamiento para la aplicación."),
        ("Fotografías de productos", "Carga y visualización de imágenes reales en el catálogo."),
        ("Estados del cliente", "Historial de pedidos con En espera, Confirmado y Rechazado; reservas con seguimiento."),
        ("Panel de dueño", "Gestión de reservas, fotografías y pagos en revisión."),
        ("Pagos", "Comprobante adjunto con contraste de información para apoyar la revisión manual."),
        ("Correcciones visuales", "Ajuste del catálogo para eliminar desbordes de botones y mejorar la presentación."),
    ], [2.1, 3.95])
    heading(doc, "Resultados y cierre")
    doc.add_paragraph("La versión final entrega un MVP funcional con persistencia de datos, gestión diferenciada por roles y servicios externos aplicados al contexto de una churrasquería. El catálogo, carrito, pedidos, reservas, comprobantes y panel de dueño funcionan como partes de un mismo flujo, en lugar de pantallas aisladas. La validación final se realiza mediante el Protocolo UAT incluido en esta entrega.")
    heading(doc, "Limitaciones y mejoras futuras")
    doc.add_paragraph("El producto se entrega como MVP académico. La disponibilidad de clima, mapas y voz depende de conectividad y de los permisos del dispositivo. El flujo de pago requiere revisión humana y no reemplaza una pasarela bancaria certificada. Como evolución se recomienda integrar notificaciones, una pasarela de pago autorizada, registros de auditoría más detallados, métricas de uso y pruebas de carga con mayor volumen de pedidos.")
    add_figure_pair(doc, [
        ("Figura 5. Ubicación", "Horario, clima, contacto y mapa.", IMAGES["ubicacion"]),
        ("Figura 6. Reserva", "Solicitud de mesa del cliente.", IMAGES["reserva"]),
    ])
    doc.add_page_break()
    heading(doc, "Requisitos funcionales")
    doc.add_paragraph("Los requisitos funcionales describen el comportamiento observable que el MVP debe ofrecer a cada rol. Se priorizaron los recorridos que permiten a una persona conocer la oferta, solicitar un pedido o una mesa y conocer el resultado de la gestión sin depender de mensajes externos.")
    add_table(doc, ["Código", "Requisito", "Criterio de cumplimiento"], [
        ("RF 01", "Mostrar catálogo digital", "Productos, categorías, precio, descripción e imagen visibles."),
        ("RF 02", "Buscar productos", "Búsqueda por texto y por voz cuando el permiso está concedido."),
        ("RF 03", "Gestionar carrito", "Agregar, quitar, calcular cantidades y total."),
        ("RF 04", "Registrar pedidos", "Datos básicos y estado inicial en espera."),
        ("RF 05", "Registrar reservas", "Fecha, hora, personas y estado inicial en espera."),
        ("RF 06", "Mostrar historial", "Pedidos y reservas visibles según el usuario autenticado."),
        ("RF 07", "Gestionar operación", "Dueño acepta o deniega reservas y revisa pagos."),
        ("RF 08", "Gestionar fotografías", "Dueño actualiza imágenes de productos."),
    ], [0.7, 2.25, 3.25])
    heading(doc, "Requisitos no funcionales")
    doc.add_paragraph("Además de las funciones visibles, el proyecto necesita condiciones de calidad que permitan demostrar un uso razonable en un dispositivo Android. Estas condiciones orientan la prueba, el despliegue y las mejoras de siguientes versiones.")
    add_table(doc, ["Categoría", "Requisito aplicado", "Verificación"], [
        ("Usabilidad", "Pantallas con etiquetas claras, acciones visibles y mensajes de estado.", "Recorrido manual de cliente y dueño."),
        ("Seguridad", "Autenticación, perfiles y restricciones de datos por rol.", "Pruebas de acceso y políticas RLS."),
        ("Compatibilidad", "Ejecución en Android mediante APK de Flutter.", "Instalación en emulador y teléfono Android."),
        ("Persistencia", "Pedidos, reservas, perfiles y archivos se conservan en Supabase.", "Consulta posterior desde historial y panel."),
        ("Rendimiento", "Carga razonable de pantallas con datos demostrativos.", "Observación en recorridos del MVP."),
        ("Mantenibilidad", "Código organizado por pantallas y servicios.", "Análisis estático y pruebas automatizadas."),
    ], [1.1, 3.5, 1.6])
    heading(doc, "Historias de usuario del cliente")
    add_table(doc, ["Código", "Historia", "Criterio de aceptación"], [
        ("HU C01", "Como cliente, quiero ver el menú para conocer productos y precios.", "Puedo explorar categorías y productos visibles."),
        ("HU C02", "Como cliente, quiero buscar por texto o voz para encontrar un producto rápidamente.", "El catálogo aplica el filtro o informa una limitación."),
        ("HU C03", "Como cliente, quiero armar un pedido para solicitar los productos elegidos.", "El total se calcula y el pedido se registra."),
        ("HU C04", "Como cliente, quiero adjuntar un comprobante para informar mi pago.", "El archivo queda en revisión manual."),
        ("HU C05", "Como cliente, quiero consultar el estado para saber si mi pedido fue atendido.", "Veo En espera, Confirmado o Rechazado."),
        ("HU C06", "Como cliente, quiero reservar una mesa para solicitar disponibilidad.", "La reserva se registra y muestra su estado."),
        ("HU C07", "Como cliente, quiero conocer ubicación y horarios antes de visitar el local.", "Veo datos de contacto, clima y acciones de mapa."),
    ], [0.8, 3.2, 2.2])
    heading(doc, "Historias de usuario del dueño")
    add_table(doc, ["Código", "Historia", "Criterio de aceptación"], [
        ("HU D01", "Como dueño, quiero diferenciar mis funciones de las de un cliente.", "Mi cuenta autorizada habilita el panel operativo."),
        ("HU D02", "Como dueño, quiero revisar reservas para decidir según disponibilidad.", "Puedo aceptar o denegar las solicitudes pendientes."),
        ("HU D03", "Como dueño, quiero revisar pagos para contrastar el comprobante con el pedido.", "Veo monto esperado y datos disponibles para comparación."),
        ("HU D04", "Como dueño, quiero confirmar o rechazar un pago para actualizar su estado.", "El cliente observa el resultado en su historial."),
        ("HU D05", "Como dueño, quiero cargar fotos para mantener el catálogo actualizado.", "La foto se almacena y es visible en el catálogo."),
    ], [0.8, 3.2, 2.2])
    heading(doc, "Diseño de la experiencia de cliente")
    doc.add_paragraph("La navegación principal parte de la pantalla de bienvenida y presenta opciones directas para ver el menú, revisar el pedido, administrar la cuenta, reservar, enviar consulta y conocer la ubicación. El catálogo utiliza tarjetas de producto con fotografía, descripción, precio y un control para agregar al carrito. La decisión busca reducir pasos en operaciones frecuentes y mantener mensajes de estado legibles.")
    add_figure_pair(doc, [
        ("Figura 7. Inicio", "Entrada a la aplicación.", IMAGES["inicio"]),
        ("Figura 8. Carrito", "Resumen previo al pedido.", IMAGES["carrito"]),
    ])
    heading(doc, "Diseño de la experiencia del dueño")
    doc.add_paragraph("El dueño utiliza una vista diferenciada desde Mi cuenta. Desde ella puede abrir las funciones de operación, cambiar la portada, gestionar fotos de productos, configurar la referencia QR, verificar pagos y gestionar reservas. Las decisiones de pago y reserva se mantienen explícitas para evitar que el sistema confirme por sí mismo actividades que requieren una validación del negocio.")
    doc.add_paragraph("La experiencia prioriza listas de solicitudes y acciones concretas. Una reserva en espera requiere una decisión de aceptar o denegar; un comprobante en revisión presenta información de contraste y permite confirmar o rechazar con una observación. Esta separación reduce ambigüedad y conserva un registro del estado visible para el cliente.")
    add_figure_pair(doc, [
        ("Figura 9. Reserva", "Solicitud que será gestionada.", IMAGES["reserva"]),
        ("Figura 10. Estado", "Resultado visible para cliente.", IMAGES["gestionar"]),
    ])
    heading(doc, "Modelo lógico de datos")
    doc.add_paragraph("El modelo de datos vincula las operaciones a un usuario autenticado. Un perfil almacena el rol; los productos se consultan desde el catálogo; un pedido contiene el cliente, total y estado; los detalles relacionan pedido y productos; una reserva registra fecha, hora, cantidad de personas y estado. Los comprobantes se almacenan como archivos y se relacionan con el pedido que se revisa.")
    add_table(doc, ["Entidad", "Propósito", "Relación relevante"], [
        ("Perfil", "Identificar cuenta y rol.", "Se relaciona con pedidos y reservas."),
        ("Producto", "Representar la oferta del menú.", "Se utiliza en detalles de pedido y fotos."),
        ("Pedido", "Registrar solicitud y total.", "Incluye detalles y estado de pago."),
        ("Detalle de pedido", "Registrar producto y cantidad.", "Pertenece a un pedido."),
        ("Reserva", "Registrar solicitud de mesa.", "Pertenece a un usuario y tiene estado."),
        ("Comprobante", "Guardar evidencia documental.", "Pertenece a un pedido para revisión."),
    ], [1.35, 2.8, 2.05])
    heading(doc, "Autenticación y seguridad")
    doc.add_paragraph("La autenticación se resuelve con Supabase Auth. Al crear una cuenta, el sistema obtiene una identidad que se asocia con un perfil de cliente. El rol dueño debe asignarse de forma autorizada; no se presenta como una opción libre durante el registro. Esta regla evita que cualquier cuenta nueva obtenga capacidades administrativas.")
    doc.add_paragraph("Las políticas de seguridad por fila delimitan las consultas y actualizaciones. El cliente debe consultar únicamente sus propios pedidos y reservas; el dueño requiere acceso a las listas operativas y a los cambios de estado. Las claves de configuración se inyectan al ejecutar o compilar la aplicación, por lo que no deben divulgarse dentro de documentos, capturas o repositorios públicos.")
    heading(doc, "Almacenamiento de imágenes")
    doc.add_paragraph("Supabase Storage almacena fotografías de la portada, imágenes de productos y archivos de comprobantes. La aplicación valida que los comprobantes seleccionados sean imágenes JPG o PNG con un límite de tamaño indicado en la interfaz. Después de la carga, se guarda la referencia del archivo para que la interfaz pueda mostrar el recurso o dejarlo disponible para revisión.")
    doc.add_paragraph("Durante la evolución de la versión final se configuró el bucket requerido para fotografías. También se corrigió la actualización visual posterior a la carga para evitar errores de estado asíncrono en Flutter. Estas correcciones permitieron que el dueño reemplazara imágenes y verificara el resultado en el catálogo.")
    doc.add_page_break()
    heading(doc, "Integraciones de información")
    doc.add_paragraph("La sección de ubicación integra datos informativos del restaurante, acciones de llamada, WhatsApp y apertura de mapa. El clima se obtiene desde un servicio externo y se presenta como información contextual. La búsqueda por voz usa el permiso de micrófono del dispositivo y el reconocimiento disponible en Android; por ello la interfaz conserva una alternativa de búsqueda escrita.")
    doc.add_paragraph("Estas integraciones fueron seleccionadas para mejorar el recorrido principal sin convertirlas en dependencias críticas para crear un pedido o una reserva. Si una integración no está disponible por conectividad, permisos o servicio externo, el catálogo, el carrito y las solicitudes principales siguen siendo el núcleo funcional del MVP.")
    add_figure_pair(doc, [
        ("Figura 11. Voz", "Búsqueda asistida por micrófono.", IMAGES["voz"]),
        ("Figura 12. Ubicación", "Información contextual del local.", IMAGES["ubicacion"]),
    ])
    doc.add_page_break()
    heading(doc, "Despliegue y ejecución")
    doc.add_paragraph("El proyecto se ejecuta con Flutter en modo de desarrollo mediante flutter run, seleccionando un emulador o teléfono Android con depuración USB. Para distribuir una copia de prueba se genera un APK con flutter build apk. La aplicación requiere URL y clave pública de Supabase a través de parámetros de compilación o ejecución, de acuerdo con la configuración del proyecto.")
    add_table(doc, ["Elemento", "Mínimo", "Recomendado"], [
        ("Sistema operativo", "Android compatible con Flutter y Play Services disponibles.", "Android actualizado con conectividad estable."),
        ("Memoria", "Dispositivo capaz de ejecutar aplicaciones Flutter.", "4 GB de RAM o más para pruebas fluidas."),
        ("Conectividad", "Internet para Supabase, clima y mapas.", "Wi-Fi o datos móviles estables."),
        ("Permisos", "Almacenamiento o selector de archivos y micrófono para voz.", "Permisos concedidos durante la prueba UAT."),
    ], [1.4, 2.25, 2.55])
    doc.add_page_break()
    heading(doc, "Plan de pruebas y control de calidad")
    doc.add_paragraph("El control de calidad se organizó en tres niveles. Primero, análisis estático y pruebas automatizadas disponibles para detectar errores antes de la ejecución. Segundo, pruebas funcionales orientadas a módulos individuales: catálogo, voz, carrito, pedido, reserva, comprobante, ubicación y panel de dueño. Tercero, UAT con un recorrido continuo que confirma que la experiencia completa conserva datos y muestra estados coherentes.")
    doc.add_paragraph("Cuando se encontró una incidencia, se revisó si correspondía a configuración de Supabase, política de acceso, almacenamiento de archivos, estado asíncrono en Flutter o versión instalada en el emulador. Esta clasificación permitió corregir problemas de clave de API, bucket de Storage, actualización de fotos, renderizado del catálogo y carga del historial de pedidos.")
    doc.add_page_break()
    heading(doc, "Resultados de validación")
    add_table(doc, ["Área", "Resultado alcanzado", "Evidencia"], [
        ("Catálogo", "Productos con fotos, categorías, precios y búsqueda.", "Capturas del menú digital."),
        ("Pedido", "Carrito, total, registro e historial de estados.", "Estados En espera, Confirmado y Rechazado."),
        ("Pago", "Comprobante cargado y revisión manual del dueño.", "Pantallas de adjuntar y revisar."),
        ("Reserva", "Solicitud cliente y resultado visible después de gestión.", "Formulario e historial de reservas."),
        ("Administración", "Fotos, reservas y pagos disponibles al rol dueño.", "Recorrido UAT y pruebas funcionales."),
    ], [1.2, 3.4, 1.6])
    doc.add_paragraph("Las evidencias adjuntas muestran una versión funcional con operaciones persistentes. La confirmación de pagos no se automatiza: este comportamiento es un control de seguridad y debe entenderse como una decisión de alcance, no como una omisión del flujo.")
    doc.add_page_break()
    heading(doc, "Protocolo UAT y entrega")
    doc.add_paragraph("El documento UAT complementario presenta doce pasos secuenciales para la aceptación final. El recorrido parte de la pantalla de bienvenida, explora el catálogo, utiliza búsqueda por voz, arma un carrito, registra un pedido y adjunta un comprobante de prueba. Luego cambia al rol dueño para revisar el pago, consulta el historial, registra una reserva, la gestiona y comprueba que el cliente observe el resultado.")
    doc.add_paragraph("La persona revisora debe marcar cada resultado como conforme o no conforme, describir incidentes y completar el acta de conformidad. El criterio de aceptación exige ausencia de defectos bloqueantes en las operaciones principales. Los hallazgos menores pueden permanecer registrados para una mejora posterior, siempre que no alteren el registro o los estados de cliente y dueño.")
    doc.add_page_break()
    heading(doc, "Referencias técnicas")
    doc.add_paragraph("Flutter. (2026). Documentación de Flutter para desarrollo de aplicaciones multiplataforma. https://docs.flutter.dev/")
    doc.add_paragraph("Supabase. (2026). Documentación de autenticación, base de datos, Storage y políticas de seguridad. https://supabase.com/docs")
    doc.add_paragraph("Open Meteo. (2026). API meteorológica utilizada para información contextual. https://open-meteo.com/")
    doc.add_paragraph("OpenStreetMap. (2026). Datos cartográficos y recursos de mapa. https://www.openstreetmap.org/")
    doc.add_paragraph("Estas referencias se presentan con formato bibliográfico breve para documentar las plataformas y servicios empleados. Las capturas de evidencia incluidas en los anexos proceden de las pruebas internas de la aplicación realizadas el 25 de noviembre de 2026.")
    doc.add_page_break()
    heading(doc, "Anexo A Evidencia del catálogo y carrito")
    add_figure_pair(doc, [
        ("Figura A1. Catálogo", "Productos y precios disponibles.", IMAGES["catalogo"]),
        ("Figura A2. Carrito", "Resumen y monto de pedido.", IMAGES["carrito"]),
    ])
    doc.add_page_break()
    heading(doc, "Anexo B Evidencia de pedidos y comprobantes")
    add_figure_pair(doc, [
        ("Figura B1. Historial", "Tres estados del pedido.", IMAGES["pedidos"]),
        ("Figura B2. Comprobante", "Archivo de prueba para revisión.", IMAGES["comprobante"]),
    ])
    doc.add_page_break()
    heading(doc, "Anexo C Reservas e información")
    add_figure_pair(doc, [
        ("Figura C1. Reserva", "Formulario de solicitud.", IMAGES["reserva"]),
        ("Figura C2. Ubicación", "Datos y acciones de contacto.", IMAGES["ubicacion"]),
    ])
    path = OUT / "03_Informe_Final_Brasas_del_Oriente_Ampliado.docx"
    doc.save(path)
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prepare_images()
    outputs = [create_uat(), create_tests(), create_report()]
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
