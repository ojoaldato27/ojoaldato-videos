import * as THREE from 'three';
import { makeCarPro } from './car_pro.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
// Ojo al dato · vídeo 3D «El rebufo en F1» (estilo C: minimal blanco con Ojo en 3D).
// Render determinista: window.renderAt(t) dibuja el fotograma del segundo t y devuelve un JPEG en dataURL.
// window.TIMING (lo pone render3d.py): {total, lines:[{start,end,tokens:[{w,key,s,e}]}], outro:{...}}

const W = 720, H = 1280;
const RED = 0xE62828, INK = 0x111111, GREY = 0x9a9a9a;
const CSS_RED = '#E62828';

// ---------- renderer y capa 2D ----------
const gl = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
const PR = 1.5;   // Iker (28/10): «no se ve con mucha calidad» → se dibuja a 1080x1920 de verdad
gl.setPixelRatio(PR); gl.setSize(W, H);
const out = document.createElement('canvas'); out.width = W * PR; out.height = H * PR;
const ctx = out.getContext('2d');
document.body.appendChild(out);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
const cam = new THREE.PerspectiveCamera(38, W / H, 0.5, 250);
scene.add(cam);
scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d8d8, 1.6));
const sun = new THREE.DirectionalLight(0xffffff, 1.4); sun.position.set(6, 14, 8); scene.add(sun);

const grad = new THREE.DataTexture(new Uint8Array([150, 150, 150, 255, 215, 215, 215, 255, 255, 255, 255, 255]), 3, 1);
grad.minFilter = grad.magFilter = THREE.NearestFilter; grad.needsUpdate = true;
const toon = (c, extra = {}) => new THREE.MeshToonMaterial({ color: c, gradientMap: grad, ...extra });
const BLACK = new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide });

// silueta negra (casco invertido) + aristas finas
function ink(mesh, k = 1.06, edges = true) {
  const hull = new THREE.Mesh(mesh.geometry, BLACK);
  hull.scale.setScalar(k);
  mesh.add(hull);
  if (edges) mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry, 35), new THREE.LineBasicMaterial({ color: INK })));
  return mesh;
}
function box(w, h, d, c, k) { return ink(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(c)), k); }

// ---------- utilidades ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const eob = x => { x = clamp(x); const c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lerp = (a, b, u) => a + (b - a) * u;
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

// ---------- pista recta ----------
const world = new THREE.Group(); scene.add(world);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(1200, 1200), new THREE.MeshBasicMaterial({ color: 0xffffff }));
ground.rotation.x = -Math.PI / 2; ground.position.y = -0.05; world.add(ground);
const straight = new THREE.Group(); world.add(straight);
const road = new THREE.Mesh(new THREE.PlaneGeometry(1200, 11), new THREE.MeshBasicMaterial({ color: 0xf1f1f1 }));
road.rotation.x = -Math.PI / 2; straight.add(road);
for (const z of [-5.5, 5.5]) {
  const l = new THREE.Mesh(new THREE.PlaneGeometry(1200, 0.12), new THREE.MeshBasicMaterial({ color: INK }));
  l.rotation.x = -Math.PI / 2; l.position.set(0, 0.025, z); straight.add(l);
}
// pianos rojos y blancos y rayas discontinuas (se desplazan para dar velocidad)
const dashes = [], kerbs = [];
for (let i = 0; i < 70; i++) {
  const d = new THREE.Mesh(new THREE.PlaneGeometry(3, 0.14), new THREE.MeshBasicMaterial({ color: 0xc4c4c4 }));
  d.rotation.x = -Math.PI / 2; d.position.y = 0.02; straight.add(d); dashes.push(d);
}
for (let i = 0; i < 140; i++) {
  for (const z of [-6.1, 6.1]) {
    const k = new THREE.Mesh(new THREE.PlaneGeometry(2, 1.1), new THREE.MeshBasicMaterial({ color: i % 2 ? 0xffffff : RED }));
    k.rotation.x = -Math.PI / 2; k.position.set(0, 0.015, z); k.userData.i = i; straight.add(k); kerbs.push(k);
  }
}
function scrollTrack(s) {
  dashes.forEach((d, i) => { d.position.x = ((i * 8 - s) % 560 + 560) % 560 - 280; });
  kerbs.forEach(k => { k.position.x = ((k.userData.i * 4 - s) % 560 + 560) % 560 - 280; });
  for (const [tx, len] of (typeof SCROLLED !== 'undefined' ? SCROLLED : [])) tx.offset.x = (s / len) % 1;
}

// ---------- curva (escenas 7-8) ----------
const CURVE_R = 34;
const curve = new THREE.Group(); world.add(curve);
{
  const ring = new THREE.Mesh(new THREE.RingGeometry(CURVE_R - 5.5, CURVE_R + 5.5, 160, 1, 0, Math.PI), new THREE.MeshBasicMaterial({ color: 0xf1f1f1, side: THREE.DoubleSide }));
  ring.rotation.x = -Math.PI / 2; curve.add(ring);
  for (const r of [CURVE_R - 5.5, CURVE_R + 5.5]) {
    const e = new THREE.Mesh(new THREE.RingGeometry(r - 0.07, r + 0.07, 160, 1, 0, Math.PI), new THREE.MeshBasicMaterial({ color: INK, side: THREE.DoubleSide }));
    e.rotation.x = -Math.PI / 2; e.position.y = 0.025; curve.add(e);
  }
  for (let i = 0; i < 48; i++) {
    const a0 = i / 48 * Math.PI;
    const k = new THREE.Mesh(new THREE.RingGeometry(CURVE_R - 6.6, CURVE_R - 5.5, 6, 1, a0, Math.PI / 48), new THREE.MeshBasicMaterial({ color: i % 2 ? 0xffffff : RED, side: THREE.DoubleSide }));
    k.rotation.x = -Math.PI / 2; k.position.y = 0.015; curve.add(k);
  }
}
curve.position.set(0, 0, 0);


// ---------- entorno de circuito con texturas (Iker, 28/10: «mejora las texturas y adecua el fondo al tema») ----------
function canvasTex(w, h, draw, rx = 1, ry = 1) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry);
  t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
