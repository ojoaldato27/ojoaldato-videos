// Prueba 3D «Dedos arrugados» (Iker 06/11: «muy planos en 2D, haz un ejemplo corto en 3D y más animado»).
// Render determinista: window.renderAt(t) dibuja el fotograma del segundo t y devuelve un JPEG en dataURL.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const W = 720, H = 1280;
const gl = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
gl.setPixelRatio(1); gl.setSize(W, H);
gl.toneMapping = THREE.ACESFilmicToneMapping; gl.toneMappingExposure = 1.05;
gl.outputColorSpace = THREE.SRGBColorSpace;
gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(gl.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xcfe6ee);
scene.fog = new THREE.Fog(0xcfe6ee, 9, 22);
const pm = new THREE.PMREMGenerator(gl);
scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
const cam = new THREE.PerspectiveCamera(42, W / H, 0.05, 60);

// ---------- luces
scene.add(new THREE.HemisphereLight(0xffffff, 0x8fb4c4, 0.9));
const sun = new THREE.DirectionalLight(0xfff2dd, 2.4);
sun.position.set(3, 7, 4); sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
Object.assign(sun.shadow.camera, { left: -4, right: 4, top: 5, bottom: -3, near: 1, far: 20 });
scene.add(sun);
const rim = new THREE.DirectionalLight(0x9fd8ff, 1.2); rim.position.set(-4, 3, -3); scene.add(rim);

// ---------- baño: pared de azulejos, suelo y bañera
function tileTex() {
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const x = c.getContext('2d');
  x.fillStyle = '#b7d3dc'; x.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) {
    x.fillStyle = (i + j) % 2 ? '#eef6f8' : '#e2eff3';
    x.fillRect(i * 64 + 3, j * 64 + 3, 58, 58);
    x.fillStyle = 'rgba(255,255,255,.55)'; x.fillRect(i * 64 + 8, j * 64 + 8, 18, 5);
  }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(10, 6);
  t.colorSpace = THREE.SRGBColorSpace; return t;
}
const wall = new THREE.Mesh(new THREE.PlaneGeometry(30, 18), new THREE.MeshStandardMaterial({ map: tileTex(), roughness: 0.35 }));
wall.position.set(0, 6, -4.2); wall.receiveShadow = true; scene.add(wall);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), new THREE.MeshStandardMaterial({ color: 0xb08a6a, roughness: 0.7 }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -1.3; floor.receiveShadow = true; scene.add(floor);

const porcelain = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.15, clearcoat: 1, clearcoatRoughness: 0.08 });
const tubOuter = new THREE.Mesh(new RoundedBoxGeometry(7.4, 1.6, 4.6, 6, 0.6), porcelain);
tubOuter.position.set(0, -0.55, -1.0); tubOuter.castShadow = tubOuter.receiveShadow = true; scene.add(tubOuter);
// borde: un anillo redondeado por encima del agua
const rimShape = new THREE.Shape(); rimShape.absarc(0, 0, 1, 0, Math.PI * 2);
const rimGeo = new THREE.TorusGeometry(1, 0.16, 16, 80); rimGeo.scale(3.45, 2.1, 1);
const rimM = new THREE.Mesh(rimGeo, porcelain); rimM.rotation.x = -Math.PI / 2; rimM.position.set(0, 0.25, -1.0); rimM.castShadow = true; scene.add(rimM);
// grifo
const metal = new THREE.MeshStandardMaterial({ color: 0xdfe6ea, metalness: 1, roughness: 0.18 });
const tap = new THREE.Mesh(new THREE.TorusGeometry(0.35, 0.08, 12, 30, Math.PI), metal);
tap.position.set(-2.6, 0.75, -2.9); tap.rotation.y = Math.PI / 2; scene.add(tap);

// ---------- agua (se deforma cada fotograma: olas + ondas que salen de la mano)
const WSEG = 140;
const waterGeo = new THREE.PlaneGeometry(6.6, 3.8, WSEG, WSEG); waterGeo.rotateX(-Math.PI / 2);
const water = new THREE.Mesh(waterGeo, new THREE.MeshPhysicalMaterial({
  color: 0x5bb6e6, roughness: 0.04, metalness: 0.0, transparent: true, opacity: 0.82, clearcoat: 1, clearcoatRoughness: 0.03, envMapIntensity: 1.4
}));
water.position.set(0, 0.05, -1.0); water.receiveShadow = true; scene.add(water);
const wBase = waterGeo.attributes.position.array.slice();

