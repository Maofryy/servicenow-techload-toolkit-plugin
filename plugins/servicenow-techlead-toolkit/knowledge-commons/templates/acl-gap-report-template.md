# ACL Gap & Risk Report — Template

Use this structure for Layer 3 of the ACL Logic Architect output. Produce one report per table in the export. Omit any severity section that has no findings.

---

## Gap & Risk Report — `{table_name}`

### 🔴 Critical
<!-- Trigger conditions:
  - Table has no active ACLs at all
  - admin_overrides=true on any field-level ACL
  - advanced=true but script field is empty (broken ACL — behavior undefined)
  - A Deny Unless ACL is inactive (active=false) — that gate is silently open
-->
- {Specific finding referencing the exact field and operation, e.g.: "`cost` field: admin_overrides=true on a field-level Deny Unless ACL — admins bypass this restriction entirely"}

### 🟡 Warning
<!-- Trigger conditions:
  - Table has read ACL but missing write, create, or delete ACL
  - Field has write protection but no read protection (asymmetric)
  - Deny Unless ACLs present but no Allow If ACL on the table — parent ACL fallback silently in effect
  - admin_overrides=true on a record-level ACL
  - Broad roles (admin, snc_internal, super_admin) used without tighter scoping on sensitive tables
-->
- {Specific finding, e.g.: "`alm_asset` table: read and write ACLs exist but no create or delete ACL — those operations are unprotected"}

### 🔵 Info
<!-- Trigger conditions:
  - SAC auto-generated ACLs detected in the export
  - Script-based ACLs present (translations provided in Layers 1 and 2)
  - Inactive ACLs present (active=false, non-Deny-Unless)
-->
- {Specific finding, e.g.: "3 SAC auto-generated ACLs detected (marked [SAC] in the matrix) — do not modify these manually"}

---
*Repeat this block for each table in the export. If a table has no findings, write: "No gaps detected for `{table_name}`."*
