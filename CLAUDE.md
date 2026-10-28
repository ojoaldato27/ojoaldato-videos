# Ojo al dato · sistema de vídeos

Shorts de curiosidades del canal «Ojo al dato» (Iker). Todo se renderiza aquí con Python (PIL + numpy + scipy) y ffmpeg.

- **Ruta obligatoria:** clona el repo en `/home/claude/shorts-ingenieria` (el código usa rutas absolutas desde ahí).
- **Preparar la sesión:** `bash setup.sh`.
- **Qué hacer cada noche:** lee entero `INSTRUCCIONES_NOCHE.md` y síguelo. Plan y fichas: doc «Plan de subidas» (https://claude.ai/artifact/SieCw4wUBgcTDj2ETj9LPy).
- **Vista previa sin voz:** `cd content/cine && python3 ../../tools/prevall.py <modulo> /tmp/prev.jpg 0.65`.
- **Render completo:** `cd content/cine && python3 fast.py <modulo>` → `output/cine/<TITLE>.mp4`; control: `python3 qc.py <mp4>`.
- **Portada:** `python3 ../../tools/cover.py <modulo> q 2.0 <salida.jpg>`.
- **Módulos de referencia (estilo 7):** `content/cine/c06_agujero_min.py` (Ojo actuando, cámara, TRANS_PLAN), `c05_frenos_min.py`, `c07_aviones_min.py`, `c08_concorde_min.py`. Piezas planas: `content/cine/flatkit7.py`. Marca, narrador, subtítulos y cierre: `pipeline/flat3.py`; mascota: `pipeline/ojo.py`.
- **Voz:** ElevenLabs (conector), voz Fernando `dlGxemPxFMTY7iXagmOj` (Iker volvió a ella el 28/10; Álvaro ya no se usa), una toma; MP3 y `_words.json` en `content/cine/voz/`.
- **Música (Iker, 27/10):** alterna synthwave, lofi_hh, premium, playful y exp (una distinta por vídeo); ver INSTRUCCIONES_NOCHE.md.
- **Guardar siempre en el repo:** voz y copia ligera de cada vídeo en cuanto existan (commit + push).
- **Ahorro de uso (Iker, 27/10):** mínimas búsquedas y pasos, mensajes cortos. Nunca guardes claves ni contraseñas en el repo.
