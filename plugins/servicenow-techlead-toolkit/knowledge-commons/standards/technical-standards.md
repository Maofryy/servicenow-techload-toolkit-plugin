# Technical Standards — ServiceNow Scripting Best Practices

This is the firm's "Definition of Done" for ServiceNow scripting. Every script merged to production must comply with these standards.

---

## 🔴 Critical Rules (Never Violate)

### 1. No `.update()` or `.insert()` Inside a Loop
```javascript
// ❌ WRONG — executes a DB write per iteration
while (gr.next()) {
    gr.state = 2;
    gr.update(); // N database writes
}

// ✅ CORRECT — batch with GlideRecord or use a single update with a query condition
var gr = new GlideRecord('incident');
gr.addQuery('state', 1);
gr.query();
gr.setValue('state', 2);
gr.updateMultiple(); // ONE database operation
```
**Why**: A loop over 1,000 records triggers 1,000 separate DB transactions. This kills database performance and can hit transaction timeouts.

---

### 2. No Role Checks on the Client Side
```javascript
// ❌ WRONG — client-side role checks are trivially bypassed
if (g_user.hasRole('admin')) {
    // show sensitive field
}

// ✅ CORRECT — enforce on the server via ACL or Business Rule
// Client-side: use for UI behaviour only (show/hide), never for security enforcement
```
**Why**: JavaScript in the browser is readable and modifiable by any user. Client-side role checks are UI sugar only. Real enforcement must happen server-side via ACL.

---

### 3. No Hard-Coded sys_ids in Production Logic
```javascript
// ❌ WRONG — sys_ids differ between instances
var groupId = '1234abc567def890';

// ✅ CORRECT — resolve by name at runtime
var gr = new GlideRecord('sys_user_group');
gr.get('name', 'Network Support');
var groupId = gr.sys_id;

// ALSO CORRECT — use a system property for configurable values
var groupId = gs.getProperty('u_network_support_group_id');
```
**Why**: sys_ids are instance-specific. Hard-coded IDs break when the application is promoted between sub-prod and production, or migrated.

---

### 4. No Business Logic in Client Scripts
```javascript
// ❌ WRONG — querying a table from a Client Script
var ga = new GlideAjax('MyScriptInclude');
// ...then performing complex business logic in the CS

// ✅ CORRECT — Client Scripts handle UI state only
// All business logic lives in Script Includes, called via GlideAjax if server data is needed
```
**Why**: Client Scripts run on the user's browser. Logic placed here is duplicated (it must also exist server-side for API and import scenarios), fragile, and untestable via ATF.

---

### 5. Always Use `gs.log()` / `gs.error()` for Server-Side Logging — Never `gs.print()`
```javascript
// ❌ Only works in background scripts, not in production code
gs.print('Debug value: ' + myVar);

// ✅ Use the proper logging API
gs.log('VendorApprovalUtils: processing request ' + current.number, 'VendorApprovalUtils');
gs.error('VendorApprovalUtils: API call failed for ' + current.number, 'VendorApprovalUtils');
```

---

## 🟡 Warning Rules (Require Justification to Override)

### 6. Always Check for Null Before Chaining Reference Fields
```javascript
// ❌ WRONG — throws if requested_for has no manager
var managerEmail = current.requested_for.manager.email;

// ✅ CORRECT — nil check at each reference hop
var managerEmail = '';
if (!current.requested_for.nil() && !current.requested_for.manager.nil()) {
    managerEmail = current.requested_for.manager.email.toString();
}
```

---

### 7. Wrap REST Calls in Try/Catch with Meaningful Error Handling
```javascript
// ❌ WRONG — silent failure
var response = new sn_ws.RESTMessageV2('VendorAPI', 'GET');
response.execute();

// ✅ CORRECT
try {
    var rm = new sn_ws.RESTMessageV2('VendorAPI', 'GET');
    rm.setStringParameter('id', current.u_vendor_id);
    var response = rm.execute();
    var statusCode = response.getStatusCode();

    if (statusCode !== 200) {
        gs.error('VendorAPI call failed: HTTP ' + statusCode + ' for record ' + current.number, 'VendorUtils');
        // Set fallback state on current record
        current.u_integration_status = 'error';
        current.u_integration_error = 'HTTP ' + statusCode;
    }
} catch (e) {
    gs.error('VendorAPI exception: ' + e.message + ' for record ' + current.number, 'VendorUtils');
}
```

---

### 8. Use `GlideAggregate` for Counts — Never `GlideRecord`
```javascript
// ❌ WRONG — loads every matching record into memory just to count them
var gr = new GlideRecord('incident');
gr.addQuery('state', 1);
gr.query();
var count = gr.getRowCount(); // DO NOT USE — deprecated and memory-intensive

// ✅ CORRECT
var ga = new GlideAggregate('incident');
ga.addQuery('state', 1);
ga.addAggregate('COUNT');
ga.query();
var count = ga.next() ? ga.getAggregate('COUNT') : 0;
```

---

### 9. Never Query in a Display Business Rule
```javascript
// ❌ WRONG — a GlideRecord query in a Display BR runs on every form load
(function executeRule(current, previous) {
    var gr = new GlideRecord('sys_user_group');
    gr.query(); // This fires for every user who opens ANY incident form
})(current, previous);

// ✅ CORRECT — use g_scratchpad to pass values set once, or use a Script Include cached result
```

---

### 10. Script Includes Must Be Instantiable Classes (Not Loose Functions)
```javascript
// ❌ WRONG — global function pollution
function myHelper() { ... }

// ✅ CORRECT — class-based Script Include
var VendorApprovalUtils = Class.create();
VendorApprovalUtils.prototype = {
    initialize: function() {},

    getVendorDetails: function(vendorId) {
        // ...
    },

    type: 'VendorApprovalUtils'
};
```

---

## 🔵 Naming Conventions

| Artifact | Convention | Example |
|---|---|---|
| Custom table | `u_` prefix + lowercase + underscores | `u_vendor_request` |
| Custom field | `u_` prefix + lowercase + underscores | `u_approval_threshold` |
| Script Include | PascalCase | `VendorApprovalUtils` |
| Business Rule | `[Table] - [Trigger] - [Purpose]` | `Incident - Before Insert - Set Priority` |
| Client Script | `[Table] - [Event] - [Purpose]` | `sc_req_item - onChange - Toggle Cost Field` |
| Flow | `[Domain] [Action] Flow` | `Vendor Request Approval Flow` |
| Scheduled Job | `[Frequency] [Purpose] Job` | `Daily Vendor SLA Escalation Job` |
| ATF Test | `[Artifact] - [Scenario]` | `Vendor Request - Inactive Requester Edge Case` |

---

## Definition of Done (Scripting)

Before any script is committed to the Update Set, verify:
- [ ] No `gr.update()` in loops
- [ ] No hard-coded sys_ids
- [ ] Null checks on every reference chain beyond 1 hop
- [ ] Try/catch on all REST/SOAP calls
- [ ] `gs.log()` present for non-trivial operations
- [ ] Script Include uses class pattern
- [ ] ATF test covers the happy path
- [ ] ATF test covers at least one edge case (null field, inactive user, or API failure)
- [ ] Code reviewed by tech lead before merge
