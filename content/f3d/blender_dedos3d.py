"""«Dedos arrugados» del vídeo 2D, pasado a 3D (Iker 06/11). Renderiza SOLO el dibujo (fondo 3D) a 12 fps;
textos, subtítulos, banner y voz los pone después el sistema 2D (content/cine/c20_dedos3d.py).
Uso: VAR=contorno|suave|plastilina|juguete python3 blender_dedos3d.py <carpeta_frames> <f0> <f1> [ancho alto muestras]
Planos (segundos): q 0–4.5 · banera 4.5–8.1 · esponja 8.1–11.3 · medicos 11.3–15.4"""
import sys, os, math, runpy
outd, F0, F1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
RW, RH, SAMP = (int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (432, 768, 10)
VAR = os.environ.get("VAR", "contorno")
FPS = 12
os.makedirs(outd, exist_ok=True)
os.environ["CLIPS"] = "1"
here = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["x", outd, str(RW), str(RH), str(SAMP)]
G = runpy.run_path(os.path.join(here, "blender_styles.py"))
import bpy
from mathutils import Vector
sc = bpy.context.scene
hand, brain, d1, d2, beak, water, tub, wall, floor, win, cam, cd, tgt = (G[k] for k in ("hand", "brain", "d1", "d2", "beak", "water", "tub", "wall", "floor", "win", "cam", "cd", "tgt"))
M, toon, emis, assign, set_world, light, clear_lights, freestyle, tiles_nodes, skin_nodes = (G[k] for k in (
    "M", "toon", "emis", "assign", "set_world", "light", "clear_lights", "freestyle", "tiles_nodes", "skin_nodes"))
G["reset"]()


def rgb(r, g, b):
    return (r / 255) ** 2.2, (g / 255) ** 2.2, (b / 255) ** 2.2, 1.0


# paleta del vídeo 2D
C = {"skin": rgb(246, 196, 160), "water": rgb(90, 170, 220), "tile": rgb(196, 222, 228), "tile2": rgb(210, 232, 236), "grout": rgb(240, 246, 248),
     "floor": rgb(176, 136, 104), "tub": rgb(250, 250, 252), "duck": rgb(255, 205, 40), "beak": rgb(255, 120, 30), "brain": rgb(246, 150, 175),
     "towel": rgb(236, 110, 100), "sponge": rgb(255, 214, 80), "spongeg": rgb(80, 170, 90), "ink": rgb(28, 28, 32), "white": rgb(255, 255, 255),
     "red": rgb(220, 30, 40), "coat": rgb(246, 236, 214), "sepia": rgb(196, 158, 112), "sepia2": rgb(150, 112, 76), "raisin": rgb(110, 55, 70),
     "nerve": rgb(255, 214, 60), "gold": rgb(236, 190, 60)}


def soft(col, rough=0.5):
    return M("s", **{"Base Color": col, "Roughness": rough})


def clay(col):
    def f(nt, b):
        b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = 0.85
        tc = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]
        vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = 20; nt.links.new(tc, vo.inputs["Vector"])
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 5; nt.links.new(tc, nz.inputs["Vector"])
        ad = nt.nodes.new("ShaderNodeMath"); ad.operation = "ADD"; nt.links.new(vo.outputs["Distance"], ad.inputs[0]); nt.links.new(nz.outputs["Fac"], ad.inputs[1])
        bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.3; nt.links.new(ad.outputs[0], bu.inputs["Height"]); nt.links.new(bu.outputs[0], b.inputs["Normal"])
    return M("c", nodes=f)


def mat(col, kind="obj"):
    """Material según la versión (VAR)."""
    if VAR == "contorno":
        return toon("t", col, shade=0.62)
    if VAR == "plastilina":
        return clay(col)
    if VAR == "juguete":
        return M("j", **{"Base Color": col, "Roughness": 0.2, "Coat Weight": 1.0, "Coat Roughness": 0.08})
    return soft(col, 0.45)


def skin_mat():
    if VAR == "suave":
        return M("h", nodes=skin_nodes(C["skin"], 0.8))
    if VAR == "contorno":
        return toon("h", C["skin"], 0.62)
    return mat(C["skin"])


def add(o, col=None, m=None):
    o.data.materials.clear(); o.data.materials.append(m or mat(col)); return o


def sphere(r, loc, seg=48):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2); o = bpy.context.object
    for p in o.data.polygons: p.use_smooth = True
    return o


