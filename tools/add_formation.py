#!/usr/bin/env python3
"""Ajoute la page formation-n8n.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : formation-n8n.html ajoutée")
