#!/usr/bin/env python3
"""Génère les 6 hubs par famille métier : V2 : toutes les 40 verticales réparties.
Usage : python3 tools/gen_hubs.py  (à exécuter dans /root/consulting/site/)
"""
import os, re

HEADER = """<header class="site-header nav-v4">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">Jeremy<span>, Data Analyst · Automatisation &amp; IA</span></a>
    <nav class="main-nav" aria-label="Navigation principale">
      <a href="index.html">Accueil</a>
      <details class="nav-drop">
        <summary>Solutions ▾</summary>
        <div class="nav-drop-menu">
          <a href="detecteur-taches.html">🎯 Trouver MES tâches à automatiser</a>
          <a href="automatiser-devis.html">Devis &amp; factures</a>
          <a href="relance-impayes.html">Relances &amp; impayés</a>
          <a href="service-client.html">Service client &amp; avis</a>
          <a href="compte-rendu-reunion.html">Comptes-rendus &amp; RDV</a>
          <span class="nav-drop-sep"></span>
          <a href="index.html#solutions" class="nav-drop-all">Toutes les solutions →</a>
        </div>
      </details>
      <a href="guides.html">Guides</a>
      <a href="demos.html">Démos</a>
      <a href="labo-demo.html">Labo</a>
      <a href="abonnements.html">Abonnements</a>
      <a href="tarifs.html">Tarifs</a>
      <a class="btn btn-primary nav-cta" href="contact.html">15 min offertes</a>
    </nav>
    <details class="nav-mobile">
      <summary>☰ Menu</summary>
      <nav aria-label="Navigation mobile">
        <a href="index.html">Accueil</a>
        <a href="detecteur-taches.html">🎯 Trouver mes tâches</a>
        <a href="automatiser-devis.html">Devis &amp; factures</a>
        <a href="relance-impayes.html">Relances &amp; impayés</a>
        <a href="service-client.html">Service client &amp; avis</a>
        <a href="compte-rendu-reunion.html">Comptes-rendus &amp; RDV</a>
        <a href="index.html#solutions">Toutes les solutions →</a>
        <a href="guides.html">Guides gratuits</a>
        <a href="demos.html">Démos</a>
        <a href="labo-demo.html">Labo</a>
        <a href="abonnements.html">Abonnements</a>
        <a href="tarifs.html">Tarifs</a>
        <a class="btn btn-primary" href="contact.html">15 min offertes</a>
      </nav>
    </details>
  </div>
</header>"""

STYLE_HUB = """
.hub-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:24px}
@media(max-width:860px){.hub-grid{grid-template-columns:1fr}}
.hub-card{background:var(--white);border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px;box-shadow:var(--shadow)}
.hub-card h3{margin:0 0 4px;font-size:17px}
.hub-card p{font-size:13px;color:var(--ink-soft);margin:0 0 12px}
.hub-links{display:flex;flex-wrap:wrap;gap:6px}
.hub-links a{font-size:12px;background:var(--paper-2);border:1px solid var(--line);border-radius:20px;padding:5px 11px;text-decoration:none;color:var(--ink);transition:.15s}
.hub-links a:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.hub-cta{margin-top:26px}
"""

def page(filename, emoji, title, meta, intro, familles, cta_note):
    cards = ""
    for fam in familles:
        links = "".join(f'          <a href="{href}">{label}</a>\n' for href, label in fam["links"])
        cards += f"""<div class="hub-card">
        <h3>{fam['icon']} {fam['nom']}</h3>
        <p>{fam['desc']}</p>
        <div class="hub-links">
{links}        </div>
      </div>
"""
    html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://VOTRE-DOMAINE.fr/{filename}">
<link rel="stylesheet" href="style.css">
<style>{STYLE_HUB}</style>
</head>
<body>
{HEADER}
<section class="hero">
  <div class="wrap">
    <span class="eyebrow">Le réservoir par métier</span>
    <h1>{emoji} <em>{title.split(' : ')[0]}</em></h1>
    <p class="sub">{intro}</p>
  </div>
