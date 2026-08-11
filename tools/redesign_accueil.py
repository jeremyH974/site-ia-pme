#!/usr/bin/env python3
"""Redesign de l'accueil : parcours d'onboarding 1-2-3 (choisir → tester → décider).
Les sections lourdes (Malt, Osez l'IA, pédagogie) sont repliées dans un accordéon.
Idempotent. À lancer après build_site + inject_seo + condense_footer.
Usage : python3 tools/redesign_accueil.py (dans /root/consulting/site/)
"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(SITE, "index.html")

BODY = """<main class="wrap">
  <div class="hero" style="padding:26px 0 18px;text-align:center">
    <p style="margin:0 0 6px;font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent,#3fae78)">Testez, c'est gratuit et instantané</p>
    <h1 style="font-size:clamp(28px,5vw,44px);line-height:1.15;margin:0 0 10px">Vous perdez des heures sur les devis, factures et relances&nbsp;?<br><em>On les automatise, et vous le voyez avant d'acheter.</em></h1>
    <p style="font-size:17px;opacity:.9;max-width:640px;margin:0 auto 18px">Je suis Jeremy, ex-contrôleur de gestion devenu data analyst en automatisation &amp; IA. Chaque solution est <strong>testable en direct</strong>, sans engagement.</p>
    <p style="margin:0 0 6px"><a class="btn btn-primary" href="labo-demo.html" style="font-size:17px;padding:13px 26px">🧪 Tester une démo (30 s)</a>&nbsp;&nbsp;<a class="btn btn-ghost" href="contact.html" style="font-size:17px;padding:13px 26px">📞 Appel 15 min gratuit</a></p>
    <p style="font-size:13px;opacity:.7;margin:8px 0 0">35 automatisations · 107 pages de guides · aucune donnée envoyée sans votre accord</p>
  </div>

  <h2 style="text-align:center;margin:26px 0 12px">Comment ça marche ? <span style="opacity:.7">3 étapes, 10 minutes</span></h2>
  <div class="hub-grid">
    <div class="demo-card" style="margin:0"><h3>1️⃣ Choisissez votre objectif</h3><div class="demo-desc">Encaisser plus vite, vendre mieux, servir vos clients, être en règle.</div><p style="margin:10px 0 0"><a class="btn btn-ghost" href="solutions-par-besoin.html">Voir les besoins →</a></p></div>
    <div class="demo-card" style="margin:0"><h3>2️⃣ Testez en direct</h3><div class="demo-desc">Chaque démo tourne vraiment : une IA génère le résultat sous vos yeux.</div><p style="margin:10px 0 0"><a class="btn btn-ghost" href="labo-demo.html">Ouvrir le Labo →</a></p></div>
    <div class="demo-card" style="margin:0"><h3>3️⃣ Décidez, sans pression</h3><div class="demo-desc">Un appel de 15 min pour voir ce que ça vaut CHEZ vous, chiffres à l'appui.</div><p style="margin:10px 0 0"><a class="btn btn-ghost" href="contact.html">Réserver l'appel →</a></p></div>
  </div>

  <h2 style="text-align:center;margin:26px 0 12px">Votre objectif, d'abord</h2>
  <div class="hub-grid">
    <div class="demo-card" style="margin:0"><h3>💰 Encaisser</h3><div class="demo-desc">Relances impayés, rapprochement, facture électronique.</div><a class="btn btn-ghost" href="labo-demo.html?f=encaisser">Tester →</a></div>
    <div class="demo-card" style="margin:0"><h3>📈 Vendre</h3><div class="demo-desc">Devis 24/7, relance de devis, prospection.</div><a class="btn btn-ghost" href="labo-demo.html?f=vendre">Tester →</a></div>
    <div class="demo-card" style="margin:0"><h3>🤝 Servir</h3><div class="demo-desc">RDV, avis, support, clients perdus de vue.</div><a class="btn btn-ghost" href="labo-demo.html?f=servir">Tester →</a></div>
    <div class="demo-card" style="margin:0"><h3>🧠 Décider</h3><div class="demo-desc">Briefing, reporting, veille, clôture.</div><a class="btn btn-ghost" href="labo-demo.html?f=savoir">Tester →</a></div>
    <div class="demo-card" style="margin:0"><h3>📋 Être en règle</h3><div class="demo-desc">Facture élec, IA Act, transparence IA.</div><a class="btn btn-ghost" href="labo-demo.html?f=conformite">Tester →</a></div>
    <div class="demo-card" style="margin:0"><h3>💊 Santé</h3><div class="demo-desc">Ordonnancier, entrée en relation, rappels.</div><a class="btn btn-ghost" href="labo-demo.html?f=sante">Tester →</a></div>
  </div>

  <div class="aio-box" style="margin:22px 0">
    <details><summary style="cursor:pointer;font-weight:600">💡 Pourquoi maintenant ? (cliquez pour voir)</summary>
      <div style="padding-top:10px">
        <p><strong>Le marché explose.</strong> Source : <a href="https://www.malt.fr" target="_blank" rel="noopener">rapport Malt Tech Trends 2026</a> : ×60 de demandes d'agents IA en 1 an, ×14 pour n8n, +125 % IA en tête des compétences demandées, TJM 400-700 €/jour.</p>
        <p><strong>L'État encourage.</strong> Le plan national <a href="https://www.economie.gouv.fr/actualites/osez-lia-un-plan-pour-diffuser-lia-dans-toutes-les-entreprises" target="_blank" rel="noopener">« Osez l'IA »</a> (1er juillet 2025) accompagne les TPE/PME : sensibilisation, formation, accompagnement : <a href="https://www.entreprises.gouv.fr/priorites-et-actions/transition-numerique" target="_blank" rel="noopener">France 2030</a> mobilisé.</p>
        <p><strong>Une obligation arrive.</strong> La facturation électronique : réception 01/09/2026, émission 01/09/2027 : le bilan de conformité est <a href="labo-demo.html?f=conformite">testable ici</a>.</p>
      </div>
    </details>
  </div>

  <div style="text-align:center;margin:30px 0 14px">
    <h2 style="margin:0 0 8px">15 minutes pour savoir si c'est pour vous.</h2>
    <p style="opacity:.9;margin:0 0 14px">On regarde vos 3 tâches les plus répétitives, on chiffre le temps gagné. Gratuit, sans engagement.</p>
    <a class="btn btn-primary" href="contact.html" style="font-size:18px;padding:14px 30px">📞 Réserver mon appel de 15 min</a>
  </div>
</main>"""

def main():
    html = open(IDX, encoding="utf-8").read()
    if "1️⃣ Choisissez votre objectif" in html:
        print("accueil déjà redessiné")
        return
    # extraire header (avant <main) et footer (depuis <footer)
    m_main = re.search(r"<body[^>]*>", html)
    m_foot = re.search(r"<footer", html)
    if not m_main or not m_foot:
        print("structure introuvable")
        return
    header = html[:m_main.end()]
    footer = html[m_foot.start():]
    # préserver la barre de navigation du site (sinon le redesign l'écrase)
    m_h = re.search(r"<header.*?</header>", html, flags=re.S)
    header_site = m_h.group(0) if m_h else ""
    open(IDX, "w", encoding="utf-8").write(header + "\n" + header_site + "\n" + BODY + "\n" + footer)
    print("accueil redessiné : parcours 1-2-3")

if __name__ == "__main__":
    main()
