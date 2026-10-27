"""Cybertruck · estilo «monigotes Paint» (Iker, 21/10: «aunque monigotes Paint también me gusta… hazme dos vídeos diferentes,
uno de cada, y usa el Cybertruck en ambos»). Dibujos simples a propósito sobre blanco, contorno negro tembloroso que «hierve»
como dibujado a mano, colores planos de Paint, texto negro grande y monigotes que reaccionan. Mismo guion y voz que c01_cyber."""
import math, random
from PIL import Image, ImageDraw
from c01_cyber import *          # noqa: F401,F403
import vid2, dark as DK
from docu import font
from render import W, H, ease, clamp, lerp

TITLE = "Cybertruck_paint"
FRAME = vid2.frame
BG = (255, 255, 255)
TRANS_POOL = ["scribble", "paper", "whip", "iris", "push", "zoom_in", "whip_r"]
TRANS_SEED = 11
FOCUS_PT = {"hook": (560, 900), "press": (540, 900), "musk": (420, 820), "score": (540, 960), "fold": (540, 960),
            "stage": (560, 1000), "ball": (640, 900), "orders": (540, 820)}
CAM_PUSH = 0.04
SHAKE = 14
AUDIO = {"music": [("hook", "warm")], "gains": {"warm": 1.0}, "amb": {}, "bed": [("hook", "end")], "bpm": 112,
         "sfx": [("press+0.8", "impact", 0.12), ("press+0.85", "glitch", 0.05), ("ball+0.75", "glass", 0.12),
                 ("ball+1.55", "glass", 0.10), ("orders+0.2", "pop", 0.08), ("musk+0.3", "pop", 0.06)]}
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
K = (0, 0, 0)
RED, BLUE, YEL, GRAY, DGRAY = (237, 28, 36), (0, 162, 232), (255, 242, 0), (195, 195, 195), (127, 127, 127)


def _seed(t, base=0):
    return base + int(t / 0.12)                     # el trazo «hierve» cada 0,12 s, como dibujado a mano


def J(pts, rng, j=3.0):
    return [(x + rng.uniform(-j, j), y + rng.uniform(-j, j)) for x, y in pts]


def poly(d, pts, fill, rng, w=6, j=3.0):
    p = J(pts, rng, j)
    if fill:
        d.polygon(p, fill=fill)
    d.line(p + [p[0]], fill=K, width=w, joint="curve")


def circ(d, cx, cy, r, fill, rng, w=6, j=2.5):
    pts = [(cx + math.cos(a) * r, cy + math.sin(a) * r) for a in [k * 2 * math.pi / 28 for k in range(28)]]
    poly(d, pts, fill, rng, w, j)


def line(d, pts, rng, col=K, w=6, j=2.5):
    d.line(J(pts, rng, j), fill=col, width=w, joint="curve")


def text(d, xy, txt, size, col=K, anchor="mm"):
    d.text(xy, txt, font=font(BOLD, size), fill=col, anchor=anchor)


def stick(d, x, y, s, rng, mood="happy", arms="down", label=None):
    """Monigote: cabeza (r=70·s) y cuerpo; y es el centro de la cabeza."""
    r = 70 * s
    circ(d, x, y, r, (255, 255, 255), rng, int(7 * s))
    ey = y - 12 * s
    for ex in (x - 24 * s, x + 24 * s):
        d.ellipse([ex - 9 * s, ey - 11 * s, ex + 9 * s, ey + 11 * s], fill=K)
    if mood == "wow":
        d.ellipse([x - 16 * s, y + 20 * s, x + 16 * s, y + 52 * s], fill=K)
    elif mood == "sad":
        d.arc([x - 28 * s, y + 26 * s, x + 28 * s, y + 66 * s], 200, 340, fill=K, width=int(6 * s))
    elif mood == "oops":
        line(d, [(x - 26 * s, y + 36 * s), (x - 10 * s, y + 28 * s), (x + 6 * s, y + 40 * s), (x + 24 * s, y + 30 * s)], rng, K, int(6 * s), 1)
        d.ellipse([x + 52 * s, y - 52 * s, x + 66 * s, y - 30 * s], fill=BLUE)
    else:
        d.arc([x - 30 * s, y + 4 * s, x + 30 * s, y + 46 * s], 20, 160, fill=K, width=int(6 * s))
    b0, b1 = (x, y + r), (x, y + r + 190 * s)
    line(d, [b0, b1], rng, K, int(7 * s))
    sh = (x, y + r + 50 * s)
    A = {"down": [(-80, 120), (80, 120)], "up": [(-100, -60), (100, -60)], "point": [(-80, 120), (150, -20)],
         "hips": [(-70, 60), (70, 60)], "wave": [(-80, 120), (110, -90)]}[arms]
    for ax, ay in A:
        line(d, [sh, (x + ax * s, sh[1] + ay * s)], rng, K, int(7 * s))
    for lx in (-60, 60):
        line(d, [b1, (x + lx * s, b1[1] + 120 * s)], rng, K, int(7 * s))
    if label:
        text(d, (x, y + r + 360 * s), label, int(40 * s))


