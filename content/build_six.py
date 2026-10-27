"""Seis versiones del vídeo del avión Madrid → Los Ángeles: cada una con su idea, guion y edición.
Datos: solo los comprobados en SOURCES (build_formats)."""
import json, os
import build_formats as B
from build_formats import build, REG, FLIGHT_FULL, DESC_COMMON
from build_examples import A as STORY

B.WPS = 2.3
HERE = os.path.dirname(os.path.abspath(__file__))
TAKEOFF = {"cam0": [-3.7, 40.4, 16], "cam1": [-11, 45, 16], "f0": 0, "f1": 0.05, "alt0": 0, "alt1": 11000,
           "spd0": 250, "spd1": 900, "temp0": 15, "temp1": -56}
ROUTE = {"cam0": [-30, 50, 7.5], "cam1": [-66, 52, 7.5], "f0": 0.16, "f1": 0.5, "straight": 0.6, "regions": REG}
LANDING = {"cam0": [-92, 46, 9], "cam1": [-118, 34.5, 9], "f0": 0.62, "f1": 1.0, "alt0": 11000, "alt1": 0,
           "spd0": 900, "spd1": 250, "temp0": -56, "temp1": 20, "regions": REG}
GLOBE = {"view_lat": 50, "view_lon0": -40, "view_lon1": -70, "note": "≈ 790 km menos"}
FULL = dict(FLIGHT_FULL, cam0=[-55, 47, 6.4], cam1=[-60, 47, 6.4])

V = {}

# 1 · VIRAL ULTRADINÁMICA — lista de 7 a ritmo alto
V["01_Viral_Ultradinamico"] = ("viral", "7 cosas que le pasan a tu avión (y no sabes) ✈️", [
    ("title", {"lines": ["7 cosas que", "le pasan a", "TU AVIÓN"], "hl": 2, "pad": 0.2},
     ["7 cosas que le pasan a *tu avión*… y no sabes", "La última te va a romper la cabeza"]),
    ("top_card", {"n": 7, "title": "Fuera, −56 °C"}, ["Número 7: ahí fuera hace *−56 °C*"], "#7 · El frío"),
    ("thermo", {}, ["Cada kilómetro que subes, pierdes unos *6,5 °C*"], "#7 · El frío"),
    ("top_card", {"n": 6, "title": "Aire al 30 %"}, ["Número 6: solo queda un *30 %* del aire"], "#6 · El aire"),
    ("density", {}, ["Menos aire, menos resistencia: *menos combustible*"], "#6 · El aire"),
    ("top_card", {"n": 5, "title": "Cabina a 2.400 m"}, ["Número 5: dentro respiras como a *2.400 metros*"],
     "#5 · La cabina"),
    ("chips", {}, ["Por eso tu bolsa de patatas *se hincha*"], "#5 · La cabina"),
    ("top_card", {"n": 4, "title": "Ventanas sin esquinas"}, ["Número 4: las ventanillas *no tienen esquinas*"],
     "#4 · Ventanillas"),
    ("window", {"phase": "square"}, ["En 1954, dos aviones Comet *se partieron* en el aire"], "#4 · Ventanillas"),
    ("window", {"phase": "round"}, ["Desde entonces: redondas, 3 capas y un *agujerito*"], "#4 · Ventanillas"),
    ("top_card", {"n": 3, "title": "No va recto"}, ["Número 3: tu avión *no va recto*"], "#3 · La ruta"),
    ("flight", FULL, ["De Madrid a Los Ángeles sube hasta *Canadá*"], "#3 · La ruta"),
    ("top_card", {"n": 2, "title": "Es más corto"}, ["Número 2: ese rodeo es *más corto*"], "#2 · La esfera"),
    ("globe_land", GLOBE, ["En una esfera, esa curva te ahorra *790 km*"], "#2 · La esfera"),
    ("top_card", {"n": 1, "title": "El mapa miente"}, ["Y número 1: el mapa te *miente*"], "#1 · El mapa"),
    ("greenland", {"morph": 4.6, "note": "≈ 14 veces más pequeña"},
     ["Groenlandia parece tan grande como *África*…", "…y es *14 veces* más pequeña"], "#1 · El mapa"),
    ("outro_nls", {}, ["¿Cuál no sabías? Mándaselo a quien *vuele pronto*"]),
])

