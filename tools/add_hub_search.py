#!/usr/bin/env python3
"""Ajoute une barre de recherche filtrable aux 6 hubs de verticales.
Idempotent (marqueur 'hub-search'). Usage : python3 tools/add_hub_search.py
"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HUBS = ["hub-artisans-btp.html", "hub-sante-bien-etre.html", "hub-tourisme-accueil.html",
        "hub-commerce-services.html", "hub-transport-logistique.html", "hub-b2b-pro.html"]

WIDGET = """<div class="hub-search" style="margin:14px 0">
  <input type="search" placeholder="🔍 Rechercher un métier… (garage, pharmacie, traiteur…)" oninput="filtreHub(this.value)" style="width:100%;max-width:520px;padding:10px 12px;border:1px solid var(--border,#e5e7eb);border-radius:8px;font-size:14px;background:var(--bg,#fff);color:inherit">
</div>
<style>.hub-search .demo-card{transition:opacity .15s}.hub-search .demo-card.hide{display:none}</style>
<script>
function filtreHub(q){q=(q||'').toLowerCase();document.querySelectorAll('.hub-grid .demo-card, .hub-grid a, .aio-box .demo-card').forEach(function(c){var box=c.closest('.demo-card')||c;box.classList.toggle('hide',!!q&&box.textContent.toLowerCase().indexOf(q)===-1)});}
</script>"""

def main():
    n = 0
    for hub in HUBS:
        p = os.path.join(SITE, hub)
        if not os.path.exists(p):
            print(f"  ⚠️ {hub} absent")
            continue
        html = open(p, encoding="utf-8").read()
        if "hub-search" in html:
            continue
        # insérer après le h1/sub du hub (avant la grille)
        m = re.search(r"<div class=\"hub-grid\"", html)
        if m:
            html = html[:m.start()] + WIDGET + "\n" + html[m.start():]
            open(p, "w", encoding="utf-8").write(html)
            n += 1
            print(f"  ✅ {hub}")
        else:
            print(f"  ⚠️ {hub}: grille introuvable")
    print(f"{n} hubs équipés de la recherche")

if __name__ == "__main__":
    main()
