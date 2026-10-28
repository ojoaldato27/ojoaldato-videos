// Ojo al dato · vídeo 3D «El rebufo en F1» (estilo C: minimal blanco con Ojo en 3D).
// Render determinista: window.renderAt(t) dibuja el fotograma del segundo t y devuelve un JPEG en dataURL.
// window.TIMING (lo pone render3d.py): {total, lines:[{start,end,tokens:[{w,key,s,e}]}], outro:{...}}
import * as THREE from 'three';
import { makeCarPro } from './car_pro.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const W = 720, H = 1280;
const RED = 0xE62828, INK = 0x111111, GREY = 0x9a9a9a;
const CSS_RED = '#E62828';

// ---------- renderer y capa 2D ----------
const gl = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
gl.setSize(W, H); gl.setPixelRatio(1);
const out = document.createElement('canvas'); out.width = W; out.height = H;
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

// ---------- escenas ----------
const HEAD = [
  ['¿Por qué van tan pegados?', 'El rebufo en la F1'],
  ['Una pared de aire', 'A más de 300 km/h'],
  ['El aire frena', 'Casi toda la potencia'],
  ['El rebufo', 'Un hueco de aire revuelto'],
  ['Dentro del rebufo', 'El aire ya no frena tanto'],
  ['Más rápido', 'Sin tocar nada'],
  ['El adelantamiento', 'En la frenada'],
  ['La trampa', 'Aire sucio en las curvas'],
  ['Menos agarre', 'Ruedas al límite'],
  ['Desde 2026', 'A menos de un segundo'],
  ['La respuesta', '¿Por qué tan pegados?'],
];
const OJO_POSE = ['think', 'point', 'push', 'surprise', 'point', 'cheer', 'surprise', 'think', 'think', 'point', 'cheer'];
const GAP_MIN = 6.2;   // morro-cola: 5 m de coche + aire; nunca se solapan en el mismo carril

const LOOK = new THREE.Vector3();
const prevFrame = document.createElement('canvas'); prevFrame.width = W; prevFrame.height = H; let prevA = 0;
function setBg(si) {
  // fondo de color por escena, como en el vídeo del agujero (window.BGMODE = 'color'), o blanco
  if (typeof CIRCUIT !== 'undefined' && CIRCUIT) { scene.background = TEX.sky; return; }
  if (window.BGMODE === 'color') {
    const P = [[0xFFE2B0, 0xF2C98A], [0xCFE6FF, 0xA9CBEA], [0xFFD2B5, 0xF0B48E], [0xFFF0A6, 0xEBD677], [0xD9F0CF, 0xB5DCA6],
               [0xFFE2B0, 0xF2C98A], [0xCFE6FF, 0xA9CBEA], [0xFFD2B5, 0xF0B48E], [0xFFF0A6, 0xEBD677], [0xD9F0CF, 0xB5DCA6], [0xFFE2B0, 0xF2C98A]][si];
    scene.background.setHex(P[0]); ground.material.color.setHex(P[1]);
  } else { scene.background.setHex(0xffffff); ground.material.color.setHex(0xffffff); }
}
function setCam(px, py, pz, lx, ly, lz, up) { cam.up.set(...(up || [0, 1, 0])); cam.position.set(px, py, pz); LOOK.set(lx, ly, lz); cam.fov = 38; cam.updateProjectionMatrix(); cam.lookAt(lx, ly, lz); cam.updateMatrixWorld(); }
// Iker (28/10): «más dinámico y enérgico, sin cortes secos» → la cámara nunca está quieta y los cambios de escena
// son un zoom continuo: la escena acaba acercándose a un detalle y la siguiente empieza pegada a otro y se abre.
function camFx(t, t0, t1, si, keyTimes) {
  const dur = Math.max(0.6, t1 - t0), k = clamp((t - t0) / dur);
  const P = cam.position.clone(), D = LOOK.clone().sub(P);
  let f = 0.06 * ease(k);                                   // empuje lento durante toda la escena
  const tin = t - t0, tout = Math.max(0, t1 - t);
  let roll = 0, fov = 38;
  // Iker (28/10): «demasiados zooms rápidos» → zoom de entrada/salida más corto de recorrido y más largo de tiempo,
  // con fundido entre las dos escenas (ver renderAt), sin golpes de cámara.
  if (si > 0 && tin < 1.3) { const a = 1 - ease(tin / 1.3); f += 0.28 * a; fov -= 3 * a; }
  if (tout < 1.0) { const a = ease(1 - tout / 1.0); f += 0.24 * a; fov -= 2 * a; }
  const kick = 0;
  const sw = 0.006 * D.length();
  P.add(D.multiplyScalar(f));
  P.x += Math.sin(t * 0.9) * sw * 0.5;
  P.y += Math.sin(t * 1.1 + 1) * sw * 0.3;
  cam.position.copy(P); cam.fov = fov - 3 * kick; cam.updateProjectionMatrix();
  cam.lookAt(LOOK); cam.rotateZ(roll); cam.updateMatrixWorld();
}
function hideAll() {
  wakeCone.visible = false; arrows.forEach(a => a.visible = false); air.visible = false;
  straight.visible = true; curve.visible = false; carB.visible = true; carA.visible = true;
  heatWheels(carB, 0);
}
// a la curva: coche en el ángulo a (rad) del semicírculo, con su carril (r)
function onCurve(car, a, r = CURVE_R, slide = 0) {
  const x = Math.cos(a) * r, z = -Math.sin(a) * r;
  car.position.set(x, 0, z); car.rotation.y = a + Math.PI / 2 + slide;
  car.userData.wheels.forEach(w => { w.rotation.y = 0.25; });
}

