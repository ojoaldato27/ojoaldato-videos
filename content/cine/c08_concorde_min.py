"""08 · ¿Por qué dejó de volar el Concorde? — estilo 7 con el formato nuevo. Elegido por Iker el 21/10 («El final del
Concorde»). Datos: British Airways «Celebrating Concorde» (2.160 km/h, hasta 60.000 pies ≈ 18.000 m, se estiraba entre
6 y 10 pulgadas ≈ 15-25 cm, Londres–Nueva York en algo menos de 3 h 30 frente a unas 8 h, último vuelo comercial el
24/10/2003); Guinness (récord Nueva York–Londres 2 h 52 min 59 s, 7/2/1996); AeroCorner y Dawn/AFP (20 fabricados, 7 de
BA y 7 de Air France; accidente del vuelo 4590 el 25/7/2000, 109 a bordo y 4 en tierra; caída de la primera clase tras
el 11-S; Airbus dejó de dar piezas; EE. UU. prohibió el vuelo supersónico civil sobre tierra en 1973)."""
import os
import math
from gadgets import *            # noqa: F401,F403
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED, SOFT, txt

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "08_Concorde_estilo7"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c08_concorde")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Por qué dejó de volar el avión de pasajeros *más rápido* de la historia?",
    "El Concorde volaba a *2.160 km/h*: dos veces la velocidad del sonido.",
    "Iba a *18.000 metros* de altura, casi el doble que un avión normal.",
    "Y se calentaba tanto por el roce del aire que *se estiraba*: hasta 25 centímetros en pleno vuelo.",
    "Londres–Nueva York en menos de *tres horas y media*… cuando un avión normal tarda unas ocho.",
    "Su récord: Nueva York–Londres en *2 horas y 53 minutos*, en 1996.",
    "Entonces… ¿qué falló?",
    "Primero, el ruido: al romper la barrera del sonido hacía un *estampido* tan fuerte que Estados Unidos prohibió volar supersónico sobre tierra.",
    "Así que solo podía ir a tope *sobre el mar*.",
    "Segundo: solo se fabricaron *20*, y solo 14 volaron con pasajeros.",
    "Tercero: en julio del 2000, un Concorde de Air France se estrelló en París: murieron *113 personas*.",
    "Y un año después, tras el 11-S, se vendían muchos menos billetes de *primera clase*.",
    "Cuando Airbus dejó de fabricar sus piezas, mantenerlo era *carísimo*.",
    "El 24 de octubre de 2003 hizo su *último vuelo* comercial.",
    "Así que… ¿por qué dejó de volar? No por lento: por *caro, ruidoso* y por un mundo que cambió.",
]
OUTRO_LINE = "Desde entonces, volamos más despacio que en 2003… ¡Ojo al dato!"
NAMES = ["q", "speed", "alt", "stretch", "time", "record", "fail", "boom", "sea", "twenty", "crash", "sept", "airbus",
         "last", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("boom", 1.2)
HEAD = {
    0: ("El más rápido", "¿POR QUÉ DEJÓ DE VOLAR?"),
    1: ("2.160 km/h", "MACH 2: EL DOBLE QUE EL SONIDO"),
    2: ("18.000 metros", "CASI EL DOBLE DE ALTO"),
    3: ("+25 cm", "SE ESTIRABA CON EL CALOR"),
    4: ("3 h 30", "LONDRES – NUEVA YORK"),
    5: ("2 h 53", "EL RÉCORD DE 1996"),
    6: ("¿Qué falló?", "TRES PROBLEMAS"),
    7: ("1 · El ruido", "EL ESTAMPIDO SÓNICO"),
    8: ("Solo sobre el mar", "PROHIBIDO SOBRE TIERRA EN EE. UU."),
    9: ("2 · Solo 20", "Y 14 CON PASAJEROS"),
    10: ("3 · El accidente", "PARÍS, 25 DE JULIO DE 2000"),
    11: ("El 11-S", "MENOS PRIMERA CLASE"),
    12: ("Sin piezas", "MANTENERLO ERA CARÍSIMO"),
    13: ("24-10-2003", "EL ÚLTIMO VUELO"),
    14: ("La respuesta", "CARO, RUIDOSO… Y OTRO MUNDO"),
}
NARRATOR = {}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
FL.use("minimal", HEAD)

FRAME = vid2.frame
FPS = 60
BG = (248, 248, 246)
TRANS_POOL = ["push", "whip", "zoom_in", "iris", "whip_r", "spin"]
TRANS_PLAN = ["whip", "zoom_out", "flash", "whip_r", "zoom_in", "drop", "glitch", "whip", "zoom_out", "flash", "iris", "fall",
              "whip_r", "zoom_in"]
TRANS_SEED = 43
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_profe"
OJO_POSES = {"q": "think", "speed": "surprise", "alt": "point", "stretch": "surprise", "time": "point", "record": "surprise",
             "fail": "think", "boom": "surprise", "sea": "point", "twenty": "point", "crash": "think", "sept": "think",
             "airbus": "smirk", "last": "think", "answer": "smirk"}
ACT = ("stretch", "boom")          # Ojo actúa dentro de la escena
NARR = (lambda img, V, t, shots, si: None if shots[si]["name"] in ACT else FL.NARR(img, V, t, shots, si))
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
OUTRO_MIN = 5.0
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
IDX = {n: i for i, n in enumerate(NAMES)}
SKY = (226, 238, 250)


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def _h(img, name, t):
    FL.head(img, t, IDX[name])


def _sky(img, y0=380, y1=1150):
    K.D(img).rectangle([0, y0, W, y1], fill=SKY)


def _clouds(img, t, speed=300, y0=420, y1=1100, n=5):
    d = K.D(img)
    for k in range(n):
        x = W + 200 - ((t * speed + k * 310) % (W + 400))
        y = y0 + (k * 157) % (y1 - y0)
        for dx, r in ((0, 40), (40, 52), (90, 38)):
            d.ellipse([x + dx - r, y - r, x + dx + r, y + r * 0.6], fill=(255, 255, 255))


def _ojo(img, cx, cy, sc, pose="surprise", ang=0.0, sx=1.0):
    import ojo as OJ
    from PIL import Image
    f = OJ.figure(pose, OJO_TRAJE, 0.0, (0.05, 0.0), 0.0)
    ff = f.resize((max(1, int(f.width * sc * sx)), max(1, int(f.height * sc))), Image.BILINEAR)
    if abs(ang) > 0.01:
        ff = ff.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    img.paste(ff, (int(cx - ff.width / 2), int(cy - ff.height / 2)), ff)


def _clip(img):
    d = K.D(img)
    d.rectangle([0, 0, W, 379], fill=BG)
    d.rectangle([0, 1151, W, H], fill=BG)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    _sky(img)
    _clouds(img, t, 900)
    K.concorde(img, lerp(-300, 540, ease(clamp(t / 1.2))), 760, 0.8)
    FL.speed_lines(img, 60, 700, 260, 820, clamp(t / 0.5), n=5)
    _clip(img)
    FL.big(img, 900, 470, "?", 150, RED, clamp((t - 1.4) / 0.3))
    _h(img, "q", t)


def sh_speed(img, t, T, L):
    _sky(img)
    _clouds(img, t, 1400)
    K.concorde(img, 540, 700, 0.8)
    _clip(img)
    v = 2160 * ease(clamp(t / 1.6))
    FL.big(img, 640, 1050, f"{int(v):,}".replace(",", ".") + " km/h", 110, RED, 1.0)
    FL.pill(img, 640, 1250, "MACH 2", clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "speed", t)


def sh_alt(img, t, T, L):
    d = K.D(img)
    base = 1120
    top = 440
    scale = (base - top) / 19000
    d.rectangle([0, top - 20, W, base], fill=SKY)
    for m in (0, 5000, 10000, 15000):
        y = base - m * scale
        d.line([(60, y), (1020, y)], fill=(200, 214, 230), width=2)
        txt(img, (70, y - 18), f"{m // 1000} km", 30, SOFT, "lm")
    # Everest, avión normal, Concorde
    d.polygon([(130, base), (250, base - 8848 * scale), (370, base)], fill=(200, 200, 206), outline=INK)
    k = ease(clamp((t - 0.3) / 1.4))
    K.plane_top(img, 560, base - 11000 * scale * k, -math.pi / 2 + 0.3, 1.6)
    txt(img, (560, base - 11000 * scale * k + 60), "11 km", 34, INK)
    K.concorde(img, 820, base - 18000 * scale * k, 0.3)
    txt(img, (820, base - 18000 * scale * k + 70), "18 km", 40, RED)
    _h(img, "alt", t)


def sh_stretch(img, t, T, L):
    """Ojo mide con una regla cómo se estira el avión al calentarse."""
    _sky(img)
    st = 1 + 0.12 * ease(clamp((t - 0.6) / 2.0))
    K.concorde(img, 560, 720, 0.85, stretch=st, col=(255, int(250 - 60 * (st - 1) / 0.12), int(252 - 100 * (st - 1) / 0.12)))
    K.ruler(img, 120, 900, 1000, k=clamp((t - 0.2) / 0.6))
    _clip(img)
    _ojo(img, 170, 1000, 0.6, "surprise")
    FL.big(img, 700, 1230, "+25 cm", 120, RED, clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "stretch", t)


def sh_time(img, t, T, L):
    for k, (y, h, lab, col, sc) in enumerate(((600, 3.5, "Concorde", RED, 0.25), (900, 8.0, "Avión normal", INK, 0.0))):
        q = ease(clamp((t - 0.3 - k * 0.3) / 1.2))
        d = K.D(img)
        d.line([(140, y), (940, y)], fill=K.PALE, width=26)
        d.line([(140, y), (140 + 800 * h / 8 * q, y)], fill=col, width=26)
        txt(img, (140, y - 56), lab, 46, col, "lm")
        txt(img, (940, y + 56), f"{h:.1f} h".replace(".", ",").replace(",0 h", " h"), 46, col, "rm")
    _h(img, "time", t)


def sh_record(img, t, T, L):
    frac = clamp(t / 2.0)
    FL.stopwatch(img, 540, 760, 230, frac * 0.48, "2 h 53")
    FL.pill(img, 640, 1220, "7 · 2 · 1996", clamp((t - 0.5) / 0.3), col=RED)
    _h(img, "record", t)


def sh_fail(img, t, T, L):
    _sky(img)
    K.concorde(img, 540, 760 + 30 * math.sin(t * 6), 0.8, ang=0.05 * math.sin(t * 7))
    _clip(img)
    FL.big(img, 540, 1060, "¿?", 160, RED, clamp((t - 0.2) / 0.3))
    _h(img, "fail", t)


def sh_boom(img, t, T, L):
    """Estampido: el cono de choque llega a las casas y Ojo se tapa los oídos."""
    d = K.D(img)
    _sky(img)
    gx = 980
    d.rectangle([0, gx, W, 1150], fill=(200, 210, 170))
    x = lerp(-200, 1200, clamp(t / 3.0))
    K.concorde(img, x, 560, 0.45)
    for k in range(3):
        r = 240 + k * 70
        d.arc([x - 140 - r * 2.2, 560 - r, x - 140, 560 + r * 1.6], 290, 360, fill=(120, 120, 130), width=5)
    for i, hx in enumerate((330, 560, 790)):
        sh = 8 * math.sin(t * 40) if abs(x - 140 - hx) < 360 else 0
        d.rectangle([hx - 60 + sh, gx - 90, hx + 60 + sh, gx], fill=(255, 255, 255), outline=INK, width=5)
        d.polygon([(hx - 75 + sh, gx - 90), (hx + 75 + sh, gx - 90), (hx + sh, gx - 150)], fill=RED, outline=INK)
    _clip(img)
    _ojo(img, 160, 1050, 0.55, "surprise", ang=0.08 * math.sin(t * 30) if t > 1.0 else 0)
    FL.big(img, 680, 1230, "¡BUM!", 130, RED, clamp((t - 1.0) / 0.2))
    _h(img, "boom", t)


def sh_sea(img, t, T, L):
    box = (40, 440, 1040, 1100, -90, 10, 65, 25)
    K.world_map(img, box)
    lon = [(-0.45, 51.47), (-73.78, 40.64)]
    p0, p1 = K.merc(lon[0][0], lon[0][1], box), K.merc(lon[1][0], lon[1][1], box)
    q = ease(clamp(t / 1.8))
    d = K.D(img)
    d.line([p0, (lerp(p0[0], p1[0], q), lerp(p0[1], p1[1], q))], fill=RED, width=8)
    K.plane_top(img, lerp(p0[0], p1[0], q), lerp(p0[1], p1[1], q), math.atan2(p1[1] - p0[1], p1[0] - p0[0]), 1.4)
    txt(img, (p0[0] - 40, p0[1] + 40), "Londres", 34, INK)
    txt(img, (p1[0] + 60, p1[1] + 40), "Nueva York", 34, INK)
    _h(img, "sea", t)


def sh_twenty(img, t, T, L):
    n = int(clamp(t / 1.6) * 20)
    for i in range(n):
        x = 160 + (i % 5) * 190
        y = 520 + (i // 5) * 150
        col = RED if (i < 14 and t > lt(L, 0, 0.55)) else (200, 200, 206)
        K.concorde(img, x, y, 0.15, col=col if col != (200, 200, 206) else (235, 235, 238))
        if col == RED:
            K.D(img).ellipse([x - 8, y + 34, x + 8, y + 50], fill=RED)
    FL.big(img, 640, 1240, "14 de 20", 100, RED, clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "twenty", t)


def sh_crash(img, t, T, L):
    """Escena sobria: fecha y cifra, sin dibujar el accidente."""
    d = K.D(img)
    d.rounded_rectangle([140, 460, 940, 1100], radius=30, fill=(36, 36, 42))
    txt(img, (540, 600), "25 · 07 · 2000", 70, (255, 255, 255))
    txt(img, (540, 700), "Vuelo 4590 · París", 46, (200, 200, 206))
    k = clamp((t - lt(L, 0, 0.6)) / 0.4)
    if k > 0:
        FL.big(img, 540, 880, "113", 170, RED, k)
        txt(img, (540, 1010), "víctimas", 46, (200, 200, 206))
    _h(img, "crash", t)


def sh_sept(img, t, T, L):
    d = K.D(img)
    rows, cols = 3, 4
    for r in range(rows):
        for c in range(cols):
            x, y = 230 + c * 210, 560 + r * 190
            empty = (r * cols + c) % 3 != 0 and t > 0.8
            d.rounded_rectangle([x - 70, y - 80, x + 70, y + 60], radius=20, fill=(255, 255, 255) if empty else (120, 60, 70), outline=INK, width=5)
            d.rounded_rectangle([x - 80, y + 50, x + 80, y + 80], radius=12, fill=(90, 50, 56))
    FL.pill(img, 640, 1240, "2001 · PRIMERA CLASE VACÍA", clamp((t - 0.6) / 0.3))
    _h(img, "sept", t)


def sh_airbus(img, t, T, L):
    d = K.D(img)
    # llave inglesa tachada y billetes que vuelan
    d.line([(380, 900), (700, 580)], fill=(150, 150, 160), width=40)
    d.ellipse([650, 520, 770, 640], fill=(150, 150, 160))
    d.ellipse([690, 560, 730, 600], fill=BG)
    k = ease(clamp((t - 0.4) / 0.4))
    d.line([(300, 500), (300 + 500 * k, 500 + 500 * k)], fill=RED, width=22)
    FL.bills(img, 760, 1080, int(clamp(t / 1.5) * 6) + 1, 0.8)
    FL.big(img, 640, 1240, "€€€", 110, RED, clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "airbus", t)


def sh_last(img, t, T, L):
    _sky(img)
    d = K.D(img)
    d.rectangle([0, 1010, W, 1150], fill=(110, 110, 118))
    for x in range(0, W, 120):
        d.rectangle([x + 20, 1070, x + 80, 1082], fill=(255, 255, 255))
    q = ease(clamp(t / 2.4))
    K.concorde(img, lerp(-100, 600, q), lerp(700, 960, q), 0.7, ang=lerp(-0.12, 0.0, q), nose=1.0)
    _clip(img)
    FL.stamp(img, 640, 1240, "FIN · 2003", clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "last", t)


def sh_answer(img, t, T, L):
    items = [("Caro", 0.45), ("Ruidoso", 0.55), ("Otro mundo", 0.8)]
    for k, (s, fr) in enumerate(items):
        kk = clamp((t - lt(L, 0, fr)) / 0.3)
        if kk > 0:
            y = 580 + k * 170
            FL.big(img, 240, y, "✓", 90, RED, kk, fo=F(FL.DJ, 90))
            txt(img, (330, y), s, 72, INK, "lm")
    _h(img, "answer", t)


FNS = {n: globals()["sh_" + n] for n in NAMES}
FOCUS_PT = {n: (540, 780) for n in NAMES}

AUDIO = {
    "music": [("q", "lofi_hh")],
    "gains": {},
    "amb": {"wind": ["q", "speed", "fail"]},
    "sfx": [("q+0.2", "whoosh", 0.08), ("speed+0.3", "whoosh_up", 0.08), ("alt+0.5", "swell", 0.06), ("stretch+0.6", "click", 0.1),
            ("time+0.3", "tick", 0.06), ("record+0.3", "tick", 0.06), ("fail+0.2", "swell", 0.06), ("boom+1.0", "boom", 0.4),
            ("sea+0.3", "whoosh", 0.07), ("twenty+0.3", "pop", 0.06), ("sept+0.6", "paper", 0.1), ("airbus+0.4", "pop", 0.06),
            ("last+0.5", "rumble", 0.2), ("answer+0.4", "ding", 0.06)],
    "bpm": 100,
}
