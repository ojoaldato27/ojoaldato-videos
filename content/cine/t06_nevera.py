"""T06 · Tu nevera no fabrica frío (estilo Titanic, ilustración detallada con corte lateral)."""
from gadgets import *
import t02_microondas as T2

xf, callout, glow_line, top_shade, wavy = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T2.wavy

TITLE = "Tu_nevera_no_fabrica_frio"
LINES = [
    "Tu nevera *no fabrica frío*.",
    "Entonces… ¿cómo enfría la comida?",
    "Lo que hace es *sacar el calor* de dentro… y echarlo fuera.",
    "Por sus tubos circula un líquido especial: el *refrigerante*.",
    "Dentro de la nevera, ese líquido *hierve*… a temperaturas bajísimas.",
    "Y para hervir necesita calor: se lo *roba a tu comida*.",
    "Igual que el *sudor* te enfría al evaporarse.",
    "Ese gas viaja hasta el *compresor*: el zumbido que oyes.",
    "Al comprimirlo, el gas *se calienta mucho*.",
    "Luego pasa por los tubos de atrás… y *suelta el calor* en tu cocina.",
    "Por eso la parte de atrás está *caliente*.",
    "Al enfriarse, el gas vuelve a ser *líquido*.",
    "Cruza un tubo estrechísimo, pierde presión… y vuelve dentro, listo para *hervir* otra vez.",
    "Un ciclo que se repite *todo el día*.",
    "Por eso, si dejas la nevera abierta para refrescar la cocina… *la calientas*.",
    "Tu nevera es, en realidad, *una bomba de calor*.",
    "A veces, las cosas no funcionan como parecen… sino justo al revés.",
]
SHOTS = [("open", 0, 1, 0.3), ("move", 2, 3, 0.3), ("boil", 4, 6, 0.3), ("compress", 7, 8, 0.3), ("back", 9, 11, 0.3),
         ("valve", 12, 13, 0.3), ("door", 14, 14, 0.3), ("final", 15, 16, 1.8)]
FOCUS = {"boil": (540, 880, 1.1), "compress": (540, 880, 1.1)}
NOTIF = ("boil", 1.0)
HYPE = {"line": 1, "text": ['ENTONCES…', '¿CÓMO ENFRÍA?'], "delay": [0, 0.45]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
KW_OVERRIDE = {16: []}
NARRATOR = {"open": ("wave", "left"), "move": ("point", "left"), "boil": ("surprise", "left"), "compress": ("point", "left"),
            "back": ("point", "left"), "valve": ("think", "left"), "door": ("smirk", "left"), "final": ("think", "left")}

COLD = (120, 200, 255)
HOT = (255, 110, 60)
ORANGE = (255, 150, 60)


# ------------------------------------------------------------------ cocina y nevera de frente
def _room():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, 1250), grad=((90, 84, 80), (60, 56, 54)))
    for y in range(560, 1250, 70):
        off = 50 if (y // 70) % 2 else 0
        for x in range(-100, W + 100, 100):
            c.rect((x + off + 3, y + 3, x + off + 97, y + 67), grad=((150, 146, 140), (118, 114, 108)), r=4)
    c.rect((40, 160, 300, 520), fill=(40, 34, 30), r=6)
    c.rect((54, 174, 286, 506), grad=((14, 20, 44), (40, 30, 60)))
    rr = random.Random(2)
    for i in range(40):
        x, y = rr.uniform(60, 280), rr.uniform(380, 500)
        c.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 210, 140))
    c.line([(170, 174), (170, 506)], (40, 34, 30), 8)
    for k in range(10):
        y0 = 1250 + k * (k + 4) * 6
        y1 = 1250 + (k + 1) * (k + 5) * 6
        for j in range(-8, 9):
            x0a, x0b = 540 + j * 120 * (1 + k * 0.12), 540 + (j + 1) * 120 * (1 + k * 0.12)
            x1a, x1b = 540 + j * 120 * (1 + (k + 1) * 0.12), 540 + (j + 1) * 120 * (1 + (k + 1) * 0.12)
            col = (200, 194, 184) if (j + k) % 2 else (70, 66, 62)
            c.poly([(x0a, y0), (x0b, y0), (x1b, y1), (x1a, y1)], fill=col)
    return c.done().convert("RGBA")


