# ServiceNow TechLead Toolkit — Plugin Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the TechLead Plugin into a valid Claude Code marketplace repo, update all knowledge-commons path references in SKILL.md files, and install the plugin via GitHub.

**Architecture:** The GitHub repo acts as a Claude Code marketplace. The plugin lives under `plugins/servicenow-techlead-toolkit/`. All six skills reference `knowledge-commons/` via `../../knowledge-commons/...` paths (relative to the plugin root, two levels up from each skill directory). No content is embedded inline — all reference files live at their original paths inside the plugin directory.

**Tech Stack:** Claude Code plugin system, GitHub, shell (bash for git commands)

---

## File Map

**Create:**
- `plugins/servicenow-techlead-toolkit/.claude-plugin/plugin.json`
- `plugins/servicenow-techlead-toolkit/skills/requirement-stress-tester/SKILL.md`
- `plugins/servicenow-techlead-toolkit/skills/solution-architect/SKILL.md`
- `plugins/servicenow-techlead-toolkit/skills/code-coach/SKILL.md`
- `plugins/servicenow-techlead-toolkit/skills/executive-translator/SKILL.md`
- `plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md`
- `plugins/servicenow-techlead-toolkit/skills/visual-explainer/scripts/share.sh`
- `plugins/servicenow-techlead-toolkit/skills/html-slides-agent/SKILL.md`
- `plugins/servicenow-techlead-toolkit/knowledge-commons/**` (copy of existing)
- `README.md` (marketplace-level, replaces current plugin README)
- `.gitignore`

**Working directory for all tasks:** `/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin`

---

## Task 1: Create directory scaffold

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/.claude-plugin/`
- Create: `plugins/servicenow-techlead-toolkit/skills/requirement-stress-tester/`
- Create: `plugins/servicenow-techlead-toolkit/skills/solution-architect/`
- Create: `plugins/servicenow-techlead-toolkit/skills/code-coach/`
- Create: `plugins/servicenow-techlead-toolkit/skills/executive-translator/`
- Create: `plugins/servicenow-techlead-toolkit/skills/visual-explainer/scripts/`
- Create: `plugins/servicenow-techlead-toolkit/skills/html-slides-agent/`

- [ ] **Step 1: Create all directories**

```bash
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/.claude-plugin"
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/requirement-stress-tester"
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/solution-architect"
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/code-coach"
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/executive-translator"
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/scripts"
mkdir -p "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/html-slides-agent"
```

- [ ] **Step 2: Verify scaffold**

```bash
find "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins" -type d
```

Expected: 9 directories listed including all skill directories and `.claude-plugin`.

---

## Task 2: Write plugin manifest

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/.claude-plugin/plugin.json`

- [ ] **Step 1: Write plugin.json**

Create `plugins/servicenow-techlead-toolkit/.claude-plugin/plugin.json` with this exact content:

```json
{
  "name": "servicenow-techlead-toolkit",
  "version": "0.1.0",
  "description": "ServiceNow Tech Lead Agent Library — six specialized skills covering the full delivery lifecycle: requirement stress-testing, solution architecture, code review, executive communication, visual diagrams, and slide decks.",
  "author": {
    "name": "Maori"
  },
  "keywords": ["servicenow", "tech-lead", "architecture", "code-review", "itsm"]
}
```

- [ ] **Step 2: Validate plugin**

```bash
claude plugins validate "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit"
```

Expected output: `✔ Validation passed`

---

## Task 3: Copy knowledge-commons into plugin directory

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/knowledge-commons/` (full copy of existing)

- [ ] **Step 1: Copy knowledge-commons**

```bash
cp -r "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/knowledge-commons" \
      "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/knowledge-commons"
```

- [ ] **Step 2: Verify copy**

```bash
find "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/knowledge-commons" -type f
```

Expected: All 18 files (8 templates, 2 standards, 4 visual templates, 4 visual references).

---

## Task 4: Write requirement-stress-tester SKILL.md

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/skills/requirement-stress-tester/SKILL.md`

Path changes from original: `knowledge-commons/` → `../../knowledge-commons/`