def truck(d, ox, oy, s, rng, col=GRAY):
    T = lambda pts: [(ox + x * s, oy + y * s) for x, y in pts]
    poly(d, T(DK.CYBER["body"]), col, rng, 7)
    poly(d, T(DK.CYBER["glass"]), (153, 217, 234), rng, 5)
    for ln in DK.CYBER["lines"][:2]:
        line(d, T(ln), rng, K, 4)
    for cx, cy, r in DK.CYBER["wheels"]:
        circ(d, ox + cx * s, oy + cy * s, r * s, K, rng, 6)
        circ(d, ox + cx * s, oy + cy * s, r * s * 0.45, DGRAY, rng, 4)
    line(d, T([(2, 174), (40, 168)]), rng, YEL, 8, 1)


def title(d, t, txt, y=250, size=70):
    k = clamp(t / 0.25)
    if k <= 0:
        return
    lines_ = txt.split("\n")
    for i, ln in enumerate(lines_):
        text(d, (W / 2, y + i * (size + 16) - (1 - ease(k)) * 30), ln, size)


# ------------------------------------------------------------------ escenas
def sh_hook(img, t, T, L):
    rng = random.Random(_seed(t, 1))
    d = ImageDraw.Draw(img)
    title(d, t, "¿POR QUÉ PARECE\nDIBUJADO CON REGLA?")
    truck(d, 40, 700, 1.0, rng)
    u = ease(clamp((t - 1.0) / 1.2))
    if u > 0:                                        # una regla amarilla que se apoya en el techo
        x0, y0, x1, y1 = 40 + 2, 700 + 176 - 30, 40 + 440, 700 + 44 - 30
        ang = math.atan2(y1 - y0, x1 - x0)
        Lr = 520 * u
        ex, ey = x0 + math.cos(ang) * Lr, y0 + math.sin(ang) * Lr
        nx, ny = -math.sin(ang) * 46, math.cos(ang) * 46
        poly(d, [(x0, y0), (ex, ey), (ex - nx, ey - ny), (x0 - nx, y0 - ny)], YEL, rng, 5, 1.5)
        for k in range(1, int(Lr / 26)):
            px, py = x0 + math.cos(ang) * k * 26, y0 + math.sin(ang) * k * 26
            ln_ = 18 if k % 5 == 0 else 10
            d.line([(px, py), (px - math.sin(ang) * -ln_, py - math.cos(ang) * ln_)], fill=K, width=3)
    stick(d, 200, 1260, 0.8, rng, "wow" if t > 2.0 else "happy", "down")
    if t > 2.0:
        text(d, (330, 1150), "??", 80, RED)


def sh_press(img, t, T, L):
    rng = random.Random(_seed(t, 2))
    d = ImageDraw.Draw(img)
    title(d, t, "ACERO SUPERDURO")
    v = clamp((t - 0.3) / 0.5)
    y = lerp(420, 790, ease(v) ** 2)
    poly(d, [(330, 420), (750, 420), (750, 470), (330, 470)], DGRAY, rng)               # pistón
    line(d, [(540, 470), (540, y)], rng, K, 30, 1)
    poly(d, [(300, y), (780, y), (780, y + 110), (300, y + 110)], GRAY, rng)               # prensa
    poly(d, [(250, 920), (830, 920), (830, 950), (250, 950)], (180, 180, 190), rng)        # chapa
    poly(d, [(200, 950), (880, 950), (880, 1040), (200, 1040)], DGRAY, rng)
    if t > 0.8:
        for k in range(6):                                                                 # la prensa se raja
            x = 340 + k * 75
            line(d, [(x, y + 6), (x + 18, y + 40), (x - 6, y + 70), (x + 14, y + 104)], rng, K, 5, 3)
        k = ease(clamp((t - 0.8) / 0.2))
        text(d, (540, 1180), "¡CRACK!", int(130 * (0.7 + 0.3 * k)), RED)
    stick(d, 880, 1300, 0.7, rng, "wow" if t > 0.8 else "happy", "up" if t > 0.8 else "down")


