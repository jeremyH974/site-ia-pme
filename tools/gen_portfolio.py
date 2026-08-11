#!/usr/bin/env python3
"""Génère automatisations.html : le showroom des 35 blocs, depuis le manifest de l'export NAS.
Usage : python3 tools/gen_portfolio.py (dans /root/consulting/site/)
Industrialisé : à re-lancer après chaque nouveau bloc.
"""
import json, os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(os.path.dirname(SITE), "export-nas", "manifest.json")

# Axe par dossier (lettre du code 92)
AXES = {
 "bloc-c-relance-impayes": ("A", "💰", "Encaisser et payer"),
 "bloc-b1-agent-devis": ("B", "📈", "Vendre et garder le fil"),
 "bloc-b1-fiche-apres-appel": ("B", "📇", "Vendre et garder le fil"),
 "bloc-b2-avis-google": ("C", "🤝", "Servir le client"),
 "bloc-b3-tri-emails": ("A", "📧", "Encaisser et payer"),
 "bloc-b3-dedoublonnage": ("B", "🗃️", "Vendre et garder le fil"),
 "bloc-b4-rappel-rdv": ("C", "🤝", "Servir le client"),
 "bloc-b5-standard-ia": ("C", "💬", "Servir le client"),
 "bloc-b6-prise-rdv": ("C", "🗓️", "Servir le client"),
 "bloc-b7-gestion-stock": ("D", "🏭", "Produire et livrer"),
 "bloc-b8-compte-rendu": ("F", "🧠", "Savoir et décider"),
 "bloc-b9-rapprochement": ("A", "🏦", "Encaisser et payer"),
 "bloc-b10-reporting": ("F", "📊", "Savoir et décider"),
 "bloc-b11-statut-client": ("C", "🚚", "Servir le client"),
 "bloc-b12-retour-client": ("C", "🔄", "Servir le client"),
 "bloc-b13-standard-vocal": ("C", "🎙️", "Servir le client"),
 "bloc-b14-relance-devis": ("B", "📄", "Vendre et garder le fil"),
 "bloc-b15-briefing-matinal": ("F", "🌅", "Savoir et décider"),
 "bloc-b16-veille-concurrentielle": ("F", "📡", "Savoir et décider"),
 "bloc-b17-support-tickets": ("C", "🎫", "Servir le client"),
 "bloc-b18-notes-frais": ("A", "🧾", "Encaisser et payer"),
 "bloc-b19-idees-contenu": ("B", "💡", "Vendre et garder le fil"),
 "bloc-b20-article-seo": ("B", "📰", "Vendre et garder le fil"),
 "bloc-b21-facture-elec": ("A", "🧾", "Encaisser et payer"),
 "bloc-b22-base-clients": ("A", "🗂️", "Encaisser et payer"),
 "bloc-b23-reconductions": ("G", "⏰", "Contracter et se conformer"),
 "bloc-b24-verif-factures": ("G", "✅", "Contracter et se conformer"),
 "bloc-b25-factures-intl": ("G", "🌍", "Contracter et se conformer"),
 "bloc-b26-statuts-transmission": ("G", "📨", "Contracter et se conformer"),
 "bloc-g10-transparence-ia": ("G", "🤖", "Contracter et se conformer"),
 "bloc-e1-preselection-cv": ("E", "👥", "Recruter et gérer les gens"),
 "bloc-f5-cloture-mensuelle": ("F", "📊", "Savoir et décider"),
 "bloc-c8-clients-inactifs": ("C", "💛", "Servir le client"),
 "bloc-j7-ordonnancier": ("J", "💊", "Professions réglementées"),
 "bloc-j12-doc-relation": ("J", "📋", "Professions réglementées"),
}

