"""20 · Dedos — prueba «OJO PRESENTADOR» (Iker 06/11: «el ojo está muy tieso, debería hablar mucho a cámara»).
Ojo grande que habla a cámara: boca sincronizada con la voz, cejas, parpadeo, gestos y balanceo. A su lado, una
tarjeta con la imagen exacta de cada frase. Voz: c20_dedos3d.mp3 (las 4 primeras frases, sin gastar créditos)."""
import os
import math
import subprocess
import numpy as np
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED
from PIL import Image, ImageDraw, ImageFilter
import pro
from pro import hook_text, lt, WHITE, solid, glow
import ojo as OJ
import c20_dedos as D

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "20_Dedos_presentador"
VOICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c20_dedos3d.mp3")
LINES = [
    "Tus dedos no se arrugan por culpa del agua. ¡Es tu *cerebro* el que lo hace a propósito!",
    "Pasas diez minutos en la *bañera* y tus dedos acaban como *pasas*.",
    "Siempre nos han dicho que la piel se *empapa* como una *esponja*.",
    "Pero hace casi *cien años* unos médicos descubrieron algo rarísimo.",
]
OUTRO_LINE = None
NAMES = ["q", "banera", "esponja", "medicos"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS, HYPE, FOLLOW, NARRATOR, PUSH = {}, None, None, {}, {}
NOTIF = None
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
FL.use("minimal", HEAD)
FRAME = vid2.frame
FPS = 30
BG = (40, 46, 80)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "suave", "suave"]
TRANS_SEED = 20
TD = 0.35
CAM_PUSH = 0.0
SHAKE = 0
CUT_SFX = False
FL.TH["narr"] = True
TRAJE = "c_biologo"
OUTRO_FN = FL.make_outro(TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"

# ------------------------------------------------------------------ boca sincronizada con la voz
_ENV = []


def envelope():
    if not _ENV:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", VOICE, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
        a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        hop = 16000 // 30
        rms = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a) - hop, hop)])
        rms = rms / (np.percentile(rms, 95) + 1e-6)
        sm = np.convolve(rms, [0.25, 0.5, 0.25], "same")
        _ENV.extend(np.clip(sm, 0, 1).tolist())
    return _ENV


def talk_at(t):
    e = envelope()
    i = int(t * 30) - int(cine_lead() * 30)
    if 0 <= i < len(e):
        v = e[i]
        return 0.0 if v < 0.12 else min(1.0, v * 1.2)
    return 0.0


def cine_lead():
    import cine
    return cine.VOICE_LEAD


_MOUTH = {}


def ojo_talk(img, cx, feet, sc, pose, t, look=(0.0, 0.0), brow=0.0, tilt=0.0):
    """Ojo grande hablando: boca (abre según la voz), cejas, parpadeo, balanceo."""
    tk = talk_at(t)
    blink = 1.0 if (t % 3.1) < 0.11 else 0.0
    f = OJ.figure(pose, TRAJE, blink, (round(look[0], 2), round(look[1], 2)), 0.0).copy()
    d = ImageDraw.Draw(f)
    mx, my = 250, 238
    if tk < 0.08:                                            # boca cerrada: sonrisa
        d.arc([mx - 30, my - 18, mx + 30, my + 10], 20, 160, fill=INK, width=7)
    else:
        h = 8 + 34 * tk
        w = 30 + 12 * tk
        d.ellipse([mx - w, my - h / 2, mx + w, my + h / 2], fill=(50, 14, 22), outline=INK, width=6)
        d.chord([mx - w * 0.6, my, mx + w * 0.6, my + h / 2 - 3], 0, 180, fill=(236, 110, 120))
    by = 92 - 16 * brow                                      # cejas
    for sx in (-1, 1):
        x0 = 250 + sx * 40
        d.line([(x0 - 34, by + 6 - sx * 4 * brow), (x0 + 34, by - 2 + sx * 4 * brow)], fill=INK, width=12)
    bob = -2.5 * tk + 1.5 * math.sin(t * 1.6)
    s = sc
    ff = f.resize((int(f.width * s), int(f.height * s)), Image.BICUBIC)
    ang = tilt * 0.4 + 0.8 * math.sin(t * 0.9)
    ff = ff.rotate(ang, expand=True, resample=Image.BICUBIC)
    x = int(cx - ff.width / 2)
    y = int(feet - ff.height * 0.93 + bob)
    K.D(img).ellipse([cx - 150 * sc, feet - 18 * sc, cx + 150 * sc, feet + 18 * sc], fill=(30, 20, 20, 70))
    img.paste(ff, (x, y), ff)