def sh_musk(img, t, T, L):
    rng = random.Random(_seed(t, 3))
    d = ImageDraw.Draw(img)
    poly(d, [(220, 1200), (620, 1200), (580, 1500), (260, 1500)], (185, 122, 87), rng)    # atril
    stick(d, 420, 860, 1.0, rng, "happy", "point", None)
    text(d, (420, 1400), "MUSK", 56, (255, 255, 255))
    k = ease(clamp((t - 0.3) / 0.3))
    if k > 0:
        bx, by = 600, 520
        poly(d, [(bx - 260 * k, by - 150 * k), (bx + 300 * k, by - 150 * k), (bx + 300 * k, by + 150 * k), (bx - 40 * k, by + 150 * k),
                 (bx - 150 * k, by + 260 * k), (bx - 120 * k, by + 150 * k), (bx - 260 * k, by + 150 * k)], (255, 255, 255), rng, 6, 2)
        if k > 0.95:
            text(d, (bx + 20, by - 60), "ESTE ACERO", 52)
            text(d, (bx + 20, by + 10), "NO SE PUEDE", 52)
            text(d, (bx + 20, by + 80), "ESTAMPAR", 52, RED)


def sh_score(img, t, T, L):
    rng = random.Random(_seed(t, 4))
    d = ImageDraw.Draw(img)
    title(d, t, "PARA DOBLARLO...")
    poly(d, [(160, 760), (920, 760), (920, 1120), (160, 1120)], (190, 190, 200), rng)
    u = ease(clamp((t - 0.4) / 1.4))
    if u > 0:
        x = lerp(540, 540, u)
        y1 = lerp(760, 1120, u)
        for yy in range(760, int(y1), 40):
            d.line([(x, yy), (x, min(y1, yy + 24))], fill=RED, width=10)
        stick(d, 820, 1300, 0.7, rng, "happy", "point")
        poly(d, [(x - 10, y1), (x + 14, y1 - 10), (x + 70, y1 - 140), (x + 46, y1 - 150)], BLUE, rng, 4, 1)   # rotulador
    text(d, (540, 1200), "SURCO", 60, RED)


def _fold_pts(u):
    a = math.radians(170 * u)
    right = [(540 + 380 * math.cos(a), 760 + 40 * math.sin(a) * 0), (540 + 380 * math.cos(a), 1120)]
    return right


def sh_fold(img, t, T, L):
    rng = random.Random(_seed(t, 5))
    d = ImageDraw.Draw(img)
    title(d, t, "COMO UN PAPEL DOBLADO")
    u = ease(clamp(t / 1.4))
    if u < 1:
        poly(d, [(160, 760), (540, 760), (540, 1120), (160, 1120)], (190, 190, 200), rng)
        xr = 540 + 380 * math.cos(math.radians(175 * u))
        shade = (int(190 - 60 * math.sin(math.pi * u)),) * 3
        poly(d, [(540, 760), (xr, 760 - 120 * math.sin(math.pi * u)), (xr, 1120 - 120 * math.sin(math.pi * u)), (540, 1120)], shade, rng)
    else:
        v = ease(clamp((t - 1.4) / 1.2))
        truck(d, lerp(160, 40, v), lerp(800, 760, v), lerp(0.5, 1.0, v), rng)
        if v >= 1:
            text(d, (540, 1250), "SOLO PLANOS Y ARISTAS", 52, RED)


def sh_stage(img, t, T, L):
    rng = random.Random(_seed(t, 6))
    d = ImageDraw.Draw(img)
    poly(d, [(60, 420), (1020, 420), (1020, 560), (60, 560)], RED, rng)
    text(d, (540, 490), "2019 · LOS ÁNGELES", 60, (255, 255, 255))
    truck(d, 40, 760, 1.0, rng)
    poly(d, [(0, 1080), (W, 1080), (W, 1110), (0, 1110)], (185, 122, 87), rng)
    for k in range(9):                                                                     # público
        circ(d, 70 + k * 118, 1260 + (k % 2) * 30, 52, (255, 255, 255), rng, 5)
    if t > 1.0:
        text(d, (780, 680), "¡BLINDADO!", 70, BLUE)


def _crack(d, cx, cy, k, rng, R=170):
    for j in range(10):
        a = j * 2 * math.pi / 10 + rng.uniform(-0.2, 0.2)
        pts = [(cx, cy)]
        r = 0
        while r < R * k:
            r += rng.uniform(25, 50)
            a += rng.uniform(-0.3, 0.3)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        d.line(pts, fill=K, width=4)


