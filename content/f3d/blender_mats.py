"""Muestrario de texturas en BLENDER (Cycles) — Iker 06/11: «fatal muy mala textura, dame muchos más ejemplos».
Mano orgánica (modificador Skin + Subdivision), cerebro y patito; cada material en una imagen.
Uso: python3 blender_mats.py <carpeta_salida> [ancho alto muestras]"""
import sys, os, math
import bpy

out = sys.argv[1]
RW, RH, SAMP = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (432, 768, 24)
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMP
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Medium High Contrast"

# ---------- mundo y luces
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.03, 0.035, 0.05, 1); bg.inputs[1].default_value = 1.0


def area(name, loc, rot, size, energy, col):
    d = bpy.data.lights.new(name, "AREA"); d.size = size; d.energy = energy; d.color = col
    o = bpy.data.objects.new(name, d); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o)


area("key", (-3, -4, 6), (math.radians(50), 0, math.radians(-35)), 4, 900, (1, 0.93, 0.85))
area("rim", (4, 3, 4), (math.radians(-60), 0, math.radians(140)), 3, 700, (0.6, 0.8, 1))
area("fill", (3, -5, 2), (math.radians(80), 0, math.radians(30)), 5, 150, (1, 1, 1))

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.45))
floor = bpy.context.object
fm = bpy.data.materials.new("floor"); fm.use_nodes = True
fb = fm.node_tree.nodes["Principled BSDF"]; fb.inputs["Base Color"].default_value = (0.12, 0.13, 0.16, 1); fb.inputs["Roughness"].default_value = 0.5
floor.data.materials.append(fm)

# ---------- mano orgánica con metaballs (las piezas se funden solas) → malla
mb = bpy.data.metaballs.new("hand"); mb.resolution = 0.03; mb.render_resolution = 0.025; mb.threshold = 0.6
hand = bpy.data.objects.new("hand", mb); sc.collection.objects.link(hand)


def el(kind, co, rad, sx=0, sy=0, sz=0, rot=None, stiff=2.0):
    e = mb.elements.new(); e.type = kind; e.co = co; e.radius = rad; e.stiffness = stiff
    if kind in ("ELLIPSOID", "CAPSULE"):
        e.size_x, e.size_y, e.size_z = sx, sy, sz
    if rot is not None:
        e.rotation = rot
    return e


from mathutils import Quaternion, Vector
el("ELLIPSOID", (0, 0, 0.5), 1.0, 0.98, 0.32, 0.72, stiff=2.5)              # palma
el("ELLIPSOID", (0, 0, 0.95), 1.0, 0.9, 0.27, 0.3, stiff=2.0)
el("CAPSULE", (0, 0, -0.7), 0.5, 0.5, 0, 0, Quaternion((0, 1, 0), math.radians(90)), 2.0)   # muñeca
el("ELLIPSOID", (0.02, 0, 0.0), 1.0, 0.55, 0.26, 0.35, stiff=2.0)
for x, L, a in ((-0.36, 0.95, -0.09), (-0.12, 1.1, -0.03), (0.13, 1.05, 0.03), (0.37, 0.82, 0.1)):
    base = Vector((x, 0, 0.95))
    d = Vector((math.sin(a), 0, math.cos(a)))
    for k, (f0, f1, r) in enumerate(((0, 0.42, 0.165), (0.42, 0.72, 0.15), (0.72, 1.0, 0.14))):
        c = base + d * (L * (f0 + f1) / 2)
        q = Vector((1, 0, 0)).rotation_difference(d)
        el("CAPSULE", tuple(c), r, L * (f1 - f0) / 2, 0, 0, q, 2.0)
for (p0, p1, r) in (((-0.4, 0.05, 0.25), (-0.7, 0.1, 0.6), 0.2), ((-0.7, 0.1, 0.6), (-0.9, 0.12, 0.9), 0.17), ((-0.9, 0.12, 0.9), (-1.0, 0.12, 1.12), 0.15)):
    v0, v1 = Vector(p0), Vector(p1); d = (v1 - v0)
    el("CAPSULE", tuple((v0 + v1) / 2), r, d.length / 2, 0, 0, Vector((1, 0, 0)).rotation_difference(d.normalized()), 2.0)
hand.rotation_euler = (0, 0, math.radians(-12))
bpy.context.view_layer.objects.active = hand; hand.select_set(True)
bpy.ops.object.convert(target="MESH")
hand = bpy.context.object
bpy.ops.object.shade_smooth()
sm = hand.modifiers.new("smooth", "CORRECTIVE_SMOOTH"); sm.iterations = 6

