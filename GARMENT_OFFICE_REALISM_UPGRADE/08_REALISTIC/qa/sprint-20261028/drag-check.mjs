import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

// Execute the current viewer's actual handlers in a minimal DOM/render boundary.
// No copy of the sign expressions is used as the implementation under test.
const here = dirname(fileURLToPath(import.meta.url));
const repo = resolve(here, '../../../..');
const relative = 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/viewer/app.js';
const source = readFileSync(resolve(repo, relative), 'utf8');
const baseCommit = '20a3de996191ee2ecbe57928780b49209a289832';
const original = execFileSync('git', ['show', `${baseCommit}:${relative}`], { cwd: repo, encoding: 'utf8' });
const between = (text, start, end) => {
  const a = text.indexOf(start), b = text.indexOf(end, a);
  assert(a >= 0 && b > a, `Cannot locate ${start}`);
  return text.slice(a, b);
};
const move = text => between(text, "el.addEventListener('pointermove',", '\n\n// a trackpad pinch');
const step = text => between(text, 'function walkStep(dt) {', "\nel.addEventListener('dblclick'");
const keys = text => between(text, "const MOVE_KEYS = new Set", "addEventListener('keyup'");
const lock = text => between(move(text), '  if (USE_WALKING', "  if ((S.mode === 'walk'");
const checks = [];
const check = (name, fn) => { fn(); checks.push({ name, passed: true }); };
const near = (actual, expected) => assert(Math.abs(actual - expected) < 1e-10, `${actual} != ${expected}`);
function runtime(mode = 'walk', useWalking = false, pointerLocked = false) {
  const callbacks = {};
  const el = { addEventListener: (name, cb) => { callbacks[name] = cb; }, style: {} };
  const ctx = {
    USE_WALKING: useWalking, document: { pointerLockElement: pointerLocked ? el : null }, el,
    S: { mode, atCam: 'CAM_01' },
    walk: { yaw: 0, pitch: 0, drag: { x: 100, y: 100 }, keys: {}, glide: null, eye: 1.6 },
    THREE: { MathUtils: { clamp: (x, lo, hi) => Math.max(lo, Math.min(hi, x)) } },
    applyWalkLook() { ctx.lookCalls++; }, updateInfoButtons() { ctx.infoCalls++; },
    lookCalls: 0, infoCalls: 0, flight: null, needsRender: false,
    camera: { position: { x: 0, y: 1.6, z: 0, set(x, y, z) { Object.assign(this, { x, y, z }); } } },
    walking: { step(input) { ctx.stepInput = input; } }, afterWalking() {},
    blocked: () => false, roomAt: () => null, walkCard() {},
  };
  vm.createContext(ctx);
  vm.runInContext(move(source) + '\n' + step(source), ctx);
  return { ctx, move: callbacks.pointermove };
}
for (const mode of ['walk', 'rooms']) {
  for (const [name, dx, dy] of [['right', 40, 0], ['left', -40, 0], ['down', 0, 30], ['up', 0, -30]]) {
    check(`${mode}: ${name} direct drag follows the requested positive client delta`, () => {
      const r = runtime(mode);
      r.move({ clientX: 100 + dx, clientY: 100 + dy });
      near(r.ctx.walk.yaw, dx * 0.0035); near(r.ctx.walk.pitch, dy * 0.0035);
      assert.equal(r.ctx.walk.drag.x, 100 + dx); assert.equal(r.ctx.walk.drag.y, 100 + dy);
      assert.equal(r.ctx.lookCalls, 1); assert.equal(r.ctx.infoCalls, 1); assert.equal(r.ctx.S.atCam, null);
    });
  }
}
check('Pitch retains both safety clamps', () => {
  const r = runtime();
  r.move({ clientX: 100, clientY: 1100 }); near(r.ctx.walk.pitch, 1.2);
  r.move({ clientX: 100, clientY: -1100 }); near(r.ctx.walk.pitch, -1.2);
});
check('Pointer movement without an active drag does not turn the room', () => {
  const r = runtime(); r.ctx.walk.drag = null;
  r.move({ clientX: 140, clientY: 130 }); near(r.ctx.walk.yaw, 0); near(r.ctx.walk.pitch, 0);
});
check('Existing pointer-lock FPS look remains byte-identical and behaves unchanged', () => {
  assert.equal(lock(source), lock(original));
  const r = runtime('walk', true, true);
  r.move({ movementX: 40, movementY: 30, clientX: 140, clientY: 130 });
  near(r.ctx.walk.yaw, -40 * 0.0022); near(r.ctx.walk.pitch, -30 * 0.0022);
  assert.equal(r.ctx.walk.drag.x, 100); assert.equal(r.ctx.infoCalls, 0);
});
check('Keyboard handler and complete walking step remain byte-identical to baseline', () => {
  assert.equal(keys(source), keys(original)); assert.equal(step(source), step(original));
});
for (const [key, expected] of [['ArrowRight', -0.16], ['ArrowLeft', 0.16]]) {
  check(`Legacy keyboard ${key} turning remains unchanged`, () => {
    const r = runtime(); r.ctx.walk.keys[key] = true; r.ctx.walkStep(0.1); near(r.ctx.walk.yaw, expected);
  });
}
check('Collision-controller keyboard arrows still strafe without changing yaw', () => {
  const r = runtime('walk', true); r.ctx.walk.keys.ArrowRight = true; r.ctx.walk.yaw = 0.4;
  r.ctx.walkStep(0.1); assert.equal(r.ctx.stepInput.strafe, 1); near(r.ctx.stepInput.yaw, 0.4); near(r.ctx.walk.yaw, 0.4);
});
const report = {
  baseline: baseCommit, source: relative, status: 'passed', checks,
  scope: 'Actual source pointermove and walkStep handlers executed in Node VM with DOM/render boundaries stubbed.',
  limits: ['Not a native MacBook or browser pointer-lock interaction test.', 'No scene pixels or visual judgement is inferred from this handler test.'],
};
writeFileSync(resolve(here, 'drag-check.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ status: report.status, passed: checks.length }));
