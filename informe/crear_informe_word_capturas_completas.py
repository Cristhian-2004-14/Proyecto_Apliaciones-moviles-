from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(r"C:\Users\Usuario\Desktop\actividad_1")
MEDIA=ROOT/".qa_powerpoint_adj"/"ppt"/"media"
OUT=ROOT/"entregables"/"informe_avance_brasas_apa7_word_indice_funcional.docx"

doc=Document(); sec=doc.sections[0]
for a in ("top_margin","bottom_margin","left_margin","right_margin"): setattr(sec,a,Inches(1))
for n in ("Normal","Title","Heading 1","Heading 2"):
 st=doc.styles[n]; st.font.name="Times New Roman"; st._element.rPr.rFonts.set(qn("w:ascii"),"Times New Roman"); st._element.rPr.rFonts.set(qn("w:hAnsi"),"Times New Roman"); st.font.size=Pt(12)
def font(r,b=False,i=False,size=12):
 r.font.name="Times New Roman"; r._element.rPr.rFonts.set(qn("w:ascii"),"Times New Roman"); r._element.rPr.rFonts.set(qn("w:hAnsi"),"Times New Roman"); r.font.size=Pt(size); r.bold=b; r.italic=i
def p(txt="",align=WD_ALIGN_PARAGRAPH.LEFT,indent=True,italic=False):
 x=doc.add_paragraph(); x.alignment=align; x.paragraph_format.line_spacing=2; x.paragraph_format.space_after=Pt(0)
 if indent: x.paragraph_format.first_line_indent=Inches(.5)
 r=x.add_run(txt); font(r,i=italic); return x
def h(txt):
 x=doc.add_paragraph(style="Heading 1"); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.paragraph_format.line_spacing=2; x.paragraph_format.space_before=Pt(10); x.paragraph_format.space_after=Pt(6); x.paragraph_format.keep_with_next=True; font(x.add_run(txt),b=True); return x
def br(): doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
def figure(image,num,caption,explain):
 br(); h(f"Evidencia visual {num}")
 p(explain)
 q=doc.add_paragraph(); q.alignment=WD_ALIGN_PARAGRAPH.CENTER; q.paragraph_format.space_before=Pt(8); q.paragraph_format.space_after=Pt(3)
 # Conserva la captura completa. El ancho de 6.2 pulgadas mantiene la proporción y cabe en la página.
 q.add_run().add_picture(str(image),width=Inches(6.2))
 c=doc.add_paragraph(); c.alignment=WD_ALIGN_PARAGRAPH.CENTER; c.paragraph_format.line_spacing=1.15; c.paragraph_format.space_after=Pt(4); font(c.add_run(f"Figura {num}. {caption}"),i=True,size=11)
 p("La imagen se presenta completa para conservar el contexto de la prueba y permitir la lectura de los elementos visibles en la aplicación.",indent=False)

# Header page number
hp=sec.header.paragraphs[0]; hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT; rr=hp.add_run(); fld=OxmlElement("w:fldSimple"); fld.set(qn("w:instr"),"PAGE"); rr._r.append(fld); font(rr)

# Page 1
t=doc.add_paragraph(); t.alignment=WD_ALIGN_PARAGRAPH.CENTER; t.paragraph_format.line_spacing=2; t.paragraph_format.space_after=Pt(18); font(t.add_run("Informe de avance del MVP móvil Brasas del Oriente"),b=True)
h("Resumen")
p("Este informe presenta el desarrollo de Brasas del Oriente, un producto mínimo viable construido con Flutter para una churrasquería local. El proyecto reúne un menú digital, consultas, solicitudes de reserva y una sección de ubicación y horarios. También incorpora validaciones de formularios, una arquitectura organizada en pantallas, servicios y modelos, y una preparación inicial para Supabase. El documento muestra capturas completas de las pruebas visuales incluidas en la presentación del proyecto.",indent=False)
p("Palabras clave: Flutter, aplicación móvil, catálogo digital, reserva, Supabase.",indent=False,italic=True)

# Contenido principal. El índice navegable se agrega después mediante internal_nav.py.
br(); h("Introducción y problema")
p("Los negocios gastronómicos suelen usar redes sociales y mensajes para mostrar su oferta y atender consultas. Aunque estos canales son útiles, obligan al cliente a pedir información repetida sobre platos, precios, horarios o disponibilidad. Brasas del Oriente se plantea como un MVP que concentra esas acciones en una experiencia móvil sencilla.")
p("El problema central consiste en facilitar el acceso a la información y ordenar las solicitudes del usuario. La aplicación permite revisar el menú, enviar una consulta y solicitar una mesa. No pretende reemplazar todavía la gestión completa de un restaurante, sino validar el recorrido principal antes de incorporar procesos que requieren más seguridad, como pagos, autenticación y confirmación automática de disponibilidad.")
h("Objetivo general")
p("Desarrollar un MVP multiplataforma que permita al usuario conocer el menú de una churrasquería, registrar una consulta, solicitar una reserva y revisar la ubicación y los horarios del negocio.")