def cyl(r, depth, loc, rot=(0, 0, 0), r2=None, verts=32):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r2, radius2=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.object
    for p in o.data.polygons: p.use_smooth = True
    return o


def rbox(sx, sy, sz, loc, bev=0.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.scale = (sx, sy, sz)
    b = o.modifiers.new("b", "BEVEL"); b.width = bev; b.segments = 5
    for p in o.data.polygons: p.use_smooth = True
    return o


def torus(R, r, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, rotation=rot)
    o = bpy.context.object
    for p in o.data.polygons: p.use_smooth = True
    return o


def parent(ch, par):
    for c in ch:
        c.parent = par; c.matrix_parent_inverse = par.matrix_world.inverted()


# ---------- materiales del baño
add(hand, m=skin_mat()); add(brain, C["brain"]); add(d1, C["duck"]); add(d2, C["duck"]); add(beak, C["beak"])
wm = toon("w", C["water"], 0.7) if VAR == "contorno" else M("w", **{"Base Color": C["water"], "Roughness": 0.05, "Transmission Weight": 0.6 if VAR == "suave" else 0, "IOR": 1.33, "Coat Weight": 0.6})
add(water, m=wm); add(tub, C["tub"])
if VAR == "contorno":
    add(wall, m=toon("wa", C["tile"], 0.85)); add(floor, m=toon("f", C["floor"]))
else:
    add(wall, m=M("wa", nodes=tiles_nodes(C["tile"], C["tile2"], C["grout"], scale=34, rough=0.35 if VAR != "plastilina" else 0.9)))
    add(floor, C["floor"])
WALL_BATH = wall.data.materials[0]; WALL_SEP = mat(C["sepia"]); FLOOR_BATH = floor.data.materials[0]; FLOOR_SEP = mat(rgb(110, 80, 56))
add(win, m=emis("win", (1, 0.95, 0.8, 1), 3.5)); win.location = (2.4, 3.35, 4.6)
towel = add(rbox(1.0, 0.12, 1.6, (-2.6, 3.25, 2.4), 0.1), C["towel"])
bar = add(cyl(0.05, 1.6, (-2.6, 3.2, 3.25), (0, math.radians(90), 0)), C["sepia2"])

# ---------- Ojo 3D (como el del vídeo 2D: cabeza-ojo blanca con contorno, iris rojo, bata, cuerpo de palo)
ojo = bpy.data.objects.new("ojo", None); sc.collection.objects.link(ojo)
parts = []
head = add(sphere(0.42, (0, 0, 1.75), 64), C["white"]); parts.append(head)
iris = add(cyl(0.2, 0.05, (0, -0.4, 1.75), (math.radians(90), 0, 0), verts=48), C["red"]); parts.append(iris)
pupil = add(cyl(0.09, 0.05, (0, -0.43, 1.75), (math.radians(90), 0, 0), verts=32), C["ink"]); parts.append(pupil)
glint = add(sphere(0.035, (0.07, -0.46, 1.83), 16), m=emis("g", (1, 1, 1, 1), 2)); parts.append(glint)
ring = add(torus(0.42, 0.025, (0, 0, 1.75), (math.radians(90), 0, 0)), C["ink"]); parts.append(ring)
coat = add(cyl(0.16, 0.85, (0, 0, 0.95), r2=0.36, verts=40), C["white"]); parts.append(coat)
pocket = add(rbox(0.12, 0.02, 0.12, (0.15, -0.3, 1.0), 0.01), C["spongeg"]); parts.append(pocket)
neck = add(cyl(0.035, 0.3, (0, 0, 1.38)), C["ink"]); parts.append(neck)
legs = [add(cyl(0.035, 0.55, (x, 0, 0.27)), C["ink"]) for x in (-0.12, 0.12)]; parts += legs
shoes = [add(sphere(0.07, (x, -0.04, 0.02), 16), C["ink"]) for x in (-0.12, 0.12)]; parts += shoes
arms = []
for sx in (-1, 1):
    pv = bpy.data.objects.new("arm", None); sc.collection.objects.link(pv); pv.location = (0.2 * sx, 0, 1.3)
    a = add(cyl(0.032, 0.6, (0.2 * sx, 0, 1.0)), C["ink"]); hnd = add(sphere(0.06, (0.2 * sx, 0, 0.68), 16), C["ink"])
    parent([a, hnd], pv); arms.append(pv)
parent(parts + arms, ojo)
mag = bpy.data.objects.new("mag", None); sc.collection.objects.link(mag)
lens = add(torus(0.22, 0.035, (0, 0, 0), (math.radians(90), 0, 0)), C["ink"])
glass = add(cyl(0.2, 0.01, (0, 0, 0), (math.radians(90), 0, 0)), m=M("gl", **{"Base Color": (0.8, 0.9, 1, 1), "Roughness": 0, "Transmission Weight": 1, "IOR": 1.3}))
handle = add(cyl(0.035, 0.35, (0.2, 0, -0.2), (0, math.radians(-45), 0)), C["sepia2"])
parent([lens, glass, handle], mag)


def ojo_pose(t, loc, s=0.6, rz=0.0, armL=0.3, armR=-0.3, hop=0.0):
    ojo.location = Vector(loc) + Vector((0, 0, hop + 0.02 * math.sin(t * 3))); ojo.scale = (s, s, s); ojo.rotation_euler = (0, 0, rz)
    arms[0].rotation_euler = (0, armL, 0); arms[1].rotation_euler = (0, armR, 0)


# ---------- extras: gotas, espuma, chispas, pasa, esponja, cuadro con médico
drops = [add(sphere(0.05, (0, 0, -9), 16), m=wm) for _ in range(8)]
for o in drops: o.scale = (1, 1, 1.35)
foam = [add(sphere(0.12 + 0.05 * (i % 3), (-3.3 + i * 0.38, -1.4 + 0.08 * (i % 2), 0.2), 16), C["white"]) for i in range(18)]
sparks = [add(sphere(0.06, (0, 0, -9), 12), m=emis("sp", (1, 0.9, 0.3, 1), 6)) for _ in range(6)]
raisin = add(sphere(0.3, (0, 0, -9), 64), C["raisin"]); raisin.scale = (1, 1, 0.8)
rt = bpy.data.textures.new("rz", "STUCCI"); rt.noise_scale = 0.08; rt.turbulence = 8
rm = raisin.modifiers.new("d", "DISPLACE"); rm.texture = rt; rm.strength = 0.08
sponge = add(rbox(1.3, 0.75, 0.55, (0, 0, -9), 0.12), C["sponge"])
sponge_top = add(rbox(1.3, 0.75, 0.16, (0, 0, -9), 0.06), C["spongeg"])
if VAR != "contorno":
    def sp_nodes(nt, b):
        b.inputs["Base Color"].default_value = C["sponge"]; b.inputs["Roughness"].default_value = 0.9
        tc = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]; vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 14
        nt.links.new(tc, vo.inputs["Vector"]); bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.9; bu.invert = True
        nt.links.new(vo.outputs["Distance"], bu.inputs["Height"]); nt.links.new(bu.outputs[0], b.inputs["Normal"])
    add(sponge, m=M("sp", nodes=sp_nodes))
