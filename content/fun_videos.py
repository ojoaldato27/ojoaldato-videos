from fun_build import build, I, T, N, M, O, S

V = {}

# 1 · TITANIC
V["F01_titanic"] = dict(
    title="La llave que pudo salvar el Titanic 🔑", question="¿Qué abría la llave?",
    desc="Los vigías del Titanic no tenían prismáticos… y la llave de su caja se había quedado en tierra.",
    tags=["curiosidades", "historia", "titanic", "sabías que"],
    beats=[
        dict(bg="navy", lines=["Una simple *llave* pudo haber salvado el Titanic", "¿Tú qué crees que abría?"], items=[
            (0, 0.0, I("ship", 540, 760, 620)),
            (0, 1.2, I("key", 820, 430, 240)),
            (1, 0.2, M("wow", 220, 1180, 230))]),
        dict(bg="cream", q_from=True, lines=["¿La puerta del motor, la caja de los prismáticos… o la sala de la radio?",
                                             "Quédate, que al final te lo cuento"], items=[
            (0, 0.0, O(["La puerta del motor", "Los prismáticos", "La sala de la radio"], 1, y=520)),
            (1, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="sky", lines=["Abril de 1912: el Titanic zarpa en su primer viaje",
                              "El barco más grande de su época… e *insumergible*, decían"], items=[
            (0, 0.0, I("ship", 540, 760, 720, tw={"x": [None, 1.4, -380, 540]})),
            (0, 0.8, T("1912", 540, 430, 90)),
            (1, 1.6, S("¿INSUMERGIBLE?", 540, 1120, 80))]),
        dict(bg="mint", lines=["Arriba, en el mástil, dos vigías buscaban icebergs",
                               "Pero tenían un problema: *no tenían prismáticos*"], items=[
            (0, 0.0, I("mast", 360, 760, 620)),
            (1, 0.3, I("binoculars", 780, 640, 300)),
            (1, 1.4, I("cross", 780, 640, 280, float=False))]),
        dict(bg="orange", lines=["Los prismáticos estaban guardados bajo llave",
                                 "Y esa llave la tenía el oficial *David Blair*",
                                 "Pero lo cambiaron a última hora… y se bajó del barco *con la llave en el bolsillo*"], items=[
            (0, 0.0, I("binoculars", 540, 520, 280)),
            (1, 0.0, I("person", 300, 930, 340)),
            (1, 0.4, I("key", 760, 930, 260, tw={"x": [2.6, 3.8, 760, 330], "s": [2.6, 3.8, 260, 110]})),
            (1, 0.8, T("David Blair", 300, 1200, 52)),
            (2, 2.2, M("no", 830, 1180, 200))]),
        dict(bg="navy", lines=["El 14 de abril, de noche, los vigías vieron el iceberg *demasiado tarde*",
                               "Apenas *un minuto* antes del choque"], items=[
            (0, 0.0, I("iceberg", 760, 760, 440)),
            (0, 0.0, I("ship", 300, 840, 440, tw={"x": [None, 4.5, 160, 420]})),
            (1, 0.0, I("clock", 820, 420, 200, speed=6)),
            (1, 0.4, T("Solo 1 minuto", 540, 1180, 66))]),
        dict(bg="pink", lines=["Pero espera, que lo más curioso viene ahora",
                               "Tras el hundimiento, uno de los vigías dijo que con prismáticos *lo habrían visto a tiempo*"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.3, I("mast", 330, 820, 520)),
            (1, 1.2, I("binoculars", 780, 760, 300)),
            (1, 2.4, I("check", 780, 1080, 160, float=False))]),
        dict(bg="lime", lines=["¿La respuesta? La llave abría *la caja de los prismáticos*",
                               "Aunque hoy los expertos todavía discuten si habría cambiado algo"], confetti=(0, 0.4), items=[
            (0, 0.0, O(["La puerta del motor", "Los prismáticos", "La sala de la radio"], 1, y=520, reveal=(0, 0.3))),
            (1, 0.0, M("think", 540, 1130, 240))]),
        dict(bg="yellow", lines=["En 2007, esa llave se subastó por *90.000 libras*",
                                 "Una llave pequeñita… con una historia *gigante*"], items=[
            (0, 0.0, I("key", 540, 560, 380)),
            (0, 1.0, I("money", 540, 960, 320)),
            (1, 0.6, M("happy", 540, 1220, 200))]),
    ])

# 2 · LA CARA OCULTA DE LA LUNA
OPT_L = ["No gira", "Gira al ritmo de su vuelta", "La otra cara está a oscuras"]
V["F02_luna"] = dict(
    title="Nunca has visto la otra cara de la Luna 🌕", question="¿Por qué siempre vemos la misma cara?",
    desc="La Luna gira justo al ritmo de su vuelta a la Tierra. Por eso nadie vio su otra cara hasta 1959.",
    tags=["curiosidades", "espacio", "luna", "sabías que"],
    beats=[
        dict(bg="navy", lines=["Nunca has visto la otra cara de la *Luna*", "Ni tú, ni tus padres, ni nadie… *hasta 1959*"], items=[
            (0, 0.0, I("moon", 540, 680, 560, face=True)),
            (1, 0.3, M("wow", 220, 1180, 220)),
            (1, 1.4, T("1959", 830, 1180, 80))]),
        dict(bg="cream", q_from=True, lines=["¿Por qué? ¿Porque la Luna no gira, porque gira al mismo ritmo que da la vuelta a la Tierra…",
                                             "…o porque la otra cara está siempre *a oscuras*?"], items=[
            (0, 0.0, O(OPT_L, 1, y=520)),
            (1, 1.0, M("think", 540, 1110, 300))]),
        dict(bg="sky", lines=["La Luna tarda casi *un mes* en dar la vuelta a la Tierra",
                              "Y tarda *lo mismo* en girar sobre sí misma"], items=[
            (0, 0.0, I("orbit", 540, 760, 900, speed=0.9)),
            (1, 0.3, I("curve_arrow", 850, 1180, 200))]),
        dict(bg="mint", lines=["Por eso siempre nos enseña *la misma cara*",
                               "Es como bailar sin dejar de mirar a tu pareja"], items=[
            (0, 0.0, I("earth", 330, 760, 360, face=True)),
            (0, 0.3, I("moon", 790, 760, 280, face=True)),
            (1, 0.3, M("happy", 540, 1180, 220))]),
        dict(bg="orange", lines=["Los científicos lo llaman *acoplamiento de marea*",
                                 "La gravedad de la Tierra fue frenando su giro hasta *sincronizarlo*"], items=[
            (0, 0.0, T("Acoplamiento de marea", 540, 470, 60)),
            (1, 0.0, I("earth", 320, 820, 340)),
            (1, 0.4, I("moon", 790, 820, 260)),
            (1, 1.0, I("curve_arrow", 790, 820, 360))]),
        dict(bg="navy", lines=["Pero espera, que lo más curioso viene ahora",
                               "En 1959, la sonda soviética *Luna 3* fotografió por fin la otra cara"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("satellite", 760, 600, 360, tw={"x": [None, 3.0, 900, 640]})),
            (1, 0.8, I("moon", 330, 960, 380, side="far")),
            (1, 2.2, I("camera", 760, 1120, 220, flash=True))]),
        dict(bg="lilac", lines=["Y en 2019, China fue la primera en *aterrizar* allí", "Con la misión *Chang'e 4*"], items=[
            (0, 0.0, I("moon", 540, 820, 600, side="far")),
            (0, 1.2, I("flag", 640, 560, 240)),
            (1, 0.2, T("Chang'e 4", 540, 1230, 64))]),
        dict(bg="lime", lines=["¿La respuesta? La B: gira al mismo ritmo que da la vuelta",
                               "Y la C es un mito: la otra cara recibe *tanta luz del Sol* como esta",
                               "No es la cara oscura… es la cara *oculta*"], confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_L, 1, y=520, reveal=(0, 0.3))),
            (1, 0.4, S("MITO", 820, 880, 70)),
            (1, 1.0, I("sun", 300, 1150, 240)),
            (2, 0.3, M("wink", 760, 1170, 220))]),
        dict(bg="yellow", lines=["Así que la próxima vez que mires a la Luna…",
                                 "…recuerda que *siempre te enseña la misma cara*"], items=[
            (0, 0.0, I("moon", 540, 700, 560, face=True)),
            (1, 0.4, M("wink", 220, 1180, 200))]),
    ])

