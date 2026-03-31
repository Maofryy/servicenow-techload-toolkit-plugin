# Claude Code Plugin Packaging — Design Spec

**Date:** 2026-03-31  
**Author:** Maori  
**Status:** Approved

---

## Goal

Package the ServiceNow TechLead Toolkit as a properly installable Claude Code plugin that:
- Works locally in any Claude Code session after a one-time install
- Can be shared with teammates via a GitHub marketplace link
- Preserves `knowledge-commons/` as a single source of truth for all reference content

---

## Repo

**GitHub:** `https://github.com/Maofryy/servicenow-techload-toolkit-plugin`

The repo acts as a **Claude Code marketplace** — a GitHub repo with a `plugins/` subdirectory that Claude Code's install system can discover and install from.

---

## Directory Structure

```
servicenow-techload-toolkit-plugin/         ← GitHub repo root (marketplace)
  plugins/
    servicenow-techlead-toolkit/            ← the plugin
      .claude-plugin/
        plugin.json                         ← plugin manifest
      skills/
        requirement-stress-tester/
          SKILL.md
        solution-architect/
          SKILL.md
        code-coach/
          SKILL.md
        executive-translator/
          SKILL.md
        visual-explainer/
          SKILL.md
        html-slides-agent/
          SKILL.md
      knowledge-commons/                    ← single source of truth (runtime)
        standards/
          technical-standards.md
          oob-module-index.md
        templates/
          gap-analysis-template.md
          edge-case-checklist.md
          tdd-template.md
          oob-vs-custom-template.md
          peer-review-scorecard.md
          teaching-moment-template.md
          health-snippet-template.md
          business-value-pitch-template.md
        visual/
          templates/
            architecture.html
            data-table.html
            mermaid-flowchart.html
            slide-deck.html
          references/
            css-patterns.md
            libraries.md
            responsive-nav.md
            slide-patterns.md
  README.md
```

The `knowledge-commons/` directory lives **inside** the plugin root (`plugins/servicenow-techlead-toolkit/`). This makes it available at the plugin's install path after `claude plugins install`.

---

## Path Reference Convention

All SKILL.md files reference knowledge-commons files using paths **relative to the plugin root**:

```
../../knowledge-commons/templates/gap-analysis-template.md
../../knowledge-commons/standards/technical-standards.md
../../knowledge-commons/visual/templates/architecture.html
```

When Claude Code loads a skill it provides: `Base directory for this skill: /path/to/plugin/skills/<skill-name>`. Claude navigates two levels up (`../../`) to reach the plugin root and constructs the absolute path for the Read tool.

---

## Skills

Six skills ship with the plugin:

| Skill | Phase | Knowledge-commons deps |
|---|---|---|
| `requirement-stress-tester` | Phase I — Discovery | gap-analysis-template.md, edge-case-checklist.md |
| `solution-architect` | Phase II — Architecture | tdd-template.md, oob-vs-custom-template.md, oob-module-index.md |
| `code-coach` | Phase III — Code Quality | technical-standards.md, peer-review-scorecard.md, teaching-moment-template.md |
| `executive-translator` | Phase III — Communication | health-snippet-template.md, business-value-pitch-template.md |
| `visual-explainer` | Utility | visual/templates/*, visual/references/* |
| `html-slides-agent` | Utility | visual/templates/slide-deck.html, visual/references/* |

No skill embeds content inline. All skills read from `knowledge-commons/` at runtime via the Read tool. Updating a knowledge-commons file immediately affects every skill that references it — no secondary edits needed.

---

## Plugin Manifest

`.claude-plugin/plugin.json`:

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

---

## Installation

**For Maori (local dev + initial setup):**

```bash
# 1. From the Windows source folder, push to GitHub (one-time git setup)
git init
git remote add origin https://github.com/Maofryy/servicenow-techload-toolkit-plugin.git
git add .
git commit -m "Initial release v0.1.0"
git push -u origin main

# 2. Add the GitHub repo as a Claude Code marketplace
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin

# 3. Install the plugin
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

**For teammates:**

```bash
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

---

## Maintenance Workflow

To update a template or standard:

1. Edit the file in `plugins/servicenow-techlead-toolkit/knowledge-commons/`
2. `git commit` and `git push`
3. Teammates run `claude plugins update servicenow-techlead-toolkit`

No changes to SKILL.md files needed unless the skill's workflow logic changes.

---

## Source vs. Deployed

The Windows folder (`/mnt/c/Users/benha/Documents/Work/Claude Skills/TechLead Plugin/`) is the **development source**. The `plugins/servicenow-techlead-toolkit/` subfolder within the GitHub repo is the **deployable plugin**. The top-level `knowledge-commons/` in the Windows folder (outside `plugins/`) can be kept or removed — it is no longer the runtime source.

---

## What Changes From Current State

| Item | Current | After |
|---|---|---|
| Repo structure | Flat (plugin at root of Windows folder) | Nested under `plugins/servicenow-techlead-toolkit/` |
| knowledge-commons location | Outside plugin dir | Inside plugin dir |
| Path references in SKILL.md | `knowledge-commons/...` | `../../knowledge-commons/...` |
| Plugin registration | Not in installed_plugins.json | Installed via `claude plugins install` |
| Teammate install | Manual copy | One-liner CLI command |