# 2 · CINEMATOGRÁFICA DOCUMENTAL — narración pausada
V["02_Cinematografico_Documental"] = ("doc", "Madrid → Los Ángeles: lo que no ves de tu vuelo", [
    ("flight", TAKEOFF, ["Madrid. Un avión despega rumbo a *Los Ángeles*.",
                         "En pocos minutos alcanza los *11.000 metros*."], "El ascenso"),
    ("thermo", {}, ["Allí arriba, la temperatura cae hasta los *−56 °C*.",
                    "Cada kilómetro de altura, el aire pierde unos *6,5 grados*."], "El ascenso"),
    ("density", {}, ["Y se vuelve tan fino que queda menos de *un tercio* del aire del suelo."], "El ascenso"),
    ("cabin", {}, ["Dentro, la cabina se presuriza.", "Pero no como en tierra: como a unos *2.400 metros*."],
     "La cabina"),
    ("window", {"phase": "square"}, ["Las ventanillas guardan una lección.",
                                     "En 1954, dos aviones Comet se partieron en pleno vuelo.",
                                     "La fatiga del metal empezó en las *esquinas*."], "La ventanilla"),
    ("window", {"phase": "round"}, ["Desde entonces, no tienen esquinas: tienen *tres capas* y un pequeño orificio."],
     "La ventanilla"),
    ("flight", ROUTE, ["Sobre el mapa, la ruta parece un capricho: sube hacia *Canadá*."], "La ruta"),
    ("globe_land", GLOBE, ["Pero sobre la esfera de la Tierra es el camino *más corto*.",
                           "Unos 790 kilómetros menos."], "La ruta"),
    ("greenland", {"morph": 5.6, "note": "≈ 14 veces más pequeña"},
     ["El engaño está en el mapa: para aplanar el planeta, se estiran los polos.",
      "Groenlandia parece del tamaño de África.", "En realidad, África es *catorce veces* mayor."], "El mapa"),
    ("flight", LANDING, ["Tras 9.363 kilómetros, el avión desciende sobre *Los Ángeles*."], "La llegada"),
    ("outro_nls", {}, ["Si aún no lo sabías… *ahora ya lo sabes*."]),
])

# 3 · MISTERIO — una investigación con revelación final
V["03_Misterio_Suspense"] = ("mystery", "Hay algo raro en la ruta de tu avión…", [
    ("flight", FULL, ["Hay algo *raro* en la ruta de tu avión.", "De Madrid a Los Ángeles… no va recto.",
                      "Sube hacia el norte. Hacia *Canadá*.", "¿Por qué daría un *rodeo*?"], "El caso"),
    ("thermo", {}, ["Primera pista: a 11.000 metros, fuera hace *−56 °C*."], "Las pistas"),
    ("density", {}, ["Segunda: el aire es tan fino que *casi no frena* al avión."], "Las pistas"),
    ("cabin", {}, ["Tercera: dentro respiras como a *2.400 metros*… y no lo notas."], "Las pistas"),
    ("window", {"phase": "square"}, ["Hasta las ventanillas esconden algo.",
                                     "En 1954, dos aviones Comet *se partieron* en el aire."], "El secreto"),
    ("window", {"phase": "round"}, ["Desde entonces, ninguna tiene *esquinas*."], "El secreto"),
    ("globe_land", GLOBE, ["Pero la respuesta al rodeo estaba en la forma de la Tierra.",
                           "En una esfera, esa curva *es* la línea recta.", "Te ahorras unos *790 km*."],
     "La respuesta"),
    ("greenland", {"morph": 5.4, "note": "≈ 14 veces más pequeña"},
     ["El culpable es el mapa que has visto *toda tu vida*.", "Groenlandia parece tan grande como *África*…",
      "…pero es *14 veces* más pequeña."], "El culpable"),
    ("outro_nls", {}, ["Ahora mira otra vez el mapa… ¿qué más te ha *ocultado*?"]),
])

# 4 · VISUAL CREATIVA — el vuelo en 7 números
V["04_Visual_Creativo"] = ("creative", "Tu vuelo a Los Ángeles en 8 números ✈️", [
    ("title", {"lines": ["Tu vuelo", "en 8", "NÚMEROS"], "hl": 2, "pad": 0.2},
     ["Tu vuelo de Madrid a Los Ángeles, en *8 números*"]),
    ("flight", TAKEOFF, ["*11.000* metros: la altura a la que vuelas"], "Altura"),
    ("thermo", {}, ["*−56 °C*: lo que hay al otro lado de la ventanilla"], "Frío"),
    ("density", {}, ["*30 %*: el aire que queda a esa altura", "Menos aire, menos resistencia… menos combustible"],
     "Aire"),
    ("cabin", {}, ["*2.400* metros: la altura a la que respiras en la cabina"], "Cabina"),
    ("chips", {}, ["Por eso se hincha tu bolsa de patatas"], "Cabina"),
    ("window", {"phase": "round"}, ["*3* capas tiene tu ventanilla, y un agujerito"], "Ventanilla"),
    ("window", {"phase": "square"}, ["Redondas desde que los Comet de 1954 fallaron por las esquinas"], "Ventanilla"),
    ("flight", ROUTE, ["*790* kilómetros te ahorra la curva por Canadá"], "Ruta"),
    ("globe_land", GLOBE, ["Porque en una esfera, esa curva es el camino *más corto*"], "Ruta"),
    ("greenland", {"morph": 4.4, "note": "≈ 14 veces más pequeña"},
     ["*14*: las veces que Groenlandia cabe en África", "Aunque en el mapa parezcan iguales"], "Mapa"),
    ("record", {}, ["Y *4 h 56 min*: el récord de un 747 de Nueva York a Londres",
                    "El viento lo empujaba a casi 1.300 km/h"], "Récord"),
    ("outro_nls", {}, ["¿Qué número te ha sorprendido más? Mándaselo a quien *vuele pronto*"]),
])