# ---------- cerebro y patito
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(1.35, 0.3, 2.2), segments=96, ring_count=64)
brain = bpy.context.object; brain.scale = (1.2, 1.05, 0.92)
tx = bpy.data.textures.new("folds", "STUCCI"); tx.noise_scale = 0.12; tx.turbulence = 6
dm = brain.modifiers.new("d", "DISPLACE"); dm.texture = tx; dm.strength = 0.06
bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=(1.25, -0.6, -0.12), segments=64, ring_count=32)
d1 = bpy.context.object; d1.scale = (1.3, 1.0, 0.8); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.27, location=(1.6, -0.6, 0.32), segments=64, ring_count=32)
d2 = bpy.context.object; bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.26, location=(1.92, -0.6, 0.3), rotation=(0, math.radians(90), 0))
beak = bpy.context.object
bm = bpy.data.materials.new("beak"); bm.use_nodes = True; bm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 0.35, 0.05, 1)
beak.data.materials.append(bm)


# ---------- materiales (nodos)
def mat(name, build):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    build(nt, b)
    return m


def tex_coord(nt):
    return nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]


def bump(nt, b, height_out, strength, dist=0.02):
    bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = strength; bu.inputs["Distance"].default_value = dist
    nt.links.new(height_out, bu.inputs["Height"]); nt.links.new(bu.outputs["Normal"], b.inputs["Normal"])


def wrinkles(nt, b, strength=0.6):
    """Arrugas en las yemas: bandas de una textura de ondas, solo arriba de los dedos (coordenada Z del objeto)."""
    tc = tex_coord(nt)
    wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
    wv.inputs["Scale"].default_value = 9; wv.inputs["Distortion"].default_value = 6; wv.inputs["Detail"].default_value = 3
    nt.links.new(tc, wv.inputs["Vector"])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc, sep.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs[1].default_value = 1.6; mr.inputs[2].default_value = 1.85
    nt.links.new(sep.outputs["Z"], mr.inputs[0])
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    nt.links.new(wv.outputs["Fac"], mul.inputs[0]); nt.links.new(mr.outputs[0], mul.inputs[1])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 220; nt.links.new(tc, nz.inputs["Vector"])
    add = nt.nodes.new("ShaderNodeMath"); add.operation = "MULTIPLY_ADD"; add.inputs[1].default_value = 0.08
    nt.links.new(nz.outputs["Fac"], add.inputs[0]); nt.links.new(mul.outputs[0], add.inputs[2])
    bump(nt, b, add.outputs[0], strength, 0.03)


def set_(b, **kw):
    for k, v in kw.items():
        b.inputs[k].default_value = v


def skin_real(nt, b):
    set_(b, **{"Base Color": (0.72, 0.42, 0.3, 1), "Roughness": 0.45, "Subsurface Weight": 0.35, "Subsurface Scale": 0.15,
              "Coat Weight": 0.15, "Coat Roughness": 0.3})
    b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2)
    wrinkles(nt, b, 0.7)


def clay(col):
    def f(nt, b):
        set_(b, **{"Base Color": col, "Roughness": 0.85})
        tc = tex_coord(nt)
        vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = 28
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6
        nt.links.new(tc, vo.inputs["Vector"]); nt.links.new(tc, nz.inputs["Vector"])
        mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "ADD"
        nt.links.new(vo.outputs["Distance"], mx.inputs[0]); nt.links.new(nz.outputs["Fac"], mx.inputs[1])
        bump(nt, b, mx.outputs[0], 0.35)
    return f


def vinyl(col):
    return lambda nt, b: set_(b, **{"Base Color": col, "Roughness": 0.18, "Coat Weight": 1.0, "Coat Roughness": 0.05})


def gummy(col):
    def f(nt, b):
        set_(b, **{"Base Color": col, "Roughness": 0.1, "Transmission Weight": 0.85, "IOR": 1.4, "Subsurface Weight": 0.3, "Coat Weight": 1})
    return f


def ceramic(col):
    return lambda nt, b: set_(b, **{"Base Color": col, "Roughness": 0.25, "Coat Weight": 1, "Coat Roughness": 0.02})


def felt(col):
    def f(nt, b):
        set_(b, **{"Base Color": col, "Roughness": 1.0, "Sheen Weight": 1.0, "Sheen Roughness": 0.6})
        tc = tex_coord(nt); nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 160; nz.inputs["Detail"].default_value = 12
        nt.links.new(tc, nz.inputs["Vector"]); bump(nt, b, nz.outputs["Fac"], 0.5)
    return f