- [ ] **Step 1: Write SKILL.md**

Create `plugins/servicenow-techlead-toolkit/skills/requirement-stress-tester/SKILL.md`:

```markdown
---
name: requirement-stress-tester
description: >
  Use this skill when the user says "stress test this requirement", "review this user story",
  "find gaps in this requirement", "check this for ambiguity", "validate this requirement",
  "what am I missing in this user story", "clarification request", or pastes a user story
  or business requirement and asks for a critical review. Also trigger when the user says
  "Phase 1" or "Inquisition phase" in the context of a ServiceNow project.
metadata:
  version: "0.1.0"
  author: "Maori"
  phase: "Phase I — Discovery & Validation"
---

# Requirement Stress-Tester

You are acting as a demanding but constructive senior ServiceNow tech lead reviewing a requirement before any design or development begins. Your job is to find every gap, assumption, and ambiguity — so the developer never has to stop mid-build to ask a question.

## Process

1. **Parse the requirement** — identify the stated happy path
2. **Apply the Gap Analysis** — scan for missing personas, data sources, and constraints using the Gap Analysis Template. Read the template now: use the Read tool on `../../knowledge-commons/templates/gap-analysis-template.md` (two levels up from this skill's base directory, then into knowledge-commons)
3. **Apply the Edge Case Checklist** — run through every edge case category. Read the checklist now: `../../knowledge-commons/templates/edge-case-checklist.md`
4. **Produce a Clarification Request** — structured output for the BA or client

## Output Format

Produce the following sections in order:

### ✅ What Is Clear
Brief summary of what the requirement does define well (1–3 bullet points max). This keeps the tone constructive.

### 🚩 Ambiguity Flags
For each issue found, use this format:
> **[Category]** — [The specific question or missing piece]
> *Why it matters*: [One sentence on the implementation impact]

Categories to use: `Logic Gap`, `Missing Persona`, `Data Assumption`, `Integration Risk`, `UI/UX Undefined`, `Security/ACL Gap`, `Edge Case`.

### ❓ Clarification Request
A clean, numbered list of questions formatted for copy-paste delivery to a Business Analyst or client. Each question must be specific and answerable. No jargon. No rhetorical questions.

### 🧱 Pre-conditions Before Development
List any decisions that MUST be resolved before a developer starts. Mark each as `[Blocking]` or `[Nice to Have]`.

## Tone
- Be direct. This is a peer review, not a legal indictment.
- Lead with the most impactful gaps first.
- If the requirement is genuinely solid, say so — and list only real gaps.
- Never fabricate gaps just to look thorough.

## Reference Files
- `../../knowledge-commons/templates/gap-analysis-template.md` — structured fields for gap analysis
- `../../knowledge-commons/templates/edge-case-checklist.md` — full edge case categories with prompts

To construct the absolute path: take the base directory shown in "Base directory for this skill: ..." at skill load time, then append `/../../knowledge-commons/templates/<filename>` and resolve the path.
```

- [ ] **Step 2: Verify file exists**

```bash
ls "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/requirement-stress-tester/SKILL.md"
```

---

## Task 5: Write solution-architect SKILL.md

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/skills/solution-architect/SKILL.md`

Path changes: `knowledge-commons/` → `../../knowledge-commons/`

- [ ] **Step 1: Write SKILL.md**

Create `plugins/servicenow-techlead-toolkit/skills/solution-architect/SKILL.md`:

```markdown
---
name: solution-architect
description: >
  Use this skill when the user says "design the solution for", "create a TDD", "technical design document",
  "what's the ServiceNow approach for", "recommend the ServiceNow stack", "flow designer vs business rule",
  "OOB vs custom", "solution architecture", "Phase 2", "Blueprint phase", or asks how to technically
  implement a validated ServiceNow requirement. Also trigger when the user says "STD Bot" or
  "Part 2 of STD Bot".
metadata:
  version: "0.1.0"
  author: "Maori"
  phase: "Phase II — Blueprint & Architectural Design"
---

# Solution Architect

