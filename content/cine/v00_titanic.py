"""V00 · La llave que pudo salvar el Titanic — los planos ilustrados de titanic_pro, montados con el motor nuevo
(pregunta con hype, palabras clave, emojis y sonido suave)."""
from objs import *
import titanic_pro as TP

TP.TOP = TOP  # que los rótulos de los planos caigan en la capa fija del motor

TITLE = "La_llave_que_pudo_salvar_el_Titanic"
LINES = TP.LINES
SHOTS = TP.SHOTS
FOCUS = {}
NOTIF = ("gangway", 1.0)
HYPE = {"line": 1, "text": ["¿QUÉ ABRÍA?", "¿POR QUÉ NO ESTABA EN EL BARCO?"], "delay": [0, 0.9]}
STICKER_EXTRA = [('llave', '🔑'), ('abria', '🔓'), ('barco', '🚢'), ('zarpa', '🚢'), ('viaje', '🧳'), ('insumergible', '🛟'), ('oficial', '⚓'), ('sustituido', '🔄'), ('bolsillo', '👖'), ('=luna', '🌑'), ('vigias', '👀'), ('iceberg', '🧊'), ('sombra', '👀'), ('campana', '🔔'), ('hunde', '🌊'), ('personas', '🕯️'), ('prismaticos', '🔭'), ('tiempo', '⏱️'), ('dudan', '🤔'), ('subasto', '🔨'), ('libras', '💷'), ('gigante', '🧊')]
NOTIF_TEXT = "Suscríbete para más historias que no sabías"
KW_STATIC = True  # los rótulos de titanic_pro no pasan por cine.spaced: se comparan con los textos del código
KW_OVERRIDE = {11: ["UNA SOMBRA EN EL AGUA"], 19: ["MUCHOS LO DUDAN"]}
FNS = {k: getattr(TP, "sh_" + k) for k, *_ in SHOTS}
AUDIO = {
    "music": [("night_open", "mystery"), ("port_wide", "doc"), ("night_wide", "drone"), ("impact", "tension"), ("sinking", "epic"),
              ("key_spot", "mystery"), ("auction", "premium")],
    "gains": {"mystery": 0.8},
    "duck": [("impact", "impact+1.6", 0.5)],
    "amb": {"sea": ["night_open", "night_wide", "nest_close", "pov_iceberg", "bell", "sinking"],
            "crowd": ["port_wide", "ship_depart", "gangway"], "room": ["key_spot", "box_open", "fleet_quote", "auction"]},
    "sfx": [("night_open@L1", "chime", 0.06), ("ship_depart+0.3", "horn", 0.3), ("gangway@L2+0.2", "paper", 0.15),
            ("nest_close+0.3", "swell", 0.1),
            ("pov_iceberg+0.5", "heart", 0.3), ("pov_iceberg+1.1", "heart", 0.3),
            ("bell+0.2", "bell", 0.35), ("bell+0.75", "bell", 0.35), ("bell+1.3", "bell", 0.35),
            ("impact+0.3", "boom", 0.5), ("impact+0.3", "impact", 0.4), ("sinking+0.5", "rumble", 0.3),
            ("key_spot+0.3", "ding", 0.1), ("box_open+0.4", "click", 0.3), ("fleet_quote+0.3", "paper", 0.12),
            ("auction+0.6", "gavel", 0.4), ("auction@L1+0.3", "swell", 0.14)],
    "bpm": 92,
}
