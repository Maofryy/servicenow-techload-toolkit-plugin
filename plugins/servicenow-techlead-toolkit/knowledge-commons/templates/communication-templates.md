# Communication Templates

Reusable skeletons for structured communication mediums.
Used by the Communication Drafter skill at runtime. Adapt all fields in [brackets] to context.

---

## Jira Ticket

**Title:** [Imperative verb phrase, max 80 characters: "Add approval step to Change Request workflow". For bugs: "Fix [behaviour] in [context]". For tasks: "Configure [artifact] for [purpose]".]

**Context**
[1–2 sentences. What triggered this work? What is the current state that needs to change?]

**Requirement**
[Plain statement of what this ticket delivers. One paragraph. No jargon.]

**Acceptance Criteria**
Each criterion must be verifiable without ambiguity. Bad: "System handles errors gracefully." Good: "When the API returns a 500, the user sees an error message and the transaction is not saved."
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]
- [ ] [Edge case or error condition]

**Dependencies / Blockers**
[Upstream tickets, decisions, or integrations required before this can start. "None" if none.]

**Story Points:** [1 / 2 / 3 / 5 / 8 / 13]

---

## Email

**Subject:** [Direct, noun-led: "Decision Required: [Topic] by [Date]" or "Update: [Topic]"]

[Name / Team],

[BLUF — one sentence stating the purpose and required action.]

[Body — 1–3 short paragraphs. One point per paragraph. No more.]

[Call to action — explicit: "Please confirm by [Date]." or "No response needed — for your awareness."]

[Closing],
[Name]

---

## Requirement Rejection

[Name / Team],

Thank you for the submission.

**The requirement as stated cannot be implemented as proposed.** [One sentence: the core reason — technical risk, platform constraint, architectural conflict, or scope misalignment. Adjust directness to audience: firm for internal teams, diplomatically framed for client-facing communications.]

**Specifically:** [1–2 sentences describing what would break, what risk it introduces, or why it conflicts with existing architecture or platform standards.]

**Alternative path:** [Concrete proposal — what CAN be done, what needs to change in the requirement, or what pre-condition must be met first.]

**Next step:** [Clear ask — a meeting, a revised requirement, or a specific decision needed.]

[Name]