frame_ = add(rbox(1.7, 0.12, 2.1, (0, 0, -9), 0.04), C["sepia2"])
canvas = add(rbox(1.45, 0.05, 1.85, (0, 0, -9), 0.01), C["sepia"])
doc = bpy.data.objects.new("doc", None); sc.collection.objects.link(doc)
dparts = [add(sphere(0.33, (0, 0, 0.45), 48), rgb(236, 200, 160)), add(cyl(0.2, 0.9, (0, 0, -0.35), r2=0.55), C["coat"]),
          add(sphere(0.345, (0, 0.03, 0.55), 48), rgb(110, 90, 70)),
          add(torus(0.09, 0.015, (-0.12, -0.31, 0.47), (math.radians(90), 0, 0)), C["ink"]),
          add(torus(0.09, 0.015, (0.12, -0.31, 0.47), (math.radians(90), 0, 0)), C["ink"]),
          add(rbox(0.25, 0.05, 0.06, (0, -0.32, 0.3), 0.02), rgb(90, 70, 50)), add(rbox(0.3, 0.04, 0.4, (0.32, -0.45, -0.25), 0.01), rgb(250, 244, 226))]
dparts[2].scale = (1, 1, 0.55); dparts[2].location = (0, 0.04, 0.62)
parent(dparts, doc)
SCENE_OBJS = {"bath": [hand, brain, d1, d2, beak, water, tub, towel, bar] + foam, "sponge": [sponge, sponge_top], "doc": [frame_, canvas, doc] + dparts}

