"""Músicas de fondo nuevas (27/10), todas sintetizadas aquí: sin licencias de terceros.
Estilos: trailer (épica tráiler), heroic (orquestal heroica), phonk, synthwave, lofi_hh (lo-fi hip hop).
Uso: en el módulo del vídeo, AUDIO["music"] = [("q", "<estilo>")]; cine.music_bed los reconoce."""
import numpy as np
import music3 as M

SR = M.SR
STYLES = ("trailer", "heroic", "phonk", "synthwave", "lofi_hh")

D_MIN = [[146.83, 174.61, 220.0], [116.54, 146.83, 174.61], [174.61, 220.0, 261.63], [130.81, 164.81, 196.0]]
HERO = [[196.0, 246.94, 293.66], [146.83, 185.0, 220.0], [164.81, 196.0, 246.94], [130.81, 164.81, 196.0]]   # G D Em C
F_MIN = [[174.61, 207.65, 261.63], [138.59, 174.61, 207.65], [155.56, 196.0, 233.08], [130.81, 164.81, 196.0]]
SW = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66], [164.81, 207.65, 246.94]]


def _n(dur):
    return np.zeros(int((dur + 3) * SR))


def saw(f, d, decay=0.0, cut=3000, det=0.006):
    t = M.tt(d)
    w = sum(np.sin(2 * np.pi * f * (1 + det * j) * k * t) / k for k in range(1, 10) for j in (-1, 0, 1)) / 3
    e = np.minimum(1, t / 0.02) * (np.exp(-t * decay) if decay else 1.0)
    return M.lp(w * e, cut)


def brass(f, d):
    t = M.tt(d)
    e = np.minimum(1, t / 0.12) * np.minimum(1, np.clip((d - t) / 0.3, 0, 1))
    return saw(f, d, 0, 1800 + 0 * f) * e * 0.5


def taiko(d=0.9, f0=95, f1=48):
    t = M.tt(d)
    f = f1 + (f0 - f1) * np.exp(-t * 14)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    return body


def boom(rng, d=1.6):
    t = M.tt(d)
    sub = np.sin(2 * np.pi * np.cumsum(30 + 40 * np.exp(-t * 6)) / SR) * np.exp(-t * 2.2)
    nz = M.lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 5) * 0.4
    return sub + nz


def bass808(f, d, glide=0.0):
    t = M.tt(d)
    fr = f * (1 + glide * np.exp(-t * 18))
    w = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(fr) / SR))
    return M.lp(w, 260) * np.exp(-t * 1.6) * np.minimum(1, t / 0.004)


def cowbell(f, d=0.35):
    t = M.tt(d)
    w = np.sign(np.sin(2 * np.pi * f * t)) + np.sign(np.sin(2 * np.pi * f * 1.48 * t))
    return M.hp(M.lp(w, 4000), 500) * np.exp(-t * 11) * 0.5


def clap(rng, d=0.25):
    t = M.tt(d)
    n = M.hp(rng.standard_normal(len(t)), 1200)
    e = np.exp(-t * 26) + 0.6 * np.exp(-np.clip(t - 0.012, 0, None) * 26) * (t > 0.012)
    return n * e * 0.5


def vinyl(rng, dur):
    n = int((dur + 3) * SR)
    hiss = M.hp(rng.standard_normal(n), 3000) * 0.012
    pops = np.zeros(n)
    for i in rng.integers(0, n, int(dur * 7)):
        pops[i] = rng.uniform(0.2, 0.6) * rng.choice([-1, 1])
    return hiss + M.lp(pops, 5000)


