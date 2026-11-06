"""Muestrario de ESTILOS visuales en Blender (Iker 06/11: «digo estilo, dame más estilos»).
Misma escena (bañera, agua, mano arrugada, cerebro, patito, pared de azulejos) con 12 estilos completos.
Uso: python3 blender_styles.py <carpeta> [ancho alto muestras]   ·   ONLY=03 para uno solo."""
import sys, os, math
import bpy
from mathutils import Vector, Quaternion

out = sys.argv[1]
RW, RH, SAMP = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (432, 768, 24)
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = RW, RH
W = bpy.data.worlds.new("w"); sc.world = W; W.use_nodes = True
BG = W.node_tree.nodes["Background"]


def link(o):
    sc.collection.objects.link(o); return o


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


# ---------- escena
def metaball_hand():
    mb = bpy.data.metaballs.new("hand"); mb.resolution = 0.03; mb.render_resolution = 0.025; mb.threshold = 0.6
    o = link(bpy.data.objects.new("handmb", mb))

    def el(kind, co, rad, sx=0, sy=0, sz=0, rot=None, st=2.0):
        e = mb.elements.new(); e.type = kind; e.co = co; e.radius = rad; e.stiffness = st
        if kind in ("ELLIPSOID", "CAPSULE"):
            e.size_x, e.size_y, e.size_z = sx, sy, sz
        if rot is not None:
            e.rotation = rot
    el("ELLIPSOID", (0, 0, 0.5), 1.0, 0.98, 0.32, 0.72, st=2.5)
    el("ELLIPSOID", (0, 0, 0.95), 1.0, 0.9, 0.27, 0.3)
    el("ELLIPSOID", (0.02, 0, 0.0), 1.0, 0.55, 0.26, 0.35)
    el("CAPSULE", (0, 0, -0.9), 0.5, 0.7, 0, 0, Quaternion((0, 1, 0), math.radians(90)))
    for x, L, a in ((-0.36, 0.95, -0.09), (-0.12, 1.1, -0.03), (0.13, 1.05, 0.03), (0.37, 0.82, 0.1)):
        base = Vector((x, 0, 0.95)); d = Vector((math.sin(a), 0, math.cos(a)))
        for f0, f1, r in ((0, 0.42, 0.165), (0.42, 0.72, 0.15), (0.72, 1.0, 0.14)):
            el("CAPSULE", tuple(base + d * (L * (f0 + f1) / 2)), r, L * (f1 - f0) / 2, 0, 0, Vector((1, 0, 0)).rotation_difference(d))
    for p0, p1, r in (((-0.4, 0.05, 0.25), (-0.7, 0.1, 0.6), 0.2), ((-0.7, 0.1, 0.6), (-0.9, 0.12, 0.9), 0.17), ((-0.9, 0.12, 0.9), (-1.0, 0.12, 1.12), 0.15)):
        v0, v1 = Vector(p0), Vector(p1); d = v1 - v0
        el("CAPSULE", tuple((v0 + v1) / 2), r, d.length / 2, 0, 0, Vector((1, 0, 0)).rotation_difference(d.normalized()))
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.convert(target="MESH")
    h = bpy.context.object; smooth(h)
    h.location = (0, 0.2, 0.15); h.rotation_euler = (math.radians(-6), 0, math.radians(-10))
    return h