# Page 4
br(); h("Objetivos específicos y alcance")
p("Los objetivos específicos fueron diseñar una navegación clara, implementar un catálogo con búsqueda y filtros, crear formularios con validación local, organizar una capa de servicios para el acceso a datos y preparar scripts de Supabase con tablas, datos semilla y reglas de acceso.")
p("El alcance funcional incluye una pantalla de bienvenida, una pantalla principal con accesos directos, menú digital, consulta, reserva y ubicación. El catálogo puede mostrar datos locales cuando la configuración de Supabase no está disponible. Los formularios solicitan solo la información necesaria para la función que cumplen.")
p("El alcance no incluye pedidos con carrito, pagos, autenticación, panel administrativo ni confirmación automática de reservas. Estas funciones quedan como una posible fase posterior después de completar las pruebas en Android y verificar la conexión con los datos remotos.")

# Page 5
br(); h("Tecnología y diseño de la solución")
p("Se compararon Flutter, React Native y desarrollo nativo para Android e iOS. La matriz ponderada evaluó costo, rendimiento previsto, comunidad, compatibilidad y curva de aprendizaje. Flutter obtuvo 91 puntos sobre 100, React Native 83 y el desarrollo nativo 66. Para este caso, Flutter permitió concentrar el desarrollo en una base de código común.")
p("La aplicación usa Material 3 y una identidad visual basada en tonos cálidos relacionados con la parrilla. La estructura separa pantallas, widgets reutilizables, servicios, modelos y configuración. Esta división facilita mantener la interfaz y sustituir datos demostrativos por datos remotos sin modificar el flujo principal del usuario.")

figure(MEDIA/"image5.png",1,"Pantalla principal con accesos al menú, reserva y ubicación","La primera captura muestra la pantalla principal completa dentro del entorno de prueba. Se conservó el contexto del editor y del emulador porque forma parte de la evidencia proporcionada en la presentación.")
figure(MEDIA/"image20.png",2,"Pantalla de catálogo y estado de error controlado","La segunda captura evidencia que el catálogo contempla un estado de error y ofrece la opción Reintentar cuando no logra cargar la información.")
figure(MEDIA/"image23.png",3,"Formulario para enviar consultas","La tercera captura muestra los campos de nombre, teléfono y mensaje, además del botón de envío y el mensaje de confirmación visible al final.")
figure(MEDIA/"image25.png",4,"Formulario de reserva con mensajes de validación","La cuarta captura muestra cómo la interfaz comunica los errores de nombre y teléfono antes de permitir que la solicitud se complete.")
figure(MEDIA/"image26.png",5,"Formulario de reserva con datos de prueba","La quinta captura muestra el mismo flujo después de ingresar datos de prueba, seleccionar fecha y hora y dejar preparada la confirmación de reserva.")

# Page 11
br(); h("Pruebas y validaciones")
p("Las validaciones documentadas incluyen el formato del código, el análisis estático y una prueba automatizada de navegación. El comando dart format lib test finalizó sin cambios pendientes. El comando flutter analyze reportó que no existían incidencias. Además, flutter test aprobó una prueba de navegación definida para el proyecto.")
p("Las capturas visuales complementan estas verificaciones porque muestran los estados de la interfaz: acceso principal, catálogo, consulta y reserva. Sin embargo, las capturas no sustituyen una validación completa con un dispositivo Android. El reporte diferencia las evidencias de interfaz de las pruebas de ejecución pendientes.")

# Page 12
br(); h("Limitaciones y conclusiones")
p("La principal limitación actual corresponde al entorno Android. Se requiere un JDK válido y un emulador o dispositivo físico configurado para ejecutar el flujo completo. También queda pendiente verificar la configuración real de Supabase, la lectura remota del catálogo y el registro de consultas y reservas.")
p("El proyecto ya ofrece un avance funcional consistente con el objetivo de un MVP académico. Las pantallas implementadas muestran un recorrido comprensible para el usuario y las validaciones protegen los formularios contra datos incompletos. El siguiente paso consiste en realizar pruebas de extremo a extremo y ampliar el alcance solo después de confirmar la estabilidad del flujo existente.")

# Page 13
br(); h("Referencias")
for x in ["Flutter. (s. f.-a). FAQ. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/resources/faq", "Flutter. (s. f.-b). Flutter performance profiling. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/perf/ui-performance", "Meta. (s. f.). Platform-specific code. React Native. https://reactnative.dev/docs/platform-specific-code.html", "Google. (s. f.). Develop for Android. https://developer.android.com/develop", "Apple. (s. f.). SwiftUI. https://developer.apple.com/swiftui/"]:
 z=p(x,indent=False); z.paragraph_format.left_indent=Inches(.5); z.paragraph_format.first_line_indent=Inches(-.5)

OUT.parent.mkdir(parents=True,exist_ok=True); doc.save(OUT); print(OUT)
