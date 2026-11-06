// Muestrario de texturas: renderAt(i) dibuja la misma escena (mano arrugada + cerebro + patito) con el material nº i.
import { THREE, setup, v3, canvasTex, makeHand, wrinkle, makeBrain } from './lib3d.js';
const { scene, cam, render, gl } = setup({ bg: 0x2b2f3a, exposure: 1.0, envI: 1.0, bloom: [0.2, 0.4, 0.9], dof: false });
scene.add(new THREE.HemisphereLight(0xffffff, 0x445566, 0.5));
const key = new THREE.DirectionalLight(0xfff2e0, 2.6); key.position.set(-3, 6, 5); key.castShadow = true; key.shadow.mapSize.set(1024, 1024); scene.add(key);
const rim = new THREE.DirectionalLight(0x9fd0ff, 2.0); rim.position.set(4, 3, -4); scene.add(rim);
const floor = new THREE.Mesh(new THREE.CircleGeometry(6, 64), new THREE.MeshStandardMaterial({ color: 0x3a3f4c, roughness: 0.6 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -0.4; floor.receiveShadow = true; scene.add(floor);

const noise = (w, h, f) => canvasTex(w, h, (x) => { const id = x.createImageData(w, h);
  for (let j = 0; j < h; j++) for (let i = 0; i < w; i++) { const c = f(i, j); const k = (j * w + i) * 4; id.data[k] = c[0]; id.data[k + 1] = c[1]; id.data[k + 2] = c[2]; id.data[k + 3] = 255; }
  x.putImageData(id, 0, 0); });
const rnd = (i, j) => { const s = Math.sin(i * 127.1 + j * 311.7) * 43758.5453; return s - Math.floor(s); };
const skinCol = noise(256, 256, (i, j) => { const r = rnd(i, j), b = 0.5 + 0.5 * Math.sin(i * 0.05) * Math.sin(j * 0.07);
  return [222 + 20 * b - 15 * r, 158 + 10 * b - 12 * r, 130 + 8 * b - 10 * r]; });
const pores = noise(256, 256, (i, j) => { const v = 150 - (rnd(i, j) > 0.93 ? 90 : 0) + 25 * Math.sin(i * 0.9 + Math.sin(j * 0.3) * 4); return [v, v, v]; });
const wood = noise(256, 256, (i, j) => { const g = Math.sin((i + 30 * Math.sin(j * 0.03)) * 0.25) * 0.5 + 0.5; return [150 + 60 * g, 95 + 40 * g, 50 + 20 * g]; });
const marble = noise(256, 256, (i, j) => { const v = Math.abs(Math.sin((i + j) * 0.04 + 3 * Math.sin(i * 0.05) + 2 * Math.sin(j * 0.07))); const c = 235 - 120 * Math.pow(1 - v, 8); return [c, c, c + 4]; });
const stone = noise(256, 256, (i, j) => { const v = 110 + 70 * rnd(i >> 2, j >> 2) * 0.6 + 40 * rnd(i, j) * 0.4; return [v, v * 0.97, v * 0.92]; });
const knit = noise(256, 256, (i, j) => { const v = 130 + 90 * Math.abs(Math.sin(i * 0.4 + Math.abs(Math.sin(j * 0.2)) * 2)) * Math.abs(Math.cos(j * 0.4)); return [v, v, v]; });
[wood, marble, stone].forEach(t => t.repeat.set(2, 2)); knit.repeat.set(6, 6); pores.repeat.set(4, 4); skinCol.repeat.set(2, 2);

const P = (o) => new THREE.MeshPhysicalMaterial(o);
const MATS = [
  ['Realista (piel)', c => c === 'hand' ? P({ map: skinCol, color: 0xffffff, roughness: 0.55, bumpMap: pores, bumpScale: 0.6, sheen: 0.6, sheenColor: new THREE.Color(0xff9a8a), clearcoat: 0.15 }) : null],
  ['Vinilo de juguete', c => P({ color: c, roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.1 })],
  ['Porcelana', c => P({ color: c, roughness: 0.08, clearcoat: 1, clearcoatRoughness: 0.02, sheen: 0.2 })],
  ['Gominola', c => P({ color: c, roughness: 0.15, transmission: 0.75, thickness: 0.8, ior: 1.4, clearcoat: 1 })],
  ['Cristal', c => P({ color: 0xeaf6ff, roughness: 0.02, transmission: 1, thickness: 0.6, ior: 1.5, attenuationColor: new THREE.Color(c), attenuationDistance: 1.2 })],
  ['Hielo', c => P({ color: 0xdff4ff, roughness: 0.25, transmission: 0.9, thickness: 1, ior: 1.31, bumpMap: stone, bumpScale: 0.6 })],
  ['Cromo', c => P({ color: 0xffffff, metalness: 1, roughness: 0.08 })],
  ['Oro', c => P({ color: 0xffc95a, metalness: 1, roughness: 0.22 })],
  ['Holográfico', c => P({ color: 0xffffff, metalness: 0.6, roughness: 0.15, iridescence: 1, iridescenceIOR: 1.8, iridescenceThicknessRange: [200, 900] })],
  ['Madera tallada', c => P({ map: wood, roughness: 0.6, bumpMap: wood, bumpScale: 1.5 })],
  ['Mármol', c => P({ map: marble, roughness: 0.15, clearcoat: 0.8 })],
  ['Piedra', c => P({ map: stone, roughness: 0.95, bumpMap: stone, bumpScale: 3 })],
  ['Terciopelo', c => P({ color: c, roughness: 1, sheen: 1, sheenRoughness: 0.35, sheenColor: new THREE.Color(0xffffff).lerp(new THREE.Color(c), 0.3) })],
  ['Punto de lana', c => P({ color: c, roughness: 1, bumpMap: knit, bumpScale: 4, sheen: 0.8, sheenRoughness: 0.6 })],
  ['Plástico mate (bloque)', c => P({ color: c, roughness: 0.45, clearcoat: 0.3 })],
  ['Cerámica esmaltada', c => P({ color: c, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.25, bumpMap: stone, bumpScale: 0.25 })],
];
const COL = { hand: 0xf0a882, brain: 0xff8fb0, duck: 0xffcc22 };
const hand = makeHand(); hand.position.set(0.05, -0.4, 0); hand.rotation.y = -0.35; scene.add(hand);
hand.userData.fingers.forEach((f, i) => wrinkle(f, i === 4 ? 0.6 : 0.9));
const brain = makeBrain(); brain.position.set(1.05, 2.75, 0.2); brain.scale.setScalar(0.62); brain.rotation.y = 0.5; scene.add(brain);
const duck = new THREE.Group(); scene.add(duck); duck.position.set(1.15, -0.05, 0.9); duck.rotation.y = -0.9; duck.scale.setScalar(0.75);
const db = new THREE.Mesh(new THREE.SphereGeometry(0.42, 48, 32)); db.scale.set(1.3, 0.8, 1); duck.add(db);
const dh = new THREE.Mesh(new THREE.SphereGeometry(0.27, 48, 32)); dh.position.set(0.35, 0.42, 0); duck.add(dh);
const beak = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.25, 24), new THREE.MeshStandardMaterial({ color: 0xff7a1a })); beak.rotation.z = -Math.PI / 2; beak.position.set(0.66, 0.4, 0); duck.add(beak);
scene.traverse(o => { if (o.isMesh) o.castShadow = true; });
cam.position.set(1.0, 1.8, 6.2); cam.lookAt(0.55, 1.25, 0);
window.renderAt = function (t) {
  const i = Math.floor(t) % MATS.length; const [, f] = MATS[i];
  const hm = i === 0 ? f('hand') : f(COL.hand);
  hand.traverse(o => { if (o.isMesh && !o.userData.nail) o.material = hm; });
  brain.material = (i === 0 ? P({ color: COL.brain, roughness: 0.35, clearcoat: 0.7 }) : f(COL.brain));
  [db, dh].forEach(m => m.material = (i === 0 ? P({ color: COL.duck, roughness: 0.3, clearcoat: 1 }) : f(COL.duck)));
  
  return render();
};
window.MAT_NAMES = MATS.map(m => m[0]);
window.READY = true;