def trailer(dur, rng):
    m = _n(dur)
    beat = 60 / 92
    t, k = 0.0, 0
    while t < dur:                      # ostinato de cuerdas en semicorcheas
        ch = D_MIN[(k // 32) % 4]
        f = ch[[0, 2, 1, 2][k % 4]] * 2
        M.add(m, saw(f, beat / 4 * 0.9, 9, 2600), t, 0.05)
        t += beat / 4
        k += 1
    t, k = 0.0, 0
    while t < dur:                      # acordes graves sostenidos
        for f in D_MIN[k % 4]:
            M.add(m, M.strings(f / 2, beat * 8 + 0.8), t, 1.1)
        t += beat * 8
        k += 1
    t, i = 0.0, 0
    while t < dur:                      # taikos
        M.add(m, taiko(), t, 0.55)
        if i % 4 == 3:
            M.add(m, taiko(0.6, 120, 60), t + beat * 0.5, 0.35)
            M.add(m, taiko(0.6, 120, 60), t + beat * 0.75, 0.3)
        if i % 2 == 1:
            M.add(m, M.lp(M.snare(rng, 0.3), 2500), t, 0.18)
        t += beat
        i += 1
    t = beat * 8
    while t < dur:                      # golpe grande cada 2 compases
        M.add(m, boom(rng), t, 0.5)
        t += beat * 8
    return m


def heroic(dur, rng):
    m = _n(dur)
    beat = 60 / 100
    t, k = 0.0, 0
    while t < dur:
        ch = HERO[k % 4]
        for f in ch:
            M.add(m, M.strings(f, beat * 4 + 0.8), t, 0.9)
            M.add(m, brass(f / 2, beat * 3.6), t, 0.16)
        t += beat * 4
        k += 1
    mel = [392.0, 440.0, 493.88, 587.33, 493.88, 440.0, 392.0, 329.63]
    t, k = beat * 4, 0
    while t < dur:                      # fanfarria de trompas (suave, deja hueco a la voz)
        M.add(m, brass(mel[k % 8], beat * 0.95), t, 0.07)
        t += beat
        k += 1
    t, i = 0.0, 0
    while t < dur:
        M.add(m, taiko(0.7, 85, 45), t, 0.35 if i % 2 == 0 else 0.2)
        M.add(m, M.hat(M.np.random.default_rng(i), 0.04), t + beat / 2, 0.04)
        t += beat
        i += 1
    return m


def phonk(dur, rng):
    m = _n(dur)
    beat = 60 / 130
    mel = [0, 3, 7, 3, 10, 7, 3, 0, 5, 3, 7, 12, 10, 7, 5, 3]
    t, k = 0.0, 0
    while t < dur:                      # melodía de cencerro, la firma del phonk
        root = F_MIN[(k // 16) % 4][0] * 2
        if k % 16 not in (7, 15):
            M.add(m, cowbell(root * 2 ** (mel[k % 16] / 12)), t, 0.09)
        t += beat / 2
        k += 1
    t, i = 0.0, 0
    while t < dur:
        if i % 8 in (0, 3, 6):
            M.add(m, M.kick(0.35, 140, 45, 9), t, 0.55)
        if i % 4 == 2:
            M.add(m, clap(rng), t, 0.3)
        roll = 3 if i % 8 == 7 else 1
        for r in range(2 * roll):
            M.add(m, M.hat(rng, 0.03), t + r * beat / (2 * roll), 0.07)
        if i % 4 == 0:
            f = F_MIN[(i // 16) % 4][0] / 2
            M.add(m, bass808(f, beat * 3.5, 0.6), t, 0.45)
        t += beat
        i += 1
    return np.tanh(m * 1.4) / 1.4


def synthwave(dur, rng):
    m = _n(dur)
    beat = 60 / 100
    t, k = 0.0, 0
    while t < dur:
        for f in SW[k % 4]:
            M.add(m, M.pad(f, beat * 4 + 0.8, 1.4), t, 0.7)
        t += beat * 4
        k += 1
    arp = [0, 7, 12, 16, 12, 7]
    t, k = 0.0, 0
    while t < dur:
        root = SW[(k // 16) % 4][0] * 2
        M.add(m, saw(root * 2 ** (arp[k % 6] / 12), beat / 4 * 0.8, 14, 3200), t, 0.045)
        f = SW[(k // 16) % 4][0] / 2
        M.add(m, M.lp(saw(f, beat / 4 * 0.8, 8, 900), 500), t, 0.12)
        t += beat / 4
        k += 1
    t, i = 0.0, 0
    while t < dur:
        M.add(m, M.kick(0.3, 110, 45, 10), t, 0.5)
        if i % 2 == 1:
            sn = M.snare(rng, 0.35)
            gate = np.ones(len(sn)); gate[int(0.18 * SR):] = 0
            M.add(m, M.lp(sn * gate, 6000), t, 0.3)
        M.add(m, M.hat(rng, 0.04), t + beat / 2, 0.06)
        t += beat
        i += 1
    return m


def lofi_hh(dur, rng):
    m = _n(dur)
    beat = 60 / 84
    jazz = [[220.0, 261.63, 329.63, 392.0], [146.83, 174.61, 220.0, 261.63], [196.0, 246.94, 293.66, 349.23],
            [261.63, 329.63, 392.0, 493.88]]
    t, k = 0.0, 0
    while t < dur:
        for f in jazz[k % 4]:
            M.add(m, M.rhodes(f, beat * 4 + 0.5), t + 0.02 * rng.random(), 0.16)
        M.add(m, M.lp(M.pluck(jazz[k % 4][0] / 2, beat * 2, 3), 300), t, 0.35)
        M.add(m, M.lp(M.pluck(jazz[k % 4][0] / 2 * 1.5, beat * 2, 3), 300), t + beat * 2.5, 0.25)
        t += beat * 4
        k += 1
    t, i = 0.0, 0
    while t < dur:
        sw = beat * 0.08 if i % 2 else 0
        if i % 4 in (0,) or i % 8 == 5:
            M.add(m, M.kick(0.35, 90, 45, 9), t, 0.5)
        if i % 4 in (1, 3):
            M.add(m, M.lp(M.snare(rng, 0.2), 3200), t, 0.22)
        M.add(m, M.lp(M.hat(rng, 0.05), 9000), t + beat / 2 + sw, 0.05)
        t += beat
        i += 1
    m = M.lp(m, 4200)
    return m + vinyl(rng, dur)[:len(m)]


def bed(style, dur, rng):
    return {"trailer": trailer, "heroic": heroic, "phonk": phonk, "synthwave": synthwave, "lofi_hh": lofi_hh}[style](dur, rng)