const R0 = rng(11);
const noise = (x, w, h, n, cols, size = 2) => { for (let i = 0; i < n; i++) { x.fillStyle = cols[(R0() * cols.length) | 0]; x.fillRect(R0() * w, R0() * h, size * (0.5 + R0()), size * (0.5 + R0())); } };
const TEX = {
  asphalt: canvasTex(256, 256, (x, w, h) => { x.fillStyle = '#4d5056'; x.fillRect(0, 0, w, h); noise(x, w, h, 5000, ['#43464b', '#5a5d63', '#3b3d42', '#63666c'], 2);
    x.globalAlpha = 0.08; for (let i = 0; i < 6; i++) { x.fillStyle = '#000'; x.fillRect(0, R0() * h, w, 6 + R0() * 10); } x.globalAlpha = 1; }, 150, 1.4),
  grass: canvasTex(256, 256, (x, w, h) => { for (let i = 0; i < 4; i++) { x.fillStyle = i % 2 ? '#5aa548' : '#66b453'; x.fillRect(0, i * h / 4, w, h / 4); }
    noise(x, w, h, 6000, ['#4f9640', '#6fbd5b', '#58a046', '#78c463'], 2); }, 75, 75),
  barrier: canvasTex(128, 64, (x, w, h) => { x.fillStyle = '#1e1f22'; x.fillRect(0, 0, w, h);
    for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) { const cx = 16 + c * 32, cy = 16 + r * 32;
      x.fillStyle = (r + c) % 2 ? '#e8e8e8' : '#d8262b'; x.beginPath(); x.arc(cx, cy, 15, 0, 7); x.fill();
      x.fillStyle = '#141416'; x.beginPath(); x.arc(cx, cy, 7, 0, 7); x.fill(); } }, 600, 1),
  boards: canvasTex(512, 64, (x, w, h) => { x.fillStyle = '#E62828'; x.fillRect(0, 0, w / 2, h); x.fillStyle = '#ffffff'; x.fillRect(w / 2, 0, w / 2, h);
    x.font = '900 30px Inter, Arial'; x.textBaseline = 'middle'; x.textAlign = 'center';
    x.fillStyle = '#fff'; x.fillText('OJO AL DATO', w / 4, h / 2 + 2); x.fillStyle = '#E62828'; x.fillText('¡OJO AL DATO!', 3 * w / 4, h / 2 + 2); }, 120, 1),
  crowd: canvasTex(256, 128, (x, w, h) => { x.fillStyle = '#6b6f78'; x.fillRect(0, 0, w, h);
    for (let r = 0; r < 12; r++) { x.fillStyle = '#585c64'; x.fillRect(0, r * 10.6 + 8, w, 2.5); }
    noise(x, w, h, 2600, ['#E62828', '#ffffff', '#ffd23f', '#2f6fd6', '#111111', '#f08a24', '#e8e8e8'], 3.2); }, 150, 1),
  trees: canvasTex(256, 128, (x, w, h) => { x.fillStyle = '#9fd0f5'; x.fillRect(0, 0, w, h);
    for (let i = 0; i < 40; i++) { const cx = R0() * w, r = 14 + R0() * 22; x.fillStyle = ['#3f7d3a', '#4a8c42', '#356c31'][i % 3];
      x.beginPath(); x.arc(cx, h - 20 - R0() * 20, r, 0, 7); x.fill(); } x.fillStyle = '#3f7d3a'; x.fillRect(0, h - 30, w, 30); }, 20, 1),
  sky: canvasTex(4, 256, (x, w, h) => { const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#5ea6ea'); g.addColorStop(0.6, '#a9d4f7'); g.addColorStop(1, '#e8f5ff'); x.fillStyle = g; x.fillRect(0, 0, w, h); }),
};
TEX.sky.wrapS = TEX.sky.wrapT = THREE.ClampToEdgeWrapping;
const CIRCUIT = window.ENV !== 'plain';
if (CIRCUIT) {
  road.material = new THREE.MeshLambertMaterial({ map: TEX.asphalt });
  ground.material = new THREE.MeshLambertMaterial({ map: TEX.grass, color: 0xffffff });
  straight.children.forEach(m => { if (m.material && m.material.color && m.material.color.getHex() === INK) m.material.color.setHex(0xf2f2f2); });
  dashes.forEach(d => d.material.color.setHex(0xf2f2f2));
  // run-off asfaltado claro tras el piano, barrera de neumáticos con vallas, grada con público y árboles al fondo
  const runoff = new THREE.MeshLambertMaterial({ map: TEX.asphalt.clone(), color: 0xc9ccd2 }); runoff.map.repeat.set(150, 0.6); runoff.map.needsUpdate = true;
  for (const z of [-9, 9]) { const r = new THREE.Mesh(new THREE.PlaneGeometry(1200, 4.6), runoff); r.rotation.x = -Math.PI / 2; r.position.set(0, -0.01, z); straight.add(r); }
  const bar = new THREE.MeshLambertMaterial({ map: TEX.barrier });
  const brd = new THREE.MeshLambertMaterial({ map: TEX.boards });
  for (const z of [-14, 14]) {
    const b = new THREE.Mesh(new THREE.BoxGeometry(1200, 0.95, 0.9), bar); b.position.set(0, 0.47, z); straight.add(b);
    const bd = new THREE.Mesh(new THREE.PlaneGeometry(1200, 1.0), brd); bd.position.set(0, 1.55, z - Math.sign(z) * 0.0); bd.rotation.y = z > 0 ? Math.PI : 0; straight.add(bd);
    const post = new THREE.Mesh(new THREE.BoxGeometry(1200, 0.06, 0.06), new THREE.MeshLambertMaterial({ color: 0x9a9da3 })); post.position.set(0, 3.2, z); straight.add(post);
  }
  const stand = new THREE.Mesh(new THREE.PlaneGeometry(1200, 11), new THREE.MeshLambertMaterial({ map: TEX.crowd }));
  stand.position.set(0, 5.2, -24); stand.rotation.x = -0.55; straight.add(stand);
  const roof = new THREE.Mesh(new THREE.BoxGeometry(1200, 0.35, 7), new THREE.MeshLambertMaterial({ color: 0xf2f2f2 })); roof.position.set(0, 11.2, -26); straight.add(roof);
  const standB = new THREE.Mesh(new THREE.PlaneGeometry(1200, 11), new THREE.MeshLambertMaterial({ map: TEX.crowd.clone() }));
  standB.material.map.needsUpdate = true; standB.position.set(0, 5.2, 24); standB.rotation.set(0.55, Math.PI, 0); straight.add(standB);
  const trees = new THREE.Mesh(new THREE.PlaneGeometry(1200, 22), new THREE.MeshBasicMaterial({ map: TEX.trees, transparent: false, fog: true }));
  trees.position.set(0, 9, -70); straight.add(trees);
  // curva: asfalto, run-off y barrera alrededor
  curve.children[0].material = new THREE.MeshLambertMaterial({ map: (() => { const t = TEX.asphalt.clone(); t.repeat.set(10, 10); t.needsUpdate = true; return t; })(), side: THREE.DoubleSide });
  curve.children.forEach((m, i) => { if (i > 0 && m.material.color && m.material.color.getHex() === INK) m.material.color.setHex(0xf2f2f2); });
  for (const r of [CURVE_R + 12, CURVE_R - 11]) {
    const tb = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.95, 160, 1, true, 0, Math.PI), new THREE.MeshLambertMaterial({ map: (() => { const t = TEX.barrier.clone(); t.repeat.set(r * 1.6, 1); t.needsUpdate = true; return t; })(), side: THREE.DoubleSide }));
    tb.position.y = 0.47; tb.rotation.y = -Math.PI / 2; curve.add(tb);
  }
  scene.fog = new THREE.Fog(0xe8f5ff, 70, 230);
}
const SCROLLED = CIRCUIT ? [[TEX.asphalt, 8], [TEX.barrier, 2], [TEX.boards, 10], [TEX.crowd, 8]] : [];

// ---------- coche de F1 (morro hacia +X, 5 m) ----------
function makeCar(col, stripe) {
  const g = new THREE.Group();
  const add = (m, x, y, z) => { m.position.set(x, y, z); g.add(m); return m; };
  add(box(2.6, 0.5, 0.95, col), -0.2, 0.42, 0);                 // monocasco
  const nose = ink(new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.34, 1.8, 10), toon(col)));
  nose.rotation.z = -Math.PI / 2; add(nose, 1.95, 0.36, 0);
  add(box(1.2, 0.36, 0.5, col), -0.3, 0.42, 0.66);              // pontones
  add(box(1.2, 0.36, 0.5, col), -0.3, 0.42, -0.66);
  add(box(0.9, 0.42, 0.55, col), -0.9, 0.85, 0);                 // tapa motor
  add(box(0.5, 0.05, 1.95, INK, 1.0), 2.75, 0.18, 0);           // alerón delantero
  add(box(0.42, 0.05, 1.55, col), -2.05, 1.1, 0);                // alerón trasero
  add(box(0.42, 0.5, 0.05, INK, 1.0), -2.05, 0.88, 0.78);
  add(box(0.42, 0.5, 0.05, INK, 1.0), -2.05, 0.88, -0.78);
  add(box(1.0, 0.06, 0.12, stripe, 1.0), 0.6, 0.68, 0);          // franja
  const helmet = ink(new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 12), toon(0xffffff)));
  add(helmet, 0.15, 0.82, 0);
  const halo = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.04, 6, 16, Math.PI), new THREE.MeshBasicMaterial({ color: INK }));
  halo.rotation.y = Math.PI / 2; add(halo, 0.25, 0.8, 0);
  g.userData.wheels = [];
  for (const [x, z] of [[1.55, 0.88], [1.55, -0.88], [-1.45, 0.9], [-1.45, -0.9]]) {
    const wmat = toon(0x222222);
    const w = ink(new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.36, x > 0 ? 0.32 : 0.4, 18), wmat), 1.05, false);
    w.rotation.x = Math.PI / 2; add(w, x, 0.36, z);
    const rim = new THREE.Mesh(new THREE.CircleGeometry(0.16, 12), new THREE.MeshBasicMaterial({ color: 0xbbbbbb }));
    rim.position.set(0, (x > 0 ? 0.17 : 0.21) * Math.sign(z), 0); rim.rotation.x = Math.sign(z) * -Math.PI / 2; w.add(rim);
    w.userData.mat = wmat; g.userData.wheels.push(w);
  }
  return g;
}
// cada coche lleva dos versiones: «real» (por defecto, Iker 28/10: «el F1 más real») y la antigua de dibujo (window.CARMODE = 'toon')
function dualCar(col, stripe, band) {
  const w = new THREE.Group();
  const toonV = makeCar(col, stripe), realV = makeCarPro(col, stripe === 0xffffff ? 0x15161a : stripe, band);
  w.add(toonV, realV); w.userData = { toonV, realV, wheels: [...toonV.userData.wheels, ...realV.userData.wheels] };
  return w;
}
const carA = dualCar(RED, 0xffffff, 0xf2c200);   // el de delante
const carB = dualCar(0x26282e, RED, 0xffffff);   // el que caza el rebufo
world.add(carA, carB);
// luz realista: reflejos de estudio y sombra en el suelo
{
  const pm = new THREE.PMREMGenerator(gl);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.6;
  gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
  sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
  Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 60 });
}
const shadowCatcher = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), new THREE.ShadowMaterial({ opacity: 0.22 }));
shadowCatcher.rotation.x = -Math.PI / 2; shadowCatcher.position.y = 0.03; shadowCatcher.receiveShadow = true; scene.add(shadowCatcher);
function carMode() {
  const real = window.CARMODE !== 'toon';
  for (const c of [carA, carB]) { c.userData.realV.visible = real; c.userData.toonV.visible = !real; }
  // la sombra sigue al coche rojo
  sun.position.set(carA.position.x + 6, 14, carA.position.z + 8); sun.target.position.copy(carA.position); sun.target.updateMatrixWorld();
}
function placeCar(car, x, z, yaw = 0, spin = 0) {
  car.position.set(x, 0, z); car.rotation.y = yaw;
  car.userData.wheels.forEach(w => { w.rotation.y = -spin; });
}
function heatWheels(car, h) {
  const c = new THREE.Color(0x222222).lerp(new THREE.Color(RED), h);
  car.userData.wheels.forEach(w => w.userData.mat.color.copy(c));
}

