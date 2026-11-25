"""Inject numbers.json into screening.html (run after screen.py)."""
import json, re, os
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, "numbers.json")))
p = os.path.join(here, "screening.html")
h = open(p).read()
h = re.sub(r"const AUM=[^;]*;", f"const AUM={d['aum']};", h, count=1)
h = re.sub(r"const R=\[.*?\];\n", lambda m: "const R=" + json.dumps(d["rows"]) + ";\n", h, count=1, flags=re.S)
open(p, "w").write(h)
print("ok", len(d["rows"]), "rows")
