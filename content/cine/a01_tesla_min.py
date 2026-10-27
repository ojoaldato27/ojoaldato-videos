"""A1 Tesla Roadster · estilo 7 «minimal blanco» (Iker lo eligió el 21/10 de la hoja de 12 estilos).
Mismo guion, voz y planos que a01_tesla; el coche en pantalla es un Cybertruck; transiciones distintas en cada corte."""
from a01_tesla import *          # noqa: F401,F403  (guion, voz, planos, titulares, banner de seguir)
import flat3 as FL
import vid2
FL.use("minimal", HEAD)
import a01_flat_scenes as SC

TITLE = "Tesla_estilo7_MINIMAL"
FRAME = vid2.frame
FPS = 60
BG = (248, 248, 246)
FNS, FOCUS_PT = SC.FNS, SC.FOCUS_PT
# formato nuevo del estilo 7 (21/10): Ojo de narrador todo el vídeo, palabras clave con marcador rojo, marca «Ojo al dato»
FL.TH["narr"] = True
OJO_TRAJE = "c_inventor"
NARR = FL.NARR
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
TRANS_POOL = ["push", "whip", "zoom_in", "iris", "whip_r", "spin"]
TRANS_SEED = 5
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
AUDIO = dict(AUDIO)