const SC = [
  // 0 · gancho: dos coches en fila, cámara baja detrás
  (t, u, L) => {
    const s = t * 85; scrollTrack(s);
    placeCar(carA, 0, 0, 0, 0); placeCar(carB, -GAP_MIN - 1.2 + Math.sin(t * 1.5) * 0.4, 0, 0, 0);
    const k = ease(u);
    setCam(lerp(-28, -19, k), lerp(4.5, 3.2, k), lerp(2.5, 1.2, k), -2, 0.3, -0.6);
    return [];
  },
  // 1 · pared de aire: lateral, solo el rojo
  (t, u) => {
    scrollTrack(t * 18); carB.visible = false;
    placeCar(carA, 0, 0); air.visible = true; airflow(t, 0, 0, 0.75, 0);
    setCam(lerp(4, 1, ease(u)), 3.2, 15, 0, 1, 0);
    return [['pill', W / 2, 330, '300 KM/H', clamp((u - 0.15) * 4)]];
  },
  // 2 · el aire frena: más cerca, barra de potencia
  (t, u) => {
    scrollTrack(t * 18); carB.visible = false;
    placeCar(carA, 0, 0); air.visible = true; airflow(t, 0, 0, 1, 0);
    setCam(5, 2.4, 9.5, 0.5, 0.8, 0);
    return [['meter', 150, 300, lerp(0, 0.8, ease((u - 0.2) * 1.6)), 'POTENCIA PARA APARTAR EL AIRE', clamp((u - 0.1) * 4)]];
  },
  // 3 · el rebufo: desde arriba, cono rojo
  (t, u) => {
    scrollTrack(t * 18); carB.visible = false;
    placeCar(carA, 4, 0); air.visible = true; airflow(t, 4, 0, 1, ease(u * 2));
    wakeCone.visible = true; wakeCone.position.set(4 - 2.6 - 8, 0.9, 0); wakeCone.material.opacity = 0.14 * ease(u * 2);
    setCam(lerp(0, -2, u), 40, 0.01, lerp(0, -2, u), 0, 0, [1, 0, 0]);
    return [['pill', W / 2, 250, 'REBUFO', clamp((u - 0.3) * 4), CSS_RED]];
  },
  // 4 · se mete en el rebufo: el negro entra desde el otro carril y se coloca detrás
  (t, u) => {
    scrollTrack(t * 18);
    const k = ease(u * 1.3);
    placeCar(carA, 4, 0); placeCar(carB, 4 - GAP_MIN - 4, lerp(3.4, 0, k), lerp(0.18, 0, ease(u * 1.3 + 0.2)) * (k < 1 ? 1 : 0));
    air.visible = true; airflow(t, 4, 0, 1, 1);
    wakeCone.visible = true; wakeCone.position.set(4 - 2.6 - 8, 0.9, 0); wakeCone.material.opacity = 0.12;
    setCam(-3, 40, 0.01, -3, 0, 0, [1, 0, 0]);
    return [['pill', W / 2, 250, 'MENOS AIRE EN CONTRA', clamp((u - 0.45) * 4)]];
  },
  // 5 · más rápido: vista de persecución, velocímetro, el hueco se cierra hasta el mínimo
  (t, u) => {
    scrollTrack(t * 18);
    placeCar(carA, 0, 0); placeCar(carB, -lerp(GAP_MIN + 4, GAP_MIN, ease(u)), 0);
    setCam(-27, 4.5, 1.6, -3, 0.2, -0.8);
    return [['gauge', W / 2, 400, lerp(300, 310, ease((u - 0.25) * 1.6)), clamp((u - 0.05) * 4)],
            ['pill', W / 2, 560, '+10 KM/H', clamp((u - 0.55) * 4), CSS_RED]];
  },
  // 6 · adelanta en la frenada: sale al otro carril (3 m de lado) y pasa
  (t, u) => {
    scrollTrack(t * 18);
    const side = ease(u * 2.2), pass = ease((u - 0.35) * 1.6);
    placeCar(carA, 0, 0); placeCar(carB, lerp(-GAP_MIN, GAP_MIN + 1.5, pass), lerp(0, -3.2, side), side < 1 ? -0.12 * Math.sin(side * Math.PI) : 0);
    setCam(lerp(-30, -24, ease(u)), 21, -1.6, 3, 0, -1.6);
    return [['pill', W / 2, 330, '¡ADELANTA!', clamp((u - 0.55) * 4), CSS_RED]];
  },
  // 7 · la trampa: curva vista desde arriba, aire sucio rojo sobre el negro, pierde carga
  (t, u) => {
    straight.visible = false; curve.visible = true;
    const a0 = lerp(0.35, 1.5, u);
    onCurve(carA, a0 + 0.31); onCurve(carB, a0);
    air.visible = true; airflow(t, carA.position.x, carA.position.z, 0.9, 1, carA.rotation.y);
    setArrows(carA, 0, 1.4); setArrows(carB, 3, lerp(1.4, 0.45, ease((u - 0.3) * 2)));
    const c = new THREE.Vector3(Math.cos(a0) * 30, 0, -Math.sin(a0) * 30);
    const m = carA.position.clone().add(carB.position).multiplyScalar(0.5);
    setCam(m.x * 0.7, 30, m.z * 0.7 + 14, m.x, 0, m.z + 3);
    return [['pill', W / 2, 330, 'AIRE SUCIO', clamp((u - 0.15) * 4), CSS_RED],
            ['pill', W / 2, 400, 'MENOS CARGA', clamp((u - 0.55) * 4)]];
  },
  // 8 · menos agarre: más cerca, el negro se va un poco abierto y las ruedas se calientan
  (t, u) => {
    straight.visible = false; curve.visible = true;
    const a0 = lerp(1.6, 2.5, u);
    const slip = Math.sin(clamp((u - 0.25) * 2) * Math.PI) * 0.15;
    onCurve(carA, a0 + 0.31); onCurve(carB, a0, CURVE_R + slip * 14, slip);
    heatWheels(carB, ease((u - 0.2) * 1.8));
    air.visible = true; airflow(t, carA.position.x, carA.position.z, 0.7, 1, carA.rotation.y);
    const c = carB.position;
    setCam(c.x * 1.45, 24, c.z * 1.45 + 6, c.x, 0, c.z);
    const p = proj(new THREE.Vector3(c.x, 1.2, c.z));
    return [['pill', p[0], p[1] - 110, 'RUEDAS CALIENTES', clamp((u - 0.45) * 4), CSS_RED]];
  },
  // 9 · 2026: a menos de 1 s, extra de energía
  (t, u) => {
    scrollTrack(t * 18);
    placeCar(carA, 0, 0); placeCar(carB, -GAP_MIN - 0.6, 0);
    setCam(-3.5, 9, 22, -3.2, 0.4, 0);
    const pa = proj(new THREE.Vector3(-2.8, 1.5, 0)), pb = proj(new THREE.Vector3(-GAP_MIN - 0.6 + 2.8, 1.5, 0));
    const pc = proj(new THREE.Vector3(-GAP_MIN - 0.6, 2.4, 0));
    return [['gap', pb, pa, '< 1 s', clamp((u - 0.15) * 4)],
            ['bolt', pc[0], pc[1] - 40, 1.6 + Math.sin(t * 10) * 0.08, clamp((u - 0.45) * 4)],
            ['pill', W / 2, 330, '+ ENERGÍA ELÉCTRICA', clamp((u - 0.5) * 4), CSS_RED]];
  },
  // 10 · respuesta: plano que gira alrededor de los dos en fila
  (t, u) => {
    scrollTrack(t * 18);
    placeCar(carA, 0, 0); placeCar(carB, -GAP_MIN - 0.4, 0);
    air.visible = true; airflow(t, 0, 0, 0.8, 1);
    const a = lerp(-0.9, 0.5, ease(u));
    setCam(-3 + Math.sin(a) * 22, 7, Math.cos(a) * 22, -3, 0.4, 0);
    return [['pill', W / 2, 330, 'VELOCIDAD GRATIS', clamp((u - 0.5) * 4), CSS_RED]];
  },
];