# 3 · TORRE EIFFEL
OPT_E = ["Un milímetro", "Unos 15 centímetros", "Dos metros"]
V["F03_eiffel"] = dict(
    title="La Torre Eiffel crece en verano 🗼", question="¿Cuánto crece en verano?",
    desc="Sus 7.300 toneladas de hierro se dilatan con el calor: la torre crece y hasta se aparta del Sol.",
    tags=["curiosidades", "ingeniería", "torre eiffel", "sabías que"],
    beats=[
        dict(bg="sky", lines=["La Torre Eiffel *no mide siempre lo mismo*", "En verano… *crece*"], items=[
            (0, 0.0, I("tower", 540, 800, 620)),
            (1, 0.0, I("tower", 540, 800, 620, tw={"grow": [None, 1.5, 0.0, 0.1]})),
            (1, 0.4, M("wow", 880, 1180, 200))]),
        dict(bg="cream", q_from=True, lines=["¿Cuánto crees que crece?", "¿Un milímetro, unos 15 centímetros… o dos metros?",
                                             "Al final te lo digo"], items=[
            (0, 0.0, O(OPT_E, 1, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="orange", lines=["Está hecha de *7.300 toneladas* de hierro", "Repartidas en más de *18.000 piezas*"], items=[
            (0, 0.0, N(0, 7300, 540, 600, 170, "toneladas de hierro")),
            (1, 0.0, N(0, 18000, 540, 1000, 140, "piezas")),
            (1, 0.6, I("tower", 880, 1180, 240))]),
        dict(bg="yellow", lines=["Y el hierro tiene una costumbre: con el calor, *se estira*", "Se llama *dilatación térmica*"], items=[
            (0, 0.0, I("sun", 300, 600, 340)),
            (0, 0.6, I("thermometer", 790, 720, 440, tw={"level": [None, 2.0, 0.2, 0.95]})),
            (1, 0.2, T("Dilatación térmica", 540, 1200, 62))]),
        dict(bg="mint", lines=["En verano, el hierro de toda la torre se dilata a la vez", "Y la torre *crece* hacia arriba"], items=[
            (0, 0.0, I("tower", 540, 820, 600, tw={"grow": [None, 4.0, 0.0, 0.1]})),
            (1, 0.2, I("arrow", 860, 520, 220, ang=-90))]),
        dict(bg="pink", lines=["Pero espera, que hay más", "El lado que da al Sol se calienta más que el otro",
                               "Y la torre se *inclina* un poquito, apartándose del Sol"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("sun", 240, 520, 260)),
            (1, 0.6, I("tower", 600, 860, 520)),
            (2, 0.3, I("arrow", 880, 700, 200, ang=0))]),
        dict(bg="navy", lines=["Por la noche, al enfriarse, *vuelve a su sitio*", "Y en invierno, con el frío, *encoge*"], items=[
            (0, 0.0, I("moon", 820, 480, 220)),
            (0, 0.0, I("tower", 500, 860, 560, tw={"grow": [None, 4.5, 0.1, -0.04]})),
            (1, 0.0, I("snowflake", 250, 520, 220))]),
        dict(bg="lime", lines=["¿La respuesta? Los ingenieros han medido entre *12 y 15 centímetros*",
                               "Más o menos lo que mide un lápiz"], confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_E, 1, y=520, reveal=(0, 0.3))),
            (1, 0.2, T("12-15 cm", 540, 1120, 90))]),
        dict(bg="yellow", lines=["Así que si la visitas en agosto…", "…estarás subiendo a una torre *un poco más alta*"], items=[
            (0, 0.0, I("tower", 540, 800, 620, grow=0.1)),
            (1, 0.3, M("happy", 870, 1180, 200))]),
    ])

