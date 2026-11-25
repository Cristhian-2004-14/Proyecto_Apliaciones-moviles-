from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'documentación técnica'


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, start=100, bottom=100, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in('w:tcMar')
    if tc_mar is None:
        tc_mar = OxmlElement('w:tcMar')
        tc_pr.append(tc_mar)
    for side, value in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = tc_mar.find(qn(f'w:{side}'))
        if node is None:
            node = OxmlElement(f'w:{side}')
            tc_mar.append(node)
        node.set(qn('w:w'), str(value))
        node.set(qn('w:type'), 'dxa')


def setup(doc, title, subtitle):
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)
    styles = doc.styles
    styles['Normal'].font.name = 'Aptos'
    styles['Normal']._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos')
    styles['Normal']._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
    styles['Normal'].font.size = Pt(10.5)
    for name, size in [('Title', 22), ('Heading 1', 15), ('Heading 2', 12)]:
        styles[name].font.name = 'Aptos Display' if name == 'Title' else 'Aptos'
        styles[name]._element.rPr.rFonts.set(qn('w:ascii'), styles[name].font.name)
        styles[name]._element.rPr.rFonts.set(qn('w:hAnsi'), styles[name].font.name)
        styles[name].font.size = Pt(size)
        styles[name].font.color.rgb = RGBColor(0, 0, 0)
    p = doc.add_paragraph(style='Title')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(title)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(subtitle).italic = True
    doc.add_paragraph('Brasas del Oriente  |  Aplicación móvil Flutter  |  Versión 1.0.0')


def add_heading(doc, text, level=1):
    doc.add_heading(text, level=level)


def add_para(doc, text, bold_lead=None):
    p = doc.add_paragraph()
    if bold_lead:
        p.add_run(bold_lead).bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(7)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(item)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for idx, header in enumerate(headers):
        cell = table.rows[0].cells[idx]
        shade(cell, '5B2C16')
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        set_cell_margins(cell)
        run = cell.paragraphs[0].add_run(header)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        if widths:
            cell.width = Inches(widths[idx])
    for row_idx, row in enumerate(rows):
        cells = table.add_row().cells
        for idx, value in enumerate(row):
            if row_idx % 2 == 1:
                shade(cells[idx], 'FBF3EF')
            cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_margins(cells[idx])
            cells[idx].text = str(value)
            if widths:
                cells[idx].width = Inches(widths[idx])
    doc.add_paragraph()
    return table


def add_footer(doc):
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run('Brasas del Oriente | Documentación técnica').font.size = Pt(8)


