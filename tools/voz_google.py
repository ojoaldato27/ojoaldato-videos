"""Voz de Google Cloud (Chirp 3 HD) — elegida por Iker el 06/11/2026: «Joven C · Umbriel» (es-ES-Chirp3-HD-Umbriel, 1,12).
Gratis hasta 1 millón de caracteres al mes (usamos <10 %). Frase a frase, igual que voz_natural.py, para que los
tiempos por palabra salgan exactos por frase. La clave NO va en el repo (es público): se lee de /home/claude/.gtts_key
o de la variable GTTS_KEY. Si la sesión no la tiene, pídesela a Iker (Google Cloud → proyecto ojoaldato → Credenciales).
También hace falta el dominio texttospeech.googleapis.com permitido en claude.ai → Ajustes → Capacidades.
Uso: python3 tools/voz_google.py <modulo>        → VOICE del módulo (.mp3) + _words.json
     python3 tools/voz_google.py --texto "<t>" <salida.mp3>
Variables: GVOZ (Umbriel), GVOZ_SPEED (1.12)
GUION PARA ESTA VOZ: frases cortas y habladas; sin «…» ni comas en medio de la idea (Google hace ahí pausas raras);
una coma solo donde una persona respiraría.
"""
import sys, os, json, base64, subprocess, importlib, urllib.request, io
import numpy as np
import soundfile as sf

ROOT = "/home/claude/shorts-ingenieria"
sys.path[:0] = [ROOT + "/tools", ROOT + "/content/cine", ROOT + "/pipeline"]
from voz_natural import frases, recorta, spoken_len   # noqa: E402

FS = 24000


def clave():
    k = os.environ.get("GTTS_KEY")
    if not k and os.path.exists("/home/claude/.gtts_key"):
        k = open("/home/claude/.gtts_key").read().strip()
    if not k:
        raise SystemExit("Falta la clave de Google TTS (GTTS_KEY o /home/claude/.gtts_key)")
    return k


def sintetiza(texto, voz, vel):
    body = {"input": {"text": texto}, "voice": {"languageCode": "es-ES", "name": f"es-ES-Chirp3-HD-{voz}"},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": FS, "speakingRate": vel}}
    r = urllib.request.Request(f"https://texttospeech.googleapis.com/v1/text:synthesize?key={clave()}",
                               json.dumps(body).encode(), {"Content-Type": "application/json"})
    wav = base64.b64decode(json.load(urllib.request.urlopen(r, timeout=60))["audioContent"])
    a, fs = sf.read(io.BytesIO(wav), dtype="float32")
    return a if a.ndim == 1 else a.mean(axis=1)


def genera(texto, out, voz=None, vel=None):
    """texto: str (se parte en frases) o lista de líneas (cada línea se lee ENTERA de una vez: entonación y pausas
    naturales; Iker 06/11: «hace pausas raras y las comas mal» al pegar trozos)."""
    voz = voz or os.environ.get("GVOZ", "Umbriel")
    vel = vel or float(os.environ.get("GVOZ_SPEED", "1.12"))
    partes, words, t = [np.zeros(int(FS * 0.12), np.float32)], [], 0.12
    for s in (texto if isinstance(texto, list) else frases(texto)):
        tipo = s[-1] if s[-1] in "?!." else "."
        a = recorta(sintetiza(s.replace("*", ""), voz, vel), FS)
        dur = len(a) / FS
        toks = s.replace("*", "").split()
        L = [spoken_len(w) for w in toks]
        tot, acc = sum(L), 0.0
        for w, l in zip(toks, L):
            ws = t + dur * acc / tot
            acc += l
            words.append({"text": w, "type": "word", "start": round(ws, 3), "end": round(t + dur * acc / tot, 3)})
        gap = {"?": 0.38, "!": 0.3}.get(tipo, 0.26)
        partes += [a, np.zeros(int(FS * gap), np.float32)]
        t += dur + gap
    y = np.concatenate(partes)
    wav = out[:-4] + ".wav"
    sf.write(wav, y, FS)
    af = "highpass=f=70,acompressor=threshold=-22dB:ratio=2:attack=10:release=150,loudnorm=I=-16:TP=-1.5"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-af", af, "-b:a", "160k", out], check=True)
    os.remove(wav)
    json.dump({"words": words, "source": f"google-chirp3-{voz}"}, open(out[:-4] + "_words.json", "w"), ensure_ascii=False, indent=0)
    n = sum(len(x.replace("*", "")) for x in (texto if isinstance(texto, list) else frases(texto)))
    print(out, len(words), "palabras · fin", words[-1]["end"], f"· CARACTERES GASTADOS: {n} (súmalos en el doc del proyecto claude/voz-consumo.md)")
    return out


if __name__ == "__main__":
    if sys.argv[1] == "--texto":
        genera(sys.argv[2], sys.argv[3])
    else:
        m = importlib.import_module(sys.argv[1])
        genera(list(m.LINES) + [m.OUTRO_LINE], m.VOICE)
