import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const workspaceDir = "C:/Users/Usuario/Desktop/actividad_1";
const skillDir = "C:/Users/Usuario/.codex/plugins/cache/openai-primary-runtime/presentations/26.1117.12345/skills/presentations";
const runtimePython = "C:/Users/Usuario/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";
const candidatePath = path.join(workspaceDir, "entregables", "Presentacion_video_Brasas_del_Oriente_Actividad_3_mejorada.pptx");
const finalPath = path.join(workspaceDir, "entregables", "Presentacion_video_Brasas_del_Oriente_Actividad_3_mejorada_final.pptx");
const stagingDir = path.join(workspaceDir, ".codex-finalizer-video");

const { finalizePresentation } = await import(pathToFileURL(
  path.join(skillDir, "container_tools", "artifact_tool_utils.mjs"),
).href);

await fs.mkdir(stagingDir, { recursive: true });
const result = await finalizePresentation({
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools", "inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-bullet-geometry", "--validate-heading-fit"],
  explicitTotalSlideCount: 8,
  requiredNativeTableOwnerSlides: [],
  fontPolicy: { basis: "design", families: ["Arial"] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, "validation-v3.json"),
});
console.log(JSON.stringify(result, null, 2));
