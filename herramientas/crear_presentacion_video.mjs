import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspace = "C:/Users/Usuario/Desktop/actividad_1";
const outputDir = path.join(workspace, "entregables");
const renderDir = path.join(workspace, ".pptx-build-video");
const finalPath = path.join(outputDir, "Presentacion_video_Brasas_del_Oriente_Actividad_3_mejorada.pptx");

const images = {
  inicio: "C:/Users/Usuario/AppData/Local/Temp/codex-clipboard-01257bc1-dfb8-436c-a3b3-9c836a7df043.png",
  carrito: "C:/Users/Usuario/AppData/Local/Temp/codex-clipboard-77017dc9-6062-42a4-915f-ac23f54448dd.png",
  cuenta: "C:/Users/Usuario/AppData/Local/Temp/codex-clipboard-999993fe-79d0-42a9-aff3-bfc7a3b01e23.png",
  supabase: "C:/Users/Usuario/AppData/Local/Temp/codex-clipboard-f92d2d12-0379-40f1-ba49-c56d4b4863b4.png",
  ubicacion: "C:/Users/Usuario/AppData/Local/Temp/codex-clipboard-31bad35d-1bdc-49d8-b8d1-76addb0fac8c.png",
  mapa: "C:/Users/Usuario/AppData/Local/Temp/codex-clipboard-3ebfad46-9369-40f4-85af-35fdcfed83f3.png",
};

const W = 1280;
const H = 720;
const colors = {
  cream: "#FFF8F2",
  dark: "#291A15",
  orange: "#D96E22",
  brown: "#9D542A",
  pale: "#FDEDE4",
  ink: "#2A211E",
  muted: "#6E625D",
  white: "#FFFFFF",
};
const imageAssets = new Map();

function text(slide, value, position, style = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = value;
  shape.text.style = {
    fontFamily: "Aptos",
    fontSize: "20pt",
    color: colors.ink,
    ...style,
  };
  return shape;
}

function rect(slide, position, fill, radius = "rounded-xl") {
  return slide.shapes.add({
    geometry: "roundRect",
    position,
    fill,
    line: { style: "solid", fill, width: 0 },
    borderRadius: radius,
  });
}

function image(slide, imagePath, position, fit = "contain") {
  return slide.images.add({
    blob: imageAssets.get(imagePath),
    contentType: "image/png",
    alt: "Captura de la aplicación Brasas del Oriente",
    fit,
    position,
    geometry: "roundRect",
    borderRadius: "rounded-xl",
  });
}

function base(slide, section) {
  slide.background.fill = colors.cream;
  rect(slide, { left: 0, top: 0, width: W, height: 14 }, colors.orange, "rounded-sm");
  text(slide, section.toUpperCase(), { left: 76, top: 44, width: 500, height: 24 }, {
    fontSize: "11pt", bold: true, color: colors.orange,
  });
  text(slide, "Brasas del Oriente · Actividad 3", { left: 76, top: 684, width: 450, height: 18 }, {
    fontSize: "10pt", color: colors.muted,
  });
}

function title(slide, value, subtitle) {
  text(slide, value, { left: 76, top: 92, width: 575, height: 122 }, {
    fontSize: "30pt", bold: true, color: colors.dark,
  });
  if (subtitle) {
    text(slide, subtitle, { left: 76, top: 246, width: 540, height: 100 }, {
      fontSize: "16pt", color: colors.muted,
    });
  }
}

function note(slide, value, top = 560) {
  rect(slide, { left: 76, top, width: 560, height: 66 }, colors.pale);
  text(slide, value, { left: 104, top: top + 16, width: 510, height: 34 }, {
    fontSize: "14pt", color: colors.ink,
  });
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(renderDir, { recursive: true });
for (const imagePath of Object.values(images)) {
  const bytes = await fs.readFile(imagePath);
  imageAssets.set(
    imagePath,
    bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength),
  );
}

const deck = Presentation.create({ slideSize: { width: W, height: H } });

// 1. Portada
{
  const slide = deck.slides.add();
  slide.background.fill = colors.cream;
  rect(slide, { left: 0, top: 0, width: W, height: 24 }, colors.orange, "rounded-sm");
  rect(slide, { left: 76, top: 116, width: 16, height: 410 }, colors.orange, "rounded");
  text(slide, "Actividad 3", { left: 128, top: 126, width: 400, height: 34 }, {
    fontSize: "17pt", bold: true, color: colors.orange,
  });
  text(slide, "Brasas del\nOriente", { left: 128, top: 180, width: 680, height: 172 }, {
    fontSize: "48pt", bold: true, color: colors.dark,
  });
  text(slide, "Aplicación Flutter para una churrasquería en Santa Cruz", { left: 128, top: 382, width: 660, height: 44 }, {
    fontSize: "21pt", color: colors.muted,
  });
  text(slide, "Supabase · pedidos · cuentas · clima · servicios externos", { left: 128, top: 458, width: 760, height: 34 }, {
    fontSize: "18pt", color: colors.brown,
  });
  text(slide, "SIS-0180 Aplicaciones Móviles I", { left: 128, top: 606, width: 410, height: 26 }, {
    fontSize: "14pt", color: colors.muted,
  });
}

