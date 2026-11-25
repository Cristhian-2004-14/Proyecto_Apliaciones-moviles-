import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';

const root = 'C:\\Users\\Usuario\\Desktop\\actividad_1';
const input = path.join(root, 'entregables', 'Brasas_del_Oriente_Defensa_del_Proyecto_v2.pptx');
const out = path.join(root, '.codex-build-defensa', 'renders');
await fs.mkdir(out, { recursive: true });
const presentation = await PresentationFile.importPptx(await FileBlob.load(input));
for (const [index, slide] of presentation.slides.items.entries()) {
  const png = await presentation.export({ slide, format: 'png', scale: 1 });
  await fs.writeFile(path.join(out, `slide-${String(index + 1).padStart(2, '0')}.png`), new Uint8Array(await png.arrayBuffer()));
}
console.log(out);
