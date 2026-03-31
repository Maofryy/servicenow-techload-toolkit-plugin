# Technical Design Document (TDD) Lite — Template

---

## Header

| Field | Value |
|---|---|
| Project / Story | |
| Architect | Maori |
| ServiceNow Release | (e.g., Washington DC, Xanadu) |
| Status | Draft / Under Review / Approved |
| Date | |
| Reviewed By | |

---

## 1. Business Context (1–2 sentences)
> What problem does this solve, and for whom? State the business outcome, not the technical mechanism.

---

## 2. Scope
- **In Scope**: [List what this design covers]
- **Out of Scope**: [Explicitly list what is NOT covered to prevent scope creep]
- **Assumptions**: [List design assumptions — these should be confirmed by the BA/client]

---

## 3. Data Model

### 3a. Table Changes

| Table | Action | Field(s) Added/Modified | Type | Notes |
|---|---|---|---|---|
| e.g. `sc_req_item` | Extend / Modify | `u_vendor_contact` | Reference → `sys_user` | Needed for third-party fulfilment tracking |

### 3b. Relationships
Describe any new table relationships (parent/child, M2M via `m2m_` table, etc.).

### 3c. Indexes
Flag any fields that will be heavily queried and should have database indexes added.

---

## 4. Automation Logic

### 4a. Technology Choice
State which mechanism(s) are used and **why** (reference the Technology Decision Framework):
> Example: "Flow Designer chosen over Business Rules because the logic is orchestration-based and must support future no-code modifications by the client admin team."

### 4b. Flow / Logic Diagram
Describe the logic steps in plain language or as a numbered sequence. For visual flows, note that the Visual Explainer skill can generate a Mermaid diagram.

```
Step 1: Triggered by [event]
Step 2: Condition — if [X], go to Step 3; else go to Step 5
Step 3: [Action]
Step 4: [Outcome / notification]
Step 5: [Alternative path]
```

### 4c. Script Includes (if applicable)

| Script Include Name | Purpose | Called From |
|---|---|---|
| `VendorApprovalUtils` | Centralises vendor lookup logic | Flow Designer Inline Script |

---

## 5. Security Model

### 5a. Roles Required

| Role | Purpose | Existing OOB or New Custom |
|---|---|---|
| `itil` | Read/write to `incident` table | OOB |
| `u_vendor_manager` | Approve vendor requests | Custom (new) |

### 5b. ACL Design

| Table | Operation | Role Required | Additional Condition |
|---|---|---|---|
| `u_vendor_request` | read | `itil` OR `u_vendor_manager` | None |
| `u_vendor_request` | write | `u_vendor_manager` | `current.state != 3` (not closed) |
| `u_vendor_request.u_cost` | read | `u_vendor_manager` | None |

### 5c. Query Business Rules (Row-Level Security)
If users should only see a subset of records (e.g., only their own requests), define a Query Business Rule here:
> Table: `u_vendor_request` | Condition: `current.addQuery('u_requested_by', gs.getUserID())` (when `itil` role, not `u_vendor_manager`)

---

## 6. User Interface

### 6a. Platform
- [ ] Classic UI (list/form views)
- [ ] Service Portal (widget)
- [ ] Employee Center (topic block / record producer)
- [ ] Agent Workspace
- [ ] Mobile App

### 6b. Form Layout Notes
Key fields to include, field groupings, and any UI Policies for conditional field visibility.

### 6c. Record Producer / Catalog Item (if applicable)
Variables, variable sets, and the mapping to the target table.

---

## 7. Notifications

| Trigger | Recipients | Channel | Template Needed |
|---|---|---|---|
| Request submitted | Requester | Email | Yes |
| Approved | Requester + Fulfiller | Email + In-app | Yes |
| Rejected | Requester | Email | Yes |
| SLA breaching (80%) | Assignment Group Manager | Email | No (use OOB SLA notification) |

---

## 8. Testing Approach

| Test Type | Coverage | Owner |
|---|---|---|
| Unit (ATF) | Happy path + 3 edge cases (inactive user, no manager, API timeout) | Dev |
| Integration | End-to-end flow in sub-prod | QA |
| UAT | Business scenario walkthroughs | Client BA |
| Regression | Existing incident/request functionality unchanged | QA |

---

## 9. Risks & Open Items

| Risk | Severity | Mitigation |
|---|---|---|
| API timeout on vendor lookup | Medium | Implement retry with 3-attempt limit and fallback to manual entry |
| Legacy data without `u_vendor_contact` populated | Low | Bulk data fix script in migration plan |

---

## 10. Dependencies
List any other stories, platform features, or data that must be in place before this can be built or deployed.
