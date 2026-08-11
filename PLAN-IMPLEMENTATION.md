# PLAN D'IMPLEMENTATION COMPLET — Écosystème d'acquisition Jeremy

Vision : **transformer les recherches Google et les posts LinkedIn en appels de 15 min**.
Pilier : le site capte → le contenu distribue → l'automatisation convertit → le suivi fidélise.
Horizon : 4 semaines (août 2026). Légende : 🤖 = je peux exécuter · 👤 = nécessite Jeremy (compte/clé/accord).

---

## PHASE 0 — FONDATIONS TECHNIQUES (semaine 1 · jours 1-3)
*Prérequis : sans ça, rien n'est indexable ni mesurable.*

| # | Tâche | Qui | Livrable |
|---|---|---|---|
| 0.1 | Choisir le nom de marque + acheter le domaine (.fr de préférence) | 👤 | domaine ≈ 10-15 €/an (ovh, gandi, namecheap) |
| 0.2 | Déployer le site sur Netlify (gratuit, HTTPS, déploiement git ou drag&drop) | 🤖 | URL stable https://votrenom.fr |
| 0.3 | Rediriger/arrêter le tunnel trycloudflare (preview uniquement) | 🤖 | propreté + sécurité |
| 0.4 | sitemap.xml + robots.txt + canonical + favicon + Open Graph complet | 🤖 | 5 pages sitemapées |
| 0.5 | Google Search Console (soumission + suivi requêtes) | 🤖+👤 | compte Google requis |
| 0.6 | Analytics (Plausible simple OU GA4) | 🤖 | mesure visites/CTA |
| 0.7 | Email pro contact@votrenom.fr + redirection | 👤 | crédibilité + tracking |
| 0.8 | Page 404 + page "Merci" (post-formulaire) | 🤖 | UX propre |

**Succès Phase 0** : site en HTTPS sur domaine propre, indexable, mesurable.

---

## PHASE 1 — LE SITE QUI CAPTE (semaine 1-2)
*Objectif : couvrir les requêtes réelles trouvées (autocomplete + gap analysis).*

### Pages P0 (cette semaine — volume max)
| Page | Requête ciblée | Contenu clé |
|---|---|---|
| `facturation-electronique-2026.html` | facturation électronique obligatoire 2026 (+ seuil, pour qui, gratuite) | échéances officielles (à vérifier), qui est concerné, erreurs à éviter, comment l'IA prépare + CTA |
| `consultant-ia-pme.html` | consultant ia pour pme, agent ia pour pme | positionnement, méthode, ROI chiffré, cas N2C, CTA |

### Pages P1 (semaine 2)
| Page | Requête ciblée | Contenu clé |
|---|---|---|
| `relance-impayes.html` | relance impaye, recouvrement factures | modèle de relance en 3 paliers, escalade automatique |
| `repondre-avis-google.html` | répondre aux avis google | réponses IA aux avis, demande d'avis post-achat |
| `compte-rendu-reunion.html` | compte rendu réunion automatique | transcription + résumé IA, démo |
| `prise-rendez-vous.html` | prise de rendez vous automatique | rappels auto, moins de no-show |

### Pages P2 (semaine 2-3, au fil de l'eau)
`automatiser-devis.html` · `automatiser-excel.html` · `chatbot-whatsapp.html` · `gestion-stock.html` (veille)

### Optimisations SEO on-page (toutes les pages)
- Title/description uniques · FAQ JSON-LD (fait) · maillage interne (page-nav) · H1 unique · temps de chargement · mobile-first
- **Ajout d'une mini-démo visuelle sur chaque page** (les rapports HTML des démos 2/4 + le webhook devis)

**Succès Phase 1** : 10-12 pages couvrant ~15 requêtes réelles.

---

## PHASE 2 — LE SITE QUI CONVERTIT (semaine 2-3)

| # | Idée | Pourquoi | Qui |
|---|---|---|---|
| 2.1 | **Formulaire de contact** (Netlify Forms/Formspree) au lieu du mailto | tracking des leads, zéro friction | 🤖 |
| 2.2 | **Lead magnet « Guide du pain automatisé »** (PDF 8 pages) : les 5 pains, AVANT/APRÈS, chiffres ROI, méthode 3 étapes | capture email = actif durable | 🤖 (contenu) + 👤 (email) |
| 2.3 | **Quiz « Test de maturité automatisation »** (5 questions → score + reco personnalisée) | lead magnet interactif, qualifie le prospect | 🤖 |
| 2.4 | **CTA WhatsApp direct** (lien wa.me) partout | sa cible vit sur WhatsApp ; la démo devis est sur WhatsApp | 🤖 |
| 2.5 | **Page « Démos »** : les 3 démos vidéo + rapports HTML embarqués | preuve > discours | 🤖 |
| 2.6 | **Page « Méthode »** détaillée (audit 48h → ROI → déploiement → garantie) | réassurance | 🤖 |
| 2.7 | **Intégration n8n dogfood** : formulaire contact → workflow n8n (réponse auto IA + notification + Google Sheets) | le site EST la démo | 🤖 |
| 2.8 | Bandeau CTA après 30 s de visite | conversion visiteurs hésitants | 🤖 |
| 2.9 | Témoignages vrais (remplacer les placeholders dès 2-3 clients) | preuve sociale | 👤 |

