"""Prueba de estilos (21/10, Iker: «hazme dos vídeos diferentes, uno de cada [oscuro minimalista y monigotes Paint], y usa el
Cybertruck en ambos»). Guion común: por qué el Cybertruck parece dibujado con regla.
Fuentes: Electrek 24/11/2019 (tuit de Musk: «you can't stamp ultra-hard 30X steel, because it breaks the stamping press…
Even bending it requires a deep score on inside of bend»); Express & Star 25/11/2019 (dos cristales «blindados» rotos con
una bola de metal en la presentación de Los Ángeles); HotHardware 27/11/2019 (250.000 reservas en pocos días, 100 $ de señal)."""
import os

STYLE = "docu"
BEATS = True
FPS = 60
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c01_cyber")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Por qué el *Cybertruck* de Tesla parece dibujado con una *regla*?",
    "Por su acero: es tan duro… que *rompería las prensas* que dan forma a los coches.",
    "Lo dijo el propio Musk: ese acero *no se puede estampar*.",
    "Y hasta para doblarlo, hay que *marcarlo* antes por dentro.",
    "Por eso todo son *planos y aristas*, como una hoja de papel doblada.",
    "Y en su presentación, en *2019*, quisieron demostrar que sus cristales blindados no se rompían…",
    "Lanzaron una bola de acero… y se *rompieron*. Dos.",
    "Aun así, en pocos días tenía *250.000 reservas*.",
]
OUTRO_LINE = "Si no lo sabías… ahora ya lo sabes. Dale a like y sígueme para más."
SHOTS = [("hook", 0, 0, 0), ("press", 1, 1, 0), ("musk", 2, 2, 0), ("score", 3, 3, 0), ("fold", 4, 4, 0),
         ("stage", 5, 5, 0), ("ball", 6, 6, 0), ("orders", 7, 7, 0)]
FOCUS = {}
HEAD = {}
NOTIF = ("fold", 1.2)            # banner de seguir hacia la mitad
FOLLOW = None
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"
CUT_SFX = True