def sh_ball(img, t, T, L):
    rng = random.Random(_seed(t, 7))
    d = ImageDraw.Draw(img)
    for k, (x0, t0) in enumerate(((180, 0.75), (600, 1.55))):                               # dos cristales
        poly(d, [(x0, 600), (x0 + 360, 600), (x0 + 360, 1000), (x0, 1000)], (153, 217, 234), rng)
        if t > t0:
            _crack(d, x0 + 180, 800, ease(clamp((t - t0) / 0.25)), random.Random(k + 3))
    for k, t0 in enumerate((0.0, 0.8)):
        v = clamp((t - t0) / 0.75)
        if 0 < v < 1:
            tx = 180 + 180 + k * 420
            bx, by = lerp(1100, tx, v), lerp(1300, 800, v)
            circ(d, bx, by, 34, DGRAY, rng, 5)
            for j in range(3):
                line(d, [(bx + 50 + j * 10, by + 20 + j * 18), (bx + 120 + j * 10, by + 60 + j * 18)], rng, K, 4)
    stick(d, 880, 1280, 0.7, rng, "oops" if t > 0.8 else "happy", "hips")
    if t > 1.6:
        text(d, (300, 1250), "¡LOS DOS!", 80, RED)


def sh_orders(img, t, T, L):
    rng = random.Random(_seed(t, 8))
    d = ImageDraw.Draw(img)
    n = int(250000 * ease(clamp((t - 0.2) / 1.4)))
    text(d, (540, 560), f"{n:,}".replace(",", "."), 150, RED)
    text(d, (540, 690), "RESERVAS", 70)
    text(d, (540, 770), "EN POCOS DÍAS", 50, DGRAY)
    for k in range(5):
        stick(d, 140 + k * 200, 1050 + (k % 2) * 40, 0.55, random.Random(_seed(t, 20 + k)), "happy", "up")


FNS = {"hook": sh_hook, "press": sh_press, "musk": sh_musk, "score": sh_score, "fold": sh_fold, "stage": sh_stage, "ball": sh_ball,
       "orders": sh_orders}


# ------------------------------------------------------------------ subtítulos y cierre
def CAPTION(img, t, chunks, y=1560):
    cur = next((c for c in chunks if c[0] - 0.02 <= t < c[1]), None)
    if not cur:
        return
    t0, t1, words = cur
    fo = font(BOLD, 66)
    d = ImageDraw.Draw(img)
    ws = [(w.upper(), hl, a) for w, hl, a, b in words]
    sp = d.textlength(" ", font=fo)
    tw = sum(d.textlength(w, font=fo) for w, _, _ in ws) + sp * (len(ws) - 1)
    if tw > 980:
        fo = font(BOLD, 52)
        sp = d.textlength(" ", font=fo)
        tw = sum(d.textlength(w, font=fo) for w, _, _ in ws) + sp * (len(ws) - 1)
    x = W / 2 - tw / 2
    yy = max(y, 1560)
    for w, hl, a in ws:
        if t >= a - 0.04:                                   # aparecen palabra a palabra, al ritmo de la voz
            d.text((x, yy), w, font=fo, fill=RED if hl else K, anchor="lm")
        x += d.textlength(w, font=fo) + sp


def OUTRO_FN(img, u, D):
    out = Image.new("RGB", (W, H), BG)
    rng = random.Random(_seed(u, 9))
    d = ImageDraw.Draw(out)
    stick(d, 540, 760, 1.0, rng, "happy", "wave")
    k = ease(clamp((u - 0.3) / 0.3))
    if k > 0:
        text(d, (540, 470), "¡DALE A LIKE", int(84 * k + 1))
        text(d, (540, 570), "Y SÍGUEME!", int(84 * k + 1), RED)
    k3 = ease(clamp((u - 1.2) / 0.4))
    if k3 > 0:
        poly(d, [(200, 1380), (500, 1380), (500, 1480), (200, 1480)], (255, 255, 255), rng, 6, 2)
        text(d, (350, 1430), "♥ ME GUSTA", 40, RED)
        follow = u > 2.0
        poly(d, [(580, 1380), (880, 1380), (880, 1480), (580, 1480)], RED if follow else (255, 255, 255), rng, 6, 2)
        text(d, (730, 1430), "SIGUIENDO" if follow else "+ SEGUIR", 40, (255, 255, 255) if follow else K)
        text(d, (540, 1560), "@ojoaldato.ya", 36, DGRAY)
    if u < 0.3:
        out = Image.blend(img, out, ease(u / 0.3))
    return out
