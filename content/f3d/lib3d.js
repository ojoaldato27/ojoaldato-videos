// Biblioteca 3D común para los vídeos 3D de «Ojo al dato» (borrador 06/11/2026).
// Renderer + posproceso (desenfoque de cámara y brillo) + piezas: mano, Ojo 3D, cerebro, agua, partículas.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
export { THREE };

export const W = 720, H = 1280;
export const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
export const clamp = x => Math.max(0, Math.min(1, x));
export const lerp = (a, b, k) => a + (b - a) * k;
export const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
export const pop = k => k <= 0 ? 0 : k >= 1 ? 1 : 1 + 2.7 * Math.pow(k - 1, 3) + 1.7 * Math.pow(k - 1, 2);

export function setup({ bg = 0x1a2233, exposure = 0.9, fog = null, envI = 0.6, bloom = [0.45, 0.6, 0.82], dof = true } = {}) {
  const gl = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  gl.setPixelRatio(1); gl.setSize(W, H);
  gl.toneMapping = THREE.ACESFilmicToneMapping; gl.toneMappingExposure = exposure;
  gl.outputColorSpace = THREE.SRGBColorSpace;
  gl.shadowMap.enabled = true; gl.shadowMap.type = THREE.PCFSoftShadowMap;
  document.body.appendChild(gl.domElement);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(bg);
  if (fog) scene.fog = new THREE.Fog(bg, fog[0], fog[1]);
  const pm = new THREE.PMREMGenerator(gl);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = envI;
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.05, 80);
  const comp = new EffectComposer(gl);
  comp.addPass(new RenderPass(scene, cam));
  let bokeh = null;
  if (dof) { bokeh = new BokehPass(scene, cam, { focus: 4, aperture: 0.004, maxblur: 0.008 }); comp.addPass(bokeh); }
  comp.addPass(new UnrealBloomPass(new THREE.Vector2(W, H), bloom[0], bloom[1], bloom[2]));
  comp.addPass(new OutputPass());
  const render = (focusDist) => {
    if (bokeh && focusDist) bokeh.uniforms.focus.value = focusDist;
    comp.render();
    return gl.domElement.toDataURL('image/jpeg', 0.93);
  };
  return { gl, scene, cam, render, bokeh };
}

// ---------- texturas de lienzo
export function canvasTex(w, h, draw, repeat = [1, 1]) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat);
  return t;
}
export const softDot = canvasTex(64, 64, (x, w) => {
  const g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.4, 'rgba(255,255,255,.5)'); g.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = g; x.fillRect(0, 0, 64, 64);
});

// partículas flotantes (polvo de luz / vapor): Points con textura suave
export function floaters(scene, n, box, color = 0xffffff, size = 0.08, opacity = 0.7) {
  const g = new THREE.BufferGeometry();
  const base = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    base[i * 3] = box[0] + Math.random() * (box[1] - box[0]);
    base[i * 3 + 1] = box[2] + Math.random() * (box[3] - box[2]);
    base[i * 3 + 2] = box[4] + Math.random() * (box[5] - box[4]);
  }
  g.setAttribute('position', new THREE.BufferAttribute(base.slice(), 3));
  const m = new THREE.PointsMaterial({ color, size, map: softDot, transparent: true, opacity, depthWrite: false, blending: THREE.AdditiveBlending });
  const p = new THREE.Points(g, m); scene.add(p);
  p.userData.update = (t, rise = 0.15) => {
    const a = g.attributes.position.array;
    for (let i = 0; i < n; i++) {
      a[i * 3] = base[i * 3] + 0.12 * Math.sin(t * 0.7 + i);
      const h = box[3] - box[2];
      a[i * 3 + 1] = box[2] + ((base[i * 3 + 1] - box[2] + t * rise * (0.5 + (i % 5) / 5)) % h);
      a[i * 3 + 2] = base[i * 3 + 2] + 0.1 * Math.cos(t * 0.5 + i * 1.3);
    }
    g.attributes.position.needsUpdate = true;
  };
  return p;
}

// ---------- mano orgánica: dedos por torno (con nudillos), yemas que se arrugan
export const skinMat = () => new THREE.MeshPhysicalMaterial({ color: 0xe8a27f, roughness: 0.5, clearcoat: 0.3, clearcoatRoughness: 0.4, sheen: 0.7, sheenRoughness: 0.5, sheenColor: new THREE.Color(0xff8f7a) });

