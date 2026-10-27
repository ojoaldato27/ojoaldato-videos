"""Comprueba si alguna palabra clave cae encima de rótulos o dibujos: mide cuánto detalle hay debajo de cada una.
Uso: python3 kwcheck.py <modulo> [umbral]  -> imprime las sospechosas y guarda una hoja con ellas."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
sys.path.insert(0, HERE)
import cine
from styles import chunks_for
from PIL import Image, ImageFilter, ImageDraw

mod = sys.argv[1]
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
SCR = "/tmp/claude-0/-home-claude/13f796bb-3765-545c-b200-821b21939a08/scratchpad"
V = importlib.import_module(mod)
shots, caps, total = cine.timeline(V)
cine.CAPS_[0] = caps
chunks = []
for c in caps:
    chunks += chunks_for(c["text"], c["start"], c["end"], n=3)
plan = cine.keyword_plan(V, shots, caps, total)
orig = cine.draw_keywords


def cell_score(bg, it):
    kim = cine._kw_img(it["txt"], it["style"])
    x, y = it["slot"][:2]
    hw = kim.size[0] / 2 + 10
    x = min(max(x, 24 + hw), cine.W - 24 - hw) if hw * 2 < cine.W - 48 else cine.W / 2
    box = (int(x - kim.size[0] / 2 + 30), int(y - kim.size[1] / 2 + 25), int(x + kim.size[0] / 2 - 30), int(y + kim.size[1] / 2 - 25))
    e = bg.crop(box).convert("L").filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(9))
    sm = e.resize((max(1, e.size[0] // 24), max(1, e.size[1] // 24)), Image.BOX)
    px = list(sm.get_flattened_data()) if hasattr(sm, "get_flattened_data") else list(sm.getdata())
    return sum(1 for v in px if v > 40) / len(px), box

bad = []
for k, it in enumerate(plan):
    best = None
    for tm in (it["t0"] + 0.3, (it["t0"] + it["t1"]) / 2, it["t1"] - 0.1):
        i = int(tm * cine.FPS)
        cine.draw_keywords = lambda *a: None
        bg = cine.frame(V, shots, chunks, total, i)
        if cine._kw_dup(it["txt"]):
            continue
        sc_ = cell_score(bg, it)
        if best is None or sc_[0] > best[0]:
            best = (sc_[0], sc_[1], tm, i)
    if best is None:
        continue
    score, box, tm, i = best
    sh = next((s["name"] for s in shots if s["start"] <= tm < s["end"]), "?")
    flag = score > thr
    print(f"{k:2d} {tm:5.1f}s {sh:12s} slot{(cine.KW_SLOTS.index(it["slot"]) if it["slot"] in cine.KW_SLOTS else -1):>2} {score:.3f} {'<<' if flag else ''} {it['txt']}", flush=True)
    if flag:
        cine.draw_keywords = orig
        im = cine.frame(V, shots, chunks, total, i).convert("RGB")
        ImageDraw.Draw(im).rectangle(box, outline=(255, 0, 0), width=6)
        bad.append(im.resize((270, 480)))
if bad:
    sheet = Image.new("RGB", (270 * min(8, len(bad)), 480 * ((len(bad) + 7) // 8)))
    for j, im in enumerate(bad):
        sheet.paste(im, ((j % 8) * 270, (j // 8) * 480))
    p = os.path.join(SCR, f"kw_{mod}.jpg")
    sheet.save(p, quality=85)
    print("hoja:", p)
