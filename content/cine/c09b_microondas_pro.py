"""09b · ¿Cómo calienta el microondas sin fuego? — versión «pro» con las mejoras del estudio de competencia (Iker, 30/10):
1. Gancho visual y de texto en el PRIMER fotograma (microondas ya encendido, vapor, pregunta grande en pantalla).
2. Más corto: ~50 s de voz (11 frases), sin relleno.
3. Giro a mitad («Pero ojo: no calienta de dentro hacia fuera»), con su propio golpe visual.
4. Profundidad: sombra suave bajo cada pieza, luz de arriba (brillo/sombra en volumen), resplandor del microondas,
   fondo de cocina desenfocado (profundidad de campo) y viñeta.
5. Voz natural (tools/voz_natural.py: Kokoro español + entonación española) y música «premium».
Datos: magnetrón 2,45 GHz (λ ≈ 12,2 cm); el agua es un dipolo y gira con el campo; penetración de pocos cm;
rejilla con agujeros de 1-2 mm; Percy Spencer, Raytheon, 1945, chocolatina derretida junto a un magnetrón de radar."""
import os
import math
from gadgets import *            # noqa: F401,F403
import flat3 as FL
import vid2
import cine
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED, txt
import ojo as OJ
from PIL import Image, ImageDraw, ImageFilter, ImageChops

cine.VOICE_LEAD = 0.2            # la voz entra casi al momento: el gancho no espera

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "09b_Microondas_pro"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c09b_microondas")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Cómo calienta el microondas tu comida… *sin fuego*?",
    "Dentro esconde un *magnetrón*, que lanza ondas invisibles, como las del wifi.",
    "Y esas ondas buscan el *agua* de tu comida.",
    "Cada molécula de agua es como un *imán diminuto*.",
    "Y las ondas la hacen girar a un lado y al otro, *2.450 millones* de veces por segundo.",
    "Millones de moléculas girando y chocando… y ese roce es *calor*.",
    "Pero ojo: no calienta de dentro hacia fuera. Las ondas solo entran *unos centímetros*.",
    "Por eso el plato *gira*… y por eso el centro a veces sigue *helado*.",
    "¿Y por qué no te cocina a ti? Los agujeros de la rejilla son *más pequeños* que las ondas: no caben, y *rebotan*.",
    "Lo descubrió *Percy Spencer* en 1945, cuando un radar le *derritió la chocolatina* del bolsillo.",
    "Así que… ¿sin fuego? Sí: las ondas hacen *girar el agua* de la comida… y ese roce la *calienta*.",
]
OUTRO_LINE = "La próxima vez que lo enciendas, acuérdate: no es fuego, es agua girando… ¡Ojo al dato!"
NAMES = ["q", "magnet", "water", "dipole", "spin", "heat", "depth", "plate", "mesh", "spencer", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("depth", 0.55)
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR = {}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
FL.use("minimal", HEAD)

FRAME = vid2.frame
FPS = 60
BG = (248, 244, 236)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "suave", "suave_out", "deriva", "suave", "suave_out", "deriva_r", "suave", "deriva", "suave_out"]
TRANS_SEED = 41
TD = 0.9
CAM_PUSH = 0.08
SHAKE = 0
CUT_SFX = False
FL.TH["narr"] = True
OJO_TRAJE = "c_fisico"
OJO_POSES = {}
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
BLUE = (70, 130, 220)
WATER = (96, 160, 236)
WHITE = (255, 255, 255)
STEEL = (226, 228, 234)
WARM = (255, 196, 92)


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


# ------------------------------------------------------------------ profundidad: sombras, luz y resplandor
_GRAD = {}


def _grad(h):
    """Degradado vertical de luz: arriba se aclara, abajo se oscurece (en el tamaño de cada pieza)."""
    h = max(2, int(h))
    if h not in _GRAD:
        col = Image.new("RGB", (1, h))
        al = Image.new("L", (1, h))
        for y in range(h):
            u = y / (h - 1)
            if u < 0.45:
                col.putpixel((0, y), (255, 255, 255))
                al.putpixel((0, y), int(70 * (1 - u / 0.45)))
            else:
                col.putpixel((0, y), (20, 16, 30))
                al.putpixel((0, y), int(60 * (u - 0.45) / 0.55))
        _GRAD[h] = (col, al)
    return _GRAD[h]