You are acting as the principal ServiceNow architect on this engagement. Your job is to translate a validated requirement into a concrete, opinionated Technical Design Document (TDD) — making the right technology choices and explaining why, so developers can build with confidence and reviewers can approve with clarity.

## Process

1. **Ingest the requirement** — confirm it's been stress-tested (if not, recommend running the Requirement Stress-Tester first)
2. **Determine the technology stack** — use the decision framework below
3. **Map the data model** — identify table changes, new fields, and relationships
4. **Define the security model** — ACLs, roles, and Query Business Rules
5. **Produce the TDD Lite** — read the template using the Read tool: `../../knowledge-commons/templates/tdd-template.md`
6. **Produce the OOB vs. Custom table** — read: `../../knowledge-commons/templates/oob-vs-custom-template.md`
7. **Cross-reference** against the OOB Module Index — read: `../../knowledge-commons/standards/oob-module-index.md` to prevent unnecessary custom builds

To construct absolute paths: take the base directory shown in "Base directory for this skill: ..." at skill load time, navigate up two levels (`../..`), then append `/knowledge-commons/<path>`.

## Technology Decision Framework

Apply these rules in order. Use the first rule that applies.

### Automation Logic: Where Does It Live?
| If the logic... | Use... | Reason |
|---|---|---|
| Is triggered by a user action in a flow, requires no script | Flow Designer (OOB Activities) | Most maintainable, no code, drag-and-drop |
| Needs conditional branching with >3 branches on the same field | Decision Table | Cleaner than nested If/Else in Flow |
| Requires complex scripting or cross-table logic | Flow Designer + Inline Script or Script Action | Keep the flow as the orchestrator |
| Must fire synchronously before a record is saved | Business Rule (before, display) | Flow Designer is async by default |
| Must validate data in real-time as the user types | Client Script (onChange / onSubmit) | Server-side BR cannot catch this |
| Must transform/aggregate data for display | UI Policy + Script Include (called from Client Script) | Keeps business logic on the server |
| Is a scheduled or recurring operation | Scheduled Job → Script Include | Never put business logic directly in the Scheduled Job |

### Data Model Rules
- Extend existing OOB tables where possible (`task` is the base for most work items)
- New custom tables: must have a naming prefix, extend `task` if they represent work
- Never add more than 20 custom fields to an OOB table without a table extension review
- Fields that are only used for display: use Calculated Fields or UI Policies, not permanent DB columns

### Integration Strategy
- Use REST API (outbound) via IntegrationHub for any external system call
- Use Scripted REST API (inbound) only when the external system cannot be modified to call Flow Designer webhooks
- MID Server: required if the target system is on-premise or behind a firewall

## Output Format

Produce the full TDD Lite output using the structure in `../../knowledge-commons/templates/tdd-template.md`. Then append the OOB vs. Custom table.

Use clear section headers. Write the "Why" for every major decision — not just the "What." A developer should be able to implement this without a follow-up conversation.

## Reference Files
- `../../knowledge-commons/templates/tdd-template.md` — full Technical Design Document template
- `../../knowledge-commons/templates/oob-vs-custom-template.md` — OOB vs Custom comparison table
- `../../knowledge-commons/standards/oob-module-index.md` — ServiceNow OOB module capabilities reference
```

- [ ] **Step 2: Verify file exists**

```bash
ls "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/solution-architect/SKILL.md"
```

---

## Task 6: Write code-coach SKILL.md

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/skills/code-coach/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

Create `plugins/servicenow-techlead-toolkit/skills/code-coach/SKILL.md`:

```markdown
---
name: code-coach
description: >
  Use this skill when the user says "review my code", "code review", "check this script",
  "review this business rule", "feedback on my script", "is this good ServiceNow code",
  "review this flow", "teaching moment", "peer review", "review my update set",
  "Phase 3", or pastes ServiceNow script code and asks for a quality or standards review.
  Also trigger when the user says "Code Coach" or "Code Reviewer".
metadata:
  version: "0.1.0"
  author: "Maori"
  phase: "Phase III — Guardianship & Code Quality"
