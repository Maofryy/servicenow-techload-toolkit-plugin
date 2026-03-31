# Peer Review Scorecard

Use this rubric to score a submitted script or artifact. Each section is scored 1–5. A merged artifact should score ≥4 in all sections, or have documented exceptions for anything below.

---

## Scoring Guide

| Score | Meaning |
|---|---|
| 5 — Excellent | Exceeds standards; could serve as a reference example |
| 4 — Good | Meets all standards; minor improvements possible |
| 3 — Acceptable | Meets minimum bar; specific improvements recommended |
| 2 — Needs Work | Has issues that must be addressed before merge |
| 1 — Blocked | Has critical issues; cannot merge in current state |

---

## Section 1: Performance

**Questions to ask:**
- Are there any queries inside loops?
- Is `GlideAggregate` used for counts?
- Are there unnecessary Display Business Rules with embedded queries?
- Could a large result set cause memory issues? Is a limit applied?
- Is the script scoped to run only when necessary (Business Rule condition is specific)?

**Score**: /5
**Notes**:

---

## Section 2: Reliability & Error Handling

**Questions to ask:**
- Are all external API calls wrapped in try/catch?
- Are null/empty reference fields checked before chaining?
- Is the failure mode defined (fallback state, error log, notification)?
- Would this script behave differently on an inactive user, missing manager, or empty field?

**Score**: /5
**Notes**:

---

## Section 3: Security

**Questions to ask:**
- Are role checks performed server-side (not client-side)?
- Are no hard-coded sys_ids present?
- Is any user-supplied input sanitised before use in a GlideRecord query?
- Could this script be exploited by a non-privileged user to access data they should not see?
- Does it touch PII, and if so, is that access justified and logged?

**Score**: /5
**Notes**:

---

## Section 4: Readability & Standards

**Questions to ask:**
- Does the naming follow the firm's convention (u_ prefix, PascalCase SI, etc.)?
- Are functions and variables named to convey intent?
- Is there a comment explaining **why** (not just what) for non-obvious logic?
- Does the Script Include use the class pattern?
- Is the code DRY — or is business logic duplicated across multiple artifacts?

**Score**: /5
**Notes**:

---

## Section 5: Upgradeability & Maintainability

**Questions to ask:**
- Does the script touch any OOB/protected objects that could be overwritten on upgrade?
- Are there hard-coded values that will require code changes for a different client or environment?
- Are system properties used for configurable values?
- Is there an ATF test? Does it cover edge cases?
- Could a future admin (with platform knowledge but not this project's context) understand and modify this?

**Score**: /5
**Notes**:

---

## Overall Assessment

| Section | Score |
|---|---|
| Performance | /5 |
| Reliability & Error Handling | /5 |
| Security | /5 |
| Readability & Standards | /5 |
| Upgradeability & Maintainability | /5 |
| **Total** | **/25** |

**Decision**: ☐ Approved ☐ Approved with Minor Comments ☐ Requires Changes ☐ Blocked

**Summary for Developer**:
