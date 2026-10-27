"""Dos ejemplos mejorados tras el estudio de mercado: cámara tranquila, historia con pregunta, final en bucle."""
import json, os
import build_formats as B
from build_formats import build, REG, FLIGHT_FULL, DESC_COMMON
B.WPS = 2.3
HERE = os.path.dirname(os.path.abspath(__file__))

A = [
    ("flight", {"cam0": [-3.7, 40.4, 16], "cam1": [-11, 45, 16], "f0": 0, "f1": 0.05, "alt0": 0, "alt1": 11000,
                "spd0": 250, "spd1": 900, "temp0": 15, "temp1": -56},
     ["¿Por qué tu avión a *Los Ángeles* pasa por *Canadá*?", "Despegas en Madrid y subes a *11.000 metros*"], "Despegue"),
    ("thermo", {}, ["Ahí fuera hace *−56 °C*", "Cada kilómetro que subes, el aire se enfría unos *6,5 °C*"], "Crucero"),
    ("density", {}, ["Y el aire es tan fino que solo queda un *30 %*", "Menos resistencia: el avión *gasta menos*"], "Crucero"),
    ("cabin", {}, ["Dentro, la cabina va presurizada como a *2.400 metros*"], "La cabina"),
    ("chips", {}, ["Por eso tu bolsa de patatas *se hincha*"], "La cabina"),
    ("window", {"phase": "round"}, ["La ventanilla es *redonda* por algo:", "3 capas y un *agujerito* que iguala la presión"],
     "La ventanilla"),
    ("window", {"phase": "square"}, ["En 1953 los Comet tenían ventanas *cuadradas*… y se agrietaron"], "La ventanilla"),
    ("flight", {"cam0": [-30, 50, 7.5], "cam1": [-66, 52, 7.5], "f0": 0.16, "f1": 0.5, "straight": 0.6, "regions": REG},
     ["Ahora mira la ruta: no va recta, sube *hacia el norte*", "Pasa sobre *Canadá*… y parece un rodeo"], "La ruta"),
    ("globe_land", {"view_lat": 50, "view_lon0": -40, "view_lon1": -70, "note": "≈ 790 km menos"},
     ["Pero en un globo, esa curva *es* la línea recta", "Te ahorras unos *790 km*"], "La ruta"),
    ("greenland", {"morph": 5.2, "note": "≈ 14 veces más pequeña"},
     ["El mapa plano engaña: deforma los polos", "Groenlandia parece tan grande como *África*…",
      "…y en realidad es *14 veces* más pequeña"], "El mapa engaña"),
    ("flight", {"cam0": [-92, 46, 9], "cam1": [-118, 34.5, 9], "f0": 0.62, "f1": 1.0, "alt0": 11000, "alt1": 0,
                "spd0": 900, "spd1": 250, "temp0": -56, "temp1": 20, "regions": REG},
     ["Tras *9.363 km*, aterrizas en Los Ángeles"], "Aterrizaje"),
    ("outro_nls", {}, ["Mándaselo a quien siempre pide *ventanilla*", "Y si alguien te pregunta…"]),
]
build("ejemplo-A-historia-larga", A, "¿Por qué tu avión a Los Ángeles pasa por Canadá? ✈️",
      "Un vuelo Madrid → Los Ángeles por dentro: −56 °C fuera, la cabina a 2.400 m, ventanillas redondas por el Comet, "
      "y por qué la ruta curva por Canadá es la más corta (y por qué Groenlandia no es tan grande)." + DESC_COMMON, "live")

Bs = [
    ("greenland", {"morph": 6.0, "note": "≈ 14 veces más pequeña"},
     ["Este mapa te ha *mentido* toda la vida", "Groenlandia parece tan grande como *África*…", "Pero si las pones a escala real…", "África es *14 veces* más grande"]),
    ("flight", FLIGHT_FULL, ["Por eso el avión a Los Ángeles parece dar un *rodeo* por Canadá"]),
    ("globe_land", {"view_lat": 50, "view_lon0": -40, "view_lon1": -70, "note": "≈ 790 km menos"},
     ["En un globo, esa curva es el camino *más corto*", "Unos *790 km* menos"]),
    ("outro_nls", {}, ["Mándaselo a quien todavía se cree *este mapa*"]),
]
build("ejemplo-B-corto", Bs, "Este mapa te ha mentido toda la vida 🌍",
      "Groenlandia parece tan grande como África, pero es 14 veces más pequeña. Y por eso los aviones parecen dar un rodeo "
      "por Canadá cuando en realidad van por el camino más corto." + DESC_COMMON, "pop", chapters_on=False)

for sid in ("ejemplo-A-historia-larga", "ejemplo-B-corto"):
    p = os.path.join(HERE, "scripts", f"{sid}.json")
    s = json.load(open(p))
    s["calm"] = True
    s["bpm"] = 110
    s["chunk_n"] = 3
    s["zoom_gap"] = 4.5
    s["notifs"] = s["notifs"][:1]
    json.dump(s, open(p, "w"), ensure_ascii=False, indent=1)
