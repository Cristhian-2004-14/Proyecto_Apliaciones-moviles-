from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from generar_guia_aceptacion_mvp import (
    ROOT,
    configure,
    heading,
    normal_paragraph,
    record_table,
    checklist,
    title,
)


OUTPUT = ROOT / "entregables" / "Protocolo_UAT_y_Acta_de_Conformidad_MVP.docx"


CASES = [
    (
        "UAT-01",
        "Catálogo de productos",
        "En la pantalla principal, toque Ver menú y revise los productos disponibles.",
        "Se muestran productos con nombre, descripción, precio y fotografía. La pantalla se puede recorrer sin mensajes de error.",
    ),
    (
        "UAT-02",
        "Filtro y búsqueda",
        "En el menú, elija una categoría. Luego escriba el nombre de un producto. Si lo desea, pulse el micrófono y permita el acceso para buscar por voz.",
        "La lista muestra productos relacionados. Si no se permite el micrófono, la aplicación explica que el permiso es necesario.",
    ),
    (
        "UAT-03",
        "Carrito y pedido",
        "Agregue dos productos, abra Mi pedido, cambie una cantidad y confirme usando nombre y teléfono de prueba.",
        "Las cantidades y el total cambian correctamente. La aplicación confirma que el pedido fue registrado.",
    ),
    (
        "UAT-04",
        "Enviar consulta",
        "Abra Enviar consulta, complete los tres campos usando información de prueba y envíe el formulario.",
        "La aplicación informa que la consulta fue enviada. Si falta un dato, indica qué se debe completar.",
    ),
    (
        "UAT-05",
        "Crear reserva",
        "Abra Reservar mesa, ingrese datos de prueba y seleccione una fecha futura.",
        "La reserva queda registrada con estado EN ESPERA. Una fecha pasada no debe ser aceptada.",
    ),
    (
        "UAT-06",
        "Historial del cliente",
        "Con la cuenta cliente, entre a Mi cuenta y seleccione Mis pedidos y reservas.",
        "Se muestran los pedidos y reservas de esa misma cuenta, con sus estados actuales.",
    ),
    (
        "UAT-07",
        "Gestión de reservas del dueño",
        "Con la cuenta del dueño, abra Mi cuenta y luego Gestionar reservas. Confirme o rechace una reserva de prueba.",
        "Solo el dueño puede realizar esta acción. El nuevo estado aparece para el cliente al actualizar su historial.",
    ),
    (
        "UAT-08",
        "Ubicación y horarios",
        "Abra Ubicación y horarios; revise los datos, espere el clima y pulse Ver mapa.",
        "Se visualizan dirección, horario y contacto. El clima se muestra o ofrece reintento, y el mapa abre correctamente.",
    ),
]


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    configure(doc)

    for _ in range(5):
        doc.add_paragraph()
    title(doc, "Protocolo de pruebas de aceptación y acta de conformidad del MVP")
    normal_paragraph(doc, "Proyecto Brasas del Oriente", before=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    normal_paragraph(doc, "Cliente evaluador Grupo Neo", before=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    normal_paragraph(doc, "Versión de software 1.0.0+1", before=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    normal_paragraph(doc, "Fecha de entrega: ____ / ____ / 2026", before=20, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    heading(doc, "1. Objetivo del documento")
    normal_paragraph(doc, "Esta guía permite al cliente revisar las funciones más importantes de Brasas del Oriente antes de aceptar la entrega. Cada prueba indica qué hacer, qué debería ocurrir y un espacio para marcar si el resultado es conforme o no conforme.", first=0.4)
    heading(doc, "2. Alcance de la entrega")
    normal_paragraph(doc, "El MVP incluye catálogo de productos, filtros y búsqueda, carrito, pedidos, consultas, reservas, historial del cliente, gestión de reservas del dueño y ubicación del negocio. La búsqueda por voz se revisa como apoyo del catálogo. El QR bancario, el OCR y la verificación de comprobantes no se incluyen en esta aceptación porque son funciones adicionales y no forman parte del recorrido principal del MVP.", first=0.4)
    heading(doc, "3. Instrucciones de acceso")
    normal_paragraph(doc, "El equipo debe instalar la versión actual de la aplicación en un teléfono Android o emulador y entregar una cuenta de prueba de cliente y una cuenta de dueño por un medio privado. Abra la aplicación desde el icono de Brasas del Oriente. No escriba contraseñas, datos bancarios ni información personal en este documento.", first=0.4)
    heading(doc, "4. Requisitos previos")
    checklist(doc, [
        "Teléfono Android o emulador con la aplicación instalada.",
        "Conexión a internet para cargar datos, clima, fotos y mapa.",
        "Cuenta de prueba de cliente y cuenta de prueba de dueño entregadas por el equipo.",
        "Permiso de micrófono solo si se realizará la búsqueda por voz.",
        "Datos de prueba para pedido, consulta y reserva.",
    ])
    heading(doc, "5. Criterios de aceptación")
    normal_paragraph(doc, "Marque Conforme cuando el resultado obtenido coincida con el resultado esperado. Marque No conforme si la función no se puede terminar, muestra información incorrecta o necesita una corrección. Registre los comentarios y, si existe un problema, adjunte una captura o describa cómo repetirlo.", first=0.4)

    heading(doc, "6. Guía de pruebas de aceptación")
    for number, (case_id, functionality, steps, expected) in enumerate(CASES, start=1):
        heading(doc, f"{case_id}  {functionality}", 2)
        record_table(doc, [
            ("ID", case_id),
            ("Funcionalidad", functionality),
            ("Instrucciones", steps),
            ("Resultado esperado", expected),
            ("Conformidad", "[ ] Conforme     [ ] No conforme"),
            ("Observaciones", "________________________________________________________________________________\n________________________________________________________________________________"),
        ])
        if number in (2, 4, 6):
            doc.add_page_break()

    heading(doc, "7. Registro general de observaciones")
    record_table(doc, [
        ("Observaciones", "________________________________________________________________________________\n________________________________________________________________________________\n________________________________________________________________________________"),
        ("Evidencias adjuntas", "________________________________________________________________________________"),
        ("Condiciones pendientes", "________________________________________________________________________________"),
    ])
    heading(doc, "8. Acta de entrega y conformidad")
    normal_paragraph(doc, "Nombre del proyecto: Brasas del Oriente", first=0.0)
    normal_paragraph(doc, "Versión entregada: 1.0.0+1", first=0.0)
    normal_paragraph(doc, "Nombre del cliente: Grupo Neo", first=0.0)
    normal_paragraph(doc, "Responsable del desarrollo: _________________________________________________", first=0.0)
    normal_paragraph(doc, "Fecha de entrega: ____ / ____ / 2026", first=0.0)
    normal_paragraph(doc, "Declaración: Confirmo que revisé las funciones incluidas en el alcance del MVP y que las observaciones, si existen, están registradas en este documento.", first=0.4)
    record_table(doc, [
        ("Resultado general", "[ ] Aceptación total     [ ] Aceptación con observaciones     [ ] Rechazo"),
        ("Observaciones o condiciones pendientes", "________________________________________________________________________________\n________________________________________________________________________________"),
    ])
    normal_paragraph(doc, "Firma del cliente: _________________________________________", before=22)
    normal_paragraph(doc, "Nombre completo: _________________________________________     Fecha: ____ / ____ / 2026", before=10)
    normal_paragraph(doc, "Firma del responsable del desarrollo: ______________________________", before=22)
    normal_paragraph(doc, "Nombre completo: _________________________________________     Fecha: ____ / ____ / 2026", before=10)

    doc.core_properties.title = "Protocolo de pruebas de aceptación y acta de conformidad del MVP"
    doc.core_properties.subject = "UAT del MVP de Brasas del Oriente"
    doc.core_properties.author = ""
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
