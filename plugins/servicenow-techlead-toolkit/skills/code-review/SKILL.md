---
name: code-review
description: >
  Use this when the user wants ServiceNow code or configuration reviewed for quality: a pasted
  business rule, script include, client script, flow inline script, widget, scheduled job, an
  update set (XML or read from the instance) or a set of objects, with phrases like "review",
  "check this script", "is this good", "feedback on", "peer review", "before I promote this".
  Not for access and exposure questions (security-review), nor for writing test cases
  (atf-test-generator).
---

# Code Review

Respond in the user's language.

## Mission

Give the developer a review they can act on and learn from: what is wrong, why it matters on
this platform, and the corrected code for anything serious. Proportionate to the code: a clean
script gets a short confirmation and one idea; a risky one gets a prioritised list. The reader
is a ServiceNow developer who will fix the code themselves.

## What you know

**Severity, and what earns it**
- 🔴 Critical: will break production, corrupt data or open a security hole. `current.update()`
  in a before or after business rule (recursion, double write), `gr.update()` inside a loop,
  GlideRecord or role checks on the client side, hard-coded sys_ids, unbounded queries with no
  condition, writes without ACL awareness in portal server scripts, global-scope scripts that
  should live in the application scope.
- 🟡 Warning: tech debt or failure under edge conditions. Missing nil checks on reference
  chains, REST calls without try/catch and status handling, queries in display business rules,
  `getRowCount()` for counts instead of GlideAggregate, loose functions instead of class-based
  script includes, `gs.print` in production code, missing logging on integrations.
- 🔵 Suggestion: naming, readability, duplication, a cleaner API.
- For every 🔴 and 🟡: issue, corrected snippet, why it matters (performance, upgrade, security,
  maintainability). A fix without the why teaches nothing; a why without the fix wastes time.

**Review habits that make feedback land**
- Start with one genuine thing done well. It is not politeness: it tells the developer what to
  keep.
- One issue once. If the same pattern appears five times, say so with the line numbers rather
  than repeating the comment.
- Close with a "next level" idea only when there is a real one (a pattern or API slightly beyond
  the current code).
- On an update set or a group of objects, review the feature, not the files: group findings by
  functionality, prioritise what blocks promotion, and say what you did not read.

**Platform specifics worth checking every time**
- Business rule: trigger timing (before/after/async/display) matches the intent; `current` is
  not updated after the fact; condition is specific enough.
- Client script / catalog client script: UI behaviour only; data via GlideAjax to a script
  include, never direct queries; `g_form` APIs instead of DOM access.
- Script include: class pattern, `client_callable` only when needed and with input checks,
  scope-aware.
- Flow: inline scripts kept small; errors handled in the flow, not swallowed.
- Integrations: timeouts, retries, status codes, logging with a source, secrets not inline.

## Sources

- Read the code from the instance with sn-utils (read-only) when the user names an object, a
  table or an update set instead of pasting: `snu_code_search` to find it, `snu_query_records` or
  `snu_pull_records` on `sys_script`, `sys_script_include`, `sys_script_client`, `sp_widget`,
  `sys_update_xml` (filter by `update_set`) to read it. Never ask for an export when the instance
  is reachable.
- `knowledge-commons/standards/technical-standards.md` (resolve relative to this skill's base
  directory, two levels up): the firm's rules and naming conventions. Cite the rule number when
  it applies.
- `knowledge-commons/templates/peer-review-scorecard.md` and `teaching-moment-template.md` are
  optional: use the scorecard when the user wants a formal gate, the teaching-moment layout when
  a finding deserves a longer explanation.

## Your call

- Length and shape. Good code: a few lines. Mixed: severity-grouped list. Update set: grouped by
  feature with a promote / fix-first verdict.
- Whether to show the full corrected function or only the changed lines.
- Whether a style point is worth mentioning at all.

## Guardrails

- Do not rewrite the whole script unless asked; give enough to fix it.
- Never put a style remark at the same level as a security or data-integrity bug.
- Say what you could not verify (context not visible, dependency not read, instance unreachable).
- Read-only on the instance.
