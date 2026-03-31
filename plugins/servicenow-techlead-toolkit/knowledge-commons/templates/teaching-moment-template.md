# Teaching Moment Comment Template

Use this format for every Critical or Warning issue in a code review. The goal is to leave the developer better than you found them — not just to fix the immediate issue.

---

## Standard Format

```
🚩 Issue
[One sentence describing what the problem is. Be specific — reference the exact line or pattern.]

💡 The Better Way
[A corrected code snippet or alternative approach. Show, don't just tell.]

📖 Why It Matters
[One to two sentences on the real-world impact: performance cost, security risk, upgrade fragility, or maintenance burden.]

🔗 Reference
[Link to ServiceNow docs, firm wiki, or the specific standard in technical-standards.md]
```

---

## Examples

### Example 1 — `gr.update()` in a Loop

🚩 **Issue**
Line 12–18: `gr.update()` is called inside the `while (gr.next())` loop, executing one database write per record.

💡 **The Better Way**
```javascript
// Replace the loop + update with updateMultiple()
var gr = new GlideRecord('incident');
gr.addQuery('assignment_group', oldGroupId);
gr.addQuery('state', 1);
gr.query();
gr.setValue('assignment_group', newGroupId);
gr.updateMultiple(); // Single DB operation regardless of record count
```

📖 **Why It Matters**
With 500 matching records this script triggers 500 separate database transactions, which will spike DB load and likely hit ServiceNow's transaction timeout limit (default 60s). `updateMultiple()` performs a single SQL UPDATE statement.

🔗 **Reference**: [ServiceNow Docs — GlideRecord updateMultiple](https://developer.servicenow.com/dev.do#!/reference/api/tokyo/server/GlideRecord-updateMultiple) | See `technical-standards.md` Rule #1

---

### Example 2 — Hard-Coded sys_id

🚩 **Issue**
Line 4: `var groupId = 'a1b2c3d4e5f67890'` — a hard-coded sys_id is used to identify the "Service Desk" group.

💡 **The Better Way**
```javascript
// Option A — resolve at runtime (works across all instances)
var gr = new GlideRecord('sys_user_group');
if (gr.get('name', 'Service Desk')) {
    var groupId = gr.sys_id.toString();
}

// Option B — use a system property (best for values that admins may need to change)
var groupId = gs.getProperty('u_service_desk_group_id', '');
if (!groupId) {
    gs.error('System property u_service_desk_group_id is not set', 'RoutingUtils');
}
```

📖 **Why It Matters**
sys_ids are auto-generated per instance and will differ between your development, UAT, and production environments. This script will work in dev and silently fail (or route to the wrong group) in production.

🔗 **Reference**: See `technical-standards.md` Rule #3

---

### Example 3 — Missing Null Check on Reference Chain

🚩 **Issue**
Line 9: `current.requested_for.manager.email` — this chain will throw a null pointer exception if `requested_for` has no manager assigned.

💡 **The Better Way**
```javascript
var managerEmail = '';
if (!current.requested_for.nil()) {
    var managerRef = current.requested_for.getRefRecord();
    if (!managerRef.manager.nil()) {
        managerEmail = managerRef.manager.getRefRecord().email.toString();
    } else {
        gs.log('No manager found for user: ' + current.requested_for.getDisplayValue(), 'ApprovalUtils');
        // Handle fallback — e.g., route to group instead
    }
}
```

📖 **Why It Matters**
Any user without a manager (contractors, new hires, deprovisioned accounts) will break this flow. This is one of the most common causes of silent flow failures in production — the record gets stuck with no approval and no error.

🔗 **Reference**: See `technical-standards.md` Rule #6

---

## Tips for Delivery
- Always use the Teaching Moment format for 🔴 Critical and 🟡 Warning items
- For 🔵 Suggestions: a brief comment is fine — save the full template for items that really need it
- If you find the same issue in multiple places, address it once with a note: "This pattern also appears on lines X, Y, and Z"
- End the review with the developer's path forward — what do they need to fix before re-review?
