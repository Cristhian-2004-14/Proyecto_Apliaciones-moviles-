import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from 'file:///C:/Users/Usuario/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const workspaceDir = 'C:\\Users\\Usuario\\Desktop\\actividad_1';
const skillDir = 'C:\\Users\\Usuario\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.1111.10930\\skills\\presentations';
const buildDir = path.join(workspaceDir, '.build-presentacion-avance');
const finalPath = path.join(workspaceDir, 'entregables', 'Presentacion_avance_Brasas_del_Oriente.pptx');
const draftPath = path.join(buildDir, 'presentacion-avance-borrador.pptx');
const W = 1280, H = 720;
const C = { coal: '#241A17', ember: '#D56D25', gold: '#F2B545', cream: '#FFF7F0', paper: '#FFFDFC', muted: '#745F54', line: '#E8D8CC', white: '#FFFFFF', green: '#2F7D5B', red: '#A34B39' };

async function writeBlob(file, blob) { await fs.writeFile(file, new Uint8Array(await blob.arrayBuffer())); }
function box(slide, x, y, w, h, fill = 'none', radius = undefined) {
  return slide.shapes.add({ geometry: radius ? 'roundRect' : 'rect', position: { left:x, top:y, width:w, height:h }, fill, line: { style:'solid', fill:'none', width:0 }, ...(radius ? { borderRadius: radius } : {}) });
}
function text(slide, value, x, y, w, h, size=24, color=C.coal, bold=false, align='left') {
  const s = slide.shapes.add({ geometry:'textbox', position:{left:x,top:y,width:w,height:h}, fill:'none', line:{style:'solid',fill:'none',width:0} });
  s.text = value; s.text.style = { fontFamily:'Aptos', fontSize:size, color, bold, alignment:align, verticalAlignment:'middle', marginLeft:0, marginRight:0, marginTop:0, marginBottom:0 };
  return s;
}
function title(slide, value, n) {
  text(slide, value, 72, 56, 950, 54, 34, C.coal, true);
  text(slide, `0${n}`, 1136, 61, 70, 30, 14, C.ember, true, 'right');
  box(slide, 72, 122, 110, 5, C.ember);
}
function footer(slide) { text(slide, 'Brasas del Oriente  |  Aplicaciones Móviles I', 72, 676, 640, 20, 12, C.muted); }
function bullet(slide, value, x, y, w, color=C.coal) { box(slide, x, y+10, 9, 9, C.ember, 'rounded-full'); text(slide, value, x+24, y, w-24, 40, 21, color); }
function chip(slide, label, x, y, w, fill, color) { box(slide,x,y,w,36,fill,'rounded-full'); text(slide,label,x+12,y+4,w-24,24,14,color,true,'center'); }

const p = Presentation.create({ slideSize: { width: W, height: H } });

// 1. Cover
{
 const s=p.slides.add(); s.background.fill=C.coal; box(s,0,0,W,H,C.coal); box(s,0,0,26,H,C.ember); box(s,850,0,430,H,'#3D2820');
 text(s,'BRASAS DEL ORIENTE',72,92,470,28,16,C.gold,true);
 text(s,'Avance del MVP\nmóvil',72,145,640,150,54,C.white,true);
 text(s,'Catálogo, consultas y reservas para una churrasquería local de Santa Cruz',72,330,610,74,25,'#F3DFD2');
 chip(s,'Flutter',72,455,115,C.ember,C.white); chip(s,'Material 3',202,455,135,'#5C3A2C','#FFE8D5'); chip(s,'Supabase',352,455,125,'#5C3A2C','#FFE8D5');
 text(s,'Presentación para video\nDuración: 5 minutos',72,590,300,50,18,'#D7BFB0');
 text(s,'01',962,120,160,80,66,C.gold,true,'center'); text(s,'AVANCE',950,215,190,32,19,C.white,true,'center');
 text(s,'Aplicaciones Móviles I',930,590,220,28,16,'#F3DFD2',false,'center');
}