# 4 · SILBO GOMERO
OPT_S = ["50 metros", "500 metros", "5 kilómetros"]
V["F04_silbo"] = dict(
    title="En esta isla de España se habla silbando 🎶", question="¿Hasta dónde se oye un silbido?",
    desc="El silbo gomero de La Gomera convierte el español en 6 sonidos silbados y se oye hasta a 5 km.",
    tags=["curiosidades", "españa", "la gomera", "silbo gomero", "sabías que"],
    beats=[
        dict(bg="mint", lines=["En una isla de España, la gente habla *silbando*", "Y no es un juego: es un idioma de verdad"], items=[
            (0, 0.0, I("island", 540, 720, 640)),
            (0, 1.2, I("person", 830, 1150, 300, whistle=True)),
            (1, 0.3, M("wow", 230, 1170, 210))]),
        dict(bg="cream", q_from=True, lines=["¿Hasta dónde crees que se oye un silbido así?", "¿50 metros, 500 metros… o 5 kilómetros?",
                                             "Te lo cuento al final"], items=[
            (0, 0.0, O(OPT_S, 2, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="sky", lines=["Es el *silbo gomero*, de la isla de La Gomera, en Canarias",
                              "Lo crearon los primeros habitantes de las islas: *los guanches*"], items=[
            (0, 0.0, I("island", 540, 640, 560)),
            (0, 1.2, T("La Gomera", 540, 1000, 66)),
            (1, 0.3, I("person", 540, 1200, 240))]),
        dict(bg="orange", lines=["La isla está llena de barrancos y montañas", "Ir de un lado a otro podía llevar horas",
                                 "Así que los pastores aprendieron a *hablar silbando*"], items=[
            (0, 0.0, I("island", 540, 700, 700)),
            (2, 0.0, I("person", 260, 1150, 280, whistle=True)),
            (2, 0.6, I("person", 820, 1150, 280, col=(90, 140, 230)))]),
        dict(bg="lilac", lines=["Pero ¿cómo se habla silbando?", "Convierte el español en solo *6 sonidos*: 2 vocales y 4 consonantes"], items=[
            (0, 0.0, M("think", 540, 600, 280, out=(1, 0.0))),
            (1, 0.0, N(0, 6, 540, 640, 260, "sonidos")),
            (1, 1.4, T("2 vocales", 300, 1080, 58)),
            (1, 2.0, T("4 consonantes", 760, 1080, 58))]),
        dict(bg="pink", lines=["Pero espera, que hay más", "Desde 1999 se enseña en los *colegios* de la isla",
                               "Y en 2009 la UNESCO lo declaró *Patrimonio de la Humanidad*"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("book", 300, 700, 340)),
            (2, 0.2, I("medal", 780, 940, 340))]),
        dict(bg="lime", lines=["¿La respuesta? Un silbido puede oírse hasta a *5 kilómetros*", "Mucho más lejos que cualquier grito"],
             confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_S, 2, y=520, reveal=(0, 0.3))),
            (1, 0.0, I("waves", 540, 1120, 320))]),
        dict(bg="yellow", lines=["Así que si algún día vas a La Gomera y oyes un silbido…",
                                 "…puede que alguien *te esté hablando*"], items=[
            (0, 0.0, I("person", 380, 820, 420, whistle=True)),
            (1, 0.3, M("wink", 820, 900, 240))]),
    ])