// ---------- aire: líneas de corriente limpias (túnel de viento) + remolinos rojos del rebufo ----------
// Iker (28/10): las rayitas de antes no gustaban → curvas suaves fijas alrededor del coche con «gotas» que viajan por ellas.
const AIR_BLUE = 0x3a86d8, AIR_SOFT = 0xb9cde3;
const air = new THREE.Group(); scene.add(air);
const flowLines = [];
{
  const seeds = [];
  for (const y of [0.35, 0.8, 1.3]) for (const z of [-1.15, -0.4, 0.4, 1.15]) seeds.push([y, z]);
  for (const [y, z] of [[2.0, 0], [2.0, -0.9], [2.0, 0.9], [0.5, -2.0], [0.5, 2.0], [1.2, -2.0], [1.2, 2.0]]) seeds.push([y, z]);
  seeds.forEach(([y, z], i) => {
    const pts = [];
    for (let x = 13; x >= -3.2; x -= 0.4) {
      const f = Math.exp(-Math.pow((x - 0.6) / 2.4, 2)) + (x < 0.6 ? Math.exp(-Math.pow((x - 0.6) / 1.6, 2)) * 0 : 0);
      let yy = y, zz = z;
      if (Math.abs(z) < 1.5 && y < 1.6) { yy = y + f * (1.75 - y) * 0.95; zz = z + f * Math.sign(z) * (1.5 - Math.abs(z)) * 0.55; }
      else { yy = y + f * 0.12; }
      pts.push(new THREE.Vector3(x, yy, zz));
    }
    const curve = new THREE.CatmullRomCurve3(pts);
    const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 80, 0.028, 6, false),
      new THREE.MeshBasicMaterial({ color: AIR_SOFT, transparent: true, opacity: 0.85 }));
    air.add(tube);
    const drops = [];
    for (let k = 0; k < 3; k++) {
      const d = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, 0.55, 4, 8), new THREE.MeshBasicMaterial({ color: AIR_BLUE, transparent: true }));
      air.add(d); drops.push(d);
    }
    flowLines.push({ curve, tube, drops, ph: (i * 0.137) % 1 });
  });
}
// remolinos del rebufo: hélices rojas que giran y se abren detrás del coche
const wakeG = new THREE.Group(); air.add(wakeG);
const wakeMats = [];
for (let h = 0; h < 5; h++) {
  const pts = [];
  for (let x = -2.4; x >= -17; x -= 0.25) {
    const k = (-2.4 - x) / 14.6, r = 0.25 + k * 1.2, a = x * 1.05 + h * (Math.PI * 2 / 5);
    pts.push(new THREE.Vector3(x, 0.85 + Math.sin(a) * r * 0.8, Math.cos(a) * r));
  }
  const m = new THREE.MeshBasicMaterial({ color: RED, transparent: true, opacity: 0.5, depthWrite: false });
  wakeMats.push(m);
  wakeG.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 160, 0.035, 6, false), m));
}
const _up = new THREE.Vector3(0, 1, 0);
// amount: cuántas líneas se ven (0..1); wake: fuerza de los remolinos (0..1). Va pegado al coche rojo (carA).
function airflow(t, cx, cz, amount, wake) {
  air.position.copy(carA.position); air.rotation.copy(carA.rotation);
  const n = Math.round(flowLines.length * amount);
  flowLines.forEach((L, i) => {
    const on = i < n;
    L.tube.visible = on;
    L.drops.forEach((d, k) => {
      d.visible = on;
      if (!on) return;
      const u = ((t * 0.55 + L.ph + k / 3) % 1);
      const p = L.curve.getPointAt(u), tg = L.curve.getTangentAt(u);
      d.position.copy(p); d.quaternion.setFromUnitVectors(_up, tg);
      d.material.opacity = Math.min(1, u * 8, (1 - u) * 8);
    });
  });
  wakeG.visible = wake > 0.02;
  wakeG.rotation.x = -t * 3.2;
  wakeMats.forEach(m => { m.opacity = 0.55 * wake; });
}

// cono del rebufo
const wakeCone = new THREE.Mesh(new THREE.ConeGeometry(1.6, 16, 24, 1, true), new THREE.MeshBasicMaterial({ color: RED, transparent: true, opacity: 0.12, depthWrite: false, side: THREE.DoubleSide }));
wakeCone.rotation.z = -Math.PI / 2; wakeCone.material.visible = false; scene.add(wakeCone);

// flechas de carga aerodinámica
const arrows = [];
for (let i = 0; i < 6; i++) { const a = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(), 1.5, RED, 0.4, 0.3); scene.add(a); arrows.push(a); }
function setArrows(car, n0, len) {
  const xs = [1.6, 0, -1.6];
  for (let i = 0; i < 3; i++) {
    const a = arrows[n0 + i];
    if (!car) { a.visible = false; continue; }
    a.visible = len > 0.05;
    const p = new THREE.Vector3(xs[i], 0, 0).applyEuler(car.rotation).add(car.position);
    a.position.set(p.x, 1.4 + len, p.z);
    a.setLength(Math.max(0.3, len), 0.4, 0.3);
  }
}

