import json, os
import build_formats as B
from build_formats import build, REG, DESC_COMMON
from build_six import TAKEOFF, ROUTE, LANDING, GLOBE, FULL
B.WPS = 2.3
HERE = os.path.dirname(os.path.abspath(__file__))
V = {
"P1_frio": ("¿Por qué ahí fuera hace −56 °C? ✈️", [
 ("flight", TAKEOFF, ["¿Sabías que tu ventanilla te separa de *−56 °C*?", "Despegas, y en pocos minutos estás a *11.000 metros*"], "Despegue"),
 ("thermo", {}, ["Cuanto más subes, más frío hace", "Cada kilómetro, el aire pierde unos *6,5 °C*", "A 11.000 metros: *−56 °C*"], "El frío"),
 ("density", {}, ["Y el aire se vuelve finísimo: queda solo un *30 %*", "Por eso los aviones vuelan tan alto: *menos resistencia*"], "El aire"),
 ("cabin", {}, ["Pero tú no lo notas: la cabina va *presurizada*", "Como si estuvieras a *2.400 metros*"], "La cabina"),
 ("chips", {}, ["La prueba: tu bolsa de patatas *se hincha*"], "La cabina"),
 ("outro_nls", {}, ["Mándaselo a quien siempre tiene *frío en el avión*"])]),
"P2_ventanilla": ("El secreto de la ventanilla del avión 🪟", [
 ("window", {"phase": "round"}, ["Mira bien la ventanilla del avión", "No tiene ni una sola *esquina*"], "La ventanilla"),
 ("window", {"phase": "square"}, ["En los años 50 era distinto: los Comet tenían ventanas *cuadradas*", "En 1954, dos se *partieron* en pleno vuelo", "La fatiga del metal empezó en las *esquinas*"], "El accidente"),
 ("cabin", {}, ["El problema es la presión: la cabina se infla como un globo", "Por dentro, como a *2.400 metros*; fuera, a 11.000"], "La presión"),
 ("window", {"phase": "round"}, ["Por eso hoy son redondas: reparten la fuerza", "Y tienen *3 capas*… y un agujerito que iguala la presión"], "La solución"),
 ("outro_nls", {}, ["La próxima vez que vueles, busca el *agujerito*"])]),
"P3_mapa": ("El mapa que te ha mentido toda la vida 🌍", [
 ("greenland", {"morph": 6.2, "note": "≈ 14 veces más pequeña"}, ["Este mapa te ha *mentido* toda la vida", "Groenlandia parece tan grande como *África*…", "Pero si las pones a escala real…", "África es *14 veces* más grande"], "El mapa"),
 ("flight", FULL, ["Y ese mismo mapa engaña a los pasajeros", "El vuelo Madrid → Los Ángeles parece dar un *rodeo* por Canadá"], "La ruta"),
 ("globe_land", GLOBE, ["En un globo, esa curva es el camino *más corto*", "Unos *790 km* menos que ir \"recto\""], "El globo"),
 ("outro_nls", {}, ["Mándaselo a quien todavía se cree *este mapa*"])]),
"P4_record": ("El vuelo más rápido de la historia ⚡", [
 ("record", {}, ["En 2020, un avión cruzó el Atlántico en *4 h 56 min*", "De Nueva York a Londres, casi *una hora* antes de lo normal", "Iba a casi *1.300 km/h* respecto al suelo"], "El récord"),
 ("thermo", {}, ["El truco está a *11.000 metros*", "Allí arriba, a −56 °C, soplan ríos de viento"], "El truco"),
 ("density", {}, ["Y el aire es tan fino que casi *no frena*"], "El truco"),
 ("record", {}, ["Es la *corriente en chorro*: sopla hacia el este", "Por eso ir de América a Europa suele ser *más rápido* que volver"], "El viento"),
 ("outro_nls", {}, ["¿Lo sabías? Mándaselo a quien vuele *a América*"])]),
"P5_ruta": ("¿Por qué tu avión no vuela en línea recta? ✈️", [
 ("flight", ROUTE, ["¿Por qué tu avión *no vuela recto*?", "De Madrid a Los Ángeles sube hacia *Canadá*"], "La ruta"),
 ("globe_land", GLOBE, ["Porque la Tierra no es plana", "En una esfera, esa curva *es* la línea recta"], "La esfera"),
 ("greenland", {"morph": 4.4, "note": "≈ 14 veces más pequeña"}, ["El mapa plano deforma los polos", "Por eso Groenlandia parece *gigante*… y es 14 veces menor que África"], "El mapa"),
 ("flight", LANDING, ["Resultado: *9.363 km* en vez de más de 10.100", "Te ahorras unos *790 km* de vuelo"], "La llegada"),
 ("outro_nls", {}, ["Y la próxima vez que mires el mapa del avión… ya sabes *por qué*"])]),
}
for sid, (title, segs) in V.items():
    build(sid, segs, title, title + DESC_COMMON, "premium")
    p = os.path.join(HERE, "scripts", f"{sid}.json"); s = json.load(open(p))
    s.update(chunk_n=3, seed=sum(map(ord, sid)) % 1000); s["notifs"] = s["notifs"][:1]
    json.dump(s, open(p, "w"), ensure_ascii=False, indent=1)