def manual_usuario():
    doc = Document()
    setup(doc, 'Manual de uso del MVP', 'Guía para clientes y dueño del negocio')
    add_para(doc, 'Este manual explica cómo utilizar la versión mínima funcional de Brasas del Oriente. Está dirigido a dos tipos de personas: el cliente que desea conocer el menú, realizar un pedido, enviar una consulta o solicitar una reserva; y el dueño que administra la información visible, los pedidos y las reservas. Siga los recorridos en el orden indicado durante las pruebas de aceptación.')
    add_para(doc, 'El catálogo, las cuentas, los pedidos, las consultas, las reservas y las fotos dependen de una conexión con Supabase. Por esa razón, se recomienda mantener Internet activo mientras se usa la aplicación. Las funciones de pagos QR y comprobantes son complementarias y no son necesarias para completar el recorrido mínimo descrito en este documento.')
    add_heading(doc, '1 Cómo identificar cada área')
    add_table(doc, ['Área', 'Para qué sirve', 'Quién la utiliza'], [
        ('Inicio', 'Da acceso a las funciones principales mediante tarjetas de navegación.', 'Cliente y dueño.'),
        ('Ver menú', 'Muestra los productos, filtros, buscador de texto, búsqueda por voz y carrito.', 'Cliente y dueño.'),
        ('Mi pedido', 'Permite revisar el carrito, cambiar cantidades y confirmar un pedido.', 'Cliente autenticado.'),
        ('Mi cuenta', 'Permite iniciar sesión, registrarse, cerrar sesión, revisar el historial o abrir el panel de dueño.', 'Cliente y dueño.'),
        ('Reservar mesa', 'Registra una solicitud de reserva para una fecha futura.', 'Cliente.'),
        ('Enviar consulta', 'Registra una pregunta o solicitud de contacto.', 'Cliente.'),
        ('Ubicación y horarios', 'Presenta datos del negocio, clima, contacto y mapa.', 'Cliente y dueño.'),
    ], [1.45, 3.55, 1.65])
    add_heading(doc, '2 Antes de comenzar')
    add_bullets(doc, [
        'Instale la aplicación en un teléfono Android con conexión a Internet.',
        'Para crear pedidos que queden asociados a su historial, primero inicie sesión o cree una cuenta desde Mi cuenta.',
        'Permita el acceso al micrófono solo si desea usar la búsqueda por voz. Puede negarlo; el buscador de texto seguirá disponible.',
        'El rol Dueño no se elige al registrarse. Debe ser asignado previamente en la base de datos por un administrador del proyecto.',
        'Compruebe que la fecha y hora del teléfono sean correctas; esto ayuda a registrar reservas y comprobar estados.',
    ])
    add_heading(doc, '3 Recorrido detallado del cliente')
    add_heading(doc, '3.1 Crear cuenta o iniciar sesión', level=2)
    add_para(doc, 'Desde la pantalla Inicio pulse Mi cuenta. Si ya tiene una cuenta, escriba su correo electrónico y contraseña, y pulse Ingresar. Si es su primera vez, pulse Crear una cuenta, complete los campos solicitados y finalice el registro. Tras iniciar sesión, la pantalla muestra el nombre y rol disponible para esa cuenta.')
    add_para(doc, 'Resultado esperado: la pantalla Mi cuenta deja de mostrar el formulario de acceso y permite abrir Mis pedidos y reservas. Si los datos son incorrectos o no hay Internet, la aplicación muestra un mensaje de error y no inicia sesión.')
    add_heading(doc, '3.2 Ver productos y usar filtros', level=2)
    add_para(doc, 'En Inicio pulse Ver menú. Al abrirse, el catálogo presenta tarjetas con foto, nombre, descripción, precio y botón más. Deslice hacia arriba para ver más productos. En la parte superior encontrará el campo Buscar en el menú y los filtros por rubro.')
    add_bullets(doc, [
        'Para buscar por texto, pulse el campo de búsqueda y escriba una palabra, por ejemplo lomo, yuca o bebida.',
        'Para filtrar, pulse una categoría como Bebidas, Acompañamientos o Cortes. Pulse Todos para volver a ver el catálogo completo.',
        'Si no hay coincidencias, modifique el texto o vuelva a seleccionar Todos.',
        'Las fotografías visibles son las fotos que el dueño cargó previamente para cada producto.',
    ])
    add_para(doc, 'Resultado esperado: la lista cambia sin salir de la pantalla y muestra solo los productos que coinciden con el texto o rubro seleccionado.')
    add_heading(doc, '3.3 Buscar por voz', level=2)
    add_para(doc, 'En el catálogo pulse el icono de micrófono. Android puede pedir autorización para grabar audio; seleccione Permitir solo si desea usar esta función. Pronuncie el nombre de un producto o una categoría, por ejemplo limonada o acompañamientos. Mientras la aplicación escucha, el campo de búsqueda se actualiza con las palabras detectadas. Pulse el botón de detener para finalizar la escucha.')
    add_para(doc, 'Resultado esperado: el texto reconocido se coloca en el buscador y la lista se filtra. Si el permiso fue negado, no hay conexión o el reconocimiento no está disponible en el teléfono, la aplicación informa la situación; puede continuar con la búsqueda escrita.')
    add_heading(doc, '3.4 Agregar productos y revisar el carrito', level=2)
    add_para(doc, 'Pulse el botón más de la tarjeta de un producto. Repita la acción si desea agregar más unidades o agregue otros productos. Pulse el icono de carrito, ubicado en la barra superior, para abrir Mi pedido. En esta pantalla cada fila tiene un botón menos y un botón más para disminuir o aumentar la cantidad.')
    add_bullets(doc, [
        'Use más para incrementar la cantidad de un producto.',
        'Use menos para reducirla. Si la cantidad llega a cero, el producto se elimina del pedido.',
        'Revise el total mostrado al final de la pantalla antes de continuar.',
        'Si el carrito está vacío, vuelva al menú y agregue al menos un producto.',
    ])
    add_para(doc, 'Resultado esperado: el total se actualiza cada vez que se modifica una cantidad.')
    add_heading(doc, '3.5 Confirmar un pedido', level=2)
    add_para(doc, 'Con al menos un producto en Mi pedido, pulse Confirmar pedido. Si no inició sesión, la aplicación le indicará que debe acceder desde Mi cuenta para proteger y asociar el pedido. Después de iniciar sesión, complete los datos de contacto requeridos y confirme el registro.')
    add_para(doc, 'Resultado esperado: aparece un aviso de pedido creado correctamente. El pedido se registra en Supabase con su total y el detalle de los productos. Posteriormente puede comprobarlo en Mis pedidos y reservas.')
    add_heading(doc, '3.6 Enviar una consulta', level=2)
    add_para(doc, 'Desde Inicio pulse Enviar consulta. Complete Nombre, Teléfono boliviano y Mensaje. Lea los datos antes de enviar y pulse Enviar consulta. No deje campos obligatorios vacíos.')
    add_para(doc, 'Resultado esperado: se muestra el mensaje Consulta enviada correctamente. Si falta un campo o el teléfono no tiene un formato válido, la aplicación marca el dato que debe corregirse y no registra la consulta.')
    add_heading(doc, '3.7 Solicitar una reserva', level=2)
    add_para(doc, 'Desde Inicio pulse Reservar mesa. Complete su nombre, teléfono, fecha, hora y cantidad de personas. Seleccione una fecha y hora posteriores al momento actual. Finalmente pulse el botón para enviar la reserva.')
    add_para(doc, 'Resultado esperado: la reserva queda registrada inicialmente con estado En espera. Esto no significa que la mesa esté aceptada; el dueño deberá confirmarla o rechazarla desde su panel.')
    add_heading(doc, '3.8 Consultar pedidos y reservas', level=2)
    add_para(doc, 'Abra Mi cuenta y pulse Mis pedidos y reservas. Esta pantalla reúne los pedidos y reservas asociados únicamente a la sesión activa. Revise los estados de cada reserva: En espera cuando aún no fue revisada, Confirmada cuando el dueño la aceptó o Rechazada cuando no puede atenderse.')
    add_para(doc, 'Resultado esperado: el usuario puede conocer el estado actualizado sin llamar al negocio. Si no tiene registros, la pantalla informa que no existen pedidos o reservas para esa cuenta.')
    add_heading(doc, '3.9 Revisar ubicación, contacto y mapa', level=2)
    add_para(doc, 'Desde Inicio pulse Ubicación y horarios. Revise la dirección, horario de atención, teléfono y tarjeta de clima. Use Cómo llegar para solicitar una ruta, Llamar para abrir el marcador, Contactar por WhatsApp para abrir la aplicación correspondiente y Ver mapa para visualizar la ubicación en OpenStreetMap.')
    add_para(doc, 'Resultado esperado: cada acción abre la aplicación del teléfono compatible. Si el dispositivo no tiene una aplicación para llamadas, mapas o WhatsApp, no podrá completar esa acción externa, pero los datos del negocio seguirán visibles.')
    add_heading(doc, '4 Recorrido detallado del dueño')
    add_heading(doc, '4.1 Iniciar como dueño', level=2)
    add_para(doc, 'Abra Mi cuenta e ingrese con el correo y contraseña de la cuenta a la que se asignó el rol Dueño. Cuando el acceso sea correcto, se muestra el texto Rol Dueño y los botones administrativos. Si ingresa como cliente, esos botones no estarán disponibles.')
    add_heading(doc, '4.2 Abrir el panel administrativo', level=2)
    add_para(doc, 'Pulse Abrir panel del dueño. Desde allí puede revisar los pedidos registrados y acceder a la administración de reservas según las opciones habilitadas. Use esta pantalla únicamente con la cuenta autorizada del negocio.')
    add_para(doc, 'Resultado esperado: se muestran los pedidos y datos necesarios para su gestión. Un usuario cliente no puede abrir estas opciones por las reglas de rol.')
    add_heading(doc, '4.3 Gestionar reservas', level=2)
    add_para(doc, 'En el panel de dueño abra la sección de reservas. Identifique las solicitudes En espera, revise nombre, teléfono, fecha, hora y número de personas. Seleccione Confirmar si existe disponibilidad o Rechazar si no es posible atenderla. Después de la acción, vuelva a cargar la lista si desea comprobar el cambio.')
    add_para(doc, 'Resultado esperado: el estado de la reserva cambia y el cliente puede verlo desde Mis pedidos y reservas. Esta acción es importante porque la reserva no se confirma automáticamente.')
    add_heading(doc, '4.4 Cargar o reemplazar fotos de productos', level=2)
    add_para(doc, 'Desde Mi cuenta pulse Gestionar fotos de productos. Se presenta una lista del catálogo. Pulse el icono de cámara del producto que desea modificar, elija una imagen desde la galería o cámara del teléfono y confirme la selección. Use imágenes JPG o PNG con un tamaño máximo de 5 MB.')
    add_para(doc, 'Resultado esperado: la fila cambia a Foto cargada y la imagen aparece en el catálogo. Si hay error de conexión, de permiso o de bucket de almacenamiento, la aplicación muestra un mensaje y la foto anterior se conserva.')
    add_heading(doc, '4.5 Cambiar foto de portada', level=2)
    add_para(doc, 'Desde Mi cuenta pulse Cambiar foto de portada. Seleccione una imagen válida y espere la confirmación de carga. La portada se utiliza para identificar visualmente el negocio en la aplicación.')
    add_para(doc, 'Resultado esperado: se confirma el cambio y la nueva imagen se recupera desde Storage cuando la aplicación consulte la portada.')
    add_heading(doc, '5 Estados que verá en la aplicación')
    add_table(doc, ['Elemento', 'Estado', 'Significado para el usuario'], [
        ('Reserva', 'En espera', 'La solicitud fue registrada, pero el dueño aún no toma una decisión.'),
        ('Reserva', 'Confirmada', 'El dueño aceptó la solicitud. Se recomienda confirmar detalles con el negocio si fuera necesario.'),
        ('Reserva', 'Rechazada', 'El negocio no puede atender la solicitud en esas condiciones.'),
        ('Pedido', 'Registrado', 'El pedido fue guardado con su detalle y puede ser consultado en el historial.'),
        ('Fotos', 'Foto cargada', 'La imagen del producto fue guardada en Storage y está disponible para el catálogo.'),
    ], [1.1, 1.4, 4.15])
    add_heading(doc, '6 Mensajes y solución rápida')
    add_table(doc, ['Situación', 'Acción recomendada'], [
        ('No aparece información remota', 'Compruebe la conexión a Internet y vuelva a abrir la pantalla. Si persiste, use el botón Reintentar cuando esté disponible.'),
        ('No funciona la búsqueda por voz', 'Revise que el permiso de micrófono esté autorizado en Ajustes del teléfono. Luego vuelva a intentar.'),
        ('No se puede reservar', 'Verifique que la fecha sea futura y que todos los campos requeridos estén completos.'),
        ('No aparecen opciones de dueño', 'Cierre sesión e ingrese con la cuenta a la que se asignó el rol Dueño en Supabase.'),
        ('No se puede cargar una foto', 'Compruebe la conexión, el formato JPG o PNG y que el archivo no supere 5 MB.'),
    ], [2.2, 4.4])
    add_heading(doc, '7 Recomendación de uso')
    add_para(doc, 'La aplicación es un prototipo académico. Antes de considerar un pedido como atendido o una reserva como definitiva, el negocio debe confirmar la información a través de sus canales internos. Si se realizan pruebas, utilice datos de demostración y evite publicar contraseñas, números de cuenta o información personal en capturas de pantalla.')
    add_footer(doc)
    doc.save(OUT / 'Manual_de_uso_MVP.docx')


