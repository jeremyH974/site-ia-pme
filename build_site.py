#!/usr/bin/env python3
"""Générateur du site : template unique 'gérant perdu'.
Reconstruit les pages SEO à partir de contenus structurés.
Usage : python3 build_site.py
"""
import json
import os
import re

SITE = "/root/consulting/site"

NAV_V4 = '<header class="site-header nav-v4"><!-- nav-v4 -->\n  <div class="wrap header-inner">\n    <a class="brand" href="index.html">Jeremy<span>, Data Analyst · Automatisation &amp; IA</span></a>\n    <nav class="main-nav" aria-label="Navigation principale">\n      <a href="index.html">Accueil</a>\n      <a href="solutions-par-besoin.html">Solutions</a>\n      <a href="guides.html">Guides</a>\n      <a href="demos.html">Démos</a>\n      \n      <button class="theme-toggle" onclick="toggleTheme()" aria-label="Changer de thème sombre/clair"><span class="tt-moon">🌙</span><span class="tt-sun">☀️</span></button>\n      <a class="btn btn-primary nav-cta" href="contact.html">15 min offertes</a>\n    </nav>\n    <details class="nav-mobile">\n      <summary>☰ Menu</summary>\n      <nav aria-label="Navigation mobile">\n        <a href="index.html">Accueil</a>\n        <a href="detecteur-taches.html">🎯 Trouver mes tâches</a>\n        <a href="automatiser-devis.html">Devis &amp; factures</a>\n        <a href="relance-impayes.html">Relances &amp; impayés</a>\n        <a href="service-client.html">Service client &amp; avis</a>\n        <a href="compte-rendu-reunion.html">Comptes-rendus &amp; RDV</a>\n        <a href="index.html#solutions">Toutes les solutions →</a>\n        <a href="guides.html">Guides gratuits</a>\n        <a href="demos.html">Démos</a>\n        \n        <a class="btn btn-primary" href="contact.html">15 min offertes</a>\n      </nav>\n    </details>\n  </div>\n</header>'

BRAND_HEADER = NAV_V4

BRAND_HEADER = NAV_V4

FOOTER = """<footer>
  <div class="wrap">
    <span>© 2026 Jeremy : Consultant IA &amp; Automatisation pour PME</span>
    <span><a href="index.html">Accueil</a> · <a href="guides.html">Guides</a> · <a href="demos.html">Démos</a> · <a href="methode.html">Méthode</a> ·  · <a href="newsletter.html">Newsletter</a> · <a href="quiz.html">Test 2 min</a> · <a href="mentions-legales.html">Mentions légales</a> · <a href="confidentialite.html">Confidentialité</a></span>
  </div>
</footer>"""

def header(title, meta, h1, sub, eyebrow="Pédagogie : 2 minutes chrono"):
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="stylesheet" href="style.css">
</head>
<body>

{BRAND_HEADER}

<section class="hero">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="contact.html">Voir si ça marche pour moi</a>
      <a class="btn btn-ghost" href="guide-du-pain-automatise.html">Télécharger le guide gratuit</a>
    </div>
  </div>
</section>"""

def section(label, h2, inner):
    return f"""<section>
  <div class="wrap">
    <span class="section-label">{label}</span>
    <h2>{h2}</h2>
    {inner}
  </div>
</section>"""

def prose(html):
    return f'<div class="prose">{html}</div>'

def pains(rows):
    out = ['<div class="pains">']
    for task, small, before, after in rows:
        out.append(f"""      <div class="pain-row">
        <div class="task">{task}<small>{small}</small></div>
        <div class="before">{before}</div>
        <div class="after"><strong>{after}</strong></div>
      </div>""")
    out.append("    </div>")
    return "\n".join(out)

def value_box(title, items):
    lis = "".join(f"<li>{it}</li>" for it in items)
    return f"""<div class="cta-inline">
  <h3 style="margin-bottom:10px">{title}</h3>
  <ul style="margin:0 0 14px 18px">{lis}</ul>
  <a class="btn btn-primary" href="contact.html">Recevoir ma version personnalisée</a>
</div>"""

def faq(pairs):
    details = "".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in pairs)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
    return f"""<div class="faq">{details}</div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>"""

def nav(links):
    lis = "".join(f'<a href="{f}">{t}</a>' for f, t in links)
    return f'<div class="page-nav">{lis}</div>'

def build(page, sections_html, faq_pairs, nav_links, footer_extra=""):
    html = header(page["title"], page["meta"], page["h1"], page["sub"], page.get("eyebrow", "Pédagogie : 2 minutes chrono"))
    clean_h1 = re.sub(r"<[^>]+>", "", page["h1"])
    html += f'<nav class="breadcrumb" aria-label="Fil d\'Ariane"><a href="index.html">Accueil</a> › {clean_h1}</nav>'
    html += "\n".join(sections_html)
    html += section("Vos questions, sans détour", "Les questions que tout le monde se pose", faq(faq_pairs))
    html += section("On passe à votre cas ?", "15 minutes pour savoir si c'est pour vous.",
                    f"""<div class="cta-inline"><p><strong>Un échange simple, sans jargon, sans engagement.</strong> Vous repartez avec au moins une idée concrète pour votre entreprise.</p>
<a class="btn btn-primary" href="contact.html">Réserver mes 15 minutes offertes</a>
<a class="btn btn-ghost" href="tarifs.html">Voir les tarifs</a></div>""")
    html += section("Continuer à explorer", "Tout comprendre, simplement", nav(nav_links))
    html += FOOTER + footer_extra + "\n\n</body>\n</html>\n"
    return html

PAGES = [
    dict(
        file="facturation-electronique-2026.html",
        title="Facturation électronique 2026 : ce que les PME doivent savoir (simplement)",
        meta="La réforme de la facturation électronique inquiète les PME. Voici l'essentiel en 2 minutes : qui est concerné, quand, et comment s'y préparer sans stress.",
        h1="Facturation électronique : <em>ce que les PME doivent savoir.</em>",
        sub="Vous avez reçu des mails inquiétants sur la « réforme de la facturation électronique » ? On vous explique calmement : ce qui change, quand, et ce que vous avez à faire.",
        sections=[
            section("En 30 secondes", "Ce qui change, simplement",
                prose("<p>La facturation électronique devient obligatoire en France, <strong>progressivement et sans report</strong>. Concrètement : vos factures devront circuler dans un format électronique standardisé.</p>"
                      "<p><strong>Le calendrier officiel (confirmé) :</strong></p>"
                      "<p>📅 <strong>1er septembre 2026</strong> : toutes les entreprises doivent pouvoir <strong>RECEVOIR</strong> des factures électroniques ; les grandes entreprises doivent <strong>émettre</strong>.<br>"
                      "📅 <strong>1er septembre 2027</strong> : toutes les PME et TPE doivent <strong>émettre</strong> ; démarrage de l'e-reporting pour les ventes aux particuliers.</p>"
                      "<p>⚠️ Les rumeurs de report circulent : <strong>le calendrier officiel est confirmé</strong>. Vérifiez toujours sur <strong>impots.gouv.fr</strong>, la source qui fait foi.</p>"
                      "<p>La bonne nouvelle : ce n'est pas une usine à gaz. La plupart des logiciels de facturation s'en occupent déjà. Et si vous n'avez pas encore de logiciel, c'est le moment d'en profiter pour automatiser toute votre facturation.</p>")),
            section("Les 3 erreurs à éviter", "Ce que font ceux qui vont galérer",
                pains([
                    ("Attendre septembre", "« On verra bien »", "Les outils se prennent en 2 semaines, pas en 2 jours", "Ceux qui commencent maintenant sont sereins en septembre"),
                    ("Croire que ça ne concerne pas les petites boîtes", "« C'est pour les grands »", "Toutes les entreprises sont concernées, y compris les micro-entreprises", "Une vérification de 10 min suffit pour savoir où vous en êtes"),
                    ("Voir la réforme comme une contrainte", "« Encore de la paperasse »", "Vous continuez à faire les factures à la main, en plus du nouveau format", "Ceux qui en profitent automatisent le tri, l'extraction et les relances en même temps"),
                ])),
            section("Ce que la réforme peut vous apporter", "L'occasion d'automatiser toute votre facturation",
                pains([
                    ("Trier les factures reçues", "Sans rien toucher à vos habitudes", "Chaque facture fournisseur ouverte et lue à la main", "Tri automatique + alerte sur l'urgent"),
                    ("Extraire les montants et dates", "Fini la saisie", "Montants recopiés, erreurs de frappe", "Extraction automatique dans un tableau"),
                    ("Préparer le rapprochement bancaire", "Votre clôture vous dit merci", "3 heures par mois à la clôture", "30 secondes, écarts détectés seuls"),
                ])),
            section("Votre crainte, honnêtement", "« C'est encore une usine à gaz ? »",
                prose("<p><strong>Non.</strong> Le principe est simple : vos factures circulent dans un format standard, comme des emails. Vous n'aurez rien à comprendre de la technique.</p>"
                      "<p><strong>« Je vais devoir tout changer ? »</strong> Pas forcément : on se branche sur ce que vous utilisez déjà (Excel, Gmail, votre logiciel).</p>"
                      "<p><strong>« Et si je ne fais rien ? »</strong> Vous risquez des pénalités et des clients qui ne peuvent plus vous payer. C'est le moment d'y voir clair : 15 minutes suffisent pour savoir où vous en êtes.</p>")),
        ],
        faq=[
            ("La facturation électronique, c'est quoi exactement ?", "C'est l'obligation de transmettre et recevoir les factures dans un format électronique standardisé (Factur-X, UBL, CII), au lieu d'un PDF envoyé par mail. Le but : que toutes les entreprises parlent le même langage."),
            ("La réforme a-t-elle été reportée ?", "Non : le calendrier officiel est confirmé. 1er septembre 2026 : réception pour toutes + émission pour les grandes entreprises. 1er septembre 2027 : émission pour PME/TPE + e-reporting B2C. Beaucoup de rumeurs circulent : vérifiez toujours sur impots.gouv.fr."),
            ("Qui est concerné ?", "Toutes les entreprises assujetties à la TVA, progressivement : réception dès septembre 2026 pour toutes, émission en septembre 2026 pour les grandes entreprises, puis septembre 2027 pour les PME, TPE et micro-entreprises."),
            ("PDP, c'est quoi ? (je vois ce mot partout)", "PDP = Plateforme de Dématérialisation Partenaire. C'est simplement un prestataire certifié qui transmet vos factures électroniques pour vous (souvent votre logiciel de facturation en fait partie). Vous n'avez pas besoin d'en choisir un vous-même si votre outil le fait déjà."),
            ("Quel logiciel de facturation électronique gratuit choisir ?", "Plusieurs logiciels gratuits existent (facture.net, Zervant, Wave...). Le bon choix dépend de votre volume et de votre activité : l'important est qu'il soit conforme et qu'il accepte les formats officiels. L'audit gratuit vous aide à trancher en 15 minutes."),
            ("Ça coûte cher de s'y mettre ?", "Si vous utilisez déjà un logiciel de facturation, c'est souvent déjà géré. Sinon, des solutions gratuites ou peu chères existent. Un audit de 15 min permet d'y voir clair."),
            ("Pourquoi automatiser en même temps ?", "Parce que la réforme touche exactement là où vous perdez du temps : tri des factures, saisie des montants, rapprochement. Autant en profiter pour gagner 3 heures par mois."),
        ],
        nav_links=[("automatiser-factures.html", "Automatiser les factures"), ("rapprochement-bancaire-excel.html", "Rapprochement bancaire"), ("automatiser-devis.html", "Automatiser les devis"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="consultant-ia-pme.html",
        title="Data Analyst · Automatisation &amp; IA : comment ça marche, concrètement ?",
        meta="Vous êtes dirigeant et vous n'avez pas le temps ? Voici ce qu'un consultant IA fait (et ne fait pas) pour une PME : audit, ROI chiffré, déploiement, formation.",
        h1="Data Analyst · Automatisation &amp; IA : <em>comment ça marche, concrètement ?</em>",
        sub="Vous avez vu « consultant IA » partout sans savoir ce que ça change pour une petite entreprise. Voici exactement ce que je fais (et ce que je ne fais pas), sans magie et sans jargon.",
        sections=[
            section("Ce que je fais", "Concrètement, pour votre entreprise",
                pains([
                    ("L'audit gratuit (48h)", "Étape 1, sans engagement", "On parle de vos tâches, de vos outils, de vos pertes de temps", "Je repère vos 5 tâches les plus automatisables"),
                    ("La proposition avec ROI chiffré", "Étape 2", "Vous ne savez pas ce que l'automatisation vaut pour vous", "Vous savez exactement : X heures et Y euros gagnés par an"),
                    ("Le déploiement (1 à 4 semaines)", "Étape 3", "Vous continuez à tout faire à la main", "L'automatisation tourne, testée, avec votre équipe formée"),
                ])),
            section("Ce que je ne fais pas", "Pour éviter les mauvaises surprises",
                prose("<p><strong>Pas de magie.</strong> L'IA ne résout pas tout : on automatise ce qui est répétitif et règle. Pas de promesse irréaliste.</p>"
                      "<p><strong>Pas de jargon.</strong> Si je ne peux pas expliquer simplement ce que je vais faire, c'est que je n'ai pas compris moi-même.</p>"
                      "<p><strong>Pas de dépendance.</strong> Vous restez propriétaire de vos outils et de vos données. Si on arrête de travailler ensemble, tout continue de tourner.</p>")),
            section("Combien ça coûte ?", "Moins que le temps perdu",
                prose("<p>Chaque entreprise est différente : l'automatisation d'un reporting ne coûte pas la même chose que celle de toute la facturation. La règle est simple : <strong>jamais de dépense avant un ROI chiffré.</strong></p>"
                      "<p>Pour vous donner un ordre d'idée, les agents IA « tri d'emails » ou « réponse de devis » se chiffrent en quelques milliers d'euros, pour plusieurs heures gagnées chaque semaine, chaque année.</p>")),
            section("Garantie", "Le risque est de mon côté",
                prose("<p><strong>Si ce n'est pas automatisé, vous ne payez pas.</strong> C'est la promesse qui rend la décision facile : vous testez, vous vérifiez le résultat, et seulement si ça marche, ça vous coûte quelque chose.</p>")),
        ],
        faq=[
            ("Un consultant IA, c'est pour les grandes entreprises ?", "Non : c'est même là où les PME gagnent le plus, parce qu'elles n'ont personne de dédié aux tâches répétitives. Une heure gagnée par semaine, c'est déjà 46 heures par an."),
            ("Il faut y comprendre quelque chose ?", "Non, c'est le principe. Vous décrivez votre quotidien, je m'occupe de la technique. Vous regardez le résultat."),
            ("Et si ça ne marche pas chez moi ?", "L'audit gratuit permet de le savoir avant de dépenser quoi que ce soit. Et la garantie « sinon vous ne payez pas » protège la suite."),
            ("Combien de temps avant de voir des résultats ?", "Les premières automatisations tournent souvent en 1 à 4 semaines. Le temps de gagner du temps est très court."),
        ],
        nav_links=[("agent-ia-cest-quoi.html", "Agent IA, c'est quoi ?"), ("methode.html", "La méthode en détail"), ("quiz.html", "Test de maturité 2 min"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="relance-impayes.html",
        title="Relancer les impayés : le modèle en 3 paliers (+ l'automatisation)",
        meta="80 % des impayés se règlent avec une relance polie. Voici le modèle de relance en 3 paliers, et comment l'automatiser pour ne plus jamais oublier.",
        h1="Relancer les impayés : <em>le modèle qui marche.</em>",
        sub="Une facture impayée, ce n'est pas un drame : c'est une facture qui attend une relance. Voici le modèle en 3 paliers que j'utilisais comme contrôleur de gestion, et comment l'automatiser.",
        sections=[
            section("Le réflexe qui manque", "Pourquoi les impayés s'éternisent",
                prose("<p>Ce n'est pas la mauvaise foi qui fait traîner les impayés : c'est l'oubli. Et de votre côté, c'est la même chose : vous repoussez la relance « parce que pas le temps ».</p>"
                      "<p>La règle est connue : <strong>80 % des impayés se règlent avec une relance polie et rapide.</strong> Le problème, c'est de la faire à chaque fois.</p>")),
            section("Le modèle en 3 paliers", "Ce que vous repartez avec (gratuit)",
                pains([
                    ("Palier 1 : J+7 : courtois", "« Peut-être un oubli »", "Facture impayée sans relance", "Email amical : « vérifiez si le paiement est parti » : règle 80 % des cas"),
                    ("Palier 2 : J+21 : ferme", "« On en parle ? »", "Rien ne bouge", "Relance directe avec rappel des conditions, proposition d'échéancier"),
                    ("Palier 3 : J+35 : ultimatum", "« Dernier recours »", "Toujours rien", "Mise en demeure + pénalités de retard : à ce stade, la relation est déjà en jeu"),
                ])),
            section("La version automatique", "Plus jamais de relance oubliée",
                pains([
                    ("Le déclencheur", "Une facture arrive à échéance", "Vous notez mentalement de relancer... et vous oubliez", "L'automatisation suit le calendrier à votre place"),
                    ("La relance", "Le bon message, au bon moment", "Relances incohérentes, ton différent à chaque fois", "Le palier 1 part tout seul, le 2 aussi si rien ne bouge"),
                    ("L'alerte", "Vous restez maître", "Vous découvrez l'impayé 3 mois plus tard", "Vous êtes notifié à chaque étape, vous décidez de la suite"),
                ])),
            section("Votre crainte, honnêtement", "« Relancer, ça braque le client ? »",
                prose("<p>Le contraire : <strong>un client qui paie en retard apprécie qu'on le lui rappelle poliment</strong>. C'est vous rendre service que de tenir votre trésorerie à jour.</p>"
                      "<p>Et un relance automatique n'est pas froide : on l'écrit pour être courtoise, personnalisée avec le nom du client et le numéro de facture. Comme si vous l'aviez écrite vous-même.</p>")),
        ],
        faq=[
            ("Quand relancer une facture impayée ?", "La règle des 3 paliers : courtois à J+7, ferme à J+21, ultimatum à J+35. Plus c'est rapide, plus ça se règle vite."),
            ("La relance automatique, c'est impersonnel ?", "Non : chaque message est personnalisé (nom du client, numéro de facture, montant) et rédigé sur un ton humain. Vous gardez la main sur les paliers 2 et 3."),
            ("Et si le client ne répond à aucun palier ?", "Au palier 3, on passe aux conditions contractuelles : pénalités, mise en demeure. L'automatisation vous alerte pour que vous décidiez de la suite."),
            ("Ça marche avec mon logiciel de compta ?", "Dans la grande majorité des cas, oui : on se branche sur vos emails et vos fichiers existants. Vérification gratuite pendant l'audit."),
        ],
        nav_links=[("automatiser-factures.html", "Automatiser les factures"), ("rapprochement-bancaire-excel.html", "Rapprochement bancaire"), ("automatiser-devis.html", "Automatiser les devis"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="repondre-avis-google.html",
        title="Répondre aux avis Google : le réflexe qui vous fait gagner des clients",
        meta="Les clients lisent vos réponses aux avis. Voici pourquoi répondre change tout, le modèle de réponse simple, et comment l'IA s'en charge automatiquement.",
        h1="Répondre aux avis Google : <em>le réflexe qui rapporte.</em>",
        sub="Un client sur deux choisit son prestataire en regardant les avis. Et vos réponses comptent autant que les avis eux-mêmes. Voici pourquoi, et comment ne plus jamais laisser un avis sans réponse.",
        sections=[
            section("Pourquoi c'est important", "Vos réponses valent de l'or",
                prose("<p>Quand un client hésite entre vous et un concurrent, il regarde vos avis <strong>et vos réponses</strong>. Une réponse polie et rapide montre que vous prenez soin de vos clients.</p>"
                      "<p>Un avis négatif sans réponse : vous perdez le client qui lisait. Un avis négatif avec une réponse construite : vous le rassurez, et vous montrez que vous savez gérer les problèmes.</p>")),
            section("Le modèle simple", "Ce que vous repartez avec (gratuit)",
                pains([
                    ("Avis positif", "« Merci ! » en 2 phrases", "Pas de réponse, un client qui se sent ignoré", "Merci + une précision personnelle + invitation à revenir"),
                    ("Avis négatif", "La réponse qui désamorce", "Réponse défensive ou... silence", "Merci du retour + excuse courte + solution proposée + invitation à en parler en privé"),
                    ("Le réflexe régularité", "Toujours répondre", "Oublis, réponses en rafale une fois par mois", "Une réponse à chaque avis, sous 48h"),
                ])),
            section("La version automatique", "L'IA répond à votre place",
                pains([
                    ("L'IA rédige", "En suivant votre ton", "Chaque réponse à écrire, le ton qui varie", "Une réponse personnalisée, validée par vous avant envoi"),
                    ("Vous validez", "Vous gardez la main", "Peur que l'IA dise n'importe quoi", "L'IA propose, vous approuvez en 1 clic : ou vous ajustez"),
                    ("La demande d'avis", "Post-achat automatique", "Des clients contents mais silencieux", "Une demande d'avis polie envoyée automatiquement après chaque prestation"),
                ])),
            section("Votre crainte, honnêtement", "« Je n'ai pas le temps d'écrire des réponses. »",
                prose("<p>Justement : c'est une des tâches les plus faciles à automatiser, parce que les réponses se ressemblent. L'IA connaît votre ton, elle propose, vous validez.</p>"
                      "<p>Et la demande d'avis automatique après chaque prestation fait grimper votre note et votre visibilité : sans que vous y pensiez.</p>")),
        ],
        faq=[
            ("Pourquoi répondre aux avis Google ?", "Parce que les clients qui hésitent lisent vos réponses : elles montrent que vous prenez soin de vos clients. Un avis sans réponse, c'est une occasion perdue."),
            ("L'IA peut répondre à ma place ?", "Oui : elle rédige une réponse personnalisée dans votre ton, et vous la validez avant envoi. Vous gardez toujours le contrôle."),
            ("Comment obtenir plus d'avis ?", "En demandant, simplement : une demande d'avis automatique après chaque prestation, au bon moment, fait toute la différence."),
            ("Et les avis négatifs ?", "Une réponse polie qui propose une solution désamorce la plupart des situations. Les clients qui lisent retiennent votre professionnalisme."),
        ],
        nav_links=[("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("prise-rendez-vous.html", "Rappels de rendez-vous"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="compte-rendu-reunion.html",
        title="Compte-rendu de réunion automatique : l'IA s'en charge",
        meta="Finies les heures à rédiger des comptes-rendus. Transcription + résumé IA : décisions, actions, responsables. Exemple concret et gratuit.",
        h1="Compte-rendu de réunion : <em>l'IA s'en charge.</em>",
        sub="Une réunion d'une heure = une heure de compte-rendu. Voici comment l'IA transforme votre réunion en compte-rendu clair, en quelques secondes. Exemple à l'appui.",
        sections=[
            section("Le problème", "La réunion finie, le vrai travail commence",
                prose("<p>Vous sortez de réunion, tout le monde était d'accord... et trois jours plus tard, personne ne se souvient de qui devait faire quoi. Le compte-rendu, c'est ce qui transforme une discussion en décisions, mais personne n'a le temps de le rédiger.</p>")),
            section("L'exemple", "Voici ce que l'IA produit (gratuit)",
                """<div class="example-box">
<span class="in">→ Réunion du 24/07 · 45 min · 4 participants</span><br><br>
<strong>Décisions</strong><br>
• Lancer la nouvelle gamme en septembre<br>
• Passer le reporting en automatique (moins de 2h/semaine)<br><br>
<strong>Actions</strong><br>
• [Julie] Contacter le fournisseur avant vendredi<br>
• [Marc] Préparer le budget : avant le 31/07<br>
• [Tout le monde] Tester le rapport automatique cette semaine<br><br>
<strong>Prochaine réunion</strong> : jeudi 31/07, 9h
</div>"""),
            section("Comment ça marche", "Simple comme une réunion",
                pains([
                    ("1. L'enregistrement", "Teams, Zoom, Google Meet ou un téléphone", "Quelqu'un note frénétiquement", "L'audio est enregistré, personne ne note plus"),
                    ("2. La transcription", "Tout ce qui a été dit, écrit", "Les notes incomplètes, les décisions perdues", "La transcription complète est générée"),
                    ("3. Le compte-rendu", "Décisions, actions, responsables, dates", "3 heures de rédaction", "Le résumé clair est prêt en quelques secondes"),
                ])),
            section("Votre crainte, honnêtement", "« L'IA va rater les sous-entendus. »",
                prose("<p>La transcription complète reste disponible : le compte-rendu résume, mais rien n'est perdu. Et vous relisez le compte-rendu avant de l'envoyer : 2 minutes au lieu de 2 heures.</p>")),
        ],
        faq=[
            ("Ça marche avec quels outils ?", "Teams, Zoom, Google Meet, et même un simple enregistrement téléphonique. La transcription se fait ensuite automatiquement."),
            ("Le compte-rendu est-il fiable ?", "Il reprend ce qui a été dit, structure les décisions et les actions. Vous le relisez et le corrigez avant envoi : 2 minutes au lieu de 2 heures."),
            ("Et la confidentialité ?", "Les enregistrements et transcriptions restent chez vous, sur vos outils. Rien ne part chez un tiers."),
            ("Est-ce que ça remplace le secrétariat ?", "Ça libère le secrétariat de la saisie pour le confier à la vérification et au suivi des actions : le travail qui a de la valeur."),
        ],
        nav_links=[("repondre-avis-google.html", "Répondre aux avis Google"), ("automatiser-excel.html", "Automatiser Excel"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="prise-rendez-vous.html",
        title="Rappels de rendez-vous automatiques : stop aux rendez-vous manqués",
        meta="Les rendez-vous manqués coûtent cher : 1 client sur 10 ne vient pas. Les rappels automatiques par SMS, WhatsApp ou email réduisent les absences. Explication simple.",
        h1="Rendez-vous manqués : <em>le rappel qui change tout.</em>",
        sub="Un rendez-vous sur dix est manqué, faute de rappel. Un simple message automatique avant le RDV réduit fortement les absences. Voici comment ça marche, simplement.",
        sections=[
            section("Le problème", "Ce que les rendez-vous manqués vous coûtent",
                prose("<p>Chaque rendez-vous manqué, c'est du temps perdu et de l'argent perdu. Et dans la plupart des cas, ce n'est pas de la mauvaise volonté : <strong>c'est un oubli.</strong> Un rappel bien envoyé règle le problème.</p>")),
            section("Ce que vous repartez avec", "Le principe du rappel en 3 temps",
                pains([
                    ("La confirmation", "Dès la prise de RDV", "Le client note le RDV sur un ticket et le perd", "Un message de confirmation avec la date, l'heure et l'adresse"),
                    ("Le rappel J-2", "Le bon moment", "Le client oublie jusqu'au jour J", "Un rappel léger : « à jeudi 10h ! »"),
                    ("Le rappel J-1", "Le filet de sécurité", "Le jour J, le client est déjà ailleurs", "Un dernier rappel avec les infos pratiques"),
                ])),
            section("La version automatique", "Tout se déclenche tout seul",
                pains([
                    ("La prise de RDV", "Par téléphone, site ou WhatsApp", "Vous notez, vous relancez à la main", "Le RDV est saisi, les rappels se programment seuls"),
                    ("Le canal", "SMS, WhatsApp ou email : ce que préfèrent vos clients", "Des rappels incohérents, ou pas de rappel du tout", "Le bon canal pour chaque client"),
                    ("Le résultat", "Moins d'absences, des journées pleines", "Des trous dans l'agenda chaque semaine", "Les rendez-vous manqués diminuent fortement"),
                ])),
            section("Votre crainte, honnêtement", "« Ça va faire robot, non ? »",
                prose("<p>Un rappel bien rédigé sonne humain : « Bonjour Marie, à demain 10h chez nous ! Besoin d'un rappel, répondez simplement. » Vos clients apprécient qu'on pense à eux : c'est du service, pas du robot.</p>")),
        ],
        faq=[
            ("Quel canal de rappel choisir ?", "Celui que vos clients utilisent déjà : WhatsApp pour beaucoup de commerces, SMS pour le grand public, email pour les professionnels. On s'adapte à vos clients."),
            ("Ça fonctionne avec mon agenda actuel ?", "Oui, on se branche sur votre agenda (Google Agenda, Outlook...) et votre façon de prendre les RDV actuelle."),
            ("Combien ça réduit les absences ?", "Les rappels automatiques réduisent nettement les rendez-vous manqués : c'est l'un des gains les plus rapides à mesurer."),
            ("Est-ce que mes clients vont trouver ça intrusif ?", "Au contraire : un rappel est un service. La plupart des clients l'apprécient, et c'est vous qui choisissez le ton et la fréquence."),
        ],
        nav_links=[("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("repondre-avis-google.html", "Répondre aux avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatiser-devis.html",
        title="Automatiser vos devis : répondez en 30 secondes, 24h/24",
        meta="Un client demande un devis à 22h, le concurrent répond le lendemain. Un agent IA répond en 30 secondes avec prix, délai et livrables. Démo réelle.",
        h1="Automatiser vos devis : <em>le premier qui répond gagne.</em>",
        sub="Quand un client demande un devis, la vitesse fait la différence. Voici comment un agent IA répond en 30 secondes, 24h/24 : avec un exemple réel de réponse.",
        sections=[
            section("Le problème", "Le devis qui attend, le client qui part",
                prose("<p>Un client vous écrit à 22h. Vous répondez « dès lundi ». Pendant ce temps, votre concurrent a répondu en 10 minutes. <strong>Le devis, c'est souvent le premier qui répond qui gagne.</strong></p>")),
            section("La démo réelle", "Ce que l'agent IA a répondu, tout seul",
                """<div class="example-box">
