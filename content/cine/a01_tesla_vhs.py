"""A1 Tesla Roadster · estilo 8 «VHS años 80» (Iker lo eligió el 21/10 de la hoja de 12 estilos).
Mismo guion, voz y planos que a01_tesla; el coche en pantalla es un Cybertruck. Encima de todo va el efecto de cinta:
colores separados, líneas de barrido, ruido, alguna línea de tracking y el rótulo PLAY / contador / fecha."""
import numpy as np
from PIL import Image, ImageDraw
from a01_tesla import *          # noqa: F401,F403
import flat3 as FL
import vid2, cine
FL.use("vhs", HEAD)
import a01_flat_scenes as SC

TITLE = "Tesla_estilo8_VHS"
FPS = 30
BG = (30, 26, 34)
FNS, FOCUS_PT, CAPTION, OUTRO_FN = SC.FNS, SC.FOCUS_PT, SC.CAPTION, SC.OUTRO_FN
TRANS_POOL = ["glitch", "zoom_in", "whip", "glitch", "push", "whip_r"]
TRANS_SEED = 8
CAM_PUSH = 0.04
SHAKE = 10
CUT_SFX = True
AUDIO = dict(AUDIO)
AUDIO["music"] = [("open", "noir"), ("accel", "space"), ("delays", "noir"), ("final", "space")]
AUDIO["gains"] = {"noir": 1.0, "space": 0.9}

_NZ = [np.random.default_rng(i).normal(0, 11, (960, 540, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(5)]
_SCAN = np.ones((1920, 1, 1), np.float32)
_SCAN[::4] = 0.78
_SCAN[1::4] = 0.9


def FRAME(V, shots, chunks, total, i):
    img = vid2.frame(V, shots, chunks, total, i)
    t = i / cine.FPS
    a = np.asarray(img.resize((810, 1440), Image.BILINEAR).resize((1080, 1920), Image.BILINEAR)).astype(np.float32)
    out = a.copy()
    out[..., 0] = np.roll(a[..., 0], 6, 1)
    out[..., 2] = np.roll(a[..., 2], -6, 1)
    out = out * 0.96 + 8
    out += _NZ[int(t * 30) % 5]
    out *= _SCAN
    fr = int(t * 30)
    if fr % 97 < 6:                                    # línea de «tracking» que baja de vez en cuando
        y0 = int(1920 * ((fr % 97) / 6.0))
        out[y0:y0 + 40] = np.roll(out[y0:y0 + 40], 28, 1) * 1.15
    img = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    fo = FL.F("vt323.ttf", 64)
    d.text((60, 52), "PLAY", font=fo, fill=(240, 240, 240))
    d.polygon([(200, 66), (200, 104), (232, 85)], fill=(240, 240, 240))
    s = int(t)
    d.text((1020, 52), f"SP 0:{s // 60:02d}:{s % 60:02d}", font=fo, fill=(240, 240, 240), anchor="ra")
    d.text((60, 1810), "OCT. 15 2026", font=fo, fill=(255, 190, 90))
    return img
