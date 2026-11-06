// Escena «mano que sale del agua» con 3 estilos: 'clay' (plastilina stop-motion), 'toon' (dibujo animado 3D con contorno),
// 'diorama' (baño en miniatura flotando, con Ojo). Uso: import { run } from './bath_scene.js'; run('clay')
import { THREE, setup, ease, clamp, lerp, v3, pop, canvasTex, floaters, makeHand, wrinkle, tipWorld, makeBrain, makeOjo } from './lib3d.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

// contorno negro de dibujo animado (casco invertido que sigue a la geometría, también cuando se deforma)
function outlineMat(th = 0.02) {
  return new THREE.ShaderMaterial({
    side: THREE.BackSide,
    vertexShader: `uniform float th; void main(){ vec3 p = position + normal * th; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
    fragmentShader: `void main(){ gl_FragColor = vec4(0.07,0.06,0.09,1.0); }`,
    uniforms: { th: { value: th } }
  });
}
function addOutlines(root, th) {
  const list = []; root.traverse(o => { if (o.isMesh && !o.userData.noOutline) list.push(o); });
  list.forEach(o => { const m = new THREE.Mesh(o.geometry, outlineMat(th)); m.userData.noOutline = true; o.add(m); });
}

const clayBump = canvasTex(256, 256, (x) => {
  const id = x.createImageData(256, 256);
  for (let i = 0; i < 256 * 256; i++) { const px = i % 256, py = (i / 256) | 0;
    const v = 128 + 40 * Math.sin(px * 0.21 + Math.sin(py * 0.13) * 3) * Math.sin(py * 0.17) + (Math.random() - 0.5) * 50;
    id.data[i * 4] = id.data[i * 4 + 1] = id.data[i * 4 + 2] = v; id.data[i * 4 + 3] = 255; }
  x.putImageData(id, 0, 0);
}, [3, 3]);
const feltBump = canvasTex(256, 256, (x) => {
  const id = x.createImageData(256, 256);
  for (let i = 0; i < 256 * 256; i++) { const v = 110 + Math.random() * 120; id.data[i * 4] = id.data[i * 4 + 1] = id.data[i * 4 + 2] = v; id.data[i * 4 + 3] = 255; }
  x.putImageData(id, 0, 0);
  for (let i = 0; i < 900; i++) { x.strokeStyle = `rgba(255,255,255,${Math.random() * 0.5})`; x.beginPath(); const a = Math.random() * 256, b = Math.random() * 256; x.moveTo(a, b); x.quadraticCurveTo(a + 6, b - 4, a + Math.random() * 16 - 8, b + Math.random() * 16 - 8); x.stroke(); }
}, [4, 4]);
const toonGrad = (() => { const d = new Uint8Array([70, 160, 255]); const t = new THREE.DataTexture(d, 3, 1, THREE.RedFormat); t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t; })();

export function run(style) {
  const S = {
    clay: { bg: 0xe9d2b0, exposure: 1.0, envI: 0.25, bloom: [0.05, 0.3, 0.95], fog: [8, 20] },
    toon: { bg: 0x7fd3f0, exposure: 1.0, envI: 0.2, bloom: [0.1, 0.3, 0.95], fog: null },
    felt: { bg: 0xcdb8e0, exposure: 1.0, envI: 0.2, bloom: [0.05, 0.3, 0.95], fog: [8, 20] },
    diorama: { bg: 0xf2c9a0, exposure: 1.0, envI: 0.55, bloom: [0.25, 0.5, 0.9], fog: null },
  }[style];
  const { scene, cam, render, bokeh } = setup(S);
  const M = (color, extra = {}) => {
    if (style === 'clay') return new THREE.MeshStandardMaterial({ color, roughness: 0.92, metalness: 0, bumpMap: clayBump, bumpScale: 1.6, ...extra });
    if (style === 'toon') return new THREE.MeshToonMaterial({ color, gradientMap: toonGrad, ...extra });
    if (style === 'felt') return new THREE.MeshPhysicalMaterial({ color, roughness: 1, sheen: 1, sheenRoughness: 0.75, sheenColor: new THREE.Color(0xffffff), bumpMap: feltBump, bumpScale: 2.2, ...extra });
    return new THREE.MeshPhysicalMaterial({ color, roughness: 0.35, clearcoat: 0.4, ...extra });
  };
  scene.add(new THREE.HemisphereLight(0xffffff, style === 'toon' ? 0x8899aa : 0x6a5040, style === 'toon' ? 1.4 : 0.6));
  const key = new THREE.DirectionalLight(0xfff0d8, style === 'toon' ? 2.2 : 3.0); key.position.set(-3, 7, 4); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024); Object.assign(key.shadow.camera, { left: -6, right: 6, top: 7, bottom: -4 }); key.shadow.bias = -0.0008; scene.add(key);
  const world = new THREE.Group(); scene.add(world);

  // pared, suelo, bañera
  const tileC = style === 'felt' ? ['#7b6aa8', '#c9b6e6', '#b9a3dc'] : style === 'toon' ? ['#3fb8e8', '#7fd8f7', '#66cdf2'] : style === 'clay' ? ['#7aa6a8', '#b9d6d2', '#a9cbc6'] : ['#6c9fb0', '#cfe7ee', '#bcdde6'];
  const tiles = canvasTex(256, 256, (x) => { x.fillStyle = tileC[0]; x.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { x.fillStyle = (i + j) % 2 ? tileC[1] : tileC[2]; x.beginPath(); x.roundRect(i * 64 + 4, j * 64 + 4, 56, 56, 10); x.fill(); } }, [8, 5]);
  const wallM = style === 'felt' ? new THREE.MeshPhysicalMaterial({ map: tiles, roughness: 1, sheen: 1, sheenRoughness: 0.8, sheenColor: new THREE.Color(0xffffff), bumpMap: feltBump, bumpScale: 1.5 }) : style === 'clay' ? new THREE.MeshStandardMaterial({ map: tiles, roughness: 0.95, bumpMap: clayBump, bumpScale: 1 }) : style === 'toon' ? new THREE.MeshToonMaterial({ map: tiles, gradientMap: toonGrad }) : new THREE.MeshStandardMaterial({ map: tiles, roughness: 0.3 });
  const WW = style === 'diorama' ? 8 : 30;
  const wall = new THREE.Mesh(new THREE.BoxGeometry(WW, style === 'diorama' ? 5 : 18, 0.3), wallM); wall.position.set(0, style === 'diorama' ? 1.2 : 6, -4.2); wall.receiveShadow = true; world.add(wall);
  const floorM = M(style === 'toon' ? 0xffc46b : 0xb58c63);
  const floor = new THREE.Mesh(new THREE.BoxGeometry(WW, 0.6, style === 'diorama' ? 8 : 30), floorM); floor.position.set(0, -1.6, 0); floor.receiveShadow = true; world.add(floor);
  if (style === 'diorama') {        // bloque de tierra bajo el suelo y pared lateral: maqueta flotando
    const dirt = new THREE.Mesh(new THREE.BoxGeometry(8, 2.2, 8), M(0x8a5a3a)); dirt.position.set(0, -3.0, 0); world.add(dirt);
    const side = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5, 8), wallM); side.position.set(-4.0, 1.2, 0); side.receiveShadow = true; world.add(side);
    const mat = new THREE.Mesh(new RoundedBoxGeometry(2.2, 0.06, 1.3, 2, 0.03), M(0xff8a8a)); mat.position.set(1.2, -1.27, 2.2); world.add(mat);
  }
  const tub = new THREE.Mesh(new RoundedBoxGeometry(7.4, 1.8, 4.6, 6, 0.7), M(0xfafafa, style === 'toon' ? {} : { roughness: style === 'clay' ? 0.9 : 0.12 }));
  tub.position.set(0, -0.6, -1.4); tub.castShadow = tub.receiveShadow = true; world.add(tub);
  if (style === 'diorama') { tub.scale.set(0.78, 0.78, 0.78); tub.position.set(0.3, -0.6, -1.9); }
  const WS = 110, wg = new THREE.PlaneGeometry(style === 'diorama' ? 5.2 : 6.6, style === 'diorama' ? 2.9 : 3.8, WS, WS); wg.rotateX(-Math.PI / 2);
  const waterM = style === 'felt' ? M(0x3fa7d6) : style === 'clay' ? new THREE.MeshStandardMaterial({ color: 0x4fb0c8, roughness: 0.55, bumpMap: clayBump, bumpScale: 0.8 })
    : style === 'toon' ? new THREE.MeshToonMaterial({ color: 0x2aa0e0, gradientMap: toonGrad })
    : new THREE.MeshPhysicalMaterial({ color: 0x2a8fbf, roughness: 0.03, clearcoat: 1, transparent: true, opacity: 0.9 });
  const water = new THREE.Mesh(wg, waterM); water.position.set(tub.position.x, 0.3 * tub.scale.y - 0.02, tub.position.z); water.receiveShadow = true; world.add(water);
  const wb = wg.attributes.position.array.slice();

  const hand = makeHand(M(style === 'toon' ? 0xffb38a : style === 'clay' ? 0xe9a98a : 0xe8a27f)); world.add(hand); const F = hand.userData.fingers;
  const brain = makeBrain(); brain.material = M(0xff8fb0, style === 'diorama' ? { emissive: 0xff4d70, emissiveIntensity: 0 } : {}); world.add(brain);
  const duck = new THREE.Group(); world.add(duck);
  const y = M(0xffcc22); const db = new THREE.Mesh(new THREE.SphereGeometry(0.42, 32, 20), y); db.scale.set(1.3, 0.8, 1); duck.add(db);
  const dh = new THREE.Mesh(new THREE.SphereGeometry(0.27, 32, 20), y); dh.position.set(0.35, 0.42, 0); duck.add(dh);
  const bk = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.25, 16), M(0xff7a1a)); bk.rotation.z = -Math.PI / 2; bk.position.set(0.66, 0.4, 0); duck.add(bk);
  [-0.12, 0.12].forEach(zz => { const e = new THREE.Mesh(new THREE.SphereGeometry(0.045, 10, 8), new THREE.MeshBasicMaterial({ color: 0x111111 })); e.userData.noOutline = true; e.position.set(0.52, 0.52, zz); duck.add(e); });
  let ojo = null;
  if (style === 'diorama' || style === 'toon') { ojo = makeOjo(); world.add(ojo); if (style === 'toon') ojo.traverse(o => { if (o.isMesh && o.material && o.material.color && !o.userData.keep) { const c = o.material.color.getHex(); o.material = M(c); } }); }
  // gotas
  const dropM = style === 'toon' ? new THREE.MeshToonMaterial({ color: 0xbfeaff, gradientMap: toonGrad }) : M(0xbfe6ff, style === 'clay' ? {} : { roughness: 0, transparent: true, opacity: 0.9 });
  const drops = Array.from({ length: 8 }, () => { const d = new THREE.Mesh(new THREE.SphereGeometry(0.06, 14, 10), dropM); d.scale.set(1, 1.35, 1); world.add(d); return d; });
  const sparks = Array.from({ length: 6 }, () => { const s = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 8), new THREE.MeshBasicMaterial({ color: 0xfff27a })); s.userData.noOutline = true; world.add(s); return s; });
  if (style === 'toon') { addOutlines(world, 0.025); }
  const dust = floaters(scene, 60, [-4, 4, -1, 5, -4, 2], style === 'clay' ? 0xffffff : 0xfff6dd, 0.06, style === 'toon' ? 0.0 : 0.5);

  window.renderAt = function (t) {
    if (style === 'clay') t = Math.floor(t * 12) / 12;          // stop-motion: 12 posturas por segundo
    const rise = ease(clamp((t - 0.15) / 0.8));
    const hs = style === 'diorama' ? 0.62 : 1;
    hand.scale.setScalar(hs);
    hand.position.set(tub.position.x - (style === 'diorama' ? 0.6 : 0), water.position.y + lerp(-2.4, 0.1, rise) * hs - 0.1, tub.position.z + 0.2);
    hand.rotation.set(0.04 * Math.sin(t * 0.9), -0.3 + 0.15 * Math.sin(t * 0.6), 0.03 * Math.sin(t * 1.2) + (style === 'toon' ? 0.08 * Math.sin(t * 3) : 0));
    const bkk = pop(clamp((t - 2.0) / 0.5));
    brain.visible = bkk > 0.01; brain.scale.setScalar(Math.max(0.01, bkk) * 0.8 * hs);
    brain.position.set(hand.position.x + 1.05 * hs, water.position.y + 2.75 * hs + 0.08 * Math.sin(t * 2.2), hand.position.z + 0.1); brain.rotation.y = 0.4 + t * 0.5;
    if (brain.material.emissive) brain.material.emissiveIntensity = bkk * (0.2 + 0.2 * Math.sin(t * 11));
    const wr = clamp(0.1 + 0.15 * ease(clamp(t / 2)) + 0.85 * ease(clamp((t - 2.7) / 1.3)));
    F.forEach((f, i) => wrinkle(f, wr * (i === 4 ? 0.7 : 1) * (style === 'toon' ? 1.2 : 1)));
    const tip = tipWorld(F[1]);
    const on = t > 2.3 && t < 4.8 && bkk > 0.3;
    if (bkk > 0.3) { const c = new THREE.CatmullRomCurve3([brain.position.clone(), brain.position.clone().lerp(tip, 0.5).add(v3(0, 0.4, 0.2)), tip]);
      sparks.forEach((s, i) => { s.visible = on; s.position.copy(c.getPointAt(Math.max(0, ((t - 2.3) * 0.9 + i / 6) % 1))); }); }
    else sparks.forEach(s => s.visible = false);
    const a = wg.attributes.position.array, amp = style === 'clay' ? 1.8 : 1;
    for (let i = 0; i < a.length; i += 3) { const x = wb[i], z = wb[i + 2], d = Math.hypot(x + 0.0, z - 0.2);
      a[i + 1] = amp * (0.03 * Math.sin(x * 2.1 + t * 1.4) + 0.02 * Math.sin(z * 3 - t * 1.8) + Math.sin(d * 8 - t * 7) * Math.exp(-d * 0.8) * 0.06 * (0.3 + rise)); }
    wg.attributes.position.needsUpdate = true; wg.computeVertexNormals();
    drops.forEach((d, i) => { const tp = tipWorld(F[i % 4]); const per = 0.9 + (i % 3) * 0.17, ph = ((t + i * 0.31) % per) / per;
      d.position.set(tp.x, tp.y - 0.05 - 2.4 * hs * ph * ph, tp.z + 0.05); d.visible = t > 0.8 && d.position.y > water.position.y; });
    duck.position.set(tub.position.x - 1.9 * hs * (style === 'diorama' ? 1.2 : 1), water.position.y + 0.12 + 0.05 * Math.sin(t * 2.3), tub.position.z + 0.6);
    duck.scale.setScalar(hs); duck.rotation.set(0.08 * Math.sin(t * 2.1), 0.6 + 0.3 * Math.sin(t * 0.4), 0.06 * Math.sin(t * 1.7));
    if (ojo) {
      if (style === 'diorama') { ojo.scale.setScalar(0.5); ojo.position.set(2.0, -1.3, 1.4); ojo.rotation.y = 0.3; }
      else { ojo.scale.setScalar(0.55); ojo.position.set(2.15, water.position.y + 0.35, -0.2); ojo.rotation.y = -0.6; }
      const sur = t > 2.7 ? Math.max(0, Math.sin(Math.PI * clamp((t - 2.7) / 0.6))) : 0;
      ojo.userData.anim(t, { surprise: sur, lookX: -0.4, lookY: -0.15, wave: clamp((t - 4.6) / 0.3) });
    }
    dust.userData.update(t, 0.08);
    let look, pos;
    const k = ease(clamp(t / 5.6));
    if (style === 'diorama') { const ang = lerp(0.75, 0.25, k); cam.fov = 18; cam.updateProjectionMatrix();
      pos = v3(Math.sin(ang) * 21, lerp(12, 8.5, k), Math.cos(ang) * 21); look = v3(0.6, -0.4, -0.4); world.rotation.y = 0;
      if (bokeh) { bokeh.uniforms.aperture.value = 0.02; bokeh.uniforms.maxblur.value = 0.012; } }
    else { pos = v3(lerp(1.4, 0.3, k), lerp(1.0, 2.2, k), lerp(4.4, 2.6, k)); look = v3(hand.position.x + 0.35, lerp(1.1, 2.3, k), hand.position.z); }
    cam.position.copy(pos); cam.lookAt(look);
    return render(pos.distanceTo(look));
  };
  window.READY = true;
}
