"""Música y efectos 100 % originales, sintetizados con numpy (sin licencias de terceros)."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100


def _note(freq, dur, sr=SR):
    t = np.arange(int(dur * sr)) / sr
    # pad suave: dos senos ligeramente desafinados + armónico
    w = (np.sin(2 * np.pi * freq * t) + 0.6 * np.sin(2 * np.pi * freq * 1.003 * t)
         + 0.25 * np.sin(2 * np.pi * freq * 2 * t))
    env = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8)
    return w * np.clip(env, 0, 1)


def _lowpass(x, cutoff, sr=SR):
    b, a = butter(2, cutoff / (sr / 2), btype="low")
    return lfilter(b, a, x)


def _kick(sr=SR):
    t = np.arange(int(0.25 * sr)) / sr
    f = 110 * np.exp(-t * 18) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 14)


def _hat(rng, sr=SR):
    n = int(0.05 * sr)
    x = rng.standard_normal(n) * np.exp(-np.arange(n) / sr * 80)
    b, a = butter(2, 7000 / (sr / 2), btype="high")
    return lfilter(b, a, x)


def _whoosh(rng, sr=SR):
    n = int(0.45 * sr)
    t = np.arange(n) / sr
    x = rng.standard_normal(n)
    out = np.zeros(n)
    # barrido de filtro simple por bloques
    for i in range(0, n, 512):
        c = 400 + 5000 * (i / n)
        b, a = butter(2, c / (sr / 2), btype="low")
        out[i:i + 512] = lfilter(b, a, x[i:i + 512])
    return out * np.sin(np.pi * t / t[-1]) ** 2


def _pop(sr=SR, f0=900, f1=260, d=0.07):
    t = np.arange(int(d * sr)) / sr
    f = f1 + (f0 - f1) * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 55)


def _ding(sr=SR, f=1320, d=0.6):
    t = np.arange(int(d * sr)) / sr
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7)


def _tick(sr=SR):
    t = np.arange(int(0.05 * sr)) / sr
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 120)


def _correct(sr=SR):
    a = _ding(sr, 988, 0.35)
    b = _ding(sr, 1319, 0.6)
    out = np.zeros(int(0.12 * sr) + len(b))
    out[:len(a)] += a
    out[int(0.12 * sr):int(0.12 * sr) + len(b)] += b
    return out


def _wrong(sr=SR):
    t = np.arange(int(0.45 * sr)) / sr
    w = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.5 + np.sin(2 * np.pi * 147 * t) * 0.5
    return _lowpass(w, 1200) * np.exp(-t * 4)


def _boom(sr=SR):
    t = np.arange(int(0.5 * sr)) / sr
    f = 40 + 120 * np.exp(-t * 14)
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 6)


def _notif(sr=SR):
    """Aviso de notificación original: dos notas tipo cristal/marimba (no es el sonido de Apple)."""
    out = np.zeros(int(0.7 * sr))
    for k, (f, t0) in enumerate(((1568.0, 0.0), (2093.0, 0.11))):
        t = np.arange(int(0.55 * sr)) / sr
        w = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 30)) * np.exp(-t * 9)
        i = int(t0 * sr)
        out[i:i + len(w)] += w[: len(out) - i]
    return out


def build_track(duration, cues, path, seed=7, bpm=100, sfx=None, sfx_gain=1.0, music_gain=1.0):
    """duration en s; cues = instantes de whoosh; sfx = [(t, tipo)] con tipo pop|ding|tick|correct|wrong|boom."""
    rng = np.random.default_rng(seed)
    n = int(duration * SR) + SR
    mix = np.zeros(n)
    # progresión Am - F - C - G, 2 compases por acorde aprox.
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63],
              [130.81, 196.0, 261.63], [196.0, 246.94, 293.66]]
    seg = 4 * 60 / bpm * 1  # 1 compás
    t0, k = 0.0, 0
    while t0 < duration:
        for f in chords[k % 4]:
            s = _note(f, seg * 2 + 0.8)
            i = int(t0 * SR)
            mix[i:i + len(s)] += 0.12 * s[: max(0, n - i)]
        t0 += seg * 2
        k += 1
    mix = _lowpass(mix, 1800)
    # ritmo suave que entra tras el gancho
    beat = 60 / bpm
    kick, t = _kick(), 2.0
    while t < duration - 0.5:
        i = int(t * SR)
        mix[i:i + len(kick)] += 0.35 * kick[: n - i]
        h = _hat(rng)
        j = int((t + beat / 2) * SR)
        mix[j:j + len(h)] += 0.05 * h[: max(0, n - j)]
        t += beat
    for c in cues:
        w = _whoosh(rng)
        i = int(max(0, c - 0.3) * SR)
        mix[i:i + len(w)] += 0.10 * w[: max(0, n - i)]
    mix *= music_gain
    gens = {"pop": (_pop, 0.22), "ding": (_ding, 0.16), "tick": (_tick, 0.25), "correct": (_correct, 0.3),
            "wrong": (_wrong, 0.3), "boom": (_boom, 0.45), "notif": (_notif, 0.4)}
    for tt, kind in (sfx or []):
        g, gain = gens[kind]
        w = g()
        i = int(max(0, tt) * SR)
        if i < n:
            mix[i:i + len(w)] += gain * sfx_gain * w[: n - i]
    mix = mix[: int(duration * SR)]
    fade = int(1.2 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= np.max(np.abs(mix)) + 1e-9
    stereo = np.stack([mix, np.roll(mix, 220)], axis=1) * 0.8
    wavfile.write(path, SR, (stereo * 32767).astype(np.int16))
    return path
