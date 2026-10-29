// ---------- Urda (Toledo), 28/10/2026 · tono informativo y triste (Iker, 29/10) ----------
// El choque NO se ve: la escena 3 funde a oscuro antes. Nada de colores alegres: cielo nublado, campo seco de La Mancha.
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { makeTrainPro, LIVERY } from './train_pro.js';

const LOOK_URDA = new URLSearchParams(location.search).get('look') || 'a';   // a: mañana dorada · b: día claro
const OJO_POSE = ['think', 'point', 'point', 'think', 'think', 'think', 'point', 'point', 'think', 'think', 'think'];
cam.far = 1200; cam.updateProjectionMatrix();
scene.fog = new THREE.Fog({ a: 0xf1d9b5, b: 0xd9ebf8, c: 0xf2a873 }[LOOK_URDA], 260, 1300);

// texturas
// Iker (29/10): «colores, texturas y fondo» → texturas más reales (como el circuito del F1) y dos looks a elegir
const SKYC = { a: ['#4a86c9', '#94c3e8', '#f6d9b0', '#f3b77c'], b: ['#2f7fd8', '#7fbdf0', '#cfe8fb', '#eaf5fd'], c: ['#3b3f86', '#b8669a', '#f59a5c', '#ffcf7a'] }[LOOK_URDA];
const R1 = rng(31);
const UT = {
  field: canvasTex(1024, 1024, (x, w, h) => {
    // parcelas irregulares con surcos en distintas direcciones y caminos de tierra clara entre ellas
    const P = ['#a8743f', '#c29a55', '#8f9a4c', '#b25a36', '#a3ad5c', '#cdb177', '#97683a', '#7f8f45', '#c48a4a'];
    x.fillStyle = '#d8c39a'; x.fillRect(0, 0, w, h);
    for (let gy = 0; gy < 6; gy++) for (let gx = 0; gx < 5; gx++) {
      const x0 = gx * w / 5 + 3, y0 = gy * h / 6 + 3, ww = w / 5 - 6, hh = h / 6 - 6;
      x.save(); x.beginPath(); x.moveTo(x0 + R1() * 8, y0 + R1() * 8); x.lineTo(x0 + ww - R1() * 8, y0 + R1() * 8);
      x.lineTo(x0 + ww - R1() * 8, y0 + hh - R1() * 8); x.lineTo(x0 + R1() * 8, y0 + hh - R1() * 8); x.closePath(); x.clip();
      x.fillStyle = P[(R1() * P.length) | 0]; x.fillRect(x0, y0, ww, hh);
      const ang = R1() * Math.PI; x.translate(x0 + ww / 2, y0 + hh / 2); x.rotate(ang);
      x.globalAlpha = 0.18; x.fillStyle = '#2b1c10'; for (let k = -300; k < 300; k += 5) x.fillRect(-300, k, 600, 1.6);
      x.globalAlpha = 0.10; x.fillStyle = '#fff3d6'; for (let k = -300; k < 300; k += 5) x.fillRect(-300, k + 2.5, 600, 1);
      x.restore(); }
    x.globalAlpha = 1; noise(x, w, h, 26000, ['rgba(40,25,10,0.18)', 'rgba(255,245,220,0.14)', 'rgba(70,90,30,0.12)'], 2.2);
  }, 10, 10),
  vines: canvasTex(256, 256, (x, w, h) => {   // viñedo en otoño: tierra rojiza clara y cepas verdes/amarillas en hileras
    x.fillStyle = '#c98a5a'; x.fillRect(0, 0, w, h); noise(x, w, h, 5000, ['#b97a4c', '#d89a68', '#c4845a'], 2);
    for (let i = 0; i < 8; i++) { const y = i * 32 + 16;
      x.fillStyle = 'rgba(80,40,20,0.25)'; x.fillRect(0, y + 5, w, 6);
      for (let j = 0; j < 22; j++) { const cx = j * 11.6 + 6, c = R1() < 0.35 ? '#e8c04e' : (R1() < 0.5 ? '#b8cf5e' : '#93b648');
        x.fillStyle = c; x.beginPath(); x.ellipse(cx, y, 6.5, 5, 0, 0, 7); x.fill();
        x.fillStyle = 'rgba(255,255,220,0.35)'; x.beginPath(); x.ellipse(cx - 2, y - 2, 2.5, 1.8, 0, 0, 7); x.fill(); } } }, 120, 6),
  slab: canvasTex(128, 512, (x, w, h) => { x.fillStyle = '#7d766c'; x.fillRect(0, 0, w, h); noise(x, w, h, 5000, ['#6b655c', '#8f887d', '#5c574f', '#a29b8f'], 2.5);
    for (let i = 0; i < 8; i++) { const y = i * 64 + 20; x.fillStyle = 'rgba(0,0,0,0.35)'; x.fillRect(4, y + 3, w - 8, 22); x.fillStyle = '#b9b5ae'; x.fillRect(2, y, w - 4, 20);
      x.fillStyle = 'rgba(255,255,255,0.25)'; x.fillRect(2, y, w - 4, 3); noise(x, w, 0, 0, ['#000'], 1); } }, 1, 400),
  ballast: canvasTex(256, 256, (x, w, h) => { x.fillStyle = '#7a756d'; x.fillRect(0, 0, w, h); noise(x, w, h, 14000, ['#5f5b55', '#8f8a82', '#4e4b46', '#a8a399', '#6d6258'], 3.2); }, 300, 4),
  hills: canvasTex(1024, 256, (x, w, h) => {
    const ridge = (base, amp, col, seed) => { const r = rng(seed); x.fillStyle = col; x.beginPath(); x.moveTo(0, h);
      for (let i = 0; i <= 64; i++) x.lineTo(i * w / 64, base + Math.sin(i * 0.5 + seed) * amp + (r() - 0.5) * amp * 0.6); x.lineTo(w, h); x.fill(); };
    ridge(h * 0.35, 18, LOOK_URDA === 'a' ? '#b7aea6' : '#a9b8c9', 3);   // sierra lejana, azulada por la distancia
    ridge(h * 0.55, 14, LOOK_URDA === 'a' ? '#a08a62' : '#8f9a6a', 7);   // loma cercana
    for (let i = 0; i < 9; i++) { const cx = 360 + i * 34, cy = h * 0.55 - 4 + Math.sin(i * 0.5 + 7) * 14;   // molinos blancos en la loma
      x.fillStyle = '#f7f4ee'; x.fillRect(cx - 5, cy - 22, 10, 22); x.fillStyle = '#333'; x.beginPath(); x.moveTo(cx - 6, cy - 22); x.lineTo(cx, cy - 30); x.lineTo(cx + 6, cy - 22); x.fill();
      x.strokeStyle = '#5a4433'; x.lineWidth = 1.5; for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + i; x.beginPath(); x.moveTo(cx, cy - 25); x.lineTo(cx + Math.cos(a) * 14, cy - 25 + Math.sin(a) * 14); x.stroke(); } }
  }, 3, 1),
  sky: canvasTex(512, 1024, (x, w, h) => {
    const g = x.createLinearGradient(0, 0, 0, h); g.addColorStop(0, SKYC[0]); g.addColorStop(0.5, SKYC[1]); g.addColorStop(0.82, SKYC[2]); g.addColorStop(1, SKYC[3]);
    x.fillStyle = g; x.fillRect(0, 0, w, h);
    x.filter = 'blur(10px)'; const r = rng(4);
    for (let i = 0; i < 26; i++) { const cx = r() * w, cy = h * (0.12 + r() * 0.55), rw = 40 + r() * 110;
      x.fillStyle = LOOK_URDA !== 'b' ? `rgba(255,${235 + (r() * 15) | 0},${215 + (r() * 20) | 0},${0.55 + r() * 0.3})` : `rgba(255,255,255,${0.6 + r() * 0.3})`;
      for (let k = 0; k < 5; k++) { x.beginPath(); x.ellipse(cx + (k - 2) * rw * 0.35, cy + (r() - 0.5) * 12, rw * 0.45, rw * 0.22, 0, 0, 7); x.fill(); } }
    x.filter = 'none';
  }),
};
UT.hills.wrapT = THREE.ClampToEdgeWrapping; UT.hills.transparent = true;
UT.sky.wrapS = UT.sky.wrapT = THREE.ClampToEdgeWrapping;

