"""Genera los guiones de los 3 formatos del vídeo de aviones. El tiempo de cada frase se calcula
para que una voz (CapCut / ElevenLabs) la lea cómoda: ~2,5 palabras por segundo."""
import json, re, os

WPS = 3.1
HERE = os.path.dirname(os.path.abspath(__file__))
REG = [["Canadá", -100, 58], ["Groenlandia", -42, 73], ["EE. UU.", -98, 40], ["Océano Atlántico", -40, 38]]


def dur(txt, mn=1.6):
    n = len(re.findall(r"\w+", txt.replace("*", "")))
    return max(mn, n / WPS + 0.3)


def build(sid, segs, title, desc, style, chapters_on=True):
    t, scenes, caps, chs = 0.0, [], [], []
    for seg in segs:
        typ, params, lines = seg[0], dict(seg[1]), seg[2]
        chap = seg[3] if len(seg) > 3 else None
        st = t
        for ln in lines:
            if isinstance(ln, tuple):
                txt, d_ = ln
            else:
                txt, d_ = ln, dur(ln)
            if txt:
                caps.append({"start": round(t, 2), "end": round(t + d_, 2), "text": txt})
            t += d_
        t += params.pop("pad", 0.0)
        params["dur"] = round(t - st, 2)
        scenes.append({"type": typ, "start": round(st, 2), "end": round(t, 2), "params": params})
        if chap:
            if chs and chs[-1]["text"] == chap:
                chs[-1]["end"] = round(t, 2)
            else:
                chs.append({"start": round(st, 2), "end": round(t, 2), "text": chap})
    mid = min((sc["start"] for sc in scenes), key=lambda x: abs(x - t * 0.45)) + 0.5
    notifs = [{"t": round(mid, 2), "title": "nolosabias_datos", "body": "Suscríbete para más datos que no sabías"},
              {"t": round(t - 4.2, 2), "title": "nolosabias_datos", "body": "Sígueme: mañana, otro dato que no sabías"}]
    s = {"id": sid, "notifs": notifs, "style": style, "caption_mode": "words", "chunk_n": 2, "bpm": 124, "duration": round(t, 2), "seed": 11, "thumb_time": 2.0,
         "watermark": "@nolosabias_datos", "burn_captions": True, "scenes": scenes, "captions": caps,
         "chapters": chs if chapters_on else [],
         "metadata": {"title": title, "description": desc,
                      "tags": ["curiosidades", "datos curiosos", "aviones", "sabías que", "ciencia", "mapas"]},
         "rights": [{"asset": "animación y mapas esquemáticos", "license": "propio"},
                    {"asset": "música y efectos (sintetizados con código)", "license": "propio"},
                    {"asset": "tipografías Inter y DejaVu", "license": "licencia comercial", "note": "OFL / libre"}],
         "sources": SOURCES}
    json.dump(s, open(os.path.join(HERE, "scripts", f"{sid}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{sid}: {s['duration']:.1f} s, {len(caps)} frases")


SOURCES = ["Ruta ortodrómica Madrid–Los Ángeles ≈ 9.363 km vs. 10.154 km en recta Mercator (cálculo propio, R = 6.371 km)",
           "Atmósfera estándar ISA: a 11.000 m, −56,5 °C y densidad 0,364 kg/m³ (1,225 a nivel del mar); gradiente 6,5 °C/km",
           "14 CFR 25.841: altitud de cabina no superior a 8.000 ft (≈ 2.400 m) en operación normal",
           "de Havilland Comet: accidentes de 1953-1954 por fatiga del metal en esquinas de ventanas; ventanas actuales de 3 capas con orificio de respiración",
           "British Airways, 8-9/02/2020: Nueva York–Londres en 4 h 56 min, ~800 mph (≈ 1.290 km/h) respecto al suelo (NPR / Flightradar24)",
           "Superficies: Groenlandia ≈ 2,17 millones de km², África ≈ 30,4 millones de km²"]

DESC_COMMON = ("\n\nFuentes: atmósfera estándar ISA; normativa FAA 14 CFR 25.841; récord de British Airways (febrero 2020, "
               "NPR/Flightradar24); cálculo propio de rutas sobre esfera.\nAnimación, mapas y música originales.\n\n"
               "#curiosidades #datoscuriosos #sabiasque #aviones #ciencia")

FLIGHT_FULL = {"cam0": [-55, 47, 6.4], "cam1": [-60, 47, 6.4], "f0": 0.0, "f1": 1.0, "hud": False,
               "straight": 0.8, "regions": REG}

# ---------------------------------------------------------------- 1. VIAJE EN DIRECTO
live = [
    ("flight", {"cam0": [-3.7, 40.4, 30], "cam1": [-11, 45, 15], "f0": 0, "f1": 0.05, "alt0": 0, "alt1": 11000,
                "spd0": 250, "spd1": 900, "temp0": 15, "temp1": -56},
     ["Estás en un vuelo de *Madrid a Los Ángeles*", "Despegas… y en pocos minutos subes a *11.000 metros*"], "Despegue"),
    ("thermo", {}, ["Ahí fuera hace *−56 °C*", "Cada kilómetro que subes, el aire se enfría unos *6,5 °C*"], "Crucero"),
    ("density", {}, ["Y el aire es *mucho más fino*: solo un 30 % del que hay en el suelo", "Menos resistencia… y *menos combustible*"], "Crucero"),
    ("cabin", {}, ["Pero tú respiras sin problema: la cabina va *presurizada*",
                   "Aunque no como en el suelo: como mucho, como a *2.400 metros*"], "La cabina"),
    ("chips", {}, ["Por eso tu bolsa de patatas *se hincha* en pleno vuelo"], "La cabina"),
    ("window", {"phase": "round"}, ["Mira la ventanilla: es *redonda* por algo",
                                    "Tiene 3 capas, y ese *agujerito* iguala la presión entre ellas"], "La ventanilla"),
    ("window", {"phase": "square"}, ["Los Comet de 1953 tenían ventanas *cuadradas*… y se agrietaron por las esquinas"],
     "La ventanilla"),
    ("flight", {"cam0": [-30, 50, 9], "cam1": [-66, 52, 7], "f0": 0.16, "f1": 0.5, "straight": 0.6, "regions": REG},
     ["Ahora mira el mapa: vamos *hacia el norte*", "Pasamos sobre *Canadá*… ¿no sería más corto ir recto?"], "La ruta"),
    ("globe_land", {"view_lat": 50, "view_lon0": -40, "view_lon1": -70, "note": "≈ 790 km menos"},
     ["En un globo, esta curva *es* la línea recta", "Es el camino más corto sobre una esfera: unos *790 km* menos"], "La ruta"),
    ("greenland", {"morph": 2.8, "note": "≈ 14 veces más pequeña"},
     ["El culpable es el mapa plano: *deforma* los polos", "Groenlandia parece casi tan grande como África…",
      "…y en realidad es *14 veces* más pequeña"], "El mapa engaña"),
    ("flight", {"cam0": [-92, 46, 6], "cam1": [-118, 34.5, 20], "f0": 0.62, "f1": 1.0, "alt0": 11000, "alt1": 0,
                "spd0": 900, "spd1": 250, "temp0": -56, "temp1": 20, "regions": REG},
     ["Tras *9.363 km*, aterrizas en Los Ángeles"], "Aterrizaje"),
    ("record", {}, ["Y a la vuelta, el viento empuja: la *corriente en chorro*",
                    "En 2020 un 747 hizo Nueva York → Londres en *4 h 56 min*", "A casi *1.300 km/h* respecto al suelo"],
     "Bonus"),
    ("outro_nls", {}, ["Sígueme para más cosas que *no sabías*"]),
]
build("formato1-viaje-en-directo", live, "Así es un vuelo Madrid → Los Ángeles por dentro ✈️",
      "Te acompañamos en un vuelo de Madrid a Los Ángeles: a 11.000 m fuera hace −56 °C, la cabina va como a 2.400 m, "
      "las ventanillas son redondas por los accidentes del Comet, la ruta curva es la más corta y el mapa plano engaña "
      "(Groenlandia es 14 veces más pequeña que África)." + DESC_COMMON, "live")

# ---------------------------------------------------------------- 2. TOP 5
top = [
    ("title", {"lines": ["5 cosas que", "NO sabías", "de los aviones"], "hl": 1, "pad": 0.4},
     ["5 cosas que *no sabías* de los aviones", "La número 1 te va a sorprender"]),
    ("top_card", {"n": 5, "title": "Fuera hace −56 °C"}, ["Número 5: fuera hace *−56 °C*", "Más frío que en la Antártida casi todo el año"], "#5 · −56 °C"),
    ("density", {}, ["Y el aire tiene solo un *30 %* de densidad: por eso gastan menos combustible"], "#5 · −56 °C"),
    ("top_card", {"n": 4, "title": "Ventanillas redondas"}, ["Número 4: las ventanillas son *redondas* por un accidente"],
     "#4 · Ventanillas"),
    ("window", {"phase": "square"}, ["Los Comet de los años 50 tenían ventanas cuadradas y se *agrietaron*"],
     "#4 · Ventanillas"),
    ("window", {"phase": "round"}, ["Desde entonces son redondas, con 3 capas y un *agujerito* que iguala la presión"],
     "#4 · Ventanillas"),
    ("top_card", {"n": 3, "title": "Vas a 2.400 m"}, ["Número 3: dentro del avión estás *a 2.400 metros*"], "#3 · La cabina"),
    ("cabin", {}, ["La cabina se presuriza, pero no como en el suelo: como mucho, como a *2.400 m*"], "#3 · La cabina"),
    ("chips", {}, ["Por eso las bolsas de patatas *se hinchan*… y el vino sabe distinto"], "#3 · La cabina"),
    ("top_card", {"n": 2, "title": "No vuelan en línea recta"}, ["Número 2: los aviones *no vuelan en línea recta*"],
     "#2 · La ruta"),
    ("flight", FLIGHT_FULL, ["De Madrid a Los Ángeles, el avión sube hasta *Canadá*"], "#2 · La ruta"),
    ("globe_land", {"view_lat": 50, "view_lon0": -40, "view_lon1": -70, "note": "≈ 790 km menos"},
     ["En un globo, esa curva es el camino *más corto*", "Unos *790 km* menos que ir \"recto\""], "#2 · La ruta"),
    ("greenland", {"morph": 2.6, "note": "≈ 14 veces más pequeña"},
     ["El mapa engaña: Groenlandia parece como *África*…", "…y en realidad es *14 veces* más pequeña"], "#2 · La ruta"),
    ("top_card", {"n": 1, "title": "El viento adelanta tu vuelo"}, ["Y número 1: el viento puede *adelantar tu vuelo*"],
     "#1 · El viento"),
    ("record", {}, ["En 2020, un 747 voló de Nueva York a Londres en *4 h 56 min*",
                    "La corriente en chorro lo empujaba: casi *1.300 km/h* respecto al suelo"], "#1 · El viento"),
    ("outro_nls", {}, ["¿Cuál no sabías? Sígueme para *más*"]),
]
build("formato2-top5", top, "5 cosas que NO sabías de los aviones ✈️",
      "Top 5: el frío de −56 °C a 11.000 m, por qué las ventanillas son redondas, la cabina a 2.400 m, la ruta curva "
      "que es la más corta y el récord de 4 h 56 min de Nueva York a Londres." + DESC_COMMON, "pop")

# ---------------------------------------------------------------- 3. QUIZ
CD = ("3… 2… 1…", 3.0)


def q(i, stmt, ans, expl_segs, chap):
    st = dur(stmt)
    reveal = ("¡Verdadero!" if ans else "¡Falso!", 1.3)
    return [("quiz", {"i": i, "n": 5, "answer": ans, "count_at": st, "text": stmt}, [stmt, CD, reveal], chap)] + \
           [(a, b, c, chap) for a, b, c in expl_segs]


quiz = [("title", {"lines": ["¿Aciertas", "las 5?", "V o F"], "hl": 1, "pad": 0.3},
         ["Verdadero o falso: ¿aciertas *las 5*?"])]
quiz += q(1, "Los aviones vuelan en *línea recta*", False, [
    ("flight", FLIGHT_FULL, ["En el mapa hacen una curva hacia el norte, sobre *Canadá*"]),
    ("globe_land", {"view_lat": 50, "view_lon0": -40, "view_lon1": -70, "note": "≈ 790 km menos"},
     ["Pero en un globo esa curva es el camino *más corto*", "Unos *790 km* menos"])], "Pregunta 1/5")
quiz += q(2, "Groenlandia es casi tan grande como *África*", False, [
    ("greenland", {"morph": 1.6, "note": "≈ 14 veces más pequeña"},
     ["Los mapas planos deforman los polos", "África es *14 veces* más grande"])], "Pregunta 2/5")
quiz += q(3, "A 11.000 metros, fuera hace *−56 °C*", True, [
    ("thermo", {}, ["Cada kilómetro que subes, el aire se enfría unos *6,5 °C*"]),
    ("density", {}, ["Y el aire es tan fino que el avión *gasta menos*"])], "Pregunta 3/5")
quiz += q(4, "La cabina va presurizada *como a nivel del mar*", False, [
    ("cabin", {}, ["Va como si estuvieras a unos *2.400 metros*, como mucho"]),
    ("chips", {}, ["Por eso se *hinchan* las bolsas de patatas"])], "Pregunta 4/5")
quiz += q(5, "Ir de América a Europa tarda *lo mismo* que volver", False, [
    ("record", {}, ["La corriente en chorro empuja hacia el este",
                    "En 2020, un 747 hizo Nueva York → Londres en *4 h 56 min*"])], "Pregunta 5/5")
quiz += [("quiz_end", {}, [("¿Cuántas acertaste? Dímelo en *comentarios*", 2.9)])]
build("formato3-quiz", quiz, "¿Verdadero o falso? 5 preguntas sobre aviones ✈️",
      "Quiz de 5 preguntas: ¿vuelan en línea recta?, ¿Groenlandia es tan grande como África?, ¿hace −56 °C fuera?, "
      "¿la cabina va como a nivel del mar?, ¿se tarda lo mismo en ir que en volver de América?" + DESC_COMMON, "show")