def guia_desarrollo():
    doc = Document()
    setup(doc, 'Guía de desarrollo y despliegue', 'Requisitos técnicos y compatibilidad de Brasas del Oriente')
    add_para(doc, 'Esta guía establece los requisitos para desarrollar, compilar, probar y desplegar la aplicación. El proyecto está orientado a Android y consume Supabase, Open Meteo, OpenStreetMap y servicios del sistema operativo como micrófono, galería, teléfono, mapas y WhatsApp.')
    add_heading(doc, '1 Requisitos de desarrollo')
    add_table(doc, ['Componente', 'Mínimo', 'Recomendado'], [
        ('Sistema operativo', 'Windows 10 de 64 bits, macOS o Linux compatible con Flutter', 'Windows 11 de 64 bits'),
        ('Flutter', 'Canal stable compatible con Dart 3.12 o superior', 'Última versión stable validada con flutter doctor'),
        ('Dart', 'SDK 3.12 o superior', 'Versión incluida por el SDK Flutter stable'),
        ('JDK', 'Java 17', 'Java 17 LTS'),
        ('Android Studio', 'Versión con Android SDK, Platform Tools y emulador', 'Versión estable más reciente'),
        ('Android Gradle Plugin', '9.0.1 según android/settings.gradle.kts', 'Mantener la versión definida por el proyecto'),
        ('Gradle Wrapper', '9.1.0 según gradle-wrapper.properties', 'Mantener la versión definida por el proyecto'),
        ('Memoria del equipo', '8 GB RAM', '16 GB RAM'),
        ('Espacio libre', '10 GB para SDK, cachés y compilación', '20 GB o más'),
    ], [1.55, 2.25, 2.8])
    add_heading(doc, '2 Dependencias principales')
    add_table(doc, ['Paquete', 'Uso'], [
        ('supabase_flutter', 'Autenticación, base de datos, Storage y RPC.'),
        ('flutter_map y latlong2', 'Mapa de OpenStreetMap.'),
        ('http', 'Consulta del clima con API REST.'),
        ('image_picker', 'Selección de fotos y comprobantes.'),
        ('speech_to_text', 'Búsqueda por voz con permiso RECORD_AUDIO.'),
        ('google_mlkit_text_recognition', 'OCR local para el extra de comprobantes.'),
        ('url_launcher', 'Llamadas, WhatsApp, rutas y enlaces externos.'),
    ], [2.2, 4.4])
    add_heading(doc, '3 Compatibilidad para usuarios finales')
    add_table(doc, ['Aspecto', 'Mínimo', 'Recomendado'], [
        ('Plataforma', 'Android 5.0 o superior, API 21 o superior', 'Android 10 o superior'),
        ('Pantalla', '360 x 640 dp aproximados', 'Teléfono con 6 pulgadas o más'),
        ('Memoria RAM', '2 GB', '4 GB o más'),
        ('Almacenamiento libre', '150 MB para instalación y caché', '500 MB o más'),
        ('Red', 'Internet para Supabase, clima y mapas', 'Wi Fi o 4G estable'),
        ('Micrófono', 'Necesario solo para búsqueda por voz', 'Micrófono operativo con permiso concedido'),
        ('Servicios externos', 'Aplicación de llamadas, mapas o WhatsApp según botón usado', 'Aplicaciones actualizadas'),
    ], [1.75, 2.35, 2.5])
    add_heading(doc, '4 Configuración para desarrollo')
    add_bullets(doc, [
        'Clone o copie el proyecto en una carpeta local sin alterar los archivos de código.',
        'Ejecute flutter pub get para instalar las dependencias bloqueadas en pubspec.lock.',
        'Cree un proyecto Supabase propio y ejecute los scripts de la carpeta supabase en el orden documentado en README.md.',
        'No coloque claves secretas ni service role dentro del código, GitHub, APK o variables públicas.',
        'Ejecute la aplicación usando SUPABASE_URL y SUPABASE_PUBLISHABLE_KEY como dart define.',
    ])
    add_heading(doc, '5 Pruebas y despliegue')
    add_table(doc, ['Etapa', 'Acción', 'Resultado esperado'], [
        ('Calidad estática', 'flutter analyze', 'No deben existir errores de análisis.'),
        ('Pruebas unitarias', 'flutter test', 'Las pruebas de modelos, validadores y flujos deben completarse.'),
        ('Emulador o teléfono', 'flutter run con variables Supabase', 'La aplicación inicia y puede iniciar sesión.'),
        ('APK de pruebas', 'flutter build apk --debug con variables Supabase', 'Se genera app-debug.apk para instalar manualmente.'),
        ('Publicación formal', 'Configurar firma release, revisar R8/ML Kit y construir release', 'APK o AAB firmado, probado y apto para distribución.'),
    ], [1.4, 2.7, 2.5])
    add_heading(doc, '6 Consideraciones de seguridad y operación')
    add_bullets(doc, [
        'Las políticas RLS de Supabase deben permanecer activas en tablas y buckets.',
        'Las operaciones administrativas deben requerir el rol Dueño.',
        'Las fotos y comprobantes se validan por formato y tamaño antes de cargarse.',
        'Un comprobante o resultado OCR no sustituye la comprobación bancaria real.',
        'Antes de distribuir una versión release, configure un certificado de firma distinto a la clave debug.',
    ])
    add_footer(doc)
    doc.save(OUT / 'Guia_de_desarrollo_y_despliegue.docx')


