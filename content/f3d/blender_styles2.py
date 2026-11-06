"""Muestrario 2 de ESTILOS (Iker 06/11: «ninguno me acaba de gustar, dame otro frame con otros estilos»).
Reutiliza la escena de blender_styles.py. Uso: python3 blender_styles2.py <carpeta>"""
import sys, os, math, runpy
out = sys.argv[1]
os.environ["CLIPS"] = "1"
here = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["x", out, "432", "768", "20"]
G = runpy.run_path(os.path.join(here, "blender_styles.py"))
import bpy
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops, ImageDraw
import random
sc = bpy.context.scene
hand, brain, d1, d2, beak, water, tub, wall, floor, win, cam, cd, tgt = (G[k] for k in ("hand", "brain", "d1", "d2", "beak", "water", "tub", "wall", "floor", "win", "cam", "cd", "tgt"))
M, toon, emis, assign, set_world, light, clear_lights, freestyle, tiles_nodes, skin_nodes = (G[k] for k in (
    "M", "toon", "emis", "assign", "set_world", "light", "clear_lights", "freestyle", "tiles_nodes", "skin_nodes"))
ALL = (hand, brain, d1, d2, beak, water, tub, wall, floor, win)


def remesh_blocks(o, depth=6):
    m = o.modifiers.new("ST_r", "REMESH"); m.mode = "BLOCKS"; m.octree_depth = depth; m.use_remove_disconnected = False


def flat(o, ratio):
    m = o.modifiers.new("ST_dec", "DECIMATE"); m.ratio = ratio
    for p in o.data.polygons:
        p.use_smooth = False


