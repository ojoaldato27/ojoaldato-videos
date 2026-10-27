import json, os
import build_formats as B
from build_formats import build
B.WPS = 2.3
HERE = os.path.dirname(os.path.abspath(__file__))
Q1 = "Entonces, ¿qué pasaría si el Sol *desapareciera* ahora mismo?"
F1 = "El Sol que estás viendo ahora mismo… *no es el Sol de ahora*"
SEGS = [
 ("sunset", {"freeze": B.dur(F1) - 0.6}, [F1, "Y al final te cuento qué pasaría si *desapareciera de golpe*"], "La pregunta"),
 ("distance", {}, ["El Sol está a unos *150 millones de km*", "Y la luz viaja a unos *300.000 km por segundo*"], "La distancia"),
 ("laps", {}, ["En un solo segundo, podría dar *7 vueltas y media* a la Tierra"], "La velocidad"),
 ("clock", {}, ["Aun así, tarda *8 minutos y 20 segundos* en llegar", "El Sol que ves es el de hace 8 minutos: estás viendo *el pasado*"], "El retraso"),
 ("core", {}, ["Pero esto no es lo más raro", "Esa luz nació en el núcleo del Sol, a unos *15 millones de grados*",
               "Allí la materia está tan apretada que la luz choca una y otra vez, *como en un laberinto*"], "El núcleo"),
 ("escape", {}, ["Tarda *miles de años* en salir a la superficie…", "…y luego solo *8 minutos* en llegar a tus ojos"], "La salida"),
 ("vanish", {"off": B.dur(Q1)}, [Q1, "Durante 8 minutos lo seguirías viendo *brillar*",
               "Y la Tierra seguiría girando *como si nada*: la gravedad también viaja a la velocidad de la luz"], "La respuesta"),
 ("dark", {}, ["Pasados esos 8 minutos: *oscuridad*", "Y la Tierra saldría disparada *en línea recta*"], "La respuesta"),
 ("outro_nls", {}, ["La próxima vez que veas un atardecer… recuerda que estás viendo *el pasado*"]),
]
sid = "S1_sol"
build(sid, SEGS, "El Sol que ves no es el de ahora ☀️", "La luz del Sol tarda 8 min 20 s en llegar… y miles de años en salir de su núcleo. ¿Y si desapareciera?", "premium")
p = os.path.join(HERE, "scripts", f"{sid}.json"); s = json.load(open(p))
s.update(chunk_n=3, seed=41); s["notifs"] = s["notifs"][:1]
s["metadata"]["tags"] = ["curiosidades", "espacio", "sol", "ciencia", "sabías que", "luz"]
json.dump(s, open(p, "w"), ensure_ascii=False, indent=1)
