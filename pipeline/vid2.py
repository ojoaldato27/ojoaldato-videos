"""Motor de los vídeos en los estilos nuevos (21/10, Iker): «oscuro minimalista» y «monigotes Paint», con una transición
DISTINTA en cada corte (trans.py: zoom que se mete en un punto y sale en el plano siguiente, barridos, iris, giros, glitch,
empujes, rotulador, hoja de papel…). Usa la línea de tiempo de la voz (cine.timeline con STYLE='docu') y su mezcla de audio.

El módulo de vídeo aporta: FNS {plano: fn(img, t, T, L)}, BG, TRANS_POOL, TRANS_SEED, FOCUS_PT {plano: (x, y)},
CAM_PUSH, SHAKE, CAPTION(img, t, chunks_con_tiempos, y), OUTRO_FN(img, u, D) → imagen, NOTIF/NOTIF_TEXT y CAP_Y opcional."""
import math
from PIL import Image
import cine
import trans
import pop
from render import W, H, ease, clamp

TD = 0.5          # duración de cada transición (centrada en el corte)
_PLAN = {}


def _render(V, shots, k, t):
    s = shots[k]
    img = Image.new("RGB", (W, H), V.BG)
    lt = max(0.0, t - s["start"])
    V.FNS[s["name"]](img, lt, s["end"] - s["start"], s["lines"])
    # cámara: empuje lento + sacudida en las palabras clave
    q = ease(clamp(lt / max(1.0, s["end"] - s["start"])))
    z = 1.0 + getattr(V, "CAM_PUSH", 0.05) * q
    fx, fy = V.FOCUS_PT.get(s["name"], (540, 960))
    dx = dy = 0.0
    amp0 = getattr(V, "SHAKE", 0)
    if amp0:
        for h in cine.docu_beats(V)[1]:
            v = t - h
            if 0 <= v < 0.2:
                a = amp0 * (1 - v / 0.2)
                dx += a * math.sin(v * 90)
                dy += a * math.cos(v * 70)
                z *= 1 + 0.04 * math.sin(math.pi * v / 0.2)
    if abs(z - 1) > 1e-3 or dx or dy:
        cw, ch = W / z, H / z
        x0 = min(max(0, fx - fx / z + dx), W - cw)
        y0 = min(max(0, fy - fy / z + dy), H - ch)
        img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
    return img


def frame(V, shots, chunks, total, i):
    t = i / cine.FPS
    o0 = total - cine.end_hold(V)
    key_ = (V.TITLE, len(shots))
    if key_ not in _PLAN:
        tp = getattr(V, "TRANS_PLAN", None)              # lista fija de transiciones por corte (21/10: más variedad)
        _PLAN[key_] = list(tp)[: len(shots) - 1] if tp and len(tp) >= len(shots) - 1 else trans.plan(len(shots) - 1, V.TRANS_POOL, getattr(V, "TRANS_SEED", 3))
    plan = _PLAN[key_]
    si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
    img = None
    for k in range(1, len(shots)):
        cut = shots[k]["start"]
        td = getattr(V, "TD", TD)                       # duración de la transición por módulo (29/10: suaves, más largas)
        if cut - td / 2 <= t < cut + td / 2 and t < o0:
            u = (t - (cut - td / 2)) / td
            A = _render(V, shots, k - 1, min(t, cut - 1e-3))
            B = _render(V, shots, k, max(t, cut))
            img = trans.apply(plan[k - 1], A, B, u, V.FOCUS_PT.get(shots[k - 1]["name"], (540, 960)))
            break
    if img is None:
        img = _render(V, shots, si, t)
    if t >= o0:
        img = V.OUTRO_FN(img, t - o0, cine.end_hold(V))
    by = {x["name"]: x for x in shots}
    if getattr(V, "NARR", None) and t < o0:                  # Ojo de narrador todo el vídeo (21/10)
        V.NARR(img, V, t, shots, si)
    if getattr(V, "NOTIF", None) and t < o0:
        img = cine.V2.notif_banner(img, t - (cine.at(V.NOTIF[0], by) + V.NOTIF[1]), getattr(V, "HANDLE", "@ojoaldato.ya"),
                                   V.NOTIF_TEXT, icon=getattr(V, "NOTIF_ICON", None))
    if t < o0 + 0.15:
        y = getattr(V, "CAP_Y", {}).get(shots[si]["name"], 1490)
        V.CAPTION(img, t, pop.chunks_t(cine.CAPS_[0]), y)
    return img