# ---------- post-procesos con PIL
def post_watercolor(p):
    im = Image.open(p).convert("RGB")
    a = im.filter(ImageFilter.ModeFilter(9)).filter(ImageFilter.SMOOTH_MORE)
    edges = im.filter(ImageFilter.FIND_EDGES).convert("L").point(lambda v: 255 - min(255, v * 2))
    paper = Image.effect_noise(im.size, 22).convert("L").filter(ImageFilter.GaussianBlur(1.2))
    a = ImageEnhance.Color(a).enhance(0.85)
    a = ImageChops.multiply(a, Image.merge("RGB", [edges] * 3).filter(ImageFilter.GaussianBlur(0.6)))
    a = ImageChops.multiply(a, Image.merge("RGB", [paper.point(lambda v: 200 + v // 5)] * 3))
    Image.blend(a, Image.new("RGB", im.size, (250, 244, 230)), 0.12).save(p)


def post_pixel(p):
    im = Image.open(p).convert("RGB")
    s = im.resize((im.width // 6, im.height // 6), Image.BILINEAR).quantize(24).convert("RGB")
    s.resize(im.size, Image.NEAREST).save(p)


def post_pencil(p):
    im = Image.open(p).convert("L")
    inv = ImageOps.invert(im).filter(ImageFilter.GaussianBlur(6))
    sk = Image.eval(Image.merge("LA", [im, inv]).getchannel(0), lambda v: v)
    dodge = Image.fromarray(__import__("numpy").clip(__import__("numpy").asarray(im, float) * 255.0 / (256.0 - __import__("numpy").asarray(inv, float)), 0, 255).astype("uint8"))
    paper = Image.effect_noise(im.size, 18).filter(ImageFilter.GaussianBlur(0.8)).point(lambda v: 225 + v // 10)
    out = ImageChops.multiply(dodge, paper)
    Image.merge("RGB", [out, out, out.point(lambda v: max(0, v - 8))]).save(p)


def post_bw(p):
    im = ImageOps.grayscale(Image.open(p)); im = ImageEnhance.Contrast(im).enhance(1.5)
    g = Image.effect_noise(im.size, 30)
    im = Image.blend(im, g, 0.1)
    v = Image.new("L", im.size, 0); dv = ImageDraw.Draw(v)
    for i in range(40):
        dv.ellipse([-im.width * 0.3 + i * 4, -im.height * 0.1 + i * 6, im.width * 1.3 - i * 4, im.height * 1.1 - i * 6], fill=int(255 * i / 40))
    im = ImageChops.multiply(im, v.filter(ImageFilter.GaussianBlur(30)))
    im.convert("RGB").save(p)


# ---------- estilos
SK = (0.75, 0.45, 0.33, 1)


def base_cine():
    G["st_cine"]()


def s_acuarela():
    G["st_toon"](); sc.render.use_freestyle = False
    for o, col in ((hand, (1, 0.7, 0.55, 1)), (brain, (1, 0.55, 0.7, 1)), (water, (0.35, 0.7, 0.95, 1)), (wall, (0.85, 0.92, 0.95, 1)), (floor, (0.95, 0.85, 0.7, 1))):
        assign(o, toon("a", col, shade=0.7))
    return post_watercolor


def s_lapiz():
    base_cine(); return post_pencil


def s_pixel():
    G["st_toon"](); sc.render.use_freestyle = False; return post_pixel


def s_voxel():
    base_cine()
    for o in (hand, brain, d1, d2):
        remesh_blocks(o, 6)
    remesh_blocks(water, 5)


def s_origami():
    base_cine(); clear_lights()
    for o in (hand, brain, d1, d2, tub):
        flat(o, 0.012 if o is not tub else 0.2)
    for o, col in ((hand, (0.98, 0.95, 0.9, 1)), (brain, (1, 0.6, 0.7, 1)), (d1, (1, 0.85, 0.2, 1)), (d2, (1, 0.85, 0.2, 1)), (water, (0.4, 0.75, 0.95, 1)),
                   (tub, (0.97, 0.97, 0.97, 1)), (wall, (0.93, 0.89, 0.82, 1)), (floor, (0.8, 0.72, 0.6, 1))):
        assign(o, M("o", **{"Base Color": col, "Roughness": 0.95}))
    flat(water, 0.01)
    set_world((0.95, 0.9, 0.82, 1), 0.6); win.hide_render = True
    light("SUN", (0, 0, 10), (math.radians(45), math.radians(-30), math.radians(20)), 4, size=2)


def s_bloques():
    """Juguete de bloques de plástico brillante."""
    base_cine()
    for o in (hand, brain, d1, d2):
        remesh_blocks(o, 5)
    for o, col in ((hand, (1, 0.62, 0.35, 1)), (brain, (0.95, 0.2, 0.35, 1)), (d1, (1, 0.8, 0.0, 1)), (d2, (1, 0.8, 0.0, 1)), (water, (0.05, 0.45, 0.95, 1)), (floor, (0.15, 0.6, 0.25, 1))):
        assign(o, M("l", **{"Base Color": col, "Roughness": 0.15, "Coat Weight": 1}))


def s_fieltro():
    base_cine()

    def felt(col):
        def f(nt, b):
            b.inputs["Base Color"].default_value = col; b.inputs["Roughness"].default_value = 1; b.inputs["Sheen Weight"].default_value = 1; b.inputs["Sheen Roughness"].default_value = 0.6
            tc = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]; nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 180; nz.inputs["Detail"].default_value = 14
            nt.links.new(tc, nz.inputs["Vector"]); bu = nt.nodes.new("ShaderNodeBump"); bu.inputs["Strength"].default_value = 0.6
            nt.links.new(nz.outputs["Fac"], bu.inputs["Height"]); nt.links.new(bu.outputs[0], b.inputs["Normal"])
        return f
    for o, col in ((hand, (0.9, 0.55, 0.42, 1)), (brain, (0.95, 0.45, 0.6, 1)), (d1, (1, 0.78, 0.1, 1)), (d2, (1, 0.78, 0.1, 1)), (water, (0.2, 0.55, 0.85, 1)),
                   (tub, (0.95, 0.95, 0.93, 1)), (wall, (0.55, 0.75, 0.7, 1)), (floor, (0.6, 0.4, 0.3, 1))):
        assign(o, M("f", nodes=felt(col)))


def s_noir():
    G["st_real"](); return post_bw


def s_macro():
    """Macro hiperrealista: solo la yema, lente de cerca y desenfoque extremo."""
    base_cine()
    G["tgt"].location = (-0.15, 0.2, 2.0); cam.location = (0.25, -1.6, 2.1); cd.lens = 85; cd.dof.aperture_fstop = 1.2


def s_sombras():
    """Sombras chinescas: siluetas negras a contraluz sobre un cielo de colores."""
    set_world((0.0, 0.0, 0.0, 1), 1)
    for o in ALL:
        assign(o, emis("k", (0.01, 0.01, 0.015, 1), 1))
    wall.hide_render = False
    m = bpy.data.materials.new("sky"); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    tc = nt.nodes.new("ShaderNodeTexCoord"); gr = nt.nodes.new("ShaderNodeTexGradient"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB"); e = ramp.color_ramp.elements
    e[0].color = (1, 0.45, 0.15, 1); e[1].color = (0.25, 0.1, 0.45, 1); e2 = e.new(0.5); e2.color = (1, 0.25, 0.4, 1)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Y"], ramp.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = 1.5; nt.links.new(ramp.outputs[0], em.inputs[0])
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    assign(wall, m); win.hide_render = True; cd.dof.use_dof = False
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"


def s_isometrico():
    """Isométrico limpio: cámara ortográfica en diagonal, colores planos y suaves."""
    G["st_pastel"]()
    cd.type = "ORTHO"; cd.ortho_scale = 9.5; cam.location = (8, -8, 8.5); G["tgt"].location = (0, 0.4, 0.8); cd.dof.use_dof = False


def s_escultura():
    """Escultura de museo: mármol blanco, foco cenital y pared oscura."""
    G["st_real"](); clear_lights()

    def marble(nt, b):
        tc = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]; nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.5
        nz.inputs["Detail"].default_value = 10; nz.inputs["Distortion"].default_value = 4; nt.links.new(tc, nz.inputs["Vector"])
        r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements; e[0].position = 0.47; e[0].color = (0.93, 0.92, 0.9, 1); e[1].position = 0.5; e[1].color = (0.4, 0.4, 0.42, 1)
        e2 = e.new(0.53); e2.color = (0.95, 0.94, 0.92, 1); nt.links.new(nz.outputs["Fac"], r.inputs[0]); nt.links.new(r.outputs[0], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = 0.25; b.inputs["Subsurface Weight"].default_value = 0.2
    for o in (hand, brain, d1, d2, beak, tub):
        assign(o, M("m", nodes=marble))
    assign(water, M("w", **{"Base Color": (0.05, 0.05, 0.06, 1), "Roughness": 0.05}))
    light("SPOT", (0.2, -1.0, 7), (math.radians(8), 0, 0), 3500, (1, 0.95, 0.88), 0).data.spot_size = math.radians(30)
    light("AREA", (-3, -3, 2), (math.radians(70), 0, math.radians(-40)), 60, (0.7, 0.8, 1), 2)


STYLES = [("01 Acuarela", s_acuarela), ("02 Dibujo a lapiz", s_lapiz), ("03 Pixel art", s_pixel), ("04 Voxel", s_voxel),
          ("05 Origami", s_origami), ("06 Bloques de juguete", s_bloques), ("07 Fieltro", s_fieltro), ("08 Cine blanco y negro", s_noir),
          ("09 Macro hiperrealista", s_macro), ("10 Sombras chinescas", s_sombras), ("11 Isometrico", s_isometrico), ("12 Escultura de museo", s_escultura)]
for name, fn in STYLES:
    G["reset"](); G["tgt"].location = (0.15, 0.3, 1.65)
    post = fn()
    p = os.path.join(out, name + ".png"); sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    if post:
        post(p)
    print("ok", name, flush=True)