**Succès Phase 2** : chaque visiteur a un chemin clair → formulaire/WhatsApp → appel.

---

## PHASE 3 — DISTRIBUTION & CONTENU (semaine 1-4, continu)

| # | Canal | Action | Qui |
|---|---|---|---|
| 3.1 | **LinkedIn** | Publier les 3 vidéos (scripts prêts) : S2 devis, S3 reporting, S4 rapprochement | 👤 (filmer) + 🤖 (posts) |
| 3.2 | **LinkedIn** | 2 posts texte/semaine issus du monitoring hebdo (angles automatiques) | 🤖 (cron → suggestions) |
| 3.3 | **YouTube** | Héberger les démos (30-60 s) → les embarquer dans la page Démos | 👤 (upload) |
| 3.4 | **Google Business Profile** | Créer la fiche (Normandie/remote) → demander des avis → LA page avis devient utile | 👤 |
| 3.5 | **Malt** | Compléter le profil (mots-clés rapport 2026 : n8n, agents IA, automatisation data) + répondre aux missions ciblées | 👤 + 🤖 (aide) |
| 3.6 | **Le site en support** | Chaque post LinkedIn → lien vers la page SEO correspondante | 🤖 |

**Succès Phase 3** : 1 vidéo + 2 posts/semaine, tous reliés au site.

---

## PHASE 4 — NURTURING AUTOMATISÉ (semaine 3-4)

| # | Idée | Pourquoi | Qui |
|---|---|---|---|
| 4.1 | **Séquence email 5 messages** post-lead magnet : pain → solution → démo → offre audit → relance | les curieux deviennent des leads chauds | 🤖 (contenu) + 👤 (outil email) |
| 4.2 | **Automatisation n8n complète (dogfood n°2)** : formulaire → email de bienvenue + PDF → notification Jeremy → suivi dans Sheets → relance J+3 si pas de réponse | le système vend pendant que Jeremy dort (c'est LE pitch LinkedIn) | 🤖 |
| 4.3 | **Newsletter mensuelle** « 1 pain, 1 automatisation, 1 chiffre » | présence durable | 🤖 |
| 4.4 | **Suivi des appels** : template de prise de notes + CRM simple (Sheets ou Airtable) | pipeline visible | 🤖 |

**Succès Phase 4** : aucun lead perdu, relance automatique, pipeline suivi.

---

## PHASE 5 — MESURE & ITÉRATION (continu)

| # | KPI | Source |
|---|---|---|
| 5.1 | Visiteurs/semaine + pages vues | analytics |
| 5.2 | Requêtes Google qui amènent du trafic (top 10) | Search Console → on renforce les pages qui marchent |
| 5.3 | Leads (formulaires + WhatsApp) + taux de conversion | forms/analytics |
| 5.4 | Appels pris / devis envoyés / missions signées | suivi pipeline |
| 5.5 | Nouveaux pains détectés par le monitoring hebdo → nouvelles pages | cron 1137ae0240b6 |

**Règle d'itération** : chaque semaine, 1 nouveau pain → 1 page → 1 post LinkedIn → 1 angle email.

---

## CE QUE J'EXÉCUTE vs CE QU'IL TE FAUT (résumé)
- **🤖 Automatique dès que tu valides** : pages P0/P1/P2, formulaire, quiz, lead magnet (rédaction), CTA WhatsApp, page Démos, intégration n8n dogfood, sitemap/robots/canonical, séquence email (rédaction), plan de posts LinkedIn.
- **👤 Bloqué sur toi** : achat du domaine (~15 €), compte Netlify/Google (5 min), filmer les 3 vidéos, créer la fiche Google Business, upload YouTube, outil d'emailing (MailerLite gratuit ou Brevo), 1er vrai client pour témoignage.

## PROCHAINE ACTION IMMÉDIATE (jour 1)
1. 👤 Tu achètes le domaine (dis-moi lequel, je m'occupe du reste)
2. 🤖 Je construis la page **facturation-electronique-2026.html** (P0, volume max)
3. 🤖 Je prépare le déploiement Netlify (compte à créer par toi, 5 min)
