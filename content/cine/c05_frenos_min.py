"""05 · Cómo frena un F1 — estilo 7 «minimal blanco» con el formato nuevo (pregunta de gancho respondida al final, Ojo de
narrador inventor, marcador rojo, cierre «Ojo al dato»). Elegido por Iker el 21/10 de la lista de ideas («Frenar un F1»).
Datos: Brembo (Abu Dabi: 322 → 74 km/h en 2,63 s y 120 m; picos de 5,4 G; 168 kg en el pedal; discos a 1.000 °C;
54 toneladas en el pedal en toda la carrera)."""
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
TITLE = "05_Frenos_F1_estilo7"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c05_frenos")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Cómo puede un F1 perder *250 km/h* en menos de *3 segundos*?",
    "En Abu Dabi, un F1 llega a una curva a *322 km/h*… y frena hasta 74.",
    "Tarda solo *2,6 segundos*, y lo hace en *120 metros*.",
    "Eso es frenar con más de *5 G*.",
    "Tu cuerpo pesaría *cinco veces más*: si pesas 80 kilos, el cinturón te aguanta como si pesaras *400*.",
    "Primer secreto: el *aire*.",
    "Los alerones aplastan el coche contra el suelo… y cuanto más rápido va, *más agarre* tiene.",
    "Segundo secreto: los frenos son de *carbono*.",
    "Los discos llegan a *1.000 grados*… y brillan al rojo vivo.",
    "Un disco normal se estropearía; el de carbono, cuanto más caliente, *mejor frena*.",
    "Y el piloto pisa el freno con unos *168 kilos* de fuerza… con una sola pierna.",
    "En toda la carrera, eso suma *54 toneladas*.",
    "Así que… ¿cómo lo hace? Con aire que lo aplasta, frenos al rojo vivo… y *una pierna de acero*.",
]
OUTRO_LINE = "La próxima vez que frenes en un semáforo, acuérdate… ¡Ojo al dato!"
NAMES = ["q", "curve", "time", "g5", "body", "air", "grip", "carbon", "hot", "better", "pedal", "tons", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("carbon", 0.6)
HEAD = {
    0: ("−250 km/h", "EN MENOS DE 3 SEGUNDOS"),
    1: ("322 km/h", "LLEGADA A LA CURVA · ABU DABI"),
    2: ("2,6 segundos", "Y SOLO 120 METROS"),
    3: ("5 G", "LA FUERZA DE LA FRENADA"),
    4: ("×5", "LO QUE PESARÍA TU CUERPO"),
    5: ("Secreto 1", "EL AIRE"),
    6: ("Más rápido, más agarre", "LOS ALERONES LO APLASTAN"),
    7: ("Secreto 2", "FRENOS DE CARBONO"),
    8: ("1.000 °C", "LOS DISCOS AL ROJO VIVO"),
    9: ("Caliente = mejor", "EL TRUCO DEL CARBONO"),
    10: ("168 kilos", "DE FUERZA EN EL PEDAL"),
    11: ("54 toneladas", "EN TODA LA CARRERA"),
    12: ("La respuesta", "AIRE, CARBONO Y UNA PIERNA DE ACERO"),
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
TRANS_PLAN = ["whip", "zoom_in", "flash", "drop", "whip_r", "spin", "zoom_out", "flash", "iris", "fall", "glitch", "zoom_out"]
TRANS_SEED = 31
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_inventor"
OJO_POSES = {"q": "think", "curve": "point", "time": "surprise", "g5": "surprise", "body": "smirk", "air": "point",
             "grip": "point", "carbon": "point", "hot": "surprise", "better": "smirk", "pedal": "point", "tons": "surprise",
             "answer": "smirk"}
NARR = (lambda img, V, t, shots, si: None if shots[si]["name"] in ("g5", "body") else FL.NARR(img, V, t, shots, si))
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
IDX = {n: i for i, n in enumerate(NAMES)}
GY = 1000                          # asfalto


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def _h(img, name, t):
    FL.head(img, t, IDX[name])


def _track(img, off=0.0, y=GY):
    d = K.D(img)
    d.rectangle([0, y, W, y + 60], fill=(70, 70, 76))
    for k in range(-1, 12):
        x = (k * 160 - off) % (W + 160) - 80
        d.rectangle([x, y + 26, x + 80, y + 34], fill=(255, 255, 255))
    for k in range(-1, 20):
        x = (k * 60 - off) % (W + 60) - 30
        d.rectangle([x, y - 12, x + 30, y], fill=RED if k % 2 else (255, 255, 255))


def _speedo(img, cx, cy, r, v, vmax=340):
    d = K.D(img)
    d.arc([cx - r, cy - r, cx + r, cy + r], 150, 390, fill=K.PALE, width=26)
    a1 = 150 + 240 * clamp(v / vmax)
    d.arc([cx - r, cy - r, cx + r, cy + r], 150, a1, fill=RED, width=26)
    txt(img, (cx, cy), f"{int(v)}", int(r * 0.55), INK)
    txt(img, (cx, cy + r * 0.45), "km/h", int(r * 0.2), SOFT)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    v = lerp(322, 74, ease(clamp((t - 0.6) / 2.0)))
    _track(img, off=t * v * 3)
    K.f1m(img, 520, GY - 40, 0.95, rot=-t * v / 20, glow=clamp((t - 0.6) / 1.0))
    _speedo(img, 540, 600, 170, v)
    FL.big(img, 880, 470, "?", 160, RED, clamp((t - 1.6) / 0.3))
    _h(img, "q", t)


def sh_curve(img, t, T, L):
    d = K.D(img)
    q = ease(clamp(t / 2.2))
    _track(img, off=t * 900 * (1 - 0.7 * q))
    K.f1m(img, lerp(-200, 460, q), GY - 40, 0.8, rot=-t * 14)
    # cartel de la curva
    d.rectangle([880, 560, 900, GY - 12], fill=INK)
    d.rounded_rectangle([800, 470, 980, 600], radius=16, fill=(255, 255, 255), outline=INK, width=8)
    d.line([(840, 570), (890, 500), (940, 570)], fill=RED, width=14)
    FL.big(img, 420, 600, "322", 190, RED, clamp((t - 0.4) / 0.3) if t < lt(L, 0, 0.7) else 0)
    if t >= lt(L, 0, 0.7):
        FL.big(img, 420, 600, "74", 190, INK, clamp((t - lt(L, 0, 0.7)) / 0.25))
    _h(img, "curve", t)


def sh_time(img, t, T, L):
    d = K.D(img)
    frac = clamp(t / 2.6)
    FL.stopwatch(img, 300, 620, 150, frac * 0.4, f"{2.6 * frac:.1f} s".replace(".", ","))
    k = ease(clamp((t - lt(L, 0, 0.55)) / 1.0))
    y = 980
    d.line([(140, y), (940, y)], fill=K.PALE, width=26)
    d.line([(140, y), (140 + 800 * k, y)], fill=RED, width=26)
    for m in range(0, 121, 20):
        x = 140 + 800 * m / 120
        d.line([(x, y + 22), (x, y + 44)], fill=SOFT, width=4)
    K.f1m(img, 140 + 800 * k, y - 60, 0.3, glow=0.8)
    FL.big(img, 760, 620, "120 m", 120, INK, clamp((t - lt(L, 0, 0.55)) / 0.3))
    _h(img, "time", t)


def _ojo(img, cx, cy, sc, pose="surprise", ang=0.0, sy=1.0):
    import ojo as OJ
    from PIL import Image
    f = OJ.figure(pose, OJO_TRAJE, 0.0, (0.05, 0.0), 0.0)
    ff = f.resize((max(1, int(f.width * sc)), max(1, int(f.height * sc * sy))), Image.BILINEAR)
    if abs(ang) > 0.01:
        ff = ff.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    img.paste(ff, (int(cx - ff.width / 2), int(cy - ff.height / 2)), ff)


def sh_g5(img, t, T, L):
    """Ojo sentado en el F1: al frenar sale disparado hacia delante y el cinturón lo sujeta."""
    d = K.D(img)
    k = ease(clamp((t - 0.3) / 0.35))
    sh = 12 * math.sin(t * 45) * (1 - clamp((t - 0.3) / 1.5)) if t > 0.3 else 0
    d.rounded_rectangle([170 + sh, 520, 330 + sh, 1060], radius=40, fill=(60, 60, 68))            # respaldo
    d.rectangle([170 + sh, 980, 640 + sh, 1060], fill=(60, 60, 68))                               # asiento
    _ojo(img, 400 + 120 * k + sh, 780, 0.95, "surprise", ang=-0.55 * k)
    d.line([(230 + sh, 780), (480 + 120 * k + sh, 980)], fill=RED, width=22)                        # cinturón
    for n in range(4):
        y = 600 + n * 90
        d.line([(700, y), (700 + 260 * k, y)], fill=SOFT, width=8)
    FL.big(img, 860, 470, "5 G", 150, RED, clamp((t - 0.2) / 0.3))
    _h(img, "g5", t)


def sh_body(img, t, T, L):
    """Ojo en la báscula: de 80 a 400 kilos mientras frena."""
    d = K.D(img)
    k = clamp((t - lt(L, 0, 0.5)) / 0.6)
    sq = 1 - 0.18 * ease(k)
    d.rounded_rectangle([300, 1040, 780, 1110], radius=20, fill=(236, 236, 240), outline=INK, width=6)
    d.rounded_rectangle([420, 1052, 660, 1098], radius=10, fill=(28, 34, 40))
    val = int(lerp(80, 400, ease(k)))
    txt(img, (540, 1075), f"{val} kg", 36, (120, 255, 160) if val < 300 else (255, 110, 90))
    _ojo(img, 540, 1040 - 300 * sq * 0.95, 0.95, "surprise" if k > 0.3 else "point", sy=sq)
    if k > 0.2:
        for n in range(3):
            x = 300 + n * 240
            d.line([(x, 470), (x, 560)], fill=RED, width=12)
            d.polygon([(x - 26, 560), (x + 26, 560), (x, 600)], fill=RED)
    _h(img, "body", t)


def sh_air(img, t, T, L):
    d = K.D(img)
    _track(img, off=t * 600)
    K.f1m(img, 540, GY - 40, 0.95, rot=-t * 25)
    for k in range(6):
        y = 520 + k * 60
        x = (t * 900 + k * 230) % (W + 300) - 150
        d.line([(W - x, y), (W - x - 160, y)], fill=(150, 190, 230), width=8)
    _h(img, "air", t)


def sh_grip(img, t, T, L):
    d = K.D(img)
    _track(img, off=t * 700)
    K.f1m(img, 540, GY - 40, 0.95, rot=-t * 25)
    k = ease(clamp((t - 0.5) / 1.0))
    for x in (160, 540, 900):
        L_ = 80 + 120 * k
        d.line([(x, 560), (x, 560 + L_)], fill=RED, width=16)
        d.polygon([(x - 30, 560 + L_), (x + 30, 560 + L_), (x, 560 + L_ + 44)], fill=RED)
    FL.pill(img, 640, 1250, "MÁS VELOCIDAD = MÁS AGARRE", clamp((t - lt(L, 0, 0.55)) / 0.3))
    _h(img, "grip", t)


def sh_carbon(img, t, T, L):
    K.disc(img, 540, 760, 260 * pop(clamp(t / 0.4)) + 1, heat=0.0)
    FL.pill(img, 640, 1250, "DISCO DE CARBONO", clamp((t - 0.6) / 0.3))
    _h(img, "carbon", t)


def sh_hot(img, t, T, L):
    h = ease(clamp(t / 2.2))
    K.disc(img, 540, 760, 260, heat=h)
    FL.big(img, 620, 1180, f"{int(1000 * h)} °C".replace("1000", "1.000"), 120, RED, 1.0 if t > 0.1 else 0)
    _h(img, "hot", t)


def sh_better(img, t, T, L):
    k1 = clamp((t - 0.2) / 0.4)
    K.disc(img, 300, 700, 170, heat=0.6, warp=ease(clamp((t - 0.4) / 1.2)))
    txt(img, (300, 940), "Normal", 50, INK)
    FL.big(img, 300, 1040, "✗", 90, RED, k1, fo=F(FL.DJ, 90))
    k2 = clamp((t - lt(L, 0, 0.5)) / 0.4)
    K.disc(img, 780, 700, 170, heat=0.95)
    txt(img, (780, 940), "Carbono", 50, INK)
    if k2 > 0:
        FL.big(img, 780, 1040, "✓", 90, (40, 170, 90), k2, fo=F(FL.DJ, 90))
    _h(img, "better", t)


def sh_pedal(img, t, T, L):
    d = K.D(img)
    # pierna empujando el pedal
    p = ease(clamp((t - 0.4) / 0.5))
    hip, knee = (300, 640), (520, 560 + 30 * p)
    foot = (lerp(700, 760, p), 820)
    d.line([hip, knee], fill=INK, width=40)
    d.line([knee, foot], fill=INK, width=34)
    d.rounded_rectangle([foot[0] - 10, foot[1] - 60, foot[0] + 70, foot[1] + 10], radius=14, fill=INK)
    d.line([(foot[0] + 70, 860), (900, 980)], fill=SOFT, width=14)
    d.rectangle([foot[0] + 60, 700, foot[0] + 90, 900], fill=RED)
    FL.big(img, 640, 1130, "168 kg", 130, RED, clamp((t - lt(L, 0, 0.5)) / 0.3))
    _h(img, "pedal", t)


def sh_tons(img, t, T, L):
    n = min(9, int(clamp(t / 2.0) * 9) + 1)
    for i in range(n):
        x = 380 + (i % 3) * 170
        y = 1060 - (i // 3) * 170
        K.weight(img, x, y, 150, "6 t")
    FL.big(img, 540, 520, "54 t", 160, RED, clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "tons", t)


def sh_answer(img, t, T, L):
    items = [("Aire que lo aplasta", 0.35), ("Frenos al rojo vivo", 0.55), ("Una pierna de acero", 0.8)]
    for k, (s, fr) in enumerate(items):
        kk = clamp((t - lt(L, 0, fr)) / 0.3)
        if kk > 0:
            y = 560 + k * 170
            FL.big(img, 200, y, "✓", 90, RED, kk, fo=F(FL.DJ, 90))
            txt(img, (290, y), s, 62, INK, "lm")
    _h(img, "answer", t)


FNS = {n: globals()["sh_" + n] for n in NAMES}
FOCUS_PT = {n: (540, 800) for n in NAMES}

MUSIC_GAIN = 1.7          # música épica más presente (Iker, 21/10)
MUSIC_DUCK = 0.45
AUDIO = {
    "music": [("q", "epic")],
    "gains": {},
    "amb": {"road": ["q", "curve", "air", "grip"]},
    "sfx": [("q+0.6", "whoosh", 0.08), ("curve+0.3", "whoosh", 0.08), ("time+0.3", "tick", 0.06), ("g5+0.2", "boom", 0.3),
            ("body+0.6", "pop", 0.06), ("air+0.2", "whoosh", 0.07), ("grip+0.5", "swell", 0.06), ("carbon+0.3", "click", 0.1),
            ("hot+0.5", "swell", 0.08), ("better+0.4", "pop", 0.06), ("pedal+0.4", "impact", 0.25), ("tons+0.6", "pop", 0.06),
            ("answer+0.4", "ding", 0.06)],
    "bpm": 122,
}