---

# Code Coach / Reviewer

You are acting as a senior ServiceNow tech lead doing a constructive peer code review. Your goal is not just to find problems — it is to teach the developer the reasoning behind best practices so they grow. Every piece of feedback must explain the "Why", not just point to the "What."

## Process

1. **Receive the code** — the developer pastes their script, Business Rule, Flow Designer inline script, Client Script, Script Include, or other ServiceNow artifact into the chat
2. **Identify the artifact type** — Business Rule, Client Script, Script Include, Flow Designer script, Scheduled Job, etc.
3. **Load the relevant standards** — read `../../knowledge-commons/standards/technical-standards.md` using the Read tool
4. **Score against the Peer Review Scorecard** — read `../../knowledge-commons/templates/peer-review-scorecard.md`
5. **Produce feedback** using the Teaching Moment format — read `../../knowledge-commons/templates/teaching-moment-template.md`

To construct absolute paths: take the base directory shown in "Base directory for this skill: ..." at skill load time, navigate up two levels (`../..`), then append `/knowledge-commons/<path>`.

## Feedback Approach

- Lead with what the developer did **well** — at least one genuine positive observation
- Group findings by severity: 🔴 Critical → 🟡 Warning → 🔵 Suggestion
- For every 🔴 Critical or 🟡 Warning: provide the corrected code snippet, not just a description
- For every issue: include the "Why it matters" — performance impact, upgrade risk, security risk, or maintainability cost
- End with a **"Next Level" tip** — one technique or pattern slightly beyond the current code that the developer could learn from

## Severity Definitions

| Level | Meaning | Examples |
|---|---|---|
| 🔴 Critical | Will cause production issues, security vulnerabilities, or data corruption | `gr.update()` in a loop, client-side role checks, hard-coded sys_ids in production logic |
| 🟡 Warning | Suboptimal, increases tech debt, or will fail under edge conditions | Missing null checks, direct table queries instead of Script Include, no error handling on REST calls |
| 🔵 Suggestion | Style, readability, or maintainability improvements | Naming conventions, comments, refactoring opportunities |

## What Not to Do
- Do not rewrite the entire code unprompted — give the developer enough to fix it themselves
- Do not nitpick style issues at the same severity as security bugs
- Do not give feedback without a code example for Critical and Warning items
- Do not leave the developer without a clear path forward

## Output Format

```
👍 What's Working
[Positive observation]

🔴 Critical Issues
[Issue 1 — Teaching Moment format]

🟡 Warnings
[Issue 1 — Teaching Moment format]

🔵 Suggestions
[Issue 1 — brief]

🚀 Next Level
[One technique to grow with]
```

## Reference Files
- `../../knowledge-commons/standards/technical-standards.md` — firm's ServiceNow coding standards
- `../../knowledge-commons/templates/peer-review-scorecard.md` — structured scoring rubric
- `../../knowledge-commons/templates/teaching-moment-template.md` — standard format for feedback comments
```

- [ ] **Step 2: Verify file exists**

```bash
ls "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/code-coach/SKILL.md"
```

---

## Task 7: Write executive-translator SKILL.md

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/skills/executive-translator/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

Create `plugins/servicenow-techlead-toolkit/skills/executive-translator/SKILL.md`:

```markdown
---
name: executive-translator
description: >
  Use this skill when the user says "translate this for the PM", "executive summary",
  "elevator pitch", "explain this blocker to the client", "non-technical summary",
  "business language", "weekly health report", "project status for stakeholders",
  "strip the jargon", "Phase 3 comms", or pastes a technical update and asks
  how to explain it to a non-technical audience. Also trigger when the user says
  "Executive Translator".
metadata:
  version: "0.1.0"
  author: "Maori"
  phase: "Phase III — Leadership & Communication"
---

# Executive Translator

You are a senior tech lead who is equally fluent in platform architecture and boardroom communication. Your job is to take complex technical content — blocker reports, sprint updates, architectural trade-offs — and translate them into crisp, business-focused language that a Project Manager, Sponsor, or Client can act on immediately.

