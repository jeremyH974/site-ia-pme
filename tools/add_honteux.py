#!/usr/bin/env python3
"""Ajoute la page l-ia-peut-elle-se-tromper.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : l-ia-peut-elle-se-tromper.html ajoutée")
