import assert from 'node:assert/strict';
import { RoomLightmaps } from '../room-lightmaps.js';
const MiB = 1024 * 1024;
function record(id, size, last, shared = false) {
  const state = { geometry: 0, texture: 0, material: 0 };
  return { id, state: 'loaded', last, spec: { alwaysLoad: shared, lightMap: { size } },
    texture: { image: { width: size, height: size }, dispose() { state.texture++; } },
    groups: [{ removeFromParent() {}, traverse(fn) { fn({ geometry: { dispose() { state.geometry++; } } }); } }],
    ownedMaterials: new Set([{ dispose() { state.material++; } }]), fallback: [{ visible: false }], disposed: state };
}
const manager = Object.create(RoomLightmaps.prototype);
manager.maxResident = 6; manager.maxResidentBytes = 192 * MiB; manager.active = 'new';
manager.rooms = new Map([record('shared',4096,0,true),record('old',4096,1),record('mid',2048,2),record('new',4096,3)].map(r => [r.id,r]));
manager.status = { rooms: {} }; manager.trim();
assert.equal(manager.rooms.get('shared').state,'loaded');
assert.equal(manager.rooms.get('old').state,'available');
assert.equal(manager.rooms.get('old').fallback[0].visible,true);
assert.deepEqual(manager.rooms.get('old').disposed,{geometry:1,texture:1,material:1});
assert.equal(manager.rooms.get('mid').state,'loaded');
assert.equal(manager.rooms.get('new').state,'loaded');
assert.equal(manager.status.residentRegularBytes,160*MiB);
assert.equal(manager.status.residentSharedBytes,128*MiB);
manager.setBudget(64*MiB);
assert.equal(manager.rooms.get('mid').state,'available');
assert.equal(manager.rooms.get('new').state,'loaded');
assert.equal(manager.status.activeExceedsBudget,true);
assert.equal(manager.status.residentRegularBytes,128*MiB);
manager.trim();
assert.deepEqual(manager.rooms.get('old').disposed,{geometry:1,texture:1,material:1});
console.log(JSON.stringify({status:'passed',checks:13,scope:'Byte-bound LRU retention, active/shared protection, restoration and one-time resource disposal; no GPU allocation claim'}));
