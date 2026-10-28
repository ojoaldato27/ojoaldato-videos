// F1 más realista (Iker, 28/10: «quiero el F1 más real»). Genérico, sin marcas reales.
// Morro hacia +X, ~5,2 m de largo, ruedas en x = 1.55 / -1.45, z = ±0.88 (igual que el coche antiguo, para no solapar).
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

function extrude(pts, depth, bevel = 0.05) {
  const s = new THREE.Shape(pts.map(([x, y]) => new THREE.Vector2(x, y)));
  const g = new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 4, curveSegments: 12 });
  g.translate(0, 0, -depth / 2);
  return g;
}

export function makeCarPro(body, accent, tyreBand = 0xf2c200) {
  const g = new THREE.Group();
  const paint = new THREE.MeshPhysicalMaterial({ color: body, roughness: 0.4, metalness: 0.05, clearcoat: 1, clearcoatRoughness: 0.2, envMapIntensity: 0.55 });
  const paint2 = new THREE.MeshPhysicalMaterial({ color: accent, roughness: 0.35, metalness: 0.1, clearcoat: 0.8 });
  const carbon = new THREE.MeshStandardMaterial({ color: 0x15161a, roughness: 0.55, metalness: 0.3 });
  const rubber = new THREE.MeshStandardMaterial({ color: 0x1b1b1d, roughness: 0.92 });
  const metal = new THREE.MeshStandardMaterial({ color: 0x55585e, roughness: 0.35, metalness: 0.9 });
  const add = (geo, mat, x = 0, y = 0, z = 0) => { const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; g.add(m); return m; };

  // suelo plano y difusor
  add(new RoundedBoxGeometry(3.9, 0.05, 1.55, 2, 0.02), carbon, -0.25, 0.1, 0);
  add(new THREE.BoxGeometry(0.5, 0.18, 1.0), carbon, -2.05, 0.18, 0).rotation.z = -0.25;
  // monocasco + tapa motor con toma de aire
  add(extrude([[-2.15, 0.16], [1.2, 0.16], [1.25, 0.5], [0.6, 0.6], [0.25, 0.62], [-0.35, 0.66], [-0.55, 1.0], [-0.95, 1.0],
               [-1.9, 0.6], [-2.15, 0.42]], 0.46, 0.07), paint, 0, 0, 0);
  // aleta de tiburón
  add(extrude([[-0.95, 0.98], [-2.0, 0.62], [-2.0, 0.98]], 0.02, 0), paint2, 0, 0, 0);
  // morro afilado que cae hacia delante
  const nose = add(new THREE.CylinderGeometry(0.06, 0.27, 1.45, 20), paint, 1.9, 0.38, 0);
  nose.rotation.z = -Math.PI / 2 - 0.08; nose.scale.set(1, 1, 0.62);
  // pontones con forma de botella de cola
  for (const s of [-1, 1]) {
    const sp = add(extrude([[0.85, 0.2], [0.85, 0.5], [0.45, 0.6], [-0.7, 0.56], [-1.6, 0.3], [-1.75, 0.2]], 0.36, 0.08), paint, 0, 0, s * 0.62);
    add(new RoundedBoxGeometry(0.06, 0.24, 0.3, 2, 0.03), carbon, 0.92, 0.42, s * 0.62);   // toma
    add(new THREE.BoxGeometry(0.06, 0.06, 0.12), carbon, 0.55, 0.78, s * 0.42);             // retrovisor
  }
  // piloto y halo
  const helmet = add(new THREE.SphereGeometry(0.17, 24, 16), paint2, 0.05, 0.78, 0);
  add(new THREE.SphereGeometry(0.172, 24, 8, -0.9, 1.8, 1.2, 0.45), new THREE.MeshStandardMaterial({ color: 0x0e0e10, roughness: 0.1, metalness: 0.6 }), 0.05, 0.78, 0).rotation.y = 0;
  const halo = add(new THREE.TorusGeometry(0.3, 0.035, 10, 32, Math.PI), carbon, 0.15, 0.78, 0);
  halo.rotation.set(Math.PI / 2, 0, Math.PI / 2);
  add(new THREE.CylinderGeometry(0.03, 0.03, 0.2, 8), carbon, 0.45, 0.7, 0).rotation.z = 0.5;
  // alerón delantero: plano principal + 2 flaps + derivas
  add(new RoundedBoxGeometry(0.42, 0.03, 1.95, 2, 0.012), carbon, 2.6, 0.1, 0);
  for (const [dx, dy, r] of [[-0.06, 0.15, 0.25], [-0.14, 0.2, 0.45]]) add(new RoundedBoxGeometry(0.26, 0.025, 1.9, 2, 0.01), paint, 2.6 + dx, dy, 0).rotation.z = r;
  for (const s of [-1, 1]) add(new RoundedBoxGeometry(0.55, 0.24, 0.025, 2, 0.01), paint2, 2.55, 0.18, s * 0.98);
  // alerón trasero: plano + flap + beam wing + derivas + soporte
  add(new RoundedBoxGeometry(0.36, 0.04, 1.12, 2, 0.015), carbon, -2.28, 0.96, 0).rotation.z = 0.12;
  add(new RoundedBoxGeometry(0.26, 0.03, 1.12, 2, 0.012), paint, -2.12, 1.08, 0).rotation.z = 0.45;
  add(new RoundedBoxGeometry(0.28, 0.03, 0.9, 2, 0.012), carbon, -2.2, 0.45, 0);
  for (const s of [-1, 1]) add(new RoundedBoxGeometry(0.62, 0.62, 0.025, 2, 0.01), paint2, -2.2, 0.82, s * 0.57);
  add(new THREE.BoxGeometry(0.05, 0.4, 0.05), carbon, -2.0, 0.78, 0);
  // ---- detalle extra (Iker 28/10: «real pero más detallado») ----
  const live = new THREE.MeshPhysicalMaterial({ color: accent === 0x15161a ? 0xffffff : accent, roughness: 0.3, clearcoat: 1 });
  // franjas de decoración: a lo largo de pontones y tapa motor
  for (const s of [-1, 1]) {
    add(extrude([[0.7, 0.5], [0.35, 0.58], [-0.75, 0.54], [-1.55, 0.3], [-1.45, 0.27], [-0.75, 0.47], [0.35, 0.5]], 0.02, 0), live, 0, 0.01, s * 0.83);
    // pared lateral del suelo y deflectores
    add(new RoundedBoxGeometry(2.2, 0.12, 0.03, 2, 0.01), carbon, -0.3, 0.17, s * 0.78);
    for (const dx of [0.95, 1.05, 1.15]) add(new RoundedBoxGeometry(0.06, 0.26, 0.02, 2, 0.008), carbon, dx, 0.26, s * 0.45);
    // escapes / luces y antenas
    add(new THREE.CylinderGeometry(0.012, 0.012, 0.22, 6), carbon, -0.6, 1.1, s * 0.06);
  }
  add(extrude([[-0.6, 1.005], [-1.85, 0.66], [-1.75, 0.63], [-0.65, 0.98]], 0.25, 0.01), live, 0, 0, 0);   // franja tapa motor
  // cámara de TV sobre la toma de aire
  add(new RoundedBoxGeometry(0.16, 0.05, 0.08, 2, 0.02), paint2, -0.7, 1.05, 0);
  // número en el morro (genérico)
  {
    const c = document.createElement('canvas'); c.width = 128; c.height = 64; const x = c.getContext('2d');
    x.fillStyle = '#fff'; x.font = '900 52px Inter, Arial'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText('27', 64, 34);
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
    const num = add(new THREE.PlaneGeometry(0.34, 0.17), new THREE.MeshBasicMaterial({ map: tex, transparent: true }), 1.75, 0.495, 0);
    num.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); num.rotation.x = -Math.PI / 2 + 0.0;
    num.rotateX(0.1);
  }
  // luz de lluvia roja detrás
  add(new THREE.BoxGeometry(0.03, 0.06, 0.12), new THREE.MeshBasicMaterial({ color: 0xff2a2a }), -2.36, 0.45, 0);
  // ruedas (neumático con hombro redondeado, banda de color, llanta)
  g.userData.wheels = [];
  for (const [x, z] of [[1.55, 0.88], [1.55, -0.88], [-1.45, 0.9], [-1.45, -0.9]]) {
    const w = x > 0 ? 0.34 : 0.42, R = 0.36;
    const prof = [[0.21, -w / 2], [0.32, -w / 2], [0.355, -w / 2 + 0.04], [R, -w / 2 + 0.09], [R, w / 2 - 0.09], [0.355, w / 2 - 0.04], [0.32, w / 2], [0.21, w / 2]]
      .map(([r, y]) => new THREE.Vector2(r, y));
    const wheel = new THREE.Group(); wheel.position.set(x, R, z); g.add(wheel);
    const tm = rubber.clone();
    const tyre = new THREE.Mesh(new THREE.LatheGeometry(prof, 40), tm); tyre.rotation.x = Math.PI / 2; tyre.castShadow = true; wheel.add(tyre);
    for (const sd of [-1, 1]) {
      const band = new THREE.Mesh(new THREE.RingGeometry(0.27, 0.295, 40), new THREE.MeshStandardMaterial({ color: tyreBand, roughness: 0.6, side: THREE.DoubleSide }));
      band.position.z = sd * (w / 2 + 0.002); wheel.add(band);
      const cover = new THREE.Mesh(new THREE.CircleGeometry(0.21, 32), metal); cover.position.z = sd * (w / 2 - 0.02);
      if (sd < 0) cover.rotation.y = Math.PI; wheel.add(cover);
      for (let k = 0; k < 10; k++) {   // radios
        const sp = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.17, 0.01), carbon);
        sp.position.set(Math.cos(k * 0.628) * 0.1, Math.sin(k * 0.628) * 0.1, sd * (w / 2 - 0.015)); sp.rotation.z = k * 0.628 - Math.PI / 2; wheel.add(sp);
      }
      const hub = new THREE.Mesh(new THREE.CircleGeometry(0.05, 16), paint2); hub.position.z = sd * (w / 2 - 0.01); if (sd < 0) hub.rotation.y = Math.PI; wheel.add(hub);
    }
    // brazos de suspensión
    for (const dy of [-0.06, 0.08]) {
      const a = new THREE.Vector3(x * 0.92, R + dy, Math.sign(z) * 0.28), b = new THREE.Vector3(x, R + dy * 0.5, z * 0.82);
      const arm = add(new THREE.CylinderGeometry(0.018, 0.018, a.distanceTo(b), 6), carbon, (a.x + b.x) / 2, (a.y + b.y) / 2, (a.z + b.z) / 2);
      arm.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
    }
    wheel.userData.mat = tm;
    g.userData.wheels.push(wheel);
  }
  return g;
}
