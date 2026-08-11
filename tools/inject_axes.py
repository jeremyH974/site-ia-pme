#!/usr/bin/env python3
"""Injecte une section « Par besoin » dans les pages verticales (automatisation-*.html).
Chaque famille de métiers reçoit les 3-4 besoins pertinents, liés au Labo pré-filtré (?f=).
Idempotent : ne réinjecte pas si la section existe déjà.
Usage : python3 tools/inject_axes.py (dans /root/consulting/site/)
"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAMILLES = {
    "artisans": {"fichiers": ["garage", "electricien", "menuisier", "paysagiste", "artisan", "architecte"],
        "besoins": [("encaisser", "💰 Encaisser : relances impayés, rapprochement, facturation électronique"),
                    ("vendre", "📈 Vendre : devis express, relance des devis"),
                    ("servir", "🤝 Servir : rappels RDV, réponses aux avis")]},
    "sante": {"fichiers": ["cabinet-medical", "pharmacie", "veterinaire", "dentiste", "psychologue", "spa", "coiffure", "aide-domicile", "sante"],
        "besoins": [("servir", "🤝 Servir : rappels RDV, réponses aux avis, standard IA"),
                    ("conformite", "📋 En règle : facturation électronique"),
                    ("encaisser", "💰 Encaisser : relances impayés")]},
    "tourisme": {"fichiers": ["hotellerie", "camping", "location-saisonniere", "conciergerie", "agence-voyage", "restauration", "food-truck", "bar"],
        "besoins": [("servir", "🤝 Servir : rappels RDV, réponses aux avis, support"),
                    ("vendre", "📈 Vendre : devis express, idées de contenu")]},
    "commerce": {"fichiers": ["pressing", "boulangerie", "librairie", "salle-sport", "coach-sportif"],
        "besoins": [("vendre", "📈 Vendre : devis express, relance des devis"),
                    ("servir", "🤝 Servir : avis, statut client, retours"),
                    ("produire", "🏭 Produire : stock sous contrôle")]},
    "transport": {"fichiers": ["transport", "vtc", "auto-ecole"],
        "besoins": [("encaisser", "💰 Encaisser : relances impayés, rapprochement"),
                    ("servir", "🤝 Servir : rappels RDV, statut client")]},
    "b2b": {"fichiers": ["services-b2b", "tresorerie", "evenementiel", "syndic", "gestion-locative", "creche", "ecole", "organisme-formation", "avocat"],
        "besoins": [("encaisser", "💰 Encaisser : rapprochement bancaire, facturation électronique"),
                    ("savoir", "🧠 Décider : reporting, briefing matinal, veille"),
                    ("vendre", "📈 Vendre : devis, relance des devis, prospection")]},
}

def inject(path):
    html = open(path, encoding="utf-8").read()
    if "Chaque métier a ses besoins" in html:
        return False
    base = os.path.basename(path).replace("automatisation-", "").replace(".html", "")
    famille = None
    for fam, cfg in FAMILLES.items():
        if any(base.startswith(f) or f in base for f in cfg["fichiers"]):
            famille = fam
            break
    if not famille:
        return False
    liens = " · ".join(f'<a href="labo-demo.html?f={k}">{label}</a>' for k, label in FAMILLES[famille]["besoins"])
    section = (f'<div class="aio-box" style="margin:20px 0;padding:16px 18px">'
               f'<h3 style="margin:0 0 8px">🎯 Par besoin</h3>'
               f'<p style="margin:0 0 10px">Chaque métier a ses besoins. Commencez par votre objectif : les démos sont testables en direct :</p>'
               f'<p style="margin:0 0 8px">{liens}</p>'
               f'<p style="margin:0"><a href="solutions-par-besoin.html">Toutes les solutions par besoin →</a></p></div>')
    if "</footer>" in html:
        html = html.replace("</footer>", section + "\n</footer>", 1)
    else:
        html = html.replace("</main>", "</main>\n" + section, 1) if "</main>" in html else html + section
    open(path, "w", encoding="utf-8").write(html)
    return True

def main():
    n = 0
    for f in sorted(os.listdir(SITE)):
        if f.startswith("automatisation-") and f.endswith(".html"):
            if inject(os.path.join(SITE, f)):
                n += 1
    print(f"{n} pages verticales enrichies « Par besoin »")

if __name__ == "__main__":
    main()