// 2. Inicio
{
  const slide = deck.slides.add();
  base(slide, "Presentación");
  title(slide, "Una app para Brasas del Oriente", "La pantalla principal reúne las funciones que el cliente necesita para consultar, pedir y reservar.");
  image(slide, images.inicio, { left: 760, top: 54, width: 360, height: 610 });
  note(slide, "Menú digital, pedidos, cuenta, reservas, consultas y ubicación.");
}

// 3. Carrito
{
  const slide = deck.slides.add();
  base(slide, "Menú y carrito");
  title(slide, "Productos y pedido digital", "Cada producto presenta nombre y precio. El cliente agrega opciones, ajusta cantidades y visualiza el total antes de confirmar.");
  image(slide, images.carrito, { left: 760, top: 54, width: 360, height: 610 });
  note(slide, "El pedido de ejemplo incluye lomo fino y limonada de hierbabuena por Bs. 100.");
}

// 4. Supabase
{
  const slide = deck.slides.add();
  base(slide, "Pedido y Supabase");
  title(slide, "Datos del negocio en Supabase", "Al confirmar un pedido, la app solicita nombre y teléfono. El servicio registra el pedido y sus productos en Supabase.");
  image(slide, images.supabase, { left: 620, top: 154, width: 580, height: 340 }, "contain");
  note(slide, "El catálogo de Brasas del Oriente se consulta desde la tabla negocios.");
}

// 5. Roles
{
  const slide = deck.slides.add();
  base(slide, "Cuentas y roles");
  title(slide, "Acceso para cliente y dueño", "Supabase Authentication permite iniciar sesión. El dueño recibe acceso al panel de pedidos, mientras el cliente usa las funciones normales.");
  image(slide, images.cuenta, { left: 760, top: 54, width: 360, height: 610 });
  note(slide, "El perfil de prueba muestra el rol Dueño y el botón para abrir su panel.");
}

// 6. Clima y contacto
{
  const slide = deck.slides.add();
  base(slide, "Clima y contacto");
  title(slide, "Ubicación, clima y acciones externas", "Open-Meteo consulta el clima de Santa Cruz. La app también permite llamar, contactar por WhatsApp, solicitar una ruta y abrir el mapa.");
  image(slide, images.ubicacion, { left: 760, top: 54, width: 360, height: 610 });
  note(slide, "La tarjeta de clima administra los estados de carga, error y reintento.");
}

// 7. Mapa
{
  const slide = deck.slides.add();
  base(slide, "Mapa");
  title(slide, "Ubicación con OpenStreetMap", "El marcador sitúa a Brasas del Oriente en Santa Cruz. Elegimos OpenStreetMap, por lo que no incorporamos una clave privada de Google.");
  image(slide, images.mapa, { left: 760, top: 54, width: 360, height: 610 });
  note(slide, "El crédito visible © OpenStreetMap contributors identifica el proveedor del mapa.");
}

// 8. Cierre
{
  const slide = deck.slides.add();
  slide.background.fill = colors.dark;
  rect(slide, { left: 0, top: 0, width: W, height: 18 }, colors.orange, "rounded-sm");
  text(slide, "Cierre", { left: 96, top: 110, width: 260, height: 34 }, {
    fontSize: "17pt", bold: true, color: "#F6B36F",
  });
  text(slide, "Tecnologías aplicadas", { left: 96, top: 166, width: 860, height: 68 }, {
    fontSize: "38pt", bold: true, color: colors.white,
  });
  text(slide, "Flutter para la interfaz móvil. Supabase para autenticación y datos.\nAPI REST y JSON para el clima. Servicios externos para contacto y rutas.", { left: 96, top: 270, width: 960, height: 116 }, {
    fontSize: "21pt", color: "#F2E5DE",
  });
  rect(slide, { left: 96, top: 466, width: 940, height: 84 }, "#422D24");
  text(slide, "Codex IA apoyó el diagnóstico, la organización y la revisión técnica del proyecto.", { left: 126, top: 492, width: 880, height: 36 }, {
    fontSize: "17pt", color: "#F6B36F",
  });
  text(slide, "Gracias", { left: 96, top: 612, width: 300, height: 44 }, {
    fontSize: "25pt", bold: true, color: colors.white,
  });
}

for (let i = 0; i < deck.slides.count; i += 1) {
  const slide = deck.slides.getItem(i);
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await writeBlob(path.join(renderDir, `slide-${String(i + 1).padStart(2, "0")}.png`), png);
}

const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(finalPath);
console.log(finalPath);