// ---------- Ojo 3D (como el logo: ojo almendrado, iris rojo, palitos con codos y rodillas) ----------
function stick(len, r = 0.075) {
  const g = new THREE.Group();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 8), new THREE.MeshBasicMaterial({ color: INK }));
  m.position.y = -len / 2; g.add(m);
  const j = new THREE.Mesh(new THREE.SphereGeometry(r * 1.25, 10, 8), new THREE.MeshBasicMaterial({ color: INK }));
  g.add(j);
  return g;
}
function makeOjo() {
  const o = new THREE.Group();
  const body = new THREE.Group(); o.add(body);
  const torso = stick(1.9, 0.085); torso.position.y = 3.5; body.add(torso);
  const head = new THREE.Group(); head.position.y = 4.15; body.add(head);
  const eye = ink(new THREE.Mesh(new THREE.SphereGeometry(1, 32, 20), toon(0xffffff)), 1.07, false);
  eye.scale.set(1.25, 0.72, 0.55); head.add(eye);
  const iris = new THREE.Group(); iris.position.z = 0.56; head.add(iris);
  const ir = new THREE.Mesh(new THREE.CircleGeometry(0.43, 32), new THREE.MeshBasicMaterial({ color: RED })); iris.add(ir);
  const irRing = new THREE.Mesh(new THREE.RingGeometry(0.43, 0.48, 32), new THREE.MeshBasicMaterial({ color: INK })); irRing.position.z = 0.001; iris.add(irRing);
  const pu = new THREE.Mesh(new THREE.CircleGeometry(0.2, 24), new THREE.MeshBasicMaterial({ color: INK })); pu.position.z = 0.002; iris.add(pu);
  const hl = new THREE.Mesh(new THREE.CircleGeometry(0.08, 12), new THREE.MeshBasicMaterial({ color: 0xffffff })); hl.position.set(0.12, 0.12, 0.003); iris.add(hl);
  // párpado: semiesfera blanca que baja al parpadear
  const lid = new THREE.Mesh(new THREE.SphereGeometry(1.02, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), toon(0xffffff));
  lid.scale.set(1.25, 0.72, 0.57); head.add(lid);
  const limb = (x, y) => { const up = stick(0.85); up.position.set(x, y, 0); const lo = stick(0.85); lo.position.y = -0.85; up.add(lo); body.add(up); return [up, lo]; };
  const [lsh, lel] = limb(-0.02, 3.0), [rsh, rel] = limb(0.02, 3.0);
  const [lhip, lkn] = limb(-0.05, 1.6), [rhip, rkn] = limb(0.05, 1.6);
  o.userData = { head, iris, lid, eye, lsh, lel, rsh, rel, lhip, lkn, rhip, rkn, body };
  return o;
}
const ojo = makeOjo();
const ojoScene = new THREE.Scene();
const ojoCam = new THREE.PerspectiveCamera(38, W / H, 0.1, 100);
ojoScene.add(new THREE.HemisphereLight(0xffffff, 0xd8d8d8, 1.6));
{ const l = new THREE.DirectionalLight(0xffffff, 1.4); l.position.set(3, 6, 8); ojoScene.add(l); }
ojoScene.add(ojo);
gl.autoClear = false;
// poses: ángulos (rad) de hombro/codo/cadera/rodilla en el plano de la pantalla
const POSES = {
  idle:     { ls: 0.55, le: 0.35, rs: -0.55, re: -0.35, lh: 0.3, lk: -0.1, rh: -0.3, rk: 0.1, look: [0, 0] },
  point:    { ls: 0.6, le: 0.4, rs: -2.0, re: -0.3, lh: 0.3, lk: -0.1, rh: -0.3, rk: 0.1, look: [0.18, 0.06] },
  think:    { ls: 0.6, le: 0.4, rs: -0.7, re: -2.5, lh: 0.28, lk: -0.1, rh: -0.28, rk: 0.1, look: [-0.12, 0.14] },
  surprise: { ls: 2.4, le: 0.5, rs: -2.4, re: -0.5, lh: 0.3, lk: -0.1, rh: -0.3, rk: 0.1, look: [0, 0.02] },
  cheer:    { ls: 2.7, le: -0.3, rs: -2.7, re: 0.3, lh: 0.22, lk: -0.3, rh: -0.22, rk: 0.3, look: [0, 0.1] },
  push:     { ls: 1.45, le: 0.15, rs: -1.45, re: -0.15, lh: 0.4, lk: -0.5, rh: -0.05, rk: 0.1, look: [0.15, 0] },
  wave:     { ls: 0.55, le: 0.35, rs: -2.5, re: -0.6, lh: 0.3, lk: -0.1, rh: -0.3, rk: 0.1, look: [0.05, 0.05] },
};
function poseOjo(name, prev, u, t) {
  const A = POSES[prev] || POSES.idle, B = POSES[name] || POSES.idle, k = eob(u);
  const P = {}; for (const key in B) P[key] = key === 'look' ? [lerp(A.look[0], B.look[0], k), lerp(A.look[1], B.look[1], k)] : lerp(A[key], B[key], k);
  const d = ojo.userData, wob = Math.sin(t * 2.2) * 0.04;
  d.lsh.rotation.z = P.ls + wob; d.lel.rotation.z = P.le; d.rsh.rotation.z = P.rs - wob; d.rel.rotation.z = P.re;
  if (name === 'wave') d.rel.rotation.z = -0.6 + Math.sin(t * 9) * 0.45;
  d.lhip.rotation.z = P.lh; d.lkn.rotation.z = P.lk; d.rhip.rotation.z = P.rh; d.rkn.rotation.z = P.rk;
  d.iris.position.x = P.look[0]; d.iris.position.y = P.look[1];
  d.body.position.y = Math.abs(Math.sin(t * 2.2)) * 0.06 + (name === 'cheer' ? Math.abs(Math.sin(t * 6)) * 0.25 : 0);
  d.head.rotation.z = Math.sin(t * 1.3) * 0.05;
  // parpadeo cada ~3,3 s
  const bp = (t + 0.7) % 3.3, bl = bp < 0.16 ? Math.sin(bp / 0.16 * Math.PI) : 0;
  d.lid.visible = bl > 0.02;
  d.lid.rotation.x = lerp(-Math.PI / 2 - 0.2, -0.05, bl);
}

