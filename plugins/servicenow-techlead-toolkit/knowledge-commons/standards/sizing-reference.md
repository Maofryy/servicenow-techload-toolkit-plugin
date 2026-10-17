# Sizing Reference — man-day anchors for ServiceNow work

Reference for the chiffrage-rapide skill. Anchors, not rules: scale up for complexity, down for
OOB-heavy configuration. All values in J/H (jours-homme, man-days). Full-project WBS and
plan de charge live in the dedicated estimation app, not here.

---

## 1. Unit sizing

| Work item | Typical J/H | Notes |
|---|---|---|
| Workshop, half day | 0.5 | per attendee from the delivery team |
| Workshop, full day incl. preparation and minutes | 1.5 | |
| COPIL / COTECH meeting | 0.5 | project manager, add 0.25 for the tech lead when present |
| Catalog item + variable set | 0.5–1 | OOB approval flow included; add for custom UI policies |
| Record producer with mapping | 0.5–1 | |
| Simple business rule or flow step | 0.5–1 | |
| Complex business rule or multi-step flow | 1–3 | approvals, branches, subflows |
| Script include, reusable | 1–2 | class pattern, unit-tested |
| Client script / UI policy set for one form | 0.5–1 | |
| Service Portal widget, simple | 1–2 | display, no server logic |
| Service Portal widget, complex with backend | 3–5 | |
| REST integration, outbound, simple | 1.5–2.5 | one endpoint, static mapping |
| REST integration, complex with mapping | 3–5 | several operations, status mapping, retries, logging |
| Inbound integration (scripted REST or import set + transform) | 2–4 | |
| IntegrationHub spoke configuration | 1–2 | plus licence check |
| Notification set (event, template, conditions) | 0.5 | per 2–3 notifications |
| ACL set for one table | 0.5–1 | record + sensitive fields, roles |
| Custom table with form, list, roles | 1–2 | more if it extends task with SLAs |
| Report / dashboard | 0.5–1 | per dashboard of 4–6 widgets |
| ATF test case | 0.5–1 | per test; a suite for a feature 2–4 |
| Code review, per feature cluster | 0.5–1 | tech lead |
| Update set merge and promotion | 0.5 | per environment hop |
| MEP coordination | 0.5–1 | project manager + tech lead |
| Hypercare day | 0.5 | tech lead + developer, per working day |
| Technical documentation of a feature | 0.5–1 | |

## 2. Overheads that are forgotten in quick estimates

- Tests and fixes: 25–35% of build effort for a feature; more for integrations.
- Specification and design when only a story exists: 15–25% of build.
- Review, promotion, demo: 10% of build.
- Knowledge of the instance: a first delivery on an unknown, customised instance costs 20–40%
  more than the same feature on a clean one.

## 3. Risk coefficient

Apply one coefficient to the raw total and say why.

| Context | Coefficient |
|---|---|
| Well scoped, clean instance, no integration | ×1.10 |
| Typical lot with moderate unknowns | ×1.15 (default) |
| Complex integration or pattern not done before | ×1.25 |
| High unknowns, legacy customisations, first time on this scope | ×1.40 |

## 4. Confidence and how to express it

| Confidence | Meaning | Express as |
|---|---|---|
| High | scope and target known, instance seen | single value or tight range (±15%) |
| Medium | scope clear, details or edge cases missing | range ±25–30% |
| Low | direction only | wide range, name the two or three facts that would narrow it |

## 5. Standard assumptions, exclusions, risks (pick what applies)

Assumptions
- Client product owner available (about 2h a week) to validate; otherwise validation blocks.
- DEV / TEST / PROD access provided before build starts; otherwise +1–2 weeks.
- TEST aligned with PROD (version, plugins); otherwise regression risk after go-live.
- Third-party APIs documented and reachable from design; otherwise ×1.5 on integrations.
- Functional scope frozen after the design workshop; any change is a change order.
- UAT feedback within 5 working days per cycle; otherwise about a week of slip per cycle.

Exclusions
- Historical data migration (separate quote).
- End-user and administrator training (separate package).
- Integrations not documented at kick-off (study then change order).
- Remediation of customisations discovered during build (change order after inventory).
- Support beyond hypercare (maintenance contract).

Risks
- Scope creep: signed scope and change-order process from kick-off.
- Undocumented customisations blocking the build: technical audit before build.
- TEST not representative of PROD: instance conformity check at build start.
- Business stakeholders unavailable in UAT: contractual feedback delay.
