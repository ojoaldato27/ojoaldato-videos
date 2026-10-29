"""Vídeo 3D «Urda (Toledo)»: choque de un AVE y un Iryo, 28/10/2026. Tono informativo y triste (Iker, 29/10).
Datos contrastados el 29/10 (cifras provisionales):
- 28/10/2026 hacia las 8:54, línea AV Madrid–Andalucía entre Los Yébenes y Urda (Toledo): un AVE de Renfe alcanzó por
  detrás a un Iryo parado; descarrilaron los dos últimos coches del Iryo (Adif, 112 CLM; eldiario.es, CMM).
- Unos 540 viajeros (≈393 AVE + ≈147 Iryo, CMM; 397 + 146 según eldiario.es).
- Al menos 68 fallecidos y más de un centenar de heridos (García-Page; eldiario.es, CMM, El Progreso).
- Según el ministro de Transportes, hacia las 8:30 falló el sistema de control/señalización (LZB) del tramo y desde el
  centro de control se autorizó seguir con normalidad con el Iryo aún parado (CMM, campogibraltar24h).
- Investiga un juzgado de Orgaz (CMM). Tres días de luto oficial (BOE, Infobae). Línea cortada hasta nuevo aviso (Adif).
"""
import os

ROOT = "/home/claude/shorts-ingenieria"
PAGE = "urda"
VOZ = os.path.join(ROOT, "content/cine/voz/f3d_urda")
LINES = [
    "¿Cómo pudo un AVE chocar contra un *tren parado*… en la misma vía?",
    "Fue el 28 de octubre, en la línea de alta velocidad entre Madrid y Andalucía, cerca de *Urda*.",
    "Hacia las ocho y media falló el sistema que controla las *señales* en ese tramo, el LZB.",
    "Sin señales, los trenes se pararon. Entre ellos, un *Iryo*… y, más atrás, un *AVE* de Renfe.",
    "Según el ministro de Transportes, desde el centro de control se autorizó a los trenes a *seguir* con normalidad… con el Iryo todavía parado delante.",
    "El AVE volvió a arrancar por la *misma vía*, con el Iryo parado más adelante.",
    "A las nueve menos cinco lo *alcanzó* por detrás. Los dos últimos vagones del Iryo *descarrilaron*.",
    "En los dos trenes viajaban unas 540 personas. Al menos *68* han muerto, y más de un centenar están *heridas*.",
    "Ahora un *juzgado* de Orgaz investiga qué falló exactamente.",
    "El Gobierno ha declarado *tres días de luto* oficial, y la línea sigue *cortada*.",
    "Detrás de cada cifra hay una *familia*.",
]
OUTRO_LINE = "Todo nuestro cariño para las víctimas y para sus seres queridos."
OUTRO_HOLD = 3.5
OJO_TRAJE = "reportero"
OJO_POSES = ["think", "point", "point", "point", "point", "think", "think", "think", "point", "think", "think"]
OJO_ACT = {1: ("point", 30, 1000, 0.72), 5: ("point", 40, 1040, 0.68), 8: ("point", 640, 1020, 0.7), 9: ("think", 640, 1040, 0.7)}   # Ojo actúa, como en el F1
OJO_HIDE = {0, 6, 7, 10}        # sin Ojo en el choque, las víctimas ni las velas
OJO_HIDE_OUTRO = True
OUTRO_POSE = "think"
MUSIC, MUSIC_GAIN = "drone", 1.0
BANNER, WHOOSH, POPS = False, False, False