def fridge_front(open_=0.0):
    w, h = 900, 1180
    c = Cv(w, h)
    x0, x1 = 200, 700
    c.shadow((x0 - 20, h - 50, x1 + 40, h), 170, 14)
    if open_ > 0:
        c.rect((x0 + 24, 380, x1 - 24, h - 70), grad=((236, 246, 255), (170, 196, 220)))
        for y in (560, 740, 920):
            c.rect((x0 + 30, y, x1 - 30, y + 10), fill=(220, 236, 250, 220))
            c.rect((x0 + 30, y + 10, x1 - 30, y + 16), fill=(120, 150, 180, 160))
        c.rect((x0 + 80, 450, x0 + 150, 560), grad=((250, 250, 250), (200, 200, 210)), r=6)
        c.rect((x0 + 80, 440, x0 + 150, 470), fill=(60, 120, 220))
        c.ellipse((x0 + 220, 690, x0 + 290, 742), radial=((255, 90, 80), (170, 20, 20)), center=(0.35, 0.3))
        c.ellipse((x0 + 280, 694, x0 + 346, 742), radial=((140, 220, 90), (60, 130, 30)), center=(0.35, 0.3))
        c.rect((x0 + 120, 850, x0 + 300, 920), grad=((255, 230, 200), (220, 170, 120)), r=10)
        c.rect((x0 + 330, 820, x0 + 420, 920), grad=((240, 120, 60), (190, 70, 30)), r=8)
        c.rect((x0 + 60, 1010, x1 - 60, h - 90), fill=(200, 230, 250, 160), r=10)
        c.glow(x0 + 250, 420, 180, (240, 250, 255), 0.9)
    c.rect((x0, 20, x1, h - 60), grad=((228, 232, 238), (150, 156, 164)), horizontal=True, r=26)
    c.rect((x0 + 8, 24, x1 - 8, 36), fill=(255, 255, 255, 90), r=6)
    c.rect((x0, 350, x1, 360), fill=(80, 84, 92))
    c.rect((x1 - 60, 120, x1 - 44, 300), grad=((250, 250, 252), (130, 134, 140)), horizontal=True, r=7)
    if open_ <= 0:
        c.rect((x1 - 60, 420, x1 - 44, 760), grad=((250, 250, 252), (130, 134, 140)), horizontal=True, r=7)
    else:
        c.rect((x0 + 10, 370, x1 - 10, h - 70), fill=(0, 0, 0, 0))
    c.rect((x0 + 40, h - 100, x1 - 40, h - 70), fill=(40, 42, 46), r=6)
    for x in range(x0 + 60, x1 - 60, 22):
        c.line([(x, h - 96), (x, h - 74)], (90, 92, 98), 4)
    im = c.done()
    if open_ > 0:
        d = Image.new("RGBA", im.size, (0, 0, 0, 0))
        cd = Cv(w, h)
        dx = 180 * open_
        cd.poly([(x1, 370), (x1 + dx, 330), (x1 + dx, h - 30), (x1, h - 70)], grad=((150, 156, 164), (220, 224, 230)), horizontal=True)
        for k, y in enumerate((480, 660, 840)):
            cd.poly([(x1 + 6, y), (x1 + dx - 8, y - 22), (x1 + dx - 8, y + 30), (x1 + 6, y + 44)], fill=(200, 230, 250, 200))
        im.alpha_composite(cd.done())
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([x0, 370, x1, h - 70], radius=20, fill=255)
        inner = Cv(w, h)
        inner.rect((x0 + 10, 370, x1 - 10, h - 70), grad=((236, 246, 255), (170, 196, 220)))
        for y in (560, 740, 920):
            inner.rect((x0 + 20, y, x1 - 20, y + 10), fill=(220, 236, 250))
            inner.rect((x0 + 20, y + 10, x1 - 20, y + 16), fill=(120, 150, 180))
        inner.rect((x0 + 80, 450, x0 + 150, 560), grad=((250, 250, 250), (200, 200, 210)), r=6)
        inner.rect((x0 + 80, 440, x0 + 150, 470), fill=(60, 120, 220))
        inner.ellipse((x0 + 220, 690, x0 + 290, 742), radial=((255, 90, 80), (170, 20, 20)), center=(0.35, 0.3))
        inner.ellipse((x0 + 280, 694, x0 + 346, 742), radial=((140, 220, 90), (60, 130, 30)), center=(0.35, 0.3))
        inner.rect((x0 + 120, 850, x0 + 300, 920), grad=((255, 230, 200), (220, 170, 120)), r=10)
        inner.rect((x0 + 330, 820, x0 + 420, 920), grad=((240, 120, 60), (190, 70, 30)), r=8)
        inner.rect((x0 + 60, 1000, x1 - 60, h - 90), fill=(190, 222, 246), r=10)
        inner.glow(x0 + 250, 420, 180, (240, 250, 255), 0.9)
        ii = inner.done()
        ii.putalpha(ImageChops.multiply(ii.getchannel("A"), m))
        im.alpha_composite(ii)
    return im