// ---------- capa 2D ----------
const F = (w, s) => `${w} ${s}px Inter`;
function rrect(x, y, w, h, r) { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); }
function pill(x, y, text, u, col = '#111', size = 26) {
  if (u <= 0) return;
  const k = eob(u);
  ctx.save(); ctx.font = F(800, size);
  const tw = ctx.measureText(text).width, w = tw + size * 1.3, h = size * 1.75;
  ctx.translate(x, y); ctx.scale(k, k); ctx.globalAlpha = clamp(u * 3);
  rrect(-w / 2, -h / 2, w, h, h / 2); ctx.fillStyle = col; ctx.fill();
  ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 0, 1);
  ctx.restore();
}
function title(main, sub, u) {
  if (!main) return;
  const k = ease(u * 2.5);
  ctx.save(); ctx.globalAlpha = k; ctx.translate((1 - k) * -30, 0);
  ctx.font = F(800, 40); const tw0 = Math.max(ctx.measureText(main).width, 200);
  ctx.fillStyle = 'rgba(255,255,255,0.88)'; rrect(22, 60, tw0 + 56, 102, 14); ctx.fill();
  ctx.fillStyle = CSS_RED; ctx.fillRect(34, 72, 7, 78);
  ctx.fillStyle = '#111'; ctx.font = F(800, 40); ctx.textBaseline = 'alphabetic'; ctx.fillText(main, 56, 108);
  ctx.fillStyle = '#8a8a8a'; ctx.font = F(500, 24); ctx.fillText(sub, 57, 144);
  ctx.restore();
}
const imgPerfil = new Image(); imgPerfil.src = 'perfil.png';
function banner(u) {
  if (u <= 0 || u >= 1) return;
  const dur = 3.2, tt = u * dur;
  const y = tt < 0.35 ? lerp(-130, 40, eob(tt / 0.35)) : tt > dur - 0.3 ? lerp(40, -130, ease((tt - dur + 0.3) / 0.3)) : 40;
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.18)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 6;
  rrect(26, y, W - 52, 104, 26); ctx.fillStyle = 'rgba(248,248,248,0.97)'; ctx.fill(); ctx.restore();
  ctx.save(); rrect(44, y + 18, 68, 68, 16); ctx.clip(); if (imgPerfil.complete) ctx.drawImage(imgPerfil, 44, y + 18, 68, 68); ctx.restore();
  ctx.fillStyle = '#111'; ctx.font = F(800, 24); ctx.fillText('Ojo al dato', 128, y + 46);
  ctx.fillStyle = '#9a9a9a'; ctx.font = F(500, 19); ctx.fillText('ahora', W - 110, y + 46);
  ctx.fillStyle = '#333'; ctx.font = F(500, 21); ctx.fillText('Sígueme para un dato nuevo cada día', 128, y + 78);
}
// subtítulos palabra a palabra: trozos de 5-6 palabras, la clave en blanco sobre marcador rojo
function chunkTokens(tokens) {
  const ch = []; let cur = [];
  tokens.forEach((tk, i) => {
    cur.push(tk);
    const brk = /[.,…:;!?]$/.test(tk.w) && cur.length >= 3;
    if (cur.length >= 6 || brk || i === tokens.length - 1) { ch.push(cur); cur = []; }
  });
  return ch;
}
function captions(t, line, yc) {
  if (!line) return;
  const chunks = chunkTokens(line.tokens);
  let c = null;
  for (let i = 0; i < chunks.length; i++) {
    const s = chunks[i][0].s, e = i + 1 < chunks.length ? chunks[i + 1][0].s : line.end + 0.25;
    if (t >= s - 0.05 && t < e) { c = chunks[i]; break; }
  }
  if (!c) return;
  ctx.save(); ctx.font = F(800, 44); ctx.textBaseline = 'middle';
  const sp = 13, maxW = 640;
  const rows = [[]]; let rw = 0;
  c.forEach(tk => { const w = ctx.measureText(tk.w).width; if (rw + w > maxW && rows[rows.length - 1].length) { rows.push([]); rw = 0; } rows[rows.length - 1].push([tk, w]); rw += w + sp; });
  const y0 = (yc || 1112) - (rows.length - 1) * 31;
  rows.forEach((row, ri) => {
    const tw = row.reduce((a, [, w]) => a + w + sp, -sp);
    let x = W / 2 - tw / 2; const y = y0 + ri * 62;
    row.forEach(([tk, w]) => {
      const u = clamp((t - tk.s) / 0.12);
      if (u > 0) {
        const k = tk.key ? eob(clamp((t - tk.s) / 0.18)) : 1;
        if (tk.key) {
          ctx.save(); ctx.translate(x + w / 2, y); ctx.scale(lerp(1.35, 1, k), lerp(1.35, 1, k));
          rrect(-w / 2 - 9, -30, w + 18, 58, 10); ctx.fillStyle = CSS_RED; ctx.globalAlpha = clamp(u * 2); ctx.fill();
          ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.fillText(tk.w, 0, 2); ctx.restore();
        } else {
          const pk = lerp(1.3, 1, eob(clamp((t - tk.s) / 0.16)));   // cada palabra entra con un golpecito
          ctx.save(); ctx.translate(x + w / 2, y); ctx.scale(pk, pk);
          // sobre el asfalto: letra blanca con borde negro grueso (se lee en cualquier fondo)
          ctx.globalAlpha = u; ctx.textAlign = 'center'; ctx.lineJoin = 'round';
          ctx.lineWidth = 9; ctx.strokeStyle = '#111'; ctx.strokeText(tk.w, 0, 2);
          ctx.fillStyle = t < tk.e + 0.05 ? '#ffffff' : '#ececec'; ctx.fillText(tk.w, 0, 2); ctx.restore();
        }
      }
      x += w + sp;
    });
  });
  ctx.restore();
}
function proj(v) { const p = v.clone().project(cam); return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H]; }
function gauge(x, y, val, u) {
  if (u <= 0) return;
  ctx.save(); ctx.globalAlpha = clamp(u * 3); ctx.translate(x, y); ctx.scale(eob(u), eob(u));
  ctx.beginPath(); ctx.arc(0, 0, 118, 0, 7); ctx.fillStyle = 'rgba(255,255,255,0.92)'; ctx.fill();
  ctx.lineWidth = 14; ctx.lineCap = 'round';
  ctx.strokeStyle = '#e6e6e6'; ctx.beginPath(); ctx.arc(0, 0, 96, Math.PI * 0.8, Math.PI * 2.2); ctx.stroke();
  const f = clamp((val - 200) / 150);
  ctx.strokeStyle = CSS_RED; ctx.beginPath(); ctx.arc(0, 0, 96, Math.PI * 0.8, Math.PI * (0.8 + 1.4 * f)); ctx.stroke();
  ctx.fillStyle = '#111'; ctx.font = F(800, 50); ctx.textAlign = 'center'; ctx.fillText(Math.round(val), 0, 12);
  ctx.fillStyle = '#8a8a8a'; ctx.font = F(500, 20); ctx.fillText('km/h', 0, 44);
  ctx.restore();
}
function meter(x, y, f, label, u) {
  if (u <= 0) return;
  ctx.save(); ctx.globalAlpha = clamp(u * 3);
  rrect(x - 14, y - 46, 448, 94, 16); ctx.fillStyle = 'rgba(255,255,255,0.92)'; ctx.fill();
  ctx.fillStyle = '#111'; ctx.font = F(800, 22); ctx.fillText(label, x, y - 16);
  rrect(x, y, 420, 34, 17); ctx.fillStyle = '#ececec'; ctx.fill();
  rrect(x, y, Math.max(34, 420 * f), 34, 17); ctx.fillStyle = CSS_RED; ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = F(800, 20); ctx.fillText(Math.round(f * 100) + ' %', x + 14, y + 24);
  ctx.restore();
}
function bolt(x, y, s, u) {
  if (u <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * eob(u), s * eob(u));
  ctx.beginPath(); ctx.moveTo(4, -30); ctx.lineTo(-14, 4); ctx.lineTo(0, 4); ctx.lineTo(-6, 30); ctx.lineTo(16, -6); ctx.lineTo(2, -6); ctx.closePath();
  ctx.fillStyle = '#FFD21F'; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = '#111'; ctx.stroke(); ctx.restore();
}
function gapMarker(p1, p2, text, u) {
  if (u <= 0) return;
  ctx.save(); ctx.globalAlpha = clamp(u * 3); ctx.strokeStyle = '#111'; ctx.lineWidth = 3; ctx.setLineDash([8, 7]);
  ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke(); ctx.restore();
  pill((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 - 38, text, u, CSS_RED, 24);
}
function outroCard(t, u) {
  ctx.save(); ctx.globalAlpha = clamp(u * 3);
  ctx.fillStyle = '#111'; ctx.font = F(800, 66); ctx.textAlign = 'center';
  const k = eob(clamp(u * 1.5));
  ctx.save(); ctx.translate(W / 2, 250); ctx.scale(k, k); ctx.fillText('¡Ojo al dato!', 0, 0); ctx.restore();
  ctx.fillStyle = CSS_RED; ctx.fillRect(W / 2 - 70, 278, 140, 7);
  const bu = clamp((u - 0.25) * 3);
  if (bu > 0) {
    const bk = eob(bu);
    ctx.save(); ctx.translate(W / 2 - 130, 1150); ctx.scale(bk, bk);
    rrect(-110, -38, 220, 76, 38); ctx.fillStyle = '#111'; ctx.fill();
    ctx.fillStyle = '#fff'; ctx.font = F(800, 28); ctx.fillText('♥ Me gusta', 0, 10); ctx.restore();
    ctx.save(); ctx.translate(W / 2 + 130, 1150); ctx.scale(bk, bk);
    rrect(-110, -38, 220, 76, 38); ctx.fillStyle = CSS_RED; ctx.fill();
    ctx.fillStyle = '#fff'; ctx.font = F(800, 28); ctx.fillText('+ Seguir', 0, 10); ctx.restore();
    ctx.fillStyle = '#8a8a8a'; ctx.font = F(700, 28); ctx.fillText('@ojoaldato.ya', W / 2, 1240);
  }
  ctx.restore();
}

// ---------- Urda (Toledo), 28/10/2026 · tono informativo y triste (Iker, 29/10) ----------
// El choque NO se ve: la escena 3 funde a oscuro antes. Nada de colores alegres: cielo nublado, campo seco de La Mancha.

const OJO_POSE = ['think', 'point', 'point', 'think', 'think', 'think', 'point', 'point', 'think', 'think', 'think'];
cam.far = 1200; cam.updateProjectionMatrix();
scene.fog = new THREE.Fog(0xcfd5dc, 160, 900);

// texturas
const UT = {
  field: canvasTex(256, 256, (x, w, h) => { x.fillStyle = '#b89a62'; x.fillRect(0, 0, w, h);
    for (let i = 0; i < 16; i++) { x.fillStyle = i % 2 ? '#a88a55' : '#c2a46b'; x.fillRect(0, i * 16, w, 9); }
    noise(x, w, h, 5000, ['#9c7f4c', '#cbb07a', '#ae905a', '#8f7445'], 2); }, 120, 120),
  slab: canvasTex(64, 256, (x, w, h) => { x.fillStyle = '#9ea2a6'; x.fillRect(0, 0, w, h);
    for (let i = 0; i < 8; i++) { x.fillStyle = '#7f8387'; x.fillRect(0, i * 32 + 4, w, 12); } noise(x, w, h, 600, ['#8d9195', '#b0b4b8'], 2); }, 1, 400),
  ballast: canvasTex(128, 128, (x, w, h) => { x.fillStyle = '#7d7a74'; x.fillRect(0, 0, w, h); noise(x, w, h, 4000, ['#6a6761', '#8f8b84', '#5c5a55', '#a39f97'], 3); }, 300, 4),
  hills: canvasTex(512, 128, (x, w, h) => { const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, w, h);
    x.fillStyle = '#8f8a7c'; x.beginPath(); x.moveTo(0, h); for (let i = 0; i <= 32; i++) x.lineTo(i * w / 32, h * 0.45 + Math.sin(i * 0.9) * 14 + Math.sin(i * 2.3) * 7); x.lineTo(w, h); x.fill(); }, 4, 1),
  sky: canvasTex(4, 256, (x, w, h) => { const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, '#7f8a97'); g.addColorStop(0.65, '#b9c1ca'); g.addColorStop(1, '#d9dee3'); x.fillStyle = g; x.fillRect(0, 0, w, h); }),
};
UT.hills.wrapT = THREE.ClampToEdgeWrapping; UT.hills.transparent = true;
UT.sky.wrapS = UT.sky.wrapT = THREE.ClampToEdgeWrapping;