# 5 · POR QUÉ EL MAR ES SALADO
OPT_M = ["De los peces", "De las rocas", "De la Luna"]
V["F05_mar"] = dict(
    title="¿Por qué el mar es salado y los ríos no? 🌊", question="¿De dónde sale la sal del mar?",
    desc="La lluvia desgasta las rocas, los ríos llevan los minerales al mar y el Sol evapora el agua… pero no la sal.",
    tags=["curiosidades", "ciencia", "mar", "sabías que"],
    beats=[
        dict(bg="sky", lines=["¿Por qué el mar es *salado*…", "…si los ríos que llegan a él son de agua dulce?"], items=[
            (0, 0.0, I("ocean", 540, 620, 600)),
            (1, 0.0, I("river", 540, 1020, 520)),
            (1, 0.4, M("think", 860, 400, 200))]),
        dict(bg="cream", q_from=True, lines=["¿De dónde sale tanta sal?", "¿De los peces, de las rocas… o de la Luna?",
                                             "La respuesta, al final"], items=[
            (0, 0.0, O(OPT_M, 1, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="navy", lines=["Todo empieza con la *lluvia*", "El agua de lluvia es un poquito *ácida*: lleva algo de dióxido de carbono"], items=[
            (0, 0.0, I("cloud", 540, 600, 520, rain=True)),
            (1, 0.6, T("CO2", 820, 1000, 70))]),
        dict(bg="orange", lines=["Al caer, va desgastando las *rocas*", "Y les arranca pequeñas partículas de minerales"], items=[
            (0, 0.0, I("cloud", 540, 430, 320, rain=True)),
            (0, 0.3, I("rock", 540, 780, 460)),
            (1, 0.3, I("crystals", 540, 1100, 280))]),
        dict(bg="mint", lines=["Los ríos arrastran esos minerales hasta el mar", "Pero en un río hay tan pocos que *no los notas*"], items=[
            (0, 0.0, I("river", 540, 700, 600)),
            (0, 0.4, I("crystals", 200, 700, 160, tw={"x": [None, 3.0, 200, 880]})),
            (1, 0.3, I("glass", 840, 1130, 240))]),
        dict(bg="sky", lines=["En el mar, el Sol *evapora* el agua…", "…pero la sal *no se evapora*: se queda",
                              "Y así, durante millones de años, se ha ido acumulando"], items=[
            (0, 0.0, I("sun", 820, 420, 240)),
            (0, 0.2, I("ocean", 540, 800, 620)),
            (0, 0.8, I("arrow", 330, 560, 160, ang=-90)),
            (1, 0.2, I("salt", 300, 1150, 240)),
            (2, 0.3, I("clock", 800, 1150, 200, speed=8))]),
        dict(bg="pink", lines=["Pero espera, que hay más", "Si secaras los océanos y repartieras su sal por los continentes…",
                               "…formaría una capa de *más de 160 metros*: como un edificio de 40 plantas"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("salt", 540, 680, 360)),
            (2, 0.0, N(0, 166, 540, 1080, 160, "metros de sal"))]),
        dict(bg="lime", lines=["¿La respuesta? La B: la sal sale de *las rocas*",
                               "Y casi toda es lo mismo que la sal de tu cocina: *sodio y cloro*"], confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_M, 1, y=520, reveal=(0, 0.3))),
            (1, 0.2, I("salt", 540, 1110, 260))]),
        dict(bg="yellow", lines=["Así que la próxima vez que tragues agua en la playa…",
                                 "…recuerda que estás probando *rocas de hace millones de años*"], items=[
            (0, 0.0, I("ocean", 540, 720, 560)),
            (1, 0.4, M("happy", 540, 1150, 220))]),
    ])

