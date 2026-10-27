"""N03 · ¿Cómo sabe tu móvil dónde tocas? (pantalla táctil capacitiva)."""
from neon import *

TITLE = "Como_sabe_tu_movil_donde_tocas"
LINES = [
    "Tu móvil sabe exactamente dónde pones el dedo… pero ¿cómo?",
    "¿Y por qué con guantes *no funciona*?",
    "Bajo el cristal hay una rejilla invisible de *pistas finísimas*.",
    "Unas van en horizontal… y otras en vertical, sin tocarse.",
    "Cada cruce funciona como un pequeño *condensador*: guarda un poquito de carga.",
    "La pantalla manda pulsos eléctricos por cada línea, una tras otra, sin parar.",
    "Y tu cuerpo *conduce la electricidad*.",
    "Al acercar el dedo, *robas un poco de carga* en los cruces de debajo.",
    "El móvil ve qué cruces han cambiado… y calcula *el punto exacto*.",
    "Como cada cruce se lee por separado, puede seguir *varios dedos a la vez*.",
    "¿Y los guantes? La tela *no conduce*: el dedo ya no roba carga y la pantalla no te nota.",
    "Por eso los guantes táctiles llevan *hilo conductor* en las yemas.",
    "Y por eso funciona hasta con cosas raras… como *una salchicha*.",
    "Este tipo de pantalla se describió por primera vez en 1965, en un centro de radares británico.",
    "Hoy la tocamos *miles de veces al día*…",
    "…sin preguntarnos nunca *cómo nos nota*.",
]
SHOTS = [("open", 0, 1, 0.3), ("grid", 2, 3, 0.3), ("cap", 4, 5, 0.3), ("finger", 6, 8, 0.3), ("multi", 9, 9, 0.3),
         ("gloves", 10, 11, 0.3), ("sausage", 12, 12, 0.3), ("history", 13, 15, 1.8)]
FOCUS = {"open": (540, 960, 1.12), "grid": (540, 960, 1.12), "cap": (540, 900, 1.15), "finger": (540, 960, 1.15),
         "multi": (540, 960, 1.12), "gloves": (540, 960, 1.12), "history": (540, 960, 1.12)}
NOTIF = ("cap", 1.0)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon

PX0, PY0, PX1, PY1 = 250, 480, 830, 1460
NX, NY = 7, 12


def phone(d, k=1.0, col=WH):
    rrect(d, PX0, PY0, PX1, PY1, 70, col, 7, k)
    if k > 0.8:
        rrect(d, 470, 510, 610, 540, 14, col, 4)


def nodes():
    xs = [PX0 + 70 + i * (PX1 - PX0 - 140) / (NX - 1) for i in range(NX)]
    ys = [PY0 + 110 + j * (PY1 - PY0 - 220) / (NY - 1) for j in range(NY)]
    return xs, ys


def grid(d, kh=1.0, kv=1.0, dim=1.0):
    xs, ys = nodes()
    ch = tuple(int(c * dim) for c in CY)
    cv = tuple(int(c * dim) for c in MG)
    for j, y in enumerate(ys):
        line(d, [(PX0 + 40, y), (PX1 - 40, y)], ch, 4, clamp(kh * 1.6 - j * 0.05))
    for i, x in enumerate(xs):
        line(d, [(x, PY0 + 60), (x, PY1 - 60)], cv, 4, clamp(kv * 1.6 - i * 0.08))


def finger(d, x, y, col=WH, w=6, glove=False):
    pts = [(x - 70, y + 600), (x - 70, y + 60)] + [(x + math.cos(a) * 70, y + 60 - math.sin(a) * 70) for a in
                                                    [math.pi - k / 12 * math.pi for k in range(13)]] + [(x + 70, y + 600)]
    line(d, pts, col, w)
    if not glove:
        rrect(d, x - 40, y + 10, x + 40, y + 90, 26, tuple(int(c * 0.6) for c in col), 4)
    else:
        for k in range(5):
            d.line([(x - 70, y + 160 + k * 60), (x + 70, y + 140 + k * 60)], fill=tuple(int(c * 0.5) for c in col), width=3)


def heat_nodes(d, fingers, strength=1.0):
    xs, ys = nodes()
    for x in xs:
        for y in ys:
            v = 0.0
            for fx_, fy in fingers:
                v = max(v, math.exp(-((x - fx_) ** 2 + (y - fy) ** 2) / (2 * 90 ** 2)))
            v *= strength
            col = tuple(int(lerp(a, b, v)) for a, b in zip((40, 60, 100), YE))
            dot(d, x, y, 7 + 16 * v, col)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone(d, ease(clamp(t / 1.0)))
    fy = lerp(1300, 900, ease(clamp((t - 0.6) / 1.0)))
    finger(d, 560, fy)
    if t > 1.6:
        for j in range(3):
            u = ((t - 1.6) * 0.8 + j / 3) % 1.0
            circle(d, 560, 900, 30 + u * 160, tuple(int(c * (1 - u)) for c in CY), 5)
    finish(img, lay)
    gtitle2(t, 0.2, "¿CÓMO SABE TU MÓVIL", "DÓNDE TOCAS?", 250, 56, 96, WH, CY, hold=max(1.6, L[1][0] - 0.2))
    if t > L[1][0]:
        chip(t, L[1][0] + 0.2, "¿Y CON GUANTES?", 540, 330, MG, 44)
    vignette(img, 150)


