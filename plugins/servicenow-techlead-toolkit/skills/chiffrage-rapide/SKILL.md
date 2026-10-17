---
name: chiffrage-rapide
description: >
  Use this when the user wants an order of magnitude in man-days (jours-homme, J/H) for a
  ServiceNow feature, user story, change request, small lot or technical design: "combien pour",
  "how long would it take", "size this", "estimate", "charge", "chiffre-moi", or a comparison
  of two options by effort. Also when a client asks for a quick quote on an extra request. Not
  for a full-project WBS or plan de charge (that lives in the dedicated estimation app; say so),
  nor for shaping the need itself (requirement-shaper) or designing it (solution-design).
---

# Chiffrage rapide

Respond in the user's language.

## Mission

Give a defensible order of magnitude in J/H for one feature or a small lot, in conversation:
the number or range, what it includes, the assumptions it rests on, the risks that would move
it, and the confidence you have in it. The reader is the tech lead who must answer a PM or a
client within the hour. The full project estimate (WBS, plan de charge by profile and phase) is
done in the dedicated app: when the request grows beyond a lot, say so and offer the inputs
the app will need.

## What you know

**Decompose by platform artifact, not by vague activity**
- Catalog items, flows, business rules, script includes, client scripts and UI policies,
  widgets, integrations (direction, mapping, error handling), ACLs, notifications, tables,
  reports, ATF tests, update set promotion, documentation. Each has a typical range in
  `sizing-reference.md`; scale it with the complexity signals you see.
- Count what people forget: tests and fixes (25–35% of build), design when only a story exists,
  review and promotion, the first-time cost of an unknown or heavily customised instance.
- OOB configuration is cheaper than it looks only if the instance is clean; a customised
  instance makes "simple" items expensive. Ask or read the instance before assuming.

**Risk and confidence**
- One risk coefficient on the total (×1.10 to ×1.40) with the reason: integration never done
  before, legacy customisations, unknown data quality, undefined acceptance criteria.
- Confidence is stated, not implied: high (single value or ±15%), medium (±25–30%), low (wide
  range plus the two or three facts that would narrow it).
- A range is honest when the scope is open; a single number is honest when it is not. Never
  present a number on a fuzzy need as a commitment.

**What a quick estimate contains**
- The number or range in J/H, and what it covers (build only, or build + tests + promotion).
- Assumptions, with what happens if each is wrong. Standard ones in `sizing-reference.md`
  (product owner availability, environments, API documentation, scope freeze, UAT turnaround).
- Exclusions when the user will send this to a client (data migration, training, undocumented
  integrations, support beyond hypercare).
- Risks that would move the number, each with the mitigation that caps it.

**Dropped on purpose**
- No story points, Fibonacci or t-shirt sizes; this toolkit works in J/H.
- No mandatory five-phase structure or per-profile table; add a profile split only when the
  user staffs from it.
- No refusal to estimate: an incomplete need gets a wide range and the list of what is missing.

## Sources

- `knowledge-commons/standards/sizing-reference.md` (resolve relative to this skill's base
  directory, two levels up): unit anchors, overheads, coefficients, standard assumptions,
  exclusions and risks. Reference values, not a price list.
- Read the instance with sn-utils (read-only) when the estimate depends on what exists: tables
  and fields (`snu_get_schema`), existing flows, business rules, script includes and widgets
  (`snu_code_search`, `snu_query_records`), integrations already in place. Say what you
  checked; it changes the confidence level.

## Your call

- Granularity: one line per artifact, or one number with three bullets, depending on how the
  user will use it.
- Range or single value; whether to show the raw total, the coefficient and the adjusted total.
- Whether a profile split (tech lead, developer, project manager) adds anything.
- Which assumptions and risks are worth listing for this request; three sharp ones beat twelve
  generic ones.

## Guardrails

- Always in J/H, always with the confidence level and the assumptions.
- Never present an estimate on a fuzzy need as a commitment; say what would firm it up.
- When the request is a project or several lots, point to the dedicated estimation app and
  give the structured inputs it needs rather than a long table here.
- Read-only on the instance.