DESC = {
 "bloc-c-relance-impayes": "Relance des impayés en 3 paliers (J+7 poli, J+21 ferme, J+35 dernier recours)",
 "bloc-b1-agent-devis": "Devis chiffré en 30 secondes, 24h/24, selon la grille de votre métier",
 "bloc-b1-fiche-apres-appel": "Les notes d'un appel deviennent une fiche client, relance datée",
 "bloc-b2-avis-google": "Réponse professionnelle à chaque avis, ton adapté à la note",
 "bloc-b3-tri-emails": "Factures, devis, spam : classés + montants et échéances extraits",
 "bloc-b3-dedoublonnage": "Doublons détectés (SIRET, email, nom), le maître choisi",
 "bloc-b4-rappel-rdv": "Rappels J-1 et gestion des no-show, personnalisés",
 "bloc-b5-standard-ia": "Standard téléphonique IA : horaires, préparation, infos",
 "bloc-b6-prise-rdv": "3 créneaux proposés selon les préférences du client",
 "bloc-b7-gestion-stock": "Alerte + réappro chiffré au bon moment",
 "bloc-b8-compte-rendu": "Notes brutes → CR structuré (chantier, clinique, équipe)",
 "bloc-b9-rapprochement": "Opérations rapprochées de leurs factures, écart expliqué",
 "bloc-b10-reporting": "CA, tendances, anomalies : le chiffre qui parle",
 "bloc-b11-statut-client": "Le client informé de sa commande, sans appeler",
 "bloc-b12-retour-client": "Le rappel qui fait revenir (CT, retouche, abonnement)",
 "bloc-b13-standard-vocal": "Standard vocal qui répond, transcrit, transmet",
 "bloc-b14-relance-devis": "Devis sans réponse relancé à J+7, J+14, J+21",
 "bloc-b15-briefing-matinal": "Votre journée résumée chaque matin : agenda, emails, actu",
 "bloc-b16-veille-concurrentielle": "3 signaux, 1 menace, 1 opportunité chaque matin",
 "bloc-b17-support-tickets": "Tickets classés, brouillons prêts, validation humaine",
 "bloc-b18-notes-frais": "Le reçu devient une ligne de notes de frais",
 "bloc-b19-idees-contenu": "5 idées de contenu avec angle et hook, chaque jour",
 "bloc-b20-article-seo": "Article structuré H1/H2/CTA, prêt à publier",
 "bloc-b21-facture-elec": "Bilan de conformité facture électronique, actions datées",
 "bloc-b22-base-clients": "SIRET, TVA, APE, emails vérifiés avant l'échéance",
 "bloc-b23-reconductions": "Reconductions tacites : la lettre de résiliation avant la date",
 "bloc-b24-verif-factures": "Numéros, SIRET, TVA, montants vérifiés avant envoi",
 "bloc-b25-factures-intl": "Autoliquidation, export, VIES : le bon régime TVA",
 "bloc-b26-statuts-transmission": "Factures acceptées/rejetées : la relance prête",
 "bloc-g10-transparence-ia": "IA Act : le niveau de chaque usage, les obligations",
 "bloc-e1-preselection-cv": "CV pré-triés sur critères objectifs, questions prêtes",
 "bloc-f5-cloture-mensuelle": "Ventes, achats, banque consolidés, écart calculé",
 "bloc-c8-clients-inactifs": "90/180 jours sans activité : la relance de reconquête",
 "bloc-j7-ordonnancier": "Complétude des ordonnances vérifiée, points à contrôler",
 "bloc-j12-doc-relation": "Document d'entrée en relation, modèle à valider",
}

def main():
    m = json.load(open(MANIFEST, encoding="utf-8"))
    blocs = m.get("blocs", m.get("workflows", []))
    # si la structure est {slug: {...}}
    items = []
    if isinstance(blocs, dict):
        for slug, meta in blocs.items():
            items.append({"slug": slug, **meta})
    else:
        items = blocs
    # grouper par axe
    groupes = {}
    for it in items:
        slug = it.get("slug", "")
        lettre, emoji, axe = AXES.get(slug, ("X", "⚙️", "Socle"))
        groupes.setdefault(lettre, {"axe": axe, "emoji": emoji, "blocs": []})
        groupes[lettre]["blocs"].append(it)
    cards = []
    for lettre in sorted(groupes):
        g = groupes[lettre]
        cards.append(f'<h2 class="hub-title">{g["emoji"]} {g["axe"]}</h2><div class="hub-grid">')
        for it in g["blocs"]:
            slug = it.get("slug", "")
            webhook = it.get("webhook", "")
            desc = DESC.get(slug, "")
            demo = f'<a class="btn btn-ghost" href="labo-demo.html?f=all">🧪 Tester</a>' if webhook else ""
            cards.append(f'''<div class="demo-card" style="margin:0">
              <h3>{AXES.get(slug,("X","⚙️","Socle"))[1]} {slug.replace("bloc-","").replace("-"," ").title()}</h3>
              <div class="demo-desc">{desc}</div>
              {demo}
            </div>''')
        cards.append("</div>")
    body = "\n".join(cards)
    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Les 35 automatisations : le showroom complet, testable en direct</title>