// ---------- fotograma ----------
let T = null;
function sceneAt(t) {
  const n = T.lines.length;
  for (let i = n - 1; i >= 0; i--) if (t >= T.lines[i].start - (i ? 0.08 : 99)) return i;
  return 0;
}
window.renderAt = function (t) {
  T = window.TIMING;
  const outroAt = T.outro.start;
  const inOutro = t >= outroAt - 0.1;
  hideAll();
  let ui = [], si = 0, u = 0;
  // Ojo en la esquina (abajo a la izquierda, hueco reservado)
  ojo.position.set(-1.0, -1.47, -7.5); ojo.scale.setScalar(0.19); ojo.visible = false; world.visible = true;
  if (!inOutro) {
    si = sceneAt(t);
    const L = T.lines[si], end = si + 1 < T.lines.length ? T.lines[si + 1].start : outroAt;
    const FADE = 0.55;   // Iker (28/10): «aún más suaves»
    if (si > 0 && t - L.start < FADE) {           // la escena anterior, ya acercándose a su detalle
      const Lp = T.lines[si - 1];
      hideAll(); setBg(si - 1);
      SC[si - 1](t, 1, Lp); camFx(t, Lp.start, L.start, si - 1, []);
      carMode(); shadowCatcher.visible = true;
      gl.clear(); gl.render(scene, cam);
      prevFrame.getContext('2d').drawImage(gl.domElement, 0, 0); prevA = 1 - ease((t - L.start) / FADE);
      hideAll();
    } else prevA = 0;
    setBg(si);
    u = clamp((t - L.start) / Math.max(0.5, end - L.start));
    ui = SC[si](t, u, L);
    camFx(t, L.start, end, si, []);
    const sinceCut = t - L.start;
    poseOjo(OJO_POSE[si], OJO_POSE[si - 1] || 'idle', clamp(sinceCut / 0.35), t);
  } else {
    // cierre: Ojo al centro, saludando
    const uo = clamp((t - outroAt) / 0.6);
    straight.visible = false; carA.visible = carB.visible = false;
    world.visible = false; ojo.position.set(lerp(-1.0, 0, ease(uo)), lerp(-1.47, -1.3, ease(uo)), -7.5); ojo.scale.setScalar(lerp(0.19, 0.42, ease(uo))); ojo.visible = false;
    setCam(0, 0, 10, 0, 0, 0);
    poseOjo('wave', 'cheer', uo, t);
  }
  carMode(); shadowCatcher.visible = world.visible;
  gl.clear(); gl.render(scene, cam); gl.clearDepth(); gl.render(ojoScene, ojoCam);
  ctx.globalAlpha = 1; ctx.clearRect(0, 0, W, H); ctx.drawImage(gl.domElement, 0, 0);
  if (prevA > 0 && !inOutro) { ctx.globalAlpha = prevA; ctx.drawImage(prevFrame, 0, 0); ctx.globalAlpha = 1; }
  for (const it of ui) {
    const [kind, ...a] = it;
    if (kind === 'pill') pill(...a);
    else if (kind === 'gauge') gauge(...a);
    else if (kind === 'meter') meter(a[0], a[1], a[2], a[3], a[4]);
    else if (kind === 'bolt') bolt(...a);
    else if (kind === 'gap') gapMarker(...a);
  }
  if (!inOutro) {
    captions(t, T.lines[si]);
  } else {
    outroCard(t, clamp((t - outroAt) / 1.2));
    captions(t, T.outro, 380);
  }
  banner(clamp((t - T.notif) / 3.2));
  // corte: destello blanco o barra roja, alternando
  const cuts = T.lines.slice(1).map(l => l.start).concat([outroAt]);
  cuts.forEach((c, i) => {
    const d = t - c;
    if (false) {
      const a = 1 - Math.abs(d) / (d < 0 ? 0.12 : 0.16);
      if (i % 2 === 0) { ctx.fillStyle = `rgba(255,255,255,${a * 0.9})`; ctx.fillRect(0, 0, W, H); }
      else { const x = lerp(-W * 0.3, W * 1.3, (d + 0.12) / 0.28); ctx.fillStyle = CSS_RED; ctx.fillRect(x - 60, 0, 120, H); }
    }
  });
  return out.toDataURL('image/jpeg', 0.93);
};
Promise.all(['800 40px Inter', '700 28px Inter', '500 24px Inter'].map(f => document.fonts.load(f))).then(() => { window.READY = true; });

// foto de estudio del coche (para revisar el modelo): window.studio(px,py,pz, lx,ly,lz)
window.studio = function (px, py, pz, lx, ly, lz) {
  T = window.TIMING; hideAll(); straight.visible = true; carB.visible = false; air.visible = false; ojo.visible = false;
  setBg(1);
  placeCar(carA, 0, 0); carMode(); setCam(px, py, pz, lx, ly, lz);
  gl.clear(); gl.render(scene, cam);
  return gl.domElement.toDataURL('image/jpeg', 0.93);
};
