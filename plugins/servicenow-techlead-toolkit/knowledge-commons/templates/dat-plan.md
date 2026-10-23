# DAT (Dossier d'Architecture Technique) — Plan type

Checklist of chapters, not a mould. Keep the numbering and the order stable so reviewers find their
way around; adapt the depth to the project. A chapter that does not apply stays in the plan with
"Non applicable — [reason]". Fixed-price lot: size each chapter to the risk, not to symmetry.

| # | Chapter | Purpose | What it must contain | Missing? ask the client |
|---|---|---|---|---|
| 0 | Gestion documentaire *(in the template)* | Trace the document | Versions, author, status, reviewers, distribution | Who validates and when |
| 1 | Synthèse | One page for every reader | Need, chosen solution in 5 lines, key decisions, main risks, decisions awaited | — |
| 2 | Contexte et objectifs | Why this project | Business context, goals, stakeholders, existing landscape, link to the programme | Goals in measurable terms |
| 3 | Périmètre | Frame the design | Included, excluded, assumptions, constraints, dependencies, glossary pointer | Out-of-scope confirmation |
| 4 | Exigences structurantes | What drives the architecture | Only the requirements that shape it, by ID (EF/ENF), with the chapter that answers each | Source requirement list |
| 5 | Architecture globale | The big picture | Context view (system, actors, neighbours), logical view, platform choices (modules, plugins, licences), principles applied | Target landscape, platform release |
| 6 | Architecture applicative | How it is built on the platform | Scopes and applications, tables and `task` extensions, flows / business rules / script includes, UI (portal, workspace), notifications, OOB vs custom deviations with upgrade-risk level | — |
| 7 | Données et CSDM | The data and who owns it | Data model, CSDM alignment (services, offerings, CI classes), reference data, volumes, retention, migration | Volumes, data owners |
| 8 | Intégrations | Every exchange | Per interface: direction, protocol, auth, volume and frequency, real-time or batch, retry, error handling and logging, data owner, MID Server | Neighbour systems, contacts, SLAs |
| 9 | Sécurité | Access and protection | Authentication (SSO, MFA), roles and ACL model, row-level security, data classification, encryption, secrets, audit trail, compliance (RGPD…) | Security policy, classification scheme |
| 10 | Infrastructure et environnements | Where it runs | Instances, MID Servers, network flows, environment chain, promotion strategy (update sets / app repo), test data, ATF | Instance topology, release calendar |
| 11 | Exploitation et supervision | Running it | Monitoring, logs, alerts, backup/restore, upgrades, support model, RACI | Run team, tooling |
| 12 | Exigences non fonctionnelles | Measured qualities | Availability, performance, volumes, RPO/RTO, scalability, retention — each with a figure and how it is met | Target figures |
| 13 | Décisions d'architecture | Why these choices | Summary table of ADRs (decision, options, criteria, consequences, revisit condition); full ADRs in an annex | — |
| 14 | Risques, hypothèses et points ouverts | What is not settled | Risk, severity, mitigation, owner; open decisions with owner and date | — |
| A | Annexes | Detail that would slow the body | Full ADRs, interface sheets, ACL matrix, glossary, **source traceability matrix**, **open questions to the client** | — |

## Platform checklist (chapters 5–11)

- Scope prefix and naming per `standards/technical-standards.md`; no hard-coded sys_ids.
- Every custom table justified (extend an OOB table first; `task` only for units of work).
- Modified OOB artifact → wrapping or extension alternative, upgrade-risk level (`templates/oob-vs-custom-template.md`).
- Licences and IntegrationHub transactions the design consumes are counted.
- Every integration has retry and error logging; silent failure is a defect.
- ACL and role model consistent with `standards/acl-fundamentals.md`.

## Adapting by client or project

A profile (a short note at the top of the working folder) fixes: language, chapters merged or
dropped (with reason), level of detail, client vocabulary, mandatory client sections (e.g. an
architecture-board template), diagram conventions. The rules in `standards/dat-writing-rules.md`
never change with the profile.