def solid(img, fn, sh=0.32, off=(14, 22), blur=22, light=True):
    """Dibuja con fn(capa) en una capa aparte y la pega con sombra suave y luz de volumen."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(lay)
    a = lay.getchannel("A")
    bb = a.getbbox()
    if not bb:
        return
    if sh:
        sm = a.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(blur / 6))
        s = sm.resize((W, H), Image.BILINEAR).point(lambda v: int(v * sh))
        shadow = Image.new("RGBA", (W, H), (50, 36, 24, 0))
        shadow.putalpha(s)
        img.paste(shadow, off, shadow)
    if light:
        x0, y0, x1, y1 = bb
        col, al = _grad(y1 - y0)
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gc = col.resize((x1 - x0, y1 - y0))
        ga = ImageChops.multiply(al.resize((x1 - x0, y1 - y0)), a.crop(bb))
        gc.putalpha(ga)
        g.paste(gc, (x0, y0))
        lay = Image.alpha_composite(lay, g)
    img.paste(lay, (0, 0), lay)


_GLOW = None


def glow(img, cx, cy, rx, ry, col=WARM, a=1.0):
    """Resplandor suave (luz del microondas, calor, vapor)."""
    global _GLOW
    if a <= 0.01 or rx < 2 or ry < 2:
        return
    if _GLOW is None:
        g = Image.new("L", (128, 128), 0)
        d = ImageDraw.Draw(g)
        for r in range(64, 0, -1):
            d.ellipse([64 - r, 64 - r, 64 + r, 64 + r], fill=int(255 * (1 - r / 64) ** 1.6))
        _GLOW = g
    m = _GLOW.resize((int(rx * 2), int(ry * 2)), Image.BILINEAR).point(lambda v: int(v * clamp(a)))
    c = Image.new("RGBA", m.size, col + (0,))
    c.putalpha(m)
    img.paste(c, (int(cx - rx), int(cy - ry)), c)


# ------------------------------------------------------------------ Ojo
def ojo_c(img, cx, cy, sc, pose="point", ang=0.0):
    f = OJ.figure(pose, OJO_TRAJE, 0.0, (0.05, 0.0), 0.0)
    ff = f.resize((max(1, int(f.width * sc)), max(1, int(f.height * sc))), Image.BILINEAR)
    if abs(ang) > 0.01:
        ff = ff.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    x, y = int(cx - ff.width / 2), int(cy - ff.height / 2)
    if img.mode == "RGBA":
        img.alpha_composite(ff, (max(0, x), max(0, y)))
    else:
        img.paste(ff, (x, y), ff)


def ojo_feet(img, x, y, sc, pose="point", ang=0.0):
    f = OJ.figure(pose, OJO_TRAJE, 0.0, (0.05, 0.0), 0.0)
    ojo_c(img, x, y - f.height * sc * 0.45, sc, pose, ang)


def ojo(img, x, y, sc, pose="point", ang=0.0, t=0.0):
    """Ojo con sombra en el suelo y un leve balanceo."""
    bob = 4 * math.sin(t * 3.2)
    d = K.D(img)
    d.ellipse([x - 90 * sc, y - 14 * sc, x + 90 * sc, y + 14 * sc], fill=(40, 30, 20, 60))
    solid(img, lambda L: ojo_feet(L, x, y + bob, sc, pose, ang), sh=0.0, light=False)


# ------------------------------------------------------------------ piezas
def oven(L, cx, cy, s=1.0, glow_k=0.0, t=0.0, plate=True, mesh=True, food=True):
    """Microondas de frente con volumen: cuerpo metálico, ventana, panel con pantalla y botones."""
    d = K.D(L)
    w, h = 640 * s, 400 * s
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(34 * s), fill=STEEL, outline=INK, width=max(3, int(7 * s)))
    d.rounded_rectangle([x0 + 10 * s, y0 + 10 * s, x0 + w - 10 * s, y0 + 26 * s], radius=int(8 * s), fill=(250, 250, 252))
    wx0, wy0, wx1, wy1 = x0 + 34 * s, y0 + 40 * s, x0 + w * 0.7, y0 + h - 40 * s
    inner = tuple(int(lerp(c, g, glow_k)) for c, g in zip((52, 54, 62), (255, 200, 110)))
    d.rounded_rectangle([wx0, wy0, wx1, wy1], radius=int(16 * s), fill=inner, outline=INK, width=max(2, int(6 * s)))
    if glow_k > 0:
        glow(L, (wx0 + wx1) / 2, (wy0 + wy1) / 2, (wx1 - wx0) * 0.45, (wy1 - wy0) * 0.45, (255, 236, 170), 0.8 * glow_k)
    if plate:
        pcx, pcy = (wx0 + wx1) / 2, wy1 - 34 * s
        d.ellipse([pcx - 130 * s, pcy - 18 * s, pcx + 130 * s, pcy + 18 * s], fill=(214, 216, 224), outline=INK, width=max(2, int(4 * s)))
        if food:
            bx = pcx + 50 * s * math.cos(t * 1.6)
            d.rounded_rectangle([bx - 64 * s, pcy - 74 * s, bx + 64 * s, pcy - 6 * s], radius=int(16 * s), fill=(252, 250, 246), outline=INK, width=max(2, int(4 * s)))
            d.ellipse([bx - 54 * s, pcy - 88 * s, bx + 54 * s, pcy - 60 * s], fill=(222, 110, 60), outline=INK, width=max(2, int(3 * s)))
    if mesh:
        step = max(6, int(18 * s))
        for x in range(int(wx0) + step // 2, int(wx1), step):
            for y in range(int(wy0) + step // 2, int(wy1), step):
                d.ellipse([x - 2.2 * s, y - 2.2 * s, x + 2.2 * s, y + 2.2 * s], fill=(20, 20, 24, 90))
    # reflejo diagonal en el cristal
    d.polygon([(wx0 + 30 * s, wy0 + 6 * s), (wx0 + 90 * s, wy0 + 6 * s), (wx0 + 20 * s, wy1 - 6 * s), (wx0 + 6 * s, wy1 - 6 * s)], fill=(255, 255, 255, 40))
    px = x0 + w * 0.7
    d.line([(px, y0 + 12 * s), (px, y0 + h - 12 * s)], fill=INK, width=max(2, int(5 * s)))
    d.rounded_rectangle([px + 28 * s, y0 + 46 * s, x0 + w - 28 * s, y0 + 116 * s], radius=int(10 * s), fill=(24, 30, 36))
    on = glow_k > 0.1
    txt(L, ((px + x0 + w) / 2, y0 + 81 * s), "0:30" if on else "12:00", int(40 * s), (120, 250, 150) if on else (90, 160, 110))
    for r_ in range(3):
        for c_ in range(3):
            bx_ = px + 52 * s + c_ * 46 * s
            by_ = y0 + 160 * s + r_ * 50 * s
            d.ellipse([bx_ - 15 * s, by_ - 15 * s, bx_ + 15 * s, by_ + 15 * s], fill=WHITE, outline=INK, width=max(2, int(3 * s)))
    d.rounded_rectangle([px + 40 * s, y0 + h - 60 * s, x0 + w - 40 * s, y0 + h - 30 * s], radius=int(12 * s), fill=RED, outline=INK, width=max(2, int(3 * s)))
    for fx in (x0 + 60 * s, x0 + w - 60 * s):
        d.rounded_rectangle([fx - 30 * s, y0 + h - 4 * s, fx + 30 * s, y0 + h + 14 * s], radius=int(6 * s), fill=INK)
    return (wx0, wy0, wx1, wy1)


def wave(img, x0, x1, y, amp, lam, ph, col=RED, w=8):
    if x1 - x0 < 8:
        return
    pts = [(x, y + amp * math.sin((x - x0) / lam * 2 * math.pi - ph)) for x in range(int(x0), int(x1) + 4, 4)]
    K.D(img).line(pts, fill=col, width=w, joint="curve")


def molecule(img, cx, cy, s, ang, col=WATER, signs=True):
    """H2O con volumen: oxígeno (−) y dos hidrógenos (+), con brillo."""
    d = K.D(img)
    for da in (-0.9, 0.9):
        hx = cx + math.cos(ang + da) * 72 * s
        hy = cy + math.sin(ang + da) * 72 * s
        d.line([(cx, cy), (hx, hy)], fill=INK, width=max(2, int(9 * s)))
        d.ellipse([hx - 34 * s, hy - 34 * s, hx + 34 * s, hy + 34 * s], fill=WHITE, outline=INK, width=max(2, int(6 * s)))
        d.ellipse([hx - 20 * s, hy - 24 * s, hx - 4 * s, hy - 10 * s], fill=(255, 255, 255, 200))
        if signs:
            txt(img, (hx, hy + 2 * s), "+", int(46 * s), RED)
    d.ellipse([cx - 60 * s, cy - 60 * s, cx + 60 * s, cy + 60 * s], fill=col, outline=INK, width=max(2, int(7 * s)))
    d.ellipse([cx - 38 * s, cy - 44 * s, cx - 8 * s, cy - 20 * s], fill=(255, 255, 255, 120))
    if signs:
        txt(img, (cx, cy + 4 * s), "−", int(70 * s), WHITE)


def steam(img, x, y, t, n=3, h=220, a=170):
    d = K.D(img)
    for i in range(n):
        ph = (t * 0.7 + i / n) % 1
        xx = x + (i - (n - 1) / 2) * 50
        y0 = y - h * ph
        pts = [(xx + 18 * math.sin(yy / 28 + t * 4 + i), yy) for yy in range(int(y0 - 120), int(y0), 8)]
        if len(pts) > 1:
            d.line(pts, fill=(255, 255, 255, int(a * math.sin(math.pi * ph))), width=14, joint="curve")


def hook_text(img, lines, k, y=420, size=104):
    """Texto grande del gancho, con borde blanco: la pregunta va en pantalla desde el primer fotograma."""
    if k <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fo = F(FL.INTER_X, size)
    yy = y
    for s, hl in lines:
        tw = d.textlength(s, font=fo)
        if hl:
            d.rounded_rectangle([540 - tw / 2 - 26, yy - size * 0.62, 540 + tw / 2 + 26, yy + size * 0.62], radius=22, fill=RED + (255,))
            d.text((540, yy), s, font=fo, fill=WHITE, anchor="mm")
        else:
            d.text((540, yy), s, font=fo, fill=INK, anchor="mm", stroke_width=12, stroke_fill=WHITE)
        yy += size * 1.32
    sc = lerp(1.25, 1.0, ease(clamp(k * 3)))
    a = clamp(k)
    if abs(sc - 1) > 0.01:
        lay = lay.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
        lay = lay.crop(((lay.width - W) // 2, int(y * sc - y), (lay.width - W) // 2 + W, int(y * sc - y) + H))
    if a < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.paste(lay, (0, 0), lay)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    """GANCHO, fotograma 1: microondas ya encendido con vapor, pregunta gigante y Ojo alucinando."""
    z = 1.0 + 0.10 * ease(clamp(t / max(1, T)))
    g = 0.75 + 0.2 * math.sin(t * 7)
    glow(img, 600, 900, 520 * z, 300 * z, WARM, 0.55 * g)
    solid(img, lambda Lr: oven(Lr, 600, 900, 1.12 * z, glow_k=g, t=t))
    steam(img, 560, 760, t, n=3, h=200)
    ojo(img, 190, 1420, 0.9, "surprise", t=t)
    # fuego tachado: «sin fuego»
    k = clamp((t - lt(L, 0, 0.55)) / 0.3)
    if k > 0:
        def no_fire(Lr):
            d = K.D(Lr)
            r = 78 * pop(k)
            cx, cy = 920, 1230
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=7)
            d.polygon([(cx, cy - r * 0.6), (cx + r * 0.38, cy + r * 0.2), (cx, cy + r * 0.5), (cx - r * 0.38, cy + r * 0.2)], fill=(255, 140, 40))
            d.line([(cx - r * 0.72, cy + r * 0.72), (cx + r * 0.72, cy - r * 0.72)], fill=RED, width=14)
        solid(img, no_fire)
    hook_text(img, [("¿CALIENTA", False), ("SIN FUEGO?", True)], 1.0 if t < T - 0.8 else clamp((T - t) / 0.8), y=440, size=112)


def sh_magnet(img, t, T, L):
    """Rayos X: el microondas se vuelve transparente y aparece el magnetrón lanzando ondas; un router de wifi al lado."""
    k = ease(clamp(t / 0.9))
    cx, cy = 470, 860

    def body(Lr):
        d = K.D(Lr)
        d.rounded_rectangle([cx - 340, cy - 240, cx + 340, cy + 240], radius=40, fill=(40, 60, 96, int(lerp(255, 215, k))), outline=INK, width=8)
        for x in range(cx - 320, cx + 330, 40):
            d.line([(x, cy - 230), (x, cy + 230)], fill=(110, 150, 220, 50), width=2)
        # magnetrón con aletas
        mx, my = cx - 200, cy - 20
        sc = 0.55 + 0.45 * ease(clamp((t - 0.25) / 0.7))
        for i in range(7):
            y = my - 120 * sc + i * 40 * sc
            d.rounded_rectangle([mx - 120 * sc, y, mx + 120 * sc, y + 14 * sc], radius=4, fill=(205, 208, 218), outline=INK, width=3)
        d.rounded_rectangle([mx - 70 * sc, my - 140 * sc, mx + 70 * sc, my + 140 * sc], radius=int(14 * sc), fill=(196, 120, 70), outline=INK, width=6)
        d.rectangle([mx - 90 * sc, my - 176 * sc, mx + 90 * sc, my - 140 * sc], fill=RED, outline=INK, width=5)
        d.rectangle([mx - 90 * sc, my + 140 * sc, mx + 90 * sc, my + 176 * sc], fill=(60, 96, 210), outline=INK, width=5)
        for j in range(6):
            a = t * 5 + j
            ex, ey = mx + 40 * sc * math.cos(a), my + 40 * sc * math.sin(a)
            d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(140, 230, 255))
        return mx, my

    solid(img, body)
    mx = cx - 200
    reach = (cx + 320) - (mx + 130)
    for j in range(3):
        x_end = mx + 130 + reach * clamp((t - 0.6 - j * 0.15) / 0.9)
        wave(img, mx + 130, x_end, cy - 100 + j * 100, 34, 120, t * 9 + j, col=(255, 90, 90) if j == 1 else (255, 170, 170), w=7)
    glow(img, mx, cy - 20, 160, 160, (120, 220, 255), 0.35 * k)
    # router wifi «como las del wifi»
    kw = clamp((t - lt(L, 0, 0.6)) / 0.35)
    if kw > 0:
        def router(Lr):
            d = K.D(Lr)
            rx, ry = 900, 1270
            s = pop(kw)
            d.rounded_rectangle([rx - 110 * s, ry - 34 * s, rx + 110 * s, ry + 34 * s], radius=16, fill=WHITE, outline=INK, width=5)
            d.line([(rx - 70 * s, ry - 34 * s), (rx - 82 * s, ry - 100 * s)], fill=INK, width=6)
            d.line([(rx + 70 * s, ry - 34 * s), (rx + 82 * s, ry - 100 * s)], fill=INK, width=6)
            for i in range(3):
                d.ellipse([rx - 70 * s + i * 30 * s - 6, ry - 6, rx - 70 * s + i * 30 * s + 6, ry + 6], fill=(80, 220, 120))
            for r in (50, 80, 110):
                a = clamp((math.sin(t * 5 - r / 30) + 1) / 2)
                d.arc([rx - r, ry - 90 - r, rx + r, ry - 90 + r], 225, 315, fill=BLUE + (int(255 * a),), width=7)
        solid(img, router)
    ojo(img, 180, 1420, 0.82, "point", t=t)
    FL.pill(img, 600, 1180, "MAGNETRÓN", clamp((t - lt(L, 0, 0.3)) / 0.3), col=RED)


def sh_water(img, t, T, L):
    """Zoom dentro de la comida: el trozo crece, aparecen gotas y se convierten en moléculas de agua."""
    z = ease(clamp(t / 1.5))
    r = lerp(220, 980, z)
    cy = 880

    def food(Lr):
        d = K.D(Lr)
        d.ellipse([540 - r, cy - r * 0.58, 540 + r, cy + r * 0.58], fill=(226, 120, 66), outline=INK, width=8)
        for i in range(10):
            a = i * 0.63
            d.ellipse([540 + math.cos(a) * r * 0.6 - 30, cy + math.sin(a) * r * 0.3 - 16, 540 + math.cos(a) * r * 0.6 + 30, cy + math.sin(a) * r * 0.3 + 16], fill=(240, 150, 96))
    solid(img, food, sh=0.25 * (1 - z))

    def drops(Lr):
        for i in range(14):
            a = i * 2.4
            rr = (0.2 + (i * 37 % 60) / 100) * min(r, 520) * 0.9
            x, y = 540 + math.cos(a) * rr, cy + math.sin(a) * rr * 0.62 + 10 * math.sin(t * 3 + i)
            s = lerp(0.16, 0.6, z)
            if z > 0.62:
                molecule(Lr, x, y, s * 0.9, a + t * 1.5, signs=False)
            else:
                K.D(Lr).ellipse([x - 40 * s, y - 52 * s, x + 40 * s, y + 40 * s], fill=WATER, outline=INK, width=3)
    solid(img, drops, sh=0.22, off=(8, 12))
    FL.pill(img, 540, 1360, "MUCHA AGUA", clamp((t - lt(L, 0, 0.45)) / 0.3), col=BLUE)


def sh_dipole(img, t, T, L):
    """Molécula gigante con + y −, al lado de un imán de herradura que se le parece."""
    solid(img, lambda Lr: molecule(Lr, 640, 860, 1.75, -math.pi / 2 + 0.08 * math.sin(t * 2)))

    def magnet(Lr):
        d = K.D(Lr)
        mx, my = 230, 760 + 10 * math.sin(t * 2.4)
        d.arc([mx - 100, my - 100, mx + 100, my + 100], 180, 360, fill=RED, width=50)
        d.rectangle([mx - 125, my, mx - 75, my + 110], fill=RED)
        d.rectangle([mx + 75, my, mx + 125, my + 110], fill=RED)
        d.rectangle([mx - 125, my + 110, mx - 75, my + 150], fill=(210, 212, 222), outline=INK, width=4)
        d.rectangle([mx + 75, my + 110, mx + 125, my + 150], fill=(210, 212, 222), outline=INK, width=4)
        txt(Lr, (mx - 100, my + 196), "−", 70, INK)
        txt(Lr, (mx + 100, my + 196), "+", 64, RED)
    k = clamp((t - 0.3) / 0.4)
    if k > 0:
        solid(img, magnet)
        txt(img, (400, 860), "≈", max(2, int(110 * pop(k))), INK)
    ojo(img, 180, 1420, 0.82, "smirk", t=t)
    FL.pill(img, 620, 1360, "UN IMÁN DIMINUTO", clamp((t - lt(L, 0, 0.5)) / 0.3), col=RED)


def sh_spin(img, t, T, L):
    """El campo cambia de sentido y la molécula da la vuelta, cada vez más rápido; contador gigante."""
    f = 1.0 + 3.0 * clamp(t / max(1, T))
    ph = t * f * 2 * math.pi
    sgn = 1 if math.sin(ph) >= 0 else -1
    d = K.D(img)
    for k in range(5):
        y = 560 + k * 105
        x0, x1 = (120, 960) if sgn > 0 else (960, 120)
        d.line([(x0, y), (x1, y)], fill=(240, 150, 150, 170), width=6)
        d.polygon([(x1, y), (x1 - 34 * sgn, y - 18), (x1 - 34 * sgn, y + 18)], fill=(240, 150, 150, 170))
    ang = (math.pi if sgn > 0 else 0) + 0.3 * math.sin(ph * 2)
    solid(img, lambda Lr: molecule(Lr, 540, 820, 1.35, ang))
    FL.speed_lines(img, 300, 600, 780, 1040, clamp(t / 1.5), n=6, seed=int(t * 10) % 4)
    FL.big(img, 540, 1240, "2.450.000.000", 104, RED, clamp((t - lt(L, 0, 0.55)) / 0.3))
    FL.big(img, 540, 1345, "VECES POR SEGUNDO", 46, INK, clamp((t - lt(L, 0, 0.62)) / 0.3))


def sh_heat(img, t, T, L):
    """Muchas moléculas que se agitan y chocan; el aire se calienta, sube el termómetro y sale vapor."""
    g = ease(clamp(t / max(1, T)))
    glow(img, 540, 860, 560, 520, (255, 120, 60), 0.55 * g)

    def mols(Lr):
        for i in range(12):
            x = 150 + (i % 4) * 240 + 34 * math.sin(t * 9 + i)
            y = 600 + (i // 4) * 210 + 34 * math.cos(t * 11 + i * 2)
            molecule(Lr, x, y, 0.55, t * 8 + i, signs=False)
    solid(img, mols, off=(8, 14))
    for i in range(6):
        a = (t * 3 + i * 1.7) % 1
        if a < 0.25:
            x = 200 + (i * 173) % 680
            y = 620 + (i * 211) % 420
            d = K.D(img)
            r = 20 + 60 * a
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 210, 90, int(255 * (1 - a * 4))), width=6)

    def thermo(Lr):
        d = K.D(Lr)
        tx, ty = 950, 820
        d.rounded_rectangle([tx - 26, ty - 260, tx + 26, ty + 160], radius=26, fill=WHITE, outline=INK, width=6)
        d.ellipse([tx - 50, ty + 130, tx + 50, ty + 230], fill=RED, outline=INK, width=6)
        lv = lerp(ty + 140, ty - 230, g)
        d.rectangle([tx - 12, lv, tx + 12, ty + 150], fill=RED)
    solid(img, thermo)
    steam(img, 540, 620, t, n=4, h=260, a=200)
    FL.big(img, 540, 1290, "¡CALOR!", 130, RED, clamp((t - lt(L, 0, 0.72)) / 0.3))


def sh_depth(img, t, T, L):
    """GIRO: «PERO OJO». Corte de una patata: borde caliente, centro frío; las ondas solo entran unos centímetros."""
    k0 = clamp(t / 0.35)
    if t < 1.5:
        FL.stamp(img, 540, 560, "PERO OJO", k0, col=RED)
    myth = clamp((t - 0.7) / 0.3)
    r = 360
    cy = 900

    def potato(Lr):
        d = K.D(Lr)
        d.ellipse([540 - r, cy - r * 0.74, 540 + r, cy + r * 0.74], fill=(244, 118, 84), outline=INK, width=8)
        k = ease(clamp((t - lt(L, 1, 0.0)) / 1.2)) if len(L) > 1 else ease(clamp((t - 1.4) / 1.2))
        ri = r - 120 * k
        if k > 0:
            d.ellipse([540 - ri, cy - ri * 0.74, 540 + ri, cy + ri * 0.74], fill=(150, 190, 246))
    solid(img, potato)
    d = K.D(img)
    for a in range(0, 360, 30):
        ra = math.radians(a + t * 20)
        x0, y0 = 540 + math.cos(ra) * (r + 110), cy + math.sin(ra) * (r + 110) * 0.74
        x1, y1 = 540 + math.cos(ra) * (r - 50), cy + math.sin(ra) * (r - 50) * 0.74
        d.line([(x0, y0), (x1, y1)], fill=RED + (220,), width=6)
    if t > 1.4:
        FL.pill(img, 540, cy, "FRÍO", clamp((t - 2.0) / 0.3), col=BLUE)
    if myth > 0 and t < 3.2:
        mk = myth * clamp((3.2 - t) / 0.4)
        FL.pill(img, 540, 1250, "MITO: DE DENTRO A FUERA", mk, col=INK)
        if t > 1.1:
            d.line([(170, 1250), (910, 1250)], fill=RED + (int(255 * mk),), width=12)
    FL.big(img, 540, 1290, "2-3 cm", 120, RED, clamp((t - max(3.3, lt(L, 1, 0.6) if len(L) > 1 else 3.3)) / 0.3))


def sh_plate(img, t, T, L):
    """Vista desde arriba: el plato gira entre zonas calientes y frías; Ojo muerde y el centro sigue helado."""
    def cavity(Lr):
        d = K.D(Lr)
        d.rounded_rectangle([120, 440, 960, 1180], radius=30, fill=(60, 62, 72), outline=INK, width=8)
        for i, (x, y) in enumerate([(290, 580), (540, 580), (790, 580), (290, 810), (540, 810), (790, 810), (290, 1040), (540, 1040), (790, 1040)]):
            col = (255, 120, 80, 110) if i % 2 == 0 else (110, 160, 240, 110)
            d.ellipse([x - 120, y - 120, x + 120, y + 120], fill=col)
    solid(img, cavity, light=False)
    ang = t * 1.5

    def plate(Lr):
        d = K.D(Lr)
        d.ellipse([290, 560, 790, 1060], fill=(236, 236, 242), outline=INK, width=6)
        d.ellipse([340, 610, 740, 1010], outline=(200, 200, 210), width=4)
        for k in range(3):
            a = ang + k * 2.1
            x, y = 540 + math.cos(a) * 140, 810 + math.sin(a) * 140
            d.ellipse([x - 64, y - 64, x + 64, y + 64], fill=(222, 110, 60), outline=INK, width=4)
    solid(img, plate, off=(10, 16))
    FL.dotted_arc(img, 540, 810, 300, ang, ang + 1.4, 1.0, col=RED)
    kh = clamp((t - lt(L, 0, 0.6)) / 0.3)
    if kh > 0:
        def bite(Lr):
            d = K.D(Lr)
            cx, cy = 820, 1290
            s = pop(kh)
            d.ellipse([cx - 120 * s, cy - 70 * s, cx + 120 * s, cy + 70 * s], fill=(222, 110, 60), outline=INK, width=5)
            d.ellipse([cx - 50 * s, cy - 30 * s, cx + 50 * s, cy + 30 * s], fill=(170, 210, 250))
            for j in range(6):
                a = j * math.pi / 3 + t
                d.line([(cx, cy), (cx + math.cos(a) * 40 * s, cy + math.sin(a) * 24 * s)], fill=WHITE, width=4)
        solid(img, bite)
        FL.pill(img, 820, 1400, "¡HELADO!", kh, col=BLUE)
    ojo(img, 190, 1430, 0.78, "surprise" if kh > 0 else "point", ang=0.04 * math.sin(t * 30) * (kh > 0), t=t)


def sh_mesh(img, t, T, L):
    """La rejilla de la puerta en grande: una onda de 12 cm choca y rebota; la luz sí pasa; Ojo detrás, tan tranquilo."""
    d = K.D(img)

    def door(Lr):
        dd = K.D(Lr)
        dd.rounded_rectangle([480, 400, 600, 1260], radius=18, fill=(46, 48, 56), outline=INK, width=6)
        for y in range(430, 1240, 56):
            dd.ellipse([522, y, 558, y + 36], fill=(255, 240, 180))
    solid(img, door)
    ph = t * 5
    x_end = min(480, 70 + 520 * clamp(t / 1.2))
    wave(img, 70, x_end, 640, 110, 240, ph, col=RED, w=12)
    if t > 1.2:
        wave(img, 70, 480, 640, 80, 240, -ph, col=(240, 150, 150), w=7)
        FL.stamp(img, 330, 480, "NO CABE", clamp((t - 1.3) / 0.3))
    for k in range(4):
        y = 880 + k * 64
        x = 70 + ((t * 600 + k * 180) % 940)
        d.line([(x, y), (x + 80, y)], fill=(255, 200, 60), width=9)
    txt(img, (800, 820), "la luz sí pasa", 44, (196, 140, 20))
    ojo(img, 860, 1420, 0.82, "smirk", t=t)
    FL.big(img, 250, 1170, "12 cm", 96, RED, clamp((t - lt(L, len(L) - 1, 0.1)) / 0.3))
    FL.big(img, 250, 1290, "vs 2 mm", 60, INK, clamp((t - lt(L, len(L) - 1, 0.3)) / 0.3))


def sh_spencer(img, t, T, L):
    """1945: Ojo junto a un radar; la chocolatina del bolsillo se derrite."""
    def radar(Lr):
        d = K.D(Lr)
        d.rectangle([660, 820, 920, 1300], fill=(200, 202, 212), outline=INK, width=6)
        d.pieslice([600, 520, 980, 900], 180, 360, fill=(176, 178, 190), outline=INK, width=6)
        d.line([(790, 710), (790, 610)], fill=INK, width=8)
    solid(img, radar)
    d = K.D(img)
    for r in (90, 150, 210):
        a = int(170 * (0.5 + 0.5 * math.sin(t * 4 - r / 40)))
        d.arc([790 - r, 620 - r, 790 + r, 620 + r], 200, 340, fill=(230, 40, 40, a), width=7)
    ojo(img, 330, 1420, 1.0, "surprise" if t > 1.6 else "point", t=t)
    m = ease(clamp((t - 1.0) / 1.8))

    def choc(Lr):
        dd = K.D(Lr)
        cx, cy = 470, 1140
        dd.rounded_rectangle([cx - 76, cy - 34, cx + 76, cy + 34 + 70 * m], radius=int(10 + 26 * m), fill=(112, 62, 30), outline=INK, width=5)
        if m < 0.5:
            for j in range(3):
                dd.line([(cx - 76 + 50 * (j + 1), cy - 30), (cx - 76 + 50 * (j + 1), cy + 30)], fill=(80, 40, 18), width=4)
        for k in range(3):
            dd.ellipse([cx - 56 + k * 48, cy + 30 + 70 * m, cx - 34 + k * 48, cy + 60 + 130 * m], fill=(112, 62, 30))
    solid(img, choc)
    FL.big(img, 300, 560, "1945", 120, RED, clamp((t - 0.2) / 0.3))


def sh_answer(img, t, T, L):
    """Respuesta clara en 3 pasos (30/10, Iker: «lo de bailar el agua no lo entiendo»):
    ONDAS → el AGUA GIRA → el roce da CALOR, cada paso a la vez que la voz lo dice."""
    k1 = clamp((t - 0.2) / 0.35)
    k2 = clamp((t - lt(L, 0, 0.32)) / 0.35)
    k3 = clamp((t - lt(L, 0, 0.62)) / 0.35)
    y = 840
    xs = (190, 540, 890)
    # 1 · ondas
    if k1 > 0:
        def p1(Lr):
            d = K.D(Lr)
            s = pop(k1)
            d.rounded_rectangle([xs[0] - 140 * s, y - 140 * s, xs[0] + 140 * s, y + 140 * s], radius=36, fill=WHITE, outline=INK, width=6)
        solid(img, p1)
        for j in range(3):
            wave(img, xs[0] - 110, xs[0] + 110, y - 60 + j * 60, 18, 70, t * 9 + j, col=RED if j == 1 else (240, 150, 150), w=6)
        FL.pill(img, xs[0], y + 200, "ONDAS", k1, col=RED)
    # 2 · el agua gira
    if k2 > 0:
        def p2(Lr):
            d = K.D(Lr)
            s = pop(k2)
            d.rounded_rectangle([xs[1] - 140 * s, y - 140 * s, xs[1] + 140 * s, y + 140 * s], radius=36, fill=WHITE, outline=INK, width=6)
            molecule(Lr, xs[1], y, 0.75 * s, t * 9, signs=False)
        solid(img, p2)
        K.D(img).arc([xs[1] - 115, y - 115, xs[1] + 115, y + 115], int(t * 400) % 360, int(t * 400) % 360 + 110, fill=BLUE, width=8)
        FL.pill(img, xs[1], y + 200, "EL AGUA GIRA", k2, col=BLUE)
    # 3 · calor
    if k3 > 0:
        glow(img, xs[2], y, 200, 200, (255, 120, 60), 0.6 * k3)

        def p3(Lr):
            d = K.D(Lr)
            s = pop(k3)
            d.rounded_rectangle([xs[2] - 140 * s, y - 140 * s, xs[2] + 140 * s, y + 140 * s], radius=36, fill=(255, 238, 226), outline=INK, width=6)
            d.rounded_rectangle([xs[2] - 22, y - 100 * s, xs[2] + 22, y + 50 * s], radius=22, fill=WHITE, outline=INK, width=5)
            d.ellipse([xs[2] - 42, y + 30 * s, xs[2] + 42, y + 110 * s], fill=RED, outline=INK, width=5)
            d.rectangle([xs[2] - 10, y - 80 * s, xs[2] + 10, y + 50 * s], fill=RED)
        solid(img, p3)
        steam(img, xs[2], y - 120, t, n=2, h=140, a=200)
        FL.pill(img, xs[2], y + 200, "CALOR", k3, col=RED)
    d = K.D(img)
    for xa, kk in ((365, k2), (715, k3)):
        if kk > 0:
            d.polygon([(xa - 26, y - 22), (xa + 20, y), (xa - 26, y + 22)], fill=INK + (int(255 * kk),))
    ojo(img, 540, 1450, 0.62, "smirk", t=t)
    hook_text(img, [("¿SIN FUEGO?", False), ("¡AGUA GIRANDO!", True)], clamp((t - lt(L, 0, 0.15)) / 0.4), y=440, size=104)


# ------------------------------------------------------------------ fondo de cocina con profundidad de campo
import fondos
_BG = {}


def fondo():
    if "f" not in _BG:
        base = fondos.cocina().convert("RGB")
        top = base.filter(ImageFilter.GaussianBlur(6))
        img = Image.blend(top, Image.new("RGB", (W, H), (250, 244, 234)), 0.18)
        # viñeta suave
        v = Image.new("L", (W, H), 0)
        dv = ImageDraw.Draw(v)
        for i in range(40):
            a = int(60 * (i / 40) ** 2)
            dv.rounded_rectangle([i * 6, i * 9, W - i * 6, H - i * 9], radius=80, outline=60 - a, width=7)
        dark = Image.new("RGB", (W, H), (40, 30, 20))
        img = Image.composite(dark, img, v.filter(ImageFilter.GaussianBlur(30)).point(lambda x: int(x * 0.9)))
        # banda clara para los subtítulos
        ImageDraw.Draw(img, "RGBA").rounded_rectangle([20, 1480, W - 20, 1680], radius=30, fill=(252, 249, 243, 235))
        _BG["f"] = img
    return _BG["f"]


def _con_fondo(fn):
    def run(img, t, T, L):
        img.paste(fondo(), (0, 0))
        fn(img, t, T, L)
        img.paste(fondo().crop((0, 1470, W, H)), (0, 1470))      # zona de subtítulos siempre limpia
    return run


NARR = None
FNS = {n: _con_fondo(globals()["sh_" + n]) for n in NAMES}
FOCUS_PT = {n: (540, 860) for n in NAMES}
FOCUS_PT["q"] = (600, 900)
FOCUS_PT["plate"] = (540, 810)

OUTRO_MIN = 5.5
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {
    "music": [("q", "premium")],
    "gains": {},
    "amb": {},
    "sfx": [("q+0.05", "swell", 0.07), ("magnet+0.5", "zap", 0.05), ("water+0.3", "whoosh_up", 0.06),
            ("dipole+0.4", "pop", 0.05), ("spin+0.4", "whoosh", 0.05), ("heat+0.5", "swell", 0.06),
            ("depth+0.05", "pop", 0.07), ("plate+0.3", "tick", 0.05), ("mesh+1.2", "whoosh", 0.05),
            ("spencer+1.2", "pop", 0.05), ("answer+0.6", "ding", 0.06)],
    "bpm": 100,
}