</section>
<section>
  <div class="wrap">
    <span class="section-label">Toutes les solutions pour ce métier</span>
    <h2>Choisissez votre point d'entrée</h2>
    <div class="hub-grid">{cards}</div>
    <div class="hub-cta" style="text-align:center">
      <p style="color:var(--ink-soft);font-size:14px">{cta_note}</p>
      <div class="cta-inline" style="justify-content:center">
        <a class="btn btn-primary" href="detecteur-taches.html">🎯 Trouver MES tâches à automatiser</a>
        <a class="btn btn-ghost" href="labo-demo.html">🧪 Tester les démos en direct</a>
      </div>
    </div>
  </div>
</section>
<footer>
  <div class="wrap">
    <span>© 2026 Jeremy : Consultant IA &amp; Automatisation pour PME</span>
    <span><a href="index.html">Accueil</a> · <a href="demos.html">Démos</a> · <a href="labo-demo.html">Labo</a> · <a href="confidentialite.html">Confidentialité</a> · <a href="contact.html">Contact</a></span>
  </div>
</footer>
</body>
</html>"""
    open(filename, "w", encoding="utf-8").write(html)
    print(f"✅ {filename}")

# === HUBS : toutes les verticales par famille ===
page("hub-artisans-btp.html", "🛠️", "Automatisation artisans & BTP : toutes les solutions au même endroit",
     "Devis express, planning chantiers, relances impayés, avis Google : toutes les automatisations pour artisans, garagistes, électriciens, menuisiers et paysagistes.",
     "Devis qui traînent, chantiers mal suivis, clients qui oublient de payer : chaque métier du BTP a ses mêmes 5 pains. Voici toutes les solutions, au même endroit.",
     [
         {"icon": "🚗", "nom": "Garage / auto", "desc": "RDV, révisions, rappels, avis", "links": [("automatisation-garage.html", "Page garage"), ("labo-demo.html", "Démo rappel RDV"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "⚡", "nom": "Électricien", "desc": "Devis express, attestations, chantiers", "links": [("automatisation-electricien.html", "Page électricien"), ("automatiser-devis.html", "Devis express"), ("relance-impayes.html", "Relance impayés")]},
         {"icon": "🪚", "nom": "Menuisier / atelier", "desc": "Devis, planning atelier, suivi commandes", "links": [("automatisation-menuisier.html", "Page menuisier"), ("automatiser-devis.html", "Devis express"), ("labo-demo.html", "Démo statut client")]},
         {"icon": "🌿", "nom": "Paysagiste", "desc": "Contrats d'entretien récurrents, devis", "links": [("automatisation-paysagiste.html", "Page paysagiste"), ("abonnements.html", "Contrats récurrents"), ("relance-impayes.html", "Relance impayés")]},
         {"icon": "🎨", "nom": "Artisans (peinture…)", "desc": "Le guide complet des artisans", "links": [("automatisation-artisan.html", "Page artisans"), ("automatiser-devis.html", "Devis express"), ("pack-pme.html", "Pack PME gratuit")]},
         {"icon": "📐", "nom": "Architecte", "desc": "Devis honoraires, CR chantier, dossiers", "links": [("automatisation-architecte.html", "Page architecte"), ("compte-rendu-reunion.html", "Comptes-rendus"), ("labo-demo.html", "Démo CR")]},
     ],
     "Toutes ces automatisations existent déjà et tournent : testez-les en direct dans le Labo.")

page("hub-sante-bien-etre.html", "🩺", "Automatisation santé & bien-être : toutes les solutions",
     "Rappels de rendez-vous, gestion des no-show, avis, comptes-rendus : toutes les automatisations pour cabinets médicaux, pharmacie, vétérinaires et bien-être.",
     "Des rendez-vous manqués, des rappels oubliés, des patients qui ne reviennent pas : la santé vit de la régularité. Voici toutes les solutions, au même endroit.",
     [
         {"icon": "🩺", "nom": "Cabinet médical / kiné", "desc": "RDV, no-show, CR, standard", "links": [("automatisation-cabinet-medical.html", "Page cabinet médical"), ("prise-rendez-vous.html", "Prise de RDV"), ("compte-rendu-reunion.html", "Comptes-rendus")]},
         {"icon": "💊", "nom": "Pharmacie", "desc": "Standard, commandes, renouvellements", "links": [("automatisation-pharmacie.html", "Page pharmacie"), ("gestion-stock-automatique.html", "Gestion de stock"), ("labo-demo.html", "Démo standard IA")]},
         {"icon": "🐾", "nom": "Vétérinaire", "desc": "Rappels vaccins par animal, RDV, avis", "links": [("automatisation-veterinaire.html", "Page vétérinaire"), ("labo-demo.html", "Démo rappel RDV"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "🦷", "nom": "Dentiste", "desc": "Contrôles, RDV, liste d'attente", "links": [("automatisation-dentiste.html", "Page dentiste"), ("prise-rendez-vous.html", "Prise de RDV"), ("labo-demo.html", "Démo rappel RDV")]},
         {"icon": "🧠", "nom": "Psychologue", "desc": "RDV, rappels, suivi discret", "links": [("automatisation-psychologue.html", "Page psychologue"), ("prise-rendez-vous.html", "Prise de RDV"), ("labo-demo.html", "Démo rappel RDV")]},
         {"icon": "💆", "nom": "Spa / institut", "desc": "RDV, fidélité, avis", "links": [("automatisation-spa.html", "Page spa"), ("prise-rendez-vous.html", "Prise de RDV"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "💇", "nom": "Coiffure / beauté", "desc": "Rappels, avis, fidélité", "links": [("automatisation-coiffure.html", "Page coiffure"), ("repondre-avis-google.html", "Avis Google"), ("labo-demo.html", "Démo rappel RDV")]},
         {"icon": "🤝", "nom": "Aide à domicile", "desc": "Planning, CESU, rappels", "links": [("automatisation-aide-domicile.html", "Page SAP"), ("labo-demo.html", "Démo rappel RDV"), ("relance-impayes.html", "Relance impayés")]},
     ],
     "Les rappels de rendez-vous à eux seuls réduisent les no-show de 30 à 50 %.")

page("hub-tourisme-accueil.html", "🏨", "Automatisation tourisme & accueil : toutes les solutions",
     "Réservations directes, avis, arrivées, planning ménage : toutes les automatisations pour hôtels, campings, locations saisonnières, restaurants et agences.",
     "Des commissions qui grignotent la marge, des avis sans réponse, des arrivées qui débordent : l'accueil vit de la fluidité. Voici toutes les solutions.",
     [
         {"icon": "🏨", "nom": "Hôtel / gîte", "desc": "Réservations directes, avis, ménage", "links": [("automatisation-hotellerie.html", "Page hôtellerie"), ("repondre-avis-google.html", "Avis Google"), ("labo-demo.html", "Démo demande d'avis")]},
         {"icon": "🏕️", "nom": "Camping / vacances", "desc": "Réservations, arrivées, avis", "links": [("automatisation-camping.html", "Page camping"), ("labo-demo.html", "Démo rappel RDV"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "🏠", "nom": "Location saisonnière", "desc": "Direct, arrivée autonome, avis", "links": [("automatisation-location-saisonniere.html", "Page loc. saisonnière"), ("repondre-avis-google.html", "Avis Google"), ("labo-demo.html", "Démo standard IA")]},
         {"icon": "🔑", "nom": "Conciergerie", "desc": "Messages, avis, réservations", "links": [("automatisation-conciergerie.html", "Page conciergerie"), ("labo-demo.html", "Démo standard IA"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "✈️", "nom": "Agence de voyage", "desc": "Devis, rappels, avis", "links": [("automatisation-agence-voyage.html", "Page agence de voyage"), ("automatiser-devis.html", "Devis express"), ("labo-demo.html", "Démo rappel RDV")]},
         {"icon": "🍽️", "nom": "Restaurant / traiteur", "desc": "Réservations, planning, fournisseurs", "links": [("automatisation-restauration.html", "Page restauration"), ("gestion-stock-automatique.html", "Gestion de stock"), ("labo-demo.html", "Démo devis")]},
         {"icon": "🚐", "nom": "Food truck", "desc": "Commandes WhatsApp, tournées, caisse", "links": [("automatisation-food-truck.html", "Page food truck"), ("chatbot-whatsapp.html", "Chatbot WhatsApp"), ("labo-demo.html", "Démo stock")]},
         {"icon": "🍺", "nom": "Bar / café", "desc": "Caisse, fournisseurs, événements", "links": [("automatisation-bar.html", "Page bar"), ("gestion-stock-automatique.html", "Gestion de stock"), ("labo-demo.html", "Démo rapprochement")]},
     ],
     "Chaque réservation directe en plus = 10-20 % de marge en plus.")

page("hub-commerce-services.html", "👔", "Automatisation commerce & services : toutes les solutions",
     "Suivi d'articles, notifications, abonnements, avis : toutes les automatisations pour pressings, boulangeries, librairies et e-commerce.",
     "Des articles oubliés, des clients silencieux, des revenus irréguliers : le commerce vit de la régularité. Voici toutes les solutions.",
     [
         {"icon": "👔", "nom": "Pressing", "desc": "Suivi articles, retraits, abonnements", "links": [("automatisation-pressing.html", "Page pressing"), ("abonnements.html", "Abonnements clients"), ("labo-demo.html", "Démo retour client")]},
         {"icon": "🥖", "nom": "Boulangerie", "desc": "Fournisseurs, stocks, avis", "links": [("automatisation-boulangerie.html", "Page boulangerie"), ("gestion-stock-automatique.html", "Gestion de stock"), ("labo-demo.html", "Démo stock")]},
         {"icon": "📚", "nom": "Librairie", "desc": "Commandes, événements, avis", "links": [("automatisation-librairie.html", "Page librairie"), ("labo-demo.html", "Démo retour client"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "🛒", "nom": "E-commerce", "desc": "Statut commandes, avis, relances", "links": [("ia-pour-ecommerce.html", "Page e-commerce"), ("labo-demo.html", "Démo statut client"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "🧾", "nom": "Gestion de stock", "desc": "Alertes de seuil, réappro", "links": [("gestion-stock-automatique.html", "Page stock"), ("labo-demo.html", "Démo stock"), ("pack-pme.html", "Pack PME gratuit")]},
         {"icon": "🧭", "nom": "Trouver mes tâches", "desc": "Le détecteur 42 profils", "links": [("detecteur-taches.html", "Le détecteur"), ("quiz.html", "Le quiz"), ("pack-pme.html", "Pack PME gratuit")]},
     ],
     "Les abonnements transforment un commerce irrégulier en revenu prévisible.")

page("hub-transport-logistique.html", "🚚", "Automatisation transport & logistique : toutes les solutions",
     "Facturation, rapprochement des gains, rappels, tournées : toutes les automatisations pour transporteurs, VTC et auto-écoles.",
     "Chaque course = une facture, chaque client = un rappel, chaque semaine = un pointage. Voici toutes les solutions pour rouler sans paperasse.",
     [
         {"icon": "🚚", "nom": "Transport / livraison", "desc": "Facturation tournées, lettres de voiture", "links": [("automatisation-transport.html", "Page transport"), ("relance-impayes.html", "Relance impayés"), ("labo-demo.html", "Démo rapprochement")]},
         {"icon": "🚕", "nom": "VTC / taxi", "desc": "Facturation auto, rappels, rapprochement", "links": [("automatisation-vtc.html", "Page VTC"), ("labo-demo.html", "Démo rapprochement"), ("relance-impayes.html", "Relance impayés")]},
         {"icon": "🚗", "nom": "Auto-école", "desc": "Rappels de leçon, CERFA, heures", "links": [("automatisation-auto-ecole.html", "Page auto-école"), ("prise-rendez-vous.html", "Prise de RDV"), ("labo-demo.html", "Démo rappel RDV")]},
         {"icon": "🏋️", "nom": "Salle de sport / coach", "desc": "Séances, abonnements, avis", "links": [("automatisation-salle-sport.html", "Page salle de sport"), ("automatisation-coach-sportif.html", "Page coach"), ("labo-demo.html", "Démo rappel RDV")]},
     ],
     "Le rapprochement automatique des gains plateformes évite les écarts invisibles.")

page("hub-b2b-pro.html", "💼", "Automatisation B2B & professions libérales : toutes les solutions",
     "Devis, relances, comptes-rendus, agents IA : toutes les automatisations pour experts-comptables, professions libérales, écoles et organismes.",
     "Des heures de saisie, des relances oubliées, des CR à rédiger : les professionnels paient leur paperasse en heures. Voici toutes les solutions.",
     [
         {"icon": "🏦", "nom": "Trésorerie / finance", "desc": "Rapprochement, prévisionnel, alertes", "links": [("automatisation-tresorerie.html", "Page trésorerie"), ("labo-demo.html", "Démo rapprochement"), ("experts-comptables.html", "Experts-comptables")]},
         {"icon": "💼", "nom": "Cabinets & agences", "desc": "Devis, reporting, suivi missions", "links": [("automatisation-services-b2b.html", "Page cabinets"), ("labo-demo.html", "Démo tri email"), ("relance-impayes.html", "Relance impayés")]},
         {"icon": "⚖️", "nom": "Avocat", "desc": "Relances, CR, honoraires", "links": [("automatisation-avocat.html", "Page avocat"), ("compte-rendu-reunion.html", "Comptes-rendus"), ("labo-demo.html", "Démo CR")]},
         {"icon": "🏢", "nom": "Experts-comptables", "desc": "Tri emails, rapprochement, reporting", "links": [("experts-comptables.html", "Page experts-comptables"), ("labo-demo.html", "Démo tri email"), ("labo-demo.html", "Démo rapprochement")]},
         {"icon": "🏠", "nom": "Immobilier", "desc": "Devis, relances, avis, mandats", "links": [("ia-pour-immobilier.html", "Page immobilier"), ("automatiser-devis.html", "Devis express"), ("repondre-avis-google.html", "Avis Google")]},
         {"icon": "🏢", "nom": "Syndic", "desc": "Charges, relances, assemblées", "links": [("automatisation-syndic.html", "Page syndic"), ("relance-impayes.html", "Relance impayés"), ("compte-rendu-reunion.html", "Comptes-rendus")]},
         {"icon": "🗝️", "nom": "Gestion locative", "desc": "Quittances, loyers, états des lieux", "links": [("automatisation-gestion-locative.html", "Page gestion locative"), ("relance-impayes.html", "Relance impayés"), ("ia-pour-immobilier.html", "Immobilier")]},
         {"icon": "🎓", "nom": "Formation / écoles", "desc": "Inscriptions, convocations, bilans", "links": [("automatisation-organisme-formation.html", "Page formation"), ("automatisation-ecole.html", "Page école"), ("automatisation-creche.html", "Page crèche")]},
         {"icon": "🎪", "nom": "Événementiel", "desc": "Devis, prestataires, invités", "links": [("automatisation-evenementiel.html", "Page événementiel"), ("automatiser-devis.html", "Devis express"), ("compte-rendu-reunion.html", "Comptes-rendus")]},
         {"icon": "📚", "nom": "Professions libérales", "desc": "CR, RDV, standard, facturation", "links": [("professions-liberales.html", "Page professions libérales"), ("compte-rendu-reunion.html", "Comptes-rendus"), ("labo-demo.html", "Démo standard IA")]},
         {"icon": "🤖", "nom": "Agents IA", "desc": "Comprendre, se méfier, adopter", "links": [("agent-ia-cest-quoi.html", "Agent IA c'est quoi ?"), ("ia-peut-elle-se-tromper.html", "Où l'IA se trompe"), ("apprendre-n8n.html", "Apprendre n8n")]},
         {"icon": "🚀", "nom": "Offre ETI", "desc": "Pilote IA 30 jours (5-15 k€)", "links": [("offre-eti.html", "Le pilote ETI"), ("automatisation-tresorerie.html", "Trésorerie"), ("contact.html", "Contact")]},
     ],
     "L'expert-comptable est le prescripteur n°1 de l'automatisation PME : cette page lui est dédiée.")