# ------------------------------------------------------------------ nevera en corte lateral
CB = (230, 380, 780, 1300)  # caja exterior de la nevera en corte


def _cut():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((30, 34, 44), (10, 10, 14)))
    x0, y0, x1, y1 = CB
    c.rect((x0, y0, x1, y1), grad=((200, 204, 212), (130, 134, 142)), horizontal=True, r=20)
    c.rect((x0 + 14, y0 + 14, x1 - 14, y1 - 14), fill=(232, 206, 110))
    for k in range(0, 60):
        y = y0 + 20 + k * 16
        c.line([(x0 + 16, y), (x0 + 50, y - 20)], (210, 176, 80, 160), 2)
        c.line([(x1 - 50, y), (x1 - 16, y - 20)], (210, 176, 80, 160), 2)
    ix0, iy0, ix1, iy1 = x0 + 56, y0 + 56, x1 - 56, y1 - 120
    c.rect((ix0, iy0, ix1, iy1), grad=((226, 238, 250), (176, 200, 222)))
    for y in (560, 760, 960):
        c.rect((ix0 + 20, y, ix1, y + 10), fill=(250, 255, 255, 220))
    c.rect((ix0 + 140, 470, ix0 + 200, 558), grad=((252, 252, 252), (200, 200, 210)), r=6)
    c.rect((ix0 + 140, 462, ix0 + 200, 486), fill=(60, 120, 220))
    c.ellipse((ix0 + 240, 706, ix0 + 300, 758), radial=((255, 90, 80), (170, 20, 20)), center=(0.35, 0.3))
    c.rect((ix0 + 120, 890, ix0 + 300, 958), grad=((255, 230, 200), (220, 170, 120)), r=10)
    c.rect((ix0 + 320, 860, ix0 + 400, 958), grad=((240, 120, 60), (190, 70, 30)), r=8)
    c.rect((x1 - 14, y0, x1 + 16, y1 - 20), grad=((210, 214, 220), (150, 154, 160)), r=8)
    c.rect((x0, y1 - 106, x1, y1), fill=(44, 46, 52), r=12)
    c.ellipse((x0 + 40, y1 - 96, x0 + 170, y1 - 10), radial=((90, 92, 100), (16, 16, 18)), center=(0.36, 0.3))
    return c.done().convert("RGBA")


EVAP = [(296, 440)] + [(296 + (34 if i % 2 else 0), 440 + i * 28) for i in range(1, 12)]
PATH = ([(330, 1260), (330, 1240), (210, 1220), (180, 1200)] +
        [(150 if i % 2 else 200, 1180 - i * 46) for i in range(16)] +
        [(176, 420), (250, 400), (296, 420)] + EVAP[1:] + [(310, 780), (310, 1150), (300, 1236)])
SEG_COLOR = None


def path_color(u):
    if u < 0.06:
        return (255, 80, 50)
    if u < 0.5:
        k = (u - 0.06) / 0.44
        return (255, int(lerp(80, 170, k)), int(lerp(50, 120, k)))
    if u < 0.58:
        return (180, 140, 255)
    if u < 0.82:
        return (130, 210, 255)
    return (90, 240, 255)