def write_readme():
    text = r'''# Guía de replicación en otra computadora

Esta guía permite preparar una computadora nueva para ejecutar **Brasas del Oriente**. La aplicación se desarrolló con Flutter para Android y utiliza Supabase como backend.

## 1. Requisitos

- Git.
- Flutter canal `stable` compatible con Dart `3.12` o superior.
- Android Studio con Android SDK, Platform Tools, emulador o teléfono físico.
- Java 17.
- Una cuenta y un proyecto en Supabase.
- Internet para descargar dependencias, conectarse a Supabase, consultar el clima y cargar mapas.

Verifica el entorno con:

```powershell
flutter doctor
```

## 2. Obtener el proyecto

```powershell
git clone URL_DEL_REPOSITORIO
cd actividad_1
flutter pub get
```

Si recibiste el proyecto como carpeta comprimida, descomprímelo y ejecuta los dos últimos comandos dentro de la carpeta raíz.

## 3. Configurar Supabase

1. Crea un proyecto en [Supabase](https://supabase.com/).
2. En **SQL Editor**, ejecuta los scripts de la carpeta `supabase/` en el orden indicado por el README principal.
3. Para el MVP, asegúrate de ejecutar los scripts de pedidos, cuentas, ubicación, Storage y fotos de productos.
4. Crea las cuentas necesarias y asigna el rol Dueño a la cuenta administradora según el script de roles.
5. Copia la URL del proyecto y la **Publishable key**. No uses `service_role` en Flutter.

## 4. Ejecutar en emulador o teléfono

Con un emulador iniciado o un teléfono conectado con depuración USB:

```powershell
flutter run --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La URL y la clave pública se entregan por comando para evitar guardarlas en el repositorio.

## 5. Comandos de calidad

```powershell
dart format lib test
flutter analyze
flutter test
```

También puedes ejecutar el script incluido:

```powershell
powershell -ExecutionPolicy Bypass -File .\herramientas\ejecutar_pruebas.ps1
```

## 6. Crear una APK para pruebas

```powershell
flutter build apk --debug --dart-define=SUPABASE_URL=https://TU_PROYECTO.supabase.co --dart-define=SUPABASE_PUBLISHABLE_KEY=TU_CLAVE_PUBLICA
```

La salida se encuentra en:

```text
build\app\outputs\flutter-apk\app-debug.apk
```

Pasa ese archivo a un teléfono Android e instala la APK autorizando instalaciones desde la fuente elegida.

## 7. Estructura relevante

```text
lib/           Código Flutter: páginas, servicios y modelos
test/          Pruebas automatizadas
supabase/      Scripts SQL, RLS, Storage y funciones RPC
herramientas/  Scripts auxiliares de diagnóstico y pruebas
documentación técnica/  Manuales del proyecto
```

## 8. Solución rápida de problemas

| Situación | Acción |
| --- | --- |
| La app indica que Supabase no está configurado | Inicia con ambos `--dart-define` y revisa URL/clave pública. |
| No se descargan paquetes | Comprueba Internet y ejecuta `flutter pub get`. |
| El teléfono no aparece | Activa Depuración USB, autoriza el equipo y ejecuta `flutter devices`. |
| Fallan fotos o Storage | Comprueba los buckets y políticas de Storage definidos en los scripts SQL. |
| No funciona voz | Acepta el permiso de micrófono y verifica que el dispositivo tenga reconocimiento de voz disponible. |

## Seguridad

No subas a GitHub secretos, contraseñas, claves `service_role`, datos bancarios ni archivos de configuración locales. La clave publishable es la única clave de Supabase que usa la aplicación cliente.
'''
    (OUT / 'README_replicacion.md').write_text(text, encoding='utf-8')


