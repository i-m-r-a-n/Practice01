import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Reapply the existing released six-door Boolean repair to the named fallback copy.
// This is not a new layout: dimensions/cutters are audited by the asset pipeline.
export async function applyDoorwayRepairs(model, manifest) {
  const status = { required: !!manifest.repairs?.length, state: 'not-provided', objects: [] };
  if (!manifest.repairs?.length) return status;
  const materials = new Map();
  model.traverse(o => { if (o.isMesh) for (const m of (Array.isArray(o.material) ? o.material : [o.material])) materials.set(m.name, m); });
  const plans = [], loaded = [];
  try {
    for (const spec of manifest.repairs) {
      const repair = await new GLTFLoader().loadAsync(new URL(spec.glb, manifest.url).href);
      loaded.push(repair.scene); repair.scene.updateMatrixWorld(true);
      for (const name of spec.objects) {
        const normalized = THREE.PropertyBinding.sanitizeNodeName(name);
        const original = model.getObjectByName(name) || model.getObjectByName(normalized);
        const replacement = repair.scene.getObjectByName(name) || repair.scene.getObjectByName(normalized);
        if (!original || !replacement) throw new Error(`Repair node missing: ${name}`);
        if (plans.some(p => p.original === original)) throw new Error(`Repair node duplicated: ${name}`);
        replacement.traverse(mesh => {
          if (!mesh.isMesh) return;
          const source = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
          const next = source.map(material => {
            const base = materials.get(material.name);
            if (!base) throw new Error(`Repair material missing: ${material.name}`);
            return base;
          });
          source.forEach(m => m.dispose());
          mesh.material = Array.isArray(mesh.material) ? next : next[0];
        });
        plans.push({ name, original, replacement });
      }
    }
    model.updateMatrixWorld(true);
    for (const { name, original, replacement } of plans) {
      replacement.name = original.name;
      original.parent.attach(replacement); original.removeFromParent();
      status.objects.push(name);
    }
    status.state = 'applied';
    return status;
  } catch (error) {
    // No partial application: validation of every replacement precedes scene mutation.
    loaded.forEach(root => root.traverse(o => o.geometry?.dispose()));
    throw error;
  }
}
