"""A1 Tesla Roadster · estilo 12 «póster vintage» (Iker lo eligió el 21/10 de la hoja de 12 estilos).
Mismo guion, voz y planos que a01_tesla; el coche en pantalla es un Cybertruck. Paleta crema, azul marino, rojo y
mostaza, rayos de sol que giran despacio y grano de papel por encima."""
import numpy as np
from PIL import Image
from a01_tesla import *          # noqa: F401,F403
import flat3 as FL
import vid2, cine
FL.use("poster", HEAD)
import a01_flat_scenes as SC

TITLE = "Tesla_estilo12_POSTER"
FPS = 60
BG = (244, 232, 206)
FNS, FOCUS_PT, CAPTION, OUTRO_FN = SC.FNS, SC.FOCUS_PT, SC.CAPTION, SC.OUTRO_FN
TRANS_POOL = ["iris", "zoom_in", "push", "whip", "spin", "whip_r"]
TRANS_SEED = 12
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
AUDIO = dict(AUDIO)
AUDIO["music"] = [("open", "playful"), ("brabham", "warm"), ("accel", "playful"), ("delays", "warm"), ("final", "playful")]
AUDIO["gains"] = {"playful": 1.0, "warm": 1.0}

_G = [np.random.default_rng(i).normal(0, 9, (960, 540, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1) for i in range(4)]
_ys, _xs = np.mgrid[0:1920, 0:1080].astype(np.float32)
_VIG = (1 - 0.18 * (((_xs - 540) / 540) ** 2 + ((_ys - 960) / 960) ** 2) ** 1.5)[..., None].clip(0.75, 1)


def FRAME(V, shots, chunks, total, i):
    img = vid2.frame(V, shots, chunks, total, i)
    t = i / cine.FPS
    a = np.asarray(img).astype(np.float32) * _VIG + _G[int(t * 12) % 4]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