const rail = new THREE.Group(); scene.add(rail);
{
  const fld = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshLambertMaterial({ map: UT.field })); fld.rotation.x = -Math.PI / 2; fld.position.y = -0.3; rail.add(fld);
  const bal = new THREE.Mesh(new THREE.PlaneGeometry(1600, 16), new THREE.MeshLambertMaterial({ map: UT.ballast })); bal.rotation.x = -Math.PI / 2; bal.position.set(0, -0.05, 3); rail.add(bal);
  const steel = new THREE.MeshStandardMaterial({ color: 0x9aa0a6, metalness: 0.85, roughness: 0.35 });
  for (const z of [0, 6]) {
    const sl = new THREE.Mesh(new THREE.BoxGeometry(1600, 0.3, 3.0), [0, 0, new THREE.MeshLambertMaterial({ map: UT.slab }), 0, 0, 0].map(m => m || new THREE.MeshLambertMaterial({ color: 0x8d9195 })));
    sl.material[2].map.rotation = Math.PI / 2; sl.position.set(0, 0.1, z); rail.add(sl);
    for (const dz of [-0.72, 0.72]) { const r = new THREE.Mesh(new THREE.BoxGeometry(1600, 0.18, 0.08), steel); r.position.set(0, 0.34, z + dz); rail.add(r); }
    const wire = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1600, 4), new THREE.MeshBasicMaterial({ color: 0x2c2f33 })); wire.rotation.z = Math.PI / 2; wire.position.set(0, 5.6, z); rail.add(wire);
  }
  const poleM = new THREE.MeshLambertMaterial({ color: 0x5d6166 });
  for (let x = -780; x <= 780; x += 45) for (const z of [-3.2, 9.2]) {
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.18, 7.2, 8), poleM); p.position.set(x, 3.3, z); rail.add(p);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 4.2), poleM); arm.position.set(x, 6.2, z + (z < 0 ? 2.0 : -2.0)); rail.add(arm);
  }
  // olivos dispersos por el campo
  const tr = rng(5), crown = new THREE.MeshLambertMaterial({ color: 0x5f6b45 }), trunk = new THREE.MeshLambertMaterial({ color: 0x5a4632 });
  for (let i = 0; i < 260; i++) {
    const x = (tr() - 0.5) * 1400, z = (tr() < 0.5 ? -1 : 1) * (22 + tr() * 420) + 3;
    const c = new THREE.Mesh(new THREE.SphereGeometry(1.6 + tr(), 8, 6), crown); c.scale.y = 0.75; c.position.set(x, 2.1, z); rail.add(c);
    const k = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.25, 1.6, 6), trunk); k.position.set(x, 0.6, z); rail.add(k);
  }
  const hl = new THREE.Mesh(new THREE.PlaneGeometry(3000, 120), new THREE.MeshBasicMaterial({ map: UT.hills, transparent: true, fog: false, color: 0xc8c8c8 })); hl.position.set(0, 30, -700); rail.add(hl);
}

// tren de alta velocidad genérico (sin logotipos): morro afilado + coches con ventanas y franja
function nose(len, w, h) {
  const g = new THREE.CylinderGeometry(0.01, 1, len, 28, 8);
  g.rotateZ(-Math.PI / 2); g.translate(len / 2, 0, 0);
  const p = g.attributes.position;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i) / len; const k = Math.pow(1 - x, 0.55);
    p.setY(i, p.getY(i) * h * k - (1 - k) * h * 0.45); p.setZ(i, p.getZ(i) * w * Math.pow(1 - x, 0.4)); }
  g.computeVertexNormals(); return g;
}
function makeTrain(body, stripe, label, n = 4) {
  const g = new THREE.Group();
  const paint = new THREE.MeshPhysicalMaterial({ color: body, roughness: 0.35, clearcoat: 0.8 });
  const strM = new THREE.MeshPhysicalMaterial({ color: stripe, roughness: 0.4, clearcoat: 0.6 });
  const glass = new THREE.MeshStandardMaterial({ color: 0x1b2128, roughness: 0.15, metalness: 0.5 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x2a2c30, roughness: 0.7 });
  g.userData.cars = [];
  for (let i = 0; i < n; i++) {
    const c = new THREE.Group(); c.position.x = -i * 20.6; g.add(c); g.userData.cars.push(c);
    const b = new THREE.Mesh(new RoundedBoxGeometry(19.6, 3.5, 2.9, 3, 0.45), paint); b.position.y = 2.35; c.add(b);
    for (const s of [-1, 1]) {
      const wnd = new THREE.Mesh(new THREE.BoxGeometry(16.5, 0.62, 0.02), glass); wnd.position.set(0, 2.85, s * 1.455); c.add(wnd);
      const st = new THREE.Mesh(new THREE.BoxGeometry(19.0, 0.32, 0.02), strM); st.position.set(0, 1.55, s * 1.456); c.add(st);
    }
    for (const bx of [-6.8, 6.8]) { const bg = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.8, 2.3), dark); bg.position.set(bx, 0.62, 0); c.add(bg); }
    if (i === 0 || i === n - 1) {
      const nz = new THREE.Mesh(nose(7.5, 1.45, 1.75), paint); nz.position.set(9.6, 2.35, 0); if (i === n - 1) { nz.rotation.y = Math.PI; nz.position.x = -9.6; } c.add(nz);
      const ws = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 12, 0, Math.PI * 2, 0, 1.0), glass); ws.scale.set(2.2, 0.55, 1.05);
      ws.position.set(i === 0 ? 11.6 : -11.6, 3.15, 0); ws.rotation.z = i === 0 ? -0.95 : 0.95; c.add(ws);
      const ns = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.3, 2.95), strM); ns.position.set(i === 0 ? 11.5 : -11.5, 1.55, 0); ns.scale.set(1, 1, 0.7); c.add(ns);
    }
    if (i === 1) { const pt = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.12, 0.6), dark); pt.position.set(0, 4.45, 0); pt.rotation.z = 0.25; c.add(pt); }
    c.traverse(m => { if (m.isMesh) m.castShadow = true; });
  }
  g.userData.label = label;
  return g;
}
const iryo = makeTrain(0xc0172d, 0xffffff, 'IRYO');      // rojo
const ave = makeTrain(0xf2f3f5, 0x5b2a86, 'AVE');        // blanco con franja morada
scene.add(iryo, ave);

// señales a pie de vía (para explicar el fallo de señalización)
const signals = [];
for (let i = 0; i < 7; i++) {
  const s = new THREE.Group(); s.position.set(-60 + i * 55, 0, -2.2); rail.add(s);
  const post = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 3.4, 6), new THREE.MeshLambertMaterial({ color: 0x3b3e42 })); post.position.y = 1.7; s.add(post);
  const head = new THREE.Mesh(new RoundedBoxGeometry(0.5, 1.0, 0.35, 2, 0.1), new THREE.MeshLambertMaterial({ color: 0x1d1f22 })); head.position.y = 3.6; s.add(head);
  const lamp = new THREE.Mesh(new THREE.CircleGeometry(0.16, 16), new THREE.MeshBasicMaterial({ color: 0x2bd96b })); lamp.position.set(0.0, 3.75, 0.18); s.add(lamp);
  s.userData.lamp = lamp; signals.push(s);
}
// cinta y valla cortando la vía, mástil con bandera a media asta, velas
const tape = new THREE.Group(); rail.add(tape);
{
  const red = new THREE.MeshLambertMaterial({ color: 0xd8262b }), white = new THREE.MeshLambertMaterial({ color: 0xf2f2f2 });
  for (let k = 0; k < 8; k++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.25, 1.0), k % 2 ? red : white); b.position.set(30, 1.2, -1.6 + k * 1.15); tape.add(b); }
  for (const z of [-2, 7.6]) { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.3, 6), white); p.position.set(30, 0.65, z); tape.add(p); }
}
const flag = new THREE.Group(); rail.add(flag);
{
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.09, 11, 8), new THREE.MeshStandardMaterial({ color: 0xcfd2d6, metalness: 0.7, roughness: 0.3 })); pole.position.y = 5.5; flag.add(pole);
  const c = document.createElement('canvas'); c.width = 96; c.height = 64; const x = c.getContext('2d');
  x.fillStyle = '#c60b1e'; x.fillRect(0, 0, 96, 64); x.fillStyle = '#ffc400'; x.fillRect(0, 16, 96, 32);
  const f = new THREE.Mesh(new THREE.PlaneGeometry(3, 2, 12, 4), new THREE.MeshLambertMaterial({ map: new THREE.CanvasTexture(c), side: THREE.DoubleSide }));
  f.position.set(1.55, 6.2, 0); flag.add(f); flag.userData.cloth = f;   // a media asta
  flag.position.set(8, 0, -9);
}
const candles = new THREE.Group(); scene.add(candles);
{
  const wax = new THREE.MeshLambertMaterial({ color: 0xf4efe2 });
  for (let i = 0; i < 9; i++) {
    const c = new THREE.Group(); c.position.set((i % 3 - 1) * 0.55 + (Math.floor(i / 3) % 2) * 0.25, 0, (Math.floor(i / 3) - 1) * 0.55); candles.add(c);
    const h = 0.35 + (i * 37 % 10) / 30;
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.11, h, 16), wax); b.position.y = h / 2; c.add(b);
    const fl = new THREE.Mesh(new THREE.SphereGeometry(0.05, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffc35a })); fl.scale.y = 1.8; fl.position.y = h + 0.08; c.add(fl);
    const pl = new THREE.PointLight(0xffa640, 0.6, 2.5); pl.position.y = h + 0.12; c.add(pl);
    c.userData.flame = fl;
  }
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.05, 32), new THREE.MeshLambertMaterial({ color: 0x6b6d70 })); base.position.y = -0.03; candles.add(base);
  candles.position.set(40, 0.0, -6);
}

