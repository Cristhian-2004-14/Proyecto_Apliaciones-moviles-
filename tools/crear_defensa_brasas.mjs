import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = 'C:\\Users\\Usuario\\Desktop\\actividad_1';
const buildDir = path.join(workspaceDir, '.codex-build-defensa');
const outputDir = path.join(workspaceDir, 'entregables');
const draftPath = path.join(buildDir, 'Brasas_del_Oriente_Defensa_borrador.pptx');

const c = {
  ink: '#241713',
  cocoa: '#3B2720',
  cream: '#FFF7F0',
  peach: '#FCE8DC',
  orange: '#D96F28',
  gold: '#F0B35C',
  muted: '#765F55',
  white: '#FFFFFF',
  green: '#2E7D5B',
};

function box(slide, { left, top, width, height, text = '', size = '20pt', color = c.ink, bold = false, fill = 'none', line = 'none', align = 'left', valign = 'top', geometry = 'textbox' }) {
  const shape = slide.shapes.add({
    geometry,
    position: { left, top, width, height },
    fill,
    line: { style: 'solid', fill: line, width: line === 'none' ? 0 : 1 },
  });
  shape.text = text;
  shape.text.style = {
    fontFace: 'Aptos',
    fontSize: size,
    color,
    bold,
    alignment: align,
    verticalAlignment: valign,
    marginLeft: 0,
    marginRight: 0,
    marginTop: 0,
    marginBottom: 0,
  };
  return shape;
}

function rect(slide, left, top, width, height, fill, geometry = 'rect') {
  return slide.shapes.add({
    geometry,
    position: { left, top, width, height },
    fill,
    line: { style: 'solid', fill, width: 0 },
  });
}

function base(slide, number, title, subtitle = '') {
  slide.background.fill = c.cream;
  rect(slide, 0, 0, 1280, 18, c.orange);
  box(slide, { left: 72, top: 54, width: 950, height: 54, text: title, size: '30pt', color: c.ink, bold: true });
  if (subtitle) box(slide, { left: 74, top: 115, width: 1000, height: 34, text: subtitle, size: '14pt', color: c.muted });
  box(slide, { left: 1122, top: 666, width: 86, height: 20, text: String(number).padStart(2, '0'), size: '11pt', color: c.muted, align: 'right' });
  box(slide, { left: 72, top: 668, width: 450, height: 18, text: 'Brasas del Oriente · Defensa del proyecto', size: '10pt', color: c.muted });
}

function bullet(slide, x, y, w, text, color = c.ink) {
  rect(slide, x, y + 10, 10, 10, c.orange, 'ellipse');
  box(slide, { left: x + 26, top: y, width: w - 26, height: 42, text, size: '18pt', color });
}

function step(slide, x, y, number, title, body) {
  rect(slide, x, y, 46, 46, c.orange, 'ellipse');
  box(slide, { left: x, top: y + 9, width: 46, height: 27, text: String(number), size: '17pt', color: c.white, bold: true, align: 'center' });
  box(slide, { left: x + 64, top: y - 2, width: 280, height: 30, text: title, size: '18pt', color: c.ink, bold: true });
  box(slide, { left: x + 64, top: y + 31, width: 270, height: 48, text: body, size: '14pt', color: c.muted });
}

