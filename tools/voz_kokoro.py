"""Voz del narrador con Kokoro (gratis, ilimitada, local). Voz elegida por Iker el 28/10: em_alex.
Uso:
  python3 tools/voz_kokoro.py <modulo_en_content/cine>            → content/cine/voz/<voz del módulo>.mp3 + _words.json
  python3 tools/voz_kokoro.py --texto "<guion>" <salida.mp3>        → mp3 + _words.json (tiempos por pausas)
Modelo en /home/claude/tts (lo descarga setup.sh desde GitHub).
"""
import sys, os, re, subprocess, importlib, json

ROOT = "/home/claude/shorts-ingenieria"
TTS = "/home/claude/tts"
VOZ = {"em_alex": 0.75, "am_fenrir": 0.25}   # «Alex 5 · enérgico», elegida por Iker el 28/10
SPEED = float(os.environ.get("VOZ_SPEED", "1.0"))
sys.path[:0] = [ROOT + "/content/cine", ROOT + "/pipeline", ROOT + "/tools"]

# lo que Kokoro lee mal escrito en abreviatura
REPL = [(r"\bkm/h\b", "kilómetros por hora"), (r"\bF1\b", "Fórmula 1"), (r"\b11-S\b", "once ese"), (r"\bLZB\b", "ele zeta be"), (r"\bAVE\b", "Ave"),
        (r"–", " a "), (r"→", " a "), (r"«|»", ""), (r"\*", "")]


def para_voz(t):
    for a, b in REPL:
        t = re.sub(a, b, t)
    return t


def sintetiza(texto, mp3):
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro(os.path.join(TTS, "kokoro-v1.0.onnx"), os.path.join(TTS, "voices-v1.0.bin"))
    st = sum(k.get_voice_style(n) * w for n, w in VOZ.items())
    a, sr = k.create(para_voz(texto), voice=st, speed=SPEED, lang="es")
    wav = mp3[:-4] + ".wav"
    sf.write(wav, a, sr)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "160k", mp3], check=True)
    os.remove(wav)


def tiempos(texto_guion, mp3):
    import align_local
    words, used, S = align_local.align(texto_guion, mp3)
    out = os.path.splitext(mp3)[0] + "_words.json"
    json.dump({"words": words, "source": "kokoro+align_local"}, open(out, "w"), ensure_ascii=False, indent=0)
    print(mp3, "·", len(words), "palabras ·", used, "/", S, "pausas · fin", words[-1]["end"])


if __name__ == "__main__":
    if sys.argv[1] == "--texto":
        txt, mp3 = sys.argv[2], sys.argv[3]
    else:
        m = importlib.import_module(sys.argv[1])
        txt = " ".join(l.replace("*", "") for l in m.LINES) + " " + m.OUTRO_LINE
        mp3 = m.VOICE
    sintetiza(txt, mp3)
    tiempos(txt.replace("*", ""), mp3)