def flow(img, t, speed=0.08, n=70, only=None, alpha=1.0):
    pts = PATH
    segs, tot = [], 0
    for p, q in zip(pts, pts[1:]):
        L_ = math.hypot(q[0] - p[0], q[1] - p[1])
        segs.append((p, q, tot, L_))
        tot += L_
    glow_line(img, pts, (120, 130, 150), 6, 4, int(160 * alpha))
    for i in range(n):
        u = (i / n + t * speed) % 1.0
        if only and not (only[0] <= u <= only[1]):
            continue
        s_ = u * tot
        for p, q, a, L_ in segs:
            if a <= s_ <= a + L_:
                k = (s_ - a) / max(1, L_)
                x, y = lerp(p[0], q[0], k), lerp(p[1], q[1], k)
                paste(img, glow(30, path_color(u), 1.0), x, y, 1.0, alpha)
                break


def heat_arrows(img, t, pts_list, col, k=1.0):
    for P_ in pts_list:
        seg = wavy(P_, clamp(k), 12, 60, t * 10)
        if len(seg) > 2:
            glow_line(img, seg, col, 5, 8, 220)
            x2, y2 = seg[-1]
            x1, y1 = seg[-6] if len(seg) > 6 else seg[0]
            a = math.atan2(y2 - y1, x2 - x1)
            d = ImageDraw.Draw(img, "RGBA")
            d.polygon([(x2 + math.cos(a) * 22, y2 + math.sin(a) * 22), (x2 + math.cos(a + 2.5) * 20, y2 + math.sin(a + 2.5) * 20),
                       (x2 + math.cos(a - 2.5) * 20, y2 + math.sin(a - 2.5) * 20)], fill=col + (240,))


def cutaway(img, t, flow_k=1.0, arrows=0.0, labels=0.0, t_lab=0.0):
    AC(img, cached("fridge_cut", _cut))
    if flow_k > 0:
        flow(img, t, alpha=flow_k)
    if arrows > 0:
        heat_arrows(img, t, [[(560, 520), (360, 520)], [(600, 730), (360, 640)], [(560, 920), (360, 760)]], ORANGE, arrows)
        heat_arrows(img, t, [[(170, 700), (40, 640)], [(170, 900), (40, 900)], [(170, 500), (40, 420)]], HOT, arrows)
    if labels > 0:
        callout(img, t, t_lab, 330, 560, 640, 300 + 40, "EVAPORADOR", COLD, 32)
        callout(img, t, t_lab + 0.4, 300, 1236, 780, 1380, "COMPRESOR", (230, 230, 240), 32)
        callout(img, t, t_lab + 0.8, 160, 760, 200, 300 + 40, "CONDENSADOR", HOT, 32)


# ------------------------------------------------------------------ planos
def front(img, t, open_k, mist=0.0):
    AC(img, cached("fridge_room", _room))
    paste(img, spr(fridge_front, round(open_k, 2)), 540, 846, 0.88)
    if open_k > 0:
        paste(img, glow(500, (200, 230, 255), 0.5), 540, 900, 1.0, open_k)
        if mist > 0:
            T2.smoke(img, t, [(560, 1100, 0.9), (700, 1150, 0.9)], col=(230, 244, 255), alpha=int(60 * mist), spread=(160, 30), grow=120, speed=0.4)


def sh_open(img, t, T, L):
    a1 = L[1][0]
    ok = ease(clamp((t - 0.6) / 1.2))
    front(img, t, ok, ok)
    top_shade(img)
    big(t, 0.3, "NO FABRICA FRÍO", 270, 92, WHITE, hold=max(1.6, a1 - 0.3), pop=False)
    vignette(img, 190)


def sh_move(img, t, T, L):
    a1 = L[1][0]
    cutaway(img, t, ease(clamp((t - a1) / 0.8)), ease(clamp((t - 0.4) / 1.4)) * (1 - 0.6 * ease(clamp((t - a1) / 0.6))))
    if t > a1 + 0.6:
        callout(img, t, a1 + 0.6, 200, 900, 640, 1380, "REFRIGERANTE", (200, 180, 255), 34)
    if t < a1:
        big(t, 0.3, "SACA EL CALOR", 280, 96, ORANGE, sub="Y LO ECHA FUERA")
    else:
        big(t, a1 + 0.2, "EL REFRIGERANTE", 290, 84, (200, 180, 255), pop=False)
    vignette(img, 190)


