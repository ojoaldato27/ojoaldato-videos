"""Uso: python3 run.py <modulo> [sheet|render|both] [salida_dir]"""
import sys, os, importlib, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
sys.path.insert(0, HERE)
import cine

mod = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "sheet"
out_dir = sys.argv[3] if len(sys.argv) > 3 else "/home/claude/shorts-ingenieria/output/cine"
os.makedirs(out_dir, exist_ok=True)
V = importlib.import_module(mod)
shots, caps, total = cine.timeline(V)
print(json.dumps({"total": round(total, 1), "shots": [(s["name"], round(s["start"], 1)) for s in shots]}))
if mode in ("sheet", "both"):
    times = []
    for s in shots:
        times += [s["start"] + min(1.2, (s["end"] - s["start"]) * 0.3), s["start"] + (s["end"] - s["start"]) * 0.8]
    p = cine.sheet(V, times, os.path.join(out_dir, mod + "_sheet.jpg"), cols=6, scale=0.2)
    print("sheet", p)
if mode in ("render", "both"):
    t0 = time.time()
    out = os.path.join(out_dir, V.TITLE + ".mp4")
    cine.render(V, out)
    print("render", out, round(time.time() - t0), "s")
