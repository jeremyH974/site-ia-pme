#!/usr/bin/env python3
"""Injecte un widget « Tester en direct » dans les pages verticales : 2-3 démos par famille,
appelées via le tunnel n8n, résultat affiché inline. Idempotent.
Usage : python3 tools/inject_demowidget.py (dans /root/consulting/site/)
"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N8N = "https://quantitative-infinite-rand-collecting.trycloudflare.com"

DEMOS = {
    "artisans": [
        ("devis", "💶 Devis express", {"client": "Démo", "prestation": "Peinture salon 25 m²", "details": "2 couches, fournitures incluses", "zone": "Rouen", "verticale": "peinture"}),
        ("relance-devis", "📄 Relance de devis", {"client": "Démo", "prestation": "Peinture salon 25 m²", "montant": "1450", "jours": "10"}),
        ("avis", "⭐ Réponse avis", {"client": "Démo", "note": "4", "texte": "Très bon travail, équipe sérieuse"}),
    ],
    "sante": [
        ("rdv", "📅 Rappel RDV", {"client": "Démo", "date_rdv": "2026-08-05", "heure": "09:30", "prestation": "Consultation"}),
        ("faq", "💬 Standard IA", {"question": "Quels sont vos horaires ?"}),
        ("avis", "⭐ Réponse avis", {"client": "Démo", "note": "5", "texte": "Accueil parfait"}),
    ],
    "tourisme": [
        ("avis", "⭐ Réponse avis", {"client": "Démo", "note": "4", "texte": "Très bon séjour"}),
        ("rdv", "📅 Rappel RDV", {"client": "Démo", "date_rdv": "2026-08-05", "heure": "14:00", "prestation": "Arrivée"}),
        ("retour", "🔄 Retour client", {"client": "Démo", "prestation": "Séjour", "echeance": "15/08/2026"}),
    ],
    "commerce": [
        ("avis", "⭐ Réponse avis", {"client": "Démo", "note": "3", "texte": "Bien mais un peu long"}),
        ("statut", "🚚 Statut client", {"client": "Démo", "prestation": "Commande 458", "etape": "pret"}),
        ("stock", "📦 Stock", {"produit": "Peinture blanche", "niveau": "2", "seuil": "5", "fournisseur": "Peintures Pro"}),
    ],
    "transport": [
        ("relance", "📧 Relance impayés", {"client": "Démo", "montant": "980", "jours": "28"}),
        ("rdv", "📅 Rappel RDV", {"client": "Démo", "date_rdv": "2026-08-06", "heure": "10:00", "prestation": "Révision"}),
        ("statut", "🚚 Statut client", {"client": "Démo", "prestation": "Course 102", "etape": "retard"}),
    ],
    "b2b": [
        ("rapprochement", "🏦 Rapprochement", {"libelle": "VIREMENT SARL DUPONT", "montant": "2450", "facture_attendue": "FAC-2026-118"}),
        ("reporting", "📈 Reporting", {"periode": "Juin 2026", "ca_total": "14520", "nb_factures": "42", "contexte": "Période stable"}),
        ("relance-devis", "📄 Relance devis", {"client": "Démo", "prestation": "Prestation B2B", "montant": "3200", "jours": "15"}),
    ],
}

FAMILLES_FICHIERS = {
    "artisans": ["garage", "electricien", "menuisier", "paysagiste", "artisan", "architecte"],
    "sante": ["cabinet-medical", "pharmacie", "veterinaire", "dentiste", "psychologue", "spa", "coiffure", "aide-domicile", "sante"],
    "tourisme": ["hotellerie", "camping", "location-saisonniere", "conciergerie", "agence-voyage", "restauration", "food-truck", "bar"],
    "commerce": ["pressing", "boulangerie", "librairie", "salle-sport", "coach-sportif"],
    "transport": ["transport", "vtc", "auto-ecole"],
    "b2b": ["services-b2b", "tresorerie", "evenementiel", "syndic", "gestion-locative", "creche", "ecole", "organisme-formation", "avocat"],
}

def famille_for(base):
    for fam, fichiers in FAMILLES_FICHIERS.items():
        if any(base.startswith(f) or f in base for f in fichiers):
            return fam
    return None

def inject(path):
    html = open(path, encoding="utf-8").read()
    if "widget-out" in html:
        return False
    base = os.path.basename(path).replace("automatisation-", "").replace(".html", "")
    fam = famille_for(base)
    if not fam:
        return False
    demos = DEMOS[fam]
    btns = []
    for kind, label, payload in demos:
        payload_json = json_dumps(payload)
        btns.append(f'<button class="btn btn-ghost" onclick="testV(\'{kind}\', this, {payload_json})" style="margin:4px">{label}</button>')
    widget = f"""<div class="aio-box" style="margin:20px 0;padding:16px 18px">
      <h3 style="margin:0 0 8px">🧪 Testez en direct</h3>
      <p style="margin:0 0 10px">Cliquez : une vraie IA génère le résultat sous vos yeux (5-15 s).</p>
      <div>{''.join(btns)}</div>
      <div class="widget-out" style="margin-top:10px;padding:12px;background:var(--paper-2,#f3f4f6);border-radius:8px;font-size:14px;white-space:pre-wrap"></div>
      <script>
      function testV(kind, btn, payload){{
        var out = btn.parentNode.parentNode.querySelector('.widget-out');
        out.className = 'widget-out'; out.textContent = '⏳ Génération en cours… (5-15 s)';
        fetch('{N8N}/webhook/demo-' + kind, {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }}, body: JSON.stringify(payload) }})
          .then(function(r){{ return r.json(); }})
          .then(function(d){{ out.textContent = d.resultat || (d && d.titre ? d.titre + ' : ' + (d.points||[]).join(', ') : JSON.stringify(d).slice(0,400)); }})
          .catch(function(e){{ out.textContent = 'Erreur : réessayez dans un instant.'; }});
      }}
      </script>
    </div>"""
    if "</footer>" in html:
        html = html.replace("</footer>", widget + "\n</footer>", 1)
    else:
        html += widget
    open(path, "w", encoding="utf-8").write(html)
    return True

def json_dumps(d):
    import json
    return json.dumps(d, ensure_ascii=False)

def main():
    n = 0
    for f in sorted(os.listdir(SITE)):
        if f.startswith("automatisation-") and f.endswith(".html"):
            if inject(os.path.join(SITE, f)):
                n += 1
    print(f"{n} pages verticales équipées du widget de test en direct")

if __name__ == "__main__":
    main()
