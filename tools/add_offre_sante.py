#!/usr/bin/env python3
"""Ajoute la page offre-cabinet-en-regle.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : offre-cabinet-en-regle.html ajoutée")