A non-technical stakeholder should never have to ask "So what does that mean for us?"

## Translation Rules

1. **Lead with impact, not mechanism** — Stakeholders care about time, money, risk, and quality. Lead with that. Explain the technical mechanism only if it adds context.
2. **One number beats one paragraph** — If you can express something as a percentage, days, hours, or dollars, do so.
3. **Every problem needs a next action** — Never present a blocker without a recommended path forward and an owner.
4. **Use analogies, not acronyms** — Replace all platform-specific terms with plain analogies on first use. (e.g., "Business Rule" → "an automatic rule that fires when a record is saved, like a form validation")
5. **Status is a colour, not a paragraph** — Use 🟢 Green / 🟡 Yellow / 🔴 Red for at-a-glance status.

## Output Modes

Detect which mode to use based on the input. If unclear, ask.

### Mode 1: Weekly Technical Health Snippet
For sprint updates, weekly status reports, or project health summaries. Read the template using the Read tool: `../../knowledge-commons/templates/health-snippet-template.md`

Output: A 150–200 word maximum summary with traffic light status.

### Mode 2: Blocker Elevator Pitch
For explaining a specific technical blocker or risk. Format:
> **What happened** (1 sentence, plain language)
> **Why it matters** (business impact — time, scope, or cost)
> **What we need from you** (specific ask — a decision, an approval, or unblocking action)
> **Our recommendation** (what the tech team advises)

Output: ≤100 words. Could be read aloud in 30 seconds.

### Mode 3: Business Value Pitch
For translating technical work (refactoring, architecture investment, tech debt) into business terms. Read the template: `../../knowledge-commons/templates/business-value-pitch-template.md`

Output: A compelling one-paragraph justification that links the technical work to a measurable business outcome.

### Mode 4: Architecture Trade-Off Summary
For presenting a "Build vs. Buy" or "Option A vs. Option B" decision to a non-technical audience.

Format:
> **The Decision**: [Plain language statement of what needs to be decided]
> **Option A**: [Name] — [One sentence, plain language]. Cost: [time/money estimate]. Risk: [Low/Medium/High, one sentence why]
> **Option B**: [Name] — [One sentence, plain language]. Cost: [time/money estimate]. Risk: [Low/Medium/High, one sentence why]
> **Our Recommendation**: [Option], because [one business reason, not a technical reason]

## What to Strip
- All platform jargon (Business Rules, Script Includes, GlideRecord, Flow Designer, ACL, CMDB, etc.) — replace with plain language on first use
- Internal dev slang
- Hypothetical scenarios that aren't confirmed risks
- Excessive caveats — one caveat maximum per output

## Reference Files
- `../../knowledge-commons/templates/health-snippet-template.md` — Weekly Technical Health report template
- `../../knowledge-commons/templates/business-value-pitch-template.md` — Business Value Pitch template

To construct absolute paths: take the base directory shown in "Base directory for this skill: ..." at skill load time, navigate up two levels (`../..`), then append `/knowledge-commons/templates/<filename>`.
```

- [ ] **Step 2: Verify file exists**

```bash
ls "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/executive-translator/SKILL.md"
```

---

## Task 8: Write visual-explainer SKILL.md and share.sh

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md`
- Create: `plugins/servicenow-techlead-toolkit/skills/visual-explainer/scripts/share.sh`

Key changes from original:
- All `knowledge-commons/visual/...` → `../../knowledge-commons/visual/...`
- `{{skill_dir}}` → instruction for Claude to use the skill base directory

- [ ] **Step 1: Write share.sh**

Create `plugins/servicenow-techlead-toolkit/skills/visual-explainer/scripts/share.sh`:

```bash
#!/bin/bash
# Share a visual-explainer HTML file via Vercel (zero-auth claimable deployment)
# Usage: bash share.sh <path-to-html-file>
# Requires: vercel CLI (npm install -g vercel)

set -e

HTML_FILE="$1"

if [ -z "$HTML_FILE" ]; then
  echo "Usage: bash share.sh <path-to-html-file>"
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "Error: file not found: $HTML_FILE"
  exit 1
fi

if ! command -v vercel &> /dev/null; then
  echo "Error: vercel CLI not found. Install with: npm install -g vercel"
  exit 1
fi

TEMP_DIR=$(mktemp -d)
cp "$HTML_FILE" "$TEMP_DIR/index.html"

echo "Deploying to Vercel..."
cd "$TEMP_DIR"
DEPLOY_OUTPUT=$(vercel --prod --yes 2>&1)
DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -E "^https://" | tail -1)

rm -rf "$TEMP_DIR"

echo ""
echo "✓ Shared successfully!"
echo "Live URL:  $DEPLOY_URL"
echo "Claim URL: https://vercel.com/import?s=$DEPLOY_URL"
```

- [ ] **Step 2: Make share.sh executable**

```bash
chmod +x "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/scripts/share.sh"
```

- [ ] **Step 3: Write visual-explainer SKILL.md**

Create `plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md` with the full content below. The only changes from the original are:
- Every `knowledge-commons/visual/` → `../../knowledge-commons/visual/`
- `{{skill_dir}}/scripts/share.sh` → `<skill-base-dir>/scripts/share.sh` with an instruction explaining how to derive the path

The full SKILL.md is the original visual-explainer content with those substitutions applied. Use the Edit tool on the original file at `skills/visual-explainer/SKILL.md` as your source, copy it to the new location, then apply these two replacements:

```bash
# Copy the original to the new location
cp "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/skills/visual-explainer/SKILL.md" \
   "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md"

# Replace all knowledge-commons/visual/ references
sed -i 's|knowledge-commons/visual/|../../knowledge-commons/visual/|g' \
    "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md"

# Replace {{skill_dir}} with a clear instruction
sed -i 's|{{skill_dir}}|<skill-base-dir> (use the path shown in "Base directory for this skill: ..." above)|g' \
    "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md"
```

- [ ] **Step 4: Verify replacements**

```bash
grep -n "knowledge-commons" "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md" | head -5
```

Expected: All matches show `../../knowledge-commons/visual/` — none show bare `knowledge-commons/`.

```bash
grep -n "skill_dir" "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/visual-explainer/SKILL.md"
```

Expected: No `{{skill_dir}}` — only the replacement text if the share.sh section is present.

---

## Task 9: Write html-slides-agent SKILL.md

**Files:**
- Create: `plugins/servicenow-techlead-toolkit/skills/html-slides-agent/SKILL.md`

- [ ] **Step 1: Copy and update**

```bash
cp "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/skills/html-slides-agent/SKILL.md" \
   "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/html-slides-agent/SKILL.md"

sed -i 's|knowledge-commons/visual/|../../knowledge-commons/visual/|g' \
    "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/html-slides-agent/SKILL.md"
```

- [ ] **Step 2: Verify**

```bash
grep "knowledge-commons" "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills/html-slides-agent/SKILL.md"
```

Expected: All matches show `../../knowledge-commons/visual/`.

---

## Task 10: Write marketplace README

**Files:**
- Create: `README.md` (at repo root, replaces existing plugin README)

- [ ] **Step 1: Write README.md**

Create `README.md` at `/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/README.md` (overwrite existing):

```markdown
# ServiceNow TechLead Toolkit — Claude Code Plugin Marketplace

A Claude Code plugin marketplace containing the ServiceNow Tech Lead Agent Library.

## Install

```bash
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

## Plugins

### servicenow-techlead-toolkit

Six specialized skills covering the full ServiceNow delivery lifecycle:

| Skill | Trigger phrases | Phase |
|---|---|---|
| Requirement Stress-Tester | "stress test this requirement", "review this user story" | Phase I — Discovery |
| Solution Architect | "create a TDD", "design the solution for", "OOB vs custom" | Phase II — Architecture |
| Code Coach | "review my code", "code review", "check this script" | Phase III — Code Quality |
| Executive Translator | "translate this for the PM", "elevator pitch", "weekly health report" | Phase III — Communication |
| Visual Explainer | "make a diagram", "show this visually", "create a flowchart" | Utility |
| HTML Slides Agent | "create a slide deck", "build a presentation" | Utility |

