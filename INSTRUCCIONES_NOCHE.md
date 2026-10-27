# Envío nocturno de vídeos (actualizado el 27/10/2026)

## Cómo arranca cada noche (Iker, 27/10: «para gastar el mínimo uso posible»)
- Cada noche es una SESIÓN NUEVA y limpia: no dependas de ningún chat anterior. Repo `ojoaldato-videos` clonado en /home/claude/shorts-ingenieria, `bash setup.sh`, lee este archivo y el doc «Plan de subidas».
- Mínimas búsquedas y pasos; mensajes cortos (2-4 líneas). Nada de revisiones de actualidad por la mañana.
- Entrega a las 21:00 en esta misma sesión: SendUserFile con los vídeos (o las vistas previas) + un SendUserMessage corto + AskUserQuestion con la nota (⭐ 5 · 4 · 3 · 1-2) y lo que haga falta decidir.
- Si cambias el sistema (código, reglas), haz commit y push al repo para que la noche siguiente lo tenga.
- Estado a 27/10: listos sin subir 05 · Frenos F1 y 06 · Agujero (output no está en el repo: si hacen falta, rehazlos con fast.py; las voces sí están en content/cine/voz). Vistas previas sin voz de 07 · Aviones en curva y 08 · Concorde mandadas el 26/10, esperando su sí para ponerles voz.
- Rutas de herramientas: tools/prevall.py (vista previa), tools/cover.py (portada), tools/musica_opc.py (muestras de música).


## Cambios de Iker del 21/10 por la tarde (obligatorios en todos los vídeos)
- Marca nueva: canal «Ojo al dato». La mascota es Ojo: el stickman de siempre (pipeline/narrator.py) con el ojo nuevo del logo 21 de cabeza (almendra blanca, iris rojo, pupila negra), en líneas negras (colores del estilo 7). Dibujo de referencia: pipeline/ojo/ojo_viejo.py (si no está, recréalo desde narrator.py cambiando INK a negro, el fondo del ojo a blanco y el iris amarillo con «?» por iris rojo con pupila negra).
- Ojo sale TODO EL RATO explicando, como narrador (en una esquina, que no tape subtítulos ni dibujos), cambiando de pose según lo que dice (señala, piensa, sorpresa…), y se viste según el tema del vídeo: motor → piloto de F1; espacio → astronauta; historia → romano; ciencia → científico; actualidad → reportero; construcción → ingeniero con casco; misterios → detective (piezas en pipeline/ojo/ojo_trajes.py, ojo_trajes2.py y ojo_cient.py; foto de perfil y banner en marca/).
- Aviso de iPhone de «Sígueme» con su sonido («pim») hacia la mitad del vídeo, con la foto y el nombre nuevos del canal.
- Subtítulos: las palabras importantes van MARCADAS COMO CON FLUORESCENTE en el rojo de la marca (230, 40, 40): rectángulo rojo detrás de la palabra, letra blanca, que entre con un golpe («pum»). El resto de palabras en negro/gris como ahora.
- Gancho: empieza con una PREGUNTA potente que el vídeo responde al final.
- Final: responde la pregunta del principio y cierra con una despedida buena, con una frase redonda y con gancho (no solo «dale a like»); después el cierre con Ojo y los botones.