// espuma: bolitas blancas en el borde
const foam = new THREE.InstancedMesh(new THREE.SphereGeometry(0.11, 12, 10), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 }), 160);
scene.add(foam);
const foamPos = [];
for (let i = 0; i < 160; i++) {
  const a = (i / 160) * Math.PI * 2 + (i % 3) * 0.03;
  const r = 0.92 + 0.07 * Math.sin(i * 7.1);
  foamPos.push([Math.cos(a) * 3.2 * r, Math.sin(a) * 1.85 * r - 1.0, 0.6 + 0.6 * ((i * 37) % 10) / 10]);
}

// ---------- mano (dedos = cápsulas que se deforman en las yemas)
const skin = new THREE.MeshPhysicalMaterial({ color: 0xf0c09c, roughness: 0.48, clearcoat: 0.35, clearcoatRoughness: 0.35, sheen: 0.5, sheenColor: new THREE.Color(0xffd0c0) });
const hand = new THREE.Group(); scene.add(hand);
const palm = new THREE.Mesh(new RoundedBoxGeometry(1.05, 1.15, 0.42, 6, 0.2), skin);
palm.position.y = 0.85; palm.castShadow = true; hand.add(palm);
const wrist = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.42, 1.6, 32), skin);
wrist.position.y = -0.2; wrist.castShadow = true; hand.add(wrist);
const fingers = [];
const FDEF = [[-0.39, 0.62, -0.10], [-0.13, 0.75, -0.03], [0.13, 0.71, 0.03], [0.39, 0.55, 0.10]];
function makeFinger(len, rad) {
  const g = new THREE.CapsuleGeometry(rad, len, 10, 40);
  const base = g.attributes.position.array.slice();
  const m = new THREE.Mesh(g, skin); m.castShadow = true;
  return { m, g, base, len, rad };
}
FDEF.forEach(([x, len, ang]) => {
  const f = makeFinger(len, 0.12);
  f.m.position.set(x, 1.4 + len / 2 + 0.05, 0); f.m.rotation.z = -ang;
  hand.add(f.m); fingers.push(f);
});
const thumb = makeFinger(0.5, 0.13);
thumb.m.position.set(-0.62, 0.95, 0.08); thumb.m.rotation.z = 0.85; hand.add(thumb.m); fingers.push(thumb);
// uñas
const nailM = new THREE.MeshPhysicalMaterial({ color: 0xffe0d6, roughness: 0.2, clearcoat: 1 });
fingers.forEach(f => {
  const n = new THREE.Mesh(new THREE.SphereGeometry(f.rad * 0.78, 16, 10), nailM);
  n.scale.set(1, 1.25, 0.35); n.position.set(0, f.len / 2 + f.rad * 0.35, f.rad * 0.72); f.m.add(n);
});

function wrinkle(f, k, t) {
  const p = f.g.attributes.position.array, b = f.base;
  const top = f.len / 2 + f.rad;
  for (let i = 0; i < p.length; i += 3) {
    const x = b[i], y = b[i + 1], z = b[i + 2];
    const u = (y - (f.len / 2 - 0.22)) / (top - (f.len / 2 - 0.22));      // 0..1 zona de la yema
    let s = 1;
    if (u > 0 && k > 0) {
      const mask = Math.min(1, u * 2) * (1 - Math.max(0, (u - 0.92) / 0.08));
      const ang = Math.atan2(z, x);
      const ridge = Math.sin(y * 95 + Math.sin(ang * 3 + y * 20) * 1.6);
      s = 1 + 0.085 * k * mask * ridge - 0.05 * k * mask;
    }
    p[i] = x * s; p[i + 1] = y; p[i + 2] = z * s;
  }
  f.g.attributes.position.needsUpdate = true; f.g.computeVertexNormals();
}

// ---------- cerebro 3D que manda la orden
const brainGeo = new THREE.SphereGeometry(0.62, 96, 64);
const bb = brainGeo.attributes.position.array;
for (let i = 0; i < bb.length; i += 3) {
  const x = bb[i], y = bb[i + 1], z = bb[i + 2];
  const n = 1 + 0.07 * Math.sin(x * 22 + Math.sin(y * 9) * 3) * Math.cos(z * 19 + y * 7) + 0.04 * Math.sin(y * 31 + x * 5);
  const gap = Math.abs(x) < 0.05 ? 0.9 : 1;
  bb[i] = x * 1.25 * n * gap; bb[i + 1] = y * 0.95 * n; bb[i + 2] = z * 1.1 * n;
}
brainGeo.computeVertexNormals();
const brainMat = new THREE.MeshPhysicalMaterial({ color: 0xf29bb0, roughness: 0.35, clearcoat: 0.6, emissive: 0xff5577, emissiveIntensity: 0 });
const brain = new THREE.Mesh(brainGeo, brainMat); brain.castShadow = true; scene.add(brain);
const brainLight = new THREE.PointLight(0xff7799, 0, 6); scene.add(brainLight);