# ------------------------------------------------------------------ tarjeta con la imagen exacta de cada frase
CX0, CY0, CX1, CY1 = 500, 470, 1050, 1150


def card(img, k, draw, t, tint=(255, 255, 255)):
    if k <= 0:
        return
    s = pop(k)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw(lay)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle([CX0, CY0, CX1, CY1], radius=40, fill=255)
    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", (W, H), 0), m))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(base)
    db.rounded_rectangle([CX0 + 12, CY0 + 18, CX1 + 12, CY1 + 18], radius=40, fill=(0, 0, 0, 70))
    db.rounded_rectangle([CX0, CY0, CX1, CY1], radius=40, fill=tint + (255,))
    base.alpha_composite(lay)
    ImageDraw.Draw(base).rounded_rectangle([CX0, CY0, CX1, CY1], radius=40, outline=INK + (255,), width=8)
    cx, cy = (CX0 + CX1) / 2, (CY0 + CY1) / 2
    ang = 0.5 * math.sin(t * 0.8)
    if s != 1 or ang:
        bb = base.crop((CX0 - 40, CY0 - 40, CX1 + 60, CY1 + 60))
        bb = bb.resize((max(1, int(bb.width * s)), max(1, int(bb.height * s))), Image.BICUBIC).rotate(ang, expand=True, resample=Image.BICUBIC)
        img.paste(bb, (int(cx - bb.width / 2 + 10), int(cy - bb.height / 2 + 10)), bb)
    else:
        img.paste(base, (0, 0), base)


def sh_q(img, t, T, L):
    def pic(Lr):
        d = K.D(Lr)
        d.rectangle([CX0, CY0, CX1, CY1], fill=(214, 236, 244))
        wr = 0.2 + 0.8 * ease(clamp((t - 2.6) / 1.4))
        D.hand(Lr, 760, 800 + 40 * (1 - ease(clamp(t / 0.8))), 0.66, wr, t)
        D.water(Lr, 1040, t, CX0, CX1, 200)
        bk = pop(clamp((t - lt(L, 0, 0.55)) / 0.35))
        if bk > 0:
            D.brain(Lr, 950, 590, 0.4 * bk)
    card(img, clamp(t / 0.35), pic, t)
    if t > lt(L, 0, 0.6):
        D.signal(img, (900, 640), (745, 610), t)
    ojo_talk(img, 270, 1790, 1.5, "surprise" if t < 1.0 else ("point" if t > lt(L, 0, 0.5) else "think"), t, look=(0.08, 0.0) if t > 2.5 else (0, 0), brow=1.0 if t < 1.2 else 0.3)
    hook_text(img, [("NO ES EL AGUA", False), ("ES TU CEREBRO", True)], 1.0 if t < T - 0.4 else clamp((T - t) / 0.4), y=300, size=96)


def sh_banera(img, t, T, L):
    m = 10 * ease(clamp(t / max(1.0, lt(L, 0, 0.55))))

    def pic(Lr):
        d = K.D(Lr)
        d.rectangle([CX0, CY0, CX1, CY1], fill=(255, 248, 232))
        wr = clamp(m / 10)
        col = tuple(int(lerp(a, b, wr * 0.5)) for a, b in zip(D.SKIN, (236, 176, 160)))
        D.capsule(d, (680, 1250), (680, 700), 115, col, INK, 8)
        for j in range(8):
            y = 680 + j * 36
            d.line([(580 + q * 25, y + 12 * wr * math.sin(q * 1.6 + j)) for q in range(9)], fill=D.WRK + (int(250 * wr),), width=7)
        k = clamp((t - lt(L, 0, 0.62)) / 0.3)
        if k > 0:
            D.raisin(Lr, 940, 860, 0.9 * pop(k))
            FL.big(Lr, 830, 860, "=", 110, INK, k)
    card(img, clamp(t / 0.3), pic, t)
    D.clock(img, 960, 390, m, clamp(t / 0.3))
    ojo_talk(img, 270, 1790, 1.5, "smirk" if t > lt(L, 0, 0.62) else "point", t, look=(0.1, -0.03), brow=0.6 if t > lt(L, 0, 0.62) else 0.0)


