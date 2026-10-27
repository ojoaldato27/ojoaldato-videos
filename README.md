# Ingeniería en 30 s — sistema de producción de Shorts

## Arquitectura (v1)

```
temas.md ──► guion JSON ──► music.py ──► render.py ──► run.py (QC) ──► output/<id>/
 (ideas y      (gancho,      (música y     (animación      (resolución,     ├ <id>.mp4
  puntuación)   escenas,      efectos       9:16 + texto    fps, duración,   ├ miniatura.jpg
                subtítulos,   originales)   sincronizado)   volumen -14     ├ metadatos.txt
                metadatos,                                  LUFS, ritmo de   └ qc.json
                derechos)                                   subtítulos,
                                                            derechos)    ──► registro.csv
```

- **Todo es original:** animaciones dibujadas con código, música sintetizada con numpy y tipografía Inter (licencia OFL, uso comercial permitido). No hay material de terceros.
- **Control de calidad automático (`run.py`):** 1080×1920, 30 fps, 10-60 s, audio a -14 LUFS, gancho visible en los primeros 0,3 s, subtítulos sin solaparse y a ≤ 20 caracteres/s, título ≤ 100 caracteres y todos los recursos con licencia.
- **Registro (`registro.csv`):** una fila por vídeo, con estado, fecha de publicación, URL y métricas a las 48 h para mejorar los siguientes.

## Cómo se hace un vídeo nuevo

1. Elegir un tema de `content/temas.md`.
2. Escribir `content/scripts/<id>.json` con las escenas, los subtítulos, los metadatos y los derechos.
3. `python3 pipeline/run.py content/scripts/<id>.json`
4. Si el tema necesita un diagrama nuevo, se añade una función `sc_*` en `render.py`. Cada tema nuevo suele necesitar una, y eso es lo que evita que el canal parezca "producido en masa".

## Límites actuales (comprobados)

- Este entorno **no puede acceder a la API de YouTube**: la red lo bloquea. La subida va por YouTube Studio (programación nativa y gratis) o por un conector como Metricool.
- **No hay motor de voz** disponible ni instalable aquí. La v1 es texto animado + música. La voz se puede añadir con ElevenLabs (de pago) si se conecta.