# 6 · AVIONES BLANCOS
OPT_A = ["Es más barato", "Por seguridad", "Por las dos cosas"]
V["F06_aviones_blancos"] = dict(
    title="¿Por qué casi todos los aviones son blancos? ✈️", question="¿Por qué son blancos?",
    desc="El blanco refleja el sol, deja ver grietas y fugas, ahorra pintura y facilita revender el avión.",
    tags=["curiosidades", "aviones", "sabías que"],
    beats=[
        dict(bg="sky", lines=["Casi todos los aviones son *blancos*", "Y no es por estética"], items=[
            (0, 0.0, I("plane", 540, 720, 700, tw={"x": [None, 1.2, -300, 540]})),
            (1, 0.3, M("think", 860, 1160, 210))]),
        dict(bg="cream", q_from=True, lines=["¿Tú por qué crees que es?", "¿Porque es más barato, por seguridad… o por las dos cosas?",
                                             "Te lo digo al final"], items=[
            (0, 0.0, O(OPT_A, 2, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="yellow", lines=["Primero: el blanco *refleja* la luz del Sol", "Así el avión se calienta menos y la pintura se estropea menos"], items=[
            (0, 0.0, I("sun", 280, 520, 320)),
            (0, 0.5, I("plane", 600, 900, 560)),
            (1, 0.3, I("thermometer", 880, 560, 300, level=0.3, hot=False))]),
        dict(bg="mint", lines=["Segundo: en el blanco se ven mucho mejor las *grietas* y las fugas de aceite",
                               "Los mecánicos las detectan antes"], items=[
            (0, 0.0, I("plane", 540, 620, 560)),
            (0, 1.0, I("magnifier", 600, 960, 420))]),
        dict(bg="orange", lines=["Tercero: la pintura *pesa*", "Pintar entero un avión grande puede añadir entre 270 y 540 kilos",
                                 "Como llevar *8 pasajeros* extra en cada vuelo"], items=[
            (0, 0.0, I("paint", 300, 620, 320)),
            (1, 0.0, I("weight", 780, 640, 320, label="kg")),
            (2, 0.0, N(0, 8, 540, 1060, 200, "pasajeros extra"))]),
        dict(bg="pink", lines=["Pero espera, que hay más", "Los colores oscuros *se destiñen* antes y hay que repintarlos más",
                               "Y un avión puede volar *más de 25 años*, pasando de aerolínea en aerolínea"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("paint", 540, 680, 320, col=(60, 60, 90))),
            (2, 0.0, N(0, 25, 540, 1080, 180, "años volando"))]),
        dict(bg="sky", lines=["Si es blanco, repintarlo para la siguiente aerolínea es *más fácil y barato*",
                              "Y hay indicios de que los pájaros lo ven mejor"], items=[
            (0, 0.0, I("plane", 300, 640, 420, stripe=(230, 80, 90))),
            (0, 0.6, I("plane", 780, 820, 420, stripe=(90, 200, 120))),
            (1, 0.2, I("bird", 540, 1130, 260))]),
        dict(bg="lime", lines=["¿La respuesta? La C: *las dos cosas*", "Es más barato… y más seguro"], confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_A, 2, y=520, reveal=(0, 0.3))),
            (1, 0.0, M("happy", 540, 1130, 240))]),
        dict(bg="yellow", lines=["Así que la próxima vez que veas un avión de colores…",
                                 "…piensa que a alguien le ha costado *bastante más*"], items=[
            (0, 0.0, I("plane", 540, 720, 640, col=(255, 140, 170), stripe=(120, 80, 220))),
            (1, 0.3, M("wink", 540, 1150, 220))]),
    ])