hand = metaball_hand()
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(1.15, 0.5, 3.0), segments=96, ring_count=64)
brain = bpy.context.object; brain.scale = (1.2, 1.05, 0.92); smooth(brain)
tx = bpy.data.textures.new("folds", "STUCCI"); tx.noise_scale = 0.12; tx.turbulence = 6
dm = brain.modifiers.new("d", "DISPLACE"); dm.texture = tx; dm.strength = 0.06
# patito
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, location=(-1.25, -0.2, 0.3), segments=64, ring_count=32)
d1 = bpy.context.object; d1.scale = (1.3, 1.0, 0.8); smooth(d1)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.27, location=(-0.9, -0.2, 0.72), segments=64, ring_count=32)
d2 = bpy.context.object; smooth(d2)
bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.26, location=(-0.6, -0.2, 0.7), rotation=(0, math.radians(90), 0))
beak = bpy.context.object
# agua: plano con olas (desplazamiento)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.6, 0.15))
water = bpy.context.object; water.scale = (6.4, 3.6, 1)
sub = water.modifiers.new("s", "SUBSURF"); sub.subdivision_type = "SIMPLE"; sub.levels = sub.render_levels = 6
wt = bpy.data.textures.new("waves", "CLOUDS"); wt.noise_scale = 0.35
wd = water.modifiers.new("d", "DISPLACE"); wd.texture = wt; wd.strength = 0.06; smooth(water)
# bañera: caja redondeada hueca
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.6, -0.75))
tub = bpy.context.object; tub.scale = (7.2, 4.2, 1.6)
bv = tub.modifiers.new("b", "BEVEL"); bv.width = 0.35; bv.segments = 8; bv.affect = "EDGES"
smooth(tub)
# pared y suelo
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 3.4, 4), rotation=(math.radians(90), 0, 0))
wall = bpy.context.object; wall.scale = (30, 12, 1)
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.25))
floor = bpy.context.object
# ventana (luz)
bpy.ops.mesh.primitive_plane_add(size=1, location=(-3.2, 3.35, 5.0), rotation=(math.radians(90), 0, 0))
win = bpy.context.object; win.scale = (2.4, 2.8, 1)

# cámara
cd = bpy.data.cameras.new("cam"); cd.lens = 42
cam = link(bpy.data.objects.new("cam", cd)); sc.camera = cam
tgt = link(bpy.data.objects.new("tgt", None)); tgt.location = (0.15, 0.3, 1.65)
c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
cd.dof.focus_object = tgt
LIGHTS = []


def light(kind, loc, rot, energy, col=(1, 1, 1), size=3):
    d = bpy.data.lights.new("L", kind); d.energy = energy; d.color = col
    if kind == "AREA":
        d.size = size
    if kind == "SUN":
        d.angle = math.radians(size)
    o = link(bpy.data.objects.new("L", d)); o.location = loc; o.rotation_euler = rot; LIGHTS.append(o); return o


def clear_lights():
    for o in LIGHTS:
        bpy.data.objects.remove(o)
    LIGHTS.clear()


# ---------- utilidades de material
def M(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    for k, v in kw.items():
        if k in ("nodes",):
            continue
        b.inputs[k].default_value = v
    if "nodes" in kw:
        kw["nodes"](m.node_tree, b)
    return m


def emis(name, col, s=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = col; e.inputs[1].default_value = s
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0]); return m


