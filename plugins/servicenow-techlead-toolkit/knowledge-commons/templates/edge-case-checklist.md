# Edge Case Checklist

Run every requirement through these categories. For each one, ask: "Has the requirement addressed this? If not, is it truly irrelevant, or is it a gap?"

---

## Category 1: User State Edge Cases

| Edge Case | Probe Question |
|---|---|
| Inactive user | What if `requested_for` or `assigned_to` is inactive? Does the form block submission? Does it throw an error mid-flow? |
| Locked-out user | Can a locked account still receive work items or notifications? |
| User with no manager | If the flow escalates to `requested_for.manager`, what happens when that field is empty? |
| User with no group | What if `assigned_to` has no assignment group? Does auto-routing fail silently? |
| Guest / external user | Is this accessible to customers via CSM Portal? What fields are exposed? |
| VIP user | Does the story mention any priority or SLA overrides for executive-level users? |

---

## Category 2: Null & Empty Field Handling

| Field Type | Probe Question |
|---|---|
| Reference fields | What happens if a required reference lookup returns no results? |
| Date/Time fields | Is a null date treated as "no deadline" or "overdue immediately"? |
| Free-text fields | Is there a character limit? What happens with special characters or HTML injection? |
| Choice fields | What if the choice value is deprecated in a future release? |
| Multi-line / list fields | What is the separator? What is the maximum items? |

---

## Category 3: Integration & API Risks

| Risk | Probe Question |
|---|---|
| Timeout | What is the acceptable timeout for the external call? What is the fallback? |
| Error response | Does a 400/500 from the API block the flow, send an alert, or retry? |
| Authentication expiry | What happens if the OAuth token expires mid-flow? Is there auto-refresh? |
| Partial response | If the API returns incomplete data, does the flow proceed, pause, or error? |
| Rate limiting | Is this call made in bulk (e.g., a scheduled job)? Could it hit rate limits? |
| No response / MID Server down | Is there a dead-letter queue or manual fallback process? |

---

## Category 4: Flow & Approval Logic

| Scenario | Probe Question |
|---|---|
| Approver rejects | What happens after rejection? Is re-submission allowed? How many times? |
| Approver does not respond | Is there an escalation timer? To whom? |
| Delegated approver | Is approval delegation supported? Does the delegate have the right role? |
| Parallel vs. sequential approval | Are all approvers needed simultaneously, or in order? |
| Auto-approval rules | Are there conditions where the request should auto-approve (e.g., low-cost, low-risk)? |
| Cancelled mid-flow | Who can cancel? What is cleaned up (open tasks, active approvals, notifications)? |

---

## Category 5: SLA & Time-Based Logic

| Risk | Probe Question |
|---|---|
| Time zone | Is the SLA calculated in the user's TZ, the server's TZ, or a fixed TZ? |
| Business hours | Does the SLA clock run 24/7 or only during business hours? |
| Holiday schedule | Is there a schedule attached? Is it accurate for all regions affected? |
| Pause conditions | Does the SLA pause when the ticket is waiting on a third party? Who sets the pause state? |
| SLA breach action | What happens on breach — just a flag, an alert, an escalation? To whom? |

---

## Category 6: UI & Platform Compatibility

| Platform | Probe Question |
|---|---|
| Classic UI vs. Workspace | Is this form used in Service Operations Workspace, Agent Workspace, or Classic? Different layouts apply. |
| Employee Center / Portal | If customer/employee-facing, is the form widget responsive? Are all fields accessible without admin role? |
| Mobile | Does the story require mobile compatibility? ServiceNow mobile has field and widget limitations. |
| Accessibility | Are there WCAG / screen reader requirements? |

---

## Category 7: Security & Compliance

| Risk | Probe Question |
|---|---|
| Role escalation | Can a user trigger an action that grants themselves a role or access beyond their current rights? |
| PII / Sensitive data | Are any fields PII? Are they masked in notifications or audit logs? |
| ACL gaps | Who should NOT be able to read or write this record? Is that explicitly defined? |
| Audit trail | Is field-level auditing required? Are any fields excluded from audit for performance reasons? |
| Data residency | If multi-instance or multi-region: which instance does this data live on? |

---

## Category 8: Upgrade & Maintainability

| Risk | Probe Question |
|---|---|
| Protected objects | Does the solution touch any ServiceNow-owned tables, scripts, or UI pages that could be overwritten on upgrade? |
| Hard-coded values | Are sys_ids, user names, or group names hard-coded anywhere? |
| Test coverage | Is there a test suite or ATF test planned for this story? |
| Rollback plan | If this goes wrong in production, is there a documented rollback path? |
