# PLAN DES 7 ACTIONS (avec exploration préalable)

Chaque action : exploration (preuves) → plan → implémentation → vérification.

## ACTION 1 — Service client automatique + Guide "IA pour les nuls"
**Exploration** : `automatisation service client` · `support client` (autocomplete réels) ; `intelligence artificielle pour les nuls pdf gratuit`.
**Plan** :
- `service-client.html` (page pain, template existant) : réponses FAQ auto, SAV premier niveau, réclamations, suivi de ticket → AVANT/APRÈS + craintes + FAQ JSON-LD
- `guide-ia-pour-les-nuls.html` (imprimable) : les 3 idées, glossaire 10 mots, 5 exemples, la peur de l'emploi
- Ajout au hub guides + nav "Je cherche à..."

## ACTION 2 — Générateur de devis + Excel facture auto
**Exploration** : `générateur de devis gratuit` · `générateur de devis ia` · `logiciel devis facture artisan` · `facture excel automatique gratuit`.
**Plan** :
- `generateur-devis.html` (outil interactif JS) : formulaire (entreprise, client, date, lignes prestations/quantité/prix, TVA) → devis propre imprimable en PDF + lien upsell "version automatique 24/7"
- `modele-facture-excel.xlsx` (fichier réel openpyxl) : numéro auto, TVA 20%, total HT/TTC, prêt à imprimer + mini-guide dans la page téléchargement
- Page de téléchargement + liens depuis automatiser-devis / automatiser-excel

## ACTION 3 — Pages secteur + peur de l'emploi + formation
**Exploration** : `ia pour artisan` · `agent ia pour artisan` · `ia remplace emploi` · `formation ia salarié`.
**Plan** :
- `automatisation-artisan.html` : les 6 pains artisan (devis, factures, RDV, avis, relances, planning chantier)
- `ia-remplace-t-elle-mon-employe.html` : la peur n°1, réponse factuelle + SEO
- `formation-ia-pme.html` : offre formation équipe (atelier 2h, demi-journée, accompagnement)

## ACTION 4 — Offre 490 € + prix par pain + maintenance
**Exploration** : `combien coute un agent ia` ; référentiel Malt (TJM 400-700 niches IA, missions 1 500-9 000 € selon pain).
**Plan** :
- `tarifs.html` : audit gratuit → offre découverte 490 € (1 automatisation simple, prix fixe) → missions par pain (fourchettes honnêtes) → maintenance 150-300 €/mois
- Notes prix ajoutées aux pages pain (CTA)
- Maintenance visible sur la page méthode

## ACTION 5 — Formulaire contact → workflow n8n (dogfood)
**Exploration** : instance n8n 2.32.7 OK, credential DeepSeek OK, procédure import/activation connue (skill n8n-instance-ops). Pas de credentials Gmail/Sheets → scope : capture + stockage local + confirmation.
**Plan** :
- Workflow "Agent Contact Site" : Webhook `/contact` → Code (extraction + sauvegarde CSV `/root/consulting/leads.csv`) → DeepSeek (accusé personnalisé) → réponse JSON
- Activation (import + publish + restart + race 8s)
- `contact.html` : formulaire → fetch POST webhook (fallback mailto si échec)
- Test réel (curl) + lead vérifié dans CSV
- ⚠️ J+3 relance : nécessite Gmail/Telegram → note dans l'état

## ACTION 6 — Page experts-comptables + 3 emails prospection
**Exploration** : `automatisation cabinet comptable` · `automatisation expert comptable` · `ia comptable` (cabinets cherchent eux-mêmes).
**Plan** :
- `experts-comptables.html` (page B2B) : 3 usages (saisie, relances clients, reporting), partenariat (commission), CTA
- `prospection-emails.md` : 3 emails prêts (expert-comptable, artisan BTP, PME locale)

## ACTION 7 — SEO technique + 404 + popup WhatsApp
**Exploration** : head actuel = title/meta seulement ; pas de canonical/OG/schéma ; pas de 404 ; gérants sur mobile.
**Plan** :
- Générateur : header enrichi (canonical placeholder domaine, OG, JSON-LD ProfessionalService) + bouton WhatsApp flottant mobile (footer) → régénérer les 9 pages
- Patch des pages clés écrites à la main (index, contact, guides, newsletter, quiz, detecteur, demos, methode)
- `404.html` (Netlify-ready)
- Vérif : canonical/OG/schéma présents, 404 OK
