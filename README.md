# ServiceNow TechLead Toolkit — Claude Code Plugin Marketplace

A Claude Code plugin marketplace containing the ServiceNow Tech Lead Agent Library — ten specialized skills covering the full delivery lifecycle.

## Install

```bash
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

## Delivery Pipeline

```
  RAW NEED / ROUGH STORY
         │
         ▼
┌─────────────────────┐
│   Design Challenger  │  "Shape it" — OOB-first challenge,
│   (Phase 0 / II-A)  │   challenged user story + TDD skeleton
└─────────┬───────────┘
          │                         ┌────────────────────────┐
          ▼              gaps ◄─────┤  Requirement            │
┌─────────────────────┐             │  Stress-Tester          │
│  Requirement         │────────────►  (Phase I)              │
│  Stress-Tester       │  7+/10     │  "Certify it" — DoR     │
│  (Phase I)           │            │   score + gap list      │
└─────────┬────────────┘            └────────────────────────┘
          │ certified (7+/10)
          ▼
┌─────────────────────┐
│  Platform Blueprint  │  "Specify it" — full TDD,
│    (Phase II-B)      │   exact artifacts, build sequence
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Estimation Wizard   │  Story points, work breakdown,
│   (Phase II→III)     │   dependencies, risk flags
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│     Code Coach       │  Per-PR code review, severity-based
│     (Phase III)      │  feedback, best practices enforcement
└─────────────────────┘

         ──── Communication (Cross-Phase) ────
    Executive Translator │ Communication Drafter
    Meeting Scribe

         ──── Utility (any phase) ────────────
         Visual Explainer │ HTML Slides Agent
```

## Plugins

### servicenow-techlead-toolkit

| Skill | Trigger phrases | Phase |
|---|---|---|
| Design Challenger | "architect this", "how should we build this in ServiceNow", "challenge this requirement", "rough need into a story" | Phase 0/II-A — Design Challenging |
| Requirement Stress-Tester | "stress test this requirement", "review this user story", "find gaps in this requirement" | Phase I — Discovery |
| Platform Blueprint | "blueprint this", "what configuration is needed", "implementation spec", "what do I need to build" | Phase II-B — Platform Blueprint |
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
    skills/                    # Ten skill definitions (SKILL.md per skill)
    knowledge-commons/         # Shared reference files — single source of truth
      standards/               # Technical standards, OOB module index
      templates/               # Gap analysis, TDD, scorecard, output templates
      visual/                  # HTML templates and CSS/JS reference files
        templates/
        references/
```

## Version

0.3.0 — Replaced solution-architect with design-challenger and platform-blueprint for sharper phase ownership
