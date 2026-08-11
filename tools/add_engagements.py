#!/usr/bin/env python3
"""Ajoute la page engagements-fiabilite.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : engagements-fiabilite.html ajoutée")
