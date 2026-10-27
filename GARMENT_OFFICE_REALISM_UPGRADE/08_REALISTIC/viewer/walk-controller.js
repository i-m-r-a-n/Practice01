// Phase 5 controller. The supplied static grid already includes its 0.15m player radius.
// No noclip recovery: callers must start at a verified walkable position.
export function createWalking({ position, blocked, eye = 1.6, updateActors = () => {} }) {
  let vx = 0, vz = 0, steps = 0, collisions = 0, distance = 0;
  return {
    reset() { vx = vz = 0; position.y = eye; },
    state() { return { position: position.toArray(), velocity: [vx, vz], steps, collisions, distance, eye }; },
    step({ forward = 0, strafe = 0, yaw = 0, dt = 0, fast = false } = {}) {
      dt = Math.max(0, Math.min(0.25, dt));
      const n = Math.max(1, Math.hypot(forward, strafe));
      forward /= n; strafe /= n;
      const speed = fast ? 2.8 : 1.4;
      const targetX = (-Math.sin(yaw) * forward + Math.cos(yaw) * strafe) * speed;
      const targetZ = (-Math.cos(yaw) * forward - Math.sin(yaw) * strafe) * speed;
      const count = Math.max(1, Math.ceil(dt / (1 / 90))), h = dt / count;
      for (let i = 0; i < count; i++) {
        updateActors(h, position);
        steps++;
        if (blocked(position.x, position.z)) { vx = vz = 0; collisions++; break; }
        const damping = 1 - Math.exp(-12 * h);
        vx += (targetX - vx) * damping; vz += (targetZ - vz) * damping;
        if (Math.abs(vx) < 0.0001) vx = 0;
        if (Math.abs(vz) < 0.0001) vz = 0;
        const oldX = position.x, oldZ = position.z;
        const dx = vx * h, dz = vz * h;
        if (!blocked(position.x + dx, position.z + dz)) { position.x += dx; position.z += dz; }
        else {
          collisions++;
          if (!blocked(position.x + dx, position.z)) position.x += dx; else vx = 0;
          if (!blocked(position.x, position.z + dz)) position.z += dz; else vz = 0;
        }
        distance += Math.hypot(position.x - oldX, position.z - oldZ);
      }
      position.y = eye;
      return this.state();
    },
  };
}