const rail = new THREE.Group(); scene.add(rail);
{
  const fld = new THREE.Mesh(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshStandardMaterial({ map: UT.field, roughness: 1 })); fld.rotation.x = -Math.PI / 2; fld.position.y = -3.3; rail.add(fld);
  { const sh = new THREE.Shape(); sh.moveTo(-14, -3.25); sh.lineTo(-6, 0); sh.lineTo(12, 0); sh.lineTo(20, -3.25); sh.lineTo(-14, -3.25);   // sección del terraplén (z, y)
    const eg = new THREE.ExtrudeGeometry(sh, { depth: 1600, bevelEnabled: false }); eg.rotateY(-Math.PI / 2); eg.translate(800, -0.06, 0);
    const em = new THREE.Mesh(eg, new THREE.MeshLambertMaterial({ color: 0xb39064 })); em.receiveShadow = true; rail.add(em); }
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
    const c = new THREE.Mesh(new THREE.SphereGeometry(1.6 + tr(), 8, 6), crown); c.scale.y = 0.75; c.position.set(x, 2.1 - 3, z); rail.add(c);
    const k = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.25, 1.6, 6), trunk); k.position.set(x, 0.6 - 3, z); rail.add(k);
  }
  // viñedo de verdad en 3D (Iker 29/10: «el campo y el fondo»): hileras de cepas con colores de otoño sobre tierra rojiza
  for (const z of [-44, 50]) { const v = new THREE.Mesh(new THREE.PlaneGeometry(1600, 60), new THREE.MeshLambertMaterial({ color: 0xb8794c })); v.rotation.x = -Math.PI / 2; v.position.set(0, -3.2, z); rail.add(v); }
  {
    const geo = new THREE.IcosahedronGeometry(0.75, 0); geo.scale(1.3, 0.8, 1);
    const rows = []; for (let z = 23; z < 72; z += 3.2) rows.push(z); for (let z = -17; z > -70; z -= 3.2) rows.push(z);
    const per = Math.floor(900 / 1.9), N = rows.length * per;
    const vm = new THREE.InstancedMesh(geo, new THREE.MeshLambertMaterial(), N);
    const M = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color(), rv = rng(77); let k = 0;
    const PAL = [0x9cbf4a, 0x7fa83c, 0xd9b545, 0xc98b3a, 0xb5c95a, 0xa04a2c];
    for (const z of rows) for (let i = 0; i < per; i++) {
      const sc = 0.8 + rv() * 0.5; q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), rv() * 6.3);
      M.compose(new THREE.Vector3(-650 + i * 1.9 + rv() * 0.3, 0.45 * sc - 3, z + (rv() - 0.5) * 0.3), q, new THREE.Vector3(sc, sc, sc));
      vm.setMatrixAt(k, M); vm.setColorAt(k, col.setHex(PAL[(rv() < 0.55 ? 0 : (rv() * PAL.length) | 0)]).offsetHSL(0, 0, (rv() - 0.5) * 0.08)); k++; }
    vm.instanceMatrix.needsUpdate = true; vm.instanceColor.needsUpdate = true; vm.frustumCulled = false; rail.add(vm);
  }
  const wall = new THREE.MeshLambertMaterial({ color: 0xf6f3ec }), roofM = new THREE.MeshLambertMaterial({ color: 0xc0583a });
  const hr = rng(21);
  for (let i = 0; i < 26; i++) { const x = (hr() - 0.5) * 1300, z = (hr() < 0.5 ? -1 : 1) * (90 + hr() * 300);
    const h = new THREE.Mesh(new THREE.BoxGeometry(9, 4, 6), wall); h.position.set(x, 2 - 3, z); rail.add(h);
    const r = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 6, 2.2, 4), roofM); r.rotation.y = Math.PI / 4; r.scale.set(1.1, 1, 0.75); r.position.set(x, 5.1 - 3, z); rail.add(r); }
  for (let i = 0; i < 7; i++) { const m = new THREE.Group(); m.position.set(-260 + i * 38, 22, -560);
    const tw = new THREE.Mesh(new THREE.CylinderGeometry(3.2, 3.8, 12, 16), wall); tw.position.y = 6; m.add(tw);
    const cap = new THREE.Mesh(new THREE.ConeGeometry(3.6, 4, 16), new THREE.MeshLambertMaterial({ color: 0x2b2b2b })); cap.position.y = 14; m.add(cap);
    for (let k = 0; k < 4; k++) { const sail = new THREE.Mesh(new THREE.BoxGeometry(0.5, 9, 0.2), new THREE.MeshLambertMaterial({ color: 0x6b4a33 }));
      sail.position.set(0, 12 + Math.cos(k * Math.PI / 2 + i) * 4.5, 3.9 + 0); sail.position.x = Math.sin(k * Math.PI / 2 + i) * 4.5; sail.rotation.z = -(k * Math.PI / 2 + i); m.add(sail); }
    rail.add(m); }
  const hl = new THREE.Mesh(new THREE.PlaneGeometry(3400, 200), new THREE.MeshBasicMaterial({ map: UT.hills, transparent: true, fog: false })); hl.position.set(0, 55, -900); rail.add(hl);
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
const iryo = makeTrainPro(LIVERY[{ blanco: 'iryoBlanco', bicolor: 'iryoBicolor' }[new URLSearchParams(location.search).get('iryo')] || 'iryo'], 8);   // 8 coches, como el Frecciarossa de Iryo
const ave = makeTrainPro(LIVERY.ave, 8);        // blanco con franja morada
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