function fingerGeo(len, r) {
  const pts = [];
  const N = 40;
  for (let i = 0; i <= N; i++) {
    const u = i / N, y = u * len;
    let rad = r * (1 - 0.18 * u) * (1 + 0.07 * Math.exp(-Math.pow((u - 0.42) / 0.07, 2)) + 0.05 * Math.exp(-Math.pow((u - 0.72) / 0.06, 2)));
    pts.push(new THREE.Vector2(rad, y));
  }
  const rt = r * 0.82;
  for (let i = 1; i <= 12; i++) { const a = (i / 12) * Math.PI / 2; pts.push(new THREE.Vector2(rt * Math.cos(a), len + rt * Math.sin(a) * 0.95)); }
  const g = new THREE.LatheGeometry(pts, 48);
  g.userData = { len, r, top: len + rt * 0.95 };
  return g;
}

export function makeHand(mat = skinMat()) {
  const hand = new THREE.Group();
  const palmG = new RoundedBoxGeometry(1.3, 1.3, 0.42, 10, 0.2);
  { const a = palmG.attributes.position.array; for (let i = 0; i < a.length; i += 3) { const u = (a[i + 1] + 0.65) / 1.3; a[i] *= 0.78 + 0.22 * Math.min(1, u * 1.4); a[i + 2] *= 1 + 0.25 * Math.sin(Math.PI * Math.min(1, Math.max(0, u))); } palmG.computeVertexNormals(); }
  const palm = new THREE.Mesh(palmG, mat); palm.position.y = 0.72; hand.add(palm);
  const wristG = new THREE.CylinderGeometry(0.46, 0.42, 1.8, 40); wristG.scale(1, 1, 0.5);
  const wrist = new THREE.Mesh(wristG, mat); wrist.position.y = -0.3; hand.add(wrist);
  const fingers = [];
  const DEF = [[-0.36, 0.78, 0.12, -0.10], [-0.12, 0.92, 0.125, -0.03], [0.12, 0.88, 0.122, 0.03], [0.35, 0.68, 0.11, 0.11]];
  const nailM = new THREE.MeshPhysicalMaterial({ color: 0xf6c9bb, roughness: 0.15, clearcoat: 1 });
  const add = (x, y, len, r, rz, rx = 0) => {
    const g = fingerGeo(len, r);
    const m = new THREE.Mesh(g, mat); m.position.set(x, y, 0); m.rotation.set(rx, 0, -rz);
    const nail = new THREE.Mesh(new THREE.SphereGeometry(r * 0.52, 20, 12), nailM);
    nail.scale.set(1, 1.3, 0.25); nail.position.set(0, g.userData.top - r * 0.85, r * 0.7); m.add(nail);
    hand.add(m);
    const f = { m, g, base: g.attributes.position.array.slice(), ...g.userData };
    fingers.push(f); return f;
  };
  DEF.forEach(([x, len, r, rz]) => add(x, 1.18 + (Math.abs(x) < 0.2 ? 0.06 : 0), len + 0.2, r, rz));
  add(-0.55, 0.62, 0.62, 0.14, 0.95, 0.15);
  hand.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  hand.userData.fingers = fingers;
  return hand;
}

export function wrinkle(f, k) {
  const p = f.g.attributes.position.array, b = f.base;
  const y0 = f.len * 0.62;
  for (let i = 0; i < p.length; i += 3) {
    const x = b[i], y = b[i + 1], z = b[i + 2];
    const u = (y - y0) / (f.top - y0);
    let s = 1;
    if (u > 0 && k > 0) {
      const mask = Math.min(1, u * 2.5) * (1 - Math.max(0, (u - 0.9) / 0.1));
      const ang = Math.atan2(z, x);
      const ridge = Math.sin(y * 70 + 1.7 * Math.sin(ang * 3 + y * 25));
      s = 1 + k * mask * (0.07 * ridge - 0.045);
    }
    p[i] = x * s; p[i + 1] = y; p[i + 2] = z * s;
  }
  f.g.attributes.position.needsUpdate = true; f.g.computeVertexNormals();
}

export function tipWorld(f) { f.m.updateWorldMatrix(true, false); return v3(0, f.top, 0).applyMatrix4(f.m.matrixWorld); }

// ---------- cerebro
export function makeBrain() {
  const g = new THREE.SphereGeometry(0.62, 128, 80);
  const a = g.attributes.position.array;
  for (let i = 0; i < a.length; i += 3) {
    const x = a[i], y = a[i + 1], z = a[i + 2];
    const n = 1 + 0.06 * Math.sin(x * 24 + Math.sin(y * 10) * 3) * Math.cos(z * 21 + y * 8) + 0.035 * Math.sin(y * 33 + x * 6 + z * 4);
    const gap = 1 - 0.09 * Math.exp(-Math.pow(x / 0.05, 2));
    a[i] = x * 1.22 * n * gap; a[i + 1] = y * 0.92 * n; a[i + 2] = z * 1.08 * n;
  }
  g.computeVertexNormals();
  const m = new THREE.MeshPhysicalMaterial({ color: 0xf08aa3, roughness: 0.32, clearcoat: 0.7, emissive: 0xff4d70, emissiveIntensity: 0 });
  const b = new THREE.Mesh(g, m); b.castShadow = true;
  return b;
}

