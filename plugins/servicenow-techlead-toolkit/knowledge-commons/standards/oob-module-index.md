# OOB Module Index — Knowledge Commons

A condensed reference of core ServiceNow module capabilities. Consult this before designing a custom solution — the platform likely already does what you need.

---

## ITSM — IT Service Management

### Incident Management
- **Table**: `incident` (extends `task`)
- **Key OOB Features**: Priority matrix (Impact × Urgency), SLA, auto-assignment rules, major incident workflow, parent/child incident linking
- **Notification**: OOB email notifications on state change, assignment, resolution
- **Before You Customise**: Check if `category` / `subcategory` fields + Business Rules can handle routing before creating a custom assignment logic

### Problem Management
- **Table**: `problem` (extends `task`)
- **Key OOB Features**: Root cause analysis workflow, known error (KEDB), link to incidents, problem task (`problem_task`)
- **Note**: Problem state model changed significantly in ITSM v3 (Rome+). Confirm release before designing state flow

### Change Management
- **Table**: `change_request` (extends `task`)
- **Types OOB**: Standard, Normal, Emergency
- **Key OOB Features**: CAB workbench, Conflict Detection, Change Schedule, Risk Assessment calculator, approval policy engine
- **Before You Customise**: Change Approval policies (Policy engine, not Flow Designer) are highly configurable — exhaust these before writing custom approval BRs

### Request / Fulfilment
- **Tables**: `sc_request`, `sc_req_item`, `sc_task`
- **Key OOB Features**: Service Catalog with Record Producers and Order Guides, variable sets, catalog client scripts, fulfilment flow via Flow Designer
- **Rule**: Keep fulfilment logic in Flow Designer, not in Catalog Client Scripts (CSS are for UI behaviour only)

### Knowledge Management
- **Table**: `kb_knowledge`
- **Key OOB Features**: Versioning, feedback, KB blocks, audience targeting, Employee Center integration
- **Tip**: Use `kb_category` and `kb_knowledge_base` effectively before creating custom portal pages

---

## CSM — Customer Service Management

- **Core Tables**: `sn_customerservice_case` (extends `task`), `customer_account`, `consumer`
- **Key Features**: Case lifecycle, customer-facing portal (CSM Portal), SLA per account, entitlements, asset linking
- **Important**: CSM has its own role model (`sn_customerservice.agent`, `.manager`) — do not reuse ITSM roles
- **Playbooks**: CSM supports Playbooks (guided workflows) — evaluate before building custom flows for agent guidance

---

## HRSD — HR Service Delivery

- **Core Tables**: `sn_hr_core_case` (extends `task`), `sn_hr_core_task`
- **Key Features**: HR case confidentiality model (data separation from IT), Center of Excellence routing, Document Management (e-signature integration), Employee Relations
- **Critical**: HR cases have a unique security model — `hr_confidential` is enforced at the ACL level. Never bypass this by copying field values to non-HR tables without a privacy review
- **Employee Center**: Unified portal for HR + IT + Facilities — content blocks, topic pages, and promoted search are configured here, not in Portal Designer

---

## ITOM — IT Operations Management

### Discovery
- Populates CMDB via MID Server probes and sensors
- **Do not** create CMDB records manually for discoverable assets — let Discovery own them
- Use Identification & Reconciliation Engine (IRE) rules, not custom BRs, to deduplicate CIs

### Event Management
- **Table**: `em_event`, alerts → `em_alert`
- Connectors map raw events to ServiceNow alerts via Alert Management rules
- Alerts can auto-create incidents via Alert Management → Incident creation rules — configure here before writing a custom integration

### Service Mapping
- Builds Application Services (maps CIs to business services)
- Pattern-based (agentless) and agent-based options
- Required for accurate impact analysis in Incident

### CMDB
- **Base table**: `cmdb_ci`; every CI type extends this
- CI Class Manager controls hierarchy — do not add fields directly to `cmdb_ci`; extend the appropriate CI class
- Use `cmdb_rel_ci` for relationships, not custom reference fields

---

## SecOps — Security Operations

- **Core Tables**: `sn_si_incident` (Security Incident), `sn_vul_vulnerability_entry`
- **Key Features**: SOAR playbooks, Threat Intelligence, Vulnerability Response (integrates with Qualys, Tenable, etc.)
- **Note**: SecOps has its own SLA and assignment model separate from ITSM — avoid shared Business Rules

---

## App Engine / Custom Applications

- **Platform**: App Engine Studio (AES) for low-code app builders; full platform access for developers
- **Tables**: Prefix with client abbreviation (e.g., `x_acme_vendor_request`)
- **Scoped Apps**: Always develop client customisations in a scoped application — never in the Global scope unless there is a documented technical reason
- **Scope rule**: Scripts in scoped apps cannot access Global scope without explicit API permission — design accordingly

---

## Common Platform Capabilities (Check Before Building Custom)

| Need | OOB Capability | Where to Configure |
|---|---|---|
| Conditional field visibility | UI Policy | Form Designer → UI Policies |
| Field calculation | Calculated Field (on table) or UI Policy | Table config / UI Policy |
| Repeating logic on multiple approvers | Approval activity in Flow Designer | Flow Designer |
| Send email on record change | Notification (Event-based) | System Notification → Notifications |
| Restrict who sees a record | ACL + optionally Query Business Rule | Security → Access Control |
| Route work to correct team | Assignment Rules (for Incident/Case) | Assignment Rules module |
| Enforce data quality | Data Policies (server + client enforced) | Data Policies module |
| Multi-step task checklist | Checklist (on task table) | OOB, enabled per form |
| Scheduled recurring task | Scheduled Job → calls Script Include | System Scheduler |
| Survey / feedback | Survey Management → trigger on state change | Survey module |
| Docgen / PDF output | Document Generation (IntegrationHub) | Flow Designer action |
