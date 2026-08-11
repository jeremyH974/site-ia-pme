# Recherche besoins / pains / retours d'expérience — site acquisition v2

Date : 31/07/2026 · Sources : commentaires Hacker News (threads réels), autocomplete Google FR.
Limite : Reddit, DuckDuckGo et Bing bloquent l'IP serveur (403) — pas de témoignages de forums FR récupérables d'ici ; à surveiller via le monitoring hebdo.

## 1. Pains validés par des retours d'expérience réels

### Pain facturation / emails → compta (le plus fort)
- Thread HN "invoicing paper small business" : la douleur facturation est universelle chez les petites boîtes, MAIS les clients résistent au changement d'habitudes (« je ne veux pas d'app pour recevoir mes factures »).
- Thread HN "HTTP standards invoicing" : **« I would pay $30/month for that »** (parser les emails de factures forwardés → Excel/QuickBooks/JSON). Des gens paient déjà pour ce pain.
- « Encore après 20 ans, les grandes boîtes n'arrivent pas à sortir des CSV exploitables » → le pain **exports bancaires/compta mal foutus** est universel.

### Pain coût des outils SaaS
- Thread HN "Activepieces (YC S22)" : le comparatif revient en boucle — « Zapier : free/100 tâches/mois · n8n : 20 € / 5 000 workflows ».
- L'open source self-hosted = différenciateur prix MASSIF pour les PME. C'est un argument de vente à mettre en avant, pas une note technique.

### Phase de questionnement FR (autocomplete)
- Requêtes réelles : `n8n avis` · `agent ia avis` · `chatgpt entreprise avis` · `automatiser son entreprise avec l ia` · `comment automatiser son entreprise`.
- Confirme : le visiteur du site est en mode "c'est quoi / avis / ça vaut le coup ?" → le site doit répondre à ÇA, pas vendre.

## 2. Ce qu'on pourrait AJOUTER au site (par priorité)

### P1 — Pages SEO dédiées (le vrai levier d'acquisition)
Créer une page par requête "phase c'est quoi" (chaque page = une réponse pédagogique + CTA) :
1. `agent-ia-cest-quoi.html` → cible "agent ia c'est quoi" (requête réelle)
2. `n8n-cest-quoi.html` → cible "n8n c'est quoi" + "n8n avis"
3. `rapprochement-bancaire-excel.html` → cible "rapprochement bancaire excel" (pain réel, universel)
4. `automatiser-factures.html` → cible "automatisation factures fournisseurs"
Chaque page : définition simple (2 paragraphes), exemple AVANT/APRÈS, mini-démo, CTA 15 min.

### P1 — Section objections ("Vos craintes, honnêtement")
Issue des retours d'expérience (résistance au changement, craintes de casse) :
- « Mes clients vont-ils devoir changer leurs habitudes ? » → Non : l'automatisation travaille sur VOS outils, vos clients ne voient rien.
- « Et si une automatisation casse ? » → Monitoring + alerte + maintenance (répond au pain "intégrations qui cassent").
- « Mes données sont-elles en sécurité ? » → n8n self-hosted = vos données restent chez vous.

### P2 — Bloc "Pourquoi c'est moins cher qu'un abonnement SaaS"
Comparatif simple : Zapier (coût par tâche) vs n8n open source (forfait mission, données chez vous). 3 lignes, zéro jargon. Argument ROI renforcé.

### P2 — Section "Résultats réels" (pas de faux témoignages)
- Cas réel N2C Peinture (4 j/semaine → 45 min) déjà cité → le transformer en histoire courte avec chiffres.
- Chiffres des démos (reporting 2 h → 10 s ; devis 30 s à 22 h ; rapprochement 3 h/mois → 30 s).
- Quand Jeremy aura 2-3 vrais clients : les remplacer par de vrais témoignages (jamais d'inventés).

### P3 — FAQ enrichie
- « C'est quoi la différence entre IA et automatisation ? » (l'IA fait, l'automatisation orchestre — les 3 idées du site le disent déjà, en faire une FAQ courte)
- « Pourquoi open source ? » (coût + données + pas de dépendance)

## 3. Verdict
Le site v1 est bon pour "rassurer et convertir". Pour **capter la phase c'est quoi** (le vrai trafic), il faut les pages SEO dédiées (P1) — c'est le chantier qui apporte des visiteurs, le reste optimise la conversion.
