// EJEMPLO H · «Papel recortado»: capas de papel con grosor y sombras, olas de papel que se mueven, mano de papel que sale y se arruga.
import { THREE, setup, ease, clamp, lerp, v3, pop, canvasTex } from './lib3d.js';
const { scene, cam, render } = setup({ bg: 0xf3e6cf, exposure: 1.0, envI: 0.3, bloom: [0.05, 0.3, 0.95] });
scene.add(new THREE.HemisphereLight(0xffffff, 0x998877, 0.9));
const key = new THREE.DirectionalLight(0xfff4e0, 2.6); key.position.set(-4, 6, 8); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -8, right: 8, top: 10, bottom: -8 }); key.shadow.bias = -0.0005; key.shadow.radius = 6; scene.add(key);
const fiber = canvasTex(256, 256, (x) => { x.fillStyle = '#fff'; x.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 1400; i++) { x.strokeStyle = `rgba(120,100,80,${Math.random() * 0.12})`; x.beginPath(); const a = Math.random() * 256, b = Math.random() * 256; x.moveTo(a, b); x.lineTo(a + Math.random() * 14 - 7, b + Math.random() * 14 - 7); x.stroke(); } }, [2, 2]);
const P = (c) => new THREE.MeshStandardMaterial({ color: c, map: fiber, roughness: 1 });
const ext = (shape, d = 0.06) => { const g = new THREE.ExtrudeGeometry(shape, { depth: d, bevelEnabled: true, bevelThickness: 0.008, bevelSize: 0.008, bevelSegments: 1, curveSegments: 24 }); return g; };
const add = (g, c, z, cast = true) => { const m = new THREE.Mesh(g, P(c)); m.position.z = z; m.castShadow = cast; m.receiveShadow = true; scene.add(m); return m; };
// fondo: pared con azulejos de papel y ventana
add(new THREE.BoxGeometry(14, 24, 0.05), 0xbcdde3, -1.2, false);
for (let i = 0; i < 6; i++) for (let j = 0; j < 9; j++) { const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(1.6, 0); s.lineTo(1.6, 1.6); s.lineTo(0, 1.6); s.lineTo(0, 0);
  const m = add(ext(s, 0.02), (i + j) % 2 ? 0xd6ecef : 0xc8e4e8, -1.15, true); m.position.x = -5 + i * 1.75; m.position.y = -3 + j * 1.75; }
const ws = new THREE.Shape(); ws.absarc(0, 0, 1.4, 0, Math.PI * 2); const win = add(ext(ws, 0.04), 0xfff0b8, -1.0); win.position.set(2.7, 7.2, -1.0);
// olas de papel (4 capas)
const waves = [];
const waveCols = [0x1f6fa8, 0x2b86c0, 0x3fa0d6, 0x63bce6];
for (let k = 0; k < 4; k++) {
  const s = new THREE.Shape(); const Wd = 16;
  s.moveTo(-Wd / 2, -6); for (let i = 0; i <= 64; i++) { const x = -Wd / 2 + Wd * i / 64; s.lineTo(x, 0.22 * Math.sin(x * 2.2 + k * 1.3)); } s.lineTo(Wd / 2, -6); s.lineTo(-Wd / 2, -6);
  const m = add(ext(s, 0.05), waveCols[k], -0.2 + k * 0.35); waves.push(m);
}
// bañera de papel (borde delante)
const ts = new THREE.Shape(); ts.moveTo(-7, -6); ts.lineTo(-7, -0.6); ts.quadraticCurveTo(-7, 0.2, -6.2, 0.2); ts.lineTo(6.2, 0.2); ts.quadraticCurveTo(7, 0.2, 7, -0.6); ts.lineTo(7, -6);
const tub = add(ext(ts, 0.08), 0xfffbf4, 1.3); tub.position.y = -0.9;
// mano de papel (silueta)
const hs = new THREE.Shape();
hs.moveTo(-0.75, -4); hs.lineTo(-0.75, 0.6); hs.quadraticCurveTo(-0.95, 1.1, -1.35, 1.6); hs.quadraticCurveTo(-1.55, 1.95, -1.2, 2.05); hs.quadraticCurveTo(-0.9, 1.9, -0.7, 1.55);
const fx = [[-0.62, 3.3], [-0.2, 3.65], [0.22, 3.5], [0.62, 3.0]];
hs.lineTo(-0.8, 1.6);
fx.forEach(([x, top], i) => { const w = 0.19; hs.lineTo(x - w, 1.7); hs.lineTo(x - w, top - w); hs.absarc(x, top - w, w, Math.PI, 0, true); hs.lineTo(x + w, 1.7); });
hs.lineTo(0.85, 1.4); hs.lineTo(0.75, -4); hs.lineTo(-0.75, -4);
const hand = add(ext(hs, 0.07), 0xf1b08e, 0.6);
const nails = fx.map(([x, top]) => { const s = new THREE.Shape(); s.absellipse(0, 0, 0.11, 0.15, 0, Math.PI * 2); const m = new THREE.Mesh(ext(s, 0.02), P(0xffd8cc)); m.position.set(x, top - 0.22, 0.09); m.castShadow = true; hand.add(m); return m; });
// arrugas: tiras de papel oscuro en las yemas que aparecen
const wrinkles = [];
fx.forEach(([x, top]) => { for (let j = 0; j < 4; j++) { const s = new THREE.Shape(); const y0 = top - 0.5 - j * 0.12;
  s.moveTo(x - 0.15, y0); for (let q = 0; q <= 8; q++) s.lineTo(x - 0.15 + 0.3 * q / 8, y0 + 0.025 * Math.sin(q * 1.9 + j)); for (let q = 8; q >= 0; q--) s.lineTo(x - 0.15 + 0.3 * q / 8, y0 - 0.025 + 0.025 * Math.sin(q * 1.9 + j)); 
  const m = new THREE.Mesh(ext(s, 0.015), P(0xb86a52)); m.position.z = 0.085; hand.add(m); wrinkles.push(m); } });
