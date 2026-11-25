import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const workspaceDir = 'C:\\Users\\Usuario\\Desktop\\actividad_1';
const skillDir = 'C:\\Users\\Usuario\\.codex\\plugins\\cache\\openai-primary-runtime\\presentations\\26.1123.11515\\skills\\presentations';
const buildDir = path.join(workspaceDir, '.codex-build-defensa');
const candidatePath = path.join(buildDir, 'Brasas_del_Oriente_Defensa_borrador.pptx');
const finalPath = path.join(workspaceDir, 'entregables', 'Brasas_del_Oriente_Defensa_del_Proyecto_v2.pptx');
const runtimePython = 'C:\\Users\\Usuario\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe';

const { finalizePresentation } = await import(pathToFileURL(
  path.join(skillDir, 'container_tools', 'artifact_tool_utils.mjs'),
).href);

await fs.mkdir(path.dirname(finalPath), { recursive: true });
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, 'container_tools', 'inspect_presentation_package_integrity.py'),
  layoutValidatorPath: path.join(skillDir, 'container_tools', 'inspect_presentation_layout_geometry.py'),
  layoutArgs: ['--expected-slide-size-emu', '12192000,6858000', '--validate-heading-fit'],
  explicitTotalSlideCount: 8,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  // Artifact Tool materializa la tipografía editable como Arial en el PPTX.
  fontPolicy: { basis: 'design', families: ['Arial'] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(buildDir, 'defensa-validacion-v2.json'),
});
console.log(JSON.stringify(result));
