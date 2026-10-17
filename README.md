# ServiceNow TechLead Toolkit — Claude Code Plugin Marketplace

A Claude Code plugin marketplace containing the ServiceNow Tech Lead toolkit: ten skills for the ServiceNow delivery lifecycle, from a raw client need to the slide deck that presents it. The skills read the live instance through the **sn-utils** MCP and never write to it unless explicitly asked.

## Install

```bash
claude plugins marketplace add github:Maofryy/servicenow-techload-toolkit-plugin
claude plugins install servicenow-techlead-toolkit@servicenow-techload-toolkit-plugin
```

**Prerequisite:** the [sn-utils](https://www.arnoudkooi.com/) MCP server connected to Claude Code, with the SN Utils helper tab open on the target instance (type `/token` in the ServiceNow tab). Without it the skills still work from what you paste, but they will tell you what they could not verify.

## Skills

| Domain | Skill | Use it when |
|---|---|---|
| Framing and design | `requirement-shaper` | A raw need, mail or rough story has to become a challenged, OOB-first user story with testable criteria, out-of-scope and client questions |
| | `solution-design` | The need is clear and you want the technical answer: build spec, ADR (flow vs BR, extend task or not…) or a DAT section |
| | `csdm-assistant` | Mapping a client's landscape to CSDM objects, auditing the CMDB for CSDM gaps, or building a maturity roadmap by process |
| Estimation | `chiffrage-rapide` | An order of magnitude in J/H for a feature or a small lot, with assumptions, risks and confidence (full WBS lives in the dedicated app) |
| Quality and security | `code-review` | A script, business rule, widget or update set needs a constructive review with corrected code |
| | `security-review` | Who can see, change or trigger what: ACLs, portal, client-callable scripts, REST, integrations, sensitive data |
| | `atf-test-generator` | Turning a story, spec or update set into ATF tests, and spotting criteria that cannot be tested |
| Deliverables | `communication` | Any written deliverable: client or PM mail, Slack, ticket, PR comment, refusal, COPIL update, meeting minutes |
| | `visual-explainer` | A diagram, comparison table, roles grid, timeline or dashboard as a self-contained HTML page |
| | `html-slides` | A slide deck as a self-contained HTML page (PM slides, estimation slides, ELO presets) |

Every skill answers in the user's language, adapts its format to the question, states what it verified on the instance versus what it assumed, and never writes to the instance.

## snow-launcher (experimental mod)

`plugins/snow-launcher/` adds a button bar above the prompt: one click fills `/servicenow-techlead-toolkit:<skill> ` in the input, `/snow` shows or hides the bar. Requires Claude Code ≥ 2.1.287. Validated with `claude plugin validate`, not yet exercised in a live session.

```bash
claude --plugin-dir plugins/snow-launcher
```

## Update

After a change is pushed to this repo:

```bash
claude plugins update servicenow-techlead-toolkit
```

## Structure

```
plugins/
  servicenow-techlead-toolkit/
    .claude-plugin/plugin.json   # Plugin manifest
    skills/                      # Ten skills (SKILL.md per skill)
    knowledge-commons/           # Shared references — used as references, never as moulds
      standards/                 # technical-standards, oob-module-index, acl-fundamentals, sizing-reference
      templates/                 # Design, requirement, review, ACL and communication references
      visual/                    # HTML templates and CSS/JS references for visual-explainer and html-slides
  snow-launcher/                 # Experimental launcher bar mod
```

## Version

1.0.0 — Refonte: ten skills, no imposed formats or blocking gates, instance read through sn-utils, new csdm-assistant and atf-test-generator, snow-launcher mod.

0.7.0 — Added wbs-estimation skill. 0.4.0 — Added acl-logic-architect skill.
