// EJEMPLO C · «Cámara superlenta»: estornudo congelado, cientos de gotas brillando a contraluz, cámara que viaja entre ellas.
import { THREE, setup, ease, clamp, lerp, v3, pop, floaters, skinMat } from './lib3d.js';
const { scene, cam, render } = setup({ bg: 0x070a14, exposure: 1.05, envI: 0.3, bloom: [0.55, 0.5, 0.72] });
scene.add(new THREE.HemisphereLight(0x5f7fbf, 0x050508, 0.35));
const rimL = new THREE.SpotLight(0x9fd0ff, 120, 30, 0.5, 0.6); rimL.position.set(6, 3, -5); rimL.target.position.set(1, 1.8, 0); scene.add(rimL, rimL.target);
const keyL = new THREE.DirectionalLight(0xffe0c0, 1.6); keyL.position.set(-3, 4, 5); scene.add(keyL);
// cabeza estilizada de perfil
const skin = skinMat();
const head = new THREE.Group(); scene.add(head);
const hg = new THREE.SphereGeometry(1, 64, 48); hg.scale(1.0, 1.15, 0.95); head.add(new THREE.Mesh(hg, skin));
const nose = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.55, 32), skin); nose.rotation.z = -Math.PI / 2 - 0.3; nose.position.set(1.05, 0.05, 0); head.add(nose);
const hair = new THREE.Mesh(new THREE.SphereGeometry(1.03, 48, 32, 0, Math.PI * 2, 0, 1.2), new THREE.MeshPhysicalMaterial({ color: 0x3a2418, roughness: 0.6 }));
hair.rotation.z = 0.35; head.add(hair);
const lidM = new THREE.MeshPhysicalMaterial({ color: 0x3a2418 });
const lid = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.025, 8, 24, Math.PI), lidM); lid.position.set(0.82, 0.32, 0.42); lid.rotation.set(0, -0.6, Math.PI); head.add(lid);
const mouth = new THREE.Mesh(new THREE.SphereGeometry(0.16, 24, 16), new THREE.MeshPhysicalMaterial({ color: 0x6a1a26 })); mouth.scale.set(0.6, 1, 1); mouth.position.set(0.92, -0.42, 0.1); head.add(mouth);
const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.9, 1.2, 12, 32), new THREE.MeshPhysicalMaterial({ color: 0x2f6fd0, roughness: 0.55, sheen: 0.5 }));
body.position.set(-0.2, -2.3, 0); scene.add(body);
head.position.set(0, 0.2, 0); head.rotation.z = 0.12;
// gotas
const N = 700;
const drops = new THREE.InstancedMesh(new THREE.SphereGeometry(0.045, 12, 8), new THREE.MeshPhysicalMaterial({ color: 0x8fd0ff, roughness: 0, clearcoat: 1, transparent: true, opacity: 0.75, envMapIntensity: 2.5 }), N);
drops.frustumCulled = false; scene.add(drops);
const dv = Array.from({ length: N }, (_, i) => {
  const a = (i * 2.399) % (Math.PI * 2), r = Math.sqrt((i % 97) / 97);
  const sp = 0.15 + ((i * 53) % 100) / 45;
  const big = (i % 11 === 0) ? 1.7 : 0.35 + (i % 5) * 0.18;
  return { d: v3(1, r * 0.85 * Math.sin(a), r * 0.85 * Math.cos(a)).normalize(), sp, big };
});
const mist = floaters(scene, 160, [0.8, 7, -1.6, 1.4, -1.4, 1.4], 0xbfe0ff, 0.22, 0.12);
window.renderAt = function (t) {
  // cámara superlenta: la nube avanza muy despacio
  const ts = Math.max(0, t - 0.4) * 0.55;
  const m4 = new THREE.Matrix4(), o = v3(1.0, -0.25, 0.1);
  for (let i = 0; i < N; i++) { const { d, sp, big } = dv[i]; const dist = sp * ts * 1.7;
    const p = o.clone().addScaledVector(d, dist); p.y -= 0.12 * dist * dist * (big > 2 ? 1.6 : 0.5);
    const s = t < 0.4 ? 0 : big * (1 + 0.15 * Math.sin(t * 3 + i)); m4.makeScale(s, s * 1.15, s); m4.setPosition(p.x, p.y, p.z); drops.setMatrixAt(i, m4); }
  drops.instanceMatrix.needsUpdate = true;
  mouth.scale.set(0.6, 1 + 0.6 * pop(clamp((t - 0.2) / 0.3)), 1);
  head.rotation.z = 0.12 - 0.18 * ease(clamp((t - 0.1) / 0.4));
  mist.userData.update(t, 0.02);
  const cx = 1.0 + 1.7 * ts;
  cam.position.set(cx - 1.4, 0.35 - 0.05 * t, 4.2 - 0.25 * t);
  cam.lookAt(cx + 0.2, -0.3, 0);
  return render(cam.position.distanceTo(v3(cx + 0.2, -0.3, 0)));
};
window.READY = true;