def wood(nt, b):
    tc = tex_coord(nt); wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "RINGS"; wv.inputs["Scale"].default_value = 3
    wv.inputs["Distortion"].default_value = 8; wv.inputs["Detail"].default_value = 4; nt.links.new(tc, wv.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.32, 0.15, 0.06, 1); ramp.color_ramp.elements[1].color = (0.78, 0.5, 0.25, 1)
    nt.links.new(wv.outputs["Fac"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    set_(b, Roughness=0.5); bump(nt, b, wv.outputs["Fac"], 0.25)


def marble(nt, b):
    tc = tex_coord(nt); nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.5; nz.inputs["Detail"].default_value = 10
    nz.inputs["Distortion"].default_value = 4; nt.links.new(tc, nz.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); e = ramp.color_ramp.elements
    e[0].position = 0.46; e[0].color = (0.92, 0.92, 0.94, 1); e[1].position = 0.5; e[1].color = (0.25, 0.25, 0.3, 1)
    e2 = e.new(0.54); e2.color = (0.95, 0.95, 0.96, 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    set_(b, **{"Roughness": 0.1, "Coat Weight": 0.6})


def gold(nt, b):
    set_(b, **{"Base Color": (1.0, 0.72, 0.3, 1), "Metallic": 1.0, "Roughness": 0.22})


def glass(col):
    return lambda nt, b: set_(b, **{"Base Color": col, "Roughness": 0.02, "Transmission Weight": 1.0, "IOR": 1.5})


def stone(nt, b):
    tc = tex_coord(nt); vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = 9
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 40; nz.inputs["Detail"].default_value = 12
    nt.links.new(tc, vo.inputs["Vector"]); nt.links.new(tc, nz.inputs["Vector"])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.inputs["Factor"].default_value = 0.5
    nt.links.new(vo.outputs["Color"], mx.inputs[6]); nt.links.new(nz.outputs["Color"], mx.inputs[7])
    bw = nt.nodes.new("ShaderNodeRGBToBW"); nt.links.new(mx.outputs[2], bw.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].color = (0.25, 0.24, 0.22, 1); ramp.color_ramp.elements[1].color = (0.7, 0.68, 0.64, 1)
    nt.links.new(bw.outputs[0], ramp.inputs[0]); nt.links.new(ramp.outputs[0], b.inputs["Base Color"])
    set_(b, Roughness=0.9); bump(nt, b, bw.outputs[0], 0.8)


def knit(col):
    def f(nt, b):
        set_(b, **{"Base Color": col, "Roughness": 1, "Sheen Weight": 0.8})
        tc = tex_coord(nt); wv = nt.nodes.new("ShaderNodeTexWave"); wv.inputs["Scale"].default_value = 30; wv.bands_direction = "Z"
        wv.inputs["Distortion"].default_value = 1.5; nt.links.new(tc, wv.inputs["Vector"])
        wv2 = nt.nodes.new("ShaderNodeTexWave"); wv2.inputs["Scale"].default_value = 30; wv2.bands_direction = "X"; nt.links.new(tc, wv2.inputs["Vector"])
        mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"; nt.links.new(wv.outputs["Fac"], mm.inputs[0]); nt.links.new(wv2.outputs["Fac"], mm.inputs[1])
        bump(nt, b, mm.outputs[0], 0.9)
    return f


SKIN, PINK, YEL = (0.85, 0.52, 0.4, 1), (0.95, 0.42, 0.55, 1), (1.0, 0.75, 0.05, 1)
LOOKS = [
    ("01 Piel realista", skin_real, ceramic(PINK), vinyl(YEL)),
    ("02 Plastilina", clay((0.85, 0.5, 0.38, 1)), clay(PINK), clay(YEL)),
    ("03 Vinilo de juguete", vinyl(SKIN), vinyl(PINK), vinyl(YEL)),
    ("04 Gominola", gummy((0.95, 0.45, 0.3, 1)), gummy(PINK), gummy(YEL)),
    ("05 Ceramica", ceramic((0.95, 0.93, 0.9, 1)), ceramic(PINK), ceramic(YEL)),
    ("06 Fieltro", felt((0.85, 0.5, 0.4, 1)), felt(PINK), felt(YEL)),
    ("07 Madera", wood, wood, wood),
    ("08 Marmol", marble, marble, marble),
    ("09 Oro", gold, gold, gold),
    ("10 Cristal", glass((0.85, 0.95, 1, 1)), glass((1, 0.7, 0.8, 1)), glass((1, 0.9, 0.5, 1))),
    ("11 Piedra", stone, stone, stone),
    ("12 Lana tejida", knit((0.9, 0.55, 0.45, 1)), knit(PINK), knit(YEL)),
]

# cámara
cd = bpy.data.cameras.new("cam"); cd.lens = 55
cam = bpy.data.objects.new("cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (1.0, -7.6, 1.8)
tgt = bpy.data.objects.new("tgt", None); tgt.location = (0.35, 0, 0.95); sc.collection.objects.link(tgt)
c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
cd.dof.use_dof = True; cd.dof.focus_object = tgt; cd.dof.aperture_fstop = 2.8

only = os.environ.get("ONLY")
for name, fh, fb_, fd in LOOKS:
    if only and not name.startswith(only):
        continue
    for ob, f in ((hand, fh), (brain, fb_), (d1, fd), (d2, fd)):
        ob.data.materials.clear(); ob.data.materials.append(mat(name, f))
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("ok", name, flush=True)