def tube_boil(img, t, t0, steal=0.0):
    sky(img, (20, 30, 50), (6, 8, 14), 1.0)
    cx, cy = 540, 760
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([-20, cy - 150, W + 20, cy + 150], radius=40, fill=(170, 180, 196, 255))
    d.rounded_rectangle([-20, cy - 122, W + 20, cy + 122], radius=30, fill=(40, 60, 100, 255))
    d.rectangle([-20, cy - 10, W + 20, cy + 122], fill=(90, 120, 220, 255))
    rr = random.Random(4)
    for i in range(46):
        x = (rr.uniform(0, W) + t * rr.uniform(40, 120)) % W
        ph = (t * rr.uniform(0.6, 1.4) + rr.random()) % 1.0
        y = cy + 110 - ph * 220
        r = 6 + 16 * ph
        al = int(220 * (1 - ph) if y > cy - 10 else 140 * (1 - ph))
        d.ellipse([x - r, y - r, x + r, y + r], outline=(220, 240, 255, al), width=3)
    spaced(d, 540, cy + 200, "LÍQUIDO HIRVIENDO · BAJO CERO", f(F_SER, 34), (200, 230, 255, 230), 4)
    if steal > 0:
        paste(img, spr(apple), 540, 1180, 1.0)
        heat_arrows(img, t, [[(480, 1080), (420, cy + 160)], [(600, 1080), (660, cy + 160)], [(540, 1060), (540, cy + 170)]], ORANGE, steal)


def apple():
    c = Cv(320, 320)
    c.shadow((40, 280, 280, 316), 150, 8)
    c.ellipse((20, 40, 300, 300), radial=((255, 110, 90), (150, 16, 16)), power=1.1, center=(0.36, 0.3))
    c.ellipse((70, 80, 120, 130), fill=(255, 255, 255, 90))
    c.line([(160, 60), (172, 10)], (90, 60, 30), 10)
    c.poly([(172, 30), (240, 10), (210, 50)], grad=((120, 200, 80), (60, 130, 40)))
    return c.done()