<span class="in">→ Message reçu : « On est une boîte de nettoyage avec 3 agences. On reçoit beaucoup de demandes de devis par email et WhatsApp, on perd du temps à répondre. Combien ça coûte ? »</span><br><br>
<span class="out">→ Réponse en 30 secondes :</span><br>
« Bonjour Sophie, je comprends parfaitement votre besoin : automatiser la réponse aux demandes de devis. Je peux vous proposer une solution d'agent IA qui trie, qualifie et répond automatiquement avec des devis pré-remplis. »<br><br>
💰 Prix estimé : 4 000 – 8 000 € · ⏱️ Délai : 2-4 semaines<br>
📦 Inclus : agent de tri et qualification, réponses automatiques (email + WhatsApp), intégration de vos outils, tableau de bord de suivi<br>
👉 Prochaine étape : un appel de 15 minutes pour cadrer vos besoins
</div>"""),
            section("Comment ça marche, simplement", "Trois briques, zéro magie",
                pains([
                    ("1. La demande arrive", "Email, WhatsApp, formulaire", "Une demande qui attend votre disponibilité", "Le message est capté automatiquement"),
                    ("2. L'IA comprend et chiffre", "Elle connaît vos tarifs et vos délais", "Un devis qui prend des heures à préparer", "Elle propose prix, délais, livrables : dans votre référentiel"),
                    ("3. Vous restez maître", "Vous validez ou ajustez", "Des réponses qui partent sans contrôle", "Vous êtes notifié, vous gardez la main sur les gros dossiers"),
                ])),
            section("Votre crainte, honnêtement", "« Un devis, ça se négocie, ça se personnalise. »",
                prose("<p>Vrai, et c'est pour ça que l'IA ne remplace pas la négociation : elle <strong>prépare</strong>. Le premier contact, la réponse rapide, la fourchette chiffrée : c'est elle. L'appel, la personnalisation, la négociation : c'est vous. Elle ne vous vole pas le travail, elle vous le prépare.</p>")),
        ],
        faq=[
            ("Un devis automatique, ce n'est pas trop impersonnel ?", "C'est l'inverse : la réponse arrive en 30 secondes, elle est personnalisée avec le nom du client et adaptée à sa demande. Le premier contact est meilleur que « on revient vers vous »."),
            ("Et si l'IA se trompe sur le prix ?", "Vous définissez le référentiel de prix (fourchettes, forfaits) : l'IA chiffre dedans. Et vous êtes notifié pour valider les gros dossiers."),
            ("Ça marche avec WhatsApp ?", "Oui, c'est même l'un des canaux les plus efficaces : les demandes arrivent souvent le soir et le week-end, quand vous ne pouvez pas répondre."),
            ("Ça coûte combien ?", "Moins qu'une demande perdue. L'audit gratuit permet de chiffrer précisément ce que les devis manqués vous coûtent."),
        ],
        nav_links=[("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("facturation-electronique-2026.html", "Facturation électronique"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatiser-excel.html",
        title="Automatiser Excel : la fin des macros qui prennent la tête",
        meta="Reporting, rapprochement, consolidation : les tâches Excel répétitives s'automatisent avec l'IA. Exemples concrets et temps gagné pour les PME.",
        h1="Automatiser Excel : <em>la fin des macros qui prennent la tête.</em>",
        sub="Vous passez vos semaines à copier-coller des chiffres dans Excel ? La bonne nouvelle : ces tâches s'automatisent, sans toucher à vos fichiers. Exemples concrets.",
        sections=[
            section("Le problème", "Excel est génial... sauf quand il vous mange la vie",
                prose("<p>Excel est l'outil de toutes les PME. Mais les tâches répétitives : consolider, copier-coller, mettre en forme, vérifier : prennent des heures chaque semaine. Les macros aident, mais elles sont fragiles et personne n'a le temps de les maintenir.</p>")),
            section("Ce qu'on automatise, concrètement", "Vos fichiers restent, le travail part",
                pains([
                    ("Le reporting hebdomadaire", "Ventes, activité, tableaux de bord", "2 heures de copier-coller et de mise en forme", "Le rapport est généré en 10 secondes, avec analyse IA"),
                    ("Le rapprochement bancaire", "Relevé vs factures", "3 heures par mois, à la clôture", "30 secondes, écarts détectés et analysés"),
                    ("La consolidation", "Plusieurs fichiers à rassembler", "Copier-coller et erreurs à chaque fois", "Les fichiers se fusionnent automatiquement, les totaux se vérifient"),
                    ("Les extractions de données", "Emails, PDF, sites", "Saisie manuelle, fautes de frappe", "L'IA lit les documents et remplit le tableau"),
                ])),
            section("Votre crainte, honnêtement", "« On a des années de fichiers Excel, on ne va pas tout changer. »",
                prose("<p>Personne ne vous demande de changer : l'automatisation <strong>travaille avec vos fichiers existants</strong>. On ajoute une couche qui fait le travail répétitif à votre place, et vous gardez vos habitudes pour le reste.</p>")),
        ],
        faq=[
            ("Il faut savoir coder pour automatiser Excel ?", "Non : un consultant s'en occupe. Vous, vous continuez à utiliser vos fichiers comme avant : le travail répétitif en moins."),
            ("Est-ce que ça remplace mes classeurs ?", "Non, ils restent la source de vérité. L'automatisation lit, remplit, consolide : elle ne détruit rien."),
            ("Et si les chiffres changent de format ?", "Les automatisations sont conçues pour tolérer les variations, et vous êtes alerté en cas d'anomalie. La vigilance se concentre là où ça compte."),
            ("Quelle est la première tâche à automatiser ?", "Celle qui revient chaque semaine et vous prend le plus de temps. On la repère ensemble pendant l'audit gratuit."),
        ],
        nav_links=[("rapprochement-bancaire-excel.html", "Rapprochement bancaire"), ("compte-rendu-reunion.html", "Compte-rendu de réunion"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="chatbot-whatsapp.html",
        title="Chatbot WhatsApp pour votre entreprise : simple et efficace",
        meta="Répondre 24h/24 sur WhatsApp, qualifier les demandes, envoyer des devis : le chatbot WhatsApp pour PME expliqué simplement, avec des exemples.",
        h1="Chatbot WhatsApp : <em>votre entreprise qui répond 24h/24.</em>",
        sub="Vos clients écrivent sur WhatsApp ? C'est là que vous devez répondre. Un chatbot bien fait répond, qualifie et prépare : sans faire fuir les vrais échanges humains.",
        sections=[
            section("Le problème", "Vos clients sont sur WhatsApp, pas dans vos mails",
                prose("<p>Pour beaucoup de PME, WhatsApp est devenu le premier canal de contact : demande de devis, question, rendez-vous. Mais répondre à chaque message, à toute heure, c'est impossible, et chaque réponse tardive est une occasion perdue.</p>")),
            section("Ce que le chatbot fait (et ne fait pas)", "L'équilibre qui fonctionne",
                pains([
                    ("Répondre aux questions fréquentes", "Horaires, tarifs, disponibilités", "Les mêmes réponses répétées 10 fois par jour", "Une réponse immédiate et correcte à chaque fois"),
                    ("Qualifier les demandes", "Qui ? Quoi ? Pour quand ?", "Des messages vagues qui demandent 3 allers-retours", "Le chatbot pose les bonnes questions, vous gagnez du temps"),
                    ("Préparer le devis", "Le premier contact", "Vous reprenez tout de zéro", "L'IA prépare une réponse chiffrée, vous validez"),
                ])),
            section("Votre crainte, honnêtement", "« Un robot qui parle à mes clients, ça va les braquer. »",
                prose("<p>Un bon chatbot se fait passer le relais dès que la conversation devient complexe : « Je vous mets en relation avec un humain. » Vos clients préfèrent une réponse immédiate de robot à un silence de 24h, et ils ne s'y trompent pas : c'est du service.</p>")),
        ],
        faq=[
            ("C'est quoi un chatbot WhatsApp ?", "Un assistant automatique qui répond aux messages reçus sur votre numéro WhatsApp : questions fréquentes, demande d'informations, première réponse de devis."),
            ("Mes clients vont parler à un robot, vraiment ?", "Pour les questions simples, oui, et c'est un service : réponse immédiate au lieu d'attendre. Dès que c'est complexe, le relais est passé à un humain."),
            ("Ça marche avec mon numéro actuel ?", "Ça fonctionne avec WhatsApp Business (gratuit) ou l'API WhatsApp pour les volumes importants. On s'adapte à votre situation."),
            ("Combien de temps pour le mettre en place ?", "Les premiers scénarios tournent souvent en quelques jours à 2 semaines, selon la complexité de vos réponses."),
        ],
        nav_links=[("automatiser-devis.html", "Automatiser les devis"), ("prise-rendez-vous.html", "Rappels de rendez-vous"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="service-client.html",
        title="Service client automatique : répondez 24h/24 sans embaucher",
        meta="Questions répétées, SAV, réclamations : le service client automatique avec l'IA. Réponses immédiates, relais humain quand il faut. Explication simple et exemples.",
        h1="Service client automatique : <em>répondez 24h/24, sans embaucher.</em>",
        sub="Vos clients posent toujours les mêmes questions ? L'IA y répond en une seconde, 24h/24, et passe le relais à un humain dès que ça se complique. Voici comment, simplement.",
        sections=[
            section("Le problème", "Les mêmes questions, jour après jour",
                prose("<p>« Quels sont vos horaires ? » « Livrez-vous le week-end ? » « Où en est ma commande ? » : les mêmes questions reviennent sans cesse. Vous (ou votre équipe) répondez, pendant que le travail qui compte attend.</p>")),
            section("Ce qu'on automatise, concrètement", "Le service client, sans faire fuir les clients",
                pains([
                    ("Répondre aux questions fréquentes", "Horaires, tarifs, délais, livraison", "Les mêmes réponses répétées chaque jour", "Réponse immédiate et correcte, 24h/24"),
                    ("Le premier niveau de SAV", "Suivi de commande, documents, infos", "Des tickets qui s'accumulent", "L'IA traite le standard, vous traitez le complexe"),
                    ("Les réclamations", "Le ton qui désamorce", "Des réponses tardives qui enveniment", "Accusé immédiat + escalade humaine rapide"),
                    ("Le suivi des demandes", "Qui a demandé quoi, quand", "Des demandes qui se perdent dans les emails", "Un journal automatique, rien ne se perd"),
                ])),
            section("Votre crainte, honnêtement", "« Un robot qui parle à mes clients, ça va les énerver. »",
                prose("<p>L'inverse : ce qui énerve les clients, c'est d'attendre. Une réponse immédiate (même automatique) est mieux perçue qu'un silence de 24h. La règle : l'IA répond au standard, <strong>le relais humain est toujours possible en un clic</strong>, et vos clients le sentent.</p>")),
        ],
        faq=[
            ("Qu'est-ce qu'on peut automatiser dans le service client ?", "Les questions fréquentes, le premier niveau de SAV (suivi, documents, infos), les accusés de réception et le journal des demandes. Le complexe reste humain."),
            ("Mes clients vont-ils sentir la différence ?", "Oui, positivement : réponse immédiate au lieu d'attendre. Et dès que c'est important, un humain reprend la main."),
            ("Ça marche avec mes canaux actuels ?", "Email, WhatsApp, formulaire du site : on se branche sur ce que vos clients utilisent déjà."),
            ("Combien de temps pour mettre en place ?", "Les premiers scénarios (FAQ, accusés, suivi) tournent souvent en 1 à 2 semaines."),
        ],
        nav_links=[("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("repondre-avis-google.html", "Répondre aux avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-artisan.html",
        title="Automatisation pour artisans : gagnez 10h/semaine sans embaucher",
        meta="Peintre, plombier, électricien, coiffeur : les 6 tâches qui vous volent du temps (devis, factures, relances, RDV, avis) et comment les automatiser simplement.",
        h1="Artisans : <em>récupérez vos semaines.</em>",
        sub="Vous êtes peintre, plombier, électricien, coiffeur ? Vous n'avez pas choisi ce métier pour faire de la paperasse. Voici les 6 tâches qui vous volent du temps, et comment les automatiser.",
        sections=[
            section("Le paradoxe de l'artisan", "Vous travaillez plus, vous gagnez moins",
                prose("<p>Chaque heure passée sur un devis, une facture ou une relance, c'est une heure de moins sur un chantier. Et pourtant, sans paperasse, il n'y a pas de chantier. Le problème : elle prend <strong>10 à 15 heures par semaine</strong> à beaucoup d'artisans.</p>")),
            section("Les 6 tâches à automatiser", "Les pains de votre métier, un par un",
                pains([
                    ("Répondre aux demandes de devis", "Le concurrent qui répond vite gagne le chantier", "Réponse sous 2 jours, quand vous êtes sur le chantier", "Réponse chiffrée en 30 secondes, 24h/24"),
                    ("Factures et saisie", "Saisie manuelle, erreurs", "Les montants recopiés à la main", "Extraction automatique, alertes sur l'urgent"),
                    ("Relancer les impayés", "Les chantiers payés en retard", "Relances oubliées, trésorerie tendue", "Relance polie et automatique en 3 paliers"),
                    ("Les rendez-vous et devis sur place", "Agenda + confirmation", "Oublis, rendez-vous manqués", "Rappels automatiques par SMS/WhatsApp"),
                    ("Les avis Google", "Votre réputation locale", "Avis sans réponse, clients contents silencieux", "Réponses automatiques + demande d'avis post-chantier"),
                    ("Le rapprochement bancaire", "La clôture du mois", "3 heures par mois à tout vérifier", "30 secondes, écarts détectés seuls"),
                ])),
            section("Votre crainte, honnêtement", "« L'informatique, ce n'est pas mon truc. »",
                prose("<p>C'est justement le principe : <strong>vous n'aurez rien à toucher.</strong> Vous décrivez votre quotidien, je construis, vous vérifiez le résultat le matin. Comme un apprenti qui s'occupe de la paperasse : sans le payer au SMIC.</p>")),
        ],
        faq=[
            ("Ça marche pour mon métier précis ?", "Oui : les pains sont les mêmes pour presque tous les artisans (devis, factures, relances, RDV, avis). On adapte les exemples à votre activité pendant l'audit."),
            ("Je n'ai pas de logiciel, je fais tout sur papier ?", "Parfait point de départ : on part de zéro, proprement. Vous pouvez même commencer avec les outils gratuits du site (générateur de devis, modèle Excel)."),
            ("Combien ça coûte ?", "Moins que les heures perdues. Chaque proposition commence par un ROI chiffré, et l'offre découverte à prix fixe permet de tester sans risque."),
            ("Mes clients verront-ils un changement ?", "Ils verront surtout que vous répondez plus vite et que les relances sont propres. Pour eux, c'est un meilleur service."),
        ],
        nav_links=[("generateur-devis.html", "Créer un devis gratuit"), ("relance-impayes.html", "Relancer les impayés"), ("repondre-avis-google.html", "Répondre aux avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="ia-remplace-t-elle-mon-employe.html",
        title="L'IA va-t-elle remplacer vos employés ? La réponse honnête",
        meta="La peur n°1 des dirigeants et des équipes, répondue factuellement : ce que l'IA fait, ce qu'elle ne fait pas, et comment l'utiliser pour enlever le travail pénible.",
        h1="L'IA va-t-elle remplacer vos employés ? <em>La réponse honnête.</em>",
        sub="C'est la première question que tout dirigeant pose, et que toute équipe se pose. Voici la réponse que je donne à mes clients, sans langue de bois.",
        sections=[
            section("Ce que l'IA fait vraiment", "Et ce qu'elle ne fera pas",
                pains([
                    ("Elle fait : le répétitif", "Saisie, tri, copier-coller, première réponse", "Des heures de travail pénible chaque semaine", "Elle traite le standard en quelques secondes"),
                    ("Elle ne fait pas : la relation", "Le contact client, la négociation, la confiance", "Un client veut parler à un humain", "Le relationnel reste 100% humain"),
                    ("Elle ne fait pas : la décision", "Choisir, arbitrer, engager", "Un dirigeant assume ses choix", "L'IA propose, vous décidez"),
                    ("Elle ne fait pas : le jugement", "Le contexte, l'intuition, le terrain", "Des situations que seul l'humain comprend", "L'IA est un outil, pas un remplaçant"),
                ])),
            section("L'exemple qui rassure", "Votre équipe ne tape plus, elle vérifie",
                prose("<p>Prenons la saisie des factures. Avant : votre employé recopie des montants pendant 2 heures. Après : l'IA extrait les montants, <strong>et votre employé vérifie en 10 minutes</strong>. Le travail est moins pénible, plus valorisant, et l'entreprise y gagne.</p>"
                      "<p>Les entreprises qui gagnent avec l'IA ne licencient pas : elles <strong>déplacent leurs équipes vers le travail qui a de la valeur</strong> : la vérification, la relation, le terrain.</p>")),
            section("Et si mon employé a peur ?", "La résistance se gère",
                prose("<p>La peur est légitime : on parle de son travail. La réponse, c'est la <strong>transparence et la formation</strong> : expliquer ce qui change, montrer que le poste évolue (pas disparaît), et former l'équipe. C'est exactement l'objet de mon atelier de formation.</p>")),
        ],
        faq=[
            ("L'IA va supprimer des emplois ?", "Dans les PME, elle transforme les postes plus qu'elle ne les supprime : le répétitif part, la vérification et la relation restent. Les équipes formées deviennent plus précieuses."),
            ("Mon employé va-t-il refuser l'outil ?", "Souvent au début, par peur. La transparence + la formation règlent la grande majorité des cas. On implique l'équipe dès le départ."),
            ("Et si l'IA se trompe ?", "C'est pour ça que la vérification humaine reste : l'IA propose, un humain valide. Le risque est plus faible qu'avec une saisie manuelle."),
            ("Comment présenter ça à mon équipe ?", "Je peux vous aider : l'atelier de formation démarre par cette discussion, avec des mots simples et des exemples de leur quotidien."),
        ],
        nav_links=[("formation-ia-pme.html", "La formation pour vos équipes"), ("agent-ia-cest-quoi.html", "Agent IA, c'est quoi ?"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="formation-ia-pme.html",
        title="Formation IA pour vos équipes : l'IA sans stress",
        meta="Ateliers pratiques pour PME : découvrir l'IA, l'utiliser au quotidien, automatiser sans peur. 3 formats : 2h, demi-journée, accompagnement 1 mois.",
        h1="Formation IA pour vos équipes : <em>l'IA sans stress.</em>",
        sub="Vos équipes ont peur de l'IA, ou n'en voient pas l'intérêt ? Un atelier pratique, avec leurs exemples, change tout. Voici les 3 formats proposés.",
        sections=[
            section("Le problème", "L'IA fait peur, ou n'intéresse pas",
                prose("<p>Deux réactions classiques en entreprise : « l'IA va me remplacer » ou « c'est un gadget ». Les deux viennent d'une même cause : <strong>personne n'a pris le temps d'expliquer et de montrer</strong>. La formation règle ça.</p>")),
            section("Les 3 formats", "Du déclic à l'adoption",
                pains([
                    ("Atelier découverte (2h)", "Format 1, pour lancer", "L'équipe ne sait pas ce que l'IA peut faire", "Démo sur VOS exemples, chacun repart avec 3 usages concrets"),
                    ("Atelier pratique (demi-journée)", "Format 2, pour adopter", "L'équipe teste mais ne l'utilise pas au quotidien", "Chacun construit son usage : emails, comptes-rendus, recherche"),
                    ("Accompagnement (1 mois)", "Format 3, pour ancrer", "Les bonnes résolutions s'éteignent en 2 semaines", "Suivi hebdo, corrections, automatisations simples en route"),
                ])),
            section("Ce que vous repartez avec", "Concret, pas théorique",
                prose("<p>Des <strong>exemples tirés de votre quotidien</strong> (pas des cas génériques), un <strong>prompt personnalisé</strong> pour vos tâches, une <strong>charte d'usage simple</strong> (ce qu'on peut confier à l'IA, ce qu'on ne confie pas), et la réponse à la question « est-ce que mon poste change ? ».</p>")),
        ],
        faq=[
            ("Mes employés n'ont jamais utilisé ChatGPT, c'est un problème ?", "Non, c'est le public idéal : on part de zéro, avec des exemples de leur métier. Pas de prérequis."),
            ("La formation se passe où ?", "À distance (visio) ou sur site en Normandie. En petit groupe (5-10 personnes) pour que chacun pratique."),
            ("On va faire quoi concrètement ?", "Écrire de vrais emails, préparer de vrais comptes-rendus, chercher de vraies infos. Chacun repart avec des outils utilisables dès le lendemain."),
            ("Ça prépare l'automatisation ?", "Oui : une équipe formée accueille l'automatisation avec curiosité au lieu de crainte. C'est l'étape 0 de tout projet."),
        ],
        nav_links=[("ia-remplace-t-elle-mon-employe.html", "L'IA va-t-elle remplacer mes employés ?"), ("methode.html", "La méthode"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="professions-liberales.html",
        title="IA pour professions libérales : avocats, architectes, kinés, conseils",
        meta="Rendez-vous, comptes-rendus, facturation, relances, veille : comment les professions libérales gagnent du temps avec l'IA. Exemples concrets, sans jargon.",
        h1="Professions libérales : <em>l'IA qui vous rend vos soirées.</em>",
        sub="Avocat, architecte, kiné, expert-comptable, consultant : votre temps est votre seule ressource. Voici les tâches que l'IA enlève de votre quotidien : simplement.",
        sections=[
            section("Le problème", "Votre heure vaut cher. Vous la donnez à la paperasse.",
                prose("<p>Chaque rendez-vous génère un compte-rendu, chaque prestation une facture, chaque oubli une relance. Une grande partie de la semaine part dans ces tâches : pendant que le travail facturable attend.</p>")),
            section("Ce qu'on automatise, concrètement", "Les 6 gains des professions libérales",
                pains([
                    ("Les comptes-rendus de rendez-vous", "Avocats, consultants, santé", "1 heure de rédaction par rendez-vous", "Résumé généré en 1 minute, décisions et actions extraites"),
                    ("Les rendez-vous et rappels", "Agenda chargé, no-show", "Les oublis coûtent des heures", "Rappels automatiques SMS/WhatsApp/email"),
                    ("La facturation des honoraires", "Suivi du temps et des prestations", "Des heures de saisie en fin de mois", "Factures générées et suivies automatiquement"),
                    ("Les relances clients", "Honoraires impayés", "Relances oubliées, gênant de relancer", "Relance polie et automatique en 3 paliers"),
                    ("La veille et la recherche", "Juridique, technique, marché", "Des heures de lecture pour rester à jour", "Synthèses automatiques des documents"),
                    ("Les réponses aux clients", "Questions fréquentes par email", "Les mêmes réponses chaque jour", "Réponse immédiate, relais humain si besoin"),
                ])),
            section("Votre crainte, honnêtement", "« La confidentialité, alors ? »",
                prose("<p>Première bonne question. La règle : <strong>vos données restent chez vous</strong> (outils open source, pas de plateforme tierce). Et la validation humaine reste systématique sur tout ce qui touche au dossier d'un client.</p>")),
        ],
        faq=[
            ("L'IA est-elle compatible avec le secret professionnel ?", "Oui, à condition d'utiliser des outils qui gardent les données chez vous et de valider ce qui sort. On vérifie ce point ensemble dès l'audit."),
            ("Je n'ai pas le temps de m'en occuper, c'est justement le problème.", "C'est le principe : vous décrivez, je construis, vous vérifiez le résultat. Vous n'avez rien à toucher."),
            ("Ça commence petit ?", "Oui : l'offre découverte (490 €) automatise une première tâche en 7 jours. Vous testez avant d'aller plus loin."),
            ("Quelle est la première tâche à automatiser ?", "Celle qui revient le plus souvent : souvent les comptes-rendus ou les relances. L'audit gratuit le confirme en 48h."),
        ],
        nav_links=[("ia-pour-avocats.html", "Pour les avocats"), ("ia-pour-architectes.html", "Pour les architectes"), ("formation-ia-pme.html", "Formation des équipes"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="ia-pour-avocats.html",
        title="IA pour avocats : comptes-rendus, relances, veille : sans déontologie brisée",
        meta="Gagner du temps sur les comptes-rendus, les relances et la veille juridique avec l'IA, en restant conforme au secret professionnel. Exemples concrets.",
        h1="Avocats : <em>l'IA qui travaille pendant vos audiences.</em>",
        sub="Le temps facturable est votre seul stock. L'IA peut vous le rendre : comptes-rendus, relances, veille : sans toucher au secret professionnel.",
        sections=[
            section("Les 5 gains concrets", "Ce que l'IA fait déjà pour des confrères",
                pains([
                    ("Compte-rendu de rendez-vous client", "Notes, décisions, prochaines étapes", "1 heure de rédaction par rendez-vous", "Résumé structuré en 1 minute, vous validez"),
                    ("Relance des honoraires", "Factures impayées, relances gênantes", "Des mois d'honoraires en attente", "Relance polie et automatique en 3 paliers"),
                    ("Veille juridique", "Textes, jurisprudence, actualités", "Des heures de lecture chaque semaine", "Synthèses automatiques des documents que vous choisissez"),
                    ("Premières réponses aux clients", "Questions fréquentes", "Les mêmes réponses répétées", "Accusé immédiat + questions de cadrage"),
                    ("Organisation des rendez-vous", "Agenda, confirmations", "Oublis et allers-retours", "Rappels automatiques"),
                ])),
            section("La déontologie, d'abord", "Ce qui ne change pas",
                prose("<p>Le secret professionnel reste le cadre : <strong>vos dossiers ne quittent pas vos outils</strong>, l'IA travaille sur vos documents sans les transmettre à des tiers, et tout ce qui sort est validé par vous. C'est un outil interne, pas un prestataire externe.</p>")),
        ],
        faq=[
            ("Est-ce que je peux utiliser l'IA sur des dossiers confidentiels ?", "Avec les bons outils (données hébergées chez vous, pas de réutilisation par des tiers) et votre validation systématique, oui. On vérifie la configuration ensemble."),
            ("L'IA va-t-elle rédiger mes conclusions ?", "Non : elle prépare, résume, structure. La rédaction finale et la responsabilité restent vôtres : c'est un assistant, pas un remplaçant."),
            ("Par quoi commencer ?", "Le compte-rendu de rendez-vous est le gain le plus rapide : 1 heure récupérée par rendez-vous, mesurable dès la première semaine."),
            ("Combien ça coûte ?", "L'offre découverte (490 €) automatise une première tâche en 7 jours. Ensuite, des fourchettes claires par mission."),
        ],
        nav_links=[("professions-liberales.html", "Professions libérales"), ("compte-rendu-reunion.html", "Compte-rendu automatique"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="ia-pour-architectes.html",
        title="IA pour architectes : devis, comptes-rendus, suivi de chantier",
        meta="Gagner du temps sur les devis, les comptes-rendus de réunion et le suivi de chantier avec l'IA. Exemples concrets pour architectes et architectes d'intérieur.",
        h1="Architectes : <em>l'IA qui gère la paperasse du chantier.</em>",
        sub="Entre les devis, les comptes-rendus de réunion et le suivi de chantier, la moitié de la semaine y passe. L'IA s'en occupe : vous gardez la création et le terrain.",
        sections=[
            section("Les 5 gains concrets", "Ce que l'IA fait déjà pour des confrères",
                pains([
                    ("Devis et honoraires", "Devis par étapes, avenants", "Des heures de préparation par projet", "Devis chiffrés en 30 secondes, à partir de votre référentiel"),
                    ("Comptes-rendus de réunion de chantier", "CR de chantier hebdomadaires", "Des heures de rédaction chaque semaine", "Compte-rendu généré en 2 minutes, décisions et actions extraites"),
                    ("Suivi des décisions", "Qui fait quoi, pour quand", "Des actions qui se perdent", "Un journal automatique, relances sur les retards"),
                    ("Facturation et relances", "Étapes, soldes, impayés", "Relances oubliées", "Relance polie et automatique"),
                    ("Recherche et veille", "Matériaux, normes, références", "Des heures de recherche", "Synthèses automatiques des documents"),
                ])),
            section("Votre crainte, honnêtement", "« La création, ça ne s'automatise pas. »",
                prose("<p>Et c'est très bien : <strong>l'IA ne touche pas à la création</strong>. Elle s'occupe de ce qui entoure le projet : les documents, les suivis, les relances, pour que votre temps aille au design et au terrain, pas au CR de chantier du vendredi soir.</p>")),
        ],
        faq=[
            ("Ça marche avec mes logiciels (DAO, métré, devis) ?", "On se branche sur vos fichiers et vos outils existants. L'automatisation travaille avec ce que vous utilisez déjà."),
            ("Les comptes-rendus seront-ils fiables ?", "Ils reprennent ce qui a été dit, structuré en décisions et actions. Vous relisez et validez avant envoi : 2 minutes au lieu de 2 heures."),
            ("Par quoi commencer ?", "Le CR de chantier est le gain le plus rapide et le plus visible : des heures récupérées chaque semaine."),
            ("Combien ça coûte ?", "Offre découverte à 490 € pour une première automatisation en 7 jours, puis fourchettes claires par mission."),
        ],
        nav_links=[("professions-liberales.html", "Professions libérales"), ("generateur-devis.html", "Générateur de devis gratuit"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="no-code-cest-quoi.html",
        title="Le no-code, c'est quoi ? L'automatisation sans coder, expliquée",
        meta="Le no-code permet de créer des automatisations sans écrire une ligne de code. Explication simple, exemples concrets pour PME, et lien avec l'IA.",
        h1="No-code : <em>automatiser sans coder, c'est possible.</em>",
        sub="Vous pensez que l'automatisation demande un informaticien ? Le no-code (et n8n en tête) prouve le contraire : des automatisations puissantes se construisent visuellement, comme des briques.",
        sections=[
            section("La définition simple", "No-code = construire sans coder",
                prose("<p>Le <strong>no-code</strong> (« sans code ») regroupe les outils qui permettent de créer des automatisations et des applications <strong>sans écrire une ligne de programmation</strong>. On relie des blocs visuels, comme des LEGO : quand un email arrive → alors cette action se déclenche.</p>"
                      "<p>C'est la raison pour laquelle l'automatisation est devenue accessible aux PME : plus besoin d'une équipe technique pour relier Gmail, Excel, WhatsApp et votre banque.</p>")),
            section("Ce que ça change pour vous", "Les automatisations no-code en action",
                pains([
                    ("Répondre aux devis", "n8n + IA", "Un devis qui attend votre disponibilité", "Réponse chiffrée en 30 secondes, construite en blocs visuels"),
                    ("Trier les emails", "Gmail + no-code", "Des heures de tri manuel", "Tri et extraction automatiques, sans développeur"),
                    ("Rapprocher la banque", "Fichiers + no-code", "3 heures par mois à la clôture", "Comparaison automatique en 30 secondes"),
                    ("Relancer les impayés", "Calendrier + no-code", "Relances oubliées", "Relances programmées en 3 paliers"),
                ])),
            section("No-code, low-code et IA", "Les mots, simplement",
                prose("<p><strong>No-code</strong> : on ne code pas du tout (blocs visuels). <strong>Low-code</strong> : on peut ajouter de petites briques de code quand nécessaire. <strong>n8n</strong> est no-code/low-code : 95 % de vos automatisations se construisent visuellement, et l'IA s'y branche pour lire, comprendre et rédiger.</p>")),
        ],
        faq=[
            ("Il faut quand même un informaticien pour le no-code ?", "Non, c'est le principe : des blocs visuels, comme assembler des briques. Un consultant peut tout construire pour vous, et vous n'avez rien à toucher."),
            ("Le no-code, c'est fiable ?", "Oui : ces outils sont utilisés par des milliers d'entreprises. La fiabilité vient de la conception (cas gérés, alertes) : c'est là que l'expérience d'un consultant compte."),
            ("No-code et IA, ça va ensemble ?", "Parfaitement : le no-code orchestre (quand X → alors Y), l'IA comprend (lire, résumer, rédiger). Ensemble, ils font le travail à votre place."),
            ("Par où commencer ?", "Le détecteur de tâches identifie vos automatisations potentielles en 2 minutes, puis l'audit gratuit chiffre le projet."),
        ],
        nav_links=[("n8n-cest-quoi.html", "n8n, c'est quoi ?"), ("detecteur-taches.html", "Détecteur de tâches"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="alternative-a-zapier.html",
        title="Alternative à Zapier : le comparatif honnête pour les PME",
        meta="Zapier devient cher dès que le volume monte. Comparatif honnête avec n8n (gratuit, open source) et les autres alternatives : prix, données, quand changer, quand rester.",
        h1="Alternative à Zapier : <em>le comparatif honnête.</em>",
        sub="Votre facture Zapier grimpe chaque mois, et le plan gratuit se limite à 100 tâches ? Vous cherchez une alternative : voici la comparaison franche, avec les cas où il vaut mieux rester.",
        sections=[
            section("Pourquoi on cherche une alternative", "Les 3 frustrations Zapier",
                pains([
                    ("Le prix par tâche", "Chaque automatisation exécutée est facturée", "La facture grimpe dès que le volume monte", "n8n : aucun coût par tâche, un prix fixe d'hébergement"),
                    ("Le plan gratuit limité", "100 tâches/mois, puis on paie", "On bloque ou on paye un abonnement", "n8n Community : gratuit, sans limite de tâches"),
                    ("Les données chez un tiers", "Tout passe par la plateforme Zapier", "Vous ne contrôlez pas où vont vos données", "n8n auto-hébergé : vos données restent chez vous"),
                ])),
            section("Le comparatif", "Zapier vs n8n vs Make, simplement",
                pains([
                    ("Zapier", "Le plus simple, le plus cher à volume", "Facile pour 1-2 automatisations simples", "Facturation par tâche ; données chez Zapier"),
                    ("n8n (open source)", "Le meilleur rapport puissance/prix", "Gratuit, auto-hébergé, sans limite", "Courbe d'apprentissage ; auto-hébergement à gérer"),
                    ("Make", "Alternative intermédiaire", "Tarifs par opération", "Données chez Make ; moins flexible que n8n"),
                ])),
            section("Quand changer, quand rester", "La réponse honnête",
                prose("<p><strong>Changez si</strong> : votre facture Zapier dépasse 50 €/mois, vous avez plus de 10 automatisations, ou vous voulez garder vos données chez vous.</p>"
                      "<p><strong>Restez si</strong> : vous avez 1-2 automatisations simples, pas d'équipe pour gérer un serveur, et que la facture reste modeste. Parfois, rester est la meilleure décision.</p>"
                      "<p>La bonne nouvelle : n8n peut se brancher en parallèle, et migrer une automatisation prend souvent une journée. C'est exactement le genre de mission que je livre en offre découverte.</p>")),
        ],
        faq=[
            ("Zapier, c'est quoi ?", "Une plateforme qui relie vos applications (Gmail, Sheets, WhatsApp...) pour automatiser des tâches, sans coder. Très simple, mais facturée par tâche exécutée."),
            ("Pourquoi Zapier est-il si cher ?", "Parce qu'il facture chaque exécution d'automatisation. Dès que votre volume monte (chaque devis, chaque email, chaque ligne), la facture suit."),
            ("n8n est vraiment gratuit ?", "Le logiciel est open source et gratuit. Vous payez juste l'hébergement (quelques euros par mois) ou le prestataire qui le configure."),
            ("La migration est-elle risquée ?", "Non : on migre une automatisation à la fois, en testant. L'offre découverte (490 €) migre votre première automatisation en 7 jours, sans risque."),
        ],
        nav_links=[("n8n-cest-quoi.html", "n8n, c'est quoi ?"), ("tarifs.html", "Les tarifs"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="freelance-automatisation-n8n.html",
        title="Freelance automatisation n8n : le prestataire qui construit, pas qui promet",
        meta="Vous cherchez un freelance n8n ? Audit gratuit, offre découverte à prix fixe, missions chiffrées et maintenance. Un prestataire qui livre du fiable, pas des démos.",
        h1="Freelance automatisation n8n : <em>je construis, je ne promets pas.</em>",
        sub="Vous cherchez quelqu'un pour automatiser vos devis, factures, relances ou reporting avec n8n ? Voici comment je travaille, ce que ça coûte, et pourquoi ça dure.",
        sections=[
            section("Ce qu'un freelance n8n fait", "Les 4 livrables concrets",
                pains([
                    ("Construire les automatisations", "Relier Gmail, Sheets, WhatsApp, votre banque", "Des flux qui n'existent pas encore", "Des automatisations qui tournent toutes seules"),
                    ("Brancher l'IA", "Lire, comprendre, rédiger", "Une IA qui travaille pour vous", "Agents IA intégrés à vos processus"),
                    ("Tester et fiabiliser", "Les cas particuliers, les erreurs", "Une automatisation qui casse le mois suivant", "Des tests, des alertes, une supervision"),
                    ("Maintenir", "Les outils changent, vos besoins aussi", "Une machine qu'on oublie jusqu'à la panne", "Une maintenance qui anticipe (150-300 €/mois)"),
                ])),
            section("Comment ça se passe", "4 étapes, sans surprise",
                prose("<p><strong>1. Audit gratuit (48h)</strong> : j'identifie les 5 tâches les plus rentables à automatiser et je chiffre le gain.</p>"
                      "<p><strong>2. Offre découverte (490 €)</strong> : une première automatisation livrée en 7 jours, garantie « sinon vous ne payez pas ».</p>"
                      "<p><strong>3. Mission</strong> : les automatisations suivantes, avec fourchettes claires par pain.</p>"
                      "<p><strong>4. Maintenance</strong> : supervision, alertes, évolutions. Vous n'y pensez plus.</p>")),
            section("Pourquoi moi", "Ex-contrôleur de gestion, pas un vendeur de démos",
                prose("<p>J'ai passé 8 ans à subir les saisies et les reporting manuels avant de les automatiser. Je parle simplement, je chiffre avant de construire, et je garantis le résultat : <strong>si ce n'est pas automatisé, vous ne payez pas</strong>.</p>")),
        ],
        faq=[
            ("Quels sont vos tarifs ?", "Audit gratuit, offre découverte 490 € (1 automatisation en 7 jours), puis fourchettes par pain : relances 1 500-3 000 €, devis 3 000-8 000 €, rapprochement 4 000-9 000 €. Voir la page tarifs."),
            ("Vous travaillez à distance ?", "Oui, 100 % à distance, partout en France. Les réunions se font en visio, les livrables par écrit."),
            ("Et si une automatisation casse ?", "La maintenance (150-300 €/mois) inclut supervision, alertes et corrections rapides. Sans maintenance, je reste joignable en intervention."),
            ("Vous êtes disponible quand ?", "L'audit gratuit se planifie sous 48h. L'offre découverte se livre en 7 jours."),
        ],
        nav_links=[("alternative-a-zapier.html", "Alternative à Zapier"), ("demos.html", "Les démos"), ("tarifs.html", "Les tarifs"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="ia-pour-ecommerce.html",
        title="IA pour e-commerce : fiches produits, SAV, relances : sans embaucher",
        meta="Fiches produits rédigées en masse, réponses clients 24/7, relances de paniers abandonnés : ce que l'IA change dans votre boutique en ligne. Exemples concrets.",
        h1="E-commerce : <em>l'IA qui vend pendant que vous dormez.</em>",
        sub="Fiches produits, SAV, paniers abandonnés, avis clients : votre boutique génère des tonnes de tâches répétitives. Voici comment l'IA les prend en charge.",
        sections=[
            section("Les 6 gains concrets", "Ce que l'IA fait déjà dans des boutiques",
                pains([
                    ("Les fiches produits", "Des centaines de produits à décrire", "Des heures de rédaction", "Fiches générées à partir de vos photos et données"),
                    ("Le SAV et les questions clients", "Les mêmes questions chaque jour", "Des réponses lentes, des clients frustrés", "Réponse immédiate 24/7, relais humain si besoin"),
                    ("Les paniers abandonnés", "70 % des paniers sont abandonnés", "Des ventes perdues chaque jour", "Relance automatique et personnalisée"),
                    ("Le suivi des commandes", "« Où est ma commande ? »", "Des emails manuels", "Suivi automatisé, questions répondues seules"),
                    ("Les avis clients", "Demander des avis, c'est fastidieux", "Des avis sans réponse", "Demande d'avis automatique après livraison"),
                    ("L'inventaire et les prévisions", "Saisies et tableaux", "Des ruptures ou des surstocks", "Alertes et prévisions simples"),
                ])),
            section("Votre crainte, honnêtement", "« Ça va faire robot »",
                prose("<p>Une réponse automatique mal écrite, oui, ça fait robot. Une réponse <strong>rédigée sur mesure par l'IA puis validée par vous</strong>, non. Le ton reste le vôtre, la relation reste humaine, l'IA s'occupe du volume.</p>")),
        ],
        faq=[
            ("L'IA peut-elle rédiger toutes mes fiches produits ?", "Oui : à partir de vos données (photos, caractéristiques), elle génère des descriptions cohérentes avec votre ton. Vous validez, elle adapte."),
            ("Et les questions techniques que l'IA ne sait pas ?", "Elle répond aux questions fréquentes et transmet le reste à un humain. Personne ne reste sans réponse."),
            ("Combien ça coûte ?", "Comme pour toute automatisation : offre découverte 490 € pour une première tâche (souvent le SAV ou les paniers abandonnés), puis fourchettes claires."),
            ("Ça marche avec Shopify, WooCommerce, PrestaShop ?", "Oui : on se branche sur votre plateforme. L'automatisation travaille avec ce que vous utilisez déjà."),
        ],
        nav_links=[("service-client.html", "Service client automatique"), ("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="ia-pour-immobilier.html",
        title="IA pour l'immobilier : annonces, prospects, visites : gagnez des heures",
        meta="Rédaction d'annonces, qualification des prospects, prise de RDV, relances : ce que l'IA change pour les agents immobiliers. Exemples concrets et sans jargon.",
        h1="Immobilier : <em>l'IA qui répond quand le téléphone sonne.</em>",
        sub="Chaque bien = une annonce, des dizaines de prospects, des visites à caler, des relances. Voici comment l'IA absorbe le volume : vous gardez la négociation et le terrain.",
        sections=[
            section("Les 6 gains concrets", "Ce que l'IA fait déjà pour des agents",
                pains([
                    ("La rédaction des annonces", "Chaque bien demande une annonce soignée", "Des heures d'écriture par bien", "Annonce générée à partir de vos notes et photos"),
                    ("La qualification des prospects", "Des dizaines de demandes par bien", "Des heures de tri et de rappels", "L'IA pose les questions, classe, et ne vous transmet que les sérieux"),
                    ("La prise de rendez-vous", "Caler les visites", "Allers-retours interminables", "Proposition de créneaux automatique, rappels"),
                    ("Les relances", "Vendeurs, acheteurs, dossiers", "Des suivis oubliés", "Relances polies et automatiques"),
                    ("Les comptes-rendus de visite", "Noter chaque visite", "Des notes perdues", "CR structuré en 1 minute, retours transmis au vendeur"),
                    ("Le suivi des dossiers", "Papiers, dates, étapes", "Des oublis coûteux", "Suivi automatique avec alertes"),
                ])),
            section("Votre crainte, honnêtement", "« Mes clients veulent de l'humain. »",
                prose("<p>Et ils l'auront : l'IA répond vite (ça, les clients adorent), puis vous prenez le relais dès que ça compte : la visite, la négociation, la signature. <strong>Personne n'achète un bien à un robot.</strong> L'IA vous rend disponible pour ce qui fait la différence.</p>")),
        ],
        faq=[
            ("L'IA peut-elle rédiger des annonces conformes ?", "Oui, à partir de vos informations, avec votre ton et les obligations légales (diagnostics, surfaces). Vous relisez et validez."),
            ("La qualification des prospects, ça marche vraiment ?", "L'IA pose des questions simples (budget, délai, type de bien) et classe. Vous n'appelez que les prospects prêts : le reste est répondu automatiquement."),
            ("Je n'ai pas de logiciel immobilier, c'est un problème ?", "Non : on part de vos outils actuels (email, téléphone, Excel). L'automatisation s'adapte."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours (souvent la qualification ou la prise de RDV), puis fourchettes claires."),
        ],
        nav_links=[("prise-rendez-vous.html", "Prise de RDV automatique"), ("service-client.html", "Service client automatique"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-et-humain.html",
        title="L'automatisation et l'humain : où mettre la limite ? La réponse honnête",
        meta="L'automatisation va-t-elle déshumaniser votre entreprise ? Réponse honnête : ce qu'on automatise, ce qu'on garde humain, et la règle des 3 questions.",
        h1="L'automatisation et l'humain : <em>où mettre la limite ?</em>",
        sub="La crainte la plus légitime : que l'automatisation éloigne l'entreprise de ses clients. Voici ma règle, franchement, et comment je l'applique chez mes clients.",
        sections=[
            section("Ce qu'on automatise", "Et ce qu'on garde humain",
                pains([
                    ("On automatise : le répétitif", "Saisie, tri, premières réponses, relances", "Des heures de travail sans valeur ajoutée", "L'IA traite le volume en quelques secondes"),
                    ("On garde humain : la relation", "La visite, la négociation, la confiance", "Un client veut parler à un humain", "L'IA prépare, l'humain conclut"),
                    ("On garde humain : la décision", "Choisir, arbitrer, engager", "Un dirigeant assume ses choix", "L'IA propose, vous décidez"),
                    ("On garde humain : le jugement", "Le contexte, l'intuition, le terrain", "Des situations que seul l'humain comprend", "L'IA est un outil, pas un substitut"),
                ])),
            section("L'exemple du service client", "La différence entre un robot et un assistant",
                prose("<p>Un serveur vocal qui vous bloque dans un labyrinthe de menus : voilà la mauvaise automatisation : elle protège l'entreprise, pas le client.</p>"
                      "<p>Une réponse automatique qui dit « merci pour votre message, je vérifie et je reviens dans l'heure » puis qui transmet à un humain : voilà la bonne. <strong>L'automatisation doit rendre l'humain plus disponible, pas moins.</strong></p>")),
            section("La règle des 3 questions", "Avant d'automatiser quoi que ce soit",
                prose("<p><strong>1. C'est répétitif ?</strong> Si oui, ça peut s'automatiser.<br>"
                      "<strong>2. Ça demande du jugement ?</strong> Si oui, l'humain garde la main.<br>"
                      "<strong>3. Ça construit la relation ?</strong> Si oui, on n'y touche pas.</p>"
                      "<p>Les 3 réponses à cette règle déterminent chaque automatisation que je construis. C'est écrit dans ma méthode et c'est non négociable.</p>")),
        ],
        faq=[
            ("Ça va déshumaniser mon entreprise ?", "Ça peut, si l'automatisation est mal conçue. Ma règle : on automatise le pénible, on garde l'humain là où il compte. Le résultat est souvent une meilleure relation, parce que vous avez enfin le temps."),
            ("Et si un client insiste pour parler à un humain ?", "Il obtient un humain, immédiatement. L'IA transmet, elle ne bloque jamais. C'est la règle de base."),
            ("Mon équipe va-t-elle devenir inutile ?", "Non : elle passe de la saisie à la vérification, du traitement à la relation. Les équipes formées deviennent plus précieuses : voir la page sur l'emploi."),
            ("Comment savoir si une tâche doit être automatisée ?", "La règle des 3 questions ci-dessus. Si vous hésitez, l'audit gratuit tranche en 15 minutes."),
        ],
        nav_links=[("ia-remplace-t-elle-mon-employe.html", "L'IA va-t-elle remplacer mes employés ?"), ("methode.html", "La méthode"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="ia-peut-elle-se-tromper.html",
        title="L'IA peut-elle se tromper ? La réponse honnête (hallucinations)",
        meta="Oui, l'IA peut se tromper : c'est ce qu'on appelle une hallucination. Où elle se trompe, où elle est fiable, et les 3 garde-fous pour l'utiliser sereinement.",
        h1="L'IA peut-elle se tromper ? <em>Oui. Voici où, et comment on la surveille.</em>",
        sub="On lit partout que l'IA « hallucine ». C'est vrai, et c'est important de le savoir avant de lui confier vos documents. La bonne nouvelle : on sait exactement où elle est fiable, et comment la surveiller.",
        sections=[
            section("Oui, elle se trompe : voici où", "Les hallucinations, expliquées simplement",
                pains([
                    ("Elle invente des chiffres", "Un chiffre d'affaires, une date, un pourcentage", "Elle « devine » au lieu de vérifier", "Tout montant cité doit être validé sur le document source"),
                    ("Elle invente des faits", "Un événement, une loi, un article", "Elle mélange ce qu'elle a lu", "Rien de factuel ne sort sans vérification"),
                    ("Elle confond les noms", "Deux clients, deux fournisseurs", "Des homonymes ou des contextes proches", "Les noms propres sont toujours relus"),
                ])),
            section("Où elle est fiable", "Ce qu'on peut lui confier sans stress",
                pains([
                    ("Reformuler et structurer", "Résumés, comptes-rendus, emails", "Elle restitue ce qu'on lui donne", "Excellente pour gagner du temps"),
                    ("Travailler sur VOS documents", "Factures, devis, relevés", "Quand le contexte est fourni, les erreurs chutent", "C'est le principe des automatisations"),
                    ("Les tâches répétitives cadrées", "Tri, classement, premières réponses", "Des règles claires, un périmètre fixe", "L'erreur est détectée par les alertes"),
                ])),
            section("Les 3 garde-fous", "Comment je construis pour que l'erreur reste sans conséquence",
                prose("<p><strong>1. La validation humaine</strong> : l'IA propose, un humain valide. Surtout pour les montants et les décisions.</p>"
                      "<p><strong>2. Le contexte fourni</strong> : l'IA ne « devine » pas à partir de rien : elle travaille sur vos documents, pas sur sa mémoire.</p>"
                      "<p><strong>3. Les alertes et la supervision</strong> : si une anomalie sort, vous le savez immédiatement. C'est le rôle de la maintenance (150-300 €/mois) et de la garantie « sinon vous ne payez pas ».</p>"
                      "<p>L'objectif n'est pas une IA parfaite (ça n'existe pas). C'est un système où <strong>l'erreur est possible, détectable et sans conséquence</strong>.</p>")),
        ],
        faq=[
            ("C'est quoi exactement une hallucination ?", "Quand l'IA affirme quelque chose de faux avec assurance : un chiffre inventé, un fait mélangé. Ce n'est pas un bug rare, c'est un comportement connu, et gérable."),
            ("Elle peut se tromper sur mes factures ?", "Elle peut. C'est pour ça qu'on ne lui fait jamais valider seule : elle extrait, vous validez. Et les anomalies sont signalées par des alertes."),
            ("Pourquoi l'utiliser alors ?", "Parce que 95 % de ce qu'elle fait est excellent et fait gagner des heures. L'enjeu est de cadrer les 5 % qui peuvent poser problème : c'est exactement le travail de conception."),
            ("Comment savoir si elle se trompe ?", "En vérifiant les points critiques (montants, dates, noms) et en gardant un humain dans la boucle. Les systèmes bien construits signalent eux-mêmes les cas douteux."),
        ],
        nav_links=[("automatisation-et-humain.html", "L'automatisation et l'humain"), ("methode.html", "La méthode + fiabilité"), ("tarifs.html", "Maintenance et garantie"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="apprendre-n8n.html",
        title="Apprendre n8n : par où commencer (gratuit, sans coder)",
        meta="Apprendre n8n de zéro : le principe en 5 minutes, l'installation gratuite, la première automatisation guidée, et quand passer à l'IA. Sans jargon.",
        h1="Apprendre n8n : <em>le parcours simple.</em>",
        sub="n8n permet d'automatiser sans coder. Voici comment l'apprendre à votre rythme : ou comment déléguer pour aller plus vite.",
        sections=[
            section("D'abord, le principe", "5 minutes pour comprendre",
                prose("<p>n8n relie vos outils entre eux avec des blocs visuels : « quand un email arrive → alors cette action se déclenche ». Pas de programmation : on assemble, comme des LEGO. Le détail est sur la page <a href=\"n8n-cest-quoi.html\">n8n, c'est quoi ?</a>.</p>")),
            section("Le parcours en 4 étapes", "De zéro à votre première automatisation",
                pains([
                    ("1. Comprendre le principe", "10 minutes", "Lire la page « n8n, c'est quoi ? » et regarder 1-2 exemples", "Vous savez expliquer ce que n8n fait"),
                    ("2. Installer (gratuit)", "15-30 minutes", "n8n est open source : installation locale ou cloud gratuit", "Vous avez n8n qui tourne chez vous"),
                    ("3. Première automatisation guidée", "1-2 heures", "Un exemple simple : email → notification, ou fichier → classement", "Vous avez fait votre premier flux"),
                    ("4. Brancher l'IA", "quelques jours", "Ajouter un agent IA à vos flux (résumés, réponses)", "Vos automatisations comprennent vos documents"),
                ])),
            section("Et si vous voulez aller plus vite ?", "Deux options",
                prose("<p><strong>Se former en autonomie</strong> : la communauté n8n est immense et gratuite (docs, forums, vidéos). C'est le bon chemin si le temps n'est pas un problème.</p>"
                      "<p><strong>Déléguer</strong> : je construis pour vous (offre découverte 490 € pour une première automatisation en 7 jours), ou je forme votre équipe (ateliers pratiques). Vous apprenez ce qui vous intéresse, je m'occupe du reste.</p>")),
        ],
        faq=[
            ("Il faut savoir coder pour apprendre n8n ?", "Non : 95 % se construit visuellement. Un peu de logique (si/alors) aide, mais rien de plus."),
            ("C'est vraiment gratuit ?", "Le logiciel est open source et gratuit. L'hébergement coûte quelques euros par mois si vous ne voulez pas gérer votre serveur."),
            ("Combien de temps pour être autonome ?", "Les bases : 1 journée. Une automatisation utile : 1 semaine. Un système complet : c'est là qu'un professionnel fait la différence."),
            ("Et si je bloque ?", "Vous pouvez me poser la question (15 min offertes), ou partir sur l'offre découverte pour voir un vrai projet livré."),
        ],
        nav_links=[("n8n-cest-quoi.html", "n8n, c'est quoi ?"), ("alternative-a-zapier.html", "Alternative à Zapier"), ("formation-ia-pme.html", "Formation pour équipes"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="gestion-stock-automatique.html",
        title="Gestion de stock automatique : fini les tableaux qui mentent",
        meta="Suivi des entrées/sorties automatique, alertes de rupture, réconciliation d'inventaire : automatisez votre gestion de stock sans changer d'outils.",
        h1="Gestion de stock : <em>fini les tableaux qui mentent.</em>",
        sub="Ruptures surprises, surstocks qui dorment, comptages interminables : la gestion de stock est un des derniers grands pains manuels. Voici ce qu'on automatise.",
        sections=[
            section("Le problème", "Un stock mal suivi coûte double",
                pains([
                    ("Les ruptures", "Un produit manque au moment de la vente", "Vente perdue + client déçu", "Alerte automatique avant la rupture"),
                    ("Les surstocks", "De l'argent immobilisé dans le placard", "Trésorerie inutilement bloquée", "Prévisions simples pour commander juste"),
                    ("Le comptage", "L'inventaire à la main", "Des heures perdues, des écarts", "Réconciliation automatique comptage/théorique"),
                ])),
            section("Ce qu'on automatise", "Le suivi sans saisie",
                pains([
                    ("Les entrées et sorties", "Chaque mouvement mis à jour à la main", "Des saisies oubliées, des écarts", "Mise à jour automatique à chaque facture/commande"),
                    ("L'alerte de seuil", "On découvre la rupture trop tard", "Des ventes perdues", "Alerte dès que le seuil mini est atteint"),
                    ("La prévision simple", "« Combien commander ? » à l'intuition", "Trop ou trop peu", "Estimation basée sur les ventes passées"),
                    ("La réconciliation", "Comptage vs tableau", "Des écarts jamais expliqués", "Écarts signalés, causes investiguées"),
                ])),
            section("Votre crainte, honnêtement", "« Il faudra tout ressaisir ? »",
                prose("<p>Non : l'automatisation se branche sur vos outils actuels (Excel, logiciel de facturation, caisse). Les mouvements se mettent à jour tout seuls à partir de ce que vous faites déjà : vous, vous lisez les alertes le matin.</p>")),
        ],
        faq=[
            ("Ça marche si je suis sur Excel ?", "Oui, c'est même le cas le plus courant : un fichier propre + des automatisations = un stock suivi sans saisie."),
            ("Et si j'ai un logiciel de caisse ou de facturation ?", "On se branche dessus : les ventes et les achats alimentent le stock automatiquement."),
            ("C'est pour quelles entreprises ?", "Commerces, restaurants, artisans, e-commerce : dès qu'il y a des produits qui entrent et sortent."),
            ("Par quoi commencer ?", "L'alerte de seuil est le gain le plus rapide : fini les ruptures surprises, mesurable dès la première semaine."),
        ],
        nav_links=[("automatiser-excel.html", "Automatiser Excel"), ("detecteur-taches.html", "Détecteur de tâches"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-garage.html",
        title="Automatisation garage auto : rappels, devis, RDV : remplissez votre planning",
        meta="Rappels d'entretien automatiques, devis express, prise de RDV, relances : comment un garage auto remplit son planning sans y penser. Exemples concrets.",
        h1="Garage auto : <em>votre planning se remplit tout seul.</em>",
        sub="Chaque voiture qui sort de l'atelier devrait revenir pour l'entretien : encore faut-il penser à le rappeler. Voici les 8 tâches que l'automatisation prend en charge.",
        sections=[
            section("Le quotidien du garage", "Les frustrations qui coûtent du CA",
                pains([
                    ("Les clients qu'on oublie de rappeler", "Entretien, contrôle technique, révision", "Des voitures qui ne reviennent jamais", "Rappel automatique à la bonne date : le client revient"),
                    ("Les devis qui attendent", "Un client compare, le garage voisin répond plus vite", "Des réparations perdues", "Devis chiffré en 30 secondes, 24h/24"),
                    ("Les rendez-vous manqués", "Créneaux d'atelier vides", "Des heures perdues", "Rappels automatiques + créneaux proposés"),
                ])),
            section("Les 8 tâches à automatiser", "De la prise de RDV au rappel d'entretien",
                pains([
                    ("Rappels d'entretien et contrôle technique", "Date ou kilométrage atteint", "Le client oublie, le garage aussi", "Rappel automatique : le planning se remplit seul"),
                    ("Devis de réparation express", "Demande via téléphone/WhatsApp", "Réponse demain, peut-être", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Prise de RDV atelier", "Allers-retours pour caler un créneau", "Des appels perdus", "Créneaux proposés automatiquement + confirmation"),
                    ("Facturation pièces et main d'œuvre", "Saisie manuelle", "Des erreurs et des heures", "Facture générée à partir de l'ordre de réparation"),
                    ("Relance des impayés", "Réparations payées en retard", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("Les avis Google", "La réputation locale du garage", "Des avis sans réponse", "Réponse automatique + demande d'avis post-réparation"),
                    ("La recherche de pièces", "Des heures sur les catalogues", "Du temps perdu", "Recherche et comparaison assistées"),
                    ("Le suivi des véhicules en atelier", "Où en est la voiture de M. Martin ?", "Des appels de suivi", "Statut envoyé automatiquement au client"),
                ])),
            section("Votre crainte, honnêtement", "« Pour une voiture, le client veut un humain. »",
                prose("<p>Et il l'aura : le diagnostic et le conseil restent 100 % humains. L'automatisation s'occupe de <strong>ce qui entoure la réparation</strong> : le rappel, le devis, le créneau, la relance. Résultat : le garage répond vite, le client se sent suivi, et l'atelier reste plein.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel d'atelier ?", "Oui : on se branche sur vos outils (planning, facturation, catalogue). L'automatisation travaille avec ce que vous utilisez déjà."),
            ("Les rappels automatiques, ça ne saoule pas les clients ?", "Un rappel d'entretien à la bonne date est perçu comme un service, pas du spam. C'est même ce qui fait revenir les clients."),
            ("Par quoi commencer ?", "Le rappel d'entretien est le gain le plus rapide : votre carnet de rendez-vous se remplit avec les clients existants."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-artisan.html", "Artisans"), ("prise-rendez-vous.html", "Prise de RDV"), ("tarifs.html", "Les tarifs"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-restauration.html",
        title="Automatisation restaurant : réservations, planning, fournisseurs : sans stress",
        meta="Réservations avec rappels, planning du personnel, commandes fournisseurs : comment un restaurant arrête les no-show et les ruptures. Exemples concrets.",
        h1="Restaurant : <em>le service, pas la paperasse.</em>",
        sub="Les réservations oubliées, le planning du samedi soir, les commandes fournisseurs : l'automatisation enlève l'administratif pour que vous gardiez l'essentiel : le service et la cuisine.",
        sections=[
            section("Le quotidien du resto", "Les 3 frustrations qui font perdre de l'argent",
                pains([
                    ("Les réservations oubliées", "Une table qui se libère sans prévenir", "Du CA perdu en service", "Confirmation + rappel automatique : les no-show chutent"),
                    ("Le planning du personnel", "Heures sup, roulements, urgences", "Des soirées sous-staffées", "Planning clair + alertes, chacun sait quand il travaille"),
                    ("Les ruptures fournisseurs", "On découvre le manque en plein service", "Des plats rayés de la carte", "Commandes réappro basées sur vos ventes"),
                ])),
            section("Les 8 tâches à automatiser", "De la réservation au rapprochement de caisse",
                pains([
                    ("Réservations + rappels", "Téléphone, messages, no-show", "Des tables perdues chaque semaine", "Confirmation auto, rappel J-1, table libérée signalée"),
                    ("Planning du personnel", "Roulements, week-ends, congés", "Des heures de bricolage", "Planning partagé + alertes de conflit"),
                    ("Commandes fournisseurs", "Inventaire à la main", "Ruptures ou surplus", "Réappro suggéré d'après les ventes"),
                    ("Devis traiteur / événements", "Demandes par téléphone", "Des réponses lentes", "Devis chiffré en 30 secondes, 24h/24"),
                    ("La carte et les prix", "Mise à jour sur tous les supports", "Des incohérences", "Carte centralisée, mise à jour en 1 clic"),
                    ("Les avis Google", "La réputation fait le choix du resto", "Des avis sans réponse", "Réponse auto + demande d'avis après le repas"),
                    ("La saisie des ventes", "Fin de service, rapprochement caisse", "Des heures de pointage", "Rapprochement automatique caisse/ventes"),
                    ("La gestion de stock", "Aliments, boissons, fournitures", "Des pertes et des manques", "Suivi automatique, alertes de seuil"),
                ])),
            section("Votre crainte, honnêtement", "« Ça va casser l'ambiance du resto ? »",
                prose("<p>Non : le client ne voit jamais l'automatisation, il voit un service plus rapide (confirmation immédiate, pas de table perdue, réponse à sa demande traiteur le soir même). <strong>L'ambiance, c'est vous : l'automatisation vous y laisse du temps.</strong></p>")),
        ],
        faq=[
            ("On est déjà débordés, on n'a pas le temps de s'y mettre.", "C'est le principe : vous décrivez, je construis. La première automatisation (souvent les rappels de réservation) est livrée en 7 jours et se fait oublier."),
            ("Ça marche avec ma caisse et mon logiciel ?", "Oui : on se branche sur vos outils actuels. Rien ne change pour votre équipe."),
            ("Et les réservations par téléphone ?", "L'automatisation gère les messages et le site ; le téléphone reste pour ceux qui préfèrent : l'IA peut aussi prendre le premier appel si vous le souhaitez."),
            ("Par quoi commencer ?", "Les rappels de réservation : le no-show est le premier poste de perte, et c'est mesurable dès la première semaine."),
        ],
        nav_links=[("gestion-stock-automatique.html", "Gestion de stock"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-cabinet-medical.html",
        title="Automatisation cabinet médical : RDV, comptes-rendus, honoraires : sans paperasse",
        meta="Prise de RDV avec rappels, comptes-rendus de consultation, relances d'honoraires : comment un cabinet médical gagne des heures. Exemples concrets, RGPD respecté.",
        h1="Cabinet médical : <em>l'IA qui soigne votre agenda.</em>",
        sub="Kiné, dentiste, ostéo, médecin : le rendez-vous manqué et le compte-rendu à rédiger vous volent des heures chaque semaine. Voici ce qu'on automatise : dans le respect du secret médical.",
        sections=[
            section("Le quotidien du cabinet", "Les frustrations qui épuisent",
                pains([
                    ("Les rendez-vous manqués", "Un créneau perdu = une heure non facturée", "Des trous dans l'agenda", "Rappel automatique + liste d'attente qui se remplit"),
                    ("Les comptes-rendus à rédiger", "Dictées, notes, courriers", "Des heures chaque soir", "CR structuré en 1 minute, validé par vous"),
                    ("Le standard qui sonne", "Les mêmes questions chaque jour", "Des interruptions permanentes", "Réponses automatiques aux questions fréquentes"),
                ])),
            section("Les 8 tâches à automatiser", "De la prise de RDV au suivi des patients",
                pains([
                    ("Prise de RDV + rappels", "Téléphone, messages", "Des créneaux perdus", "Créneaux proposés, confirmation, rappel J-1"),
                    ("Liste d'attente intelligente", "Un désistement de dernière minute", "Un créneau vide", "Le prochain patient prévenu automatiquement"),
                    ("Comptes-rendus de consultation", "Dictée ou notes manuscrites", "Des heures de rédaction", "Résumé structuré généré puis validé"),
                    ("Courriers et ordonnances types", "Documents répétitifs", "Du copier-coller", "Génération à partir du dossier, relecture incluse"),
                    ("Relance des honoraires", "Paiements en attente", "Des relances gênantes", "Relance polie et automatique en 3 paliers"),
                    ("Les avis Google", "La réputation du cabinet", "Des patients satisfaits silencieux", "Demande d'avis automatique + réponses"),
                    ("Le standard / questions fréquentes", "Horaires, préparation, documents à apporter", "Des interruptions", "Réponses immédiates, les cas réels au secrétariat"),
                    ("Le suivi des dossiers", "Documents, comptes-rendus, examens", "Des pièces égarées", "Classement automatique + alertes"),
                ])),
            section("Votre crainte, honnêtement", "« Le secret médical, alors ? »",
                prose("<p>Première bonne question. La règle : <strong>les données restent chez vous</strong> (outils auto-hébergés, pas de plateforme tierce), l'IA travaille sur vos documents sans les transmettre, et <strong>tout ce qui sort est validé par vous</strong>. C'est un assistant interne, pas un prestataire externe : comme pour les avocats.</p>")),
        ],
        faq=[
            ("Est-ce compatible avec le secret médical ?", "Oui, avec les bons outils : données hébergées chez vous, pas de réutilisation par des tiers, validation humaine systématique. On vérifie la configuration ensemble dès l'audit."),
            ("Les comptes-rendus seront-ils fiables ?", "Ils reprennent vos notes et la consultation, structurés. Vous relisez et validez avant envoi : 2 minutes au lieu de 2 heures."),
            ("Mes patients verront-ils un changement ?", "Ils verront un cabinet qui répond vite et qui les rappelle pour leurs RDV. Pour eux, c'est un meilleur service."),
            ("Par quoi commencer ?", "Les rappels de RDV : le no-show est le premier poste de perte, mesurable dès la première semaine."),
        ],
        nav_links=[("professions-liberales.html", "Professions libérales"), ("prise-rendez-vous.html", "Prise de RDV"), ("confidentialite.html", "Confidentialité"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-coiffure.html",
        title="Automatisation salon de coiffure : RDV, rappels, avis : des créneaux pleins",
        meta="Prise de RDV avec rappels, rappels de recoloration, avis Google : comment un salon de coiffure remplit ses créneaux et fait revenir ses clientes. Exemples concrets.",
        h1="Salon de coiffure : <em>des créneaux pleins, des clientes qui reviennent.</em>",
        sub="Un rendez-vous oublié, c'est un fauteuil vide. Une cliente qui ne revient pas, c'est du CA perdu. Voici les 8 automatisations qui remplissent votre planning.",
        sections=[
            section("Le quotidien du salon", "Les frustrations qui vident les fauteuils",
                pains([
                    ("Les rendez-vous oubliés", "Un no-show = un fauteuil vide", "Des heures perdues", "Rappel automatique la veille : les oublis chutent"),
                    ("Les clientes qui ne reviennent pas", "Recoloration, coupe, soin", "Elles oublient, vous aussi", "Rappel au bon moment : la cliente revient"),
                    ("Les avis Google", "La réputation fait choisir le salon", "Des clientes satisfaites silencieuses", "Demande d'avis automatique après la prestation"),
                ])),
            section("Les 8 tâches à automatiser", "De la prise de RDV au rappel de recoloration",
                pains([
                    ("Prise de RDV + rappels", "Téléphone, messages, oublis", "Des créneaux perdus", "Créneaux proposés, confirmation, rappel J-1"),
                    ("Rappels de retouche / recoloration", "4 à 6 semaines après la prestation", "La cliente oublie de revenir", "Rappel personnalisé au bon moment"),
                    ("Demande d'avis Google", "La réputation locale", "Des avis sans demande", "SMS/WhatsApp post-prestation → avis"),
                    ("Devis prestations spéciales", "Mariages, événements", "Des réponses lentes", "Devis chiffré en 30 secondes"),
                    ("La carte des prestations", "Prix et services sur tous les supports", "Des incohérences", "Carte centralisée, mise à jour en 1 clic"),
                    ("Les relances forfaits / abonnements", "Forfaits mensuels, cartes de fidélité", "Des revenus oubliés", "Relance automatique avant échéance"),
                    ("La gestion des stocks produits", "Shampoings, colorations, ventes", "Des ruptures en plein service", "Alerte de seuil + commandes suggérées"),
                    ("Les messages clients", "Confirmations, anniversaires, promos", "Des heures de textos", "Messages automatiques, ton du salon"),
                ])),
            section("Votre crainte, honnêtement", "« Mes clientes viennent pour l'ambiance, pas pour un robot. »",
                prose("<p>Et c'est exactement pourquoi on automatise l'administratif : <strong>l'ambiance, c'est vous, dans le fauteuil</strong>. L'automatisation s'occupe des rappels, des confirmations, des avis : les clientes voient juste un salon qui pense à elles.</p>")),
        ],
        faq=[
            ("Mes clientes ne vont pas trouver ça froid ?", "Un rappel « votre recoloration est à refaire cette semaine, créneau jeudi 15h ? » est perçu comme de l'attention, pas du froid. C'est ce qui fait revenir."),
            ("Ça marche avec mon agenda actuel ?", "Oui : on se branche sur votre planning (papier, Excel ou logiciel). Rien ne change pour votre équipe."),
            ("Par quoi commencer ?", "Les rappels de RDV : le no-show est le premier poste de perte, mesurable dès la première semaine."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("prise-rendez-vous.html", "Prise de RDV"), ("repondre-avis-google.html", "Avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-transport.html",
        title="Automatisation transport : factures, tournées, impayés : le papier qui roule tout seul",
        meta="Facturation des tournées, lettres de voiture, relances d'impayés : comment une entreprise de transport automatise la paperasse. Exemples concrets.",
        h1="Transport : <em>faites rouler les camions, pas le papier.</em>",
        sub="Chaque tournée génère une facture, une lettre de voiture, un suivi. Quand il y a 10 véhicules, c'est une montagne de papier. Voici comment l'automatiser.",
        sections=[
            section("Le quotidien du transporteur", "Les frustrations qui ralentissent la trésorerie",
                pains([
                    ("La facturation des tournées", "Chaque course = une facture à saisir", "Des heures de saisie en fin de semaine", "Facture générée automatiquement depuis la tournée"),
                    ("Les impayés", "Les clients paient lentement", "Une trésorerie qui souffre", "Relance automatique en 3 paliers"),
                    ("Les documents", "Lettres de voiture, mandats, preuves", "Des classeurs entiers", "Documents générés, classés, retrouvables"),
                ])),
            section("Les 8 tâches à automatiser", "De la demande de devis au rappel de paiement",
                pains([
                    ("Devis de transport / déménagement", "Volume, distance, prestations", "Des réponses lentes, des clients perdus", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Facturation des tournées", "Saisie manuelle par course", "Des heures et des erreurs", "Facture générée depuis la tournée, envoyée seule"),
                    ("Relance des impayés", "30, 60, 90 jours", "De l'argent qui dort", "Relance polie et automatique en 3 paliers"),
                    ("Lettres de voiture et documents", "Génération + archivage", "Des classeurs ingérables", "Documents générés et classés automatiquement"),
                    ("Suivi des livraisons", "« Où est ma livraison ? »", "Des appels de suivi", "Statut envoyé automatiquement au client"),
                    ("Planning véhicules / chauffeurs", "Affectations, congés, entretien", "Des conflits d'agenda", "Planning clair + alertes"),
                    ("Entretien et contrôles techniques", "CT, révisions, assurances", "Des échéances oubliées", "Alertes automatiques avant échéance"),
                    ("Les avis Google", "La réputation du transporteur", "Des clients sans retour", "Demande d'avis après livraison"),
                ])),
            section("Votre crainte, honnêtement", "« Mes tournées ne se ressemblent jamais. »",
                prose("<p>Et c'est normal : on n'automatise pas la conduite ni l'organisation des tournées. On automatise <strong>le papier autour</strong> : la facture, la lettre de voiture, la relance. Chaque tournée reste unique, sa paperasse ne l'est plus.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de gestion de transport ?", "Oui : on se branche sur vos outils (planning, facturation, TMS). L'automatisation complète ce que vous utilisez déjà."),
            ("Les factures seront-elles conformes ?", "Oui : elles reprennent vos mentions et votre format, avec la facturation électronique 2026 intégrée quand c'est nécessaire."),
            ("Par quoi commencer ?", "La facturation des tournées : c'est le plus gros volume de saisie, mesurable dès la première semaine."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatiser-factures.html", "Automatiser les factures"), ("relance-impayes.html", "Relance des impayés"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-auto-ecole.html",
        title="Automatisation auto-école : leçons pleines, zéro heure perdue, dossiers à jour",
        meta="Rappels de leçon, planning des moniteurs, dossiers élèves, relances de forfaits : comment une auto-école arrête les heures perdues. Exemples concrets.",
        h1="Auto-école : <em>plus jamais d'heure de conduite perdue.</em>",
        sub="Un élève qui oublie sa leçon, c'est une heure perdue pour vous et pour le moniteur. Les dossiers CERFA, les forfaits, le planning : voici ce qu'on automatise.",
        sections=[
            section("Le quotidien de l'auto-école", "Les frustrations qui font perdre des heures",
                pains([
                    ("Les leçons oubliées", "Un élève qui ne vient pas", "Une heure de moniteur perdue", "Rappel automatique la veille : les oublis chutent"),
                    ("Les dossiers administratifs", "CERFA, contrats, documents", "Des soirées de paperasse", "Dossiers générés, classés, à jour"),
                    ("Les demandes d'inscription", "Appels, messages, devis", "Des réponses lentes, des élèves perdus", "Réponse immédiate avec le forfait adapté"),
                ])),
            section("Les 8 tâches à automatiser", "De l'inscription à l'examen",
                pains([
                    ("Rappels de leçon", "La veille, à heure fixe", "Des trous dans le planning", "Rappel automatique : l'élève arrive préparé"),
                    ("Planning des moniteurs", "Leçons, examens, pauses", "Des conflits d'agenda", "Planning partagé, alertes de chevauchement"),
                    ("Dossiers élèves automatisés", "CERFA, contrat, suivi d'heures", "Des classeurs entiers", "Documents générés et classés automatiquement"),
                    ("Réponse aux demandes d'inscription", "« Combien coûte le forfait ? »", "Des réponses en retard", "Réponse 24h/24 avec forfait et créneaux"),
                    ("Relance des forfaits impayés", "Paiements en plusieurs fois", "De l'argent oublié", "Relance polie et automatique en 3 paliers"),
                    ("Suivi des heures de conduite", "Heures restantes par élève", "Des comptages à la main", "Solde envoyé automatiquement à l'élève"),
                    ("Rappels d'examen et de code", "Dates, révisions", "Des rendez-vous manqués", "Rappels + documents de préparation"),
                    ("Les avis Google", "La réputation locale", "Des élèves satisfaits silencieux", "Demande d'avis après l'obtention du permis"),
                ])),
            section("Votre crainte, honnêtement", "« Mes élèves veulent parler à quelqu'un. »",
                prose("<p>Et ils le peuvent : l'automatisation s'occupe des rappels, des documents et des relances : <strong>l'humain reste sur la route et à l'accueil</strong>. Les élèves voient une auto-école organisée, qui pense à eux. C'est exactement ce qui fait choisir une école.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel d'auto-école ?", "Oui : on se branche sur vos outils (planning, dossiers, facturation). Rien ne change pour vos moniteurs."),
            ("Les rappels ne dérangent pas ?", "Un rappel de leçon la veille est un service : l'élève est rassuré, vous gardez votre créneau."),
            ("Par quoi commencer ?", "Les rappels de leçon : le premier poste d'heures perdues, mesurable dès la première semaine."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-artisan.html", "Artisans"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-salle-sport.html",
        title="Automatisation salle de sport : abonnés qui restent, cours pleins, zéro relance oubliée",
        meta="Rappels de séance, relance des abonnements, planning des coachs, liste d'attente : comment une salle de sport garde ses abonnés. Exemples concrets.",
        h1="Salle de sport : <em>des abonnés qui restent, des cours qui se remplissent.</em>",
        sub="Un abonné qui arrête, c'est souvent un abonné qu'on n'a pas rappelé. Un cours avec des places vides, c'est du CA perdu. Voici les automatisations qui changent la donne.",
        sections=[
            section("Le quotidien de la salle", "Les frustrations qui vident les salles",
                pains([
                    ("Les abonnés qui ne reviennent pas", "Absence, oubli, manque de motivation", "Des abonnements qui s'arrêtent", "Rappel automatique : l'abonné revient avant d'arrêter"),
                    ("Les cours à moitié vides", "Des places libres non remplies", "Du CA perdu", "Liste d'attente + rappel de séance : les cours se remplissent"),
                    ("Les relances oubliées", "Renouvellements, impayés", "De l'argent qui dort", "Relance automatique en 3 paliers"),
                ])),
            section("Les 8 tâches à automatiser", "De l'inscription au renouvellement",
                pains([
                    ("Rappels de séance / de cours", "La veille, avec l'horaire", "Des absences évitables", "Rappel automatique : le cours se remplit"),
                    ("Relance des abonnements", "Impayés, renouvellement", "Des abonnés perdus", "Relance polie et automatique en 3 paliers"),
                    ("Liste d'attente intelligente", "Un cours complet, une place libérée", "Des places perdues", "Le prochain de la liste prévenu automatiquement"),
                    ("Planning des coachs et des cours", "Cours, créneaux, remplacements", "Des conflits d'agenda", "Planning partagé, alertes automatiques"),
                    ("Inscription en ligne", "Formulaires, paiement, contrat", "Des inscriptions perdues", "Inscription complète en 2 minutes, 24h/24"),
                    ("Rappels de renouvellement", "Échéance d'abonnement", "Des abonnés qui glissent", "Rappel avant échéance + offre de reconduction"),
                    ("Les avis Google", "La réputation locale", "Des membres silencieux", "Demande d'avis après 30 jours de présence"),
                    ("Notification des nouveaux cours", "Programme, événements", "Des membres pas au courant", "Annonces automatiques par canal favori"),
                ])),
            section("Votre crainte, honnêtement", "« Le sport, c'est du relationnel. »",
                prose("<p>Exactement : c'est pour ça qu'on automatise <strong>l'administratif qui vous vole le relationnel</strong>. Les rappels, les relances, les inscriptions tournent seuls : vous, vous êtes sur le terrain avec vos membres. L'abonné reçoit de l'attention, pas du spam : c'est comme ça qu'il reste.</p>")),
        ],
        faq=[
            ("Ça marche avec ma salle qui fonctionne au papier ?", "Oui : on commence par le rappel de séance (un simple fichier de membres suffit) et on ajoute au fur et à mesure."),
            ("Les relances ne font pas fuir les membres ?", "Une relance de renouvellement polie avec une offre de reconduction est bien reçue : c'est une attention, pas une pression."),
            ("Par quoi commencer ?", "Le rappel de séance : les cours se remplissent, les absences chutent, et c'est mesurable dès la première semaine."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-coiffure.html", "Coiffure / beauté"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-pharmacie.html",
        title="Automatisation pharmacie : standard, commandes, renouvellements : le conseil d'abord",
        meta="Standard qui répond, commandes fournisseurs, rappels de renouvellement : comment une pharmacie allège l'officine sans jamais remplacer le conseil. RGPD.",
        h1="Pharmacie : <em>l'automatisation au service du conseil.</em>",
        sub="Le standard qui sonne, les commandes, les renouvellements : chaque heure passée sur l'administratif est une heure de moins pour le conseil. Voici comment l'alléger.",
        sections=[
            section("Le quotidien de l'officine", "Les frustrations qui saturent le comptoir",
                pains([
                    ("Le standard qui sonne", "Horaires, préparation, disponibilité", "Des interruptions au comptoir", "Réponses automatiques : le téléphone se calme"),
                    ("Les commandes fournisseurs", "Inventaires, ruptures, urgences", "Des heures par semaine", "Commandes suggérées d'après vos ventes"),
                    ("Les renouvellements", "Ordonnances récurrentes, traitements longs", "Des patients qui oublient", "Rappel automatique avec accord du pharmacien"),
                ])),
            section("Les 8 tâches à automatiser", "Du standard au rapprochement",
                pains([
                    ("Standard / questions fréquentes", "Horaires, préparation, documents", "Des interruptions", "Réponses immédiates, les cas réels au comptoir"),
                    ("Commandes fournisseurs", "Inventaire à la main", "Ruptures ou surstocks", "Réappro suggéré d'après les ventes, validation incluse"),
                    ("Rappels de renouvellement", "Ordonnance récurrente", "Des traitements interrompus", "Rappel avec l'accord du pharmacien, jamais sans lui"),
                    ("Les avis Google", "La réputation de l'officine", "Des patients satisfaits silencieux", "Demande d'avis + réponses automatiques"),
                    ("Gestion des stocks", "Médicaments, parapharmacie", "Des pertes et des ruptures", "Suivi automatique, alertes de seuil"),
                    ("Facturation matériel médical", "Location, dispositifs", "De la saisie répétitive", "Factures générées, relances comprises"),
                    ("Le rapprochement de caisse", "Fin de journée, remboursements", "Des heures de pointage", "Rapprochement automatique caisse/ventes"),
                    ("Suivi des dossiers", "Ordonnances, documents", "Des pièces égarées", "Classement automatique, retrouvabilité immédiate"),
                ])),
            section("Votre crainte, honnêtement", "« Le conseil pharmaceutique ne se déléguera jamais. »",
                prose("<p>Et c'est exactement le principe : <strong>l'IA ne conseille JAMAIS</strong>. Elle ne répond pas aux questions de santé, elle ne propose aucun traitement : elle transmet tout au pharmacien. Elle s'occupe uniquement de l'administratif (standard, commandes, rappels, stocks), dans le respect du secret et du RGPD : données chez vous, validation humaine systématique.</p>")),
        ],
        faq=[
            ("C'est compatible avec le secret pharmaceutique ?", "Oui : données hébergées chez vous, pas de réutilisation par un tiers, et l'IA ne répond jamais à une question de santé : tout est transmis à l'équipe."),
            ("Les patients vont-ils parler à un robot ?", "Non : le comptoir reste 100 % humain. L'automatisation gère le standard et les rappels administratifs, rien d'autre."),
            ("Par quoi commencer ?", "Le standard : les questions répétitives (horaires, préparation) représentent la majorité des appels."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-cabinet-medical.html", "Cabinet médical"), ("gestion-stock-automatique.html", "Gestion de stock"), ("confidentialite.html", "Confidentialité"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-hotellerie.html",
        title="Automatisation hôtel / gîte : réservations directes, avis, ménage : sans Booking",
        meta="Réservations directes avec rappels, réponses aux avis, planning du ménage : comment un hôtel ou gîte réduit sa dépendance aux plateformes. Exemples concrets.",
        h1="Hôtel / gîte : <em>moins de Booking, plus de direct.</em>",
        sub="Chaque réservation via Booking coûte 15-20 % de commission. Les réservations directes se construisent avec du bon contenu, des rappels et des avis. Voici comment l'automatiser.",
        sections=[
            section("Le quotidien de l'hôtelier", "Les frustrations qui grignotent la marge",
                pains([
                    ("Les commissions des plateformes", "15-20 % sur chaque réservation", "La marge fond", "Réservations directes encouragées par l'automatisation"),
                    ("Les avis sans réponse", "La réputation se joue sur Google/Tripadvisor", "Des avis ignorés", "Réponse automatique + demande d'avis au départ"),
                    ("Le planning du ménage", "Check-out/check-in, urgences", "Des chambres pas prêtes", "Planning auto + alertes de libération"),
                ])),
            section("Les 8 tâches à automatiser", "De la réservation au retour du client",
                pains([
                    ("Réservations directes + rappels", "Le client réserve sur le site", "Des commissions perdues", "Confirmation auto, rappel J-2, check-in simplifié"),
                    ("Demande d'avis au départ", "Le client satisfait repart", "Des avis jamais écrits", "SMS/email post-checkout → avis Google"),
                    ("Réponse aux avis", "Positifs, neutres, négatifs", "Des avis sans réponse", "Réponse automatique avec ton de l'établissement"),
                    ("Planning du ménage", "Check-outs, check-ins, urgences", "Des chambres pas prêtes", "Planning auto + alerte de chambre libérée"),
                    ("Devis séminaires / événements", "Demandes de groupes", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("Relance des arrhes et soldes", "Acomptes, soldes restants", "De l'argent en attente", "Relance polie et automatique en 3 paliers"),
                    ("Le standard / questions fréquentes", "Horaires, parking, wifi, animaux", "Des interruptions", "Réponses immédiates, les cas réels à la réception"),
                    ("La gestion des canaux", "Disponibilités sur plusieurs plateformes", "Des surréservations", "Synchronisation + fermeture auto des canaux complets"),
                ])),
            section("Votre crainte, honnêtement", "« Mes clients veulent parler à quelqu'un. »",
                prose("<p>Et ils le peuvent : la réception reste 100 % humaine. L'automatisation s'occupe des confirmations, rappels, avis et relances : <strong>les clients voient un établissement réactif, les plateformes voient moins de commissions</strong>. C'est exactement ce qui fait basculer la réservation en direct.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de réservation ?", "Oui : on se branche sur vos outils (channel manager, planning, caisse). Rien ne change pour votre équipe."),
            ("Les rappels ne dérangent pas les clients ?", "Un rappel de réservation avec check-in simplifié est un service : le client est rassuré, vous réduisez les no-show."),
            ("Par quoi commencer ?", "La demande d'avis au départ : vos clients satisfaits deviennent votre meilleure publicité, mesurable dès la première semaine."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-restauration.html", "Restaurant / traiteur"), ("repondre-avis-google.html", "Avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-pressing.html",
        title="Automatisation pressing : suivi des articles, relances, avis : zéro vêtement perdu",
        meta="Suivi des articles avec étiquettes, relances de retrait, demandes d'avis : comment un pressing gagne du temps et fidélise. Exemples concrets.",
        h1="Pressing : <em>zéro vêtement perdu, zéro relance oubliée.</em>",
        sub="Un article qui traîne, un client qui ne revient pas, un avis jamais laissé : le pressing vit de la confiance et de la régularité. Voici les automatisations qui changent la donne.",
        sections=[
            section("Le quotidien du pressing", "Les frustrations qui usent la confiance",
                pains([
                    ("Le suivi des articles", "Des dizaines de vêtements par jour", "Des erreurs, des pertes", "Suivi par étiquette, statut à jour en temps réel"),
                    ("Les articles oubliés", "Les clients ne reviennent pas chercher", "Des stocks qui s'accumulent", "Rappel automatique quand l'article est prêt"),
                    ("Les avis Google", "La confiance locale", "Des clients silencieux", "Demande d'avis après le retrait"),
                ])),
            section("Les 8 tâches à automatiser", "Du dépôt au retrait",
                pains([
                    ("Suivi des articles (étiquettes)", "Dépôts, nettoyage, repassage", "Des articles égarés", "Suivi par étiquette, statut visible à chaque étape"),
                    ("Notification article prêt", "Le nettoyage est terminé", "Le client oublie de revenir", "SMS/email automatique « votre article est prêt »"),
                    ("Relance des articles en souffrance", "30, 60 jours sans retrait", "Des stocks qui s'accumulent", "Relance polie + suggestion de livraison"),
                    ("Demande d'avis au retrait", "Le client récupère son article", "Des avis jamais écrits", "SMS post-retrait → avis Google"),
                    ("Le point de caisse / encaissement", "Paiements, abonnements", "Des erreurs de caisse", "Rapprochement automatique caisse/ventes"),
                    ("Les abonnements (nettoyage régulier)", "Chemises, costumes, linge", "Des revenus irréguliers", "Rappel + renouvellement automatique d'abonnement"),
                    ("Devis pour particuliers / pros", "Costumes, rideaux, hôtels", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("La gestion des stocks produits", "Produits de lavage, emballages", "Des ruptures", "Alerte de seuil + commande suggérée"),
                ])),
            section("Votre crainte, honnêtement", "« Mes clients passent en boutique, pas en ligne. »",
                prose("<p>Et c'est parfait : l'automatisation ne remplace pas le passage en boutique, elle <strong>fait revenir</strong> : le SMS « votre article est prêt » ramène le client, la demande d'avis construit la réputation, la relance récupère les articles oubliés. Le commerce reste humain, le suivi devient infaillible.</p>")),
        ],
        faq=[
            ("Mes clients sont plutôt âgés, le SMS ça marche ?", "Le SMS est le canal le plus universel : tout le monde le lit. Et l'option « appeler » reste pour ceux qui préfèrent."),
            ("Ça marche avec mon logiciel de pressing ?", "Oui : on se branche sur vos outils (étiquettes, caisse). L'automatisation complète ce que vous utilisez déjà."),
            ("Par quoi commencer ?", "La notification article prêt : elle fait revenir les clients et libère de l'espace de stockage."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("service-client.html", "Service client"), ("repondre-avis-google.html", "Avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-electricien.html",
        title="Automatisation électricien : devis express, rappels d'entretien, chantiers : sans paperasse",
        meta="Devis électricien en 30 secondes, rappels d'entretien, planning chantiers, attestations : comment un électricien gagne des heures. Exemples concrets.",
        h1="Électricien : <em>des devis en 30 secondes, des chantiers suivis.</em>",
        sub="Chaque devis rédigé à la main, chaque attestation à remplir, chaque client à rappeler : l'administratif mange le temps de chantier. Voici ce qu'on automatise.",
        sections=[
            section("Le quotidien de l'électricien", "Les frustrations qui ralentissent les chantiers",
                pains([
                    ("Les devis à la main", "Chaque intervention = un devis à rédiger", "Des soirées de paperasse", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Les attestations", "Conformité, consuel, garanties", "Des formulaires répétitifs", "Documents générés à partir du chantier"),
                    ("Les rappels d'entretien", "Vérifications périodiques", "Des clients qui oublient", "Rappel automatique au bon moment"),
                ])),
            section("Les 8 tâches à automatiser", "De la demande de devis à la facture",
                pains([
                    ("Devis express", "Demandes via téléphone/WhatsApp", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("Prise de RDV intervention", "Allers-retours pour caler", "Des chantiers perdus", "Créneaux proposés automatiquement + confirmation"),
                    ("Rappels d'entretien périodique", "Vérifications, contrôles", "Des clients qui oublient", "Rappel automatique + créneau proposé"),
                    ("Attestations et documents", "Conformité, garanties, consuel", "Des formulaires répétitifs", "Documents générés à partir des données du chantier"),
                    ("Facturation", "Saisie des heures et matériaux", "Des erreurs et des heures", "Facture générée depuis l'intervention"),
                    ("Relance des impayés", "Chantiers payés en retard", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après le chantier"),
                    ("Le suivi des chantiers", "Où en est le chantier ?", "Des appels de suivi", "Statut envoyé automatiquement au client"),
                ])),
            section("Votre crainte, honnêtement", "« Le client veut un vrai électricien, pas un robot. »",
                prose("<p>Et il l'aura : le diagnostic et l'intervention restent 100 % humains. L'automatisation s'occupe de <strong>ce qui entoure le chantier</strong> : le devis, le créneau, l'attestation, la relance. Résultat : vous répondez vite, vous êtes payé plus vite, et vous passez plus de temps sur les chantiers.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel métier ?", "Oui : on se branche sur vos outils (planning, facturation, devis). L'automatisation travaille avec ce que vous utilisez déjà."),
            ("Les devis automatiques sont-ils fiables ?", "Ils suivent votre grille de prix exacte et vous validez avant envoi. Les cas particuliers sont transmis à l'humain."),
            ("Par quoi commencer ?", "Le devis express : c'est le gain le plus rapide, les clients comparent et répondent vite à qui répond vite."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-artisan.html", "Artisans"), ("automatiser-devis.html", "Automatiser les devis"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-veterinaire.html",
        title="Automatisation cabinet vétérinaire : rappels vaccins, RDV, avis : les animaux reviennent",
        meta="Rappels de vaccins, prise de RDV, demandes d'avis : comment un cabinet vétérinaire remplit son agenda et fidélise. Exemples concrets.",
        h1="Cabinet vétérinaire : <em>des rappels qui sauvent des vies.</em>",
        sub="Un rappel de vaccin oublié, c'est un animal non protégé et un rendez-vous manqué. Voici les automatisations qui remplissent votre agenda : au service des animaux.",
        sections=[
            section("Le quotidien du cabinet", "Les frustrations qui vident l'agenda",
                pains([
                    ("Les vaccins oubliés", "Rappels, rappels, rappels", "Des animaux non protégés", "Rappel automatique au bon moment"),
                    ("Les rendez-vous manqués", "Un créneau perdu", "Des heures non facturées", "Rappel automatique la veille + liste d'attente"),
                    ("Les avis Google", "La réputation locale", "Des clients silencieux", "Demande d'avis après la visite"),
                ])),
            section("Les 8 tâches à automatiser", "Du rappel vaccin au suivi post-op",
                pains([
                    ("Rappels de vaccins et vermifuges", "Échéances par animal", "Des rappels oubliés", "Rappel automatique personnalisé par animal"),
                    ("Prise de RDV + rappels", "Téléphone, messages", "Des créneaux perdus", "Créneaux proposés, confirmation, rappel J-1"),
                    ("Liste d'attente intelligente", "Un désistement", "Un créneau vide", "Le prochain client prévenu automatiquement"),
                    ("Demande d'avis après la visite", "Le client repart rassuré", "Des avis jamais écrits", "SMS post-visite → avis Google"),
                    ("Suivi post-opératoire", "Chirurgies, hospitalisations", "Des suivis oubliés", "Message automatique de suivi + relais si problème"),
                    ("Comptes-rendus de consultation", "Notes, traitements", "Des heures de rédaction", "CR structuré généré puis validé"),
                    ("Relance des paiements", "Soins, hospitalisations", "Des impayés", "Relance polie et automatique en 3 paliers"),
                    ("Le standard / questions fréquentes", "Urgences, horaires, tarifs", "Des interruptions", "Réponses immédiates, les urgences au cabinet"),
                ])),
            section("Votre crainte, honnêtement", "« La relation avec les animaux et leurs maîtres, ça ne se robotise pas. »",
                prose("<p>Et c'est exactement le principe : <strong>le soin et la relation restent 100 % humains</strong>. L'automatisation s'occupe des rappels, des créneaux, des avis : les maîtres voient un cabinet qui pense à leur animal. C'est ce qui fait revenir, encore et encore.</p>")),
        ],
        faq=[
            ("Les rappels sont personnalisables par animal ?", "Oui : chaque animal a ses échéances (vaccins, vermifuges, rappels). Le message cite le nom de l'animal et la date."),
            ("Ça marche avec mon logiciel vétérinaire ?", "Oui : on se branche sur vos outils (planning, dossier patient, facturation). Rien ne change pour votre équipe."),
            ("Par quoi commencer ?", "Les rappels de vaccins : c'est le poste qui remplit l'agenda avec les clients existants."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-cabinet-medical.html", "Cabinet médical"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-food-truck.html",
        title="Automatisation food truck : commandes, tournées, caisse : le camion qui tourne",
        meta="Commandes WhatsApp, planning des tournées, prévisions de stock : comment un food truck automatise sa logistique. Exemples concrets.",
        h1="Food truck : <em>la logistique qui suit le camion.</em>",
        sub="Chaque place de marché a ses pics, chaque jour a sa météo, chaque commande compte. Voici les automatisations qui font tourner le camion sans y penser.",
        sections=[
            section("Le quotidien du food truck", "Les frustrations qui font perdre des ventes",
                pains([
                    ("Les commandes de dernière minute", "Groupes, événements, réguliers", "Des ventes perdues", "Commandes WhatsApp avec confirmation automatique"),
                    ("La prévision des quantités", "Trop ou pas assez", "Du gaspillage ou des ruptures", "Prévision simple d'après les ventes passées"),
                    ("La communication des tournées", "« Où êtes-vous aujourd'hui ? »", "Des clients qui ne savent pas", "Annonce automatique des tournées et horaires"),
                ])),
            section("Les 8 tâches à automatiser", "De la commande à la tournée suivante",
                pains([
                    ("Commandes WhatsApp", "Groupes, événements, réguliers", "Des commandes notées sur un papier", "Confirmation automatique + récap de commande"),
                    ("Annonce des tournées", "Places de marché, événements", "Des clients pas au courant", "Message automatique la veille : « demain à X »"),
                    ("Prévision des quantités", "Ventes passées, météo", "Du gaspillage ou des ruptures", "Quantités suggérées par service"),
                    ("Planning des tournées", "Marchés, événements, privés", "Des conflits de planning", "Planning clair + alertes"),
                    ("Devis événements / privés", "Mariages, entreprises", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("La caisse et le rapprochement", "Fin de service, CB, espèces", "Des heures de pointage", "Rapprochement automatique caisse/ventes"),
                    ("La gestion de stock", "Ingrédients, emballages", "Des ruptures en plein service", "Alerte de seuil + commande suggérée"),
                    ("Les avis Google", "La réputation fait le client", "Des clients satisfaits silencieux", "Demande d'avis après le passage"),
                ])),
            section("Votre crainte, honnêtement", "« Je suis sur la route, je n'ai pas le temps de gérer tout ça. »",
                prose("<p>Justement : l'automatisation travaille <strong>pendant que vous cuisinez</strong>. Les commandes se confirment seules, les tournées s'annoncent seules, les quantités se prévoient seules. Vous, vous tenez la spatule.</p>")),
        ],
        faq=[
            ("Ça marche si je suis seul sur le camion ?", "Oui, c'est même le meilleur cas : l'automatisation remplace la paperasse que vous n'avez pas le temps de faire."),
            ("Les commandes WhatsApp, comment ça marche ?", "Un numéro dédié reçoit les commandes, l'IA confirme et récapitule automatiquement. Vous ne manquez plus rien."),
            ("Par quoi commencer ?", "L'annonce des tournées : vos clients réguliers reviennent dès qu'ils savent où vous êtes."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-restauration.html", "Restaurant / traiteur"), ("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-menuisier.html",
        title="Automatisation menuisier / atelier bois : devis, planning, relances : l'atelier qui tourne",
        meta="Devis menuiserie en 30 secondes, planning d'atelier, relances clients, gestion des commandes : comment un menuisier gagne des heures. Exemples concrets.",
        h1="Menuisier : <em>le bois d'abord, la paperasse ensuite.</em>",
        sub="Chaque projet, chaque devis, chaque livraison génère sa paperasse. Voici comment l'automatisation la fait disparaître, pour que vous passiez plus de temps à l'atelier.",
        sections=[
            section("Le quotidien de l'atelier", "Les frustrations qui rongent les marges",
                pains([
                    ("Les devis à la main", "Chaque projet = un devis détaillé", "Des soirées de paperasse", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Le planning de l'atelier", "Commandes, livraisons, urgences", "Des retards en cascade", "Planning clair + alertes d'échéance"),
                    ("Les clients sans nouvelles", "Où en est ma cuisine ?", "Des appels de suivi", "Statut envoyé automatiquement au client"),
                ])),
            section("Les 8 tâches à automatiser", "De la demande au chantier livré",
                pains([
                    ("Devis express", "Demandes téléphone/WhatsApp", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("Prise de RDV prise de mesures", "Allers-retours pour caler", "Des projets perdus", "Créneaux proposés + confirmation automatique"),
                    ("Planning de l'atelier", "Fabrication, séchage, livraison", "Des retards", "Planning clair + alertes d'échéance"),
                    ("Suivi de commande client", "Fabrication, finition, pose", "Des appels de suivi", "Statut envoyé automatiquement à chaque étape"),
                    ("Relance des devis envoyés", "Devis sans réponse", "Des ventes perdues", "Relance polie J+7 : « avez-vous des questions ? »"),
                    ("Facturation + relance impayés", "Acomptes, soldes", "Trésorerie tendue", "Facture générée + relance en 3 paliers"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après la livraison"),
                    ("La gestion des stocks bois", "Essences, quincaillerie", "Des ruptures", "Alerte de seuil + commande suggérée"),
                ])),
            section("Votre crainte, honnêtement", "« Mes clients veulent du sur-mesure, pas du robot. »",
                prose("<p>Et c'est exactement le principe : <strong>le sur-mesure et le savoir-faire restent 100 % humains</strong>. L'automatisation s'occupe du devis, du planning, des relances et des statuts : le client voit un atelier organisé qui le tient informé. C'est ce qui fait signer.</p>")),
        ],
        faq=[
            ("Les devis automatiques gèrent le sur-mesure ?", "Ils suivent votre grille de prix exacte et vous validez avant envoi. Les cas particuliers sont transmis à l'humain."),
            ("Ça marche avec mon logiciel de gestion ?", "Oui : on se branche sur vos outils (planning, devis, facturation). Rien ne change pour votre équipe."),
            ("Par quoi commencer ?", "Le devis express : c'est le gain le plus rapide, les clients comparent et répondent vite à qui répond vite."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-artisan.html", "Artisans"), ("automatiser-devis.html", "Automatiser les devis"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-camping.html",
        title="Automatisation camping / village vacances : réservations, arrivées, avis : la saison qui tourne",
        meta="Réservations directes, arrivées automatisées, avis, planning des hébergements : comment un camping automatise sa saison. Exemples concrets.",
        h1="Camping : <em>la saison qui tourne sans crise.</em>",
        sub="Juillet-août, tout s'accélère : réservations, arrivées, départs, avis. Voici les automatisations qui transforment le pic de saison en opération fluide.",
        sections=[
            section("Le quotidien du camping", "Les frustrations qui gâchent la saison",
                pains([
                    ("Le téléphone qui sonne", "Réservations, infos, urgences", "Des heures au standard", "Réponses automatiques + réservation en ligne"),
                    ("Les arrivées groupées", "Check-in de 50 familles", "Des files d'attente", "Arrivée simplifiée avec message d'accueil"),
                    ("Les avis", "La réputation fait la saison suivante", "Des avis jamais écrits", "Demande d'avis au départ"),
                ])),
            section("Les 8 tâches à automatiser", "De la réservation au départ",
                pains([
                    ("Réservations directes + rappels", "Le site, pas les OTA", "Des commissions (12-20 %)", "Confirmation auto + rappel J-7 et J-1"),
                    ("Messages d'accueil personnalisés", "Arrivées, hébergement, règles", "Des files d'attente", "Message d'accueil automatique avant l'arrivée"),
                    ("Planning des hébergements", "Mobil-homes, emplacements, ménage", "Des conflits", "Planning auto + alerte de libération"),
                    ("Demande d'avis au départ", "Le client satisfait repart", "Des avis jamais écrits", "SMS post-départ → avis Google"),
                    ("Réponse aux avis", "Positifs, neutres, négatifs", "Des avis sans réponse", "Réponse automatique avec le ton du camping"),
                    ("Relance des arrhes et soldes", "Acomptes, soldes restants", "De l'argent en attente", "Relance polie et automatique"),
                    ("Le standard / questions fréquentes", "Horaires, tarifs, animaux", "Des interruptions", "Réponses immédiates, les cas réels à l'accueil"),
                    ("Devis groupes / événements", "Séminaires, groupes", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                ])),
            section("Votre crainte, honnêtement", "« Mes clients viennent pour l'humain, pas pour les robots. »",
                prose("<p>Et ils le trouvent : l'accueil reste 100 % humain. L'automatisation s'occupe des confirmations, rappels, avis et relances : <strong>le client voit un camping réactif et organisé</strong>, l'équipe se concentre sur l'accueil. C'est la saison qui tourne au lieu de subir.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de réservation ?", "Oui : on se branche sur vos outils (channel manager, planning, caisse). Rien ne change pour votre équipe."),
            ("Les rappels ne dérangent pas ?", "Un rappel de réservation avec check-in simplifié est un service : le client est rassuré, vous réduisez les no-show."),
            ("Par quoi commencer ?", "La demande d'avis au départ : vos campeurs satisfaits deviennent votre meilleure publicité."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-hotellerie.html", "Hôtel / gîte"), ("repondre-avis-google.html", "Avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-paysagiste.html",
        title="Automatisation paysagiste : devis, planning chantiers, contrats d'entretien : le vert rentable",
        meta="Devis paysagiste en 30 secondes, planning des chantiers, contrats d'entretien récurrents : comment un paysagiste sécurise ses revenus. Exemples concrets.",
        h1="Paysagiste : <em>des contrats récurrents, pas que des chantiers.</em>",
        sub="Le chantier se termine, l'argent s'arrête. Les contrats d'entretien, eux, reviennent chaque mois. Voici comment l'automatisation construit la partie récurrente de votre activité.",
        sections=[
            section("Le quotidien du paysagiste", "Les frustrations qui limitent la croissance",
                pains([
                    ("Les devis saisonniers", "Printemps = vague de devis", "Des réponses lentes", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Le planning des équipes", "Chantiers, tonte, arrosage", "Des conflits", "Planning clair + alertes"),
                    ("Les contrats d'entretien", "Tondues, tailles, arrosage", "Des revenus irréguliers", "Rappel + renouvellement automatique des contrats"),
                ])),
            section("Les 8 tâches à automatiser", "Du devis à la tonte récurrente",
                pains([
                    ("Devis express", "Demandes téléphone/WhatsApp", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("Prise de RDV visite technique", "Estimation sur place", "Des projets perdus", "Créneaux proposés + confirmation automatique"),
                    ("Planning des équipes", "Chantiers, tonte, arrosage", "Des conflits", "Planning clair + alertes météo"),
                    ("Contrats d'entretien récurrents", "Tondues, tailles", "Des revenus irréguliers", "Rappel + renouvellement automatique des contrats"),
                    ("Relance des devis envoyés", "Devis sans réponse", "Des ventes perdues", "Relance polie J+7"),
                    ("Facturation + relance impayés", "Chantiers, contrats", "Trésorerie tendue", "Facture générée + relance en 3 paliers"),
                    ("Les avis Google", "La réputation locale", "Des clients silencieux", "Demande d'avis après le chantier"),
                    ("Rappels d'entretien saisonniers", "Taille, traitement, arrosage", "Des oublis", "Rappel au bon moment + créneau proposé"),
                ])),
            section("Votre crainte, honnêtement", "« Le client veut voir le paysagiste sur le terrain. »",
                prose("<p>Et il le verra : <strong>le travail de terrain reste 100 % humain</strong>. L'automatisation s'occupe des devis, plannings, relances et contrats : le client voit un pro organisé, et vous voyez vos contrats d'entretien se renouveler seuls.</p>")),
        ],
        faq=[
            ("Les contrats d'entretien, ça marche vraiment ?", "Oui : c'est le levier n°1 des paysagistes : un rappel automatique avant la fin du contrat et le renouvellement se fait tout seul."),
            ("Ça marche avec mon logiciel ?", "Oui : on se branche sur vos outils (planning, devis, facturation). Rien ne change pour vos équipes."),
            ("Par quoi commencer ?", "La relance des contrats d'entretien : c'est le poste qui transforme vos chantiers en revenus récurrents."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-artisan.html", "Artisans"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-location-saisonniere.html",
        title="Automatisation location saisonnière : réservations directes, avis, arrivées : sans Airbnb (ou presque)",
        meta="Réservations directes, messages automatiques, avis, gestion des arrivées : comment un propriétaire loue mieux. Exemples concrets.",
        h1="Location saisonnière : <em>des réservations directes, des avis qui défilent.</em>",
        sub="Chaque réservation via plateforme coûte 10-15 %. Les locations directes se construisent avec des avis et des messages impeccables. Voici comment.",
        sections=[
            section("Le quotidien du loueur", "Les frustrations qui grignotent la rentabilité",
                pains([
                    ("Les commissions Airbnb/Booking", "10-15 % par réservation", "La marge fond", "Réservations directes encouragées par l'automatisation"),
                    ("Les messages répétitifs", "« L'adresse ? », « Comment ça marche ? »", "Des heures de copier-coller", "Messages automatiques à chaque étape"),
                    ("Les avis", "La note fait tout", "Des séjours sans avis", "Demande d'avis au départ"),
                ])),
            section("Les 8 tâches à automatiser", "De la demande au merci final",
                pains([
                    ("Réservations directes + confirmation", "Le client réserve sur votre site", "Des commissions perdues", "Confirmation auto + règlement en ligne"),
                    ("Messages d'avant-arrivée", "Adresse, arrivée autonome, règles", "Des messages répétitifs", "Message automatique J-7 et J-1"),
                    ("Arrivée autonome", "Boîte à clés, code", "Des rendez-vous pour les clés", "Instructions + code envoyés automatiquement"),
                    ("Demande d'avis au départ", "Le séjour était réussi", "Des avis jamais écrits", "SMS/email post-départ → avis"),
                    ("Relance des paiements", "Soldes, caution", "De l'argent en attente", "Relance polie et automatique"),
                    ("Le standard / questions fréquentes", "Équipements, animaux, arrivée", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Devis séjours longs / groupes", "Mois, familles, entreprises", "Des réponses lentes", "Devis chiffré en 30 secondes"),
                    ("La gestion des calendriers", "Plusieurs plateformes", "Des doubles réservations", "Synchronisation + fermeture auto des canaux"),
                ])),
            section("Votre crainte, honnêtement", "« Sans Airbnb, je n'ai pas de clients. »",
                prose("<p>Et gardez Airbnb ! L'objectif n'est pas de le supprimer mais de <strong>réduire la part des commissions</strong> : les avis que vous collectez automatiquement alimentent votre site direct, et vos réservations directes reviennent plus cher à la maison. 20-30 % de direct, c'est déjà une marge énorme.</p>")),
        ],
        faq=[
            ("Ça marche avec mes annonces actuelles ?", "Oui : on se branche sur vos calendriers et vos outils. Les messages automatiques complètent ce que vous faites déjà."),
            ("Les messages automatiques ne sont pas trop froids ?", "Ils sont personnalisés avec votre ton et le nom du voyageur. La plupart des loueurs qui automatisent voient leurs notes grimper."),
            ("Par quoi commencer ?", "La demande d'avis : chaque avis en plus améliore votre classement et vos réservations directes."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-hotellerie.html", "Hôtel / gîte"), ("repondre-avis-google.html", "Avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-evenementiel.html",
        title="Automatisation événementiel : devis, planning, rappels : l'organisateur sans papier",
        meta="Devis événementiel en 30 secondes, planning des prestataires, rappels aux invités : comment un organisateur automatise. Exemples concrets.",
        h1="Événementiel : <em>l'organisation sans les tableaux qui explosent.</em>",
        sub="Prestataires, invités, plannings, devis : un événement génère des centaines de micro-tâches. Voici comment l'automatisation les absorbe.",
        sections=[
            section("Le quotidien de l'organisateur", "Les frustrations qui font craquer",
                pains([
                    ("Les devis multiples", "Chaque événement = un devis détaillé", "Des soirées de paperasse", "Devis chiffré en 30 secondes avec votre grille"),
                    ("La coordination des prestataires", "Traiteur, DJ, photographe", "Des allers-retours", "Planning centralisé + rappels automatiques"),
                    ("Les rappels aux invités", "Confirmations, relances", "Des tables incomplètes", "Rappels automatiques + relances"),
                ])),
            section("Les 8 tâches à automatiser", "De la demande au merci final",
                pains([
                    ("Devis express", "Mariages, séminaires, soirées", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("Prise de RDV découverte", "Allers-retours pour caler", "Des clients perdus", "Créneaux proposés + confirmation automatique"),
                    ("Rappels aux prestataires", "Arrivées, installation", "Des oublis", "Rappel automatique J-7 et J-1"),
                    ("Confirmations invités", "Réponses, régimes, transport", "Des tableaux à refaire", "Questionnaire + relances automatiques"),
                    ("Relance des acomptes", "Acomptes, soldes", "De l'argent en attente", "Relance polie et automatique"),
                    ("Le standard / questions fréquentes", "Lieu, tenue, stationnement", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation des pro", "Des clients satisfaits silencieux", "Demande d'avis après l'événement"),
                    ("Comptes-rendus de réunion client", "Notes, décisions, budgets", "Des heures de rédaction", "CR structuré généré puis validé"),
                ])),
            section("Votre crainte, honnêtement", "« Un événement, ça se vit, ça ne se robotise pas. »",
                prose("<p>Et c'est vrai : <strong>le jour J, l'émotion et l'adaptation restent humaines</strong>. L'automatisation s'occupe des 3 semaines avant : devis, rappels, confirmations, acomptes, pour que le jour J, vous soyez sur place, pas derrière un tableur.</p>")),
        ],
        faq=[
            ("Ça gère les événements sur mesure ?", "Les devis suivent votre grille et vous validez avant envoi. Les rappels et confirmations sont personnalisés par événement."),
            ("Ça marche avec mes outils ?", "Oui : on se branche sur vos tableurs, plannings et outils existants. Rien ne change pour votre façon de travailler."),
            ("Par quoi commencer ?", "Les rappels aux prestataires : c'est le poste qui évite les oublis et les tensions le jour J."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatiser-devis.html", "Automatiser les devis"), ("compte-rendu-reunion.html", "Comptes-rendus"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-vtc.html",
        title="Automatisation VTC / taxi : facturation, tournées, rappels clients : la route sans paperasse",
        meta="Facturation VTC automatique, rappels clients, gestion des tournées : comment un VTC gagne des heures. Exemples concrets.",
        h1="VTC / taxi : <em>la route, sans la paperasse après.</em>",
        sub="Chaque course = une facture, chaque client = un rappel, chaque semaine = un pointage. Voici comment l'automatisation rend la route rentable.",
        sections=[
            section("Le quotidien du VTC", "Les frustrations qui mangent les marges",
                pains([
                    ("La facturation à la main", "Chaque course = une facture", "Des heures de saisie", "Facture générée automatiquement après la course"),
                    ("Le rapprochement des plateformes", "Uber, Bolt, direct", "Des écarts", "Rapprochement automatique des gains"),
                    ("Les clients réguliers", "Aéroports, rendez-vous", "Des clients oubliés", "Rappel automatique des réservations"),
                ])),
            section("Les 8 tâches à automatiser", "De la réservation au rappel",
                pains([
                    ("Confirmation de course", "Réservations directes", "Des doublons", "Confirmation automatique + détails"),
                    ("Rappel de réservation", "Aéroport, RDV médical", "Des no-show", "Rappel J-1 + confirmation"),
                    ("Facturation auto", "Course terminée", "Des heures de saisie", "Facture générée + envoyée automatiquement"),
                    ("Rapprochement des gains", "Plateformes + direct", "Des écarts", "Rapprochement automatique par course"),
                    ("Relance des impayés", "Courses en compte", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après la course"),
                    ("Rappels clients réguliers", "Médecins, entreprises", "Des clients oubliés", "Message « besoin d'une course ? » personnalisé"),
                    ("Le standard / questions", "Tarifs, disponibilité, trajets", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                ])),
            section("Votre crainte, honnêtement", "« Je conduis, je n'ai pas le temps de gérer des robots. »",
                prose("<p>Justement : l'automatisation travaille <strong>pendant que vous conduisez</strong>. La facture se génère seule, le rappel se confirme seul, le rapprochement se fait seul. Vous, vous regardez la route.</p>")),
        ],
        faq=[
            ("Ça marche avec Uber/Bolt ?", "Oui : on se branche sur vos relevés et vos outils. Le rapprochement vérifie chaque course."),
            ("La facturation automatique est légale ?", "Oui : elle suit vos tarifs et vos mentions obligatoires. Vous validez avant envoi."),
            ("Par quoi commencer ?", "Le rappel de réservation : il réduit les no-show et sécurise votre journée."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-transport.html", "Transport / livraison"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-architecte.html",
        title="Automatisation architecte : devis, suivi de projets, dossiers : l'agence qui livre",
        meta="Devis d'architecte, suivi de chantiers, dossiers administratifs, comptes-rendus : comment une agence gagne des heures. Exemples concrets.",
        h1="Architecte : <em>plus de temps à concevoir, moins de paperasse.</em>",
        sub="Dossiers de permis, comptes-rendus de chantier, suivi de facturation : l'administratif mange le temps de conception. Voici ce qu'on automatise.",
        sections=[
            section("Le quotidien de l'agence", "Les frustrations qui rongent les honoraires",
                pains([
                    ("Les dossiers administratifs", "Permis, consultations, appels d'offres", "Des semaines de paperasse", "Documents générés à partir des données du projet"),
                    ("Le suivi de chantier", "CR, ordres de service, modifications", "Des heures de rédaction", "CR structuré généré depuis les notes"),
                    ("Les relances d'honoraires", "Échéanciers de paiement", "Trésorerie tendue", "Relance polie et automatique en 3 paliers"),
                ])),
            section("Les 8 tâches à automatiser", "De la consultation au chantier livré",
                pains([
                    ("Devis / honoraires", "Demandes de consultation", "Des réponses lentes", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Prise de RDV visite", "Clients, terrains, chantiers", "Des allers-retours", "Créneaux proposés + confirmation automatique"),
                    ("Comptes-rendus de chantier", "Notes de visite, réunions", "Des heures de rédaction", "CR structuré généré puis validé"),
                    ("Dossiers administratifs", "Permis, consultations", "Des formulaires répétitifs", "Documents générés à partir des données"),
                    ("Suivi de facturation", "Échéanciers d'honoraires", "Des retards", "Facture générée + relance en 3 paliers"),
                    ("Relance des devis envoyés", "Consultations sans réponse", "Des projets perdus", "Relance polie J+7"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après la livraison"),
                    ("Le standard / questions", "Honoraires, délais, démarches", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                ])),
            section("Votre crainte, honnêtement", "« Un projet d'architecture, ça se pense, ça ne se robotise pas. »",
                prose("<p>Et c'est exactement le principe : <strong>la conception et la direction d'œuvre restent 100 % humaines</strong>. L'automatisation s'occupe des devis, CR, dossiers et relances : l'agence livre plus vite, encaisse plus vite, et vous concevez.</p>")),
        ],
        faq=[
            ("Ça gère les projets sur mesure ?", "Les devis suivent votre grille et vous validez avant envoi. Les CR et dossiers sont générés puis validés par vous."),
            ("Ça marche avec mon logiciel métier ?", "Oui : on se branche sur vos outils (DAOAO, planning, facturation). Rien ne change pour votre équipe."),
            ("Par quoi commencer ?", "Les comptes-rendus de chantier : c'est le poste le plus chronophage et le plus structuré."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("compte-rendu-reunion.html", "Comptes-rendus"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-services-b2b.html",
        title="Automatisation cabinets conseil & agences : devis, reporting, suivi clients : le B2B sans friction",
        meta="Devis conseil, rapports d'activité, suivi clients, relances : comment un cabinet conseil ou une agence automatise son back-office. Exemples concrets.",
        h1="Cabinets & agences : <em>le back-office qui suit la croissance.</em>",
        sub="Chaque client = un devis, un suivi, un rapport, une facture. Le conseil facture son temps : sauf que le temps part en administration. Voici ce qu'on automatise.",
        sections=[
            section("Le quotidien du cabinet", "Les frustrations qui grignotent le chiffrable",
                pains([
                    ("Le temps non facturable", "Devis, suivis, rapports, relances", "Des heures perdues", "L'administratif réduit de 50-70 %"),
                    ("Le suivi client", "Où en est chaque mission ?", "Des tableaux à refaire", "Suivi automatique + alertes"),
                    ("Les relances", "Devis, factures, retards", "De l'argent en attente", "Relance polie et automatique en 3 paliers"),
                ])),
            section("Les 8 tâches à automatiser", "De la prospection au rapport final",
                pains([
                    ("Devis / propositions", "Nouvelles missions", "Des réponses lentes", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Comptes-rendus de réunion", "Notes de brief, comités", "Des heures de rédaction", "CR structuré généré puis validé"),
                    ("Rapports d'activité clients", "Mensuels, trimestriels", "Des nuits de mise en forme", "Rapport chiffré généré automatiquement"),
                    ("Suivi des missions", "Avancement, jalons", "Des tableaux à refaire", "Suivi automatique + alertes de jalons"),
                    ("Relance des devis et factures", "Propositions sans réponse", "Des ventes perdues", "Relance polie J+7 + 3 paliers"),
                    ("Tri des emails", "Factures fournisseurs, clients", "Des heures de tri", "Tri automatique + extraction des factures"),
                    ("Le reporting interne", "Activité, chiffre d'affaires", "Des tableaux de bord à la main", "Reporting automatique avec anomalies"),
                    ("Le standard / questions", "Disponibilités, références", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                ])),
            section("Votre crainte, honnêtement", "« Le conseil se vend sur la relation, pas sur des robots. »",
                prose("<p>Et c'est vrai : <strong>la relation et le conseil restent 100 % humains</strong>. L'automatisation s'occupe de ce qui ne crée pas de valeur : le devis, le CR, la relance, le tri, pour que vos heures facturables augmentent. C'est le modèle du cabinet moderne.</p>")),
        ],
        faq=[
            ("Ça marche avec mon CRM/outils ?", "Oui : on se branche sur vos outils existants (CRM, facturation, email). L'automatisation complète ce que vous utilisez déjà."),
            ("Le reporting automatique est-il fiable ?", "Il utilise vos chiffres réels et signale les anomalies. Vous validez avant envoi au client."),
            ("Par quoi commencer ?", "Les relances de devis et factures : c'est le poste qui augmente immédiatement votre chiffre d'affaires."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("experts-comptables.html", "Experts-comptables"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-organisme-formation.html",
        title="Automatisation organisme de formation : inscriptions, convocations, bilans : le centre qui remplit",
        meta="Inscriptions, convocations, émargements, bilans pédagogiques : comment un organisme de formation automatise son administratif. Exemples concrets.",
        h1="Organisme de formation : <em>l'administratif qui suit les stagiaires.</em>",
        sub="Inscriptions, convocations, émargements, bilans, factures : chaque session génère sa pile de papier. Voici comment l'automatisation la fait disparaître.",
        sections=[
            section("Le quotidien du centre", "Les frustrations qui bloquent les sessions",
                pains([
                    ("Les inscriptions à la main", "Formulaires, pièces, confirmations", "Des erreurs", "Inscription simplifiée + confirmation automatique"),
                    ("Les convocations", "Dates, lieux, programmes", "Des oublis", "Convocation envoyée automatiquement J-7 et J-1"),
                    ("Les bilans pédagogiques", "Présence, évaluations, rapport", "Des nuits de rédaction", "Bilan structuré généré depuis les données"),
                ])),
            section("Les 8 tâches à automatiser", "De l'inscription à la facture",
                pains([
                    ("Inscription + confirmation", "Formulaires, pièces", "Des erreurs", "Inscription simplifiée + confirmation automatique"),
                    ("Convocations et rappels", "Dates, lieux, programme", "Des oublis", "Convocation J-7 + rappel J-1"),
                    ("Émargements", "Feuilles de présence", "Des erreurs de saisie", "Génération + suivi automatique des émargements"),
                    ("Bilans pédagogiques", "Présence, évaluations", "Des nuits de rédaction", "Bilan structuré généré puis validé"),
                    ("Relance des devis", "Devis clients/entreprises", "Des ventes perdues", "Relance polie J+7"),
                    ("Facturation + relances", "Sessions, conventions", "Trésorerie tendue", "Facture générée + relance en 3 paliers"),
                    ("Le standard / questions", "Financements, CPF, dates", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("La gestion des stocks (livrets)", "Supports, livrets pédagogiques", "Des ruptures", "Alerte de seuil + commande suggérée"),
                ])),
            section("Votre crainte, honnêtement", "« La formation, c'est du contact humain. »",
                prose("<p>Et le contact reste 100 % humain : <strong>le formateur anime, l'équipe accueille</strong>. L'automatisation s'occupe des inscriptions, convocations, émargements et bilans : le stagiaire voit un organisme organisé, Qualiopi le vérifie, vous gardez vos soirées.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de formation ?", "Oui : on se branche sur vos outils (planning, inscriptions, facturation). Rien ne change pour votre équipe."),
            ("Les bilans automatiques sont-ils acceptés ?", "Ils suivent le référentiel de votre organisme et sont validés par vous avant transmission."),
            ("Par quoi commencer ?", "Les convocations et rappels : ils réduisent les no-show et les sessions sous-remplies."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-tresorerie.html",
        title="Automatisation trésorerie : prévisionnel, rapprochement, alertes : la PME qui dort tranquille",
        meta="Prévisionnel de trésorerie, rapprochement bancaire, alertes de seuil, relances : comment une PME reprend le contrôle de sa trésorerie. Exemples concrets.",
        h1="Trésorerie : <em>savoir où vous en êtes, chaque matin.</em>",
        sub="Un découvert qui arrive par surprise, un client qui paie en retard, une facture oubliée : la trésorerie est le nerf de la guerre. Voici comment l'automatisation la sécurise.",
        sections=[
            section("Le quotidien du dirigeant", "Les frustrations qui font mal dormir",
                pains([
                    ("La trésorerie en aveugle", "Des chiffres de la semaine dernière", "Des découvertes surprises", "Situation de trésorerie à jour chaque matin"),
                    ("Le rapprochement bancaire", "Des centaines d'opérations", "Des heures de pointage", "Rapprochement automatique des opérations"),
                    ("Les impayés", "Des clients qui paient en retard", "De l'argent en attente", "Relance polie et automatique en 3 paliers"),
                ])),
            section("Les 8 tâches à automatiser", "Du relevé bancaire au prévisionnel",
                pains([
                    ("Rapprochement bancaire", "Relevés, factures, virements", "Des heures de pointage", "Rapprochement automatique + écarts signalés"),
                    ("Prévisionnel de trésorerie", "Entrées, sorties, échéances", "Des découvertes surprises", "Prévisionnel glissant mis à jour automatiquement"),
                    ("Alertes de seuil", "Découvert, délais fournisseurs", "Des surprises", "Alerte automatique avant le seuil critique"),
                    ("Relance des impayés", "Factures en retard", "De l'argent en attente", "Relance polie en 3 paliers"),
                    ("Suivi des délais clients/fournisseurs", "Qui paie en retard ?", "Des écarts invisibles", "Tableau de bord des délais automatique"),
                    ("Tri des emails bancaires", "Relevés, alertes, factures", "Des heures de tri", "Tri automatique + extraction"),
                    ("Le reporting financier", "CA, marges, trésorerie", "Des nuits de tableaux", "Rapport chiffré généré avec anomalies"),
                    ("Les échéances fiscales", "TVA, charges, cotisations", "Des pénalités", "Rappels automatiques avant chaque échéance"),
                ])),
            section("Votre crainte, honnêtement", "« La trésorerie, c'est trop sensible pour la confier à une machine. »",
                prose("<p>Et c'est la bonne prudence : <strong>les décisions restent entre vos mains</strong>. L'automatisation lit vos chiffres réels, signale les écarts et les impayés, et vous validez tout. Elle ne décide rien : elle éclaire. Ex-contrôleur de gestion, c'est exactement comme ça que je l'ai appris.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel comptable ?", "Oui : on se branche sur vos exports (banque, compta, facturation). Les chiffres restent les vôtres."),
            ("Le prévisionnel est-il fiable ?", "Il est glissant et basé sur vos données réelles (factures, échéances, délais passés). Il s'améliore chaque mois."),
            ("Par quoi commencer ?", "Le rapprochement bancaire : c'est le poste le plus chronophage et le premier qui protège votre trésorerie."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("experts-comptables.html", "Experts-comptables"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-syndic.html",
        title="Automatisation syndic de copropriété : appels de fonds, relances, comptes-rendus : l'immeuble serein",
        meta="Appels de fonds, relances des copropriétaires, comptes-rendus d'assemblée, suivi des travaux : comment un syndic automatise. Exemples concrets.",
        h1="Syndic : <em>des copropriétaires informés, des charges encaissées.</em>",
        sub="Assemblées, appels de fonds, relances, travaux : chaque immeuble génère sa paperasse. Voici comment l'automatisation libère votre équipe.",
        sections=[
            section("Le quotidien du syndic", "Les frustrations qui s'accumulent par immeuble",
                pains([
                    ("Les appels de fonds", "Des dizaines par immeuble", "Des erreurs et des oublis", "Appel généré + envoyé automatiquement"),
                    ("Les impayés de charges", "Des copropriétaires en retard", "Trésorerie tendue", "Relance polie et automatique en 3 paliers"),
                    ("Les comptes-rendus d'assemblée", "Des heures de rédaction", "Des nuits perdues", "CR structuré généré puis validé"),
                ])),
            section("Les 8 tâches à automatiser", "De l'appel de fonds aux travaux",
                pains([
                    ("Appels de fonds", "Échéanciers par immeuble", "Des erreurs", "Appel généré + envoyé automatiquement"),
                    ("Relance des charges impayées", "Échéances dépassées", "De l'argent en attente", "Relance en 3 paliers"),
                    ("Comptes-rendus d'assemblée", "Décisions, votes, questions", "Des heures de rédaction", "CR structuré généré puis validé"),
                    ("Convocations d'assemblée", "Dates, ordre du jour", "Des oublis", "Convocation envoyée automatiquement"),
                    ("Suivi des travaux", "Devis, planning, attestations", "Des allers-retours", "Suivi automatique + alertes d'échéance"),
                    ("Le standard / questions", "Charges, travaux, documents", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation locale", "Des clients silencieux", "Demande d'avis après la mission"),
                    ("La gestion des contrats", "Ascenseurs, chaufferie, entretien", "Des renouvellements oubliés", "Rappel automatique des échéances de contrats"),
                ])),
            section("Votre crainte, honnêtement", "« Les copropriétaires veulent un humain responsable. »",
                prose("<p>Et ils l'ont : <strong>le syndic reste responsable et humain</strong>. L'automatisation s'occupe des envois, relances, CR et convocations : les copropriétaires voient un syndic réactif qui ne laisse rien passer. C'est exactement la réputation que vous voulez.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de syndic ?", "Oui : on se branche sur vos outils (gestion, comptabilité, planning). Rien ne change pour votre équipe."),
            ("Les relances de charges sont-elles légales ?", "Oui : elles suivent vos échéanciers et les dispositions de la copropriété, avec le ton adapté à chaque palier."),
            ("Par quoi commencer ?", "Les relances des charges impayées : c'est le poste qui protège directement la trésorerie de vos immeubles."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("relance-impayes.html", "Relance impayés"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-conciergerie.html",
        title="Automatisation conciergerie : réservations, messages, avis : l'hôte qui répond toujours",
        meta="Réservations, messages d'avant-arrivée, avis, gestion des clés : comment une conciergerie automatise ses locations. Exemples concrets.",
        h1="Conciergerie : <em>votre portefeuille qui tourne sans vous épuiser.</em>",
        sub="Chaque logement = des réservations, des messages, des avis. La conciergerie vit de la réactivité. Voici comment l'automatisation la rend possible à l'échelle.",
        sections=[
            section("Le quotidien de la conciergerie", "Les frustrations qui plafonnent la croissance",
                pains([
                    ("Les messages répétitifs", "Adresse, arrivée, wifi, départ", "Des heures de copier-coller", "Messages automatiques à chaque étape"),
                    ("Les avis", "La note fait tout", "Des séjours sans avis", "Demande d'avis au départ"),
                    ("Les réservations multiples", "Plusieurs plateformes", "Des doubles réservations", "Synchronisation + gestion centralisée"),
                ])),
            section("Les 8 tâches à automatiser", "De la réservation au départ",
                pains([
                    ("Confirmation + paiement", "Réservations directes", "Des retards", "Confirmation auto + règlement en ligne"),
                    ("Messages d'avant-arrivée", "Adresse, code, règles", "Des messages répétitifs", "Message automatique J-7 et J-1"),
                    ("Arrivée autonome", "Boîte à clés, code", "Des rendez-vous pour les clés", "Instructions + code envoyés automatiquement"),
                    ("Demande d'avis au départ", "Le séjour était réussi", "Des avis jamais écrits", "SMS/email post-départ → avis"),
                    ("Relance des paiements", "Soldes, caution", "De l'argent en attente", "Relance polie et automatique"),
                    ("Le standard / questions", "Équipements, animaux, arrivée", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Devis séjours longs / groupes", "Mois, familles, entreprises", "Des réponses lentes", "Devis chiffré en 30 secondes"),
                    ("La gestion des calendriers", "Plusieurs plateformes", "Des doubles réservations", "Synchronisation + fermeture auto"),
                ])),
            section("Votre crainte, honnêtement", "« Mes propriétaires veulent un vrai contact avec l'hôte. »",
                prose("<p>Et ils l'ont : <strong>l'accueil et le service restent humains</strong>. L'automatisation s'occupe des messages standards, des rappels et des avis : les propriétaires voient des notes qui grimpent et des charges de travail qui baissent. C'est votre argument de croissance.</p>")),
        ],
        faq=[
            ("Ça marche avec mes plateformes actuelles ?", "Oui : on se branche sur vos calendriers et vos outils. Les messages automatiques complètent ce que vous faites déjà."),
            ("Les messages ne sont pas trop froids ?", "Ils sont personnalisés avec votre ton et le nom du voyageur. Les notes de vos logements ont tendance à grimper."),
            ("Par quoi commencer ?", "La demande d'avis : chaque avis en plus améliore votre classement et vos réservations."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-location-saisonniere.html", "Loc. saisonnière"), ("repondre-avis-google.html", "Avis Google"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-creche.html",
        title="Automatisation crèche & micro-crèche : inscriptions, présences, facturation : le quotidien allégé",
        meta="Inscriptions, présences, facturations, communications aux parents : comment une crèche automatise son administratif. Exemples concrets.",
        h1="Crèche : <em>moins de paperasse, plus de temps pour les enfants.</em>",
        sub="Inscriptions, présences, factures, messages aux parents : l'administratif d'une crèche est infini. Voici comment l'automatisation le réduit drastiquement.",
        sections=[
            section("Le quotidien de la structure", "Les frustrations qui volent du temps éducatif",
                pains([
                    ("Les inscriptions", "Dossiers, contrats, pièces", "Des soirées de saisie", "Inscription simplifiée + confirmation automatique"),
                    ("Les présences", "Pointage, repas, siestes", "Des erreurs", "Saisie simplifiée + transmission aux parents"),
                    ("La facturation", "Heures réelles, repas, suppléments", "Des erreurs de calcul", "Facture générée depuis les présences réelles"),
                ])),
            section("Les 8 tâches à automatiser", "De l'inscription au message aux parents",
                pains([
                    ("Inscription + confirmation", "Dossiers, contrats", "Des soirées de saisie", "Inscription simplifiée + confirmation automatique"),
                    ("Liste d'attente", "Demandes d'inscription", "Des places perdues", "Le prochain parent prévenu automatiquement"),
                    ("Présences et transmissions", "Pointage, repas, siestes", "Des erreurs", "Saisie simplifiée + transmission aux parents"),
                    ("Facturation des présences", "Heures réelles, repas", "Des erreurs de calcul", "Facture générée depuis les présences"),
                    ("Relance des impayés", "Factures en retard", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("Messages aux parents", "Infos, fermetures, événements", "Des envois oubliés", "Message automatique aux groupes concernés"),
                    ("Le standard / questions", "Horaires, places, tarifs", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation locale", "Des parents satisfaits silencieux", "Demande d'avis après l'inscription"),
                ])),
            section("Votre crainte, honnêtement", "« La crèche, c'est de l'humain, pas des robots. »",
                prose("<p>Et c'est exactement le principe : <strong>tout le temps éducatif reste humain</strong>. L'automatisation s'occupe des inscriptions, présences, factures et messages : votre équipe retrouve des heures pour les enfants. C'est ce que les parents voient et ressentent.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de crèche ?", "Oui : on se branche sur vos outils (inscriptions, présences, facturation). Rien ne change pour votre équipe."),
            ("La facturation automatique est fiable ?", "Elle se base sur les présences réelles et vos tarifs. Vous validez avant envoi."),
            ("Par quoi commencer ?", "La facturation des présences : c'est le poste le plus chronophage et celui qui génère le plus d'erreurs."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-organisme-formation.html", "Organisme de formation"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-ecole.html",
        title="Automatisation école privée : inscriptions, convocations, paiements : l'établissement organisé",
        meta="Inscriptions, convocations aux réunions, paiements des frais, communication aux parents : comment une école automatise. Exemples concrets.",
        h1="École privée : <em>l'administratif qui suit la rentrée.</em>",
        sub="Inscriptions, réunions, factures, communications : chaque famille génère sa paperasse. Voici comment l'automatisation allège l'équipe administrative.",
        sections=[
            section("Le quotidien de l'établissement", "Les frustrations qui saturent l'administration",
                pains([
                    ("Les inscriptions", "Dossiers, entretiens, contrats", "Des semaines de saisie", "Inscription simplifiée + suivi automatique"),
                    ("Les réunions parents", "Convocations, présences", "Des oublis", "Convocation + rappel automatiques"),
                    ("Les frais de scolarité", "Échéanciers, retards", "Trésorerie tendue", "Facture générée + relance en 3 paliers"),
                ])),
            section("Les 8 tâches à automatiser", "De l'inscription à la communication",
                pains([
                    ("Inscription + dossier", "Pièces, contrats, entretiens", "Des semaines de saisie", "Inscription simplifiée + suivi automatique"),
                    ("Liste d'attente", "Demandes d'inscription", "Des places perdues", "Le prochain parent prévenu automatiquement"),
                    ("Convocations réunions", "Dates, ordre du jour", "Des oublis", "Convocation + rappel automatiques"),
                    ("Paiements des frais", "Échéanciers, bourses", "Des retards", "Facture générée + relance en 3 paliers"),
                    ("Communication parents", "Infos, événements, urgences", "Des envois oubliés", "Message automatique aux groupes concernés"),
                    ("Le standard / questions", "Inscriptions, tarifs, rythmes", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation locale", "Des familles satisfaites silencieuses", "Demande d'avis après l'inscription"),
                    ("La gestion des stocks (fournitures)", "Supports, fournitures", "Des ruptures", "Alerte de seuil + commande suggérée"),
                ])),
            section("Votre crainte, honnêtement", "« L'école, c'est une affaire de pédagogie et de relations. »",
                prose("<p>Et elle le reste : <strong>la pédagogie et les relations restent 100 % humaines</strong>. L'automatisation s'occupe des inscriptions, convocations, paiements et messages : les familles voient un établissement organisé et réactif. C'est votre meilleure publicité.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel d'école ?", "Oui : on se branche sur vos outils (vie scolaire, facturation, communication). Rien ne change pour votre équipe."),
            ("Les relances de frais sont-elles adaptées ?", "Oui : ton poli et progressif en 3 paliers, avec les mentions de votre règlement intérieur."),
            ("Par quoi commencer ?", "Les convocations et rappels de réunions : c'est le poste qui fait gagner le plus de temps immédiatement."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-organisme-formation.html", "Organisme de formation"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-gestion-locative.html",
        title="Automatisation gestion locative : quittances, relances, état des lieux : le patrimoine serein",
        meta="Quittances, relances de loyers, états des lieux, suivi des travaux : comment un gestionnaire locatif automatise. Exemples concrets.",
        h1="Gestion locative : <em>des loyers encaissés, des locataires informés.</em>",
        sub="Quittances, loyers, états des lieux, travaux : chaque bien génère sa paperasse. Voici comment l'automatisation libère le gestionnaire.",
        sections=[
            section("Le quotidien du gestionnaire", "Les frustrations qui s'accumulent par bien",
                pains([
                    ("Les quittances", "Des dizaines par mois", "Des heures de saisie", "Quittance générée + envoyée automatiquement"),
                    ("Les loyers impayés", "Des locataires en retard", "De l'argent en attente", "Relance polie et automatique en 3 paliers"),
                    ("Les états des lieux", "Entrées, sorties, litiges", "Des erreurs", "Checklist générée + suivi des écarts"),
                ])),
            section("Les 8 tâches à automatiser", "De la quittance au renouvellement",
                pains([
                    ("Quittances de loyer", "Échéances mensuelles", "Des heures de saisie", "Quittance générée + envoyée automatiquement"),
                    ("Relance des loyers impayés", "Échéances dépassées", "De l'argent en attente", "Relance en 3 paliers"),
                    ("États des lieux", "Entrées, sorties", "Des litiges", "Checklist générée + suivi des écarts"),
                    ("Rappels de renouvellement", "Baux, préavis", "Des baux oubliés", "Rappel automatique avant l'échéance"),
                    ("Suivi des travaux", "Devis, planning, attestations", "Des allers-retours", "Suivi automatique + alertes"),
                    ("Le standard / questions", "Loyers, travaux, documents", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation locale", "Des clients silencieux", "Demande d'avis après la mission"),
                    ("Le reporting propriétaires", "Comptes-rendus mensuels", "Des nuits de tableaux", "Rapport généré automatiquement"),
                ])),
            section("Votre crainte, honnêtement", "« Les propriétaires veulent un gestionnaire humain. »",
                prose("<p>Et ils l'ont : <strong>le gestionnaire reste responsable et humain</strong>. L'automatisation s'occupe des quittances, relances, états des lieux et rapports : les propriétaires voient un patrimoine suivi, des loyers encaissés, et vous gardez vos soirées.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de gestion ?", "Oui : on se branche sur vos outils (gestion, comptabilité, mandats). Rien ne change pour votre équipe."),
            ("Les quittances automatiques sont légales ?", "Oui : elles suivent votre échéancier et vos mentions obligatoires. Vous validez avant envoi."),
            ("Par quoi commencer ?", "Les quittances : c'est le poste le plus répétitif et celui qui libère le plus de temps chaque mois."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("ia-pour-immobilier.html", "Immobilier"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-spa.html",
        title="Automatisation spa & institut : réservations, rappels, fidélité : le bien-être rentable",
        meta="Réservations, rappels de RDV, cartes de fidélité, avis : comment un spa ou institut remplit son planning. Exemples concrets.",
        h1="Spa & institut : <em>des créneaux remplis, des clientes fidèles.</em>",
        sub="Chaque créneau vide est une perte sèche. Les rappels, la fidélité et les avis font la différence. Voici comment l'automatisation les rend automatiques.",
        sections=[
            section("Le quotidien de l'institut", "Les frustrations qui vident le planning",
                pains([
                    ("Les créneaux vides", "Des annulations de dernière minute", "Des pertes sèches", "Rappel automatique + liste d'attente"),
                    ("Les clientes qui oublient", "RDV pris depuis des semaines", "Des no-show", "Rappel la veille + confirmation"),
                    ("Les avis", "La réputation locale", "Des clientes silencieuses", "Demande d'avis après la prestation"),
                ])),
            section("Les 8 tâches à automatiser", "De la réservation au retour",
                pains([
                    ("Prise de RDV + rappels", "Téléphone, messages", "Des créneaux perdus", "Créneaux proposés, confirmation, rappel J-1"),
                    ("Liste d'attente intelligente", "Une annulation", "Un créneau vide", "La prochaine cliente prévenue automatiquement"),
                    ("Carte de fidélité", "Prestations, points", "Des retours irréguliers", "Points et rappels automatiques"),
                    ("Demande d'avis après la prestation", "La cliente repart détendue", "Des avis jamais écrits", "SMS post-prestation → avis Google"),
                    ("Rappels de renouvellement", "Forfaits, abonnements", "Des revenus irréguliers", "Rappel + renouvellement automatique"),
                    ("Le standard / questions", "Horaires, tarifs, prestations", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("La gestion des stocks", "Huiles, produits, serviettes", "Des ruptures", "Alerte de seuil + commande suggérée"),
                    ("Devis forfaits / événements", "Mariages, enterrements de vie", "Des réponses lentes", "Devis chiffré en 30 secondes"),
                ])),
            section("Votre crainte, honnêtement", "« Le bien-être, c'est de la présence, pas des robots. »",
                prose("<p>Et c'est vrai : <strong>la prestation et l'accueil restent 100 % humains</strong>. L'automatisation s'occupe des rappels, créneaux, fidélité et avis : vos clientes voient un institut qui pense à elles, et votre planning se remplit.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de réservation ?", "Oui : on se branche sur vos outils (planning, caisse, carte de fidélité). Rien ne change pour votre équipe."),
            ("Les rappels ne dérangent pas ?", "Un rappel de RDV avec confirmation est un service : la cliente est rassurée, vous réduisez les no-show."),
            ("Par quoi commencer ?", "Les rappels de RDV : c'est le poste qui remplit immédiatement les créneaux vides."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-coiffure.html", "Coiffure / beauté"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="automatisation-avocat.html",
        title="Automatisation cabinet d'avocat : relances, CR, rendez-vous : le cabinet qui encaisse",
        meta="Relances clients, comptes-rendus, rendez-vous, suivi des dossiers : comment un cabinet d'avocats automatise son administratif. Exemples concrets.",
        h1="Avocat : <em>le temps de plaider, pas de relancer.</em>",
        sub="Chaque dossier = des relances, des CR, des rendez-vous, des factures. Le cabinet facture ses heures : sauf qu'elles partent en administration. Voici ce qu'on automatise.",
        sections=[
            section("Le quotidien du cabinet", "Les frustrations qui mangent les heures facturables",
                pains([
                    ("Les relances clients", "Pièces, honoraires, rendez-vous", "Des heures perdues", "Relance polie et automatique en 3 paliers"),
                    ("Les comptes-rendus", "Notes d'entretien, audiences", "Des nuits de rédaction", "CR structuré généré puis validé"),
                    ("Le suivi des dossiers", "Où en est chaque dossier ?", "Des tableaux à refaire", "Suivi automatique + alertes d'échéance"),
                ])),
            section("Les 8 tâches à automatiser", "Du rendez-vous au dossier clôturé",
                pains([
                    ("Prise de RDV + rappels", "Consultations, audiences", "Des no-show", "Créneaux proposés + rappel J-1"),
                    ("Relance des pièces clients", "Documents manquants", "Des dossiers bloqués", "Relance polie et automatique"),
                    ("Comptes-rendus d'entretien", "Notes de consultation", "Des heures de rédaction", "CR structuré généré puis validé"),
                    ("Relance des honoraires", "Factures, provisions", "Trésorerie tendue", "Relance en 3 paliers"),
                    ("Suivi des échéances", "Audiences, délais, recours", "Des oublis graves", "Alertes automatiques avant chaque échéance"),
                    ("Le standard / questions", "Honoraires, rendez-vous, dossiers", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après la clôture"),
                    ("Le tri des emails", "Clients, tribunaux, oppositions", "Des heures de tri", "Tri automatique + priorisation"),
                ])),
            section("Votre crainte, honnêtement", "« Le droit, c'est de la relation de confiance, pas des robots. »",
                prose("<p>Et c'est exactement le principe : <strong>le conseil et la défense restent 100 % humains</strong>. L'automatisation s'occupe des relances, CR, échéances et factures : le client voit un cabinet organisé qui ne laisse rien passer. C'est votre meilleure réputation.</p>")),
        ],
        faq=[
            ("Le secret professionnel est-il respecté ?", "Oui : les données restent dans vos outils, l'automatisation ne les sort jamais de votre système. Vous validez chaque envoi."),
            ("Ça marche avec mon logiciel métier ?", "Oui : on se branche sur vos outils (gestion de dossiers, facturation, agenda). Rien ne change pour votre équipe."),
            ("Par quoi commencer ?", "Les relances d'honoraires : c'est le poste qui augmente immédiatement votre trésorerie."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("professions-liberales.html", "Professions libérales"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-coach-sportif.html",
        title="Automatisation coach sportif : séances, rappels, abonnements : le coach qui remplit ses créneaux",
        meta="Rappels de séance, créneaux, abonnements, avis : comment un coach sportif remplit son planning et fidélise. Exemples concrets.",
        h1="Coach sportif : <em>des créneaux pleins, des clients réguliers.</em>",
        sub="Chaque séance annulée est une perte sèche. Les rappels, les abonnements et les avis font la différence. Voici comment l'automatisation les rend automatiques.",
        sections=[
            section("Le quotidien du coach", "Les frustrations qui vident le planning",
                pains([
                    ("Les séances annulées", "Des no-show de dernière minute", "Des pertes sèches", "Rappel automatique + liste d'attente"),
                    ("Les clients irréguliers", "Ils viennent, puis disparaissent", "Des revenus instables", "Rappels de reprise personnalisés"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après la séance"),
                ])),
            section("Les 8 tâches à automatiser", "De la première séance au client fidèle",
                pains([
                    ("Prise de RDV + rappels", "Séances, bilans", "Des no-show", "Créneaux proposés + rappel J-1"),
                    ("Liste d'attente intelligente", "Une annulation", "Un créneau vide", "Le prochain client prévenu automatiquement"),
                    ("Abonnements / packs", "Forfaits, cartes de séances", "Des revenus irréguliers", "Rappel + renouvellement automatique"),
                    ("Rappels de reprise", "Clients absents depuis 2 semaines", "Des clients perdus", "Message personnalisé de reprise"),
                    ("Demande d'avis après la séance", "Le client est motivé", "Des avis jamais écrits", "SMS post-séance → avis Google"),
                    ("Le standard / questions", "Horaires, tarifs, programmes", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Comptes-rendus de bilan", "Objectifs, progression", "Des heures de rédaction", "CR structuré généré puis validé"),
                    ("Relance des impayés", "Packs, séances", "Trésorerie tendue", "Relance polie en 3 paliers"),
                ])),
            section("Votre crainte, honnêtement", "« Le coaching, c'est de la motivation humaine. »",
                prose("<p>Et elle le reste : <strong>la séance et la motivation restent 100 % humaines</strong>. L'automatisation s'occupe des rappels, créneaux, abonnements et avis : vos clients voient un coach qui pense à eux, et votre planning se remplit.</p>")),
        ],
        faq=[
            ("Ça marche avec mon planning actuel ?", "Oui : on se branche sur vos outils (planning, caisse, réseaux). Rien ne change pour votre façon de coacher."),
            ("Les rappels de reprise ne sont pas intrusifs ?", "Un message bienveillant « on vous attend à la séance de mardi ? » est perçu comme de l'attention, pas du spam."),
            ("Par quoi commencer ?", "Les rappels de séance : ils réduisent les no-show et remplissent les créneaux dès la première semaine."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-salle-sport.html", "Salle de sport"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-bar.html",
        title="Automatisation bar et café : caisse, fournisseurs, événements : le comptoir rentable",
        meta="Rapprochement caisse, commandes fournisseurs, événements, avis : comment un bar automatise sa gestion. Exemples concrets.",
        h1="Bar : <em>la marge derrière le comptoir.</em>",
        sub="Fin de service, inventaire, fournisseurs, événements : chaque soirée génère sa paperasse. Voici comment l'automatisation la fait disparaître.",
        sections=[
            section("Le quotidien du bar", "Les frustrations qui rongent la marge",
                pains([
                    ("Le point de caisse", "CB, espèces, tickets", "Des heures de pointage", "Rapprochement automatique caisse/ventes"),
                    ("Les commandes fournisseurs", "Bières, softs, snacks", "Des ruptures", "Alerte de seuil + commande suggérée"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après la soirée"),
                ])),
            section("Les 8 tâches à automatiser", "De l'ouverture à la fermeture",
                pains([
                    ("Rapprochement de caisse", "CB, espèces, tickets", "Des heures de pointage", "Rapprochement automatique + écarts signalés"),
                    ("Commandes fournisseurs", "Bières, softs, snacks", "Des ruptures", "Alerte de seuil + commande suggérée"),
                    ("Inventaire", "Kegs, bouteilles, stocks", "Des écarts", "Inventaire simplifié + valorisation automatique"),
                    ("Événements / concerts", "Annonces, rappels", "Des soirées vides", "Annonce automatique + rappels aux habitués"),
                    ("Demande d'avis après la soirée", "Les clients sont contents", "Des avis jamais écrits", "SMS post-soirée → avis Google"),
                    ("Le standard / questions", "Horaires, événements, réservations", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Relance des impayés (pros)", "Événements, traiteurs", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("La gestion des stocks", "Boissons, consommables", "Des ruptures en plein service", "Alerte de seuil + commande suggérée"),
                ])),
            section("Votre crainte, honnêtement", "« Un bar, c'est du contact et de l'ambiance. »",
                prose("<p>Et c'est vrai : <strong>l'accueil et l'ambiance restent 100 % humains</strong>. L'automatisation s'occupe de la caisse, des stocks, des fournisseurs et des avis : le patron garde ses soirées pour ses clients, pas pour ses tableaux.</p>")),
        ],
        faq=[
            ("Ça marche avec ma caisse ?", "Oui : on se branche sur vos exports de caisse et vos outils. Le rapprochement vérifie chaque fin de service."),
            ("Les commandes automatiques sont-elles fiables ?", "Elles sont suggérées à partir de vos ventes réelles et vous validez avant envoi au fournisseur."),
            ("Par quoi commencer ?", "Le rapprochement de caisse : c'est le poste qui libère le plus de temps chaque soir."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-restauration.html", "Restaurant / traiteur"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-agence-voyage.html",
        title="Automatisation agence de voyage : devis, rappels, avis : le conseiller qui répond vite",
        meta="Devis voyage, rappels de départ, demandes d'avis, suivi clients : comment une agence de voyage automatise. Exemples concrets.",
        h1="Agence de voyage : <em>répondre vite, encaisser vite, faire rêver.</em>",
        sub="Chaque demande = un devis, chaque départ = des rappels, chaque retour = un avis. Voici comment l'automatisation rend l'agence réactive à l'échelle.",
        sections=[
            section("Le quotidien de l'agence", "Les frustrations qui font perdre des ventes",
                pains([
                    ("Les devis lents", "Des demandes multiples", "Des clients qui partent ailleurs", "Devis chiffré en 30 secondes avec votre grille"),
                    ("Les rappels de départ", "Documents, horaires", "Des oublis", "Rappel automatique J-7 et J-1 avec checklist"),
                    ("Les avis", "La réputation fait vendre", "Des clients satisfaits silencieux", "Demande d'avis après le retour"),
                ])),
            section("Les 8 tâches à automatiser", "De la demande au retour de vacances",
                pains([
                    ("Devis express", "Demandes téléphone/email/WhatsApp", "Des réponses lentes", "Devis chiffré en 30 secondes avec la grille"),
                    ("Prise de RDV conseil", "Allers-retours pour caler", "Des clients perdus", "Créneaux proposés + confirmation automatique"),
                    ("Rappels de départ", "Documents, horaires, bagages", "Des oublis", "Rappel J-7 et J-1 avec checklist"),
                    ("Relance des réservations", "Acomptes, soldes", "De l'argent en attente", "Relance polie et automatique"),
                    ("Demande d'avis après le retour", "Le client est conquis", "Des avis jamais écrits", "SMS post-retour → avis Google"),
                    ("Le standard / questions", "Destinations, visas, assurances", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Suivi des clients réguliers", "Anniversaires, envies", "Des clients oubliés", "Message personnalisé de reprise de contact"),
                    ("Comptes-rendus d'entretien conseil", "Envies, budgets, contraintes", "Des heures de rédaction", "CR structuré généré puis validé"),
                ])),
            section("Votre crainte, honnêtement", "« Le voyage se vend sur le rêve et la relation. »",
                prose("<p>Et c'est vrai : <strong>le conseil et le rêve restent 100 % humains</strong>. L'automatisation s'occupe des devis, rappels, relances et avis : vos clients voient une agence qui pense à eux avant, pendant et après. C'est ce qui transforme un voyageur en habitué.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de réservation ?", "Oui : on se branche sur vos outils (GDS, réservations, facturation). Rien ne change pour votre équipe."),
            ("Les devis automatiques sont-ils personnalisables ?", "Ils suivent votre grille et vos fournisseurs, et vous validez avant envoi."),
            ("Par quoi commencer ?", "Les rappels de départ : c'est le poste qui crée le plus de valeur perçue pour vos clients."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-services-b2b.html", "Cabinets et agences"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-dentiste.html",
        title="Automatisation cabinet dentaire : rappels, contrôles, liste d'attente : des dents suivies",
        meta="Rappels de contrôle, prises de RDV, liste d'attente, avis : comment un cabinet dentaire remplit son agenda. Exemples concrets.",
        h1="Cabinet dentaire : <em>des contrôles rappelés, des agendas remplis.</em>",
        sub="Chaque contrôle oublié est un soin retardé et un créneau perdu. Voici comment l'automatisation remplit votre agenda : au service des patients.",
        sections=[
            section("Le quotidien du cabinet", "Les frustrations qui vident l'agenda",
                pains([
                    ("Les contrôles oubliés", "6 mois, 1 an : les échéances", "Des soins retardés", "Rappel automatique au bon moment"),
                    ("Les rendez-vous manqués", "Un créneau perdu", "Des heures non facturées", "Rappel la veille + liste d'attente"),
                    ("Les avis Google", "La réputation locale", "Des patients satisfaits silencieux", "Demande d'avis après le soin"),
                ])),
            section("Les 8 tâches à automatiser", "Du rappel de contrôle au suivi",
                pains([
                    ("Rappels de contrôle", "Échéances 6 mois / 1 an", "Des soins retardés", "Rappel automatique + créneau proposé"),
                    ("Prise de RDV + rappels", "Téléphone, messages", "Des créneaux perdus", "Créneaux proposés, confirmation, rappel J-1"),
                    ("Liste d'attente intelligente", "Une annulation", "Un créneau vide", "Le prochain patient prévenu automatiquement"),
                    ("Demande d'avis après le soin", "Le patient repart satisfait", "Des avis jamais écrits", "SMS post-soin → avis Google"),
                    ("Suivi post-opératoire", "Extractions, implants", "Des suivis oubliés", "Message automatique de suivi + relais si problème"),
                    ("Le standard / questions", "Urgences, devis, horaires", "Des interruptions", "Réponses immédiates, les urgences au cabinet"),
                    ("Relance des devis", "Devis de soins", "Des soins reportés", "Relance polie J+7"),
                    ("Relance des paiements", "Restes à charge", "Des impayés", "Relance polie en 3 paliers"),
                ])),
            section("Votre crainte, honnêtement", "« La santé dentaire, c'est de la relation de confiance. »",
                prose("<p>Et elle le reste : <strong>le soin et la relation restent 100 % humains</strong>. L'automatisation s'occupe des rappels, créneaux et avis : les patients voient un cabinet qui pense à eux. C'est ce qui fait revenir, et recommander.</p>")),
        ],
        faq=[
            ("Les rappels sont personnalisables par patient ?", "Oui : chaque patient a son échéance de contrôle. Le message cite son nom et le motif du rendez-vous."),
            ("Ça marche avec mon logiciel dentaire ?", "Oui : on se branche sur vos outils (planning, dossier patient, facturation). Rien ne change pour votre équipe."),
            ("Par quoi commencer ?", "Les rappels de contrôle : c'est le poste qui remplit l'agenda avec les patients existants."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-cabinet-medical.html", "Cabinet médical"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-boulangerie.html",
        title="Automatisation boulangerie : fournisseurs, stocks, avis : la baguette sans paperasse",
        meta="Commandes fournisseurs, stocks, avis, gestion des invendus : comment une boulangerie automatise sa gestion. Exemples concrets.",
        h1="Boulangerie : <em>le four qui chauffe, la paperasse qui disparaît.</em>",
        sub="Farine, fournisseurs, stocks, invendus, avis : chaque jour génère sa paperasse. Voici comment l'automatisation la fait disparaître.",
        sections=[
            section("Le quotidien de la boulangerie", "Les frustrations qui rongent la marge",
                pains([
                    ("Les commandes fournisseurs", "Farine, beurre, emballages", "Des ruptures ou des surstocks", "Commande suggérée d'après les ventes réelles"),
                    ("Les stocks", "Des dizaines de références", "Des écarts", "Inventaire simplifié + alertes de seuil"),
                    ("Les avis Google", "La réputation locale", "Des clients satisfaits silencieux", "Demande d'avis après le passage"),
                ])),
            section("Les 8 tâches à automatiser", "De la commande fournisseur à l'avis",
                pains([
                    ("Commandes fournisseurs", "Farine, beurre, emballages", "Des ruptures", "Commande suggérée d'après les ventes réelles"),
                    ("Gestion des stocks", "Références, seuils", "Des écarts", "Inventaire simplifié + alertes"),
                    ("Gestion des invendus", "Pain, viennoiseries", "Du gaspillage", "Prévision simple d'après les ventes + don suggéré"),
                    ("Devis traiteurs / pros", "Entreprises, événements", "Des réponses lentes", "Devis chiffré en 30 secondes"),
                    ("Demande d'avis après le passage", "Le client est content", "Des avis jamais écrits", "SMS → avis Google"),
                    ("Le standard / questions", "Horaires, commandes, allergènes", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Relance des impayés (pros)", "Traiteurs, entreprises", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("La caisse et le rapprochement", "Fin de service, CB, espèces", "Des heures de pointage", "Rapprochement automatique"),
                ])),
            section("Votre crainte, honnêtement", "« Ma boulangerie, c'est du fait main et du contact. »",
                prose("<p>Et c'est vrai : <strong>le pain et l'accueil restent 100 % faits main</strong>. L'automatisation s'occupe des commandes, stocks, invendus et avis : le boulanger retrouve ses nuits, et les clients leur baguette.</p>")),
        ],
        faq=[
            ("Ça marche avec ma caisse ?", "Oui : on se branche sur vos exports de caisse et vos outils. Les suggestions viennent de vos ventes réelles."),
            ("La prévision des invendus est-elle fiable ?", "Elle se base sur vos ventes passées et s'améliore chaque semaine. Vous restez seul juge des quantités."),
            ("Par quoi commencer ?", "La demande d'avis : c'est le poste qui construit votre réputation locale en continu."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-restauration.html", "Restaurant / traiteur"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-librairie.html",
        title="Automatisation librairie : commandes, avis, événements : le libraire qui vend plus",
        meta="Commandes clients, avis, événements, stocks : comment une librairie automatise sa gestion. Exemples concrets.",
        h1="Librairie : <em>des commandes suivies, des lecteurs fidèles.</em>",
        sub="Chaque commande, chaque événement, chaque avis compte. Voici comment l'automatisation libère le libraire pour ce qui compte : les livres et les lecteurs.",
        sections=[
            section("Le quotidien de la librairie", "Les frustrations qui grignotent le temps",
                pains([
                    ("Les commandes", "Commandes clients, retours", "Des oublis", "Suivi automatique des commandes + alertes"),
                    ("Les événements", "Dédicaces, ateliers", "Des salles vides", "Annonce automatique + rappels aux habitués"),
                    ("Les avis", "La réputation locale", "Des lecteurs silencieux", "Demande d'avis après l'achat"),
                ])),
            section("Les 8 tâches à automatiser", "De la commande au lecteur fidèle",
                pains([
                    ("Commandes clients", "Arrivages, retours", "Des oublis", "Suivi automatique + notification d'arrivée"),
                    ("Notification d'arrivée", "Le livre est disponible", "Le client oublie de venir", "SMS/email « votre livre est arrivé »"),
                    ("Événements / dédicaces", "Annonces, inscriptions", "Des salles vides", "Annonce automatique + rappels"),
                    ("Demande d'avis après l'achat", "Le lecteur est satisfait", "Des avis jamais écrits", "SMS → avis Google"),
                    ("Commandes fournisseurs", "Stocks, nouveautés", "Des ruptures", "Commande suggérée d'après les ventes"),
                    ("Le standard / questions", "Horaires, disponibilités", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Relance des impayés (pros)", "Écoles, collectivités", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("La caisse et le rapprochement", "Fin de service", "Des heures de pointage", "Rapprochement automatique"),
                ])),
            section("Votre crainte, honnêtement", "« La librairie, c'est du conseil, pas des robots. »",
                prose("<p>Et c'est exactement le principe : <strong>le conseil littéraire reste 100 % humain</strong>. L'automatisation s'occupe des commandes, événements, avis et stocks : le libraire passe ses journées à conseiller, pas à saisir.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de librairie ?", "Oui : on se branche sur vos outils (gestion, caisse, diffusion). Rien ne change pour votre équipe."),
            ("Les notifications d'arrivée marchent ?", "Oui : c'est le poste qui fait revenir les clients et accélère la rotation des commandes."),
            ("Par quoi commencer ?", "La notification d'arrivée : vos clients attendent leurs livres, dites-leur qu'ils sont là."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-commerce-services.html", "Réservoir Commerce"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-psychologue.html",
        title="Automatisation cabinet de psychologue : rendez-vous, rappels, suivi : l'agenda qui s'occupe de tout",
        meta="Rendez-vous, rappels de séance, suivi, avis : comment un psychologue libère son temps pour ses patients. Exemples concrets.",
        h1="Psychologue : <em>l'agenda s'occupe de tout, vous vous occupez des patients.</em>",
        sub="Chaque séance = un rappel, un créneau, parfois un report. L'administratif d'un cabinet libéral est invisible mais lourd. Voici comment l'automatisation l'allège.",
        sections=[
            section("Le quotidien du cabinet", "Les frustrations qui s'ajoutent à la charge",
                pains([
                    ("Les rappels de séance", "No-show, oublis", "Des créneaux perdus", "Rappel automatique la veille + confirmation"),
                    ("Les reports", "Un patient qui décale", "Des trous dans l'agenda", "Report simple + créneau proposé automatiquement"),
                    ("Les avis Google", "La réputation locale", "Des patients satisfaits silencieux", "Demande d'avis (délicate, optionnelle)"),
                ])),
            section("Les 8 tâches à automatiser", "Du premier contact au suivi",
                pains([
                    ("Prise de RDV + rappels", "Premiers contacts, séances", "Des allers-retours", "Créneaux proposés + rappel J-1"),
                    ("Liste d'attente", "Des demandes en attente", "Des places perdues", "Le prochain patient prévenu automatiquement"),
                    ("Gestion des reports", "Annulations, décalages", "Des trous dans l'agenda", "Report simple + créneau proposé"),
                    ("Relance des honoraires", "Séances, forfaits", "Des impayés", "Relance polie et discrète en 3 paliers"),
                    ("Comptes-rendus de séance (notes)", "Notes personnelles", "Des heures de rédaction", "Notes structurées générées puis validées"),
                    ("Le standard / questions", "Horaires, tarifs, démarrage", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation", "Des patients silencieux", "Demande discrète et optionnelle"),
                    ("Les rappels de suivi", "Patients en pause", "Des ruptures de suivi", "Message bienveillant de reprise (optionnel)"),
                ])),
            section("Votre crainte, honnêtement", "« La psychothérapie, c'est de l'humain, pas des robots. »",
                prose("<p>Et c'est exactement le principe : <strong>la thérapie reste 100 % humaine et confidentielle</strong>. L'automatisation s'occupe de l'agenda, des rappels et de la discrétion administrative : le patient voit un praticien organisé qui ne le fait jamais attendre.</p>")),
        ],
        faq=[
            ("La confidentialité est-elle garantie ?", "Oui : les données restent dans vos outils, rien n'est envoyé hors de votre système. Les messages sont sobres et neutres."),
            ("Ça marche avec mon agenda actuel ?", "Oui : on se branche sur vos outils (agenda, facturation). Rien ne change pour votre pratique."),
            ("Par quoi commencer ?", "Les rappels de séance : ils réduisent les no-show, sensibles dans cette profession."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("automatisation-cabinet-medical.html", "Cabinet médical"), ("prise-rendez-vous.html", "Prise de RDV"), ("index.html", "← Retour à l'accueil")],
    ),
    dict(
        file="automatisation-aide-domicile.html",
        title="Automatisation services à la personne : planning, facturation, rappels : l'aide qui arrive à l'heure",
        meta="Planning des intervenants, facturation, rappels, CESU : comment une entreprise de services à la personne automatise. Exemples concrets.",
        h1="Services à la personne : <em>des intervenants à l'heure, des clients suivis.</em>",
        sub="Planning, remplacements, facturation CESU, rappels : chaque intervenant, chaque client génère sa coordination. Voici comment l'automatisation la fluidifie.",
        sections=[
            section("Le quotidien de l'entreprise", "Les frustrations qui épuisent la coordination",
                pains([
                    ("Le planning des intervenants", "Remplacements, absences", "Des heures de téléphone", "Planning centralisé + remplacement proposé automatiquement"),
                    ("La facturation CESU", "Heures réelles, tiers payant", "Des erreurs", "Facture générée depuis les interventions réelles"),
                    ("Les clients oubliés", "Aides, courses, RDV", "Des rendez-vous manqués", "Rappel automatique au client et à l'intervenant"),
                ])),
            section("Les 8 tâches à automatiser", "De la prise en charge au suivi",
                pains([
                    ("Planning des intervenants", "Tournées, remplacements", "Des heures de téléphone", "Planning centralisé + alertes d'absence"),
                    ("Gestion des remplacements", "Un intervenant absent", "Un client sans aide", "Remplacement proposé automatiquement"),
                    ("Rappels au client et à l'intervenant", "Interventions à venir", "Des rendez-vous manqués", "Rappel automatique la veille"),
                    ("Facturation des heures réelles", "Heures, déplacements, CESU", "Des erreurs", "Facture générée depuis les interventions"),
                    ("Relance des impayés", "Particuliers, mandataires", "Trésorerie tendue", "Relance polie en 3 paliers"),
                    ("Le standard / questions", "Disponibilités, tarifs, aides", "Des interruptions", "Réponses immédiates, les cas réels à vous"),
                    ("Les avis Google", "La réputation locale", "Des familles satisfaites silencieuses", "Demande d'avis (avec discrétion)"),
                    ("Le suivi des contrats", "Renouvellements, avenants", "Des oublis", "Rappel automatique des échéances"),
                ])),
            section("Votre crainte, honnêtement", "« Les services à la personne, c'est de l'humain avant tout. »",
                prose("<p>Et c'est vrai : <strong>l'aide apportée reste 100 % humaine</strong>. L'automatisation s'occupe de la coordination, des rappels et de la facturation : les familles voient une entreprise fiable qui arrive à l'heure, et votre équipe arrête de courir après le téléphone.</p>")),
        ],
        faq=[
            ("Ça marche avec mon logiciel de SAP ?", "Oui : on se branche sur vos outils (planning, facturation, CESU). Rien ne change pour vos intervenants."),
            ("La facturation CESU est-elle gérée ?", "Oui : elle suit vos conventions et les heures réelles, avec les mentions obligatoires. Vous validez avant envoi."),
            ("Par quoi commencer ?", "Les rappels au client et à l'intervenant : c'est le poste qui réduit immédiatement les rendez-vous manqués."),
            ("Combien ça coûte ?", "Offre découverte 490 € pour une première automatisation en 7 jours, puis maintenance à partir de 149 €/mois."),
        ],
        nav_links=[("hub-sante-bien-etre.html", "Réservoir Santé"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="offre-eti.html",
        title="Pilote IA 30 jours pour PME & ETI : 3 automatisations chiffrées en 1 mois",
        meta="Offre pilote IA 30 jours : audit, 2 automatisations livrées et chiffrées, roadmap. Pour PME 20-500 salariés qui veulent des résultats mesurables.",
        h1="PME & ETI : <em>le pilote IA 30 jours</em>",
        sub="Pas de projet de 6 mois, pas de présentation PowerPoint : un pilote d'un mois, 2 automatisations livrées et chiffrées, et une roadmap pour la suite. 5 000 à 15 000 €.",
        sections=[
            section("Pour qui ?", "Vous êtes une PME ou une ETI si…",
                pains([
                    ("Vos équipes passent des heures sur du répétitif", "Tri d'emails, saisie, relances, rapports", "Des centaines d'heures par an", "Les 3 tâches à plus fort ROI identifiées en 1 semaine"),
                    ("Vous avez déjà un ERP mais rien ne se fait seul", "Des outils, mais des flux manuels entre eux", "Des saisies en double", "Des automatisations branchées sur VOS outils"),
                    ("Vous voulez des résultats, pas des slides", "Des projets IA qui n'aboutissent pas", "De l'argent dépensé sans mesure", "2 automatisations livrées et chiffrées en 30 jours"),
                ])),
            section("Le déroulé du pilote", "4 semaines, des livrables chaque semaine",
                pains([
                    ("Semaine 1 : Audit flash", "3 tâches à fort ROI identifiées", "Des choix au hasard", "Cartographie + chiffrage des gains potentiels"),
                    ("Semaine 2 : Pilote n°1", "La tâche la plus rentable automatisée", "Des mois d'attente", "Automatisation n°1 livrée et testée sur vos données"),
                    ("Semaine 3 : Pilote n°2", "Une 2e tâche automatisée", "Un seul cas traité", "Automatisation n°2 livrée : vos équipes formées"),
                    ("Semaine 4 : Bilan & roadmap", "Des métriques réelles", "Des promesses vagues", "Bilan chiffré (heures gagnées, erreurs évitées) + plan d'extension"),
                ])),
            section("Pourquoi ça marche ici", "Ce qui rend le pilote possible",
                pains([
                    ("Des blocs prêts, pas du sur-mesure", "14 automatisations déjà construites et testées", "Des devis à 50 000 €", "Le pilote réutilise des blocs éprouvés, paramétrés pour vous"),
                    ("Vos données restent chez vous", "Hébergement sur votre NAS ou vos serveurs", "Des données chez un prestataire", "Zéro clé API dans les fichiers, export complet chez vous"),
                    ("Un interlocuteur ex-contrôleur de gestion", "Des promesses vagues", "Des chiffres flous", "Des métriques réelles : heures, euros, erreurs : mesurés, pas estimés"),
                ])),
        ],
        faq=[
            ("Combien ça coûte ?", "Le pilote complet : 5 000 à 15 000 € selon le nombre de tâches et la complexité. L'audit flash seul : 490 €, déductible du pilote si vous continuez."),
            ("Et après le pilote ?", "Vous gardez les automatisations (elles restent à vous) et choisissez : maintenance mensuelle (à partir de 299 €/mois) ou extension sur la roadmap."),
            ("Nos données sont-elles en sécurité ?", "Oui : l'architecture est pensée pour l'hébergement chez vous (NAS ou serveur interne). Aucune clé API dans les fichiers, export complet remis à la livraison."),
            ("On commence quand ?", "L'audit flash peut démarrer sous 8 jours. Le pilote complet sous 2 à 3 semaines selon la disponibilité de vos équipes."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("automatisation-tresorerie.html", "Trésorerie"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="prospection-linkedin.html",
        title="Prospection LinkedIn pilotée : messages personnalisés, relances contextualisées, suivi",
        meta="Trouvez vos clients idéaux, scannez leurs profils, envoyez des messages personnalisés et relancez intelligemment. Un système de prospection LinkedIn qui convertit.",
        h1="Prospection LinkedIn : <em>fini les messages ignorés.</em>",
        sub="Le message générique « Bonjour, je passe » ne convertit plus. Voici un système complet : le bon prospect, le bon message, la bonne relance : avec un suivi qui mesure tout.",
        sections=[
            section("Le problème", "Pourquoi votre prospection LinkedIn ne répond pas",
                pains([
                    ("Les messages génériques", "« Bonjour, je souhaite me présenter… »", "1-2 % de réponse", "Un message qui référence SA situation et SON pain"),
                    ("Les relances oubliées", "La séquence s'arrête au 1er message", "Des opportunités perdues", "Des relances planifiées, contextualisées"),
                    ("Le suivi éparpillé", "Excel + LinkedIn + mémoire", "Des prospects perdus", "Un CRM qui suit chaque conversation"),
                ])),
            section("Le système", "4 étapes, des résultats mesurés",
                pains([
                    ("1. Trouver le client idéal", "Définition de l'ICP par votre métier", "Des prospects au hasard", "Les bons profils, les bonnes verticales"),
                    ("2. Scanner les profils", "Analyse IA de chaque profil", "Des messages à l''aveugle", "Pain détecté + score de fit 0-100"),
                    ("3. Messages personnalisés", "Générés par l''IA avec vos patterns gagnants", "Des heures de rédaction", "Un message unique par prospect, en 10 secondes"),
                    ("4. Relances contextualisées", "Chaque relance lit la conversation d''origine", "Des relances hors-sujet", "Une relance qui rebondit sur SA réponse"),
                ])),
            section("Ce qui le rend unique", "L'auto-amélioration",
                pains([
                    ("Il apprend de vos réponses", "Chaque réponse positive est analysée", "Les mêmes messages qui ne marchent pas", "Le pattern gagnant est réutilisé automatiquement"),
                    ("Multi-canaux", "LinkedIn + email dans la séquence", "Un seul canal", "J0 LinkedIn → J+3 relance → J+7 email → J+14 final"),
                    ("Zéro risque", "Envoi contrôlé, pas d''automatisation du clic", "Des comptes bannis", "Votre compte reste sain, LinkedIn ne voit rien d''anormal"),
                ])),
            section("L'offre : Prospection pilotée", "Des résultats, pas un outil à gérer",
                pains([
                    ("Mise en place (1 semaine)", "ICP + 50 prospects scannés + messages prêts", "Des semaines de tâtonnement", "490 € à 990 € selon votre métier"),
                    ("Suivi mensuel", "Relances contextualisées + nouveaux prospects + optimisation auto", "Des relances oubliées", "149 € à 299 €/mois"),
                    ("Variable sur résultats", "Payé sur les rendez-vous confirmés", "Des forfaits sans lien avec les résultats", "25 € à 50 € par RDV booké : payé seulement quand ça marche"),
                    ("Transparence totale", "Tableau de bord client : taux de réponse, RDV, conversations", "Des promesses vagues", "Vos chiffres réels, chaque mois"),
                ])),
        ],
        faq=[
            ("Ça marche pour quel métier ?", "Services B2B, agences, cabinets conseil, experts-comptables, formation, immobilier : les métiers où le client est sur LinkedIn."),
            ("Combien de temps pour voir des résultats ?", "Les premiers échanges sous 2 semaines ; un rendez-vous sous 4-6 semaines avec 40-60 contacts qualifiés."),
            ("Mon compte est-il en danger ?", "Non : l'envoi reste manuel (copier-coller contrôlé). Nous n'automatisons pas le clic, contrairement à certains outils qui font bannir les comptes."),
            ("Combien ça coûte ?", "Mise en place (ICP + 50 profils scannés + messages prêts) : 490 à 990 €. Suivi mensuel : 149 à 299 €/mois. En plus, un variable de 25 à 50 € par rendez-vous confirmé : vous ne payez la performance que lorsqu'elle arrive."),
            ("Comment je sais que ça marche ?", "Un tableau de bord client montre chaque mois vos chiffres réels : taux de réponse, relances envoyées, rendez-vous bookés. Pas de promesses vagues : vos métriques, en direct."),
            ("C'est moi qui vends ensuite ?", "Oui : vous gardez la vente. Le système vous amène des rendez-vous qualifiés et vous fait gagner du temps sur la prospection : vous, vous vendez."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("offre-eti.html", "Pilote ETI"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="formation-n8n.html",
        title="Formation n8n complète : du zéro absolu au workflow en production (débutant)",
        meta="Apprenez n8n pas à pas : 6 modules, 32 leçons, exercices pratiques et projet final. Simple, pédagogique, à jour (n8n 2.x). Débutant bienvenu.",
        h1="Formation n8n : <em>du zéro absolu au premier workflow.</em>",
        sub="Vous n'avez jamais touché à n8n ? Parfait. Ce parcours vous emmène de « c'est quoi un workflow ? » jusqu'à une automatisation fiable en production : avec la rigueur d'un professionnel.",
        sections=[
            section("La promesse", "Un parcours pensé pour les débutants",
                pains([
                    ("Zéro prérequis", "Pas besoin de coder, ni de connaître n8n", "Des cours qui supposent des connaissances", "Chaque concept est défini avant d'être utilisé"),
                    ("100 % pratique", "Chaque leçon = un exercice sur VOTRE instance", "De la théorie sans application", "Vous construisez en apprenant, pas en regardant"),
                    ("La rigueur professionnelle", "Tester, journaliser, sécuriser", "Des automatisations fragiles", "Le fil rouge : qualité, fiabilité, satisfaction"),
                ])),
            section("Le parcours", "6 modules, 32 leçons, 1 projet final",
                pains([
                    ("Module 0 : Découvrir", "L'automatisation, n8n, l'interface, le vocabulaire", "1 h", "Les bases sans jargon"),
                    ("Module 1 : Fondations", "Triggers, webhooks, expressions", "2 h", "Votre premier workflow qui répond"),
                    ("Module 2 : Premiers workflows", "Horloge, HTTP, conditions, Code", "3 h", "Le classificateur de demandes"),
                    ("Module 3 : Les données", "JSON, CSV, multi-items, les pièges", "2 h 30", "Traiter des factures"),
                    ("Module 4 : L'IA", "DeepSeek, prompts, JSON structuré, les garde-fous", "3 h", "Un répondeur qui classe les emails"),
                    ("Module 5 : Production", "Erreurs, tests, logs, sécurité, supervision", "3 h", "Un workflow fiable et traçable"),
                    ("Module 6 : Projet final", "Construire la relance impayés en 3 paliers", "4 h", "Un livrable prêt pour un vrai client"),
                ])),
            section("Ce qui rend cette formation différente", "La qualité comme fil rouge",
                pains([
                    ("Les pièges réels enseignés", "Les erreurs vécues en production (boucles vides, GET local, multi-triggers)", "Des cours théoriques", "Vous apprenez sur les vrais pièges, pas les exemples propres"),
                    ("L'IA avec des garde-fous", "L'IA peut se tromper : validation humaine, contexte, journalisation", "De l'IA sans filet", "La fiabilité avant la vitesse"),
                    ("La sécurité dès le début", "Clés protégées, hébergement maîtrisé", "Des clés exposées", "Vos données et celles de vos clients restent chez vous"),
                ])),
        ],
        faq=[
            ("Je n'ai jamais codé de ma vie, c'est pour moi ?", "Oui : aucun prérequis. Les premiers modules expliquent tout depuis zéro, avec des analogies simples (le workflow = la recette de cuisine)."),
            ("C'est à jour ?", "Oui : le parcours cible n8n 2.32.x (la version actuelle) et les bonnes pratiques 2026. Il évolue avec les versions."),
            ("Je vais vraiment construire quelque chose ?", "Dès la 2e heure vous avez un webhook fonctionnel. Le projet final est une relance impayés en 3 paliers, testée et prête à l'emploi."),
            ("Combien ça coûte ?", "Parcours complet : 490 € (290 € en lancement). Ateliers mensuels pratiques (Cercle n8n) : 49 €/mois. Formation intra-entreprise : 1 500-3 000 €/jour."),
            ("Et après la formation ?", "Vous repartez avec votre projet final + la méthode. Et si vous préférez déléguer, l'offre maintenance prend le relais."),
        ],
        nav_links=[("apprendre-n8n.html", "Apprendre n8n"), ("abonnements.html", "Cercle n8n"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="solutions-par-besoin.html",
        title="Automatisation par besoin : encaisser, vendre, servir, produire, savoir, se conformer",
        meta="Trouvez l'automatisation selon VOTRE besoin : encaisser plus vite, remplir l'agenda, fidéliser, produire sans erreur, décider mieux, être en règle. Les démos sont testables en direct.",
        h1="Par quoi voulez-vous <em>commencer ?</em>",
        sub="Chaque métier a ses besoins. Choisissez le vôtre : les automatisations correspondantes s'affichent, et chacune est testable en direct dans le Labo.",
        sections=[
            section("💰 Encaisser et payer", "Les factures rentrent, les relances partent, les comptes se rapprochent",
                pains([
                    ("Relance des impayés", "J+7 poli, J+21 ferme, J+35 dernier recours", "Des factures oubliées", "Le bon ton au bon moment : démo : 📧 Relance impayés"),
                    ("Rapprochement bancaire", "Chaque opération rapprochée de sa facture, l'écart expliqué", "Des heures de pointage", "Statut calculé par le code, zéro hallucination : démo : 🏦 Rapprochement"),
                    ("Facturation électronique", "Bilan de conformité et actions datées : réception 09/2026, émission 09/2027", "Une obligation légale subie", "Le niveau calculé, le calendrier clair : démo : 🧾 Facturation électronique"),
                    ("Tri des factures", "Facture, devis ou spam : classé automatiquement, montants extraits", "Une boîte mail saturée", "Démo : 📧 Tri emails"),
                ])),
            section("🤝 Servir le client", "Le client servi vite, bien, et qui revient",
                pains([
                    ("Rendez-vous confirmés", "Rappels J-1, créneaux proposés automatiquement", "Des rendez-vous manqués", "Démo : 📅 Rappel RDV + 🗓️ Prise de RDV"),
                    ("Réponses aux avis", "Une réponse pro à chaque avis, même les négatifs", "Des avis sans réponse", "Démo : ⭐ Avis Google"),
                    ("Support qui répond", "Tickets classés, brouillons prêts, validation humaine", "Des clients en attente", "Démo : 🎫 Support tickets"),
                    ("Statut et retours", "Le client informé de sa commande, le rappel qui fait revenir", "Des clients qui appellent pour savoir", "Démo : 🚚 Statut client + 🔄 Retour client"),
                ])),
            section("📈 Vendre et garder le fil", "Devis rapides, relances intelligentes, prospects jamais oubliés",
                pains([
                    ("Devis express", "Un devis chiffré en 30 secondes, 24h/24", "Des devis qui partent en retard", "Démo : 💶 Agent Devis"),
                    ("Relance des devis", "J+7, J+14, J+21 : le devis sans réponse n'est jamais oublié", "Des devis morts", "Démo : 📄 Relance de devis"),
                    ("Prospection LinkedIn", "Le client idéal scanné, le message personnalisé, la relance contextualisée", "Des messages génériques ignorés", "L'outil Prospection pilotée"),
                    ("Idées de contenu", "5 idées prêtes avec angle et hook, chaque matin", "La page blanche", "Démo : 💡 Machine à idées"),
                ])),
            section("🏭 Produire et livrer", "Le stock juste, les chantiers suivis, les pièces jamais perdues",
                pains([
                    ("Stock sous contrôle", "Alerte + réappro chiffré au bon moment", "Des tableaux qui mentent", "Démo : 📦 Stock"),
                    ("Compte-rendu de chantier", "Des notes brutes au CR structuré", "Des CR écrits le dimanche", "Démo : 📝 Compte-rendu"),
                ])),
            section("🧠 Savoir et décider", "Le briefing, le reporting, la veille : décidez avec des faits",
                pains([
                    ("Briefing matinal", "Votre journée résumée chaque matin", "Une matinée à tout relire", "Démo : 🌅 Briefing matinal"),
                    ("Reporting", "CA, tendances, anomalies : les chiffres qui parlent", "Des tableaux Excel interminables", "Démo : 📈 Reporting"),
                    ("Veille concurrentielle", "3 signaux, 1 menace, 1 opportunité chaque matin", "20 articles à lire", "Démo : 📡 Veille concurrentielle"),
                    ("Compte-rendu de réunion", "Décisions, actions, échéances : prêt à envoyer", "Des notes dans un carnet", "Démo : 📝 Compte-rendu"),
                ])),
            section("📋 Être en règle", "Les échéances légales, la conformité, la transparence",
                pains([
                    ("Facturation électronique", "Le bilan de conformité calculé, les actions datées", "Une obligation qui tombe en 2026-2027", "Démo : 🧾 Facturation électronique"),
                    ("La transparence IA", "L'IA Act expliqué simplement, les bonnes pratiques", "Une réglementation floue", "Guide : l'IA peut-elle se tromper ?"),
                ])),
            section("🔬 Santé et professions réglementées", "Les métiers sous obligation : ordonnances, dossiers, facturation",
                pains([
                    ("Standard IA", "Répond aux patients sans attendre", "Un standard qui sonne", "Démo : 💬 Standard IA / FAQ"),
                    ("Rappels de rendez-vous", "Moins de rendez-vous manqués", "Des créneaux perdus", "Démo : 📅 Rappel RDV"),
                ])),
        ],
        faq=[
            ("Comment choisir ?", "Cliquez sur votre besoin : les automatisations correspondantes s'affichent, avec une démo testable en direct. Chaque démo utilise de vraies données, pas une simulation."),
            ("Je ne trouve pas mon métier ?", "Les besoins ci-dessus sont transverses : toutes les PME encaissent, servent, vendent. Le détecteur de tâches vous montre les vôtres en 2 minutes."),
            ("Et si je veux tout ?", "Le Pack PME regroupe les automatisations essentielles. L'appel de 15 minutes gratuites permet de prioriser selon votre situation."),
        ],
        nav_links=[("detecteur-taches.html", "Détecter mes tâches"), ("labo-demo.html", "Tester dans le Labo"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="engagements-fiabilite.html",
        title="Nos engagements fiabilité : zéro hallucination, des sources citées, l'humain qui valide",
        meta="Pourquoi vous pouvez faire confiance : les décisions sont calculées par le code, l'IA ne rédige que le texte, chaque donnée a une source. La fiabilité est notre produit.",
        h1="La fiabilité est <em>notre produit.</em>",
        sub="Vous vendez de la qualité, nous aussi. Voici les 5 engagements qui protègent vos données, votre réputation et votre temps.",
        sections=[
            section("1. L'IA propose, la machine décide", "Les décisions critiques ne sont jamais laissées à l'IA",
                pains([
                    ("Les statuts sont calculés", "Rapproché, partiel, palier de relance, niveau de conformité : le code calcule, avec les règles officielles (clé SIRET, clé TVA, Luhn)", "Une IA qui invente", "Des résultats déterministes, vérifiables"),
                    ("L'IA rédige le texte", "Elle formule, elle n'arrête pas", "Un chiffre inventé", "Le texte est relu avant envoi"),
                    ("Zéro faux témoignage", "Les avis clients ne paraissent qu'après de vrais clients", "Des preuves inventées", "Une confiance construite sur des faits"),
                ])),
            section("2. Chaque donnée a une source", "Les chiffres, taux et échéances sont sourcés",
                pains([
                    ("Les sources officielles", "impots.gouv.fr, facturation.gouv.fr (PPF), EUR-Lex, service-public.fr, INSEE, VIES : citées en pied de page", "Des chiffres flottants", "Vérifiables en un clic"),
                    ("Les échéances légales comme FAITS", "Réception 01/09/2026, émission 01/09/2027 : intégrées comme faits, jamais devinées par l'IA", "Une loi mal comprise", "Le bon calendrier, garanti"),
                    ("Les ordres de grandeur sont marqués", "« selon les cas », « ~ » : la précision honnête", "Une fausse précision", "Des promesses tenables"),
                ])),
            section("3. Jamais d'erreur silencieuse", "Si ça casse, vous le savez",
                pains([
                    ("Tout est journalisé", "Chaque action importante est tracée (date, référence, résultat)", "Un bug invisible", "La traçabilité complète"),
                    ("Les tests 3 cas", "Normal, limite, anormal : chaque automatisation est validée", "Un test unique", "Les cas limites sont couverts"),
                    ("L'humain valide ce qui part", "Relances, devis, messages : un humain valide avant l'envoi", "Des envois automatiques", "Votre marque protégée"),
                ])),
            section("4. Vos données restent à vous", "Hébergement maîtrisé, zéro clé exposée",
                pains([
                    ("Exportable", "Tout tourne chez vous (NAS) ou chez nous, exportable à tout moment", "Une dépendance", "La liberté totale"),
                    ("Sécurité des clés", "Aucune clé API dans les fichiers, les exports ou les dépôts", "Des clés fuitées", "La conformité par défaut"),
                ])),
            section("5. La règle en cas de doute", "On ne l'affirme pas, on le vérifie",
                pains([
                    ("« À vérifier », « selon votre cas »", "Quand un point est incertain, nous le disons", "Des certitudes fausses", "Une honnêteté qui rassure"),
                    ("Les sources citées", "Vérifiez vous-même en un clic", "Un site opaque", "La transparence totale"),
                ])),
        ],
        faq=[
            ("Pourquoi cette page ?", "Parce que la fiabilité ne se promet pas : elle se prouve. Chaque démo, chaque bloc, chaque chiffre de ce site suit ces 5 engagements."),
            ("Comment vérifier une source ?", "Les liens en pied de page des pages réglementaires mènent aux sources officielles (impots.gouv.fr, EUR-Lex, service-public.fr, INSEE, VIES)."),
            ("Et si une automatisation se trompe ?", "Le système journalise tout : une erreur est détectée, tracée, corrigée : jamais silencieuse. C'est notre métier."),
        ],
        nav_links=[("solutions-par-besoin.html", "Solutions par besoin"), ("methode.html", "Méthode"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="offre-cabinet-en-regle.html",
        title="Offre cabinet en règle : servir vos patients, être en conformité, encaisser plus vite",
        meta="Pour pharmaciens, dentistes, kinés, experts-comptables : rappels de RDV, ordonnancier vérifié, document d'entrée en relation, facturation électronique. Testez les démos en direct.",
        h1="Votre cabinet <em>en règle,</em> vos patients bien servis.",
        sub="Les professions réglementées cumulent les obligations : ordonnancier, documents d'entrée en relation, facturation électronique, transparence IA. Voici les automatisations qui vous libèrent du papier : sans jamais décider à votre place.",
        sections=[
            section("Le problème", "Les obligations s'accumulent, le temps manque",
                pains([
                    ("L'ordonnancier incomplet", "Des ordonnances à vérifier avant délivrance", "Un contrôle oublié", "La complétude calculée, les questions prêtes"),
                    ("Le document d'entrée en relation", "Une obligation pour chaque nouveau client", "Un document jamais envoyé", "Le modèle généré, validé par vous"),
                    ("La facturation électronique", "Réception 09/2026, émission 09/2027", "Une échéance subie", "Le bilan de conformité, les actions datées"),
                ])),
            section("Le système", "3 volets, 9 automatisations testables",
                pains([
                    ("🤝 Servir vos patients", "Rappels de RDV, prise de rendez-vous, standard IA qui répond", "Des rendez-vous manqués", "Le patient servi vite, qui revient"),
                    ("📋 Être en règle", "Ordonnancier, document d'entrée en relation, facturation électronique, transparence IA", "Des obligations floues", "Le conformité calculée, les documents prêts"),
                    ("💰 Encaisser plus vite", "Relances des impayés, rapprochement bancaire, base clients propre", "Des paiements en retard", "La trésorerie sous contrôle"),
                ])),
            section("La règle d'or", "L'IA prépare, le professionnel décide",
                pains([
                    ("Zéro avis médical", "L'IA ne donne JAMAIS d'avis médical, elle prépare la vérification", "Une IA qui prescrit", "Le pharmacien décide, toujours"),
                    ("Zéro décision déontologique", "Les documents sont des modèles à valider par le professionnel", "Un modèle envoyé sans validation", "Votre déontologie protégée"),
                    ("Zéro hallucination", "Statuts et complétudes calculés par le code, sources citées", "Un chiffre inventé", "La fiabilité prouvée"),
                ])),
        ],
        faq=[
            ("Ça s'adresse à quels métiers ?", "Pharmacies, cabinets dentaires, kinésithérapeutes, experts-comptables, conseils en gestion : toute profession réglementée avec des obligations documentaires."),
            ("L'IA remplace-t-elle le professionnel ?", "Non, jamais : l'IA prépare (complétude, modèles, brouillons), le professionnel vérifie et décide. C'est la règle d'or de l'offre."),
            ("Combien ça coûte ?", "Mise en place (2-3 automatisations prioritaires) : 490 à 990 €. Suivi mensuel : 149 à 299 €/mois. Chaque automatisation est testable avant."),
            ("La facturation électronique est incluse ?", "Oui : le bilan de conformité (réception 09/2026, émission 09/2027) et la base clients font partie du socle."),
        ],
        nav_links=[("hub-sante-bien-etre.html", "Réservoir Santé"), ("prospection-linkedin.html", "Prospection pilotée"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),

    dict(
        file="l-ia-peut-elle-se-tromper.html",
        title="L'IA peut-elle se tromper ? Oui. Voici comment on attrape les erreurs avant vous.",
        meta="Oui, l'IA hallucine : une date inventée, un régime TVA faux. La différence, c'est le système qui attrape l'erreur avant l'envoi. Les preuves réelles, ici.",
        h1="L'IA peut-elle se tromper ? <em>Oui.</em>",
        sub="Et c'est exactement pour ça que vous pouvez nous faire confiance. Voici 3 erreurs réelles que notre système a attrapées avant qu'elles ne partent, et le mécanisme qui les bloque.",
        sections=[
            section("Les 3 erreurs réelles attrapées", "Nos tests, pas des promesses",
                pains([
                    ("La date hallucinée", "L'IA avait écrit une date de relance en 2023 au lieu de aujourd'hui + 7 jours. Corrigé : la date est calculée par le code, jamais par l'IA.", "Une date fausse envoyée", "La date est un fait calculé"),
                    ("Le régime TVA erroné", "L'IA écrivait « autoliquidation » pour un client UE sans n° de TVA valide. Corrigé : le régime est calculé (pays + type client), l'IA ne le change jamais.", "Une TVA fausse sur une facture", "Le régime est calculé, pas deviné"),
                    ("Le parseur silencieux", "Un résultat qui ne rentrait pas dans le format attendu partait sans rien dire. Corrigé : le parseur valide le format, journalise, et ne répond pas n'importe quoi.", "Une erreur silencieuse", "Tout est journalisé et visible"),
                ])),
            section("Pourquoi on l'attrape", "Le mécanisme anti-hallucination (5 règles)",
                pains([
                    ("L'IA propose, la machine décide", "Statuts, paliers, régimes, dates : calculés par le code avec les règles officielles", "Une IA qui décide", "Des résultats déterministes"),
                    ("Chaque donnée a une source", "impots.gouv.fr, EUR-Lex, service-public.fr, INSEE, VIES : citées en pied de page", "Un chiffre flottant", "Vérifiable en un clic"),
                    ("Jamais d'erreur silencieuse", "Journalisation, tests 3 cas, validation humaine avant envoi", "Un bug invisible", "La traçabilité complète"),
                    ("Zéro faux témoignage", "Les preuves sont réelles ou elles ne sont pas", "Des preuves inventées", "La confiance sur des faits"),
                    ("En cas de doute, on le dit", "« À vérifier », « selon votre cas », « aide, pas un avis juridique »", "Des certitudes fausses", "L'honnêteté qui rassure"),
                ])),
            section("Vérifiez vous-même", "La preuve est testable",
                pains([
                    ("Les 35 démos", "Chaque automatisation est testable en direct : le résultat s'affiche sous vos yeux", "Une vidéo montée", "Le vrai comportement, en direct"),
                    ("Les sources en pied de page", "Chaque page réglementaire cite ses sources officielles", "Un site opaque", "La transparence totale"),
                ])),
        ],
        faq=[
            ("Donc l'IA se trompe parfois ?", "Oui, toutes les IA hallucinent parfois. La question n'est pas de le nier, c'est de construire un système qui attrape l'erreur avant l'envoi. C'est notre métier."),
            ("Comment prouver que vous attrapez les erreurs ?", "Les 3 exemples ci-dessus sont réels (date, TVA, parseur). Et les 35 démos du Labo montrent le comportement réel, pas une simulation."),
            ("Et si une erreur passe quand même ?", "Tout est journalisé : une erreur est détectée, tracée, corrigée. Jamais silencieuse. Et vous validez avant l'envoi de toute relance ou facture."),
        ],
        nav_links=[("engagements-fiabilite.html", "Engagements fiabilité"), ("automatisations.html", "Les 35 automatisations"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),
]

def main():
    os.makedirs(SITE, exist_ok=True)
    for p in PAGES:
        html = build(p, p["sections"], p["faq"], p["nav_links"])
        with open(os.path.join(SITE, p["file"]), "w", encoding="utf-8") as f:
            f.write(html)
        print("généré:", p["file"])

if __name__ == "__main__":
    main()
