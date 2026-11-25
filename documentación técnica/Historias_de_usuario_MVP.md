# Historias de usuario del MVP

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
