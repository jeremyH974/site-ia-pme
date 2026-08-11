#!/usr/bin/env python3
"""Ajoute la page prospection-linkedin.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
        ],
        faq=[
            ("Ça marche pour quel métier ?", "Services B2B, agences, cabinets conseil, experts-comptables, formation, immobilier : les métiers où le client est sur LinkedIn."),
            ("Combien de temps pour voir des résultats ?", "Les premiers échanges sous 2 semaines ; un rendez-vous sous 4-6 semaines avec 40-60 contacts qualifiés."),
            ("Mon compte est-il en danger ?", "Non : l'envoi reste manuel (copier-coller contrôlé). Nous n'automatisons pas le clic, contrairement à certains outils qui font bannir les comptes."),
            ("Combien ça coûte ?", "Mise en place (ICP + 50 profils scannés + messages prêts) : 490 à 990 €. Suivi mensuel (relances + nouveaux prospects + optimisation) : 149 à 299 €/mois."),
        ],
        nav_links=[("hub-b2b-pro.html", "Réservoir B2B"), ("offre-eti.html", "Pilote ETI"), ("contact.html", "Contact"), ("index.html", "← Retour à l'accueil")],
    ),
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : prospection-linkedin.html ajoutée")
