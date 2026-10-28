// ---------- Urda (Toledo), 28/10/2026 · tono informativo y triste (Iker, 29/10) ----------
// El choque NO se ve: la escena 3 funde a oscuro antes. Nada de colores alegres: cielo nublado, campo seco de La Mancha.
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

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