function setBg() { scene.background = UT.sky; }
const LOOK = new THREE.Vector3();
const prevFrame = document.createElement('canvas'); prevFrame.width = W * PR; prevFrame.height = H * PR; let prevA = 0;
function setCam(px, py, pz, lx, ly, lz, up) { cam.up.set(...(up || [0, 1, 0])); cam.position.set(px, py, pz); LOOK.set(lx, ly, lz); cam.fov = 38; cam.updateProjectionMatrix(); cam.lookAt(lx, ly, lz); cam.updateMatrixWorld(); }
function camFx(t, t0, t1, si) {
  const dur = Math.max(0.6, t1 - t0), k = clamp((t - t0) / dur);
  const P = cam.position.clone(), D = LOOK.clone().sub(P);
  let f = 0.05 * ease(k); let fov = 38;
  const tin = t - t0, tout = Math.max(0, t1 - t);
  if (si > 0 && tin < 1.4) { const a = 1 - ease(tin / 1.4); f += 0.22 * a; fov -= 2 * a; }
  if (tout < 1.1) { const a = ease(1 - tout / 1.1); f += 0.18 * a; fov -= 2 * a; }
  P.add(D.multiplyScalar(f));
  cam.position.copy(P); cam.fov = fov; cam.updateProjectionMatrix(); cam.lookAt(LOOK); cam.updateMatrixWorld();
}
let DIM = 0;   // oscurecido general de la escena (0..1)
function hideAll() {
  wakeCone.visible = false; arrows.forEach(a => a.visible = false); air.visible = false;
  straight.visible = false; curve.visible = false; carA.visible = carB.visible = false; ground.visible = false; shadowCatcher.visible = false;
  rail.visible = true; iryo.visible = true; ave.visible = false; tape.visible = false; flag.visible = false; candles.visible = false;
  signals.forEach(s => s.userData.lamp.material.color.setHex(0x2bd96b));
  iryo.userData.cars.forEach(c => { c.position.z = 0; c.rotation.set(0, 0, 0); c.position.y = 0; });
  iryo.position.set(0, 0, 0); ave.position.set(-400, 0, 0); ave.userData.cars.forEach(c => c.rotation.set(0, 0, 0)); iryo.userData.cars.forEach((c, i) => { c.position.x = -i * 20.6; }); DIM = 0;
  sun.intensity = 1.0;
}
const SC = [
  // 0 · gancho: la vía vacía en el campo, plano aéreo lento
  (t, u) => { iryo.visible = false; setCam(lerp(-140, -100, u), 38, 70, lerp(20, 40, u), 0, 0); return []; },
  // 1 · fecha y lugar
  (t, u) => { iryo.visible = false; setCam(-60 + u * 20, 6, 22, 20 + u * 20, 2, 0);
    return [['clock', '28 OCT', 'MADRID – ANDALUCÍA', clamp(u * 4)], ['pill', W / 2, 520, 'CERCA DE URDA · TOLEDO', clamp((u - 0.25) * 4)]]; },
  // 2 · 8:30 · falla la señalización: las señales se apagan una a una
  (t, u) => { iryo.visible = false; signals.forEach((s, i) => { if (u > 0.2 + i * 0.07) s.userData.lamp.material.color.setHex(0x3a3d41); });
    setCam(-80, 3.6, -6, 80, 3, -2.2);
    return [['clock', '8:30', 'FALLA EL LZB', clamp(u * 4)], ['pill', W / 2, 520, 'SIN SEÑALES EN EL TRAMO', clamp((u - 0.4) * 4), CSS_RED]]; },
  // 3 · los trenes se paran: el Iryo delante y el AVE más atrás, en la misma vía
  (t, u) => { ave.visible = true; ave.position.x = -215; setCam(-420, 48, -24, -90, 0, 3);
    const pi = proj(new THREE.Vector3(-30, 6, 0)), pa = proj(new THREE.Vector3(-245, 6, 0));
    return [['pill', pi[0], pi[1] - 40, 'IRYO · PARADO', clamp((u - 0.15) * 4)], ['pill', pa[0], pa[1] - 40, 'AVE · PARADO', clamp((u - 0.45) * 4), CSS_RED]]; },
  // 4 · el centro de control autoriza seguir (según el ministro)
  (t, u) => { ave.visible = true; ave.position.x = -215; setCam(-420, 48, -24, -90, 0, 3); DIM = 0.55;
    return [['panel', u], ['pill', W / 2, 330, 'SEGÚN EL MINISTRO DE TRANSPORTES', clamp(u * 4)]]; },
  // 5 · el AVE arranca por la misma vía y se acerca
  (t, u) => { ave.visible = true; ave.position.x = lerp(-215, -165, ease(u)); setCam(lerp(-400, -340, u), 30, -20, -100, 0, 3);
    const gap = Math.max(0, (-78.8) - (ave.position.x + 17));
    const pm = proj(new THREE.Vector3((ave.position.x + 17 - 78.8) / 2, 7, 0));
    return [['pill', pm[0], pm[1], 'MISMA VÍA', clamp((u - 0.2) * 4), CSS_RED]]; },   // sin distancias inventadas
  // 6 · el alcance: reconstrucción esquemática, a cámara lenta y sin dramatismo
  (t, u) => { ave.visible = true; const cs = iryo.userData.cars;
    const hit = 0.42;
    ave.position.x = u < hit ? lerp(-165, -95.8, ease(u / hit) * 0.5 + (u / hit) * 0.5) : -95.8 + Math.min(1, (u - hit) / 0.2) * -1.2;
    const d = ease(clamp((u - hit) / 0.4));
    cs[3].position.z = 5.2 * d; cs[3].rotation.set(0.25 * d, 0.16 * d, 0); cs[3].position.y = -0.4 * d; cs[3].position.x = -61.8 + 2.5 * d;
    cs[2].position.z = 2.4 * clamp((u - hit - 0.05) / 0.4); cs[2].rotation.set(0.12 * d, 0.08 * d, 0);
    ave.userData.cars[0].rotation.x = 0.03 * d;
    setCam(-150, 15, -17, -72, 1, 3); DIM = 0.15 + 0.25 * d;
    return [['clock', '8:54', 'ALCANCE', clamp((u - hit + 0.05) * 6)]]; },
  // 7 · las víctimas
  (t, u) => { iryo.visible = false; setCam(-20, 3, 18, 60, 2, 3); DIM = 0.8;
    return [['bignum', '68', 'FALLECIDOS', clamp(u * 3)], ['pill', W / 2, 760, '≈540 VIAJEROS · MÁS DE 100 HERIDOS', clamp((u - 0.45) * 4)]]; },
  // 8 · la investigación
  (t, u) => { iryo.visible = false; tape.visible = true; setCam(14, 2.2, 10, 31, 1.2, 3); return [['pill', W / 2, 420, 'INVESTIGA UN JUZGADO DE ORGAZ', clamp((u - 0.2) * 4)]]; },
  // 9 · luto oficial y línea cortada
  (t, u) => { iryo.visible = false; flag.visible = true; tape.visible = true; const cl = flag.userData.cloth; cl.rotation.y = Math.sin(t * 1.4) * 0.15;
    setCam(-6, 4.5, 4, 8, 6, -9); return [['pill', W / 2, 330, '3 DÍAS DE LUTO OFICIAL', clamp(u * 4)], ['pill', W / 2, 400, 'LÍNEA MADRID–ANDALUCÍA CORTADA', clamp((u - 0.4) * 4), CSS_RED]]; },
  // 10 · recuerdo: velas
  (t, u) => { iryo.visible = false; candles.visible = true; sun.intensity = 0.5; DIM = 0.25;
    candles.children.forEach((c, i) => { if (c.userData.flame) c.userData.flame.scale.set(1 + Math.sin(t * 9 + i) * 0.12, 1.8 + Math.sin(t * 7 + i * 2) * 0.25, 1); });
    setCam(38.2, 1.6, -3.6, 40, 0.4, -6); return []; },
];