// ---------- Ojo 3D: cabeza-ojo, bata y cuerpo de tubos
export function makeOjo() {
  const o = new THREE.Group();
  const ink = new THREE.MeshPhysicalMaterial({ color: 0x1d1d22, roughness: 0.4, clearcoat: 0.5 });
  const white = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.12, clearcoat: 1, clearcoatRoughness: 0.05 });
  const coat = new THREE.MeshPhysicalMaterial({ color: 0xf7f7f5, roughness: 0.6, sheen: 0.4, side: THREE.DoubleSide });
  const head = new THREE.Group(); head.position.y = 2.15; o.add(head);
  const eyeball = new THREE.Mesh(new THREE.SphereGeometry(0.62, 64, 48), white); head.add(eyeball);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.035, 12, 64), ink); head.add(ring);
  const iris = new THREE.Mesh(new THREE.SphereGeometry(0.625, 64, 32, 0, Math.PI * 2, 0, 0.5),
    new THREE.MeshPhysicalMaterial({ color: 0xd8232f, roughness: 0.2, clearcoat: 1 }));
  iris.rotation.x = Math.PI / 2; head.add(iris);
  const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.63, 48, 24, 0, Math.PI * 2, 0, 0.22), new THREE.MeshPhysicalMaterial({ color: 0x050505, roughness: 0.05, clearcoat: 1 }));
  pupil.rotation.x = Math.PI / 2; head.add(pupil);
  const glint = new THREE.Mesh(new THREE.SphereGeometry(0.06, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffffff }));
  glint.position.set(0.15, 0.17, 0.6); head.add(glint);
  const lid = new THREE.Mesh(new THREE.SphereGeometry(0.645, 48, 32, 0, Math.PI * 2, 0, Math.PI / 2), white);
  lid.rotation.x = Math.PI / 2; lid.visible = false; head.add(lid);
  // bata (cono abierto) y cuello
  const coatG = new THREE.CylinderGeometry(0.34, 0.62, 1.15, 40, 1, true, 0.35, Math.PI * 2 - 0.7);
  const coatM = new THREE.Mesh(coatG, coat); coatM.position.y = 1.0; o.add(coatM);
  const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.2, 12), ink); torso.position.y = 1.05; o.add(torso);
  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.4, 12), ink); neck.position.y = 1.65; o.add(neck);
  const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.18, 0.02), new THREE.MeshStandardMaterial({ color: 0x2f9e5a })); pocket.position.set(0.24, 1.25, 0.5); o.add(pocket);
  // brazos y piernas
  const limb = (len) => { const g = new THREE.Group(); const m = new THREE.Mesh(new THREE.CapsuleGeometry(0.055, len, 6, 12), ink); m.position.y = -len / 2; g.add(m);
    const hnd = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), ink); hnd.position.y = -len - 0.05; g.add(hnd); return g; };
  const armL = limb(0.85), armR = limb(0.85); armL.position.set(-0.36, 1.5, 0); armR.position.set(0.36, 1.5, 0); o.add(armL, armR);
  const legL = limb(0.75), legR = limb(0.75); legL.position.set(-0.16, 0.48, 0); legR.position.set(0.16, 0.48, 0); o.add(legL, legR);
  [legL, legR].forEach(l => { const shoe = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 12), ink); shoe.scale.set(1, 0.6, 1.6); shoe.position.set(0, -0.82, 0.08); l.add(shoe); });
  o.traverse(m => { if (m.isMesh) m.castShadow = true; });
  o.userData = { head, armL, armR, legL, legR, lid, iris, pupil };
  // animación: pose = {wave, look:[x,y], blink, hop}
  o.userData.anim = (t, { wave = 0, lookX = 0, lookY = 0, surprise = 0, walk = 0 } = {}) => {
    const u = o.userData;
    u.head.rotation.set(-lookY, lookX, 0.05 * Math.sin(t * 1.3));
    u.head.position.y = 2.15 + 0.04 * Math.sin(t * 3) + 0.15 * surprise;
    u.armL.rotation.z = -0.35 - 0.1 * Math.sin(t * 2) - 0.9 * surprise;
    u.armR.rotation.z = 0.35 + wave * (2.3 + 0.35 * Math.sin(t * 12)) + 0.9 * surprise * (1 - wave);
    u.legL.rotation.x = 0.5 * walk * Math.sin(t * 8); u.legR.rotation.x = -0.5 * walk * Math.sin(t * 8);
    const bl = (t % 3.3) < 0.12;
    u.lid.visible = bl;
    const s = 1 + 0.25 * surprise; u.iris.scale.setScalar(1); u.pupil.scale.set(s, s, 1);
  };
  return o;
}