def sh_grid(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone(d, 1.0, DIM)
    a1 = L[1][0]
    grid(d, clamp((t - 0.3) / 1.2), clamp((t - a1) / 1.2))
    finish(img, lay)
    gtitle(t, 0.3, "UNA REJILLA INVISIBLE", 300, 80, CY, pop=False)
    vignette(img, 150)


def sh_cap(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    if t < a1:
        cx, cy = 540, 920
        d.line([(160, cy - 70), (920, cy - 70)], fill=CY, width=14)
        d.line([(cx, cy - 10), (cx, cy + 400)], fill=MG, width=14)
        for k in range(7):
            x = 300 + k * 80
            u = (t * 1.2 + k * 0.15) % 1.0
            d.arc([x - 60, cy - 120, x + 60, cy + 60], 10, 170, fill=tuple(int(c * (0.4 + 0.6 * u)) for c in YE), width=3)
        for k in range(10):
            dot(d, 230 + k * 70, cy - 98, 7, CY)
        label(d, 260, cy - 140, "– – – –", 40, CY, F_MONO)
        gtitle(t, 0.3, "CONDENSADOR", 300, 96, YE)
    else:
        phone(d, 1.0, DIM)
        grid(d, 1, 1, 0.5)
        xs, ys = nodes()
        u = (t - a1) * 2.0
        row = int(u) % NY
        ph = u % 1.0
        y = ys[row]
        x = PX0 + 40 + (PX1 - PX0 - 80) * ph
        d.line([(PX0 + 40, y), (x, y)], fill=CY, width=8)
        dot(d, x, y, 14, WH)
        chip(t, a1 + 0.2, "PULSO A PULSO", 540, 330, CY, 40)
    finish(img, lay)
    vignette(img, 150)


def sh_finger(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone(d, 1.0, DIM)
    grid(d, 1, 1, 0.45)
    a1, a2 = L[1][0], L[2][0]
    fx_, fyt = 600, 980
    q = ease(clamp((t - 0.3) / 1.4))
    fy = lerp(1500, fyt - 40, q)
    if t > a1:
        heat_nodes(d, [(fx_, fyt)], ease(clamp((t - a1) / 0.8)))
        for k in range(6):
            ph = (t * 1.5 + k / 6) % 1.0
            dot(d, lerp(fx_ + (k - 3) * 40, fx_, ph), lerp(fyt + 40, fyt - 30, ph), 6, YE)
    finger(d, fx_, fy)
    if t > a2:
        k = ease(clamp((t - a2) / 0.6))
        d.line([(fx_ - 140 * k, fyt), (fx_ + 140 * k, fyt)], fill=GR, width=4)
        d.line([(fx_, fyt - 140 * k), (fx_, fyt + 140 * k)], fill=GR, width=4)
        circle(d, fx_, fyt, 60, GR, 5, k)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "TU CUERPO CONDUCE", 300, 84, WH, pop=False)
    elif t < a2:
        gtitle(t, a1 + 0.2, "ROBAS CARGA", 300, 96, YE)
    else:
        chip(t, a2 + 0.2, "X: 600 · Y: 980", 540, 330, GR, 44)
    vignette(img, 150)


def sh_multi(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone(d, 1.0, DIM)
    grid(d, 1, 1, 0.45)
    s_ = 0.5 + 0.5 * math.sin(t * 1.6)
    p1 = (540 - 90 - 90 * s_, 980 - 120 - 120 * s_)
    p2 = (540 + 90 + 90 * s_, 980 + 120 + 120 * s_)
    heat_nodes(d, [p1, p2])
    for p in (p1, p2):
        circle(d, p[0], p[1], 50, GR, 5)
    arrow(d, (p1[0] - 10, p1[1] - 10), (p1[0] - 110, p1[1] - 150), GR, 5, s_)
    arrow(d, (p2[0] + 10, p2[1] + 10), (p2[0] + 110, p2[1] + 150), GR, 5, s_)
    finish(img, lay)
    gtitle(t, 0.3, "MULTITÁCTIL", 300, 104, GR)
    vignette(img, 150)


def sh_gloves(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone(d, 1.0, DIM)
    grid(d, 1, 1, 0.4)
    a1 = L[1][0]
    if t < a1:
        finger(d, 560, 940, BL, 7, glove=True)
        k = ease(clamp((t - 1.2) / 0.4))
        line(d, [(420, 800), (700, 1080)], RD, 12, k)
        line(d, [(700, 800), (420, 1080)], RD, 12, clamp(k * 2 - 1))
        gtitle(t, 0.3, "LA TELA NO CONDUCE", 300, 80, RD, pop=False)
    else:
        finger(d, 560, 940, BL, 7, glove=True)
        for k in range(5):
            ph = (t * 2 + k / 5) % 1.0
            dot(d, 520 + k * 20, 960 + 80 * (1 - ph), 6, YE)
        rrect(d, 500, 940, 620, 1010, 30, YE, 6)
        heat_nodes(d, [(560, 950)], ease(clamp((t - a1 - 0.5) / 0.6)))
        gtitle(t, a1 + 0.2, "HILO CONDUCTOR", 300, 90, YE)
    finish(img, lay)
    vignette(img, 150)


def sh_sausage(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone(d, 1.0, DIM)
    grid(d, 1, 1, 0.4)
    q = ease(clamp((t - 0.3) / 1.0))
    y = lerp(1500, 1000, q)
    ang = math.radians(-60)
    cx, cy = 600, y + 160
    L_ = 230
    p0 = (cx - math.cos(ang) * L_, cy - math.sin(ang) * L_)
    p1 = (cx + math.cos(ang) * L_, cy + math.sin(ang) * L_)
    d.line([p0, p1], fill=OR, width=120)
    d.line([p0, p1], fill=(50, 20, 8), width=100)
    for p in (p0, p1):
        dot(d, p[0], p[1], 60, OR)
        dot(d, p[0], p[1], 50, (50, 20, 8))
    for k in range(1, 5):
        u = k / 5
        x = p0[0] + (p1[0] - p0[0]) * u
        yy = p0[1] + (p1[1] - p0[1]) * u
        d.arc([x - 30, yy - 30, x + 30, yy + 30], 200, 300, fill=OR, width=4)
    if q > 0.95:
        tip = p0 if p0[1] < p1[1] else p1
        heat_nodes(d, [tip], ease(clamp((t - 1.3) / 0.6)))
    finish(img, lay)
    gtitle(t, 0.3, "¡UNA SALCHICHA!", 300, 100, OR)
    vignette(img, 150)


def sh_history(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    if t < a1:
        cx, cy = 540, 960
        circle(d, cx, cy, 300, GR, 5)
        circle(d, cx, cy, 200, tuple(int(c * 0.5) for c in GR), 3)
        circle(d, cx, cy, 100, tuple(int(c * 0.5) for c in GR), 3)
        a = t * 2.2
        d.line([(cx, cy), (cx + math.cos(a) * 300, cy + math.sin(a) * 300)], fill=GR, width=6)
        for k in range(1, 20):
            aa = a - k * 0.04
            d.line([(cx, cy), (cx + math.cos(aa) * 300, cy + math.sin(aa) * 300)], fill=tuple(int(c * (1 - k / 20) * 0.4) for c in GR), width=6)
        gtitle(t, 0.3, "1965", 300, 130, GR)
        chip(t, 1.0, "INGLATERRA · RADARES", 540, 500, WH, 36)
    else:
        phone(d, 1.0, CY)
        rr = random.Random(int(t * 4))
        for _ in range(3):
            x, y = rr.uniform(PX0 + 80, PX1 - 80), rr.uniform(PY0 + 120, PY1 - 120)
            circle(d, x, y, rr.uniform(20, 70), YE, 4)
        gtitle(t, a1 + 0.2, "MILES DE VECES", 300, 96, YE, pop=False)
        chip(t, a1 + 0.8, "AL DÍA", 540, 470, WH, 40)
    finish(img, lay)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "creative"), ("cap", "space"), ("finger", "creative"), ("gloves", "playful"), ("history", "space")],
    "gains": {"creative": 0.9},
    "amb": {"hum": ["grid", "cap", "finger", "multi"]},
    "sfx": [("open+0.2", "draw", 0.18), ("open+1.6", "blip", 0.15), ("open@L1+0.2", "pop", 0.2),
            ("grid+0.3", "draw", 0.2), ("grid@L1", "draw", 0.2), ("cap+0.3", "zap", 0.1), ("cap@L1", "blip", 0.1),
            ("cap@L1+0.5", "blip", 0.1), ("cap@L1+1.0", "blip", 0.1), ("finger@L1+0.2", "blip_down", 0.15),
            ("finger@L2+0.2", "ding", 0.1), ("multi+0.3", "pop", 0.2), ("gloves+1.2", "glitch", 0.15),
            ("gloves@L1+0.5", "blip", 0.15), ("sausage+1.3", "pop", 0.25), ("history+0.3", "beep", 0.1),
            ("history@L1+0.2", "pop", 0.15), ("history@L1+0.6", "pop", 0.15)],
    "bed": [("grid", "gloves")],
    "bpm": 108,
}