# 7 · LUCES APAGADAS AL ATERRIZAR
OPT_C = ["Ahorrar batería", "Ver el paisaje", "Por si hay que evacuar"]
V["F07_luces_avion"] = dict(
    title="¿Por qué apagan las luces del avión al aterrizar? 💡", question="¿Por qué apagan las luces?",
    desc="Bajan las luces para que tus ojos se acostumbren a la oscuridad y suben las persianas para ver qué pasa fuera.",
    tags=["curiosidades", "aviones", "seguridad", "sabías que"],
    beats=[
        dict(bg="navy", lines=["Antes de aterrizar de noche, *apagan las luces* del avión", "Y no es para que duermas"], items=[
            (0, 0.0, I("bulb", 540, 660, 420, tw={"on": [1.4, 2.4, 1.0, 0.0]})),
            (1, 0.0, I("window", 830, 1120, 240, night=True)),
            (1, 0.3, M("think", 230, 1130, 210))]),
        dict(bg="cream", q_from=True, lines=["¿Tú por qué crees que es?", "¿Para ahorrar batería, para que veas el paisaje… o por si hay que evacuar?",
                                             "Te lo cuento al final"], items=[
            (0, 0.0, O(OPT_C, 2, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="sky", lines=["El despegue y el aterrizaje son los momentos *más delicados* del vuelo",
                              "Si algo sale mal, hay que salir del avión *muy rápido*"], items=[
            (0, 0.0, I("plane", 540, 660, 640, tw={"x": [None, 1.5, -300, 540]})),
            (1, 0.2, I("exit_sign", 540, 1060, 420))]),
        dict(bg="navy", lines=["Pero si pasas de la luz a la oscuridad de golpe, *no ves nada*",
                               "Tus ojos necesitan un tiempo para acostumbrarse"], items=[
            (0, 0.0, I("bulb", 300, 600, 300, tw={"on": [0.6, 1.0, 1.0, 0.0]})),
            (0, 1.2, M("no", 760, 640, 300)),
            (1, 0.2, I("clock", 540, 1080, 260, speed=5))]),
        dict(bg="lilac", lines=["Por eso bajan las luces *antes*", "Así, si hay que evacuar, tus ojos *ya están listos* para la oscuridad",
                                "Y encontrarás mejor el camino hasta la *salida*"], items=[
            (0, 0.0, I("bulb", 540, 600, 340, on=0.15)),
            (1, 0.3, M("happy", 300, 1060, 260)),
            (2, 0.2, I("exit_sign", 780, 1080, 320))]),
        dict(bg="pink", lines=["Pero espera, que hay más", "¿Y por qué te piden *subir la persiana*?"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.0, I("window", 540, 780, 520, tw={"shade": [0.8, 2.0, 0.9, 0.0]}))]),
        dict(bg="sky", lines=["Para que tú y la tripulación veáis qué pasa *fuera*",
                              "Si hay *fuego* en un lado, saben que hay que salir por el otro"], items=[
            (0, 0.0, I("window", 330, 700, 420)),
            (1, 0.0, I("fire", 790, 720, 340)),
            (1, 1.2, I("arrow", 540, 1120, 320, ang=180))]),
        dict(bg="lime", lines=["¿La respuesta? La C: *por si hay que evacuar*", "Luces bajas y persianas arriba: dos trucos de seguridad"],
             confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_C, 2, y=520, reveal=(0, 0.3))),
            (1, 0.2, I("bulb", 330, 1110, 240, on=0.2)),
            (1, 0.6, I("window", 760, 1110, 240))]),
        dict(bg="yellow", lines=["Así que la próxima vez que apaguen las luces al aterrizar…",
                                 "…ya sabes que te están *preparando los ojos*"], items=[
            (0, 0.0, I("bulb", 540, 700, 420, tw={"on": [None, 1.5, 1.0, 0.2]})),
            (1, 0.3, M("wink", 540, 1150, 230))]),
    ])

# 8 · BACTERIAS Y CÉLULAS
OPT_B = ["10 bacterias", "100 bacterias", "Más o menos 1"]
V["F08_bacterias"] = dict(
    title="No tienes 10 veces más bacterias que células 🦠", question="¿Cuántas bacterias tienes por célula?",
    desc="Un estudio de 2016 calculó unos 30 billones de células y unos 38 billones de bacterias: casi 1 a 1.",
    tags=["curiosidades", "cuerpo humano", "ciencia", "sabías que"],
    beats=[
        dict(bg="mint", lines=["Seguro que has oído que tienes *10 veces más bacterias* que células", "Pues es *mentira*"], items=[
            (0, 0.0, I("bacteria", 300, 640, 280)),
            (0, 0.4, I("bacteria", 760, 560, 240, col=(255, 170, 90))),
            (0, 0.8, I("bacteria", 640, 920, 300, col=(150, 170, 255))),
            (1, 0.3, S("MITO", 540, 1180, 100))]),
        dict(bg="cream", q_from=True, lines=["Entonces, ¿cuántas bacterias tienes por cada célula?", "¿10, 100… o más o menos 1?",
                                             "Al final lo vemos"], items=[
            (0, 0.0, O(OPT_B, 2, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="pink", lines=["Tu cuerpo tiene unos *30 billones* de células", "Y la mayoría son *glóbulos rojos*"], items=[
            (0, 0.0, N(0, 30, 540, 600, 220, "billones de células")),
            (1, 0.0, I("cell", 540, 1060, 340))]),
        dict(bg="lime", lines=["Y bacterias tienes unos *38 billones*", "La mayoría viviendo en tu *intestino grueso*"], items=[
            (0, 0.0, N(0, 38, 540, 600, 220, "billones de bacterias")),
            (1, 0.0, I("bacteria", 330, 1060, 260)),
            (1, 0.4, I("bacteria", 760, 1060, 260, col=(255, 170, 90)))]),
        dict(bg="orange", lines=["¿Y de dónde salió lo de 10 a 1?", "De un cálculo de *1972*, que suponía el intestino lleno de bacterias de punta a punta",
                                 "Pero casi todas viven solo en una parte: *el colon*"], items=[
            (0, 0.0, M("think", 540, 620, 300, out=(1, 0.0))),
            (1, 0.0, T("1972", 540, 560, 100)),
            (1, 1.0, I("book", 540, 920, 380)),
            (2, 0.3, I("magnifier", 820, 1150, 220, crack=False))]),
        dict(bg="pink", lines=["Pero espera, que lo mejor viene ahora", "Cada vez que vas al baño, expulsas tantas bacterias…",
                               "…que la balanza puede ponerse *a favor de tus células*"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("toilet", 300, 820, 320)),
            (2, 0.0, I("scale", 760, 820, 420, tw={"tilt": [0.2, 1.6, 18, -12]}))]),
        dict(bg="lime", lines=["¿La respuesta? La C: más o menos *1 bacteria por cada célula*", "O sea, estás hecho *casi mitad y mitad*"],
             confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_B, 2, y=520, reveal=(0, 0.3))),
            (1, 0.0, I("cell", 330, 1110, 240)),
            (1, 0.3, I("bacteria", 760, 1110, 260))]),
        dict(bg="yellow", lines=["Así que no eres 10 veces bacteria…", "…pero tampoco *estás solo*"], items=[
            (0, 0.0, I("bacteria", 380, 760, 380)),
            (1, 0.2, M("wink", 800, 880, 240))]),
    ])

