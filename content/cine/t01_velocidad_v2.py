"""02 · ¿Qué cambia de ir a 100 o a 140? — con la edición «docu» aprobada (cabecera serif, subtítulos al ritmo de la voz,
notificación tipo iPhone, mascota y cierre), ritmo rápido y la voz del canal. Las escenas son las de la v2 (t01_velocidad)."""
import os
from t01_velocidad import *      # noqa: F401,F403
import t01_velocidad as BASE

STYLE = "docu"
DOCU_SKIN = True                 # escenas antiguas: se apagan sus rótulos y toman el azul noche
BEATS = True
XF = 0.28
TITLE = "Que_cambia_de_ir_a_100_o_a_140_v2"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "t01_velocidad")
VOICE = next((_VZ + e for e in (".mp3", ".m4a", ".wav") if os.path.exists(_VZ + e)), _VZ + ".mp3")
LINES = BASE.LINES
OUTRO_LINE = "Si no lo sabías… ahora ya lo sabes. Dale a like y sígueme para más."
HYPE = None
FOLLOW = None
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"
NOTIF = ("energy", 6.5)         # banner de seguir hacia la mitad (~41 s), pedido por Iker
HEAD = {
    0: ("100 o 140", "¿QUÉ CAMBIA DE VERDAD?"),
    1: ("¿Cuánto ganas?", "TE LO DIGO AL FINAL"),
    2: ("28 metros", "CADA SEGUNDO A 100 KM/H"),
    3: ("39 metros", "CADA SEGUNDO A 140 KM/H"),
    4: ("Un imprevisto", "ALGO SE CRUZA DELANTE"),
    5: ("1 segundo", "LO QUE TARDAS EN REACCIONAR"),
    6: ("El truco del RACE", "DISTANCIA DE SEGURIDAD"),
    7: ("100 metros", "A 100 KM/H"),
    8: ("196 metros", "A 140 KM/H"),
    9: ("¿El doble?", "SOLO VAS UN 40 % MÁS RÁPIDO"),
    10: ("Al cuadrado", "ASÍ CRECE LA ENERGÍA"),
    11: ("×2 de energía", "A 140 KM/H"),
    12: ("Un piso 13", "CHOCAR A 100 KM/H"),
    13: ("Un piso 26", "CHOCAR A 140 KM/H"),
    14: ("El aire", "TAMBIÉN CRECE CON EL CUADRADO"),
    15: ("+20 a 25 %", "DE CONSUMO, DE 120 A 140"),
    16: ("100 euros", "LA MULTA EN UNA AUTOVÍA DE 120"),
    17: ("¿Cuánto ganas?", "LA RESPUESTA"),
    18: ("17 minutos", "EN 100 KILÓMETROS"),
    19: ("17 minutos", "POR EL DOBLE DE FRENADA Y DE GOLPE"),
    20: ("Tú decides", "¿MERECE LA PENA?"),
}
# la mascota solo donde no tapa los dibujos de las escenas antiguas
NARRATOR = {"open": ("wave", "left"), "meters": None, "react": None, "rule": None, "energy": None, "fall": None,
            "air": None, "fine": ("smirk", "left"), "time": None, "verdict": ("think", "left")}
CAP_Y = {"time": 1655}           # el subtítulo pasa por debajo de las cajas «A 100 / A 140» del mapa
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
