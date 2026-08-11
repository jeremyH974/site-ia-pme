#!/usr/bin/env python3
"""Redesign de solutions-par-besoin.html : filtres + recherche + cartes ROI cliquables.
Idempotent. Usage : python3 tools/redesign_solutions.py (dans /root/consulting/site/)
"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(SITE, "solutions-par-besoin.html")

BODY = """<main class="wrap">
  <div style="padding:22px 0 10px;text-align:center">
    <h1 style="font-size:clamp(26px,4.5vw,40px);line-height:1.15;margin:0 0 8px">Par quoi voulez-vous <em>commencer</em> ?</h1>
    <p style="font-size:16px;opacity:.9;max-width:640px;margin:0 auto">Choisissez un objectif, testez la démo en 30 secondes. Pas de jargon, pas d'engagement.</p>
  </div>

  <div class="labo-filtres" style="margin:18px 0;padding:14px 16px;background:var(--card,#fff);border:1px solid var(--border,#e5e7eb);border-radius:12px">
    <input id="sol-search" type="search" placeholder="🔍 Rechercher… (facture, devis, RDV, santé, relance…)" oninput="filtreSol()" style="width:100%;padding:10px 12px;border:1px solid var(--border,#e5e7eb);border-radius:8px;font-size:14px;background:var(--bg,#fff);color:inherit">
    <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:6px">
      <button class="fbtn on" data-f="tous" onclick="filtreType(this,'tous')">Tous</button>
      <button class="fbtn" data-f="argent" onclick="filtreType(this,'argent')">💰 Gagner de l'argent</button>
      <button class="fbtn" data-f="temps" onclick="filtreType(this,'temps')">⏱️ Gagner du temps</button>
      <button class="fbtn" data-f="conformite" onclick="filtreType(this,'conformite')">📋 Être en règle</button>
      <button class="fbtn" data-f="sante" onclick="filtreType(this,'sante')">💊 Santé</button>
    </div>
  </div>
  <style>[data-theme="dark"] .labo-filtres{background:#16231c;border-color:#2a5a41}[data-theme="dark"] .labo-filtres input{background:#1c221f;border-color:#2a332e;color:#e8ece8}.fbtn{border:1px solid var(--border,#e5e7eb);border-radius:999px;padding:7px 13px;font-size:13px;cursor:pointer;background:var(--bg,#fff);color:inherit}.fbtn.on{background:var(--accent,#3fae78);color:#fff;border-color:var(--accent,#3fae78)}.demo-card{transition:opacity .15s}.demo-card.hide{display:none}</style>
  <script>
  function filtreSol(){var q=(document.getElementById('sol-search').value||'').toLowerCase();document.querySelectorAll('#sol-grid .demo-card').forEach(function(c){c.classList.toggle('hide',!!q&&c.textContent.toLowerCase().indexOf(q)===-1)});}
  function filtreType(btn,t){document.querySelectorAll('.fbtn').forEach(function(b){b.classList.remove('on')});btn.classList.add('on');document.querySelectorAll('#sol-grid .demo-card').forEach(function(c){c.classList.toggle('hide',t!=='tous'&&c.getAttribute('data-t')!==t)});}
  </script>

  <div id="sol-grid" class="hub-grid">
    <div class="demo-card" style="margin:0" data-t="argent">
      <h3>💰 Encaisser plus vite</h3>
      <div class="demo-desc">Relances d'impayés en 3 paliers, rapprochement bancaire, facturation électronique.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> ~5 h/semaine récupérées ≈ 9 200 €/an. Plus un seul impayé oublié.</p>
      <a class="btn btn-ghost" href="labo-demo.html?f=encaisser">🧪 Tester (5 démos) →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="argent">
      <h3>📈 Vendre mieux</h3>
      <div class="demo-desc">Devis 24/7, relance à J+7/J+14/J+21, clients perdus de vue relancés.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> ~3 h/semaine + des devis qui ne restent plus sans réponse.</p>
      <a class="btn btn-ghost" href="labo-demo.html?f=vendre">🧪 Tester (4 démos) →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="temps">
      <h3>🤝 Servir vos clients</h3>
      <div class="demo-desc">RDV rappelés J-1, avis répondus, support tickets classés, clients inactifs relancés.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> moins de no-show, des avis 5 étoiles, des clients qui reviennent.</p>
      <a class="btn btn-ghost" href="labo-demo.html?f=servir">🧪 Tester (7 démos) →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="temps">
      <h3>🏭 Produire et livrer</h3>
      <div class="demo-desc">Stock alerté avant la rupture, compte-rendu de chantier prêt en 2 minutes.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> zéro rupture, zéro compte-rendu oublié.</p>
      <a class="btn btn-ghost" href="automatisations.html">🧪 Voir les démos →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="temps">
      <h3>🧠 Décider avec des faits</h3>
      <div class="demo-desc">Briefing chaque matin, reporting auto, veille concurrentielle, clôture consolidée.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> la bonne décision au bon moment, sans ouvrir 5 tableurs.</p>
      <a class="btn btn-ghost" href="labo-demo.html?f=savoir">🧪 Tester (5 démos) →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="conformite">
      <h3>📋 Être en règle</h3>
      <div class="demo-desc">Facturation électronique (réception 09/2026, émission 09/2027), IA Act, transparence IA.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> l'obligation qui arrive se transforme en chantier clair et chiffré.</p>
      <a class="btn btn-ghost" href="labo-demo.html?f=conformite">🧪 Tester (6 démos) →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="sante">
      <h3>💊 Santé et professions réglementées</h3>
      <div class="demo-desc">Ordonnancier vérifié, document d'entrée en relation, rappels patients.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> la conformité calculée, le temps rendu au soin.</p>
      <a class="btn btn-ghost" href="offre-cabinet-en-regle.html">🏥 Voir l'offre →</a>
    </div>
    <div class="demo-card" style="margin:0" data-t="temps">
      <h3>👥 Recruter sans noyer</h3>
      <div class="demo-desc">CV pré-triés sur critères objectifs, questions d'entretien prêtes. La décision reste humaine.</div>
      <p style="margin:8px 0;font-size:14px"><strong>ROI :</strong> 30 min par candidature au lieu de 2 h.</p>
      <a class="btn btn-ghost" href="labo-demo.html?f=savoir">🧪 Tester →</a>
    </div>
  </div>

  <div class="aio-box" style="margin:24px 0">
    <h3 style="margin:0 0 6px">🤔 Je ne sais pas par où commencer ?</h3>
    <p style="margin:0 0 10px">Répondez à 5 questions simples : on détecte vos tâches répétitives et on vous propose les automatisations qui rapportent.</p>
    <a class="btn btn-primary" href="detecteur-taches.html">🎯 Trouver MES tâches à automatiser</a>
  </div>

  <div style="text-align:center;margin:28px 0 12px">
    <h2 style="margin:0 0 8px">15 minutes pour savoir si c'est pour vous.</h2>
    <p style="opacity:.9;margin:0 0 14px">On regarde vos 3 tâches les plus répétitives, on chiffre le temps gagné. Gratuit, sans engagement.</p>
    <a class="btn btn-primary" href="contact.html" style="font-size:17px;padding:13px 26px">📞 Réserver mon appel de 15 min</a>
  </div>
</main>"""

def main():
    html = open(PATH, encoding="utf-8").read()
    if "sol-grid" in html:
        print("solutions déjà redessiné")
        return
    m_b = re.search(r"<body[^>]*>", html)
    m_f = re.search(r"<footer", html)
    if not m_b or not m_f:
        print("structure introuvable")
        return
    header = html[:m_b.end()]
    footer = html[m_f.start():]
    # préserver la barre de navigation du site (sinon le redesign l'écrase)
    m_h = re.search(r"<header.*?</header>", html, flags=re.S)
    header_site = m_h.group(0) if m_h else ""
    open(PATH, "w", encoding="utf-8").write(header + "\n" + header_site + "\n" + BODY + "\n" + footer)
    print("solutions-par-besoin redessiné : filtres + recherche + cartes ROI")

if __name__ == "__main__":
    main()