# 9 · CRISTALES DEL COCHE
OPT_V = ["Es cristal barato", "Está hecho a propósito", "Es por el frío"]
V["F09_cristal_coche"] = dict(
    title="¿Por qué la ventanilla del coche se rompe en trocitos? 🚗", question="¿Por qué se rompe en trocitos?",
    desc="La ventanilla es cristal templado: se rompe en trocitos sin filo. El parabrisas es laminado: lleva plástico dentro.",
    tags=["curiosidades", "coches", "ingeniería", "sabías que"],
    beats=[
        dict(bg="sky", lines=["¿Por qué la ventanilla del coche se rompe en *mil trocitos*…", "…y el parabrisas, en cambio, *no se cae*?"], items=[
            (0, 0.0, I("car", 540, 600, 620)),
            (0, 1.6, I("pane", 300, 1050, 300, mode="shatter", tw={"k": [None, 0.8, 0.0, 1.0]})),
            (1, 0.2, I("pane", 780, 1050, 300, mode="web", tw={"k": [None, 0.8, 0.0, 1.0]}))]),
        dict(bg="cream", q_from=True, lines=["¿Tú qué crees?", "¿Es cristal barato, está hecho así a propósito… o es por el frío?",
                                             "La respuesta, al final"], items=[
            (0, 0.0, O(OPT_V, 1, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="orange", lines=["La ventanilla es *cristal templado*", "Se calienta a unos *620 grados*…",
                                 "…y luego se enfría de golpe con chorros de aire"], items=[
            (0, 0.0, I("pane", 540, 560, 320)),
            (1, 0.0, N(0, 620, 540, 900, 170, "grados")),
            (2, 0.0, I("fan", 540, 1150, 220))]),
        dict(bg="sky", lines=["Por fuera se enfría antes que por dentro", "Así queda *apretado* por fuera y *tenso* por dentro",
                              "Y eso lo hace unas *4 veces más fuerte* que el cristal normal"], items=[
            (0, 0.0, I("pane", 540, 700, 420)),
            (1, 0.0, I("arrow", 230, 700, 180, ang=0)),
            (1, 0.0, I("arrow", 850, 700, 180, ang=180)),
            (2, 0.0, T("x4 más fuerte", 540, 1130, 80))]),
        dict(bg="lilac", lines=["Pero cuando por fin se rompe, toda esa tensión se libera *de golpe*",
                                "Y estalla en trocitos pequeños y *sin filo*", "Así es mucho más difícil cortarse"], items=[
            (0, 0.0, I("pane", 540, 760, 520, mode="shatter", tw={"k": [1.2, 2.0, 0.0, 1.0]})),
            (2, 0.2, I("check", 540, 1180, 180, float=False))]),
        dict(bg="pink", lines=["Pero espera, que el parabrisas es otra historia",
                               "Es *cristal laminado*: dos capas de cristal con una lámina de *plástico* en medio"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.2, I("layers", 440, 820, 480, tw={"spread": [0.8, 2.2, 0.0, 1.0]}))]),
        dict(bg="mint", lines=["Si se rompe, los trozos se quedan *pegados al plástico*",
                               "Por eso se agrieta como una tela de araña… *pero no se cae*"], items=[
            (0, 0.0, I("pane", 540, 760, 520, mode="web", tw={"k": [0.5, 1.5, 0.0, 1.0]}))]),
        dict(bg="lime", lines=["¿La respuesta? La B: *está hecho a propósito*", "Romperse en trocitos es su forma de *protegerte*"],
             confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_V, 1, y=520, reveal=(0, 0.3))),
            (1, 0.0, I("car", 540, 1120, 400))]),
        dict(bg="yellow", lines=["Así que si ves cristalitos en el suelo junto a un coche…",
                                 "…eran de una *ventanilla*, no del parabrisas"], items=[
            (0, 0.0, I("car", 540, 700, 600)),
            (1, 0.3, M("wink", 540, 1150, 220))]),
    ])