const sparkMat = new THREE.MeshBasicMaterial({ color: 0xfff27a });
const sparks = []; for (let i = 0; i < 7; i++) { const s = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 8), sparkMat); scene.add(s); sparks.push(s); }
const sparkGlow = new THREE.PointLight(0xffe066, 0, 3); scene.add(sparkGlow);
let nerveMesh = null;
const nerveMat = new THREE.MeshBasicMaterial({ color: 0xffd23c, transparent: true, opacity: 0.0 });

// ---------- gotas que caen de las yemas
const drops = []; const dropMat = new THREE.MeshPhysicalMaterial({ color: 0xbfe6ff, roughness: 0, transmission: 0, transparent: true, opacity: 0.85, clearcoat: 1 });
for (let i = 0; i < 10; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.05, 14, 10), dropMat); d.scale.set(1, 1.35, 1); scene.add(d); drops.push(d); }

// ---------- patito y pasa
const duck = new THREE.Group(); scene.add(duck);
const yel = new THREE.MeshPhysicalMaterial({ color: 0xffcc22, roughness: 0.3, clearcoat: 1 });
const db = new THREE.Mesh(new THREE.SphereGeometry(0.42, 32, 20), yel); db.scale.set(1.3, 0.8, 1); duck.add(db);
const dh = new THREE.Mesh(new THREE.SphereGeometry(0.27, 32, 20), yel); dh.position.set(0.35, 0.42, 0); duck.add(dh);
const beak = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.25, 16), new THREE.MeshStandardMaterial({ color: 0xff7a1a })); beak.rotation.z = -Math.PI / 2; beak.position.set(0.66, 0.4, 0); duck.add(beak);
[-0.12, 0.12].forEach(zz => { const e = new THREE.Mesh(new THREE.SphereGeometry(0.04, 10, 8), new THREE.MeshBasicMaterial({ color: 0x111111 })); e.position.set(0.52, 0.52, zz); duck.add(e); });
duck.traverse(o => o.castShadow = true);

const raisinGeo = new THREE.SphereGeometry(0.42, 96, 64);
const rr = raisinGeo.attributes.position.array;
for (let i = 0; i < rr.length; i += 3) {
  const x = rr[i], y = rr[i + 1], z = rr[i + 2];
  const n = 1 + 0.11 * Math.sin(x * 26 + Math.cos(z * 13) * 2) * Math.sin(y * 21 + x * 6) + 0.05 * Math.sin(z * 37);
  rr[i] = x * n; rr[i + 1] = y * 0.8 * n; rr[i + 2] = z * n;
}
raisinGeo.computeVertexNormals();
const raisin = new THREE.Mesh(raisinGeo, new THREE.MeshPhysicalMaterial({ color: 0x5a2a36, roughness: 0.45, clearcoat: 0.6 }));
raisin.castShadow = true; scene.add(raisin);

// ---------- utilidades
const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
const clamp = x => Math.max(0, Math.min(1, x));
const lerp = (a, b, k) => a + (b - a) * k;
const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
const tipWorld = (f) => { f.m.updateWorldMatrix(true, false); return v3(0, f.len / 2 + f.rad, 0).applyMatrix4(f.m.matrixWorld); };
const pop = k => k <= 0 ? 0 : k >= 1 ? 1 : 1 + 2.7 * Math.pow(k - 1, 3) + 1.7 * Math.pow(k - 1, 2);

// cámara: posiciones clave (t, pos, mirar)
const CAMK = [
  [0.0, v3(1.6, 0.9, 3.7), v3(0.0, 1.55, -1.0)],
  [2.0, v3(0.9, 1.5, 3.3), v3(0.25, 1.9, -1.0)],
  [4.3, v3(-0.5, 1.7, 3.0), v3(0.2, 1.9, -1.0)],
  [5.3, v3(-2.6, 3.4, 5.2), v3(0.0, 0.8, -1.0)],
  [6.5, v3(-0.4, 2.7, 1.5), v3(0.0, 2.35, -1.0)],
  [8.6, v3(0.25, 2.65, 0.75), v3(0.3, 2.45, -1.0)],
];
function camAt(t) {
  let i = 0; while (i < CAMK.length - 2 && t > CAMK[i + 1][0]) i++;
  const [t0, p0, l0] = CAMK[i], [t1, p1, l1] = CAMK[i + 1];
  const k = ease(clamp((t - t0) / (t1 - t0)));
  cam.position.copy(p0).lerp(p1, k); const look = l0.clone().lerp(l1, k);
  cam.position.y += 0.03 * Math.sin(t * 1.7); cam.lookAt(look);
}