const blocks = [], BL = 40;
for (let x = -420; x < 60; x += BL) { const m = new THREE.Mesh(new THREE.PlaneGeometry(BL - 4, 16), new THREE.MeshBasicMaterial({ color: 0x2bd96b, transparent: true, opacity: 0.85, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.set(x + BL / 2, 0.42, 0); m.renderOrder = 2; m.userData.x0 = x; scene.add(m); blocks.push(m); }
function setBlocks(t, u, mode) {
  blocks.forEach((b, i) => { b.visible = true; const x0 = b.userData.x0, mat = b.material;
    if (mode === 'off') { const k = clamp((u - 0.15) * 1.6 - (blocks.length - i) * 0.05); mat.color.setHex(k > 0 ? 0x3a3d41 : 0x2bd96b); mat.opacity = 0.85; }
    else if (mode === 'stop') { mat.color.setHex(x0 > -100 ? 0xe62828 : 0x3a3d41); }
    else { const occ = x0 > -100; const on = occ || u > 0.2 + (i / blocks.length) * 0.5;
      mat.color.setHex(occ ? 0xe62828 : (on ? 0x2bd96b : 0x3a3d41)); mat.opacity = occ ? 0.6 + 0.35 * Math.abs(Math.sin(t * 5)) : 0.85; } });
}
const glows = [iryo, ave].map((tr, i) => { const g = new THREE.Mesh(new THREE.PlaneGeometry(86, 30), new THREE.MeshBasicMaterial({ color: i ? 0x9c6bd1 : 0xff4d4d, transparent: true, opacity: 0.35, depthWrite: false }));
  g.rotation.x = -Math.PI / 2; g.position.set(-31, 0.45, 0); tr.add(g); g.visible = false; return g; });
function glowOn() { glows.forEach(g => g.visible = true); }
function setBg() { scene.background = UT.sky; sun.color.setHex({ a: 0xffd9a8, b: 0xffffff, c: 0xff9c5a }[LOOK_URDA]); sun.position.set(LOOK_URDA === 'b' ? 20 : -60, { a: 30, b: 90, c: 14 }[LOOK_URDA], 60); }
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
// ---------- cómo quedaron los trenes (El Español, Libertad Digital, Euronews, 28-29/10) ----------
// Iryo: los 4 primeros coches intactos; luego uno torcido, otro inclinado y el último destrozado y calcinado, con el AVE empotrado.
// AVE: la cabeza motriz cayó hacia un terraplén; sus coches 6 y 7 quedaron al otro lado de la vía; restos a ambos lados.
const IRYO_X = 82.4;                                  // 8 coches: la cola sigue en x ≈ -81 como antes
const burnM = []; iryo.userData.cars[7].traverse(m => { if (m.isMesh) { m.material = m.material.clone(); burnM.push([m.material, m.material.color.clone()]); } });
function burnt(k) { const dk = new THREE.Color(0x15110f); burnM.forEach(([m, c0]) => m.color.copy(c0).lerp(dk, k * 0.97)); }
const mound = new THREE.Mesh(new THREE.SphereGeometry(1, 18, 10, 0, 6.3, 0, 1.5), new THREE.MeshLambertMaterial({ color: 0x9b6a42 }));
mound.scale.set(22, 1.4, 9); mound.position.set(-100, -0.6, -12); scene.add(mound); mound.visible = false;
const debris = new THREE.Group(); debris.position.set(-80, 0, 0); scene.add(debris);
{ const r = rng(31), cols = [0xf2f3f5, 0xd9dce1, 0x6b2c8f, 0xc4122f, 0x2a2c31, 0x8c9198, 0x15110f];
  for (let i = 0; i < 90; i++) { const m = new THREE.Mesh(new THREE.BoxGeometry(0.15 + r() * 0.7, 0.04 + r() * 0.12, 0.15 + r() * 0.5), new THREE.MeshStandardMaterial({ color: cols[(r() * cols.length) | 0], roughness: 0.6, metalness: 0.3 }));
    const z = (r() - 0.45) * 22; m.position.set((r() - 0.5) * 40, (z < -6 ? -3 * (-z - 6) / 8 : z > 12 ? -3 * (z - 12) / 8 : 0) + 0.15, z); m.rotation.set(r() * 3, r() * 3, r() * 3); m.castShadow = true; debris.add(m); } }
const rescue = new THREE.Group(); scene.add(rescue);
{ const veh = (x, z, ry, body, stripe, len, light) => { const g = new THREE.Group(); g.position.set(x, -3, z); g.rotation.y = ry;
    const b = new THREE.Mesh(new RoundedBoxGeometry(len, 2.6, 2.3, 2, 0.2), new THREE.MeshStandardMaterial({ color: body, roughness: 0.5 })); b.position.y = 1.7; g.add(b);
    const st = new THREE.Mesh(new THREE.BoxGeometry(len + 0.02, 0.35, 2.32), new THREE.MeshStandardMaterial({ color: stripe })); st.position.y = 1.4; g.add(st);
    for (const wx of [-len * 0.32, len * 0.32]) for (const wz of [-1.1, 1.1]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.3, 14), new THREE.MeshStandardMaterial({ color: 0x1b1b1b })); w.rotation.x = Math.PI / 2; w.position.set(wx, 0.42, wz); g.add(w); }
    const lt = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.25, 1.6), new THREE.MeshBasicMaterial({ color: light })); lt.position.set(len * 0.35, 3.1, 0); g.add(lt); g.userData.lt = lt; rescue.add(g); return g; };
  const V = [[-70, -24, 0.2, 0xf4f4f0, 0xf2c200, 6, 0x2a7bff], [-60, -27, -0.1, 0xf4f4f0, 0xf2c200, 6, 0x2a7bff], [-125, -25, 0.3, 0xf4f4f0, 0xf2c200, 6, 0x2a7bff],
             [-95, -30, 0, 0xc8102e, 0xf4f4f0, 9, 0x2a7bff], [-150, 30, -0.2, 0xc8102e, 0xf4f4f0, 9, 0x2a7bff], [-40, 29, 0.1, 0xf4f4f0, 0x1f9d55, 6, 0x2a7bff], [-200, -26, 0.15, 0xf4f4f0, 0xf2c200, 6, 0x2a7bff]];
  rescue.userData.v = V.map(v => veh(...v));
  // grúa amarilla y torres de luz
  const yel = new THREE.MeshStandardMaterial({ color: 0xf2b705, roughness: 0.5 });
  const cr = new THREE.Group(); cr.position.set(-140, -3, -42); const cb = new THREE.Mesh(new THREE.BoxGeometry(10, 3, 3), yel); cb.position.y = 1.9; cr.add(cb);
  const boom = new THREE.Mesh(new THREE.BoxGeometry(16, 0.6, 0.6), yel); boom.position.set(4, 7, 0); boom.rotation.set(0, 0, 0.6); cr.add(boom); rescue.add(cr);
  for (const [x, z] of [[-110, -20], [-55, -20], [-80, 25]]) { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 9, 6), new THREE.MeshLambertMaterial({ color: 0x777 })); m.position.set(x, 1.5, z); rescue.add(m);
    const l = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.8, 0.4), new THREE.MeshBasicMaterial({ color: 0xfff6c8 })); l.position.set(x, 6.2, z); rescue.add(l); }
  rescue.visible = false; }
