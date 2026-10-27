"""⚡ A1 Tesla con el estilo «pop» (pedido por Iker el 21/10: «me parecen muy sosos los vídeos, no de contenido sino de
edición… cambia el fondo, ponle mejor música, efectos, colores, todo mejóralo; coge las ideas de vídeos virales del estilo»;
«mejora mucho las imágenes como la del coche… hazlo todo más visible y que enganche… los movimientos más fluidos»).
Mismo guion, voz, escenas y formato que a01_tesla; cambia el acabado (pipeline/pop.py), los coches (pipeline/car_pro.py),
el movimiento (desenfoque de movimiento) y se renderiza a 60 fps."""
from a01_tesla import *          # noqa: F401,F403
import a01_tesla as T
import cine as _cine
import pop
import car_pro as CP

TITLE = "El_Tesla_que_salta_POP"
POP = "neon"
FPS = 60
XF = 0.0                          # cortes secos con destello (nada de fundidos)
AUDIO = dict(T.AUDIO)
AUDIO["music"] = [("open", "pop")]
AUDIO["gains"] = {}
AUDIO["amb"] = {}
AUDIO["bed"] = []

# dibujos nuevos y movimiento fluido en todas las escenas del Tesla
T.roadster = CP.roadster
T.car_sil = CP.sedan
T.paste = CP.make_smooth_paste(_cine.paste, lambda: _cine.FPS, lambda: pop.P["gt"])
pop.apply(globals())