# ---------- luces y render por versión
clear_lights()
set_world((0.75, 0.85, 0.9, 1), 0.45)
light("AREA", (-3, -3, 6), (math.radians(35), math.radians(-25), 0), 800, (1, 0.95, 0.88), 4)
light("AREA", (4, 1, 4), (math.radians(-60), 0, math.radians(120)), 350, (0.75, 0.88, 1), 2)
cd.dof.use_dof = VAR in ("suave", "juguete"); cd.dof.aperture_fstop = 3.5
if VAR == "contorno":
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    G["freestyle"](1.7)
    light("SUN", (0, 0, 10), (math.radians(40), math.radians(-25), 0), 3.5, size=1)
for o in [glint] + sparks + [win]:
    o.visible_shadow = False


def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def pop(k):
    if k <= 0: return 0.0
    if k >= 1: return 1.0
    return 1 + 2.7 * (k - 1) ** 3 + 1.7 * (k - 1) ** 2


def show(group_on):
    for g, objs in SCENE_OBJS.items():
        for o in objs:
            o.hide_render = g not in group_on
    for o in drops + sparks + [raisin, mag]:
        o.hide_render = True
    for c in mag.children:
        c.hide_render = True


H0 = Vector(hand.location); B0 = Vector(brain.scale)
emp = bpy.data.objects.new("wv", None); sc.collection.objects.link(emp)
wd = water.modifiers["d"]; wd.texture_coords = "OBJECT"; wd.texture_coords_object = emp
wr_nodes = [n for m in hand.data.materials for n in m.node_tree.nodes if n.label == "wr"]
wr0 = [n.inputs["Strength"].default_value for n in wr_nodes]
TIPS = [(-0.38, 1.85), (-0.15, 2.05), (0.15, 2.0), (0.4, 1.75)]


def set_cam(p0, p1, l0, l1, k, lens=42):
    cam.location = Vector(p0).lerp(Vector(p1), ease(k)); tgt.location = Vector(l0).lerp(Vector(l1), ease(k)); cd.lens = lens


