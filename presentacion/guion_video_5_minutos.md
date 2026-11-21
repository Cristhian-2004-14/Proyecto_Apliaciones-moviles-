# Guion para video de avance: Brasas del Oriente

**Duración total:** aproximadamente 5 minutos.  
**Consejo:** hablen con la presentación en pantalla y cambien a la app solo en la demostración final.

## Distribución del equipo

- **Persona 1:** diapositivas 1 a 3. Aproximadamente 1 minuto y 35 segundos.
- **Persona 2:** diapositivas 4 y 5. Aproximadamente 1 minuto y 35 segundos.
- **Persona 3:** diapositivas 6 y 7, incluida la demostración. Aproximadamente 1 minuto y 50 segundos.

## Persona 1: contexto y tecnología

### Diapositiva 1. Portada — 20 segundos

**Decir:**

“Buenos días. Somos el equipo de Brasas del Oriente. En este video mostraremos el avance de nuestro MVP móvil para una churrasquería local de Santa Cruz. La aplicación busca facilitar el acceso al menú, las consultas y las solicitudes de reserva.”

**Mostrar:** la portada de la presentación.

### Diapositiva 2. Problema — 35 segundos

**Decir:**

“Partimos de una necesidad sencilla: un negocio local requiere un canal digital para presentar su oferta y recibir solicitudes sin depender únicamente de las redes sociales. Por eso definimos un MVP que permite explorar el menú, enviar consultas y solicitar una mesa. Los datos y precios que se muestran son demostrativos, porque se trata de un proyecto académico.”

**Mostrar:** la diapositiva 2. Señalen los bloques de necesidad inicial y alcance académico.

### Diapositiva 3. Tecnología elegida — 40 segundos

**Decir:**

“Antes de desarrollar, comparamos Flutter, React Native y desarrollo nativo para Android e iOS. Usamos una matriz ponderada con criterios de costo, rendimiento, comunidad, compatibilidad y curva de aprendizaje. Flutter obtuvo 91 de 100 puntos. Lo elegimos porque permite trabajar desde una sola base de código y se adapta al alcance inicial del proyecto.”

**Mostrar:** la gráfica. Señalen primero Flutter y luego los criterios de la derecha.

**Transición:** “Ahora explicará [nombre de la persona 2] las funciones que ya implementamos y cómo organizamos el proyecto.”

## Persona 2: funciones y estructura técnica

### Diapositiva 4. Funciones implementadas — 55 segundos

**Decir:**

“En el avance actual ya implementamos tres grupos de funciones. Primero, el menú digital incluye búsqueda y filtros por categoría. Segundo, la reserva de mesa solicita nombre, teléfono, fecha, hora y cantidad de personas, y valida los datos antes de enviarlos. Tercero, añadimos un canal de consulta y la pantalla de ubicación y horarios. También unificamos la apariencia con Material 3 y organizamos la navegación entre pantallas.”

**Mostrar:** la diapositiva 4. No abran aún la app para mantener el ritmo.

### Diapositiva 5. Organización técnica — 40 segundos

**Decir:**

“El proyecto está organizado en capas. Las pantallas contienen la interfaz del usuario. Los servicios se encargan de consultar el catálogo y registrar las reservas. Finalmente, dejamos preparada la integración con Supabase mediante configuración, scripts SQL y reglas de acceso. Esta separación facilita mantener el código y conectar datos reales en la siguiente etapa.”

**Mostrar:** la diapositiva 5. Recorran visualmente de izquierda a derecha.

**Transición:** “Finalmente, [nombre de la persona 3] mostrará las validaciones realizadas, los pendientes y una breve demostración.”

## Persona 3: validaciones, demostración y cierre

### Diapositiva 6. Validaciones y límites — 45 segundos

**Decir:**

“Verificamos la calidad del código con `flutter analyze`, que no reportó incidencias, y con pruebas automatizadas de navegación, que aprobaron correctamente. Aún no afirmamos una ejecución completa en Android, porque el entorno requiere un JDK válido y un dispositivo o emulador configurado. También queda pendiente comprobar la conexión real con Supabase. No incluimos pagos ni autenticación en este MVP.”

**Mostrar:** la diapositiva 6. Señalen que lo verde está comprobado y lo rojo es pendiente.

### Diapositiva 7. Demostración y cierre — 65 segundos

**Decir mientras demuestran:**

“Para cerrar, mostraremos el recorrido principal. Esta es la pantalla de bienvenida. Al ingresar, el usuario puede acceder al menú digital. Aquí puede buscar un plato o filtrar por categoría. Después ingresamos al formulario de reserva. El sistema solicita los campos necesarios y valida, por ejemplo, que el teléfono tenga el formato correcto y que se elija fecha y hora. El siguiente avance será configurar el entorno Android y Supabase para ejecutar este mismo flujo con datos reales.”

“Muchas gracias.”

**Mostrar:** cambien desde la diapositiva a la app. Recorrido sugerido: bienvenida, ingreso, menú, búsqueda o filtro, reserva y un ejemplo de validación. Si la app no puede ejecutarse, muestren el código de `lib/pages/inicio_page.dart`, `lib/pages/catalogo_page.dart` y `lib/pages/reserva_page.dart` mientras explican la misma secuencia, e indiquen que la ejecución Android está pendiente.