def toon(name, col, shade=0.55, outline=True):
    """Sombreado de dibujo animado: Diffuse → Shader to RGB → rampa de 3 tonos."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    d = nt.nodes.new("ShaderNodeBsdfDiffuse"); d.inputs[0].default_value = (1, 1, 1, 1)
    s2r = nt.nodes.new("ShaderNodeShaderToRGB"); nt.links.new(d.outputs[0], s2r.inputs[0])
    r = nt.nodes.new("ShaderNodeValToRGB"); r.color_ramp.interpolation = "CONSTANT"
    e = r.color_ramp.elements; e[0].position = 0; e[0].color = tuple(cc * shade for cc in col[:3]) + (1,)
    e[1].position = 0.35; e[1].color = col; e3 = e.new(0.85); e3.color = tuple(min(1, cc * 1.18) for cc in col[:3]) + (1,)
    nt.links.new(s2r.outputs[0], r.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); nt.links.new(r.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0]); return m


def tiles_nodes(c1, c2, mortar, scale=34, rough=0.3):
    def f(nt, b):
        tc = nt.nodes.new("ShaderNodeTexCoord")
        br = nt.nodes.new("ShaderNodeTexBrick"); br.offset = 0; br.inputs["Scale"].default_value = scale
        br.inputs["Mortar Size"].default_value = 0.02; br.inputs["Brick Width"].default_value = 1.0; br.inputs["Row Height"].default_value = 1.0
        br.inputs["Color1"].default_value = c1; br.inputs["Color2"].default_value = c2; br.inputs["Mortar"].default_value = mortar
        nt.links.new(tc.outputs["UV"], br.inputs["Vector"]); nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = rough
    return f


def skin_nodes(col, wr=0.6):
    def f(nt, b):
        b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = 0.45
        b.inputs["Subsurface Weight"].default_value = 0.3; b.inputs["Subsurface Scale"].default_value = 0.15
        b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2)
        tc = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Z"
        wv.inputs["Scale"].default_value = 9; wv.inputs["Distortion"].default_value = 6; nt.links.new(tc, wv.inputs["Vector"])
        sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc, sp.inputs[0])
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs[1].default_value = 1.6; mr.inputs[2].default_value = 1.85; nt.links.new(sp.outputs["Z"], mr.inputs[0])
        mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; nt.links.new(wv.outputs["Fac"], mu.inputs[0]); nt.links.new(mr.outputs[0], mu.inputs[1])
        bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = wr; bu.inputs["Distance"].default_value = 0.03
        nt.links.new(mu.outputs[0], bu.inputs["Height"]); nt.links.new(bu.outputs[0], b.inputs["Normal"])
    return f


def assign(o, m):
    o.data.materials.clear(); o.data.materials.append(m)


def set_world(col, s=1.0):
    BG.inputs[0].default_value = col; BG.inputs[1].default_value = s


def reset():
    clear_lights()
    for o in (hand, brain, d1, d2, beak, water, tub, wall, floor, win):
        o.hide_render = False
        for m in list(o.modifiers):
            if m.name.startswith("ST_"):
                o.modifiers.remove(m)
    sc.render.use_freestyle = False
    for o in (hand, brain, d1, d2, tub, water):
        smooth(o)
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
    sc.cycles.samples = SAMP
    cd.type = "PERSP"; cd.lens = 42; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.8
    cam.location = (1.0, -5.0, 2.5)
    sc.cycles.max_bounces = 8


def freestyle(th=2.0, col=(0.05, 0.05, 0.07)):
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = "ABSOLUTE"; sc.render.line_thickness = th
    vl = bpy.context.view_layer; vl.use_freestyle = True
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("L")
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("LS")
    ls.select_by_visibility = True; ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = False
    ls.linestyle.color = col; ls.linestyle.thickness = th


# ---------- los 12 estilos
SKIN = (0.75, 0.45, 0.33, 1)
def st_cine():
    """Película de animación: piel con luz que atraviesa, luz de ventana cálida, desenfoque."""
    set_world((0.02, 0.025, 0.035, 1), 1)
    assign(hand, M("h", nodes=skin_nodes(SKIN)))
    assign(brain, M("b", **{"Base Color": (0.95, 0.45, 0.55, 1), "Roughness": 0.35, "Coat Weight": 0.6}))
    for o in (d1, d2): assign(o, M("d", **{"Base Color": (1, 0.72, 0.05, 1), "Roughness": 0.2, "Coat Weight": 1}))
    assign(beak, M("k", **{"Base Color": (1, 0.3, 0.02, 1)}))
    assign(water, M("w", **{"Base Color": (0.2, 0.55, 0.75, 1), "Roughness": 0.02, "Transmission Weight": 0.8, "IOR": 1.33}))
    assign(tub, M("t", **{"Base Color": (0.95, 0.95, 0.95, 1), "Roughness": 0.12, "Coat Weight": 1}))
    assign(wall, M("wa", nodes=tiles_nodes((0.55, 0.75, 0.8, 1), (0.6, 0.8, 0.85, 1), (0.9, 0.93, 0.93, 1))))
    assign(floor, M("f", **{"Base Color": (0.35, 0.22, 0.14, 1), "Roughness": 0.5}))
    assign(win, emis("win", (1, 0.9, 0.7, 1), 6))
    light("AREA", (-3, -1, 6), (math.radians(30), math.radians(-30), 0), 900, (1, 0.85, 0.65), 3)
    light("AREA", (4, 2, 3), (math.radians(-70), 0, math.radians(120)), 500, (0.55, 0.75, 1), 2)


def st_real():
    """Médico/realista tipo documental: gris estudio, luz dura lateral, primer plano."""
    st_cine(); clear_lights()
    set_world((0.06, 0.06, 0.065, 1), 1)
    assign(wall, M("wa", **{"Base Color": (0.08, 0.08, 0.09, 1), "Roughness": 0.8})); assign(floor, M("f", **{"Base Color": (0.05, 0.05, 0.05, 1)}))
    win.hide_render = True
    light("SPOT", (-4, -3, 5), (math.radians(55), 0, math.radians(-50)), 2500, (1, 0.97, 0.92), 0).data.spot_size = math.radians(35)
    light("AREA", (3, 3, 3), (math.radians(-70), 0, math.radians(130)), 400, (0.7, 0.85, 1), 1)
    cam.location = (0.9, -4.6, 2.1); cd.lens = 55; cd.dof.aperture_fstop = 1.8


def st_toon():
    """Dibujo animado / anime: 3 tonos planos y contorno negro."""
    set_world((0.45, 0.78, 0.95, 1), 1); sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    assign(hand, toon("h", (1.0, 0.68, 0.52, 1))); assign(brain, toon("b", (1.0, 0.55, 0.7, 1)))
    for o in (d1, d2): assign(o, toon("d", (1.0, 0.82, 0.1, 1)))
    assign(beak, toon("k", (1.0, 0.45, 0.1, 1))); assign(water, toon("w", (0.2, 0.6, 0.95, 1))); assign(tub, toon("t", (0.97, 0.97, 1, 1)))
    assign(wall, toon("wa", (0.5, 0.85, 0.95, 1))); assign(floor, toon("f", (1, 0.75, 0.45, 1))); assign(win, toon("wi", (1, 0.97, 0.75, 1)))
    light("SUN", (0, 0, 10), (math.radians(40), math.radians(-25), 0), 4, size=1)
    cd.dof.use_dof = False; freestyle(2.4)


def st_lowpoly():
    """Low-poly geométrico: caras planas y colores pastel."""
    st_cine()
    for o in (hand, brain, d1, d2, tub):
        dec = o.modifiers.new("ST_dec", "DECIMATE"); dec.ratio = 0.04 if o is not tub else 0.3
        for p in o.data.polygons: p.use_smooth = False
    assign(hand, M("h", **{"Base Color": (0.95, 0.65, 0.5, 1), "Roughness": 0.8}))
    assign(water, M("w", **{"Base Color": (0.3, 0.7, 0.85, 1), "Roughness": 0.6}))
    wd2 = water.modifiers.new("ST_dec", "DECIMATE"); wd2.ratio = 0.02
    set_world((0.95, 0.85, 0.75, 1), 1)


def st_clay():
    """Plastilina stop-motion: todo hecho a mano, mate, con huellas."""
    st_cine()

    def clay(col):
        def f(nt, b):
            b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = 0.85
            tc = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]
            vo = nt.nodes.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = 22; nt.links.new(tc, vo.inputs["Vector"])
            bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.35; nt.links.new(vo.outputs["Distance"], bu.inputs["Height"]); nt.links.new(bu.outputs[0], b.inputs["Normal"])
        return f
    for o, col in ((hand, (0.85, 0.5, 0.36, 1)), (brain, (0.95, 0.45, 0.55, 1)), (d1, (1, 0.75, 0.1, 1)), (d2, (1, 0.75, 0.1, 1)),
                   (water, (0.25, 0.6, 0.8, 1)), (tub, (0.95, 0.93, 0.88, 1)), (floor, (0.55, 0.35, 0.22, 1))):
        assign(o, M("c", nodes=clay(col)))
    assign(wall, M("wa", nodes=tiles_nodes((0.6, 0.78, 0.7, 1), (0.65, 0.82, 0.74, 1), (0.85, 0.85, 0.8, 1), rough=0.9)))


def st_miniatura():
    """Diorama en miniatura: todo parece un juguete, vista desde arriba y desenfoque fuerte (tilt-shift)."""
    st_cine()
    cam.location = (6.5, -9.5, 9.5); cd.lens = 70; cd.dof.aperture_fstop = 0.35
    set_world((0.9, 0.8, 0.7, 1), 0.8)


def st_noche():
    """Thriller / documental nocturno: azul oscuro, contraluz, niebla y luz dura."""
    st_cine(); clear_lights()
    set_world((0.005, 0.008, 0.02, 1), 1); win.hide_render = True
    assign(wall, M("wa", nodes=tiles_nodes((0.05, 0.08, 0.12, 1), (0.06, 0.09, 0.13, 1), (0.1, 0.12, 0.15, 1), rough=0.2)))
    light("SPOT", (2.5, 3, 4), (math.radians(-55), 0, math.radians(150)), 3000, (0.4, 0.65, 1), 0).data.spot_size = math.radians(40)
    light("AREA", (-3, -3, 2), (math.radians(70), 0, math.radians(-40)), 120, (1, 0.6, 0.4), 2)
    assign(brain, M("b", **{"Base Color": (0.9, 0.3, 0.45, 1), "Emission Color": (1, 0.25, 0.45, 1), "Emission Strength": 2.5, "Roughness": 0.4}))


def st_blueprint():
    """Plano técnico: líneas blancas sobre azul, como un dibujo de ingeniería en 3D."""
    set_world((0.03, 0.12, 0.35, 1), 1); sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    for o in (hand, brain, d1, d2, beak, water, tub, wall, floor, win):
        assign(o, emis("bp", (0.04, 0.15, 0.4, 1), 1))
    wall.hide_render = floor.hide_render = win.hide_render = True
    wf = hand.modifiers.new("ST_dec", "DECIMATE"); wf.ratio = 0.15
    cd.dof.use_dof = False
    sc.render.use_freestyle = True; sc.render.line_thickness = 1.3
    vl = bpy.context.view_layer; vl.use_freestyle = True
    ls = vl.freestyle_settings.linesets[0] if vl.freestyle_settings.linesets else vl.freestyle_settings.linesets.new("L")
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("LS")
    ls.select_by_edge_types = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
    ls.linestyle.color = (0.85, 0.95, 1); ls.linestyle.thickness = 1.3


def st_rayosx():
    """Rayos X: siluetas que brillan en los bordes, todo transparente sobre negro."""
    set_world((0, 0, 0, 1), 1); win.hide_render = wall.hide_render = floor.hide_render = True

    def xr(col, s=3):
        m = bpy.data.materials.new("x"); m.use_nodes = True; nt = m.node_tree
        for n in list(nt.nodes): nt.nodes.remove(n)
        lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs[0].default_value = 0.25
        e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = col
        mu = nt.nodes.new("ShaderNodeMath"); mu.operation = "MULTIPLY"; mu.inputs[1].default_value = s
        nt.links.new(lw.outputs["Facing"], mu.inputs[0]); nt.links.new(mu.outputs[0], e.inputs[1])
        tr = nt.nodes.new("ShaderNodeBsdfTransparent"); ad = nt.nodes.new("ShaderNodeAddShader")
        nt.links.new(e.outputs[0], ad.inputs[0]); nt.links.new(tr.outputs[0], ad.inputs[1])
        o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(ad.outputs[0], o.inputs[0]); return m
    assign(hand, xr((0.5, 0.85, 1, 1), 4)); assign(brain, xr((1, 0.4, 0.6, 1), 4))
    for o in (d1, d2, beak): assign(o, xr((1, 0.85, 0.3, 1), 2))
    assign(water, xr((0.3, 0.6, 1, 1), 1.2)); assign(tub, xr((0.6, 0.7, 0.9, 1), 1.5))
    cd.dof.use_dof = False; sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"


def st_pastel():
    """Pastel suave / ilustración infantil: luz plana y difusa, colores caramelo, sin sombras duras."""
    st_cine(); clear_lights()
    set_world((1.0, 0.86, 0.9, 1), 0.55); win.hide_render = True
    for o, col in ((hand, (1, 0.72, 0.62, 1)), (brain, (1, 0.6, 0.75, 1)), (d1, (1, 0.9, 0.45, 1)), (d2, (1, 0.9, 0.45, 1)),
                   (water, (0.6, 0.85, 1, 1)), (tub, (1, 1, 1, 1)), (floor, (0.85, 0.75, 1, 1))):
        assign(o, M("p", **{"Base Color": col, "Roughness": 0.7, "Sheen Weight": 0.5}))
    assign(wall, M("wa", nodes=tiles_nodes((1, 0.82, 0.88, 1), (1, 0.86, 0.9, 1), (1, 0.95, 0.97, 1), rough=0.8)))
    light("AREA", (0, -4, 6), (math.radians(35), 0, 0), 250, (1, 1, 1), 8)


def st_metal():
    """Futurista / producto premium: todo cromado y oro, reflejos, fondo de estudio oscuro."""
    st_cine(); clear_lights(); set_world((0.01, 0.01, 0.015, 1), 1); win.hide_render = True
    assign(hand, M("h", **{"Base Color": (0.95, 0.95, 0.97, 1), "Metallic": 1, "Roughness": 0.12}))
    assign(brain, M("b", **{"Base Color": (1, 0.75, 0.35, 1), "Metallic": 1, "Roughness": 0.2}))
    for o in (d1, d2): assign(o, M("d", **{"Base Color": (1, 0.75, 0.35, 1), "Metallic": 1, "Roughness": 0.15}))
    assign(water, M("w", **{"Base Color": (0.1, 0.1, 0.12, 1), "Metallic": 1, "Roughness": 0.05}))
    assign(wall, M("wa", **{"Base Color": (0.02, 0.02, 0.025, 1)}))
    for i, (x, col) in enumerate(((-4, (1, 0.9, 0.8)), (4, (0.6, 0.8, 1)), (0, (1, 1, 1)))):
        light("AREA", (x, -2 + i, 4), (math.radians(50), 0, math.radians(-x * 8)), 600, col, 1.2)


def st_comic():
    """Cómic: colores planos y saturados, contorno grueso y sombras duras (se le añade trama de puntos después)."""
    st_toon()
    for o, col in ((hand, (1, 0.62, 0.45, 1)), (brain, (1, 0.3, 0.5, 1)), (water, (0.05, 0.45, 1, 1)), (wall, (1, 0.85, 0.15, 1)), (floor, (0.9, 0.2, 0.2, 1))):
        assign(o, toon("c", col, shade=0.35))
    freestyle(4.0)


STYLES = [("01 Pelicula de animacion", st_cine), ("02 Realista documental", st_real), ("03 Dibujo animado", st_toon),
          ("04 Low-poly", st_lowpoly), ("05 Plastilina", st_clay), ("06 Miniatura", st_miniatura), ("07 Noche thriller", st_noche),
          ("08 Plano tecnico", st_blueprint), ("09 Rayos X", st_rayosx), ("10 Pastel infantil", st_pastel), ("11 Metal premium", st_metal),
          ("12 Comic", st_comic)]
only = os.environ.get("ONLY")
for name, fn in STYLES:
    if only and not name.startswith(only):
        continue
    reset(); fn()
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
    print("ok", name, flush=True)