def frame_at(t):
    emp.location = (t * 0.25, t * 0.12, 0)
    for i, f in enumerate(foam):
        f.location.z = 0.22 + 0.03 * math.sin(t * 2 + i)
    if t < 4.5:                                      # ---- GANCHO: mano que sale del agua, cerebro con impulsos, Ojo sorprendido
        show({"bath"})
        rise = ease((t - 0.05) / 0.9)
        hand.location = H0 + Vector((0, 0, -1.9 * (1 - rise) + 0.03 * math.sin(t * 1.6)))
        k = ease((t - 2.4) / 1.6)
        for n, w0 in zip(wr_nodes, wr0): n.inputs["Strength"].default_value = w0 * (0.25 + 0.95 * k) * 1.4
        bk = pop((t - 2.2) / 0.5); brain.scale = B0 * max(0.001, bk); brain.rotation_euler[2] = 0.5 * t
        on = 2.5 < t < 4.5
        tip = hand.location + Vector((-0.15, -0.05, 2.0))
        for i, s in enumerate(sparks):
            u = ((t - 2.5) * 0.9 + i / 6) % 1
            p = brain.location.lerp(tip, u) + Vector((0.3 * math.sin(math.pi * u), -0.2, 0.25 * math.sin(math.pi * u)))
            s.location = p; s.hide_render = not on
        for i, o in enumerate(drops):
            x, z = TIPS[i % 4]; per = 0.9 + (i % 3) * 0.2; ph = ((t + i * 0.37) % per) / per
            tz = hand.location.z + z - 0.15 - 2.2 * ph * ph
            o.location = (hand.location.x + x * 0.95, hand.location.y - 0.1, tz); o.hide_render = not (t > 0.9 and tz > 0.25)
        sur = 1 if t > 2.4 else 0
        ojo_pose(t, (1.3, -0.75, 0.32), 0.55, math.radians(-25), 0.3 + 2.2 * sur * ease((t - 2.4) / 0.3), -0.3 - 2.2 * sur * ease((t - 2.4) / 0.3), 0.08 * sur * abs(math.sin(t * 6)))
        set_cam((1.3, -5.6, 2.6), (0.7, -4.4, 2.3), (0.3, 0.3, 1.5), (0.3, 0.3, 1.8), t / 4.5)
        d1.location = (-1.25, -0.2, 0.3 + 0.05 * math.sin(t * 2.3)); d2.location = (-0.9, -0.2, 0.72 + 0.05 * math.sin(t * 2.3)); beak.location = (-0.6, -0.2, 0.7 + 0.05 * math.sin(t * 2.3))
    elif t < 8.1:                                    # ---- BAÑERA: Ojo dentro del agua, patito, la pasa aparece
        lt = t - 4.5
        show({"bath"}); hand.hide_render = True; brain.hide_render = True
        ojo_pose(t, (-0.5, 0.2, -0.5), 0.9, math.radians(10), 0.9 + 0.15 * math.sin(t * 2), -0.9 - 0.15 * math.sin(t * 2))
        b = 0.06 * math.sin(t * 2.3)
        d1.location = (1.1 + 0.2 * math.sin(t * 0.6), 0.2, 0.3 + b); d2.location = (1.45 + 0.2 * math.sin(t * 0.6), 0.2, 0.72 + b); beak.location = (1.75 + 0.2 * math.sin(t * 0.6), 0.2, 0.7 + b)
        rk = pop((lt - 2.5) / 0.45)
        raisin.hide_render = rk <= 0.01; raisin.location = (0.55, -0.3, 1.5 + 0.05 * math.sin(t * 3)); raisin.scale = (rk, rk, rk * 0.8); raisin.rotation_euler = (0, 0, t)
        set_cam((2.4, -6.0, 3.4), (1.0, -4.4, 2.2), (0, 0.4, 0.6), (0.2, 0.3, 1.0), lt / 3.6)
    elif t < 11.3:                                   # ---- ESPONJA: la piel «se empapa como una esponja»
        lt = t - 8.1
        show({"bath", "sponge"}); hand.hide_render = brain.hide_render = True
        for o in (d1, d2, beak): o.hide_render = True
        wet = ease(lt / 2.0)
        sponge.location = (0, 0.1, 0.62); sponge.scale = (1.3 * (1 + 0.06 * wet), 0.75, 0.55 * (1 + 0.12 * wet))
        sponge_top.location = (0, 0.1, 0.62 + 0.55 * (1 + 0.12 * wet) / 2 + 0.06); sponge_top.scale = (1.3 * (1 + 0.06 * wet), 0.75, 0.16)
        for i, o in enumerate(drops):
            ph = ((lt + i * 0.23) % 0.9) / 0.9
            o.location = (-0.5 + (i % 4) * 0.33, 0.1, 2.4 - 1.5 * ph * ph); o.hide_render = False
        ojo_pose(t, (0.72, -0.75, 0.32), 0.5, math.radians(-30), 0.4, -2.0 - 0.2 * math.sin(t * 3))
        set_cam((0.6, -3.6, 1.9), (0.25, -3.0, 1.6), (0, 0.1, 1.0), (0.1, 0.1, 1.0), lt / 3.2, 40)
    else:                                            # ---- MÉDICOS: hace casi cien años… cuadro con un médico antiguo
        lt = t - 11.3
        show({"doc"})
        frame_.location = (0, 2.9, 2.2); canvas.location = (0, 2.83, 2.2)
        doc.location = (0, 2.7, 1.9); doc.rotation_euler = (0, 0, math.radians(8 * math.sin(t * 0.8)))
        ojo_pose(t, (0.75, 0.9, 0.32), 0.6, math.radians(-35), 0.4, -1.4)
        mag.hide_render = False
        for c in mag.children: c.hide_render = False
        mag.location = ojo.location + Vector((-0.45, -0.25, 0.8)) + Vector((0.05 * math.sin(t * 2), 0, 0.05 * math.cos(t * 2))); mag.scale = (0.9, 0.9, 0.9)
        set_cam((0.2, -2.6, 2.6), (0.4, -1.6, 2.3), (0.1, 2.6, 1.9), (0.3, 2.6, 1.8), lt / 4.1, 38)
    # sepia en el plano de los médicos
    wall.data.materials[0] = WALL_SEP if t >= 11.3 else WALL_BATH
    floor.data.materials[0] = FLOOR_SEP if t >= 11.3 else FLOOR_BATH
    win.hide_render = t >= 11.3
    if t >= 11.3:
        set_world(rgb(120, 90, 60), 0.6)
    else:
        set_world((0.75, 0.85, 0.9, 1), 0.45)


LIST = [int(x) for x in os.environ["FRAMES"].split(",")] if os.environ.get("FRAMES") else range(F0, F1)
for f in LIST:
    p = os.path.join(outd, f"{f:04d}.png")
    if os.path.exists(p):
        continue
    frame_at(f / FPS)
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    print("fr", f, flush=True)
print("ok", F0, F1)