// ---------- piezas 2D propias de este vídeo ----------
function clockCard(txt, sub, u) {
  if (u <= 0) return; ctx.save(); ctx.globalAlpha = clamp(u * 2);
  rrect(W / 2 - 150, 300, 300, 150, 24); ctx.fillStyle = 'rgba(20,22,26,0.85)'; ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = F(800, 72); ctx.textAlign = 'center'; ctx.fillText(txt, W / 2, 390);
  ctx.fillStyle = '#c9cdd2'; ctx.font = F(700, 22); ctx.fillText(sub, W / 2, 428); ctx.restore();
}
function peopleGrid(n, u) {
  if (u <= 0) return; const cols = 30, rows = Math.ceil(n / cols), s = 17;
  ctx.save(); ctx.globalAlpha = clamp(u * 2);
  rrect(W / 2 - 280, 250, 560, 150 + rows * s, 24); ctx.fillStyle = 'rgba(255,255,255,0.9)'; ctx.fill();
  ctx.fillStyle = '#111'; ctx.font = F(800, 30); ctx.textAlign = 'center'; ctx.fillText('≈ 540 PASAJEROS', W / 2, 300);
  ctx.font = F(500, 20); ctx.fillStyle = '#555'; ctx.fillText('en los dos trenes', W / 2, 330);
  const shown = Math.floor(n * clamp(u * 1.2));
  for (let i = 0; i < shown; i++) { const cx = W / 2 - (cols * s) / 2 + (i % cols) * s + s / 2, cy = 360 + Math.floor(i / cols) * s;
    ctx.fillStyle = '#3a3d42'; ctx.beginPath(); ctx.arc(cx, cy, 3.4, 0, 7); ctx.fill(); ctx.fillRect(cx - 3.4, cy + 4, 6.8, 6); }
  ctx.restore();
}
function bigNum(num, label, u) {
  if (u <= 0) return; ctx.save(); ctx.globalAlpha = clamp(u * 1.5); ctx.textAlign = 'center';
  ctx.fillStyle = '#fff'; ctx.font = F(800, 190); ctx.fillText(num, W / 2, 560);
  ctx.font = F(800, 34); ctx.fillStyle = '#e9e9e9'; ctx.fillText(label, W / 2, 620);
  ctx.font = F(500, 20); ctx.fillStyle = '#b8bcc2'; ctx.fillText('Cifra provisional', W / 2, 660); ctx.restore();
}
function controlPanel(u) {
  const a = clamp(u * 4); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a;
  rrect(50, 420, W - 100, 330, 22); ctx.fillStyle = 'rgba(16,18,22,0.92)'; ctx.fill();
  ctx.fillStyle = '#9aa3ad'; ctx.font = F(700, 20); ctx.textAlign = 'left'; ctx.fillText('CENTRO DE CONTROL · ESQUEMA', 80, 460);
  ctx.strokeStyle = '#59626c'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(80, 590); ctx.lineTo(W - 80, 590); ctx.stroke();
  // Iryo parado delante
  rrect(W - 260, 570, 150, 40, 8); ctx.fillStyle = '#c0172d'; ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = F(800, 18); ctx.textAlign = 'center'; ctx.fillText('IRYO · PARADO', W - 185, 596);
  // AVE detrás, con vía libre
  const ax = lerp(110, 300, ease(u)); rrect(ax, 570, 120, 40, 8); ctx.fillStyle = '#e9eaee'; ctx.fill(); ctx.fillStyle = '#5b2a86'; ctx.fillText('AVE', ax + 60, 596);
  const on = Math.floor(u * 10) % 2 === 0 || u > 0.6;
  rrect(W / 2 - 130, 660, 260, 54, 12); ctx.fillStyle = on ? '#1fa85a' : '#1a3d28'; ctx.fill(); ctx.fillStyle = '#fff'; ctx.font = F(800, 22);
  ctx.fillText('MARCHA AUTORIZADA', W / 2, 695); ctx.restore();
}
function memorialCard(t, u) {
  ctx.save(); ctx.globalAlpha = clamp(u * 1.5); ctx.fillStyle = '#0d0e10'; ctx.fillRect(0, 0, W, H);
  // lazo negro con borde blanco
  ctx.translate(W / 2, 520); ctx.lineJoin = 'round'; ctx.lineWidth = 7; ctx.strokeStyle = '#f2f2f2'; ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.moveTo(0, -10); ctx.bezierCurveTo(-70, -110, -120, -20, -45, 40); ctx.lineTo(-95, 170); ctx.lineTo(-55, 160); ctx.lineTo(0, 20);
  ctx.lineTo(55, 160); ctx.lineTo(95, 170); ctx.lineTo(45, 40); ctx.bezierCurveTo(120, -20, 70, -110, 0, -10); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.setTransform(PR, 0, 0, PR, 0, 0); ctx.textAlign = 'center';
  ctx.fillStyle = '#f2f2f2'; ctx.font = F(800, 38); ctx.fillText('En memoria de las víctimas', W / 2, 780);
  ctx.fillText('de Urda (Toledo)', W / 2, 828); ctx.font = F(500, 22); ctx.fillStyle = '#9ea3a9'; ctx.fillText('28 de octubre de 2026', W / 2, 870);
  ctx.fillStyle = '#6f747a'; ctx.font = F(700, 22); ctx.fillText('@ojoaldato.ya', W / 2, 1230); ctx.restore();
}

// ---------- fotograma ----------
let T = null;
function sceneAt(t) { const n = T.lines.length; for (let i = n - 1; i >= 0; i--) if (t >= T.lines[i].start - (i ? 0.08 : 99)) return i; return 0; }
function drawUi(ui) {
  for (const it of ui) { const [k, ...a] = it;
    if (k === 'pill') pill(...a); else if (k === 'clock') clockCard(...a); else if (k === 'people') peopleGrid(...a);
    else if (k === 'bignum') bigNum(...a); else if (k === 'panel') controlPanel(...a); }
}
function render3(si, t, L, end) {
  hideAll(); setBg();
  const u = clamp((t - L.start) / Math.max(0.5, end - L.start));
  const ui = SC[si](t, u, L); camFx(t, L.start, end, si);
  gl.clear(); gl.render(scene, cam); return [ui, DIM];
}
window.renderAt = function (t) {
  T = window.TIMING;
  const outroAt = T.outro.start, inOutro = t >= outroAt - 0.1;
  ojo.visible = false; world.visible = false;
  let ui = [], si = 0, dim = 0;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.clearRect(0, 0, out.width, out.height);
  if (!inOutro) {
    si = sceneAt(t);
    const L = T.lines[si], end = si + 1 < T.lines.length ? T.lines[si + 1].start : outroAt;
    const FADE = 0.7;
    if (si > 0 && t - L.start < FADE) {
      const Lp = T.lines[si - 1]; const [, pd] = render3(si - 1, t, Lp, L.start);
      prevFrame.getContext('2d').drawImage(gl.domElement, 0, 0);
      const pctx = prevFrame.getContext('2d'); pctx.fillStyle = `rgba(8,9,11,${pd})`; pctx.fillRect(0, 0, prevFrame.width, prevFrame.height);
      prevA = 1 - ease((t - L.start) / FADE);
    } else prevA = 0;
    [ui, dim] = render3(si, t, L, end);
    ctx.drawImage(gl.domElement, 0, 0);
    if (dim > 0) { ctx.fillStyle = `rgba(8,9,11,${dim})`; ctx.fillRect(0, 0, out.width, out.height); }
    if (prevA > 0) { ctx.globalAlpha = prevA; ctx.drawImage(prevFrame, 0, 0); ctx.globalAlpha = 1; }
    ctx.setTransform(PR, 0, 0, PR, 0, 0);
    drawUi(ui); captions(t, T.lines[si]);
  } else {
    ctx.setTransform(PR, 0, 0, PR, 0, 0);
    memorialCard(t, clamp((t - outroAt) / 1.0)); captions(t, T.outro, 1000);
  }
  return out.toDataURL('image/jpeg', 0.97);
};
Promise.all(['800 40px Inter', '700 28px Inter', '500 24px Inter'].map(f => document.fonts.load(f))).then(() => { window.READY = true; });
[iryo, ave].forEach(tr => tr.traverse(m => { if (m.isMesh) m.frustumCulled = false; }));
