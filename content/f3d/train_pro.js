// Trenes de alta velocidad más reales (Iker 29/10: «cambia colores y texturas del tren»). Genéricos, sin logotipos.
// Caja con sección redondeada y librea pintada en textura (ventanas con reflejo, puertas, juntas, franjas),
// morro largo con parabrisas, bogies con ruedas, fuelles entre coches y equipos en el techo.
import * as THREE from 'three';

const CAR = 19.6, W2 = 1.45, H = 3.55;   // largo, semiancho y alto de la caja (m)

function liveryTex(L) {
  const c = document.createElement('canvas'); c.width = 2048; c.height = 512; const x = c.getContext('2d');
  const yy = h => 512 - (h / H) * 512;            // altura en metros → píxel
  x.fillStyle = L.body; x.fillRect(0, 0, 2048, 512);
  // degradado suave del techo y sombra en la parte baja
  let g = x.createLinearGradient(0, yy(H), 0, yy(H * 0.8)); g.addColorStop(0, L.roof); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(0, 0, 2048, yy(H * 0.8));
  x.fillStyle = L.skirt; x.fillRect(0, yy(0.55), 2048, 512 - yy(0.55));
  for (const s of L.stripes) { x.fillStyle = s.c; x.fillRect(0, yy(s.y + s.h), 2048, (s.h / H) * 512); }
  // banda de ventanas: cristal oscuro con reflejo de cielo
  const wy0 = yy(L.win[1]), wy1 = yy(L.win[0]);
  g = x.createLinearGradient(0, wy0, 0, wy1); g.addColorStop(0, '#5d7387'); g.addColorStop(0.35, '#1d2731'); g.addColorStop(1, '#0d1217');
  x.fillStyle = L.band || '#111418'; x.fillRect(0, wy0 - 6, 2048, wy1 - wy0 + 12);
  for (let i = 0; i < 14; i++) { const x0 = 170 + i * 122; x.fillStyle = g; x.beginPath(); x.roundRect(x0, wy0, 108, wy1 - wy0, 10); x.fill();
    x.fillStyle = 'rgba(255,255,255,0.18)'; x.beginPath(); x.moveTo(x0 + 10, wy0 + 4); x.lineTo(x0 + 44, wy0 + 4); x.lineTo(x0 + 16, wy1 - 6); x.lineTo(x0 + 4, wy1 - 6); x.fill(); }
  // puertas en los dos extremos
  for (const dx of [40, 1918]) { x.strokeStyle = 'rgba(0,0,0,0.45)'; x.lineWidth = 4; x.beginPath(); x.roundRect(dx, yy(2.55), 90, yy(0.6) - yy(2.55), 8); x.stroke();
    x.fillStyle = g; x.fillRect(dx + 22, yy(2.4), 46, yy(1.75) - yy(2.4)); }
  // juntas de paneles y pequeño ruido para que no parezca plástico
  x.strokeStyle = 'rgba(0,0,0,0.12)'; x.lineWidth = 2; for (const px of [150, 1890]) { x.beginPath(); x.moveTo(px, 0); x.lineTo(px, 512); x.stroke(); }
  for (let i = 0; i < 9000; i++) { x.fillStyle = Math.random() < 0.5 ? 'rgba(0,0,0,0.025)' : 'rgba(255,255,255,0.03)'; x.fillRect(Math.random() * 2048, Math.random() * 512, 2, 2); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

function bodyGeo() {
  // sección: costados casi verticales, techo muy redondeado
  const s = new THREE.Shape(); const r1 = 0.9, r0 = 0.35;
  s.moveTo(-W2 + r0, 0); s.lineTo(W2 - r0, 0); s.quadraticCurveTo(W2, 0, W2, r0);
  s.lineTo(W2, H - r1); s.quadraticCurveTo(W2 - 0.05, H, W2 - r1, H); s.lineTo(-W2 + r1, H); s.quadraticCurveTo(-W2 + 0.05, H, -W2, H - r1);
  s.lineTo(-W2, r0); s.quadraticCurveTo(-W2, 0, -W2 + r0, 0);
  const uv = {
    generateTopUV: (g, v, a, b, c) => [new THREE.Vector2(0.5, 0.95), new THREE.Vector2(0.5, 0.95), new THREE.Vector2(0.5, 0.95)],
    generateSideWallUV: (g, v, a, b, c, d) => [a, b, c, d].map(i => new THREE.Vector2(v[i * 3 + 2] / CAR, v[i * 3 + 1] / H)),
  };
  const geo = new THREE.ExtrudeGeometry(s, { depth: CAR, bevelEnabled: false, curveSegments: 10, UVGenerator: uv });
  geo.translate(0, 0, -CAR / 2); geo.rotateY(Math.PI / 2);   // largo a lo largo de X
  return geo;
}

function noseGeo(len) {
  // morro largo y afilado: la sección de la caja se estrecha y baja hacia la punta; con UV (u: a lo largo, v: alrededor)
  const segs = 26, ring = 32, pos = [], uv = [], idx = [];
  for (let i = 0; i <= segs; i++) {
    const t = i / segs;
    const hw = W2 * Math.max(0.08, Math.pow(1 - t, 0.55));
    const top = H - (H - 0.95) * Math.pow(t, 0.62), bot = 0.05 + 0.3 * t * t;
    const cy = (top + bot) / 2, hh = Math.max(0.06, (top - bot) / 2);
    for (let j = 0; j <= ring; j++) { const a = j / ring * Math.PI * 2, c = Math.cos(a), sn = Math.sin(a);
      const pc = Math.sign(c) * Math.pow(Math.abs(c), 0.55), ps = Math.sign(sn) * Math.pow(Math.abs(sn), sn > 0 ? 0.7 : 0.35);
      pos.push(t * len, cy + ps * hh, pc * hw); uv.push(t, j / ring); }
  }
  const R = ring + 1;
  for (let i = 0; i < segs; i++) for (let j = 0; j < ring; j++) { const a = i * R + j, b = a + 1; idx.push(a, a + R, b, b, a + R, b + R); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals(); return g;
}
function noseTex(L) {
  // u: 0 (unión con la caja) → 1 (punta) · v: 0 lateral, 0.25 arriba, 0.5 otro lateral, 0.75 abajo
  const c = document.createElement('canvas'); c.width = 512; c.height = 512; const x = c.getContext('2d');
  x.fillStyle = L.body; x.fillRect(0, 0, 512, 512);
  x.fillStyle = L.skirt; x.fillRect(0, 0.62 * 512, 512, 0.26 * 512);          // parte baja
  for (const v of [0.05, 0.45]) { x.fillStyle = (L.stripes[0] || {}).c || '#fff';    // franja lateral que se afila hacia la punta
    x.beginPath(); x.moveTo(0, v * 512); x.lineTo(0.75 * 512, (v + (v < 0.25 ? 0.03 : -0.03)) * 512); x.lineTo(0, (v + (v < 0.25 ? 0.06 : -0.06)) * 512); x.fill(); }
  // parabrisas oscuro con reflejo, en la parte de arriba
  const g = x.createLinearGradient(0.2 * 512, 0, 0.6 * 512, 0); g.addColorStop(0, '#0d141b'); g.addColorStop(0.5, '#2b3b4a'); g.addColorStop(1, '#0d141b');
  x.fillStyle = g; x.beginPath(); x.ellipse(0.36 * 512, 0.25 * 512, 0.17 * 512, 0.13 * 512, 0, 0, 7); x.fill();
  x.fillStyle = 'rgba(255,255,255,0.25)'; x.beginPath(); x.ellipse(0.3 * 512, 0.2 * 512, 0.06 * 512, 0.02 * 512, -0.3, 0, 7); x.fill();
  // ventanilla lateral de la cabina, a ambos lados
  x.fillStyle = '#111418'; for (const v of [0.12, 0.38]) { x.beginPath(); x.ellipse(0.12 * 512, v * 512, 0.08 * 512, 0.035 * 512, 0, 0, 7); x.fill(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

export function makeTrainPro(L, n = 4) {
  const g = new THREE.Group(); g.userData.cars = [];
  const tex = liveryTex(L);
  const paint = new THREE.MeshPhysicalMaterial({ map: tex, roughness: 0.28, metalness: 0.05, clearcoat: 1, clearcoatRoughness: 0.08 });
  const noseM = new THREE.MeshPhysicalMaterial({ map: noseTex(L), roughness: 0.25, clearcoat: 1, clearcoatRoughness: 0.06 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0x0e151c, roughness: 0.05, metalness: 0.6, clearcoat: 1 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x23262b, roughness: 0.75, metalness: 0.2 });
  const steel = new THREE.MeshStandardMaterial({ color: 0x8c9198, roughness: 0.35, metalness: 0.85 });
  const stripeM = (c) => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.3, clearcoat: 1 });
  const body = bodyGeo(), nose = noseGeo(9.5);
  for (let i = 0; i < n; i++) {
    const c = new THREE.Group(); c.position.x = -i * (CAR + 1.0); g.add(c); g.userData.cars.push(c);
    const b = new THREE.Mesh(body, paint); b.position.y = 0.55; c.add(b);
    // bogies con ruedas a la vista
    for (const bx of [-6.9, 6.9]) {
      const bg = new THREE.Mesh(new THREE.BoxGeometry(3.0, 0.55, 2.1), dark); bg.position.set(bx, 0.62, 0); c.add(bg);
      for (const wx of [-0.95, 0.95]) for (const wz of [-0.72, 0.72]) {
        const w = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.46, 0.14, 20), steel); w.rotation.x = Math.PI / 2; w.position.set(bx + wx, 0.46, wz); c.add(w); }
    }
    // techo: carenados de climatización y pantógrafo en el segundo coche
    const ac = new THREE.Mesh(new THREE.BoxGeometry(5, 0.28, 1.4), new THREE.MeshStandardMaterial({ color: L.roofEq || 0x9da2a8, roughness: 0.6 })); ac.position.set(2, H + 0.6, 0); c.add(ac);
    if (i === 1) { for (const a of [0.5, -0.5]) { const arm = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.07, 0.07), dark); arm.position.set(-3 + a, H + 1.05, 0); arm.rotation.z = a * 0.7; c.add(arm); }
      const head = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.06, 1.6), steel); head.position.set(-3, H + 1.45, 0); c.add(head); }
    // fuelle entre coches
    if (i < n - 1) { const bel = new THREE.Mesh(new THREE.BoxGeometry(1.0, 3.1, 2.6), dark); bel.position.set(-CAR / 2 - 0.5, 2.25, 0); c.add(bel); }
    // morros en cabeza y cola
    if (i === 0 || i === n - 1) {
      const dir = i === 0 ? 1 : -1;
      const nz = new THREE.Mesh(nose, noseM); nz.position.set(dir * CAR / 2, 0.55, 0); if (dir < 0) nz.rotation.y = Math.PI; c.add(nz);
      for (const z of [-0.55, 0.55]) { const hl = new THREE.Mesh(new THREE.CircleGeometry(0.13, 16), new THREE.MeshBasicMaterial({ color: dir > 0 ? 0xfff6d8 : 0xff3b2f }));
        hl.position.set(dir * (CAR / 2 + 8.2), 0.95, z * 0.75); hl.rotation.y = dir * Math.PI / 2; c.add(hl); }
    }
    c.traverse(m => { if (m.isMesh) { m.castShadow = true; m.frustumCulled = false; } });
  }
  return g;
}

export const LIVERY = {
  // Iryo: rojo intenso, banda negra de ventanas, línea blanca baja
  iryo: { body: '#c4122f', roof: '#9e0e25', skirt: '#2a2c31', band: '#0f1114', win: [2.35, 3.15], nose: 0xc4122f,
          stripes: [{ y: 0.95, h: 0.08, c: '#ffffff' }, { y: 1.1, h: 0.04, c: '#f08a24' }] },
  // AVE de Renfe: blanco con franja morada y faldón gris
  ave: { body: '#f2f3f5', roof: '#d9dce1', skirt: '#8e949c', band: '#2b2f36', win: [2.3, 3.1], nose: 0xf2f3f5,
         stripes: [{ y: 1.05, h: 0.42, c: '#6b2c8f' }, { y: 0.92, h: 0.07, c: '#c8102e' }] },
};