// 2 Problem
{
 const s=p.slides.add(); s.background.fill=C.paper; title(s,'El problema que abordamos',2); footer(s);
 text(s,'Un negocio local necesita presentar su oferta y atender solicitudes sin depender solo de redes sociales.',72,164,650,78,27,C.coal,true);
 box(s,72,290,504,225,C.cream,'rounded-2xl');
 text(s,'Necesidad inicial',108,326,330,30,18,C.ember,true); bullet(s,'Mostrar un menú claro y fácil de explorar',108,375,380); bullet(s,'Canalizar consultas y solicitudes de mesa',108,432,380);
 box(s,650,290,558,225,'#F6E8DE','rounded-2xl');
 text(s,'Alcance académico',686,326,340,30,18,C.ember,true); bullet(s,'MVP para Android e iOS desde una sola base de código',686,375,450); bullet(s,'Datos y precios demostrativos',686,432,450);
}

// 3 Decision
{
 const s=p.slides.add(); s.background.fill=C.paper; title(s,'Por qué elegimos Flutter',3); footer(s);
 text(s,'La matriz ponderada favoreció Flutter para el alcance y presupuesto del MVP.',72,160,720,40,25,C.coal,true);
 s.charts.add('bar',{ position:{left:72,top:244,width:620,height:310}, categories:['Flutter','React Native','Nativo Android/iOS'], series:[{name:'Puntaje',values:[91,83,66],fill:C.ember}], hasLegend:false, dataLabels:{showValue:true,position:'outEnd'}, yAxis:{minimumScale:0,maximumScale:100,majorUnit:20,majorGridlines:{style:'solid',fill:'#E9DED6',width:1}}, xAxis:{tickLabels:{fontSize:15}}, });
 box(s,770,245,390,290,C.cream,'rounded-2xl'); text(s,'Criterios evaluados',806,282,250,28,18,C.ember,true); bullet(s,'Costo y mantenimiento',806,330,285); bullet(s,'Compatibilidad Android e iOS',806,380,285); bullet(s,'Rendimiento, ecosistema y aprendizaje',806,430,300);
 text(s,'Resultado: 91 de 100 puntos',72,585,390,30,18,C.muted);
}

// 4 functions
{
 const s=p.slides.add(); s.background.fill=C.paper; title(s,'Funciones implementadas',4); footer(s);
 text(s,'El MVP ya cubre el recorrido principal del usuario.',72,160,700,38,25,C.coal,true);
 const cards=[['01','Menú digital','Búsqueda y filtro por categoría con datos locales o remotos.'],['02','Reserva de mesa','Formulario con fecha, hora, cantidad y validaciones.'],['03','Consulta y ubicación','Canal de contacto, información de horarios y ubicación.']];
 cards.forEach((c,i)=>{const x=72+i*376; box(s,x,252,336,266,i===0?'#FCE8D7':C.cream,'rounded-2xl'); text(s,c[0],x+28,277,55,45,32,C.ember,true); text(s,c[1],x+28,341,275,32,21,C.coal,true); text(s,c[2],x+28,392,270,76,17,C.muted);});
 text(s,'También centralizamos el tema visual y la navegación entre pantallas.',72,575,900,32,19,C.muted);
}

// 5 architecture
{
 const s=p.slides.add(); s.background.fill=C.paper; title(s,'Cómo está organizado el proyecto',5); footer(s);
 text(s,'La estructura separa interfaz, lógica y acceso a datos.',72,160,700,38,25,C.coal,true);
 const cols=[['Pantallas','Inicio, catálogo, reserva, consulta y ubicación'],['Servicios','Lectura del catálogo y creación de reservas'],['Datos','Supabase preparado con scripts SQL y RLS']];
 cols.forEach((c,i)=>{const x=72+i*380; box(s,x,270,330,190,i===1?'#FCE8D7':C.cream,'rounded-2xl'); text(s,c[0],x+26,302,270,30,22,C.ember,true); text(s,c[1],x+26,352,270,72,18,C.coal); if(i<2) text(s,'›',x+338,336,28,42,40,C.ember,true,'center');});
 box(s,72,517,116,34,C.ember,'rounded-full'); text(s,'Flutter',72,517,116,34,18,C.white,true,'center'); text(s,'se comunica mediante servicios; Supabase conserva las reglas de acceso.',210,518,800,28,18,C.muted);
}