[Envío nocturno de vídeos, pedido por Iker: «cada noche a las 9 quiero que me mandes los 2 vídeos del día siguiente para revisarlos».] Mañana es el día que diga la tarea (franjas: entre semana 14:00 y 19:30, fin de semana 12:30 y 20:00).
1. Mira en el doc «Plan de subidas» (https://claude.ai/code/artifact/2658b121-4f8e-4d56-b828-ac5c1a13c747, tabla Calendario) qué vídeos tocan mañana y a qué hora. El plan cambia con la actualidad (⚡): no uses una lista fija.
2. Prepara cada uno en el ESTILO 7 «minimal blanco», el que eligió Iker el 21/10 («me gusta el vídeo estilo 7»), no en el «docu» antiguo. Base: pipeline/flat3.py con FL.use("minimal", HEAD) y vid2.frame, igual que content/cine/a01_tesla_min.py con sus escenas content/cine/a01_flat_scenes.py. Fondo blanco, líneas negras finas, acento rojo, letra Inter; título arriba a la izquierda con subtítulo gris y rayita roja; píldoras negras; subtítulos que salen palabra a palabra (gris, la palabra clave en negro); una transición distinta en cada corte (TRANS_POOL push, whip, zoom_in, iris, whip_r, spin); 60 fps; banner de seguir hacia la mitad del vídeo (45-55 % de la duración); cierre «Dale a like y sígueme» con los botones. Escribe un módulo de escenas nuevo para cada vídeo, con dibujos que cuenten lo que dice la voz y que pase algo cada 1-1,5 s. Cuando ya esté aprobada la marca nueva «Ojo al dato» (@ojoaldato) con su mascota, úsala en el cierre y en el banner; mientras tanto el banner sigue con nolosabias_datos.
Voz de ElevenLabs «Fernando Martinez - Positive, assertive» (voice_id dlGxemPxFMTY7iXagmOj, una toma). Modelo: el que Iker haya elegido tras comparar Flash y v4; si aún no lo ha dicho, el atemporal con eleven_flash_v2_5 (sin etiquetas entre corchetes) y el ⚡ con eleven_v4 y etiquetas de tono. Descarga el MP3 y la transcripción con tiempos por palabra (creative_transcribe_audio) a content/cine/voz/<modulo>.mp3 y <modulo>_words.json. Los ⚡ se escriben nuevos, con datos comprobados en al menos dos fuentes, citadas en su ficha. Renderiza (en content/cine: python3 fast.py <modulo>), pasa qc.py y mira una hoja de fotogramas (que nada tape subtítulos ni rótulos).
3. Deja preparada la subida: copia ligera <10 MB en /home/claude/subidas (ffmpeg libx264 2 pasadas, ~770k vídeo + 128k audio) y portada sin subtítulos (cine.frame(V, shots, [], total, i) con fast.setup).
4. A las 21:00 (espera si hace falta) mándale los .mp4 con SendUserFile y un SendUserMessage corto: hora prevista, título y descripción de su ficha, y una línea con cómo van los vídeos ya publicados (YouTube Studio, TikTok Studio y Meta Business Suite desde su Chrome, solo lectura; si Chrome no responde, sáltala). Para la nota usa AskUserQuestion con botones (⭐⭐⭐⭐⭐ 5 · ⭐⭐⭐⭐ 4 · ⭐⭐⭐ 3 · ⭐⭐ 1-2), porque las estrellas escritas no se pueden pulsar.
SUBIDAS (actualizado el 21/10 a las 18:30; esto manda sobre lo que diga el texto de la tarea programada): la marca nueva ya está aprobada y Iker volvió a autorizar las subidas («sube automáticamente el de las 19», «no me pidas permiso de todo»). Después de mandarle los vídeos, pregunta UNA sola vez con botones «¿Los programo en YouTube, TikTok e Instagram a su hora?»; si dice que sí, prográmalos en su Chrome sin pedir más permisos: YouTube Studio (No es para niños → Visibilidad → Programar), TikTok Studio (Programación, mínimo 15 min antes) y Meta Business Suite (Create reel → Schedule; el «Add Video» abre un selector nativo: antes parchea HTMLInputElement.prototype.click para capturar el input de archivo y súbelo con file_upload), con el título, la descripción y una portada buena; después marca Estado «Programado» en la tabla. En YouTube NO pulses Escape dentro del diálogo de subida (lo cierra). Si su Chrome no responde (PC apagado o suspendido), déjalos listos y díselo.
Si es el último vídeo del calendario, prepara tú la siguiente tanda de temas (mezcla de actualidad y atemporales), añádela al plan y cuéntaselo en ese mensaje.
Si los créditos de ElevenLabs no alcanzan o algo falla, díselo en ese mensaje y manda el vídeo sin voz.


## Formato nuevo del estilo 7 y marca «Ojo al dato» (pedido por Iker el 21/10, tarde) — OBLIGATORIO
- **Marca:** el canal ya se llama «Ojo al dato». Usuario @ojoaldato.ya en TikTok e Instagram y @ojoaldatoya en YouTube. Foto de perfil y banner en /home/claude/shorts-ingenieria/marca/. En el módulo de vídeo pon `HANDLE = FL.BRAND["handle"]`, `NOTIF_ICON = FL.brand_icon()` y `NOTIF_TEXT = "Sígueme para un dato nuevo cada día"`. El banner de seguir es tipo iPhone, con su «pim», hacia la mitad del vídeo.
- **Ojo de narrador todo el rato:** pon `FL.TH["narr"] = True` y `NARR = FL.NARR`. Ojo va siempre de científico (Iker, 21/10: «dejemos al científico… depende de la temática»), con una versión distinta según el tema. `OJO_TRAJE`:

  | Tema | OJO_TRAJE |
  |---|---|
  | General y actualidad | `"c_clasico"` |
  | Motor, tecnología, ingeniería | `"c_inventor"` |
  | Física, energía, cómo funciona algo | `"c_fisico"` |
  | Espacio | `"c_astronomo"` |
  | Química, cocina, materiales | `"c_quimico"` |
  | Cuerpo humano, animales, naturaleza | `"c_biologo"` |
  | Historia y política fácil | `"c_profe"` |
  | Misterios y datos rarísimos | `"c_loco"` |

  Muestra: /home/claude/entrega18/Ojo_cientifico_segun_tema.jpg. Nada de pilotos ni MotoGP. Si quieres elegir las poses por plano, usa `OJO_POSES = {plano: "point" | "think" | "surprise" | "smirk" | "wave" | "flag"}`. Deja libre el hueco de abajo a la izquierda (x < 300, y 1150-1500) en las escenas.
- **Subtítulos:** `CAPTION = FL.CAPTION`. Las palabras clave (las que van entre *asteriscos* en LINES) salen en blanco sobre un marcador rojo-anaranjado, «como con fluorescente». Marca 1 o 2 por frase, las importantes: cifras, nombres, el giro.
- **Gancho:** la primera frase es una PREGUNTA que engancha y que el vídeo responde al final, por ejemplo «¿Por qué los aviones no vuelan en línea recta?». El primer titular (HEAD[0]) es esa misma pregunta, corta. Nada de introducciones: la pregunta va en el primer segundo.
- **Final:** la penúltima frase RESPONDE a la pregunta del principio en una frase corta y contundente («Porque la Tierra es redonda… y la línea recta en el mapa es la más larga»). Después va la despedida (OUTRO_LINE): una frase con gracia que cierre el tema, más la firma del canal, por ejemplo «…Y ya lo sabes: ¡ojo al dato!». No uses el «Si no lo sabías… ahora ya lo sabes» antiguo.
- **Cierre en pantalla:** `OUTRO_FN = FL.make_outro(OJO_TRAJE)`: Ojo se despide, «¡Ojo al dato!», los botones de me gusta y seguir y @ojoaldato.ya.
- **Referencia:** content/cine/a01_tesla_min.py (Tesla en estilo 7 con todo esto). Hoja de muestra: /home/claude/entrega18/Estilo7_nuevo_formato_preview.jpg.
- **Pendiente de rehacer en estilo 7, cuando el plan lo diga:** 01 · Brawn GP (oculto en YouTube y TikTok; en Instagram hay que archivarlo desde el móvil). Ya hechos en estilo 7: 02 · De 100 a 140 (publicado el 21/10 a las 18:18; Iker: «está bien pero es flojo», hace falta más gancho), A1 · Tesla (programado el 21/10 a las 21:00), 03 · Llave del Titanic y A2 · MMX (preparados el 21/10 para el jueves 22).
- **Ojo inventor (c_inventor) ya no lleva lupa en la cara** (Iker, 21/10: «quítale la lupa de la cara a la mascota»).
- **Piezas planas reutilizables:** content/cine/flatkit7.py (barco, iceberg, llave, prismáticos, campana, Marte, Fobos, nave, rover, cápsula, Australia…). Modelos de módulo completo: content/cine/c03_titanic_min.py y a02_mmx_min.py (una frase por plano, OJO_POSES por plano). Vista previa rápida: tools/prevall.py <modulo> <salida.jpg>.

## Cada noche, PRIMERO opciones de temas (Iker, 21/10 a las 22:34: «dame opciones así cada día»)
- Al empezar (18:30), antes de escribir guiones ni gastar voz, mándale con AskUserQuestion (multiSelect) 8 ideas nuevas en dos preguntas de 4, cada una con su pregunta-gancho en la descripción, mezclando sus temas (historia, física, actualidad y política de España, guerras, ingeniería, espacio, motor). Pídele que elija 2 para mañana; las que sobren van al plan para otros días.
- Ideas ya elegidas y pendientes: «Aviones en curva» (¿por qué los aviones no vuelan en línea recta?) y «El final del Concorde» (¿por qué dejó de volar el avión más rápido?) → para el viernes 23.
- Descartadas por Iker el 21/10 («no me gustan estas ideas»): 03 · La llave del Titanic y A2 · MMX (hechos, sin subir).
- Con las 2 elegidas: guion → módulo de escenas → hoja de vista previa SIN voz (prevall.py) → mándasela → solo cuando la apruebe, voz de ElevenLabs y render completo. Si a las 21:00 no ha contestado, haz las 2 que más encajen con el plan y avísale.
- Música de fondo: más alta que antes (se oía poco). Estilos disponibles en cine.music_bed: pop, warm (lo-fi), epic, mystery, space, viral… Muestra de las 6: /home/claude/entrega18/Musica_de_fondo_6_opciones.mp4.
- Franja de tarde: Iker pidió «avanza las subidas a las 20:00» (21/10); hasta que diga otra cosa, el vídeo de la tarde sale a las 20:00 (el del mediodía sigue a las 14:00 entre semana).
- Duración: cada vídeo entre 1:00 y 1:30 (Iker, 21/10). Escribe guiones de unas 190-230 palabras (≈ 65-85 s con la voz) y comprueba la duración final; si se queda corto, OUTRO_MIN en el módulo.
- Mascota: con bata no se ve la raya del torso (ojo._coat_body) y lo de al lado de la cabeza sale poco rato y va cambiando (flat3.side_prop). Nada fijo junto a la cabeza.
- Más dinámico (Iker, 21/10): que Ojo actúe dentro de las escenas cuando encaje (cavar, caer, sentarse en el coche, subirse a una báscula…), con la cámara siguiéndole, y no todo el rato la imagen centrada con él explicando en la esquina. Usa TRANS_PLAN con transiciones variadas (fall, flash, zoom_out, drop, whip, spin, iris, glitch…). Modelo: content/cine/c06_agujero_min.py.