# 10 · VENUS
OPT_VE = ["Un día", "Un año", "Los dos igual"]
V["F10_venus"] = dict(
    title="En Venus, un día dura más que un año 🪐", question="¿Qué dura más en Venus?",
    desc="Venus tarda 243 días en girar sobre sí mismo y 225 en dar la vuelta al Sol. Y además gira al revés.",
    tags=["curiosidades", "espacio", "venus", "sabías que"],
    beats=[
        dict(bg="lilac", lines=["En Venus, un día dura *más que un año*", "Y no es una forma de hablar"], items=[
            (0, 0.0, I("venus", 540, 700, 580)),
            (1, 0.3, M("wow", 230, 1160, 210))]),
        dict(bg="cream", q_from=True, lines=["¿Qué crees que dura más en Venus?", "¿Un día, un año… o los dos lo mismo?",
                                             "Al final lo vemos"], items=[
            (0, 0.0, O(OPT_VE, 0, y=520)),
            (2, 0.0, M("think", 540, 1110, 300))]),
        dict(bg="orange", lines=["Un *año* es lo que tarda un planeta en dar la vuelta al Sol", "Venus tarda *225 días*"], items=[
            (0, 0.0, I("orbit", 540, 720, 900, center="sun", body="venus", speed=1.2, locked=False)),
            (1, 0.0, I("calendar", 830, 1170, 230, txt="225"))]),
        dict(bg="sky", lines=["Un *día* es lo que tarda en girar sobre sí mismo", "Y Venus gira tan despacio que tarda *243 días*"], items=[
            (0, 0.0, I("venus", 540, 700, 460, face=False)),
            (0, 0.4, I("curve_arrow", 540, 700, 600)),
            (1, 0.2, I("calendar", 830, 1170, 230, txt="243"))]),
        dict(bg="lime", lines=["243 días girando, contra 225 dando la vuelta al Sol", "Su día es *más largo que su año*"], items=[
            (0, 0.0, I("calendar", 300, 700, 340, txt="243", sub="días · giro")),
            (0, 0.6, I("calendar", 780, 700, 340, txt="225", sub="días · año")),
            (1, 0.2, I("scale", 540, 1120, 300, tilt=-14))]),
        dict(bg="pink", lines=["Pero espera, que es todavía más raro", "Venus gira *al revés* que la Tierra",
                               "Allí el Sol sale *por el oeste* y se pone por el este"], items=[
            (0, 0.0, M("wow", 540, 700, 340, out=(1, 0.0))),
            (1, 0.0, I("venus", 540, 660, 360, face=False)),
            (2, 0.0, T("OESTE", 230, 1100, 54)),
            (2, 0.0, T("ESTE", 850, 1100, 54)),
            (2, 0.2, I("sun", 230, 960, 160, tw={"x": [None, 3.0, 230, 850], "y": [None, 3.0, 960, 960]}))]),
        dict(bg="orange", lines=["Y además es el planeta *más caliente* del sistema solar",
                                 "Su atmósfera atrapa tanto calor que el *plomo se derretiría*", "Y sus nubes son de *ácido sulfúrico*"], items=[
            (0, 0.0, I("thermometer", 300, 720, 460, level=1.0)),
            (1, 0.0, I("drop", 780, 700, 300)),
            (2, 0.0, I("cloud", 540, 1130, 320))]),
        dict(bg="lime", lines=["¿La respuesta? La A: en Venus, *un giro dura más que un año*",
                               "Darías una vuelta entera al Sol antes de que Venus girara una sola vez"], confetti=(0, 0.4), items=[
            (0, 0.0, O(OPT_VE, 0, y=520, reveal=(0, 0.3))),
            (1, 0.2, I("venus", 540, 1120, 300))]),
        dict(bg="yellow", lines=["Así que la próxima vez que se te haga largo el día…", "…acuérdate de *Venus*"], items=[
            (0, 0.0, I("venus", 540, 720, 540)),
            (1, 0.2, M("wink", 220, 1170, 210))]),
    ])

if __name__ == "__main__":
    import sys
    only = sys.argv[1:] or list(V)
    for sid in only:
        v = V[sid]
        build(sid, v["title"], v["desc"], v["question"], v["beats"], v["tags"])
