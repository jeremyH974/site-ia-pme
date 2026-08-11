#!/usr/bin/env python3
"""Injection de la navigation v3 + fil d'Ariane sur les pages manuelles du site.
Idempotent : les pages contenant déjà 'nav-v3' sont ignorées (les headers v2/anciens sont remplacés).
Usage : python3 inject_nav.py
"""
import os
import re

SITE = "/root/consulting/site"

NAV_V4 = '<header class="site-header nav-v4"><!-- nav-v4 -->\n  <div class="wrap header-inner">\n    <a class="brand" href="index.html">Jeremy<span>, Data Analyst · Automatisation &amp; IA</span></a>\n    <nav class="main-nav" aria-label="Navigation principale">\n      <a href="index.html">Accueil</a>\n      <details class="nav-drop">\n        <summary>Solutions ▾</summary>\n        <div class="nav-drop-menu">\n          <a href="detecteur-taches.html">🎯 Trouver MES tâches à automatiser</a>\n          <a href="automatiser-devis.html">Devis &amp; factures</a>\n          <a href="relance-impayes.html">Relances &amp; impayés</a>\n          <a href="service-client.html">Service client &amp; avis</a>\n          <a href="compte-rendu-reunion.html">Comptes-rendus &amp; RDV</a>\n          <span class="nav-drop-sep"></span>\n          <a href="index.html#solutions" class="nav-drop-all">Toutes les solutions →</a>\n        </div>\n      </details>\n      <a href="guides.html">Guides</a>\n      <a href="demos.html">Démos</a>\n      <a href="tarifs.html">Tarifs</a>\n      <button class="theme-toggle" onclick="toggleTheme()" aria-label="Changer de thème sombre/clair"><span class="tt-moon">🌙</span><span class="tt-sun">☀️</span></button>\n      <a class="btn btn-primary nav-cta" href="contact.html">15 min offertes</a>\n    </nav>\n    <details class="nav-mobile">\n      <summary>☰ Menu</summary>\n      <nav aria-label="Navigation mobile">\n        <a href="index.html">Accueil</a>\n        <a href="detecteur-taches.html">🎯 Trouver mes tâches</a>\n        <a href="automatiser-devis.html">Devis &amp; factures</a>\n        <a href="relance-impayes.html">Relances &amp; impayés</a>\n        <a href="service-client.html">Service client &amp; avis</a>\n        <a href="compte-rendu-reunion.html">Comptes-rendus &amp; RDV</a>\n        <a href="index.html#solutions">Toutes les solutions →</a>\n        <a href="guides.html">Guides gratuits</a>\n        <a href="demos.html">Démos</a>\n        <a href="tarifs.html">Tarifs</a>\n        <a class="btn btn-primary" href="contact.html">15 min offertes</a>\n      </nav>\n    </details>\n  </div>\n</header>'

HEADER_RE = re.compile(r"<header class=\"site-header[^\"]*\".*?</header>", re.S)


def main():
    count = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        path = os.path.join(SITE, f)
        html = open(path, encoding="utf-8").read()
        if "nav-v4" in html and '<button class="theme-toggle" onclick="toggleTheme()"' in html:
            continue
        new_html, n = HEADER_RE.subn(NAV_V4, html, count=1)
        if n == 0:
            continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", new_html, re.S)
        if m:
            h1 = re.sub(r"<[^>]+>", " ", m.group(1))
            h1 = re.sub(r"\s+", " ", h1).strip()
            bc = f'<nav class="breadcrumb" aria-label="Fil d\'Ariane"><a href="index.html">Accueil</a> › {h1}</nav>'
            if "breadcrumb" not in new_html:
                new_html = new_html.replace(NAV_V4, NAV_V4 + "\n" + bc, 1)
        open(path, "w", encoding="utf-8").write(new_html)
        print(f"{f}: nav v3")
        count += 1
    print(f"{count} pages mises à jour")


if __name__ == "__main__":
    main()
