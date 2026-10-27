"""Constructor de vídeos «fun»: cada vídeo = lista de escenas (beats) con frases y pegatinas sincronizadas."""
import json, os, re

WPS = 2.4
HERE = os.path.dirname(os.path.abspath(__file__))


def dur(txt, mn=1.6):
    n = len(re.findall(r"\w+", txt.replace("*", "")))
    return max(mn, n / WPS + 0.35)


# atajos de elementos: (frase, retardo, elemento)
def I(icon, x, y, s, **kw):
    d = {"icon": icon, "x": x, "y": y, "s": s}
    tw = kw.pop("tw", None)
    if tw:
        d["tw"] = tw
    for k in ("out", "float"):
        if k in kw:
            d[k] = kw.pop(k)
    d["opt"] = kw
    return d


def T(text, x, y, size=64, **kw):
    return dict(text=text, x=x, y=y, size=size, **kw)


def N(a, b, x, y, size=170, sub="", fmt="{:,.0f}", **kw):
    return dict(count=[a, b], x=x, y=y, size=size, sub=sub, fmt=fmt, **kw)


def M(mood, x, y, s=230, **kw):
    return dict(mascot=mood, x=x, y=y, s=s, **kw)


def O(options, correct, y=560, **kw):
    return dict(options=options, correct=correct, x=540, y=y, float=False, **kw)


def S(txt, x, y, size=90, col=(230, 50, 60), **kw):
    return dict(stamp=txt, x=x, y=y, size=size, col=col, float=False, **kw)


def build(sid, title, desc, question, beats, tags):
    t = 0.0
    scenes, caps, sfx = [], [], []
    reveal_abs, q_from = None, None
    for bi, b in enumerate(beats):
        st = t
        starts = []
        for ln in b["lines"]:
            d_ = dur(ln)
            starts.append(t - st)
            caps.append({"start": round(t, 2), "end": round(t + d_, 2), "text": ln})
            t += d_
        t += b.get("pad", 0.25)
        items = []
        for li, dt, it in b.get("items", []):
            it = json.loads(json.dumps(it))
            base = starts[li] + dt
            it["at"] = round(base, 2)
            if "tw" in it:
                for k, v in it["tw"].items():
                    v[0] = round(v[0] + base, 2) if v[0] is not None else round(base, 2)
                    v[1] = round(v[1] + base, 2)
            if "out" in it:
                it["out"] = round(starts[it["out"][0]] + it["out"][1], 2)
            if "options" in it and "reveal" in it:
                it["reveal"] = round(starts[it["reveal"][0]] + it["reveal"][1], 2)
                reveal_abs = st + it["reveal"]
            items.append(it)
            a = st + it["at"]
            if "stamp" in it:
                sfx.append((a, "impact"))
            elif "options" in it:
                for k in range(len(it["options"])):
                    sfx.append((a + k * 0.18, "pop"))
                if "reveal" in it:
                    sfx.append((st + it["reveal"], "ding"))
            elif "mascot" in it:
                sfx.append((a, "pop_low"))
            elif "count" in it:
                sfx.append((a, "riser" if False else "pop"))
                sfx.append((a + it.get("dur", 1.4), "ding"))
            else:
                sfx.append((a, "pop" if len(sfx) % 2 else "pop_low"))
        params = {"bg": b["bg"], "items": items, "dur": round(t - st, 2)}
        if "confetti" in b:
            li, dt = b["confetti"]
            params["confetti"] = round(starts[li] + dt, 2)
            sfx.append((st + params["confetti"], "whoosh"))
        scenes.append({"type": "beat", "start": round(st, 2), "end": round(t, 2), "params": params})
        if bi > 0:
            sfx.append((st, "whoosh_down"))
        if b.get("q_from"):
            q_from = t
    mid = scenes[len(scenes) // 2]["start"] + 0.6
    s = {"id": sid, "style": "fun", "music": "creative", "duration": round(t, 2), "seed": sum(map(ord, sid)) % 997,
         "thumb_time": 1.5, "watermark": "@nolosabias_datos", "chunk_n": 3, "burn_captions": True,
         "scenes": scenes, "captions": caps, "chapters": [], "sfx": [[round(a, 2), k] for a, k in sorted(sfx)],
         "question": {"text": question, "from": round(q_from or scenes[1]["end"], 2), "reveal": round(reveal_abs or t, 2)},
         "notifs": [{"t": round(mid, 2), "title": "nolosabias_datos", "body": "Suscríbete para más datos que no sabías"}],
         "metadata": {"title": title, "description": desc, "tags": tags},
         "rights": [{"asset": "animación, iconos y mascota", "license": "propio"},
                    {"asset": "música y efectos (sintetizados con código)", "license": "propio"},
                    {"asset": "tipografía Poppins", "license": "licencia comercial", "note": "OFL"}]}
    os.makedirs(os.path.join(HERE, "scripts"), exist_ok=True)
    json.dump(s, open(os.path.join(HERE, "scripts", f"{sid}.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{sid}: {s['duration']:.1f} s")
    return s
