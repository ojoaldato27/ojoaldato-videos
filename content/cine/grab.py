"""Uso: python3 grab.py <modulo> t1 t2 ... -> hoja con esos instantes (segundos globales)."""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
sys.path.insert(0, HERE)
import cine
V = importlib.import_module(sys.argv[1])
times = [float(x) for x in sys.argv[2:]]
out = os.path.join("/tmp/claude-0/-home-claude/13f796bb-3765-545c-b200-821b21939a08/scratchpad", sys.argv[1] + "_grab.jpg")
print(cine.sheet(V, times, out, cols=min(4, len(times)), scale=0.3))
