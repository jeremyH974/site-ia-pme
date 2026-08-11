#!/usr/bin/env python3
"""Ajoute la page offre-eti.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : offre-eti.html ajoutée au générateur")