def write_stories():
    text = '''# Historias de usuario del MVP

Proyecto: **Brasas del Oriente**  
Versión: **1.0.0**

Estas historias describen el alcance mínimo del producto. Los pagos QR y comprobantes son funcionalidades complementarias y no condicionan la aceptación del MVP.

## Cliente

### HU C01 Catálogo con fotos

**Como** cliente, **quiero** ver el catálogo con nombre, foto, descripción, precio y rubro, **para** elegir productos antes de realizar un pedido.

**Criterios de aceptación**

- El catálogo muestra productos obtenidos desde Supabase.
- Cada tarjeta presenta nombre, descripción, precio y foto si fue cargada.
- El cliente puede agregar un producto al carrito.

### HU C02 Búsqueda y filtros

**Como** cliente, **quiero** buscar por texto, voz y rubro, **para** encontrar productos con rapidez.

**Criterios de aceptación**

- El texto filtra por nombre, descripción o rubro.
- Los filtros muestran solo el rubro seleccionado.
- La búsqueda por voz solicita permiso de micrófono y comunica los errores de permiso o conexión.

### HU C03 Carrito y pedido

**Como** cliente, **quiero** modificar cantidades y confirmar mi pedido, **para** solicitar los productos seleccionados.

**Criterios de aceptación**

- El carrito permite sumar y restar productos.
- El total se actualiza al modificar cantidades.
- El pedido solicita datos de contacto y registra el detalle en Supabase.

### HU C04 Consulta

**Como** cliente, **quiero** enviar una consulta con mis datos de contacto, **para** solicitar información al negocio.

**Criterios de aceptación**

- El formulario valida nombre, teléfono y mensaje.
- Una consulta válida se registra y muestra confirmación.

### HU C05 Reserva

**Como** cliente, **quiero** solicitar una reserva futura, **para** planificar mi visita.

**Criterios de aceptación**

- La fecha y hora deben ser futuras.
- La reserva se crea con estado En espera.
- La aplicación informa el resultado del registro.

### HU C06 Historial

**Como** cliente autenticado, **quiero** consultar mis pedidos y reservas, **para** conocer su estado.

**Criterios de aceptación**

- Solo se muestran los registros del usuario autenticado.
- Las reservas muestran En espera, Confirmada o Rechazada.
- Los pedidos conservan su información y estado asociado.

### HU C07 Ubicación

**Como** cliente, **quiero** consultar ubicación, horarios y medios de contacto, **para** llegar o comunicarme con el negocio.

**Criterios de aceptación**

- Se muestran dirección, horarios, teléfono y clima.
- Los botones permiten abrir llamada, WhatsApp, ruta y mapa cuando el dispositivo dispone de la aplicación correspondiente.

## Dueño

### HU D01 Acceso administrativo

**Como** dueño, **quiero** iniciar sesión y acceder a un panel administrativo, **para** gestionar las operaciones del negocio.

**Criterios de aceptación**

- Solo una cuenta con rol Dueño visualiza las acciones administrativas.
- Un cliente no puede acceder a páginas ni datos reservados para dueño.

### HU D02 Gestión de reservas

**Como** dueño, **quiero** confirmar o rechazar reservas en espera, **para** mantener disponible la información correcta para el cliente.

**Criterios de aceptación**

- El dueño ve las reservas registradas.
- Puede cambiar una reserva en espera a Confirmada o Rechazada.
- El cambio aparece en el historial del cliente.

### HU D03 Gestión de fotos

**Como** dueño, **quiero** cargar o reemplazar fotos de portada y productos, **para** mantener actualizado el catálogo.

**Criterios de aceptación**

- Solo el dueño puede abrir las pantallas de carga de fotos.
- Se aceptan imágenes JPG o PNG dentro del tamaño permitido.
- La foto cargada aparece en el catálogo o portada correspondiente.
'''
    (OUT / 'Historias_de_usuario_MVP.md').write_text(text, encoding='utf-8')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    manual_usuario()
    guia_desarrollo()
    write_readme()
    write_stories()
    print(f'Documentación creada en: {OUT}')
