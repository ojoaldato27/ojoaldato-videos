"""Genera urda.js = motor de rebufo.js (hasta las escenas) + urda_scenes.js."""
import os
H = os.path.dirname(os.path.abspath(__file__))
base = open(os.path.join(H, "rebufo.js")).read().split("\n")
cut = next(i for i, l in enumerate(base) if l.startswith("// ---------- escenas ----------"))
sc = open(os.path.join(H, "urda_scenes.js")).read().split("\n")
imports = [l for l in sc if l.startswith("import ")]
body = [l for l in sc if not l.startswith("import ")]
head = [l for l in base[:cut] if l.startswith("import ")]
rest = [l for l in base[:cut] if not l.startswith("import ")]
open(os.path.join(H, "urda.js"), "w").write("\n".join(head + imports + rest + body))
print("urda.js ok")
