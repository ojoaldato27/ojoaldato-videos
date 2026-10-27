"""Seis identidades musicales originales + efectos sonoros, todo sintetizado (sin licencias de terceros).
Cada pista deja hueco a la voz: banda media atenuada, sin melodía en primer plano y con 'ducking' en las revelaciones."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
A_MIN = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [130.81, 196.0, 261.63], [196.0, 246.94, 293.66]]


def lp(x, c, o=2):
    b, a = butter(o, min(c, SR / 2 - 100) / (SR / 2), btype="low")
    return lfilter(b, a, x)


def hp(x, c, o=2):
    b, a = butter(o, c / (SR / 2), btype="high")
    return lfilter(b, a, x)


def tt(d):
    return np.arange(int(d * SR)) / SR


def env_ad(n, att, rel):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(att, 1e-4)) * np.exp(-t / max(rel, 1e-4))


def add(buf, sig, t0, g=1.0):
    i = int(max(0, t0) * SR)
    if i >= len(buf):
        return
    m = min(len(sig), len(buf) - i)
    buf[i:i + m] += g * sig[:m]


# ---------- instrumentos ----------
def pad(f, d, bright=1.0):
    t = tt(d)
    w = sum(np.sin(2 * np.pi * f * k * (1 + 0.002 * j) * t) / k ** (1.6 / bright) for k in (1, 2, 3) for j in (-1, 1))
    e = np.minimum(1, t / 0.9) * np.minimum(1, (d - t) / 0.9)
    return w * np.clip(e, 0, 1) * 0.25


def strings(f, d):
    t = tt(d)
    saw = sum(np.sin(2 * np.pi * f * k * t + 0.3 * np.sin(2 * np.pi * 5 * t)) / k for k in range(1, 8))
    e = np.minimum(1, t / 1.8) * np.minimum(1, (d - t) / 1.5)
    return lp(saw * np.clip(e, 0, 1), 1400) * 0.18


def kick(d=0.32, f0=120, f1=42, decay=11):
    t = tt(d)
    f = f1 + (f0 - f1) * np.exp(-t * 22)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)


def snare(rng, d=0.22):
    t = tt(d)
    n = hp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 22)
    return 0.6 * n + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)


def hat(rng, d=0.05):
    t = tt(d)
    return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 90)


def pluck(f, d=0.5, decay=9):
    t = tt(d)
    w = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 40)
    return w * np.exp(-t * decay)


def rhodes(f, d):
    t = tt(d)
    w = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t)) * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * t))
    return w * np.exp(-t * 1.2) * np.minimum(1, t / 0.01)


def sq(f, d, decay=12):
    t = tt(d)
    w = np.sign(np.sin(2 * np.pi * f * t))
    return lp(w, 2400) * np.exp(-t * decay)


# ---------- efectos ----------
def fx_whoosh(rng, d=0.45, up=True):
    n = int(d * SR)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    for i in range(0, n, 512):
        c = 300 + 6000 * ((i / n) if up else (1 - i / n))
        out[i:i + 512] = lp(x[i:i + 512], c)
    t = np.arange(n) / SR
    return out * np.sin(np.pi * t / t[-1]) ** 2


def fx_riser(rng, d=0.9):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n)
    for i in range(0, n, 512):
        out[i:i + 512] = lp(x[i:i + 512], 400 + 7000 * (i / n) ** 2)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 800 * (t / d) ** 2) / SR) * 0.3
    return (out * 0.7 + tone) * (t / d) ** 2


def fx_impact(rng):
    t = tt(0.9)
    b = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t * 12)) / SR) * np.exp(-t * 4)
    n = lp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 14) * 0.5
    return b + n


def fx_pop(f0=950, f1=280):
    t = tt(0.07)
    return np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * 60)) / SR) * np.exp(-t * 55)


def fx_ding(f=1320):
    t = tt(0.6)
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.01 * t)) * np.exp(-t * 7)


def fx_click():
    t = tt(0.03)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 200)


def fx_heart():
    out = np.zeros(int(0.6 * SR))
    k = kick(0.25, 70, 38, 16)
    add(out, k, 0)
    add(out, k * 0.7, 0.18)
    return lp(out, 300)


def fx_glitch(rng):
    n = int(0.18 * SR)
    x = rng.standard_normal(n)
    x = np.round(x * 3) / 3
    t = np.arange(n) / SR
    gate = (np.sin(2 * np.pi * 37 * t) > 0).astype(float)
    return hp(x, 800) * gate * np.exp(-t * 10) * 0.6


def fx_swell(rng, d=1.4):
    t = tt(d)
    w = sum(np.sin(2 * np.pi * f * t) for f in (110, 165, 220.5)) / 3
    return lp(w + 0.2 * rng.standard_normal(len(t)), 900) * (t / d) ** 1.5 * np.exp(-np.maximum(0, t - d * 0.85) * 12)


def fx_paper(rng):
    t = tt(0.25)
    return hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 18) * (1 + np.sin(2 * np.pi * 30 * t)) * 0.4


def fx_notif():
    out = np.zeros(int(0.7 * SR))
    for f, t0 in ((1568.0, 0.0), (2093.0, 0.11)):
        t = tt(0.55)
        add(out, (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 30)) * np.exp(-t * 9), t0)
    return out


# ---------- pistas ----------
def chords_loop(dur, bar, fn, gain):
    buf = np.zeros(int((dur + 2) * SR))
    t0, k = 0.0, 0
    while t0 < dur:
        for f in A_MIN[k % 4]:
            add(buf, fn(f, bar * 2 + 0.8), t0, gain)
        t0 += bar * 2
        k += 1
    return buf


def track(style, dur, rng):
    n = int((dur + 2) * SR)
    m = np.zeros(n)
    if style == "viral":
        bpm = 124
        beat = 60 / bpm
        m += lp(chords_loop(dur, 4 * beat, pad, 0.5), 2200)
        t = 1.0
        i = 0
        while t < dur:
            add(m, kick(), t, 0.55)
            if i % 2 == 1:
                add(m, snare(rng), t, 0.25)
            add(m, hat(rng), t + beat / 2, 0.1)
            t += beat
            i += 1
        # bajo
        t, k = 0.0, 0
        while t < dur:
            f = A_MIN[(k // 8) % 4][0] / 2
            add(m, lp(sq(f, beat * 0.9, 6), 400), t, 0.18)
            t += beat / 2
            k += 1
    elif style == "doc":
        bar = 60 / 70 * 4
        m += chords_loop(dur, bar, lambda f, d: strings(f / 2, d) + pad(f, d, 0.6), 0.9)
        t = 0.0
        while t < dur:
            add(m, pluck(880 * (2 ** (rng.integers(0, 5) / 12)), 2.0, 2.2), t + 2.0, 0.035)
            t += bar
    elif style == "mystery":
        t = tt(dur + 2)
        drone = np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 55.4 * t) + 0.25 * np.sin(2 * np.pi * 82.6 * t)
        m += lp(drone, 300) * 0.35 * (0.8 + 0.2 * np.sin(2 * np.pi * 0.07 * t))
        eerie = np.sin(2 * np.pi * (1244 + 6 * np.sin(2 * np.pi * 0.3 * t)) * t) * 0.02 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t))
        m += eerie
        tb = 0.5
        while tb < dur:
            add(m, fx_heart(), tb, 0.45)
            tb += 1.15
    elif style == "creative":
        bpm = 110
        beat = 60 / bpm
        m += lp(chords_loop(dur, 4 * beat, pad, 0.25), 1500)
        arp = [0, 4, 7, 12, 7, 4]
        t, k = 0.5, 0
        while t < dur:
            base = A_MIN[(k // 16) % 4][0] * 2
            add(m, pluck(base * 2 ** (arp[k % 6] / 12), 0.4, 11), t, 0.07)
            if k % 4 == 0:
                add(m, kick(0.25, 100, 50, 14), t, 0.35)
            if k % 8 == 4:
                add(m, snare(rng, 0.12), t, 0.15)
            t += beat / 2
            k += 1
    elif style == "premium":
        bpm = 90
        beat = 60 / bpm
        m += chords_loop(dur, 4 * beat, lambda f, d: rhodes(f, d), 0.35)
        t, i = 1.0, 0
        while t < dur:
            if i % 4 in (0, 2) or (i % 8 == 7):
                add(m, kick(0.3, 90, 45, 10), t, 0.4)
            if i % 4 in (1, 3):
                add(m, lp(snare(rng), 3000), t, 0.16)
            add(m, hat(rng, 0.03), t + beat / 2, 0.05)
            t += beat
            i += 1
        m = lp(m, 3500)
    elif style == "exp":
        bpm = 128
        beat = 60 / bpm
        t, k = 0.0, 0
        notes = [0, 12, 7, 3, 10, 7, 15, 12]
        while t < dur:
            base = A_MIN[(k // 32) % 4][0]
            add(m, sq(base * 2 ** (notes[k % 8] / 12), beat / 4 * 0.9, 18), t, 0.06)
            if k % 4 == 0:
                add(m, kick(0.35, 150, 40, 9), t, 0.6)
                add(m, lp(sq(base / 4, beat * 0.8, 4), 200), t, 0.25)
            if k % 8 == 4:
                add(m, snare(rng), t, 0.22)
            t += beat / 4
            k += 1
    return m, (60 / {"viral": 124, "creative": 110, "premium": 90, "exp": 128}.get(style, 70))


GAINS = {"pop": 0.22, "ding": 0.15, "whoosh": 0.12, "riser": 0.12, "impact": 0.35, "click": 0.12, "heart": 0.4,
         "glitch": 0.22, "swell": 0.18, "paper": 0.12, "notif": 0.4, "whoosh_down": 0.1, "pop_low": 0.18}


def build_track3(style, duration, sfx, duck, path, seed=7):
    """sfx = [(t, tipo)]; duck = [(t0, t1)] silencios estratégicos de la música."""
    rng = np.random.default_rng(seed)
    music, _ = track(style, duration, rng)
    music = music[: int((duration + 2) * SR)]
    # deja hueco a la voz (250 Hz – 3,5 kHz) bajando la banda media de la música
    mid = lp(hp(music, 250), 3500)
    music = music - 0.45 * mid
    env = np.ones(len(music))
    for a, b in duck:
        ia, ib = int(max(0.0, a) * SR), int(max(0.0, b) * SR)
        fade = int(0.12 * SR)
        env[max(0, ia - fade):ia] = np.minimum(env[max(0, ia - fade):ia], np.linspace(1, 0.08, ia - max(0, ia - fade)))
        env[ia:ib] = 0.08
        env[ib:ib + fade] = np.minimum(env[ib:ib + fade], np.linspace(0.08, 1, len(env[ib:ib + fade])))
    music *= env
    fxb = np.zeros(len(music))
    gens = {"pop": lambda: fx_pop(), "pop_low": lambda: fx_pop(600, 180), "ding": lambda: fx_ding(),
            "whoosh": lambda: fx_whoosh(rng), "whoosh_down": lambda: fx_whoosh(rng, 0.6, False),
            "riser": lambda: fx_riser(rng), "impact": lambda: fx_impact(rng), "click": fx_click, "heart": fx_heart,
            "glitch": lambda: fx_glitch(rng), "swell": lambda: fx_swell(rng), "paper": lambda: fx_paper(rng),
            "notif": fx_notif}
    for t, kind in sfx:
        s = gens[kind]()
        if kind == "riser":
            t = t - len(s) / SR
        elif kind == "swell":
            t = t - len(s) / SR * 0.85
        add(fxb, s, t, GAINS[kind])
    mix = music / (np.max(np.abs(music)) + 1e-9) * 0.55 + fxb
    mix = mix[: int(duration * SR)]
    fade = int(1.2 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= np.max(np.abs(mix)) + 1e-9
    stereo = np.stack([mix, np.roll(mix, 180)], axis=1) * 0.85
    wavfile.write(path, SR, (stereo * 32767).astype(np.int16))
    return path
