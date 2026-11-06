"""Clips animados de 5-6 s de cada estilo (Iker 06/11). Uso: python3 blender_clips.py <carpeta> <prefijo_estilo> [fps dur ancho alto muestras]"""
import sys, os, math, runpy, subprocess
out, pref = sys.argv[1], sys.argv[2]
FPS = int(sys.argv[3]) if len(sys.argv) > 3 else 12
DUR = float(sys.argv[4]) if len(sys.argv) > 4 else 5.5
RW, RH, SAMP = (int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])) if len(sys.argv) > 7 else (432, 768, 10)
os.environ["CLIPS"] = "1"
here = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["x", out, str(RW), str(RH), str(SAMP)]
G = runpy.run_path(os.path.join(here, "blender_styles.py"))
import bpy
from mathutils import Vector
sc = bpy.context.scene
name, fn = next((n, f) for n, f in G["STYLES"] if n.startswith(pref))
G["reset"](); fn()
hand, brain, d1, d2, beak, water, cam, tgt = (G[k] for k in ("hand", "brain", "d1", "d2", "beak", "water", "cam", "tgt"))
# agua que se mueve: textura ligada a un vacío que se desplaza
emp = bpy.data.objects.new("wv", None); sc.collection.objects.link(emp)
wd = water.modifiers["d"]; wd.texture_coords = "OBJECT"; wd.texture_coords_object = emp
# gotas que caen de las yemas
wmat = water.data.materials[0] if water.data.materials else None
drops = []
for i in range(5):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.045, location=(0, 0, -5), segments=16, ring_count=10)
    o = bpy.context.object; o.scale = (1, 1, 1.35)
    if wmat: o.data.materials.append(wmat)
    drops.append(o)
wr_nodes = [n for m in hand.data.materials for n in m.node_tree.nodes if n.label == "wr"]
wr0 = [n.inputs["Strength"].default_value for n in wr_nodes]
B0 = Vector(brain.scale); H0 = Vector(hand.location); C1 = Vector(cam.location); T1 = Vector(tgt.location)
C0 = C1 + Vector((0.9, -1.4, -0.4)); T0 = T1 + Vector((0, 0, -0.5))
D1, D2, DB = Vector(d1.location), Vector(d2.location), Vector(beak.location)
TIPS = [(-0.38, 1.85), (-0.15, 2.05), (0.15, 2.0), (0.4, 1.75)]


def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def pop(k):
    if k <= 0: return 0.0
    if k >= 1: return 1.0
    return 1 + 2.7 * (k - 1) ** 3 + 1.7 * (k - 1) ** 2


frames = os.path.join(out, "fr_" + pref); os.makedirs(frames, exist_ok=True)
N = int(DUR * FPS)
for f in range(N):
    t = f / FPS
    rise = ease((t - 0.1) / 1.0)
    hand.location = H0 + Vector((0, 0, -1.9 * (1 - rise) + 0.03 * math.sin(t * 1.6)))
    hand.rotation_euler[2] = math.radians(-10) + 0.06 * math.sin(t * 1.1)
    k = ease((t - 1.9) / 1.6)
    for n, w0 in zip(wr_nodes, wr0):
        n.inputs["Strength"].default_value = w0 * (0.12 + 0.88 * k) * 1.3
    bk = pop((t - 1.2) / 0.5)
    brain.scale = B0 * max(0.001, bk); brain.rotation_euler[2] = 0.5 * t
    bob = 0.05 * math.sin(t * 2.3)
    for o, p in ((d1, D1), (d2, D2), (beak, DB)):
        o.location = p + Vector((0.15 * math.sin(t * 0.6), 0, bob))
    emp.location = (t * 0.25, t * 0.12, 0)
    for i, o in enumerate(drops):
        x, z = TIPS[i % 4]; per = 0.9 + (i % 3) * 0.2; ph = ((t + i * 0.37) % per) / per
        tz = hand.location.z + z - 0.15 - 2.2 * ph * ph
        o.location = (hand.location.x + x * 0.95, hand.location.y - 0.05, tz if (t > 0.9 and tz > 0.2) else -5)
    kc = ease(t / DUR)
    cam.location = C0.lerp(C1, kc); tgt.location = T0.lerp(T1, kc)
    sc.render.filepath = os.path.join(frames, f"{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("fr", f, flush=True)
mp4 = os.path.join(out, f"Estilo {name}.mp4")
vf = "scale=1080:1920:flags=lanczos" if pref == "05" else f"minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale=1080:1920:flags=lanczos"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames, "%04d.png"), "-vf", vf,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", mp4], check=True)
print("ok", mp4)