def sweat(img, t, t0):
    sky(img, (230, 170, 130), (180, 110, 80), 1.0)
    rr = random.Random(6)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(60):
        x, y = rr.uniform(0, W), rr.uniform(300, 1500)
        d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=(150, 90, 60, 70))
    for i in range(9):
        x, y = 200 + (i % 3) * 330 + rr.uniform(-40, 40), 600 + (i // 3) * 260 + rr.uniform(-30, 30)
        ph = ((t - t0) * 0.5 + i * 0.13) % 1.0
        r = 60 * (1 - ph * 0.8)
        c = Cv(160, 180)
        c.poly([(80, 10), (130, 100), (80, 170), (30, 100)], fill=None)
        c.ellipse((80 - r, 110 - r, 80 + r, 110 + r), radial=((255, 255, 255, 230), (170, 210, 240, 200)), center=(0.35, 0.3))
        paste(img, c.done(), x, y, 1.0)
        T2.smoke(img, t + i, [(x, y - 50, 0.4)], col=(255, 255, 255), alpha=int(80 * ph), spread=(20, 10), grow=40, speed=0.8)
    overlay(img, (90, 160, 255), 0.25 * ease(clamp((t - t0 - 0.8) / 1.0)))


def sh_boil(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.4:
        tube_boil(img, t, 0, ease(clamp((t - a1) / 1.2)))
    else:
        xf(img, t, a2, lambda im: tube_boil(im, t, 0, 1.0), lambda im: sweat(im, t, a2), 0.7)
    if t < a1:
        big(t, 0.3, "HIERVE", 290, 120, COLD, sub="A TEMPERATURAS BAJÍSIMAS")
    elif t < a2:
        big(t, a1 + 0.3, "ROBA EL CALOR", 290, 96, ORANGE, sub="DE TU COMIDA")
    else:
        big(t, a2 + 0.2, "COMO EL SUDOR", 290, 96, WHITE)
    vignette(img, 190)


def sh_compress(img, t, T, L):
    a1 = L[1][0]
    heat = ease(clamp((t - a1) / 1.6))
    sky(img, (30, 30, 36), (10, 10, 12), 1.0)
    overlay(img, (255, 80, 40), 0.25 * heat)
    cx, cy = 540, 860
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([cx - 300, cy - 420, cx + 300, cy + 420], radius=200, fill=(36, 38, 44, 255), outline=(110, 114, 124, 255), width=10)
    d.rectangle([cx - 160, cy - 200, cx + 160, cy + 300], fill=(70, 74, 84, 255))
    d.rectangle([cx - 140, cy - 190, cx + 140, cy + 290], fill=(16, 18, 24, 255))
    ph = math.sin(t * 9)
    py = cy + 130 + ph * 90
    top = cy - 190
    d.rectangle([cx - 136, py, cx + 136, py + 60], fill=(190, 196, 206, 255))
    d.rectangle([cx - 20, py + 60, cx + 20, cy + 390], fill=(140, 146, 156, 255))
    vol = (py - top)
    rr = random.Random(2)
    col = (int(lerp(130, 255, heat)), int(lerp(210, 100, heat)), int(lerp(255, 60, heat)))
    for i in range(30):
        x = cx - 120 + ((rr.random() * 240 + t * rr.uniform(-80, 80) * (1 + heat)) % 240)
        y = top + 10 + ((rr.random() * vol + t * rr.uniform(-80, 80) * (1 + heat)) % max(10, vol - 20))
        paste(img, glow(26, col, 1.0), x, y, 1.0)
    for i in range(3):
        r = 360 + i * 60 + (t * 120) % 60
        d.arc([cx - r, cy - r, cx + r, cy + r], -30, 30, fill=(255, 255, 255, 60), width=4)
        d.arc([cx - r, cy - r, cx + r, cy + r], 150, 210, fill=(255, 255, 255, 60), width=4)
    if t < a1:
        big(t, 0.3, "EL COMPRESOR", 290, 96, WHITE, sub="EL ZUMBIDO QUE OYES")
    else:
        big(t, a1 + 0.2, "SE CALIENTA", 290, 110, HOT)
    vignette(img, 190)


def coil_back(img, t, glow_k):
    sky(img, (60, 54, 50), (24, 20, 18), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([160, 400, 920, 1320], fill=(70, 72, 78, 255))
    for x in range(200, 900, 26):
        d.line([(x, 440), (x, 1280)], fill=(40, 40, 44, 255), width=4)
    pts = []
    for i in range(14):
        y = 460 + i * 60
        pts += [(220, y), (860, y)] if i % 2 == 0 else [(860, y), (220, y)]
    col = (int(lerp(60, 255, glow_k)), int(lerp(60, 90, glow_k)), int(lerp(66, 40, glow_k)))
    glow_line(img, pts, col, 14, 12, 255)
    if glow_k > 0:
        for i in range(6):
            x = 260 + i * 110
            seg = wavy([(x, 420), (x + 20, 220)], 1.0, 10, 50, t * 8 + i)
            glow_line(img, seg, (255, 170, 100), 3, 6, int(150 * glow_k))


def thermal_back(img, t, t0):
    coil_back(img, t, 1.0)
    k = ease(clamp((t - t0) / 0.6))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle([0, 0, W, H], fill=(40, 30, 140, int(120 * k)))
    od.ellipse([140, 360, 940, 1360], fill=(255, 140, 40, int(160 * k)))
    od.ellipse([300, 520, 780, 1200], fill=(255, 230, 80, int(150 * k)))
    AC(img, ov.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([700, 1180, 960, 1260], radius=14, fill=(0, 0, 0, int(170 * k)))
    d.text((830, 1220), "CALIENTE", font=f(F_SER, 40), fill=(255, 200, 120, int(255 * k)), anchor="mm")


def condense(img, t, t0):
    sky(img, (40, 30, 30), (12, 10, 10), 1.0)
    cx, cy = 540, 820
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([-20, cy - 150, W + 20, cy + 150], radius=40, fill=(150, 156, 166, 255))
    d.rounded_rectangle([-20, cy - 122, W + 20, cy + 122], radius=30, fill=(60, 30, 30, 255))
    k = ease(clamp((t - t0 - 0.3) / 2.0))
    rr = random.Random(8)
    for i in range(40):
        x = (rr.uniform(0, W) + t * 140) % W
        u = x / W
        liquid = clamp((u - (1 - k)) / 0.2)
        y = cy + lerp(rr.uniform(-100, 100), 90 - rr.uniform(0, 30), liquid)
        col = (int(lerp(255, 180, liquid)), int(lerp(110, 140, liquid)), int(lerp(60, 255, liquid)))
        r = lerp(10, 16, liquid)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (220,))
    d.rectangle([0, cy + 70, W * k, cy + 122], fill=(180, 140, 255, 160))
    spaced(d, 540, cy + 210, "GAS  →  LÍQUIDO", f(F_SER, 40), (230, 220, 255, 230), 6)


def sh_back(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.4:
        xf(img, t, a1, lambda im: coil_back(im, t, ease(clamp((t - 0.4) / 1.4))), lambda im: thermal_back(im, t, a1), 0.6)
    else:
        xf(img, t, a2, lambda im: thermal_back(im, t, a1), lambda im: condense(im, t, a2), 0.6)
    if t < a1:
        big(t, 0.3, "SUELTA EL CALOR", 280, 88, HOT, sub="EN TU COCINA")
    elif t < a2:
        big(t, a1 + 0.2, "POR ESO QUEMA", 290, 96, ORANGE)
    else:
        big(t, a2 + 0.2, "VUELVE A LÍQUIDO", 290, 84, (200, 180, 255), pop=False)
    vignette(img, 190)


def capillary(img, t, t0):
    sky(img, (24, 26, 40), (8, 8, 12), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([-20, 660, 380, 860], radius=30, fill=(150, 156, 166, 255))
    d.rounded_rectangle([-20, 680, 380, 840], radius=24, fill=(120, 90, 200, 255))
    d.rectangle([380, 740, 700, 780], fill=(150, 156, 166, 255))
    d.rectangle([380, 750, 700, 770], fill=(150, 120, 230, 255))
    d.rounded_rectangle([700, 620, W + 20, 900], radius=30, fill=(150, 156, 166, 255))
    d.rounded_rectangle([700, 640, W + 20, 880], radius=24, fill=(30, 60, 110, 255))
    rr = random.Random(3)
    for i in range(30):
        x = 720 + ((rr.random() * 360 + t * 160) % 360)
        y = 650 + rr.uniform(0, 220)
        r = rr.uniform(4, 12)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(200, 240, 255, 200), width=2)
    for i in range(10):
        x = 380 + ((i / 10 + t * 1.2) % 1.0) * 320
        paste(img, glow(24, (200, 180, 255), 1.0), x, 760)
    gx, gy = 540, 1080
    d.ellipse([gx - 130, gy - 130, gx + 130, gy + 130], fill=(240, 236, 226, 255), outline=(90, 94, 104, 255), width=12)
    for k in range(9):
        a = math.radians(140 + k * 32.5)
        d.line([(gx + math.cos(a) * 100, gy + math.sin(a) * 100), (gx + math.cos(a) * 118, gy + math.sin(a) * 118)], fill=(40, 40, 44), width=4)
    q = ease(clamp((t - t0 - 0.6) / 1.6))
    a = math.radians(lerp(400, 160, q))
    d.line([(gx, gy), (gx + math.cos(a) * 96, gy + math.sin(a) * 96)], fill=(200, 30, 30), width=8)
    d.ellipse([gx - 14, gy - 14, gx + 14, gy + 14], fill=(40, 40, 44))
    d.text((gx, gy + 60), "PRESIÓN", font=f(F_SER, 28), fill=(60, 60, 70), anchor="mm")
    callout(img, t, t0 + 0.4, 540, 760, 540, 520, "TUBO ESTRECHÍSIMO", (200, 180, 255), 34)


def cycle(img, t, t0):
    cutaway(img, t, 1.0, 0.6, 1.0, t0 + 0.2)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy, r = 880, 1260, 70
    k = ease(clamp((t - t0) / 0.5))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 250, int(240 * k)), outline=(60, 60, 70, int(255 * k)), width=6)
    a = math.radians(-90 + (t - t0) * 360)
    d.line([(cx, cy), (cx + math.cos(a) * 52, cy + math.sin(a) * 52)], fill=(40, 40, 44, int(255 * k)), width=6)
    d.line([(cx, cy), (cx + math.cos(a / 12) * 36, cy + math.sin(a / 12) * 36)], fill=(40, 40, 44, int(255 * k)), width=8)


def sh_valve(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: capillary(im, t, 0), lambda im: cycle(im, t, a1), 0.7)
    if t < a1:
        big(t, 0.4, "PIERDE PRESIÓN", 290, 90, (200, 180, 255), pop=False)
    else:
        big(t, a1 + 0.2, "TODO EL DÍA", 165, 96, YEL)
    vignette(img, 190)


def sh_door(img, t, T, L):
    front(img, t, 1.0, 1.0)
    k = ease(clamp((t - 1.0) / 2.0))
    heat_arrows(img, t, [[(240, 1100), (80, 900)], [(240, 800), (60, 620)], [(860, 1100), (1040, 900)], [(860, 800), (1040, 600)]], HOT, k)
    d = ImageDraw.Draw(img, "RGBA")
    tx, ty = 960, 520
    d.rounded_rectangle([tx - 26, ty - 200, tx + 26, ty + 160], radius=26, fill=(250, 250, 250, 255), outline=(80, 80, 90, 255), width=4)
    lvl = lerp(80, -150, k)
    d.rounded_rectangle([tx - 10, ty + lvl, tx + 10, ty + 140], radius=10, fill=(220, 40, 40, 255))
    d.ellipse([tx - 38, ty + 120, tx + 38, ty + 196], fill=(220, 40, 40, 255))
    overlay(img, (255, 120, 60), 0.18 * k)
    top_shade(img)
    big(t, 0.3, "¿PUERTA ABIERTA?", 260, 80, WHITE, hold=2.2, pop=False)
    big(t, 2.8, "LA COCINA SE CALIENTA", 270, 64, HOT, pop=False)
    vignette(img, 190)


def sh_final(img, t, T, L):
    cutaway(img, t, 1.0, ease(clamp((t - 0.3) / 1.0)))
    top_shade(img, 200, 600)
    r0 = L[1][0] if len(L) > 1 else T          # la reflexión final sustituye al titular
    title2(t, 0.3, "TU NEVERA ES", "UNA BOMBA DE CALOR", 250, 56, 80, hold=max(1.5, r0 - 0.9), c1=WHITE, c2=YEL)
    if len(L) > 1:
        title2(t, r0 + 0.1, "A VECES, LAS COSAS", "FUNCIONAN AL REVÉS", 250, 56, 80, hold=max(2.0, T - r0 - 0.4), c1=WHITE, c2=YEL)
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "mystery"), ("move", "creative"), ("compress", "tension"), ("back", "doc"), ("valve", "creative"),
              ("door", "playful"), ("final", "premium")],
    "gains": {"mystery": 0.8},
    "amb": {"hum": ["open", "move", "compress", "back", "valve", "door", "final"], "room": ["boil"]},
    "sfx": [("open+0.6", "knock", 0.15), ("open+0.8", "whoosh", 0.12), ("open@L1", "chime", 0.06),
            ("move+0.4", "whoosh", 0.12), ("move@L1+0.2", "swell", 0.12),
            ("boil+0.3", "crackle", 0.12), ("boil@L1+0.3", "whoosh_up", 0.12), ("boil@L2", "whoosh", 0.12),
            ("compress+0.3", "hum_on", 0.25), ("compress@L1+0.2", "riser", 0.1),
            ("back@L1", "whoosh", 0.12), ("back@L2+0.3", "pop", 0.14),
            ("valve+0.6", "tick", 0.2), ("valve+1.2", "blip_down", 0.12), ("valve@L1+0.2", "ding", 0.08),
            ("door+0.3", "knock", 0.15), ("door+2.8", "riser", 0.1), ("final+0.3", "swell", 0.14)],
    "bed": [("move", "boil")],
    "bpm": 96,
}
