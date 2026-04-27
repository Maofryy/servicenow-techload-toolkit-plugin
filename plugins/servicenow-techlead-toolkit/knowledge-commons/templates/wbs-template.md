# WBS — PLAN DE CHARGE : [NOM DU PROJET]

Standard output template for the WBS Estimation skill.
Used for full-project man-day planning across the 5 ServiceNow delivery phases.

---

```
WBS & PLAN DE CHARGE — PROJET SERVICENOW

Projet  :  [Nom du projet]
Client  :  [Nom du client]
Desc    :  [Description courte]
Date    :  [Date d'estimation]
Version :  v1.0
Statut  :  En cours de planification
```

---

## NIVEAU DE CONFIANCE : XX%

**Ce qui est bien défini :**
- [élément clairement spécifié]
- ...

**Ce qui est ambigu ou manquant :**
- [élément flou + impact sur l'estimation]
- ...

**Hypothèses structurantes posées pour ce chiffrage :**
- [hypothèse — impact si fausse]
- ...

> ⚠️ *(Include this warning only if confidence < 50%)*
> Les estimations ci-dessous ont une marge d'erreur élevée (±40% ou plus).
> Il est recommandé de tenir un atelier de cadrage avant de communiquer ces chiffres au client.

---

## RÉSUMÉ DES CHARGES

Coefficient de risque appliqué : ×[X.XX] — [justification en une phrase]

| Profil           | J/H bruts | Coeff  | Charge ajustée |
|------------------|-----------|--------|----------------|
| Chef de projet   | X         | ×X.XX  | X              |
| Architecte       | X         | ×X.XX  | X              |
| Tech Lead        | X         | ×X.XX  | X              |
| MOA              | X         | ×X.XX  | X              |
| Consultant       | X         | ×X.XX  | X              |
| **TOTAL**        | **X**     |        | **X**          |

---

## PHASE 0 — GESTION DE PROJET

| N° WBS | Tâche | Chef de projet | Architecte | Tech Lead | MOA | Consultant | Total J/H |
|--------|-------|---------------|------------|-----------|-----|------------|-----------|
| 0.1    | Kick-off & Initialisation projet          | X | — | — | — | — | X |
| 0.2    | Réunions COPIL / COTECH                   | X | — | — | — | — | X |
| 0.3    | Gestion des risques & aléas               | X | — | — | — | — | X |
| 0.4    | Rédaction & validation du cahier de recette | X | — | — | X | — | X |
| 0.5    | Rédaction des comptes-rendus et livrables | X | — | — | — | — | X |
| 0.6    | Clôture projet                            | X | — | X | — | — | X |

**Sous-total Phase 0** : X J/H bruts → **X J/H ajustés** (×X.XX)

---

## PHASE 1 — CADRAGE & ATELIERS

| N° WBS | Tâche | Chef de projet | Architecte | Tech Lead | MOA | Consultant | Total J/H |
|--------|-------|---------------|------------|-----------|-----|------------|-----------|
| 1.1    | Ateliers de recueil du besoin             | X | X | — | X | — | X |
| 1.2    | Rédaction des spécifications & user stories | — | — | X | X | — | X |
| 1.3    | Audit de l'instance existante             | — | X | X | — | — | X |
| 1.4    | Validation fonctionnelle du périmètre     | X | — | — | X | — | X |
| [1.X]  | [Tâche spécifique au projet]              | — | — | — | — | — | X |

**Sous-total Phase 1** : X J/H bruts → **X J/H ajustés** (×X.XX)

---

## PHASE 2 — CONCEPTION

| N° WBS | Tâche | Chef de projet | Architecte | Tech Lead | MOA | Consultant | Total J/H |
|--------|-------|---------------|------------|-----------|-----|------------|-----------|
| 2.1    | Architecture technique & choix de configuration | — | X | X | — | — | X |
| 2.2    | Design UX / Maquettes Service Portal      | — | — | X | X | — | X |
| 2.3    | Conception des intégrations (API / Spokes) | — | X | X | — | — | X |
| 2.4    | Documentation technique d'architecture    | — | X | X | — | — | X |
| [2.X]  | [Tâche spécifique au projet]              | — | — | — | — | — | X |

**Sous-total Phase 2** : X J/H bruts → **X J/H ajustés** (×X.XX)

---

## PHASE 3 — IMPLÉMENTATION (BUILD)

| N° WBS | Tâche | Chef de projet | Architecte | Tech Lead | MOA | Consultant | Total J/H |
|--------|-------|---------------|------------|-----------|-----|------------|-----------|
| 3.1    | Configuration tables & data schema        | — | X | X | — | X | X |
| 3.2    | Logique métier (Business Rules / Flow Designer) | — | — | X | — | X | X |
| 3.3    | Intégrations & API tierces                | — | X | X | — | X | X |
| 3.4    | Service Portal & widgets                  | — | — | X | — | X | X |
| 3.5    | Gestion & promotion des Update Sets       | — | — | X | — | X | X |
| 3.6    | Tests unitaires développeur               | — | — | — | — | X | X |
| 3.7    | Revue technique / peer review Tech Lead   | — | — | X | — | — | X |
| 3.8    | Qualification interne (avant livraison client) | — | — | X | — | X | X |
| [3.X]  | [Fonctionnalité spécifique au projet]     | — | — | — | — | X | X |

**Sous-total Phase 3** : X J/H bruts → **X J/H ajustés** (×X.XX)

---

## PHASE 4 — RECETTE & DÉPLOIEMENT

| N° WBS | Tâche | Chef de projet | Architecte | Tech Lead | MOA | Consultant | Total J/H |
|--------|-------|---------------|------------|-----------|-----|------------|-----------|
| 4.1    | Tests de Non-Régression (TNR)             | — | — | X | X | X | X |
| 4.2    | Corrections post-UAT                      | — | — | X | — | X | X |
| 4.3    | Mise en Production (MEP)                  | X | — | X | — | X | X |
| 4.4    | Hypercare post Go-Live                    | X | — | X | — | X | X |
| 4.5    | Support de maintenance initial (Xj)       | — | — | X | — | X | X |

**Sous-total Phase 4** : X J/H bruts → **X J/H ajustés** (×X.XX)

---

## HYPOTHÈSES DE CHIFFRAGE

| #   | Hypothèse | Catégorie | Statut | Impact si non respectée |
|-----|-----------|-----------|--------|------------------------|
| H1  | [Hypothèse] | [Catégorie] | À valider | [Impact] |
| H2  | ... | ... | ... | ... |

## EXCLUSIONS DE PÉRIMÈTRE

| #   | Exclusion | Motif | Statut | Alternative proposée |
|-----|-----------|-------|--------|---------------------|
| E1  | [Exclusion] | [Motif] | À valider | [Alternative] |
| E2  | ... | ... | ... | ... |

## RISQUES

| #   | Risque | Probabilité | Impact | Plan de mitigation |
|-----|--------|-------------|--------|-------------------|
| R1  | [Risque] | Moyenne | Élevé | [Mitigation] |
| R2  | ... | ... | ... | ... |

---

*WBS généré par le ServiceNow TechLead Toolkit — wbs-estimation v0.1.0*
