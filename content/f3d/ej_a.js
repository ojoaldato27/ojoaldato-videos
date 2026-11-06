// EJEMPLO A · «Baño de cine»: mano que sale del agua con salpicón, luz de ventana, vapor, cerebro con impulsos.
import { THREE, setup, ease, clamp, lerp, v3, pop, canvasTex, floaters, makeHand, wrinkle, tipWorld, makeBrain } from './lib3d.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
const { scene, cam, render } = setup({ bg: 0x2a3b48, exposure: 0.95, fog: [7, 18], envI: 0.5, bloom: [0.5, 0.7, 0.8] });

scene.add(new THREE.HemisphereLight(0xbfe3ff, 0x403028, 0.45));
const key = new THREE.DirectionalLight(0xffd9a8, 3.2); key.position.set(-3, 6, -3); key.castShadow = true;
key.shadow.mapSize.set(1024, 1024); Object.assign(key.shadow.camera, { left: -4, right: 4, top: 5, bottom: -3 }); scene.add(key);
const fill = new THREE.DirectionalLight(0x8fc8ff, 1.0); fill.position.set(3, 2, 5); scene.add(fill);

const tiles = canvasTex(256, 256, (x) => { x.fillStyle = '#5f8796'; x.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { x.fillStyle = (i + j) % 2 ? '#9ec4cf' : '#93bac6'; x.fillRect(i * 64 + 3, j * 64 + 3, 58, 58); } }, [12, 7]);
const wall = new THREE.Mesh(new THREE.PlaneGeometry(30, 18), new THREE.MeshStandardMaterial({ map: tiles, roughness: 0.25 }));
wall.position.set(0, 6, -4.5); wall.receiveShadow = true; scene.add(wall);
const win = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 3.6), new THREE.MeshBasicMaterial({ color: 0xfff1cf })); win.position.set(-3.2, 4.4, -4.45); scene.add(win);
// rayo de luz de la ventana
const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 2.4, 9, 32, 1, true), new THREE.MeshBasicMaterial({ color: 0xffe6b0, transparent: true, opacity: 0.07, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
shaft.position.set(-1.2, 2.2, -2.2); shaft.rotation.z = -0.55; shaft.rotation.x = 0.35; scene.add(shaft);

const porcelain = new THREE.MeshPhysicalMaterial({ color: 0xf6f8fa, roughness: 0.12, clearcoat: 1 });
const tub = new THREE.Mesh(new RoundedBoxGeometry(7.6, 1.8, 4.8, 6, 0.7), porcelain); tub.position.set(0, -0.7, -1.0); tub.receiveShadow = true; scene.add(tub);
const WS = 160, wg = new THREE.PlaneGeometry(6.8, 4.0, WS, WS); wg.rotateX(-Math.PI / 2);
const water = new THREE.Mesh(wg, new THREE.MeshPhysicalMaterial({ color: 0x1f7fa8, roughness: 0.03, clearcoat: 1, transparent: true, opacity: 0.9, envMapIntensity: 1.5 }));
water.position.set(0, 0.24, -1.0); water.receiveShadow = true; scene.add(water);
const wb = wg.attributes.position.array.slice();

const hand = makeHand(); scene.add(hand); const F = hand.userData.fingers;
const brain = makeBrain(); scene.add(brain);
const bl = new THREE.PointLight(0xff6a8a, 0, 5); scene.add(bl);
const sparkM = new THREE.MeshBasicMaterial({ color: 0xfff08a });
const sparks = Array.from({ length: 6 }, () => { const s = new THREE.Mesh(new THREE.SphereGeometry(0.05, 12, 8), sparkM); scene.add(s); return s; });
const nerveM = new THREE.MeshBasicMaterial({ color: 0xffd23c, transparent: true, opacity: 0 }); let nerve = null;

// salpicón: gotas con física
const dropM = new THREE.MeshPhysicalMaterial({ color: 0xcfeeff, roughness: 0, clearcoat: 1, transparent: true, opacity: 0.9 });
const N = 90, splash = new THREE.InstancedMesh(new THREE.SphereGeometry(0.045, 12, 8), dropM, N); splash.frustumCulled = false; scene.add(splash);
const sv = Array.from({ length: N }, (_, i) => { const a = i * 2.4, sp = 1.2 + (i * 37 % 100) / 60; return [Math.cos(a) * sp * 0.6, 2.2 + (i * 13 % 10) / 3, Math.sin(a) * sp * 0.6]; });
const steam = floaters(scene, 70, [-3, 3, 0.3, 4.5, -2.5, 1], 0xffffff, 0.45, 0.16);
const dust = floaters(scene, 120, [-3, 3, 0, 6, -3, 2], 0xffe6b0, 0.035, 0.8);

const CK = [[0, v3(0.4, 0.55, 3.2), v3(0, 0.9, -1)], [1.6, v3(1.3, 1.2, 3.0), v3(0.1, 1.6, -1)], [3.4, v3(0.2, 2.0, 2.2), v3(0.4, 2.3, -1)], [5.2, v3(-0.4, 2.45, 1.1), v3(0.1, 2.45, -1)]];
function camAt(t) { let i = 0; while (i < CK.length - 2 && t > CK[i + 1][0]) i++; const [a, p0, l0] = CK[i], [b, p1, l1] = CK[i + 1]; const k = ease(clamp((t - a) / (b - a)));
  cam.position.copy(p0).lerp(p1, k); cam.lookAt(l0.clone().lerp(l1, k)); return cam.position.distanceTo(l0.clone().lerp(l1, k)); }

window.renderAt = function (t) {
  const rise = ease(clamp((t - 0.15) / 0.7));
  hand.position.set(0, lerp(-2.2, 0.15, rise) + 0.03 * Math.sin(t * 1.4), -1.0);
  hand.rotation.set(0.04 * Math.sin(t * 0.9), -0.3 + 0.15 * Math.sin(t * 0.6), 0.03 * Math.sin(t * 1.2));
  const bk = pop(clamp((t - 2.0) / 0.5));
  brain.visible = bk > 0.01; brain.scale.setScalar(Math.max(0.01, bk) * 0.9);
  brain.position.set(1.25, 3.25 + 0.06 * Math.sin(t * 2.2), -1.3); brain.rotation.y = 0.4 + t * 0.5;
  brain.material.emissiveIntensity = bk * (0.3 + 0.3 * Math.sin(t * 11));
  bl.position.copy(brain.position); bl.intensity = 4 * bk;
  const wr = clamp(0.1 + 0.15 * ease(clamp(t / 2)) + 0.8 * ease(clamp((t - 2.7) / 1.4)));
  F.forEach((f, i) => wrinkle(f, wr * (i === 4 ? 0.7 : 1)));
  const tip = tipWorld(F[1]);
  const on = t > 2.3 && t < 4.6;
  if (bk > 0.3) {
    const c = new THREE.CatmullRomCurve3([brain.position.clone().add(v3(-0.4, -0.35, 0.1)), v3(1.0, 2.9, -0.6), v3(0.45, 2.75, -0.8), tip]);
    if (nerve) { nerve.geometry.dispose(); scene.remove(nerve); }
    nerve = new THREE.Mesh(new THREE.TubeGeometry(c, 60, 0.012, 6), nerveM); scene.add(nerve);
    nerveM.opacity = on ? 0.6 * clamp((t - 2.3) / 0.3) : 0;
    sparks.forEach((s, i) => { s.visible = on; s.position.copy(c.getPointAt(Math.max(0, ((t - 2.3) * 0.85 + i / 6) % 1))); s.scale.setScalar(0.8 + 0.5 * Math.sin(t * 20 + i)); });
  } else sparks.forEach(s => s.visible = false);
  // agua con ondas desde la mano
  const a = wg.attributes.position.array;
  for (let i = 0; i < a.length; i += 3) { const x = wb[i], z = wb[i + 2], d = Math.hypot(x, z);
    a[i + 1] = 0.03 * Math.sin(x * 2.1 + t * 1.4) + 0.02 * Math.sin(z * 3 - t * 1.8) + Math.sin(d * 8 - t * 7) * Math.exp(-d * 0.8) * 0.06 * (0.3 + rise); }
  wg.attributes.position.needsUpdate = true; wg.computeVertexNormals();
  // salpicón al salir la mano (0.3–1.6 s)
  const m4 = new THREE.Matrix4(); const ts = t - 0.35;
  for (let i = 0; i < N; i++) { const [vx, vy, vz] = sv[i]; const y = 0.25 + vy * ts - 4.9 * ts * ts;
    m4.makeScale(1, 1.3, 1); m4.setPosition(vx * ts, y, -1.0 + vz * ts); if (ts < 0 || y < 0.2) m4.makeScale(0, 0, 0); splash.setMatrixAt(i, m4); }
  splash.instanceMatrix.needsUpdate = true;
  steam.userData.update(t, 0.25); dust.userData.update(t, 0.05);
  const fd = camAt(t);
  return render(fd);
};
window.READY = true;