function rescueOn(t) { rescue.visible = true; rescue.userData.v.forEach((g, i) => g.userData.lt.material.color.setHex(Math.sin(t * 12 + i) > 0 ? 0x2a7bff : 0x0b1a40)); }
const FIN = {
  iryo: { 4: [0, 0.3, 0, 0, 0.03], 5: [0, 0.8, 0, 0.12, -0.06], 6: [1.5, 2.2, -0.15, 0.32, 0.12], 7: [3, 3.2, -0.3, 0.22, -0.24] },   // [dx, z, y, roll, yaw]
  ave: { 0: [6.5, -9.5, -1.4, -0.7, 0.42], 1: [5.5, -2, -0.2, -0.12, -0.22], 2: [4.5, 0.6, 0, 0, 0.16], 3: [3.5, 0, 0, 0.05, -0.1],
         4: [3, 3, -0.1, 0.15, 0.3], 5: [2.5, 10, -0.4, 0.35, -0.42], 6: [2, 11, -0.4, 0.3, 0.36], 7: [1.5, 2, 0, 0, 0.1] },
};
function crashPose(d) {   // d: 0 → 1, cada coche con su pequeño retraso
  for (const [tr, key, dl] of [[iryo, 'iryo', i => (7 - i) * 0.06], [ave, 'ave', i => i * 0.06]])
    for (const [i, v] of Object.entries(FIN[key])) { const c = tr.userData.cars[i], k = ease(clamp((d - dl(+i)) / (1 - dl(+i))));
      const lift = 1.5 * Math.abs(Math.sin(v[3] * k)) + v[2] * k;   // ningún coche se mete en el suelo (Iker 29/10)
      c.position.set(-i * 20.6 + v[0] * k, lift, v[1] * k); c.rotation.set(v[3] * k, v[4] * k, 0); }
  burnt(clamp((d - 0.5) * 2)); mound.visible = false;
  const cr = ease(clamp(d * 2)); ave.userData.cars[0].scale.x = 1 - 0.14 * cr; iryo.userData.cars[7].scale.x = 1 - 0.18 * cr;   // chapa aplastada
  debris.visible = d > 0.05; debris.scale.setScalar(Math.max(0.01, ease(clamp(d * 1.5))));
}
function hideAll() {
  wakeCone.visible = false; arrows.forEach(a => a.visible = false); air.visible = false;
  straight.visible = false; curve.visible = false; carA.visible = carB.visible = false; ground.visible = false; shadowCatcher.visible = false;
  rail.visible = true; iryo.visible = true; ave.visible = false; tape.visible = false; flag.visible = false; candles.visible = false;
  signals.forEach(s => s.userData.lamp.material.color.setHex(0x2bd96b));
  iryo.userData.cars.forEach(c => { c.position.z = 0; c.rotation.set(0, 0, 0); c.position.y = 0; });
  blocks.forEach(b => b.visible = false); glows.forEach(g => g.visible = false);
  iryo.position.set(IRYO_X, 0, 0); ave.position.set(-400, 0, 0); ave.userData.cars.forEach((c, i) => { c.rotation.set(0, 0, 0); c.position.set(-i * 20.6, 0, 0); }); burnt(0); mound.visible = false; debris.visible = false; rescue.visible = false; ave.userData.cars[0].scale.x = 1; iryo.userData.cars[7].scale.x = 1; iryo.userData.cars.forEach((c, i) => { c.position.x = -i * 20.6; }); DIM = 0;
  sun.intensity = 1.0;
}
const SC = [
  // 0 · gancho: persecución detrás del AVE hasta el impacto, que se congela
  (t, u) => { ave.visible = true; const CX = -81, hit = 0.7;
    ave.position.x = u < hit ? lerp(-175, -100.4, Math.pow(u / hit, 1.6)) : -100.4 + 4 * ease(clamp((u - hit) / 0.3)); crashPose(clamp((u - hit) / 0.3) * 0.35);
    const front = ave.position.x + 19.4, sh = u > hit ? Math.exp(-(u - hit) * 14) : 0;
    setCam(Math.min(front, CX) - 42 + Math.sin(t * 71) * sh, 11 + Math.cos(t * 53) * sh, 8, CX + 12, 1, 0);
    const pf = proj(new THREE.Vector3(front, 1.2, 0)), pr = proj(new THREE.Vector3(CX, 1.2, 0)), c = proj(new THREE.Vector3(CX, 2.5, 0));
    return [['pill', pr[0], pr[1] - 110, 'TREN PARADO', clamp((hit - u) * 8), CSS_RED], ['pill', W / 2, 880, 'AVE', clamp((hit - u) * 8), '#5b2a86'],
            ['gap', pf[0], pf[1], pr[0], pr[1], clamp((hit - u) * 8)], ['flash', u > hit ? clamp(1 - (u - hit) * 8) * 0.9 : 0],
            ['impact', c[0], c[1], clamp((u - hit) / 0.3)], ['dust', c[0], c[1], clamp((u - hit) / 0.45)],
            ['pill', W / 2, 1000, 'MISMA VÍA', clamp(u * 5) * clamp((hit - u) * 8), '#1d2228']]; },
  // 1 · dónde: dron que baja del cielo sobre la línea, el Iryo pasa a toda velocidad (antes de las 8:30)
  (t, u) => { iryo.position.x = lerp(420, 160, u); const e = ease(u);
    setCam(lerp(-330, -60, e), lerp(260, 16, e), lerp(150, 34, e), lerp(-40, 40, e), 0, 0);
    const pn = proj(new THREE.Vector3(-81, 2, 0));
    return [['clock', '28 OCT', 'MADRID – ANDALUCÍA', clamp(u * 4)], ['pill', pn[0], pn[1] - 60, 'PK 118 · CERCA DE URDA (TOLEDO)', clamp((u - 0.2) * 4) * clamp((0.85 - u) * 6), CSS_RED]]; },
  // 2 · 8:30: zoom a una señal de la vía que se apaga y subida rápida a la vista de tramos, que se quedan sin señal
  (t, u) => { iryo.visible = false; const sg = signals[1], off = u > 0.3;
    sg.userData.lamp.material.color.setHex(off ? 0x1a1a1a : (Math.sin(t * 20) > 0 || u < 0.2 ? 0x2bd96b : 0x1a1a1a));
    if (u < 0.5) { const z = ease(u / 0.5); const sx = sg.position.x + rail.position.x;
      setCam(sx - lerp(18, 5, z), lerp(4, 3.2, z), lerp(-14, -6, z), sx, 3.2, -2.2);
      return [['clock', '8:30', 'FALLA EL LZB', clamp(u * 6)], ['pill', W / 2, 1000, 'EL SISTEMA QUE DA ÓRDENES A LOS TRENES', clamp((u - 0.15) * 6), CSS_RED]]; }
    const k = ease(clamp((u - 0.5) / 0.3)); setBlocks(t, 0.15 + (u - 0.5) * 2, 'off');
    setCam(-140 + (1 - k) * 60, lerp(10, 430, k), lerp(-8, 0.01, k), -140, 0, 3, [k, 1 - k, 0]);
    return [['pill', W / 2, 1000, 'LOS TRAMOS SE QUEDAN SIN SEÑAL', clamp((u - 0.6) * 5), CSS_RED]]; },
  // 3 · se paran: travelling lateral a lo largo del Iryo parado y grúa hacia atrás que descubre el AVE parado más atrás
  (t, u) => { ave.visible = true; ave.position.x = -235;
    if (u < 0.55) { const k = ease(u / 0.55); setCam(lerp(95, -40, k), 4.5, -16, lerp(85, -60, k), 2.2, 0);
      const pi = proj(new THREE.Vector3(lerp(85, -60, k), 6, 0)); return [['pill', pi[0], pi[1] - 60, 'IRYO · PARADO', clamp(u * 6), CSS_RED]]; }
    const k = ease(clamp((u - 0.55) / 0.35)); setCam(lerp(-40, -330, k), lerp(4.5, 55, k), lerp(-16, -25, k), lerp(-60, -90, k), 0, 0);
    const pa = proj(new THREE.Vector3(-250, 6, 0)), pi = proj(new THREE.Vector3(-40, 6, 0));
    return [['pill', pi[0], pi[1] - 50, 'IRYO · PARADO', 1, CSS_RED], ['pill', pa[0], pa[1] - 50, 'AVE · PARADO DETRÁS', clamp((u - 0.7) * 5), '#5b2a86']]; },
  // 4 · la clave: zoom desde muy arriba al esquema; el camino verde del AVE acaba en el tramo rojo del Iryo
  (t, u) => { ave.visible = true; ave.position.x = -235; setBlocks(t, u, 'green'); glowOn(); const h = lerp(760, 360, ease(clamp(u * 1.4)));
    setCam(-120, h, 0.01, -120, 0, 3, [1, 0, 0]); const pr = proj(new THREE.Vector3(-30, 4, 0));
    return [['pill', W / 2, 250, 'SEGÚN EL MINISTRO DE TRANSPORTES', clamp(u * 4)], ['pill', W / 2, 310, 'VÍA LIBRE PARA SEGUIR', clamp((u - 0.2) * 4), '#1fa85a'],
            ['pill', pr[0] + 150, pr[1], 'TRAMO OCUPADO', clamp((u - 0.55) * 4), CSS_RED]]; },
  // 5 · el AVE arranca: cámara baja junto a las ruedas y luego persecución, el Iryo al fondo en la misma vía
  (t, u) => { ave.visible = true; ave.position.x = lerp(-235, -175, ease(u)); if (u > 0.4) { setBlocks(t, 1, 'green'); glowOn(); }
    if (u < 0.35) setCam(ave.position.x + 30, 1.4, -6, ave.position.x + 10, 1, 0);
    else { const k = ease(clamp((u - 0.35) / 0.3)); setCam(ave.position.x + lerp(30, -75, k), lerp(1.4, 13, k), lerp(-6, 7, k), ave.position.x + lerp(10, 60, k), 2, 0); }
    const pi = proj(new THREE.Vector3(-30, 7, 0)); return [['pill', pi[0], pi[1] - 40, 'IRYO PARADO DELANTE', clamp((u - 0.45) * 4), CSS_RED], ['arrow', clamp((u - 0.35) * 1.5)]]; },
  // 6 · el alcance: la distancia se cierra, impacto (destello, temblor, polvo) y, a cámara lenta, cómo se mueve cada coche
  (t, u) => { ave.visible = true; const CX = -81, hit = 0.3;
    ave.position.x = u < hit ? lerp(-165, -100.4, u / hit) : -100.4 + 4 * ease(clamp((u - hit) / 0.3));
    const d = clamp((u - hit) / 0.6); crashPose(d);
    const front = ave.position.x + 19.4, sh = u > hit ? Math.exp(-(u - hit) * 14) : 0, jx = Math.sin(t * 71) * 0.9 * sh, jy = Math.cos(t * 53) * 0.7 * sh;
    const k = ease(clamp((u - hit + 0.04) / 0.3)), fx = Math.min(front, CX), orb = lerp(-0.3, 0.5, clamp((u - hit) / 0.7));
    setCam(lerp(fx - 42, -80 + Math.sin(orb) * 19, k) + jx, lerp(11, 8, k) + jy, lerp(8, Math.cos(orb) * 19, k), lerp(CX + 12, -80, k), lerp(1, 3.5, k), lerp(0, 0, k));
    const pf = proj(new THREE.Vector3(front, 1.2, 0)), pr = proj(new THREE.Vector3(CX, 1.2, 0)), c = proj(new THREE.Vector3(CX, 2.5, 0));
    const pre = clamp((hit - u) * 8), la = proj(new THREE.Vector3(-90, 6, -6)), li = proj(new THREE.Vector3(-55, 7, 3));
    return [['pill', W / 2, 880, 'AVE', pre, '#5b2a86'], ['pill', pr[0], pr[1] - 110, 'IRYO PARADO', pre, CSS_RED], ['gap', pf[0], pf[1], pr[0], pr[1], pre],
            ['flash', u > hit ? clamp(1 - (u - hit) * 10) * 0.85 : 0], ['dust', c[0], c[1], clamp((u - hit) / 0.6)],
            ['clock', '8:54', 'ALCANCE', clamp((u - hit + 0.05) * 6)], ['impact', c[0], c[1], clamp((u - hit) / 0.3)],
            ['pill', la[0], la[1], 'AVE', clamp((u - hit - 0.1) * 5), '#5b2a86'], ['pill', li[0], li[1], 'IRYO', clamp((u - hit - 0.1) * 5), CSS_RED],
            ['pill', W / 2, 1000, 'EL AVE SE EMPOTRA EN EL ÚLTIMO COCHE', clamp((u - hit - 0.15) * 4), CSS_RED]]; },
  // 7 · cómo quedaron, plano a plano (Iker: «no se ve bien»): cabeza del AVE en el terraplén → coches 6 y 7 al otro lado → último coche del Iryo calcinado
  (t, u) => { ave.visible = true; ave.position.x = -96.4; crashPose(1); rescueOn(t);
    const S = [[[-120, 3, -32], [-92, -1, -8]], [[-178, 16, 38], [-206, 0, 9]], [[-36, 9, 26], [-62, 1.5, 2]]];
    const i = Math.min(2, Math.floor(u * 3)), f = u * 3 - i, m = ease(clamp(f / 0.25)), A = S[Math.max(0, i - 1)], B = S[i], w = i ? m : 1;
    const P = A[0].map((v, j) => lerp(v, B[0][j], w)), L = A[1].map((v, j) => lerp(v, B[1][j], w)), push = 1 - 0.12 * ease(f);
    setCam(L[0] + (P[0] - L[0]) * push, L[1] + (P[1] - L[1]) * push, L[2] + (P[2] - L[2]) * push, ...L);
    const sm = proj(new THREE.Vector3(-59, 5, 3)), al = clamp((f - 0.2) * 6) * clamp((1 - f) * 12 + (i === 2 ? 1 : 0));
    const TX = [['CABEZA DEL AVE', 'CAYÓ HACIA UN TERRAPLÉN', '#5b2a86'], ['COCHES 6 Y 7 DEL AVE', 'AL OTRO LADO DE LA VÍA', '#5b2a86'], ['ÚLTIMO COCHE DEL IRYO', 'DESTROZADO Y CALCINADO', CSS_RED]][i];
    return [['dust', sm[0], sm[1] - 60, i === 2 ? 0.3 + 0.15 * Math.sin(t * 2) : 0], ['pill', W / 2, 250, TX[0], al, TX[2]], ['pill', W / 2, 310, TX[1], al, '#1d2228']]; },
  // 8 · las víctimas: plano bajo desde el campo hacia los restos, con la cifra
  (t, u) => { ave.visible = true; ave.position.x = -96.4; crashPose(1); rescueOn(t); setCam(-95 + Math.sin(lerp(0.5, 1.1, u)) * 110, 95, Math.cos(lerp(0.5, 1.1, u)) * 110, -120, 0, 0); DIM = 0.3;
    return [['bignum', '68', 'FALLECIDOS', clamp(u * 3)], ['pill', W / 2, 760, '≈540 VIAJEROS · MÁS DE 100 HERIDOS', clamp((u - 0.45) * 4)]]; },
  // 9 · la investigación: cámara que se acerca a los restos tras la cinta
  (t, u) => { ave.visible = true; ave.position.x = -96.4; crashPose(1); rescueOn(t); setCam(lerp(-20, -40, u), 2, lerp(-48, -38, u), -85, 1, 0); return [['pill', W / 2, 420, 'INVESTIGA UN JUZGADO DE ORGAZ', clamp((u - 0.2) * 4)]]; },
  // 9 · luto oficial y línea cortada (sin bandera, Iker 29/10)
  (t, u) => { iryo.visible = false; tape.visible = true; setCam(12, 2.6, 13, 30, 1.2, 3);
    return [['ribbon', clamp(u * 3)], ['pill', W / 2, 560, '3 DÍAS DE LUTO OFICIAL', clamp((u - 0.15) * 4)], ['pill', W / 2, 630, 'LÍNEA MADRID–ANDALUCÍA CORTADA', clamp((u - 0.4) * 4), CSS_RED]]; },
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
function ribbon(u) {
  if (u <= 0) return; ctx.save(); ctx.globalAlpha = clamp(u * 2); ctx.translate(W / 2, 330); const k = 0.55 * eob(u); ctx.scale(k, k);
  ctx.lineJoin = 'round'; ctx.lineWidth = 9; ctx.strokeStyle = '#fff'; ctx.fillStyle = '#111';
  ctx.beginPath(); ctx.moveTo(0, -10); ctx.bezierCurveTo(-70, -110, -120, -20, -45, 40); ctx.lineTo(-95, 170); ctx.lineTo(-55, 160); ctx.lineTo(0, 20);
  ctx.lineTo(55, 160); ctx.lineTo(95, 170); ctx.lineTo(45, 40); ctx.bezierCurveTo(120, -20, 70, -110, 0, -10); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
}
function arrowFwd(u) {
  const a = clamp(u * 3); if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.translate(W / 2, 760 - (u * 140 % 60));
  for (let k = 0; k < 3; k++) { ctx.strokeStyle = `rgba(255,255,255,${0.9 - k * 0.25})`; ctx.lineWidth = 10; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(-40, -k * 40 + 20); ctx.lineTo(0, -k * 40 - 10); ctx.lineTo(40, -k * 40 + 20); ctx.stroke(); } ctx.restore();
}
function gap(x0, y0, x1, y1, a) {
  if (a <= 0 || x1 - x0 < 8) return; ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = '#ffd23f'; ctx.lineWidth = 7; ctx.setLineDash([16, 10]);
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); ctx.setLineDash([]);
  for (const [x, y] of [[x0, y0], [x1, y1]]) { ctx.beginPath(); ctx.moveTo(x, y - 22); ctx.lineTo(x, y + 22); ctx.stroke(); } ctx.restore();
}
function darr(x0, y0, x1, y1, a) {
  if (a <= 0) return; const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, e = 0.3 + 0.7 * a;
  const ex = x0 + dx * 1.3 * e, ey = y0 + dy * 1.3 * e; ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = '#ff2b2b'; ctx.fillStyle = '#ff2b2b'; ctx.lineWidth = 12; ctx.lineCap = 'round';
  ctx.shadowColor = 'rgba(0,0,0,0.5)'; ctx.shadowBlur = 10; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(ex, ey); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ex + ux * 26, ey + uy * 26); ctx.lineTo(ex - uy * 22, ey + ux * 22); ctx.lineTo(ex + uy * 22, ey - ux * 22); ctx.fill(); ctx.restore();
}
function flash(a) { if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
function dust(x, y, u) {
  if (u <= 0 || u >= 1) return; ctx.save(); const r = rng(9);
  for (let i = 0; i < 26; i++) { const an = r() * 6.28, sp = 40 + r() * 170, rr = 14 + r() * 34 + u * 50;
    ctx.globalAlpha = 0.5 * (1 - u) * (0.5 + r() * 0.5); ctx.fillStyle = r() < 0.5 ? '#d9c7a8' : '#b9a58a';
    ctx.beginPath(); ctx.arc(x + Math.cos(an) * sp * ease(u), y + Math.sin(an) * sp * 0.55 * ease(u) - u * 40, rr, 0, 7); ctx.fill(); }
  ctx.restore();
}
function impact(x, y, u) {
  if (u <= 0 || u >= 1) return; ctx.save();
  for (let k = 0; k < 3; k++) { const r = 20 + (u * 1.4 - k * 0.15) * 160; if (r <= 20) continue;
    ctx.globalAlpha = clamp(1 - u * 1.1 - k * 0.15); ctx.strokeStyle = k ? '#ffffff' : '#ffd23f'; ctx.lineWidth = 8 - k * 2; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.stroke(); }
  ctx.restore();
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
    if (k === 'pill') { a[0] = Math.max(260, Math.min(W - 260, a[0])); pill(...a); } else if (k === 'clock') clockCard(...a); else if (k === 'people') peopleGrid(...a);
    else if (k === 'bignum') bigNum(...a); else if (k === 'panel') controlPanel(...a); else if (k === 'ribbon') ribbon(...a); else if (k === 'arrow') arrowFwd(...a); else if (k === 'impact') impact(...a); else if (k === 'gap') gap(...a); else if (k === 'darr') darr(...a); else if (k === 'flash') flash(...a); else if (k === 'dust') dust(...a); }
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

// foto de estudio de los trenes (para elegir colores y texturas)
window.trainStudio = function (k) {
  T = window.TIMING; hideAll(); setBg(); ave.visible = true; ave.position.set(-140, 0, 6);
  const V = [[24, 4, 14, 6, 2.2, 0], [-110, 5, 14, -132, 2.2, 6], [10, 9, 26, -20, 1.5, 3]][k];
  setCam(...V); gl.clear(); gl.render(scene, cam);
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, out.width, out.height); ctx.drawImage(gl.domElement, 0, 0);
  return out.toDataURL('image/jpeg', 0.95);
};
