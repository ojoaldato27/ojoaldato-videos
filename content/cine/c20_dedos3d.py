"""20 · Dedos arrugados en 3D — MUESTRA de 15 s (Iker 06/11: «el vídeo 2D, pero en 3D»).
El dibujo es un vídeo 3D de Blender (content/f3d/blender_dedos3d.py) que se pone de fondo; encima van los textos del
vídeo 2D: gancho, subtítulos en caja con emojis, reloj, sellos, banner y voz Umbriel. Variante: BG3D=<carpeta de fotogramas a 30 fps>."""
import os
import math
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED
from PIL import Image
import pro
from pro import hook_text, lt, WHITE
import c20_dedos as D

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "20_Dedos_3D_" + os.path.basename(os.environ.get("BG3D", "x"))
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
NOTIF = ("esponja", 0.6)
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
OJO_TRAJE = "c_biologo"
OJO_POSES = {}
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
GOLD, GREEN = D.GOLD, D.GREEN
BGDIR = os.environ.get("BG3D", "")
_BGC = {}


def bg3d(img):
    i = int(round(pro.NOW[0] * 30))
    for j in (i, i - 1, i - 2):
        p = os.path.join(BGDIR, f"{j + 1:05d}.jpg")
        if os.path.exists(p):
            if p not in _BGC:
                _BGC.clear(); _BGC[p] = Image.open(p).convert("RGB")
            img.paste(_BGC[p], (0, 0)); return


def sh_q(img, t, T, L):
    bg3d(img)
    hook_text(img, [("NO ES EL AGUA", False), ("ES TU CEREBRO", True)], 1.0 if t < T - 0.6 else clamp((T - t) / 0.6), y=330, size=100)


def sh_banera(img, t, T, L):
    bg3d(img)
    m = 10 * ease(clamp(t / max(1.0, lt(L, 0, 0.55))))
    D.clock(img, 860, 560, m, clamp(t / 0.3))
    k = clamp((t - lt(L, 0, 0.62)) / 0.3)
    if k > 0:
        FL.pill(img, 540, 1260, "COMO UNA PASA", k, col=(110, 60, 70))


def sh_esponja(img, t, T, L):
    bg3d(img)
    FL.pill(img, 540, 1240, "LA PIEL «CHUPA» AGUA", clamp((t - lt(L, 0, 0.5)) / 0.3), col=(60, 140, 210))
    q = clamp((t - lt(L, 0, 0.92)) / 0.3)
    if q > 0:
        FL.big(img, 880, 520 + 10 * math.sin(t * 4), "?", int(220 * pop(q)) + 1, RED, q)


def sh_medicos(img, t, T, L):
    bg3d(img)
    if t < 1.3:
        FL.stamp(img, 540, 380, "PERO OJO", clamp(t / 0.3) * clamp((1.3 - t) / 0.25), col=RED)
    k = clamp((t - 1.3) / 1.0)
    if k > 0:
        yr = int(lerp(2026, 1930, ease(k)))
        FL.big(img, 540, 380, str(yr) if k < 1 else "AÑOS 30", 130, GOLD, clamp(k * 3))


D.CAP_POS.update({"q": 1760, "banera": 300, "esponja": 1500, "medicos": 1760})
D.EMOJI.update({"q": ["🧠"], "banera": ["🛁", "🍇"], "esponja": ["💧", "🧽"], "medicos": ["⏳"]})
CAPTION = D.CAPTION
NO_EMOJI = set(NAMES)
NARR = None
pro.setup(globals(), OJO_TRAJE, Image.new("RGB", (W, H), (200, 220, 230)), NAMES)


def _wrap(fn, name):
    def run(img, t, T, L):
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


END_HOLD = 0.4
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {"music": [("q", "playful")], "gains": {}, "amb": {},
         "sfx": [(0.05, "pop", 0.05), ("q+2.3", "ding", 0.04), ("banera+0.3", "pop", 0.05), ("esponja+0.4", "pop", 0.04), ("medicos+0.05", "pop", 0.07)], "bpm": 104}