// cerebro de papel + señal de puntos
const bs = new THREE.Shape(); for (let i = 0; i <= 40; i++) { const a = i / 40 * Math.PI * 2; const r = 1 + 0.08 * Math.sin(a * 9); i ? bs.lineTo(1.25 * r * Math.cos(a), 0.9 * r * Math.sin(a)) : bs.moveTo(1.25 * r, 0); }
const brain = add(ext(bs, 0.08), 0xf59ab2, 0.9);
const folds = []; for (let j = 0; j < 5; j++) { const s = new THREE.Shape(); s.absarc(0, 0, 0.3, 0.2, Math.PI - 0.2, false); s.absarc(0, 0, 0.24, Math.PI - 0.2, 0.2, true);
  const m = new THREE.Mesh(ext(s, 0.02), P(0xd96f8c)); m.position.set(-0.7 + j * 0.35, (j % 2 ? -0.25 : 0.25), 0.1); brain.add(m); }
const dots = Array.from({ length: 7 }, () => { const s = new THREE.Shape(); s.absarc(0, 0, 0.1, 0, Math.PI * 2); const m = add(ext(s, 0.04), 0xffd23c, 1.0); return m; });
window.renderAt = function (t) {
  waves.forEach((w, k) => { w.position.x = 0.6 * Math.sin(t * (0.9 + k * 0.2) + k); w.position.y = -0.3 - k * 0.25 + 0.06 * Math.sin(t * 2 + k); });
  const rise = ease(clamp((t - 0.15) / 0.9));
  hand.position.set(-0.3, lerp(-4.2, -0.6, rise), 0.6); hand.rotation.z = 0.05 * Math.sin(t * 1.3);
  const wr = ease(clamp((t - 2.6) / 1.4));
  wrinkles.forEach((m, i) => { const k = clamp(wr * 1.4 - (i % 4) * 0.12); m.scale.set(k, k, 1); m.visible = k > 0.02; });
  const bk = pop(clamp((t - 1.9) / 0.5));
  brain.visible = bk > 0.01; brain.scale.setScalar(Math.max(0.01, bk)); brain.position.set(2.1, 4.6 + 0.08 * Math.sin(t * 2), 0.9); brain.rotation.z = 0.08 * Math.sin(t * 1.5);
  const tip = v3(hand.position.x - 0.2, hand.position.y + 3.5, 1.0);
  dots.forEach((d, i) => { const u = ((t - 2.2) * 0.8 + i / 7) % 1; d.visible = t > 2.2 && t < 4.8;
    const p = brain.position.clone().lerp(tip, Math.max(0, u)); p.y += 0.6 * Math.sin(Math.PI * Math.max(0, u)); d.position.set(p.x, p.y, 1.0); });
  const k = ease(clamp(t / 5.6));
  cam.position.set(lerp(0.9, -0.4, k), lerp(0.8, 2.4, k), lerp(11.5, 8.0, k)); cam.lookAt(lerp(0.2, 0.3, k), lerp(1.0, 2.2, k), 0);
  return render(cam.position.z - 0.6);
};
window.READY = true;
