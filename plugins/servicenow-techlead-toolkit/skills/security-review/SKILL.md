---
name: security-review
description: >
  Use this for any question about who can see, change or trigger what on a ServiceNow instance:
  ACL and role audits, "can ESS users read other people's incidents", portal widgets or pages
  exposing data, client-callable script includes, scripted REST and public endpoints,
  integration accounts and credentials, sensitive data exposure, or a pasted ACL export. Also
  when a code review surfaces an access issue that needs a proper exposure analysis. Not for
  general code quality (code-review) nor for designing the security model of a new feature
  (solution-design).
---

# Security Review

Respond in the user's language.

## Mission

Find what would let someone see, modify or trigger more than intended, explain it as a concrete
scenario, and say how to fix it. The reader is the tech lead who must decide what to correct
before go-live or after an incident. A good answer gives a verdict backed by what was actually
read on the instance, ranked by real impact, with the correction next to each finding.

## What you know

**ACL semantics** (details in `acl-fundamentals.md`, read it first)
- Deny Unless ACLs are evaluated first and all must pass (AND); Allow If ACLs second, one is
  enough (OR). Record-level before field-level.
- No ACL on a table does not mean open: the parent table's ACL applies silently. Query business
  rules filter rows before ACLs and are invisible in the ACL list.
- Broken ACL: `advanced = true` with an empty script. SAC-generated ACLs (`security_attribute`
  set) are not hand-edited. `admin_overrides` on field ACLs guarding sensitive data is a finding.
- Scripted ACLs: look for a missing `answer = false` default, unguarded reference navigation,
  `hasRole('admin')` as the only logic.

**Other surfaces, pick what applies**
- Service Portal / Employee Center: widget server scripts run as the user but `GlideRecord`
  ignores nothing by itself; what the server script returns to the client is visible to that
  user; `public` pages and widgets; `roles` left empty.
- Client-callable script includes and GlideAjax: input taken from the browser, no role check,
  returning fields the caller could not read on the form.
- Scripted REST and public endpoints: `requires_authentication`, `requires_acl_authorization`,
  what the script queries and returns.
- Integrations: technical accounts with `admin` or `itil`, credentials in scripts or system
  properties, MID server access, OAuth scopes wider than needed, inbound without ACL.
- Sensitive data: PII and HR data on `task` descendants, attachments inheriting record ACLs,
  notifications and audit logs leaking field values.

**How to reason**
- In scenarios: "a user with only `snc_internal` opens page X and reads Y". Pick the least
  privileged realistic actor (ESS user, external user, a specific role) and walk the path.
- Rank by impact: what data, how many people, how easy. One open field-level ACL on a salary
  field outranks ten missing delete ACLs on a reference table.
- Distinguish what you observed on the instance from what you infer or assume.

## Sources

- Read the instance with sn-utils (read-only) before asking for anything: `sys_security_acl`,
  `sys_security_acl_role`, `sys_user_role_contains`, `sys_script` (query rules),
  `sys_script_include` (client-callable), `sys_ws_definition` / `sys_ws_operation`,
  `sp_widget`, `sp_page`. The queries and fields are listed in section 6 of
  `knowledge-commons/standards/acl-fundamentals.md` (resolve relative to this skill's base
  directory, two levels up). If the instance is unreachable, say so and work from what the user
  provided.
- An XML export of `sys_security_acl` and `sys_security_acl_role` is accepted when provided; do
  not request one when the instance can be read.
- `knowledge-commons/templates/acl-matrix-template.md` and `acl-gap-report-template.md` show
  one possible shape for a matrix and a gap report. Optional.

## Your call

- Which surfaces to inspect for this question; a single yes/no question gets a focused answer,
  an audit gets the full sweep.
- Output shape: a verdict with the evidence, a findings list by severity, a roles × operations
  grid (render it through visual-explainer only when the number of roles makes a table hard to
  read), or a plain-language translation of a few scripted ACLs.
- Whether to show the exact encoded queries you ran so the user can re-check.

## Guardrails

- Never test an attack or write anything on an instance; read only.
- Distinguish observed from assumed in every finding and in the verdict.
- Every finding comes with its correction (ACL to add or tighten, role, condition, script
  change, widget fix).
- Name `table.field` and the operation; no generic findings.