window.renderAt = function (t) {
  // mano que sale del agua
  const rise = ease(clamp(t / 0.9));
  hand.position.set(0, lerp(-1.4, -0.05, rise) + 0.03 * Math.sin(t * 1.3), -1.0);
  hand.rotation.set(0.05 * Math.sin(t * 0.8), -0.25 + 0.12 * Math.sin(t * 0.5), 0.04 * Math.sin(t * 1.1));
  // el cerebro aparece a los 2,3 s; los impulsos llegan y las arrugas se disparan
  const bk = pop(clamp((t - 2.3) / 0.5));
  brain.visible = bk > 0.01; brain.scale.setScalar(Math.max(0.01, bk));
  brain.position.set(1.35, 3.05 + 0.06 * Math.sin(t * 2), -1.2); brain.rotation.y = t * 0.6;
  brainMat.emissiveIntensity = bk * (0.25 + 0.25 * Math.sin(t * 10));
  brainLight.position.copy(brain.position); brainLight.intensity = 3 * bk;
  const arrive = 2.9;
  const wr = clamp(0.12 + 0.18 * ease(clamp(t / 2.5)) + 0.75 * ease(clamp((t - arrive) / 1.4)));
  fingers.forEach((f, i) => wrinkle(f, wr * (i === 4 ? 0.8 : 1), t));
  // nervio y chispas del cerebro a la yema del dedo corazón
  const tip = tipWorld(fingers[1]);
  if (bk > 0.3) {
    const curve = new THREE.CatmullRomCurve3([brain.position.clone().add(v3(-0.3, -0.4, 0)), v3(1.1, 2.7, -0.6), v3(0.5, 2.7, -0.8), tip]);
    if (nerveMesh) { nerveMesh.geometry.dispose(); scene.remove(nerveMesh); }
    nerveMesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 60, 0.012, 6), nerveMat); scene.add(nerveMesh);
    nerveMat.opacity = 0.55 * clamp((t - 2.6) / 0.3) * (t < 4.4 ? 1 : clamp((5.0 - t) / 0.6));
    sparks.forEach((s, i) => {
      const u = ((t - 2.6) * 0.9 + i / sparks.length) % 1;
      s.visible = t > 2.6 && t < 5.0; s.position.copy(curve.getPointAt(Math.max(0, u)));
      s.scale.setScalar(0.7 + 0.5 * Math.sin(t * 20 + i));
    });
    sparkGlow.position.copy(sparks[0].position); sparkGlow.intensity = (t > 2.6 && t < 5.0) ? 2.5 : 0;
  } else { sparks.forEach(s => s.visible = false); sparkGlow.intensity = 0; }
  // agua
  const p = waterGeo.attributes.position.array;
  const hx = 0, hz = 0;
  for (let i = 0; i < p.length; i += 3) {
    const x = wBase[i], z = wBase[i + 2];
    const d = Math.hypot(x - hx, z - hz);
    const ring = Math.sin(d * 9 - t * 7) * Math.exp(-d * 0.9) * 0.05 * (0.4 + rise);
    p[i + 1] = 0.025 * Math.sin(x * 2.3 + t * 1.5) + 0.02 * Math.sin(z * 3.1 - t * 1.9) + ring;
  }
  waterGeo.attributes.position.needsUpdate = true; waterGeo.computeVertexNormals();
  // espuma
  const m4 = new THREE.Matrix4();
  foamPos.forEach(([x, z, s], i) => { m4.makeScale(s, s * 0.7, s); m4.setPosition(x, 0.12 + 0.02 * Math.sin(t * 2 + i), z); foam.setMatrixAt(i, m4); });
  foam.instanceMatrix.needsUpdate = true;
  // gotas
  drops.forEach((d, i) => {
    const f = fingers[i % 4]; const tp = tipWorld(f);
    const per = 0.9 + (i % 3) * 0.17, ph = ((t + i * 0.31) % per) / per;
    d.position.set(tp.x + 0.02 * Math.sin(i), tp.y - 0.05 - 2.6 * ph * ph, tp.z + 0.06);
    d.visible = t > 0.6 && d.position.y > 0.05;
  });
  // patito
  duck.position.set(-1.9 + 0.25 * Math.sin(t * 0.6), 0.18 + 0.05 * Math.sin(t * 2.3), -0.2);
  duck.rotation.set(0.08 * Math.sin(t * 2.1), 0.6 + 0.3 * Math.sin(t * 0.4), 0.06 * Math.sin(t * 1.7));
  // la pasa aparece al lado de la yema al decir «pasas»
  const rk = pop(clamp((t - 7.3) / 0.45));
  raisin.visible = rk > 0.01; raisin.scale.setScalar(Math.max(0.01, rk) * 0.55);
  raisin.position.set(tip.x + 0.55, tip.y - 0.05 + 0.04 * Math.sin(t * 3), tip.z); raisin.rotation.y = t * 1.2;
  camAt(t);
  gl.render(scene, cam);
  return gl.domElement.toDataURL('image/jpeg', 0.93);
};
window.READY = true;
