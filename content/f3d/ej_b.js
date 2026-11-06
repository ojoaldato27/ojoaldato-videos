// EJEMPLO B · «Rayos X»: la cámara entra en la yema; piel translúcida, hueso, vasos con glóbulos que fluyen, nervio que se enciende y los vasos se encogen.
import { THREE, setup, ease, clamp, lerp, v3, pop, floaters } from './lib3d.js';
const { scene, cam, render } = setup({ bg: 0x0a1020, exposure: 1.0, envI: 0.35, bloom: [0.45, 0.5, 0.75] });
scene.add(new THREE.HemisphereLight(0x6fa8ff, 0x100818, 0.5));
const key = new THREE.DirectionalLight(0xbfe0ff, 2.0); key.position.set(3, 5, 4); scene.add(key);
const back = new THREE.PointLight(0xff5577, 6, 10); back.position.set(-2, 1, -3); scene.add(back);
// piel translúcida (yema de lado)
const L = 3.4, R = 0.95;
const skinG = new THREE.CapsuleGeometry(R, L, 24, 96); skinG.rotateZ(Math.PI / 2);
const skinBase = skinG.attributes.position.array.slice();
const skin = new THREE.Mesh(skinG, new THREE.MeshPhysicalMaterial({ color: 0xffb08f, roughness: 0.35, transparent: true, opacity: 0.22, depthWrite: false, clearcoat: 1, side: THREE.DoubleSide }));
scene.add(skin);
const edge = new THREE.Mesh(skinG, new THREE.MeshBasicMaterial({ color: 0xffc4a8, wireframe: true, transparent: true, opacity: 0.05 })); scene.add(edge);
const bone = new THREE.Mesh(new THREE.CapsuleGeometry(0.28, 2.4, 12, 32), new THREE.MeshPhysicalMaterial({ color: 0xf3ead8, roughness: 0.6 }));
bone.rotation.z = Math.PI / 2; bone.position.x = -0.6; scene.add(bone);
// vasos sanguíneos
const vessels = [];
const vm = new THREE.MeshPhysicalMaterial({ color: 0xc81d3a, roughness: 0.3, transparent: true, opacity: 0.85, emissive: 0x5a0010 });
[[0.55, 0.25], [-0.5, -0.2], [0.1, 0.62]].forEach(([y, z], i) => {
  const c = new THREE.CatmullRomCurve3([v3(-2.4, y, z), v3(-1, y + 0.08, z), v3(0.5, y - 0.06, z), v3(2.0, y * 0.5, z * 0.6), v3(2.5, 0, 0)]);
  const m = new THREE.Mesh(new THREE.TubeGeometry(c, 80, 0.13, 16), vm); scene.add(m);
  vessels.push({ c, m });
});
// glóbulos rojos
const NC = 90; const cellG = new THREE.TorusGeometry(0.045, 0.028, 8, 16);
const cells = new THREE.InstancedMesh(cellG, new THREE.MeshPhysicalMaterial({ color: 0xff3b4f, roughness: 0.3, emissive: 0x700010 }), NC); scene.add(cells);
// nervio
const nc = new THREE.CatmullRomCurve3([v3(-2.6, -0.05, -0.3), v3(-1, 0.1, -0.35), v3(0.6, -0.1, -0.3), v3(2.2, 0.1, -0.2)]);
const nm = new THREE.MeshBasicMaterial({ color: 0x806a10 });
scene.add(new THREE.Mesh(new THREE.TubeGeometry(nc, 80, 0.05, 10), nm));
const pulses = Array.from({ length: 4 }, () => { const s = new THREE.Mesh(new THREE.SphereGeometry(0.09, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfff27a })); scene.add(s); return s; });
const pl = new THREE.PointLight(0xffe066, 0, 4); scene.add(pl);
const motes = floaters(scene, 150, [-5, 5, -4, 4, -5, -1], 0x88aaff, 0.06, 0.6);

window.renderAt = function (t) {
  // cámara: entra desde fuera y gira alrededor
  const k = ease(clamp(t / 2.2));
  const ang = lerp(0.9, -0.35, ease(clamp(t / 6)));
  const dist = lerp(9, 5.6, k);
  cam.position.set(Math.sin(ang) * dist, lerp(2.5, 0.9, k), Math.cos(ang) * dist);
  cam.lookAt(0.2, 0, 0);
  // pulso del nervio a partir de 1,8 s → vasos se encogen y la piel se pliega
  const on = t > 1.8;
  pulses.forEach((p, i) => { const u = ((t - 1.8) * 0.7 + i / 4) % 1; p.visible = on; p.position.copy(nc.getPointAt(Math.max(0, u))); });
  pl.position.copy(pulses[0].position); pl.intensity = on ? 4 : 0;
  nm.color.setHex(on ? 0xffd23c : 0x806a10);
  const sh = ease(clamp((t - 2.6) / 1.4));
  vessels.forEach(({ m }) => { m.scale.set(1, 1 - 0.45 * sh, 1 - 0.45 * sh); });
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion();
  for (let i = 0; i < NC; i++) {
    const v = vessels[i % 3]; const u = ((t * (0.18 - 0.08 * sh) + i / NC * 3) % 1);
    const p = v.c.getPointAt(u); p.y *= (1 - 0.45 * sh); p.z *= (1 - 0.45 * sh);
    q.setFromEuler(new THREE.Euler(i, t * 2 + i, 0)); m4.compose(p, q, new THREE.Vector3(1, 1, 1)); cells.setMatrixAt(i, m4);
  }
  cells.instanceMatrix.needsUpdate = true;
  // la piel de arriba se arruga
  const a = skinG.attributes.position.array;
  for (let i = 0; i < a.length; i += 3) { const x = skinBase[i], y = skinBase[i + 1], z = skinBase[i + 2];
    const s = 1 + sh * (0.05 * Math.sin(x * 9 + Math.sin(Math.atan2(z, y) * 3) * 1.5) - 0.04);
    a[i] = x; a[i + 1] = y * s; a[i + 2] = z * s; }
  skinG.attributes.position.needsUpdate = true; skinG.computeVertexNormals();
  motes.userData.update(t, 0.1);
  return render(cam.position.length());
};
window.READY = true;
