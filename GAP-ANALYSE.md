# GAP ANALYSIS — site vs besoins/pains & vs recherches Google

Date : 31/07/2026 · Méthode : sonde autocomplete Google FR (30+ requêtes) + retours d'expérience HN + analyse des 5 pages existantes.

## PARTIE 1 — Ce qui manque par rapport aux besoins & pains

### ✅ Déjà couvert par le site
| Pain | Où |
|---|---|
| Répondre aux devis | accueil + page n8n |
| Tri emails / factures / extraction | page automatiser-factures |
| Rapprochement bancaire | page dédiée |
| Reporting / macro excel | accueil (pains) |
| Relances (mention) | accueil + page factures (partiel) |
| WhatsApp / relation client | accueil (partiel) |

### 🔴 P0 — MANQUE : Facturation électronique obligatoire 2026
- **Échéance réglementaire dans ~1 mois** (1er sept. 2026 : réception ; émission progressive grandes/ETI 2026, PME/micro 2027 — ⚠️ À CONFIRMER sur impots.gouv.fr avant publication, les pages officielles n'étaient pas extractibles).
- Requêtes réelles massives : `facturation électronique obligatoire 2026` (+ "seuil", "pour qui", "micro entreprise", "gratuite", "autoentrepreneur"), `facture electronique 2026`.
- Pourquoi c'est un gap critique : panique PME dans 1 mois, volume de recherche énorme ET croissant, et l'angle "préparez la facturation électronique + automatisez vos factures" est un aimant à leads parfait.
- Action : page dédiée « Facturation électronique 2026 : ce que les PME doivent savoir » + CTA audit.

### 🟠 P1 — Manques à forte valeur
1. **Relance des impayés (page dédiée)** — requêtes réelles : `relance impaye`, `relance impaye client`, `relance impayée par mail`, `recouvrement factures`, `relance client automatique`. Le site la mentionne seulement ; une page avec modèle de relance + escalade + automatisation = utile ET SEO.
2. **Avis Google / réputation** — requêtes : `répondre aux avis google`, `réponse avis google automatique`, `comment répondre aux avis google`. Pain réel des commerçants : réponse IA aux avis + demande d'avis automatique post-achat.
3. **Compte-rendu de réunion automatique** — requêtes : `compte rendu réunion automatique teams`, `...gratuit`, `transcription réunion ia`. Pain quotidien des dirigeants ; démo facile (transcription + résumé IA).
4. **Prise de RDV / rappels** — requêtes : `prise de rendez vous automatique`, `mail confirmation rendez vous client`. Angle : moins de no-show, rappels automatiques (fort pour auto-écoles, santé, services).

### 🟡 P2 — En veille / à intégrer
- **OCR factures** (`ocr factures fournisseurs`) → à intégrer en FAQ/section de la page factures (déjà implicite).
- **Gestion de stock** (`gestion de stock pme`) → pain réel mais angle IA moins démo-able rapidement.
- **CRM / gestion commerciale** (`crm pme gratuit`, `logiciel gestion commerciale pme`) → plutôt pain "logiciel" ; opportunité secondaire "CRM simple avec n8n".
- **Répondeur IA / téléphone** (`repondeur ia`) → volume orienté grand public (iPhone/Samsung), pas la cible PME ; surveiller.

## PARTIE 2 — Ce qui manque par rapport aux recherches Google

### Matrice de couverture (requêtes réelles → pages)
| Requête réelle trouvée | Couverte ? | Action |
|---|---|---|
| agent ia c'est quoi / gratuit / exemple | ✅ page | enrichir "gratuit" (comment tester soi-même) |
| n8n c'est quoi / n8n avis | ✅ page | — |
| rapprochement bancaire excel | ✅ page | — |
| automatisation factures fournisseurs | ✅ page | — |
| **facturation électronique obligatoire 2026** | ❌ | **page P0** |
| automatiser devis / devis automatisé | ~ (accueil/n8n) | page dédiée "automatiser devis" |
| relance impayé / recouvrement | ~ (mention) | page dédiée P1 |
| répondre aux avis google | ❌ | page P1 |
| compte rendu réunion automatique | ❌ | page P1 |
| prise de rendez-vous automatique | ❌ | page P1 |
| consultant ia pour pme / agent ia pour pme | ~ (accueil) | page "Consultant IA pour PME" (requête transactionnelle !) |
| macro excel | ~ (accueil) | page "Automatiser Excel" (ou section) |
| chatbot whatsapp business | ~ (accueil) | page "Chatbot WhatsApp pour PME" |
| ocr factures | ~ | intégrer FAQ page factures |
| gestion de stock / crm pme | ❌ | veille P2 |

### 🔴 Structure SEO absente (bloquant pour être trouvé)
1. **Pas de nom de domaine** → impossible de référencer durablement (URL trycloudflare change au redémarrage).
2. **Pas de sitemap.xml ni robots.txt.**
3. **Pas de Google Search Console** (soumission + suivi des requêtes).
4. **Pas d'analytics** (impossible de mesurer quoi que ce soit).
5. Pas de canonical / Open Graph complet (partiel) / tracking CTA.

Sans les points 1-3, les pages SEO (même parfaites) ne sont jamais indexées.

## GAP v3 — Ce qui manque encore (après construction des 21 pages)

1. **🔴 Le détecteur de tâches personnalisé** — le site dit quoi automatiser en général, mais n'aide pas le visiteur à trouver SES tâches. → OUTIL CONSTRUIT : `detecteur-taches.html` (profil métier + checklist + temps → top 3 quick wins + ROI + liens vers les pages).
2. **🟠 Par métier** : pas de page « que peut automatiser un peintre / une coiffeuse / un plombier ? ». Le détecteur couvre le besoin par profil ; des pages métier pourront le renforcer en SEO plus tard.
3. **🟠 Témoignages réels** : 0 pour l'instant (placeholders interdits par principe). Devient prioritaire dès 2-3 clients livrés (cas N2C Peinture = premier candidat).
4. **🟠 Visage / vidéo de présentation** : pas de face caméra sur le site → la confiance passe d'abord par la vidéo d'intro (à filmer avec les démos).
5. **🟠 ROI par pain** : le calculateur est global (heures × valeur). Affiner : « automatiser les relances = X €/an » par page.
6. **🟡 Prix par pain** : « combien coûte l'automatisation des relances ? » — fourchettes honnêtes à publier (réduit la peur).
7. **🟡 Convaincre mon équipe** : les gérants doivent vendre le projet en interne → petit guide « 5 arguments pour votre équipe ».
8. **🟡 Plan d'action 30 jours** : la checklist existe ; un plan séquencé (semaine 1 : trier, semaine 2 : relances...) guiderait le passage à l'action.
9. **🟡 Preuve de compétence** : cas documentés, formation, nombre d'heures gagnées cumulées → à alimenter au fil des missions.
10. **🟢 Suivi des leads** : formulaire mailto = OK pour démarrer ; un vrai backend (n8n dogfood) viendra en phase 2.

## RECOMMANDATION PRIORISÉE
1. **Immédiat (cette semaine)** : domaine (+ Netlify) → Search Console → sitemap. C'est le prérequis de tout le reste.
2. **Cette semaine aussi** : page P0 « Facturation électronique 2026 » (volume max, échéance dans 1 mois) + page « Consultant IA pour PME » (requête transactionnelle).
3. **Semaine prochaine** : pages P1 (relance impayés, avis Google, compte-rendu réunion).
4. **Au fil de l'eau** : intégrer OCR à la FAQ factures, puis P2.
