#!/usr/bin/env python3
"""Injection SEO idempotente sur toutes les pages du site :
- canonical + Open Graph + JSON-LD ProfessionalService dans <head>
- bouton WhatsApp flottant (mobile) avant </body>
Usage : python3 inject_seo.py  (relance après chaque régénération si besoin)
"""
import os
import re

SITE = "/root/consulting/site"
DOMAIN = "https://VOTRE-DOMAINE.fr"
EMAIL = "contact@votresite.fr"
WHATSAPP = "https://wa.me/33600000000?text=" + "Bonjour%2C%20je%20voudrais%20mes%2015%20minutes%20offertes"

JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService",
"name":"Jeremy : Consultant IA & Automatisation pour PME",
"description":"Automatisation et IA pour PME : devis, factures, relances, rapprochement bancaire, reporting. Audit gratuit.",
"url":"DOMAIN","email":"EMAIL","telephone":"+33600000000","priceRange":"€€",
"areaServed":{"@type":"Place","name":"France"},"address":{"@type":"PostalAddress","addressRegion":"Normandie"}}
</script>""".replace("DOMAIN", DOMAIN).replace("EMAIL", EMAIL)

WA = """<a href="WHATSAPP" class="wa-float" aria-label="Me contacter sur WhatsApp">💬</a>
<style>.wa-float{position:fixed;right:16px;bottom:16px;background:#1e7a4f;color:#fff;width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 4px 12px rgba(0,0,0,.25);z-index:999;text-decoration:none}@media(min-width:900px){.wa-float{display:none}}</style>""".replace("WHATSAPP", WHATSAPP)

def inject_aio(html):
    """Bloc 'En résumé' citable par les AI Overviews de Google, placé après le hero.
    Renvoie le html modifié, ou None si rien à faire."""
    if "aio-box" in html:
        return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return None
    h1 = re.sub(r"<[^>]+>", " ", m.group(1))
    h1 = re.sub(r"\s+", " ", h1).strip()
    m2 = re.search(r'<p class="sub"[^>]*>(.*?)</p>', html, re.S)
    sub = ""
    if m2:
        sub = re.sub(r"<[^>]+>", " ", m2.group(1))
        sub = re.sub(r"\s+", " ", sub).strip()
    text = sub or h1
    box = ('<div class="aio-box"><strong>En résumé :</strong> ' + text +
           '</div>\n<style>.aio-box{background:#f4faf6;border:1px solid #cfe8d8;border-left:4px solid #1e7a4f;border-radius:8px;padding:14px 18px;margin:22px auto;max-width:1100px;font-size:16px;line-height:1.55;color:#222;box-shadow:0 1px 3px rgba(0,0,0,.05)}.aio-box strong{color:#1e7a4f}</style>')
    m = re.search(r'<section class="hero".*?</section>', html, re.S)
    anchor = m.group(0) if m else "</header>"
    return html.replace(anchor, anchor + "\n" + box, 1)


def inject_theme(html):
    """Script de thème (anti-flash) + fonction toggle, inséré dans <head>."""
    if "theme-init" in html:
        return None
    script = """<script>/* theme-init */
(function(){try{var t=localStorage.getItem("theme");if(!t){t=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light";}document.documentElement.setAttribute("data-theme",t);}catch(e){document.documentElement.setAttribute("data-theme","light");}})();
function toggleTheme(){var r=document.documentElement;var next=r.getAttribute("data-theme")==="dark"?"light":"dark";r.setAttribute("data-theme",next);try{localStorage.setItem("theme",next);}catch(e){}}</script>"""
    return html.replace("</head>", script + "\n</head>")


def inject(path):
    html = open(path, encoding="utf-8").read()
    changed = []
    fname = os.path.basename(path)

    if 'rel="canonical"' not in html:
        m = re.search(r"<title>(.*?)</title>", html)
        title = m.group(1) if m else "Jeremy : Data Analyst · Automatisation &amp; IA"
        m2 = re.search(r'name="description" content="([^"]*)"', html)
        desc = m2.group(1) if m2 else "Automatisation et IA pour PME, expliquées simplement."
        og = (
            f'<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
            f'<link rel="canonical" href="{DOMAIN}/{fname}">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:locale" content="fr_FR">\n'
            f'<meta property="og:url" content="{DOMAIN}/{fname}">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n'
        )
        html = html.replace("</head>", og + "</head>")
        changed.append("canonical/OG/favicon")

    if "ProfessionalService" not in html:
        html = html.replace("</head>", JSONLD + "\n</head>")
        changed.append("JSON-LD")

    if "wa-float" not in html:
        html = html.replace("</body>", WA + "\n</body>")
        changed.append("WhatsApp float")

    # fermer le menu mobile/dropdown au clic extérieur (praticité)
    if "nav-close-js" not in html:
        js = ('<script>/* nav-close-js */document.addEventListener("click",function(e){'
              'var open=document.querySelectorAll("details[open]");'
              'open.forEach(function(d){if(!d.contains(e.target)&&(d.classList.contains("nav-mobile")||d.classList.contains("nav-drop"))){d.removeAttribute("open");}});});</script>')
        html = html.replace("</body>", js + "\n</body>")
        changed.append("nav-close JS")

    new_html = inject_aio(html)
    if new_html:
        html = new_html
        changed.append("bloc AIO")

    theme_html = inject_theme(html)
    if theme_html:
        html = theme_html
        changed.append("theme init")

    # toggle mobile (dans le menu burger) : idempotent
    if "theme-toggle-mobile" not in html:
        mobile_anchor = '<a class="btn btn-primary" href="contact.html">15 min offertes</a>\n      </nav>'
        if mobile_anchor in html:
            toggle_mobile = ('<button class="theme-toggle theme-toggle-mobile" onclick="toggleTheme()" aria-label="Changer de thème sombre/clair">'
                             '<span class="tt-moon">🌙</span><span class="tt-sun">☀️</span></button>\n'
                             + mobile_anchor)
            html = html.replace(mobile_anchor, toggle_mobile, 1)
            changed.append("theme mobile")

    # lien Abonnements dans le menu (desktop + mobile) : idempotent
    if "abonnements.html" not in html:
        desktop = '      <a href="demos.html">Démos</a>\n      <a href="tarifs.html">Tarifs</a>'
        if desktop in html:
            html = html.replace(desktop, '      <a href="demos.html">Démos</a>\n      <a href="abonnements.html">Abonnements</a>\n      <a href="tarifs.html">Tarifs</a>', 1)
        mobile = '        <a href="demos.html">Démos</a>\n        <a href="tarifs.html">Tarifs</a>'
        if mobile in html:
            html = html.replace(mobile, '        <a href="demos.html">Démos</a>\n        <a href="abonnements.html">Abonnements</a>\n        <a href="tarifs.html">Tarifs</a>', 1)
        changed.append("menu abonnements")

    # lien Labo dans le menu (desktop + mobile) : idempotent
    if "labo-demo.html" not in html:
        desk_labo = '      <a href="demos.html">Démos</a>\n      <a href="abonnements.html">Abonnements</a>'
        if desk_labo in html:
            html = html.replace(desk_labo, '      <a href="demos.html">Démos</a>\n      <a href="labo-demo.html">Labo</a>\n      <a href="abonnements.html">Abonnements</a>', 1)
        mob_labo = '        <a href="demos.html">Démos</a>\n        <a href="abonnements.html">Abonnements</a>'
        if mob_labo in html:
            html = html.replace(mob_labo, '        <a href="demos.html">Démos</a>\n        <a href="labo-demo.html">Labo</a>\n        <a href="abonnements.html">Abonnements</a>', 1)
        changed.append("menu labo")

    # hubs métiers + ressources dans le footer (maillage global) : idempotent
    if '<footer>' in html:
        if 'Réservoirs' not in html:
            hubs = '<span><strong>Réservoirs métiers :</strong> <a href="hub-artisans-btp.html">Artisans &amp; BTP</a> · <a href="hub-sante-bien-etre.html">Santé</a> · <a href="hub-tourisme-accueil.html">Tourisme</a> · <a href="hub-commerce-services.html">Commerce</a> · <a href="hub-transport-logistique.html">Transport</a> · <a href="hub-b2b-pro.html">B2B</a></span>'
            html = html.replace('</footer>', hubs + '</footer>')
            changed.append("footer hubs")
        if 'engagements-fiabilite.html' not in html and 'no-code-cest-quoi.html' in html:
            ress = '<span><strong>Ressources :</strong> <a href="formation-n8n.html">Formation n8n</a> · <a href="no-code-cest-quoi.html">No-code</a> · <a href="freelance-automatisation-n8n.html">Freelance</a> · <a href="newsletter.html">Newsletter</a> · <a href="engagements-fiabilite.html">🛡️ Engagements fiabilité</a></span>'
            html = html.replace('</footer>', ress + '</footer>')
            changed.append("footer ressources")
        if 'solutions-par-besoin.html' not in html:
            besoin = '<span><strong>Par besoin :</strong> <a href="solutions-par-besoin.html">💰 Encaisser</a> · <a href="solutions-par-besoin.html">📈 Vendre</a> · <a href="solutions-par-besoin.html">🤝 Servir</a> · <a href="solutions-par-besoin.html">🧠 Décider</a> · <a href="solutions-par-besoin.html">📋 En règle</a></span>'
            html = html.replace('</footer>', besoin + '</footer>')
            changed.append("footer besoins")
        if 'l-ia-peut-elle-se-tromper.html' not in html and 'engagements-fiabilite.html' in html:
            anti = '<span><strong>Fiabilité :</strong> <a href="engagements-fiabilite.html">🛡️ Engagements</a> · <a href="l-ia-peut-elle-se-tromper.html">🤔 L\u2019IA se trompe-t-elle ?</a></span>'
            html = html.replace('</footer>', anti + '</footer>')
            changed.append("footer fiabilite")
        if 'automatisations.html' not in html and 'solutions-par-besoin.html' in html:
            show = '<span><strong>Showroom :</strong> <a href="automatisations.html">Les 35 automatisations</a> · <a href="labo-demo.html">Labo (35 démos)</a></span>'
            html = html.replace('</footer>', show + '</footer>')
            changed.append("footer showroom")
        # Sources officielles en pied de page (TOUTES les pages) : idempotent
        if 'data-sources' not in html and '<footer>' in html:
                src_line = ('<span class="data-sources" style="font-size:12px;opacity:.75"><strong>Sources :</strong> '
                            '<a href="https://www.impots.gouv.fr" target="_blank" rel="noopener">impots.gouv.fr</a> · '
                            '<a href="https://www.facturation.gouv.fr" target="_blank" rel="noopener">facturation.gouv.fr (PPF)</a> · '
                            '<a href="https://eur-lex.europa.eu" target="_blank" rel="noopener">EUR-Lex (IA Act)</a> · '
                            '<a href="https://www.service-public.fr" target="_blank" rel="noopener">service-public.fr</a> · '
                            '<a href="https://www.insee.fr" target="_blank" rel="noopener">INSEE</a> · '
                            '<a href="https://annuaire-entreprises.data.gouv.fr" target="_blank" rel="noopener">annuaire-entreprises.data.gouv.fr</a> · '
                            '<a href="https://ec.europa.eu/taxation_customs/vies/" target="_blank" rel="noopener">VIES (UE)</a></span>')
                html = html.replace('</footer>', src_line + '</footer>')
                changed.append("footer sources")

    if changed:
        open(path, "w", encoding="utf-8").write(html)
    return changed

def main():
    total = 0
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html") and f != "404.html":
            ch = inject(os.path.join(SITE, f))
            if ch:
                print(f"{f}: {', '.join(ch)}")
                total += 1
    print(f"{total} pages modifiées")

if __name__ == "__main__":
    main()
