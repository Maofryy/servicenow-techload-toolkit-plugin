# Business Value Pitch — Template

Use this template when you need to justify technical investment (refactoring, architecture improvements, tech debt remediation, tooling upgrades) to a non-technical audience. The goal is to make the business case — not explain the technology.

---

## The Core Formula

> "Right now, [the problem costs us X in time/money/risk]. By [the technical work, in plain terms], we will [the specific business outcome]. We estimate this will take [effort/time] and the benefit will be [measurable outcome] over [timeframe]."

---

## Full Template

### The Investment Ask
**What are we proposing?**
[One sentence, plain language — no technical jargon. Think: "We want to rebuild the engine rather than keep replacing the parts."]

**How long will it take?**
[Estimate in days or sprints. Include any dependencies.]

**What does it cost?**
[Developer hours × rate, or story points × sprint cost if the client works that way. Be specific.]

---

### The Current Cost of Inaction
Paint the picture of what "doing nothing" looks like:

- **Time lost**: [e.g., "Service Desk agents currently spend an average of 3 minutes per incident manually copying data between two systems — that's approximately 25 hours of lost time per week across the team."]
- **Risk exposure**: [e.g., "The current approach modifies a system file that ServiceNow owns. Each platform upgrade carries a risk of overwriting our changes, requiring emergency fixes at a premium day rate."]
- **Quality impact**: [e.g., "Customers are experiencing 4-hour delays in case acknowledgment because the routing logic can't handle weekend submissions."]

---

### The Business Outcome
What will be measurably better?

| Metric | Before | After (Projected) | Basis |
|---|---|---|---|
| [e.g., Agent handle time per incident] | [e.g., 8 min avg] | [e.g., 5 min avg] | [e.g., Benchmark from pilot group] |
| [e.g., Upgrade risk incidents per year] | [e.g., 3–4] | [e.g., 0] | [e.g., Elimination of dependency] |
| [e.g., Customer acknowledgment time] | [e.g., 4 hours] | [e.g., < 15 min] | [e.g., Flow Designer auto-ack] |

---

### The Payback Calculation (Optional but powerful)
> "The refactoring will cost approximately [X hours] at [£/$/€ Y per hour] = [total cost].
> At [Z hours saved per week] × [£/$/€ Y per hour], the investment pays back in approximately [N weeks/months]."

---

### Our Recommendation
[One paragraph. State clearly what you recommend, when to do it, and why now — not next quarter.]

> Example: "We recommend addressing this in Sprint 4, before the go-live preparation phase begins. Fixing this now costs 5 days of development. Fixing it after go-live — under production pressure, with live data — typically costs 3–5x more and carries reputational risk with end users."