# 5 · REDES SOCIALES PREMIUM — la historia que ya gustó, como identidad del canal
V["05_Redes_Sociales_Premium"] = ("premium", "¿Por qué tu avión a Los Ángeles pasa por Canadá? ✈️", STORY)

# 6 · EXPERIMENTAL — el ordenador de a bordo narra el vuelo
V["06_Experimental_Innovador"] = ("exp", "Informe del ordenador de a bordo: Madrid → Los Ángeles", [
    ("flight", TAKEOFF, ["Sistema de vuelo: *activado*.", "Ruta: Madrid → Los Ángeles. Altitud: *11.000 m*."],
     "Inicio"),
    ("thermo", {}, ["Temperatura exterior: *−56 °C*.", "Descenso: 6,5 °C por kilómetro."], "Sensores"),
    ("density", {}, ["Densidad del aire: *30 %*.", "Resistencia mínima. Consumo: *optimizado*."], "Sensores"),
    ("cabin", {}, ["Presión de cabina: equivalente a *2.400 m*.", "Pasajeros: sin cambios aparentes."], "Cabina"),
    ("chips", {}, ["Aviso: bolsa de patatas *hinchada*. Causa: baja presión."], "Cabina"),
    ("window", {"phase": "round"}, ["Ventanilla: 3 capas. Orificio de presión: *activo*."], "Estructura"),
    ("window", {"phase": "square"}, ["Historial, 1954: fallos por fatiga en aviones Comet.",
                                     "Solución: *esquinas redondas*."], "Estructura"),
    ("flight", ROUTE, ["Calculando ruta… Resultado: *curva hacia el norte*."], "Navegación"),
    ("globe_land", GLOBE, ["Motivo: la Tierra es una esfera. Ahorro: *790 km*."], "Navegación"),
    ("greenland", {"morph": 5.0, "note": "≈ 14 veces más pequeña"},
     ["Analizando proyección del mapa…", "Error detectado en el mapa plano.", "Groenlandia: tamaño real, *14 veces* menor que África."], "Error"),
    ("record", {}, ["Registro de 2020: un 747 de Nueva York a Londres en *4 h 56 min*.",
                    "Velocidad respecto al suelo: casi *1.300 km/h*.", "Causa: la corriente en chorro."], "Registro"),
    ("flight", LANDING, ["Distancia: 9.363 km. Aterrizaje: *completado*."], "Fin"),
    ("outro_nls", {}, ["Fin de la transmisión. ¿Sigues ahí? *Sígueme*."]),
])

DESC = {
    "01_Viral_Ultradinamico": "7 cosas que le pasan a tu avión: −56 °C fuera, aire al 30 %, cabina a 2.400 m, ventanillas sin esquinas, la ruta por Canadá y el mapa que miente.",
    "02_Cinematografico_Documental": "Un vuelo Madrid → Los Ángeles contado como un documental: el frío, el aire fino, la cabina, las ventanillas del Comet, la ruta curva y el engaño del mapa.",
    "03_Misterio_Suspense": "¿Por qué tu avión a Los Ángeles da un rodeo por Canadá? Las pistas, el secreto de las ventanillas y la respuesta.",
    "04_Visual_Creativo": "Tu vuelo de Madrid a Los Ángeles en 8 números: 11.000, −56, 30 %, 2.400, 3, 790, 14 y 4 h 56 min.",
    "05_Redes_Sociales_Premium": "¿Por qué tu avión a Los Ángeles pasa por Canadá? El vuelo por dentro y la respuesta en un globo.",
    "06_Experimental_Innovador": "El ordenador de a bordo narra tu vuelo Madrid → Los Ángeles: sensores, cabina, estructura, navegación, un error en el mapa y el récord del viento.",
}

if __name__ == "__main__":
    for sid, (style, title, segs) in V.items():
        build(sid, segs, title, DESC[sid] + DESC_COMMON, style)
        p = os.path.join(HERE, "scripts", f"{sid}.json")
        s = json.load(open(p))
        s.update(chunk_n=3, seed=sum(map(ord, sid)) % 1000)
        s["notifs"] = s["notifs"][:1]
        json.dump(s, open(p, "w"), ensure_ascii=False, indent=1)
