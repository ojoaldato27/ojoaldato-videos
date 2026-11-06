// EJEMPLO D · «Ojo en 3D»: el presentador del canal como personaje 3D, vuelta completa, saludo y mirada a cámara.
import { THREE, setup, ease, clamp, lerp, v3, pop, floaters, makeOjo, canvasTex } from './lib3d.js';
const { scene, cam, render } = setup({ bg: 0x23324a, exposure: 0.8, envI: 0.45, bloom: [0.22, 0.5, 0.93] });
scene.add(new THREE.HemisphereLight(0xcfe4ff, 0x2a2030, 0.6));
const key = new THREE.DirectionalLight(0xfff0dd, 2.6); key.position.set(3, 6, 4); key.castShadow = true; key.shadow.mapSize.set(1024, 1024); scene.add(key);
const rim = new THREE.DirectionalLight(0x7fc0ff, 2.0); rim.position.set(-4, 3, -4); scene.add(rim);
// plataforma y laboratorio desenfocado
const plat = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.7, 0.25, 64), new THREE.MeshPhysicalMaterial({ color: 0xe8edf3, roughness: 0.2, clearcoat: 1 }));
plat.position.y = -0.13; plat.receiveShadow = true; scene.add(plat);
const ringL = new THREE.Mesh(new THREE.TorusGeometry(1.62, 0.025, 8, 96), new THREE.MeshBasicMaterial({ color: 0xff3344 })); ringL.rotation.x = Math.PI / 2; ringL.position.y = 0.0; scene.add(ringL);
const board = canvasTex(512, 256, (x) => { x.fillStyle = '#9fb0c4'; x.fillRect(0, 0, 512, 256); x.strokeStyle = '#3b6fd0'; x.lineWidth = 6;
  for (let j = 0; j < 5; j++) { x.beginPath(); x.moveTo(30, 40 + j * 42); x.lineTo(220 + (j * 67) % 200, 40 + j * 42); x.stroke(); }
  x.strokeStyle = '#e04a4a'; x.beginPath(); x.arc(400, 120, 60, 0, 7); x.stroke(); });
const wb = new THREE.Mesh(new THREE.PlaneGeometry(5, 2.5), new THREE.MeshStandardMaterial({ map: board })); wb.position.set(-1.5, 3.3, -5); scene.add(wb);
for (let i = 0; i < 9; i++) { const c = [0x6fd0a0, 0xffb060, 0x80a8ff, 0xff7aa0][i % 4];
  const f = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.7, 24), new THREE.MeshPhysicalMaterial({ color: c, transparent: true, opacity: 0.8, roughness: 0.1, emissive: c, emissiveIntensity: 0.25 }));
  f.position.set(-4 + i * 1.0, 1.2 + (i % 2) * 0.1, -4.6); scene.add(f); }
const ojo = makeOjo(); scene.add(ojo);
const sparkle = floaters(scene, 90, [-4, 4, 0, 5, -4, 2], 0xffffff, 0.05, 0.8);
window.renderAt = function (t) {
  const appear = pop(clamp(t / 0.6));
  ojo.scale.setScalar(Math.max(0.01, appear));
  ojo.position.y = 0.0 + 0.25 * Math.max(0, Math.sin(Math.PI * clamp((t - 3.3) / 0.5)));
  ojo.rotation.y = lerp(0, Math.PI * 2, ease(clamp((t - 0.6) / 2.6)));
  ojo.userData.anim(t, { wave: clamp((t - 3.9) / 0.3), lookX: 0.15 * Math.sin(t * 1.5) * (t < 3.6 ? 1 : 0), surprise: Math.max(0, Math.sin(Math.PI * clamp((t - 3.3) / 0.5))) });
  sparkle.userData.update(t, 0.08);
  const k = ease(clamp(t / 5.5));
  cam.position.set(lerp(2.8, 0.8, k), lerp(2.0, 2.4, k), lerp(6.2, 4.6, k));
  cam.lookAt(0, 1.5, 0);
  return render(cam.position.distanceTo(v3(0, 1.6, 0)));
};
window.READY = true;
