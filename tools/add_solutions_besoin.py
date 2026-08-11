#!/usr/bin/env python3
"""Ajoute la page solutions-par-besoin.html au générateur build_site.py"""
src = open("build_site.py", encoding="utf-8").read()

PAGE = '''
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
]'''

marker = "]\n\ndef main():"
assert src.count(marker) == 1
src = src.replace(marker, PAGE + "\n" + marker)
open("build_site.py", "w", encoding="utf-8").write(src)
print("OK : solutions-par-besoin.html ajoutée")
