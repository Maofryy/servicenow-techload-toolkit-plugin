---
name: dat-writer
description: >
  Use this when the user wants to write, restructure or review a DAT (Dossier d'Architecture
  Technique / technical architecture document) for a client project: turning context material
  (requirements, meeting notes, schemas, exports, a solution-design output, an existing draft)
  into an ELO-branded .docx that follows DAT conventions, adapted to the client or project.
  Trigger on "DAT", "dossier d'architecture", "document d'architecture technique", "architecture
  document for the client". Not for a single decision (solution-design ADR), a build spec for
  developers (solution-design) or a slide deck (html-slides).
---

# DAT Writer

Respond in the user's language; the DAT itself is written in the client's language (French by
default).

## Mission

Turn the project's context material into a DAT that an architecture board can validate: the
right chapters in a stable order, claims traced to sources, gaps surfaced as questions, and a
finished ELO-branded `.docx` (cover, document control, table of contents, confidentiality footer).

## What you know

- The plan and the writing rules are in `knowledge-commons/` (two levels up from this skill's
  base directory): `templates/dat-plan.md` and `standards/dat-writing-rules.md`. Read both
  before drafting; they are the quality bar, adapted per project.
- The platform references are read when the chapter needs them, not up front:
  `standards/technical-standards.md` (naming, ch. 6), `templates/oob-vs-custom-template.md`
  (deviations, ch. 6), `standards/acl-fundamentals.md` (ch. 9), `templates/tdd-template.md`
  (only when the DAT must mirror a TDD).
- A statement is *constaté* (source or instance), *hypothèse* or *décision*. Constaté is the
  default and stays unmarked; hypotheses and decisions are always marked. A gap is a question
  for the client or an open point, never filled by invention.
- Individual design decisions belong in ADRs (use the `solution-design` ADR shape) with a
  summary table in the DAT.
- The working folder is the current directory. `dat.md` is the source of truth, `figures/`
  holds the rendered diagrams, the `.docx` is a build output. A new version edits `dat.md`
  and rebuilds; it never starts from the `.docx`. If `dat.md` already exists here, read it
  first: the request is probably a revision.

## How to work

1. **Collect.** Get the paths of the context material and any existing draft or client template.
   Office and PDF sources are converted to text first (the docx, pptx, xlsx and pdf skills).
   Read requirements, decisions and drafts in full; for a large corpus or bulky exports, have
   a cheaper subagent produce a one-page fact sheet per source with citations, and say so.
   If a client template or an existing DAT plan is provided, it wins over the default plan for
   structure; the writing rules still apply.
2. **Fix the profile.** Defaults: client and project name from the sources, French, the full
   plan with non-applicable chapters kept, depth per risk. Ask only when a default would
   produce the wrong document (language, a client template, chapters to merge or drop), at
   most three questions in one round.
3. **Map sources to chapters.** Build the traceability list (source → chapter) and the list of
   gaps. Show it to the user in a few lines before the full draft when the gaps are large.
4. **Verify on the instance when one is reachable** (sn-utils, read-only): scopes, tables,
   flows, integrations, roles, plugins. No instance, or the helper tab is closed: say it once,
   do not retry, and treat every claim about the current state as a hypothesis.
5. **Draft `dat.md`** in the current directory, chapter by chapter, from the plan; numbered
   headings (`# 1. …`), tables for enumerable content, `>` callouts for hypotheses and open
   points. End with the annexes: ADRs, traceability matrix, open questions to the client.
6. **Diagrams in Mermaid, inside the Markdown.** One view, one block, caption on the fence:
   ```` ```mermaid Figure 1 – Vue de contexte ````. Type by view: `flowchart` with `subgraph`
   for the context, logical and deployment views (no C4, its layout is unreliable),
   `sequenceDiagram` for an integration, `erDiagram` for the data model. Read `references/mermaid-views.md`
   before the first diagram: it holds the rules (labelled edges, stable names, no styling,
   one page per figure) and four skeletons that render. The build applies the ELO theme to
   every figure, so the diagram carries no colours. A user-supplied image goes in as
   `![Figure N – title](file.png)`. A diagram that fails to render or a missing image becomes
   a "Figure à insérer" callout automatically; read the build warnings and fix the Mermaid
   rather than ship the callout.
7. **Build the document** in the current directory:
   ```bash
   uv run <skill dir>/assets/build_dat.py dat.md DAT-<client>-<project>-v0.1.docx \
     --title "<project>" --client "<client>" --version 0.1 --status Brouillon --author Maori
   ```
   It fills `assets/ELO-DAT-Template.docx` (Century Gothic, ELO blues, ELO and ServiceNow logos,
   "© 2026 ELO. Confidential." footer) and writes the figures to `figures/`. For a revision,
   bump `--version`, describe it in `--changes`, and pass each earlier version as
   `--previous "0.1;2026-10-01;Maori;Relu;Première version"` so the document-control table
   keeps the history. Open the result. The table of contents is built by Word on opening
   (accept the field update); Pages and LibreOffice show it empty.
8. **Review before handing over:** run the checklist below and report what is left open.

## Review checklist

An item is satisfied either by sourced content or by an explicit open point; a plausible filler
satisfies nothing.

- Plan order respected, non-applicable chapters kept with a reason.
- Every requirement cited by ID is answered in a chapter or listed as a deviation or risk.
- Each interface has direction, protocol, auth, retry, error handling, owner; each missing
  cell says "à confirmer" and appears in the open questions.
- Security and non-functional chapters carry figures and named mechanisms, or the figure is an
  open point with the question to ask.
- Hypotheses marked; open points have an owner and a date, or "à attribuer" when the client
  has not named one; every figure, name and date in the text has a source in the annex.
- Each ADR lists real rejected options and a revisit condition.
- Each diagram has a caption, labelled edges and an explaining paragraph.
- Wording: short active sentences, defined acronyms, ServiceNow terms in English.

## Your call

- How much to ask before writing: one short round if the profile is unclear, otherwise start.
- Chapter depth per risk; a small lot gets a short DAT, not a ten-chapter one with empty sections.
- Whether to produce the whole document or the chapters the user asked for; a single chapter
  does not need the platform references of the others.

## Guardrails

- Never invent a figure, a name, a date or an architecture fact; ask or mark it open. An open
  point is always an acceptable answer to the review checklist; a guess never is.
- Read-only on the instance.
- Do not restyle the template (colours, fonts, logos); the branding comes from the template. The
  ServiceNow logo is a partner reference on the cover only; confirm wording with partner
  guidelines before external use.
- `assets/make_template.py` regenerates the template if the ELO charter changes.