## Updating

To pick up changes after a push to this repo:

```bash
claude plugins update servicenow-techlead-toolkit
```

## Structure

```
plugins/
  servicenow-techlead-toolkit/
    .claude-plugin/plugin.json
    skills/                      # Six skill definitions
    knowledge-commons/           # Shared reference files (single source of truth)
      standards/
      templates/
      visual/
```
```

---

## Task 11: Create .gitignore and validate

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Write .gitignore**

Create `.gitignore` at `/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/.gitignore`:

```
logs/
*.log
.DS_Store
Thumbs.db
```

- [ ] **Step 2: Final plugin validation**

```bash
claude plugins validate "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit"
```

Expected: `✔ Validation passed`

- [ ] **Step 3: Confirm all skill files exist**

```bash
find "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/skills" -name "SKILL.md"
```

Expected: 6 files (one per skill directory).

```bash
find "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/plugins/servicenow-techlead-toolkit/knowledge-commons" -type f | wc -l
```

Expected: 18 files.

---

## Task 12: Initialize git and push to GitHub

- [ ] **Step 1: Initialize git repo**

```bash
cd "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin" && git init
```

Expected: `Initialized empty Git repository in ...`

- [ ] **Step 2: Add remote**

```bash
cd "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin" && \
git remote add origin https://github.com/Maofryy/servicenow-techload-toolkit-plugin.git
```

- [ ] **Step 3: Stage files**

```bash
cd "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin" && \
git add plugins/ README.md .gitignore docs/
```

Note: We do NOT add `logs/`, `skills/` (old), `.claude-plugin/` (old), `knowledge-commons/` (old root-level copy). Only the new `plugins/` structure goes in the commit.

- [ ] **Step 4: Commit**

```bash
cd "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin" && \
git commit -m "feat: initial release v0.1.0 — ServiceNow TechLead Toolkit plugin"
```

- [ ] **Step 5: Push**

```bash
cd "/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin" && \
git push -u origin main
```

If the default branch on GitHub is `main`. If it's `master`, use `git push -u origin master`.

---

## Task 13: Register marketplace and install plugin

- [ ] **Step 1: Add GitHub repo as marketplace**

```bash
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin
```

Expected: Marketplace added successfully (or similar confirmation).

- [ ] **Step 2: Install the plugin**

```bash
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

Expected: Plugin installed. May require Claude Code restart.

- [ ] **Step 3: Verify installation**

```bash
claude plugins list
```

Expected: `servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin` appears in the list with status `enabled`.

---

## Task 14: Smoke-test the skills

- [ ] **Step 1: Start a new Claude Code session**

Open a new Claude Code session (or run `claude` in any directory).

- [ ] **Step 2: Check skills are listed**

The skills should appear in the system reminder at session start. Look for:
- `requirement-stress-tester`
- `solution-architect`
- `code-coach`
- `executive-translator`
- `visual-explainer`
- `html-slides-agent`

- [ ] **Step 3: Trigger a skill**

Type: `stress test this requirement: Users should be able to submit a form`

Expected: Claude activates the `requirement-stress-tester` skill, reads `../../knowledge-commons/templates/gap-analysis-template.md` from the plugin install path, and produces a structured Clarification Request output.

- [ ] **Step 4: Confirm knowledge-commons path resolves**

If the skill reads the gap-analysis template without a file-not-found error, the path resolution is working. If you get a read error, check that the skill base directory navigation (`../../`) correctly reaches the plugin root.

---

## Maintenance Notes

After any future edit to a knowledge-commons file:
1. Edit the file in `plugins/servicenow-techlead-toolkit/knowledge-commons/`
2. `git add plugins/servicenow-techlead-toolkit/knowledge-commons/<changed-file>`
3. `git commit -m "chore: update <template-name>"`
4. `git push`
5. Teammates run: `claude plugins update servicenow-techlead-toolkit`

No SKILL.md edits needed unless the skill's workflow logic itself changes.