async function main() {
  await fs.mkdir(buildDir, { recursive: true });
  await fs.mkdir(outputDir, { recursive: true });
  const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });

  // 1. Cover
  {
    const s = presentation.slides.add();
    s.background.fill = c.cocoa;
    rect(s, 0, 0, 26, 720, c.orange);
    box(s, { left: 88, top: 110, width: 760, height: 30, text: 'APLICACIÓN MÓVIL PARA CHURRASQUERÍA', size: '14pt', color: c.gold, bold: true });
    box(s, { left: 86, top: 168, width: 720, height: 155, text: 'Brasas del\nOriente', size: '48pt', color: c.cream, bold: true });
    rect(s, 90, 350, 110, 7, c.orange);
    box(s, { left: 88, top: 392, width: 665, height: 90, text: 'Catálogo, pedidos, reservas, pagos QR y gestión del negocio desde Flutter.', size: '24pt', color: '#EEDFD4' });
    rect(s, 910, 165, 244, 244, c.gold, 'roundRect');
    box(s, { left: 936, top: 230, width: 192, height: 90, text: 'MVP\nFlutter', size: '30pt', color: c.cocoa, bold: true, align: 'center', valign: 'middle' });
    box(s, { left: 88, top: 620, width: 690, height: 24, text: 'Defensa del proyecto · Aplicaciones Móviles', size: '14pt', color: '#C9B2A5' });
  }

  // 2. Problem and proposal
  {
    const s = presentation.slides.add();
    base(s, 2, 'Problema y propuesta', 'Digitalización del contacto entre clientes y la churrasquería');
    box(s, { left: 82, top: 190, width: 420, height: 45, text: 'Necesidad identificada', size: '22pt', color: c.orange, bold: true });
    box(s, { left: 82, top: 252, width: 410, height: 170, text: 'Los clientes necesitan consultar productos, reservar y solicitar pedidos sin depender de mensajes informales.', size: '25pt', color: c.ink, bold: true });
    rect(s, 560, 178, 6, 312, c.orange);
    box(s, { left: 616, top: 190, width: 480, height: 45, text: 'Respuesta del proyecto', size: '22pt', color: c.orange, bold: true });
    bullet(s, 620, 260, 490, 'Catálogo digital con productos, fotos y precios');
    bullet(s, 620, 326, 490, 'Pedidos y reservas vinculados a una cuenta');
    bullet(s, 620, 392, 490, 'Panel para que el dueño gestione la operación');
  }

  // 3. Architecture
  {
    const s = presentation.slides.add();
    base(s, 3, 'Desarrollo y arquitectura', 'Tecnologías aplicadas durante la implementación');
    const cols = [90, 374, 658, 942];
    const titles = ['Flutter', 'Supabase', 'Servicios externos', 'Storage'];
    const bodies = [
      'Interfaz móvil, navegación, formularios y estados de la aplicación.',
      'Autenticación, perfiles, roles, tablas, funciones SQL y políticas RLS.',
      'Open-Meteo para clima, OpenStreetMap y reconocimiento de voz.',
      'Supabase Storage para portada, fotos del catálogo y comprobantes.'
    ];
    for (let i = 0; i < cols.length; i++) {
      rect(s, cols[i], 220, 240, 245, c.peach, 'roundRect');
      box(s, { left: cols[i] + 24, top: 257, width: 192, height: 54, text: titles[i], size: '20pt', color: c.ink, bold: true, align: 'center' });
      box(s, { left: cols[i] + 24, top: 330, width: 192, height: 100, text: bodies[i], size: '15pt', color: c.muted, align: 'center' });
    }
    box(s, { left: 172, top: 540, width: 930, height: 34, text: 'La aplicación protege los datos mediante autenticación, roles de cliente y dueño, y reglas de acceso por fila.', size: '17pt', color: c.muted, align: 'center' });
  }

  // 4. Customer MVP
  {
    const s = presentation.slides.add();
    base(s, 4, 'Recorrido principal del cliente', 'Funciones MVP que el usuario puede completar desde el teléfono');
    step(s, 95, 195, 1, 'Explora el menú', 'Filtra categorías, busca por texto o usa la búsqueda por voz.');
    step(s, 95, 325, 2, 'Crea su pedido', 'Agrega productos al carrito, revisa el total y confirma sus datos.');
    step(s, 95, 455, 3, 'Consulta su estado', 'Ve pedidos, reservas y sus estados desde Mi cuenta.');
    rect(s, 720, 185, 370, 335, c.cocoa, 'roundRect');
    box(s, { left: 764, top: 230, width: 282, height: 42, text: 'MVP del cliente', size: '22pt', color: c.gold, bold: true, align: 'center' });
    box(s, { left: 764, top: 301, width: 282, height: 192, text: 'Catálogo\nCarrito\nPedidos\nReservas\nConsultas\nUbicación y clima', size: '20pt', color: c.cream, bold: true, align: 'center' });
  }

  // 5. Owner
  {
    const s = presentation.slides.add();
    base(s, 5, 'Herramientas del dueño', 'El rol de dueño concentra las tareas administrativas');
    box(s, { left: 82, top: 187, width: 430, height: 48, text: 'Contenido del negocio', size: '22pt', color: c.orange, bold: true });
    bullet(s, 88, 260, 455, 'Cambiar la foto de portada del negocio');
    bullet(s, 88, 330, 455, 'Subir o reemplazar fotos reales de productos');
    box(s, { left: 702, top: 187, width: 410, height: 48, text: 'Operación diaria', size: '22pt', color: c.orange, bold: true });
    bullet(s, 702, 260, 450, 'Revisar pedidos y comprobantes de pago');
    bullet(s, 702, 330, 450, 'Aceptar o denegar reservas de mesa');
    bullet(s, 702, 400, 450, 'Confirmar o rechazar pagos tras verificar el abono');
    rect(s, 82, 520, 1080, 5, c.gold);
    box(s, { left: 110, top: 555, width: 1030, height: 40, text: 'El sistema muestra opciones administrativas únicamente a los perfiles con rol de dueño.', size: '18pt', color: c.muted, align: 'center' });
  }

  // 6. QR
  {
    const s = presentation.slides.add();
    base(s, 6, 'Pago por QR con revisión manual', 'Alternativa implementada mientras una pasarela bancaria requiere trámites y una API formal');
    rect(s, 82, 190, 1090, 96, c.peach, 'roundRect');
    box(s, { left: 118, top: 216, width: 1006, height: 46, text: 'El cliente escanea el QR, transfiere el monto exacto y adjunta su comprobante.', size: '24pt', color: c.ink, bold: true, align: 'center' });
    step(s, 115, 365, 1, 'Pago QR', 'El sistema presenta el QR fijo y el monto del pedido.');
    step(s, 470, 365, 2, 'Comprobante', 'El cliente adjunta una imagen JPG o PNG para revisión.');
    step(s, 825, 365, 3, 'Validación', 'El dueño compara los datos y decide confirmar o rechazar.');
    box(s, { left: 150, top: 555, width: 980, height: 44, text: 'La carga del comprobante no confirma el pago por sí sola. El dueño debe constatar el abono bancario.', size: '17pt', color: c.muted, align: 'center' });
  }

  // 7. Evidence & quality
  {
    const s = presentation.slides.add();
    base(s, 7, 'Calidad y evidencia', 'Controles aplicados antes de la entrega del MVP');
    const rows = [
      ['Datos', 'Supabase guarda pedidos, reservas, perfiles, pagos y comprobantes.'],
      ['Accesos', 'RLS y roles separan las acciones del cliente y del dueño.'],
      ['Estados', 'Pedidos y reservas muestran espera, confirmación o rechazo.'],
      ['Pruebas', 'Análisis Flutter, pruebas de flujos y guía de validación UAT.'],
    ];
    let y = 190;
    for (const [label, description] of rows) {
      rect(s, 104, y, 194, 68, c.cocoa, 'roundRect');
      box(s, { left: 122, top: y + 21, width: 158, height: 28, text: label, size: '17pt', color: c.cream, bold: true, align: 'center' });
      box(s, { left: 335, top: y + 15, width: 750, height: 44, text: description, size: '17pt', color: c.ink });
      y += 87;
    }
    box(s, { left: 120, top: 556, width: 980, height: 58, text: 'Resultado: una aplicación demostrable con datos persistentes y funciones centrales para cliente y dueño.', size: '16pt', color: c.orange, bold: true, align: 'center', valign: 'middle' });
  }

  // 8. UAT
  {
    const s = presentation.slides.add();
    s.background.fill = c.cocoa;
    rect(s, 0, 0, 1280, 18, c.orange);
    box(s, { left: 90, top: 92, width: 940, height: 62, text: 'Validación final con UAT', size: '36pt', color: c.cream, bold: true });
    box(s, { left: 90, top: 175, width: 930, height: 58, text: 'El ingeniero puede seguir la guía UAT y verificar que el MVP responde como se espera.', size: '21pt', color: '#EEDFD4' });
    const checks = [
      'Consultar el catálogo y buscar un producto',
      'Crear un pedido y comprobar su estado',
      'Crear una reserva y gestionarla como dueño',
      'Realizar el flujo QR con comprobante',
      'Revisar fotos, búsqueda por voz y datos de contacto',
    ];
    let y = 285;
    for (const item of checks) {
      rect(s, 98, y + 4, 26, 26, c.gold, 'ellipse');
      box(s, { left: 101, top: y + 7, width: 20, height: 17, text: '✓', size: '12pt', color: c.cocoa, bold: true, align: 'center' });
      box(s, { left: 148, top: y, width: 850, height: 38, text: item, size: '18pt', color: c.cream });
      y += 53;
    }
    rect(s, 91, 590, 650, 4, c.orange);
    box(s, { left: 90, top: 620, width: 760, height: 32, text: 'Documento de apoyo: Protocolo UAT y guía de uso del MVP', size: '15pt', color: c.gold });
  }

  const file = await PresentationFile.exportPptx(presentation);
  await file.save(draftPath);
  console.log(JSON.stringify({ draftPath, slideCount: presentation.slides.items.length }));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
