# ServiceNow TechLead Toolkit — Claude Code Plugin Marketplace

A Claude Code plugin marketplace containing the ServiceNow Tech Lead Agent Library — nine specialized skills covering the full delivery lifecycle.

## Install

```bash
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

## Plugins

### servicenow-techlead-toolkit

| Skill | Trigger phrases | Phase |
|---|---|---|
| Requirement Stress-Tester | "stress test this requirement", "review this user story", "find gaps in this requirement" | Phase I — Discovery |
| Solution Architect | "create a TDD", "design the solution for", "OOB vs custom", "flow designer vs business rule" | Phase II — Architecture |
| Estimation Wizard | "estimate this story", "size this requirement", "work breakdown", "point this ticket" | Phase II→III — Estimation |
| Code Coach | "review my code", "code review", "check this script", "peer review" | Phase III — Code Quality |
| Executive Translator | "translate this for the PM", "elevator pitch", "weekly health report" | Phase III — Communication |
| Communication Drafter | "draft a Jira ticket", "email the client about", "reject this requirement" | Cross-Phase — Communication |
| Meeting Scribe | "meeting minutes", "write up the meeting notes", "structure these notes" | Cross-Phase — Documentation |
| Visual Explainer | "make a diagram", "show this visually", "create a flowchart" | Utility |
| HTML Slides Agent | "create a slide deck", "build a presentation", "make slides" | Utility |

## Update

After any change is pushed to this repo, teammates run:

```bash
claude plugins update servicenow-techlead-toolkit
```

## Structure

```
plugins/
  servicenow-techlead-toolkit/
    .claude-plugin/
      plugin.json              # Plugin manifest
    skills/                    # Six skill definitions (SKILL.md per skill)
    knowledge-commons/         # Shared reference files — single source of truth
      standards/               # Technical standards, OOB module index
      templates/               # Gap analysis, TDD, scorecard, output templates
      visual/                  # HTML templates and CSS/JS reference files
        templates/
        references/
```

## Version

0.2.0 — Added Communication Drafter, Meeting Scribe, and Estimation Wizard skills
