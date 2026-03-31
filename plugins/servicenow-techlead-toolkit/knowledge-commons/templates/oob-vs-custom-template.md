# OOB vs. Custom Comparison Table

Use this template to justify every customisation decision. The goal is to make clear that OOB was evaluated before any custom code was written.

---

## How to Use
For each feature in the solution, complete one row. If the OOB capability fully meets the need, use it. Only propose a customisation when there is a documented, specific reason the OOB approach does not work.

---

## Comparison Table

| Feature | OOB Capability | Proposed Customisation | Reason for Deviation | Risk of Deviation |
|---|---|---|---|---|
| Example: Multi-level approval | Flow Designer Approval activity supports serial and parallel approvals with any number of approvers | Custom approval table with additional fields for cost thresholds | OOB approval does not support conditional approval tiers based on financial bands | Low — contained to new table, no OOB table modified |
| | | | | |
| | | | | |

---

## Deviation Reason Categories (use these for consistency)

| Code | Meaning |
|---|---|
| **MISSING** | OOB capability does not exist for this feature |
| **PARTIAL** | OOB exists but lacks specific required functionality |
| **PERF** | OOB approach would cause performance issues at required scale |
| **UPGRADE** | OOB approach touches protected objects; customisation reduces upgrade risk |
| **CLIENT** | Client's existing process/data model is incompatible with OOB structure |
| **POLICY** | Client's security or compliance policy prohibits OOB behaviour |

---

## Customisation Risk Levels

| Level | Definition |
|---|---|
| **Low** | New custom table or field; no OOB tables, scripts, or UI pages modified |
| **Medium** | Extends OOB table or adds Business Rule to existing table; upgrade testing required |
| **High** | Modifies OOB script, UI page, or relies on OOB fields not guaranteed to persist |
| **Critical** | Modifies core platform behaviour (e.g., authentication, CMDB schema) |
