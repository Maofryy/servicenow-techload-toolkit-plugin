# Gap Analysis Template

Use this template when running a requirement through the stress-tester. Work through each section systematically before producing the Clarification Request.

---

## 1. Proposed User Story (Restate)
Restate the requirement in standard form:
> **As a** [Persona], **I want to** [Action], **so that** [Business Outcome].

Check: Can you fill this in completely from the provided requirement? If any field is blank or assumed, flag it.

---

## 2. Persona Validation

| Persona Role | Named in Requirement? | Questions to Ask |
|---|---|---|
| Requester | ☐ Yes / ☐ No | Who initiates this? Can it be a third party (vendor, customer)? |
| Approver | ☐ Yes / ☐ No | Who approves? What if the approver is OOO or has no manager? |
| Fulfiller / Assignee | ☐ Yes / ☐ No | Which group owns fulfilment? Is auto-assignment expected? |
| Watcher / Stakeholder | ☐ Yes / ☐ No | Who needs notifications but no action? |
| Admin / Override | ☐ Yes / ☐ No | Is there a manual override role for edge situations? |

---

## 3. Data Source Validation

- What tables are involved? Are they OOB or custom?
- Is there an integration or API call? What happens if it times out or returns an error?
- Are reference fields assumed to always be populated? (e.g., requested_for.manager)
- Are there lookup tables or data sets that must exist before go-live?

---

## 4. Business Logic Gaps

Walk through the stated logic and ask:
- What happens at **each decision point** if the condition is NOT met?
- Are there **parallel approval paths** (e.g., two approvers needed)?
- Is there a **time-based component** (SLA, escalation timer)? If so:
  - What time zone applies?
  - Does the clock pause on weekends / holidays?
- Are there **sequential dependencies** between tasks or approvals?

---

## 5. Notification & Communication Scope

- Who receives notifications and at which stage?
- What channel: Email? Portal? MS Teams? ServiceNow mobile?
- Is the content of the notification defined, or just the trigger?
- What happens if the notification fails?

---

## 6. Technical Constraints Check

- Does this require changes to existing tables, ACLs, or Business Rules already in production?
- Are there UI requirements (Portal widget, Workspace layout, mobile form)?
- Is there a performance concern (high-volume records, complex queries)?
- What ServiceNow release is the target? Are the required features available?

---

## 7. Definition of Done

Ask explicitly:
- What does "complete" look like for UAT sign-off?
- Are there reporting or KPI requirements attached to this story?
- Is rollback or deactivation behaviour defined?