def sh_esponja(img, t, T, L):
    def pic(Lr):
        d = K.D(Lr)
        d.rectangle([CX0, CY0, CX1, CY1], fill=(222, 240, 252))
        sw = ease(clamp(t / 2.2))
        D.capsule(d, (775, 1250), (775, 720), 125 + 18 * sw, D.SKIN, INK, 8)
        for j in range(6):                                  # gotas que entran en el dedo
            u = ((t * 0.9 + j / 6) % 1)
            x = 620 + (j % 3) * 155
            y = lerp(500, 820, u)
            d.polygon([(x, y - 26), (x + 15, y), (x, y + 14), (x - 15, y)], fill=(90, 170, 230, int(255 * (1 - u * 0.7))), outline=(30, 90, 150))
        q = clamp((t - lt(L, 0, 0.9)) / 0.3)
        if q > 0:
            FL.stamp(Lr, 775, 1060, "¿DE VERDAD?", q, col=RED)
    card(img, clamp(t / 0.3), pic, t)
    ojo_talk(img, 270, 1790, 1.5, "think", t, look=(0.1, 0.0), brow=0.0 if t < lt(L, 0, 0.7) else 1.0, tilt=-4)


def sh_medicos(img, t, T, L):
    def pic(Lr):
        d = K.D(Lr)
        d.rectangle([CX0, CY0, CX1, CY1], fill=(222, 200, 160))
        D.doctor(Lr, 700, 780, 0.72, t)
        D.hand(Lr, 930, 860, 0.38, 0.0, t)
        D.basin(Lr, 930, 1060, 220)
        for i in range(14):
            x = CX0 + (i * 97 + int(t * 600) * 7) % (CX1 - CX0); y = CY0 + (i * 191 + int(t * 600) * 13) % (CY1 - CY0)
            d.line([(x, y), (x + 2, y + 16)], fill=(80, 60, 40, 110), width=2)
    card(img, clamp(t / 0.3), pic, t, tint=(222, 200, 160))
    if t < 1.2:
        FL.stamp(img, 540, 330, "PERO OJO", clamp(t / 0.3) * clamp((1.2 - t) / 0.25), col=RED)
    k = clamp((t - 1.2) / 1.0)
    if k > 0:
        FL.big(img, 540, 330, str(int(lerp(2026, 1930, ease(k)))) if k < 1 else "AÑOS 30", 120, D.GOLD, clamp(k * 3))
    ojo_talk(img, 270, 1790, 1.5, "surprise" if t < 1.0 else "point", t, look=(0.1, -0.02), brow=1.0 if t < 1.2 else 0.4)


D.CAP_POS.update({"q": 1820, "banera": 1820, "esponja": 1820, "medicos": 1820})
D.EMOJI.update({"q": ["🧠"], "banera": ["🛁", "🍇"], "esponja": ["💧", "🧽"], "medicos": ["⏳"]})
CAPTION = D.CAPTION
NO_EMOJI = set(NAMES)
NARR = None
D.SCENE_BG.clear()
D.SCENE_BG.update({"q": D.bano, "banera": D.bano, "esponja": D.bano, "medicos": D.hospital})
pro.setup(globals(), TRAJE, D.bano().resize((W, H)), NAMES)


def _wrap(fn, name):
    def run(img, t, T, L):
        T_ = pro.NOW[0]
        D._bg(img, name, T_)
        D._air(img, name, T_)
        fn(img, t, T, L)
        pro._stimuli(img, name, globals())
    return run


FNS = {n: _wrap(globals()["sh_" + n], n) for n in NAMES}
_base = FRAME


def FRAME(V, shots, chunks, total, i):
    if not D._SHOT_AT:
        for s in shots:
            D._SHOT_AT[s["name"]] = (s["start"], s["end"])
    return _base(V, shots, chunks, total, i)


MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {"music": [("q", "playful")], "gains": {}, "amb": {},
         "sfx": [(0.05, "pop", 0.05), ("banera+0.2", "pop", 0.05), ("esponja+0.2", "pop", 0.04), ("medicos+0.05", "pop", 0.07)], "bpm": 104}