// 6 verification
{
 const s=p.slides.add(); s.background.fill=C.paper; title(s,'Validaciones y estado actual',6); footer(s);
 text(s,'Las pruebas de código están aprobadas. La demostración Android sigue pendiente de entorno.',72,160,1030,42,25,C.coal,true);
 box(s,72,250,500,250,'#E8F3EC','rounded-2xl'); text(s,'Comprobado',108,286,220,32,22,C.green,true); bullet(s,'flutter analyze: sin incidencias',108,341,370,C.green); bullet(s,'flutter test: navegación aprobada',108,395,370,C.green);
 box(s,636,250,572,250,'#FBEAE6','rounded-2xl'); text(s,'Pendiente de verificar',672,286,290,32,22,C.red,true); bullet(s,'JDK válido y dispositivo Android disponible',672,341,430,C.red); bullet(s,'Conexión real con Supabase y captura auténtica',672,395,440,C.red);
 text(s,'El proyecto no incorpora pagos ni autenticación.',72,565,700,32,19,C.muted);
}

// 7 demo close
{
 const s=p.slides.add(); s.background.fill=C.coal; title(s,'Demostración y siguiente paso',7); text(s,'Durante el video mostraremos:',72,170,610,40,27,C.white,true);
 const steps=[['1','Pantalla de bienvenida','Ingreso a la churrasquería'],['2','Menú digital','Búsqueda y filtros'],['3','Reserva','Validaciones del formulario']];
 steps.forEach((a,i)=>{const y=258+i*92; box(s,72,y,64,64,C.ember,'rounded-full'); text(s,a[0],72,y+13,64,34,25,C.white,true,'center'); text(s,a[1],166,y+5,260,30,21,C.gold,true); text(s,a[2],166,y+37,310,25,18,'#F3DFD2');});
 box(s,720,180,420,320,'#3D2820','rounded-2xl'); text(s,'Próximo avance',758,220,300,28,19,C.gold,true); text(s,'Configurar Android y Supabase para ejecutar el flujo completo con datos reales.',758,280,305,105,27,C.white,true); text(s,'Gracias',758,440,280,34,23,'#F3DFD2');
 text(s,'Brasas del Oriente',72,656,280,24,15,'#D7BFB0');
}

await fs.mkdir(buildDir,{recursive:true});
await fs.mkdir(path.dirname(finalPath),{recursive:true});
await (await PresentationFile.exportPptx(p)).save(draftPath);
const { finalizePresentation } = await import(new URL(`file:///${skillDir.replaceAll('\\','/')}/container_tools/artifact_tool_utils.mjs`).href);
await fs.mkdir(path.join(workspaceDir,'.codex-finalizer'),{recursive:true});
const result=await finalizePresentation({workspaceDir,candidatePath:draftPath,finalPath,pythonExecutable:'C:\\Users\\Usuario\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe',integrityValidatorPath:path.join(skillDir,'container_tools','inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skillDir,'container_tools','inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],requiredNativeChartOwnerSlides:[3],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:['Arial']},verifyArtifactToolImport:true,receiptPath:path.join(workspaceDir,'.codex-finalizer','presentacion-avance.validation.json')});
await writeBlob(path.join(buildDir,'montaje.webp'),await p.export({format:'webp',montage:true,scale:1}));
console.log(JSON.stringify({finalPath,result},null,2));
