#!/usr/bin/env python3
"""Cache-buster automatique : incrémente style.css?v= dans toutes les pages.
Usage : python3 tools/bump_cache.py (dans /root/consulting/site/)
"""
import os, re
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ver_file = os.path.join(SITE, ".cache_version")
v = None
if os.path.exists(ver_file):
    v = int(open(ver_file).read().strip() or "1") + 1
else:
    # init depuis la version max présente dans les pages (pas de bump au premier run)
    versions = []
    for f in os.listdir(SITE):
        if f.endswith(".html"):
            versions += [int(m) for m in re.findall(r'style\.css\?v=(\d+)', open(os.path.join(SITE, f), encoding="utf-8").read())]
    v = max(versions, default=1)
n = 0
for f in os.listdir(SITE):
    if f.endswith(".html"):
        p = os.path.join(SITE, f)
        html = open(p, encoding="utf-8").read()
        new = re.sub(r'href="style\.css(\?v=[0-9]+)?"', f'href="style.css?v={v}"', html)
        if new != html:
            open(p, "w", encoding="utf-8").write(new)
            n += 1
open(ver_file, "w").write(str(v))
print(f"cache-buster v{v} appliqué à {n} pages (auto)")
