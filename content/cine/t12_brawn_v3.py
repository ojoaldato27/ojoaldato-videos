"""T12 v3 · Brawn GP con ritmo rápido (pedido por Iker el 20/10: «más frames y menos tiempo cada frame, que ocurra algo
con más frecuencia»): un plano por frase (18), cambio de encuadre cada ~1,3 s al ritmo de los subtítulos, golpe de
cámara en las palabras clave y fundidos cortos. Misma voz y edición «docu» que la v2."""
from t12_brawn_v2 import *          # noqa: F401,F403  (escenas, sprites y ajustes de la v2)
import t12_brawn_v2 as V2B

TITLE = "El_equipo_de_F1_que_costo_una_libra_v3"
BEATS = True
XF = 0.28
SHOTS = [("open", 0, 0, 0), ("question", 1, 1, 0), ("honda", 2, 2, 0), ("pound", 3, 3, 0), ("engine", 4, 4, 0),
         ("livery", 5, 5, 0), ("diffuser", 6, 6, 0), ("floor", 7, 7, 0), ("legal", 8, 8, 0), ("australia", 9, 9, 0),
         ("streak", 10, 10, 0), ("cold", 11, 11, 0), ("points", 12, 12, 0), ("brazil", 13, 13, 0), ("titles", 14, 14, 0),
         ("mercedes", 15, 15, 0), ("eight", 16, 16, 0), ("final", 17, 17, 0)]
NARRATOR = dict(V2B.NARRATOR)
NARRATOR.update({"question": None, "floor": ("point", "left"), "points": None})
PUSH = {"open": (540, 900), "question": (540, 860), "honda": (540, 860), "pound": (580, 860), "engine": (600, 980),
        "livery": (540, 930), "diffuser": (700, 900), "floor": (640, 860), "legal": (600, 860), "australia": (560, 1000),
        "streak": (540, 760), "cold": (560, 900), "points": (520, 820), "brazil": (540, 820), "titles": (560, 860),
        "mercedes": (540, 900), "eight": (540, 820), "final": (580, 900)}


def sh_open(img, t, T, L):
    DC.bg(img, t, 540, 900)
    DC.glow_at(img, 540, 930, 520, (255, 214, 150), 0.22)
    k = ease(clamp((t - 0.05) / 1.0))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([200, 1040, 900, 1085], fill=(0, 0, 0, 90))
    paste(img, spr(bgp_side), lerp(700, 540, k), 930, 0.78, k)
    # destellos al pasar, para que el arranque tenga movimiento
    for i in range(3):
        u = clamp((t - 0.4 - i * 0.9) / 0.5)
        if 0 < u < 1:
            DC.glow_at(img, lerp(260, 820, u), 900, 70, (255, 240, 200), 0.6 * math.sin(u * math.pi))
    DC.pill(img, 610, 1170, "2009 · MUNDIAL DE FÓRMULA 1", ease(clamp((t - 0.6) / 0.4)))


def sh_question(img, t, T, L):
    DC.bg(img, t, 540, 880, seed=4)
    DC.glow_at(img, 540, 900, 460, (255, 214, 150), 0.14)
    paste(img, spr(car_ghost), 540, 930, 0.78, 1.0)
    rr = random.Random(4)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(80):
        u = clamp((t - rr.uniform(0, 1.0)) / 2.0)
        if u <= 0:
            continue
        px, py = rr.uniform(160, 920), rr.uniform(840, 1050)
        yy = py - u * rr.uniform(140, 360)
        xx = px + math.sin(u * 4 + i) * 30
        a = int(210 * math.sin(u * math.pi))
        d.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=(255, 214, 140, a))
    DC.stamp_text(img, 540, 640, "?", 260, GOLD, ease(clamp((t - 0.3) / 0.4)))


def sh_diffuser(img, t, T, L):
    V2B._diffuser(img, t, ease(clamp((t - 0.9) / 0.6)), ease(clamp((t - 0.15) / 0.6)), 0.0)


def sh_floor(img, t, T, L):
    V2B._diffuser(img, t, 1.0, 1.0, ease(clamp((t - lt(L, 0, 0.55)) / 0.5)))


def sh_cold(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=19)
    DC.dust(img, t, 60, 8, (230, 240, 255), 140, (0, 420, W, 1400), 40, (1.5, 3.5))
    DC.glow_at(img, 430, 860, 300, CY_, 0.25)
    paste(img, spr(tyre_cold), 430, 860, 0.85)
    lv = 0.15 + 0.05 * math.sin(t * 2)
    paste(img, spr(thermometer, round(lv, 2)), 820, 860, 0.85)
    k = ease(clamp((t - lt(L, 0, 0.62)) / 1.0))
    if k > 0:
        paste(img, spr(bgp_side, NAVY, (230, 40, 50)), lerp(1500, 560, k), 1190, 0.5, k)


def sh_points(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=21)
    dd = ImageDraw.Draw(img, "RGBA")
    x0 = 170
    for i, (lbl, pts, col) in enumerate((("BUTTON", 95, GOLD), ("VETTEL", 84, (120, 140, 230)))):
        k = ease(clamp((t - 0.1 - i * 0.25) / 0.8))
        y = 700 + i * 230
        wbar = 740 * pts / 95 * k
        dd.rounded_rectangle([x0, y, x0 + max(24, wbar), y + 110], radius=18, fill=col + (255,))
        dd.text((x0, y - 34), lbl, font=DC.font(DC.F_UI, 32), fill=(220, 224, 236), anchor="lm")
        if k > 0.08:
            dd.text((x0 + wbar - 22, y + 56), f"{int(round(pts * k))} pts", font=DC.caps_font(50, "Bold"), fill=(16, 18, 28), anchor="rm")
    DC.pill(img, 620, 1250, "CLASIFICACIÓN FINAL 2009", ease(clamp((t - 0.9) / 0.4)))


FNS = {k: (globals().get("sh_" + k) or getattr(V2B, "sh_" + k)) for k, *_ in SHOTS}