<meta name="description" content="35 automatisations IA pour PME, classées par besoin : encaisser, vendre, servir, produire, savoir, se conformer, santé. Chaque démo est testable en direct.">
<link rel="stylesheet" href="style.css?v=43">
<script>/* theme-toggle-js */function toggleTheme(){{var r=document.documentElement;var d=r.getAttribute('data-theme')==='dark';r.setAttribute('data-theme',d?'light':'dark');try{{localStorage.setItem('theme',d?'light':'dark')}}catch(e){{}}}}</script>
</head><body>
<header class="site-header"><div class="wrap"><a class="brand" href="index.html">Jeremy, Data Analyst · Automatisation &amp; IA</a>
<nav class="main-nav" aria-label="Navigation principale"><a href="index.html">Accueil</a><a href="solutions-par-besoin.html">Solutions</a><a href="labo-demo.html">Labo</a><a href="tarifs.html">Tarifs</a><a href="contact.html">Contact</a>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Changer le thème"><span class="tt-moon">🌙</span><span class="tt-sun">☀️</span></button></nav></div></header>
<main class="wrap">
<div class="labo-filtres" style="margin:18px 0 22px;padding:14px 16px;background:var(--card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px">
  <input id="portfolio-search" type="search" placeholder="🔍 Rechercher… (devis, facture, RDV, relance, santé…)" oninput="filtrePortfolio()" style="width:100%;padding:10px 12px;border-radius:8px;font-size:14px">
</div>
<style>[data-theme="dark"] .labo-filtres{{background:#16231c;border-color:#2a5a41}}[data-theme="dark"] .labo-filtres input{{background:#1c221f;border-color:#2a332e;color:#e8ece8}}.demo-card{{transition:opacity .15s}}.demo-card.hide{{display:none}}</style>
<script>
function filtrePortfolio(){{var q=(document.getElementById('portfolio-search').value||'').toLowerCase();document.querySelectorAll('.demo-card').forEach(function(c){{c.classList.toggle('hide',!!q&&c.textContent.toLowerCase().indexOf(q)===-1)}});}}
</script>
<h1>Les 35 automatisations : <em>le showroom complet</em></h1>
<p>Chaque bloc est testable en direct dans le Labo. Ils sont classés par besoin : choisissez votre axe, testez, et décidez.</p>
<p><a class="btn btn-primary" href="labo-demo.html">🧪 Ouvrir le Labo (35 démos)</a> <a class="btn btn-ghost" href="solutions-par-besoin.html">Par besoin</a></p>
{body}
</main>
<footer><div class="wrap"><p>© 2026 Jeremy : Data Analyst · Automatisation &amp; IA · <a href="engagements-fiabilite.html">🛡️ Engagements fiabilité</a> · <a href="confidentialite.html">Confidentialité</a></p>
<span class="data-sources" style="font-size:12px;opacity:.75"><strong>Sources :</strong> <a href="https://www.impots.gouv.fr" target="_blank" rel="noopener">impots.gouv.fr</a> · <a href="https://www.facturation.gouv.fr" target="_blank" rel="noopener">facturation.gouv.fr</a> · <a href="https://eur-lex.europa.eu" target="_blank" rel="noopener">EUR-Lex</a> · <a href="https://www.service-public.fr" target="_blank" rel="noopener">service-public.fr</a> · <a href="https://www.insee.fr" target="_blank" rel="noopener">INSEE</a> · <a href="https://ec.europa.eu/taxation_customs/vies/" target="_blank" rel="noopener">VIES</a></span></div></footer>
</body></html>"""
    with open(os.path.join(SITE, "automatisations.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"automatisations.html générée : {len(items)} blocs, {len(groupes)} axes")

if __name__ == "__main__":
    main()
