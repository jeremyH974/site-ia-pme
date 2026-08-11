#!/usr/bin/env python3
"""Condense le footer de toutes les pages : 9 lignes → 3 (nav, ressources, sources).
Idempotent : marqueur 'footer-condense'. À lancer après inject_seo.
Usage : python3 tools/condense_footer.py (dans /root/consulting/site/)
"""
import os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEW_FOOTER = """<footer class="footer-condensed footer-v2"><div class="wrap footer-grid">
  <div class="footer-brand">
    <p class="footer-logo">Jeremy, Data Analyst · Automatisation &amp; IA</p>
    <p class="footer-tagline">Des automatisations testables en direct, sourcées, sans jargon.</p>
    <a class="btn btn-primary" href="contact.html">📞 15 min offertes</a>
  </div>
  <nav class="footer-col" aria-label="Explorer">
    <p class="footer-title">Explorer</p>
    <a href="index.html">Accueil</a>
    <a href="solutions-par-besoin.html">Solutions par besoin</a>
    <a href="automatisations.html">Les 35 automatisations</a>
    <a href="labo-demo.html">Labo (démos en direct)</a>
  </nav>
  <nav class="footer-col" aria-label="Ressources">
    <p class="footer-title">Ressources</p>
    <a href="guides.html">Guides</a>
    <a href="formation-n8n.html">Formation n8n</a>
    <a href="no-code-cest-quoi.html">No-code</a>
    <a href="freelance-automatisation-n8n.html">Freelance n8n</a>
    <a href="consultant-ia-pme.html">Consultant IA PME</a>
    <a href="engagements-fiabilite.html">🛡️ Fiabilité</a>
    <a href="l-ia-peut-elle-se-tromper.html">🤔 L'IA se trompe-t-elle ?</a>
    <a href="a-propos.html">À propos</a>
  </nav>
  <nav class="footer-col" aria-label="Métiers">
    <p class="footer-title">Métiers</p>
    <a href="hub-artisans-btp.html">Artisans &amp; BTP</a>
    <a href="hub-sante-bien-etre.html">Santé</a>
    <a href="hub-tourisme-accueil.html">Tourisme</a>
    <a href="hub-commerce-services.html">Commerce</a>
    <a href="hub-transport-logistique.html">Transport</a>
    <a href="hub-b2b-pro.html">B2B &amp; pro</a>
  </nav>
</div>
<div class="wrap footer-bottom">
  <span class="data-sources" style="font-size:11px;opacity:.7">Sources : <a href="https://www.impots.gouv.fr" target="_blank" rel="noopener">impots.gouv.fr</a> · <a href="https://www.facturation.gouv.fr" target="_blank" rel="noopener">facturation.gouv.fr</a> · <a href="https://eur-lex.europa.eu" target="_blank" rel="noopener">EUR-Lex</a> · <a href="https://www.service-public.fr" target="_blank" rel="noopener">service-public.fr</a> · <a href="https://www.insee.fr" target="_blank" rel="noopener">INSEE</a> · <a href="https://ec.europa.eu/taxation_customs/vies/" target="_blank" rel="noopener">VIES</a></span>
  <p style="margin:4px 0 0;font-size:12px;opacity:.8">© 2026 Jeremy : Data Analyst · Automatisation &amp; IA · <a href="confidentialite.html">Confidentialité</a> · <a href="mentions-legales.html">Mentions légales</a></p>
</div></footer>"""

def main():
    n = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        p = os.path.join(SITE, f)
        html = open(p, encoding="utf-8").read()
        # remplacer TOUJOURS le footer (ancien ou déjà condensé) → idempotent
        m = re.search(r"<footer.*?</footer>", html, flags=re.S)
        if not m:
            continue
        # préserver les widgets démo insérés avant le footer (testV)
        old_footer = m.group(0)
        widgets = re.findall(r'<div class="aio-box"[^>]*>\s*<h3[^>]*>🧪 Testez en direct.*?</div>\s*</div>', old_footer, flags=re.S)
        widgets_html = "\n".join(widgets)
        html = html[:m.start()] + (widgets_html + "\n" if widgets_html else "") + NEW_FOOTER + html[m.end():]
        open(p, "w", encoding="utf-8").write(html)
        n += 1
    print(f"footer condensé sur {n} pages")

if __name__ == "__main__":
    main()
