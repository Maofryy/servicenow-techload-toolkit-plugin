# DAT — Writing and architecture rules

**Posture**
1. The DAT describes the solution as it will be built and why the structuring choices were made.
   Build detail goes to the TDD or specs; requirements are referenced by ID, never copied.
2. One reader per section: board, security, operations, build team. The synthesis serves all.
3. Every statement is one of: *constaté* (verified on the instance or in a source), *hypothèse*
   (assumed, to confirm), *décision* (taken, with owner). Mark the status when it is not obvious.
4. A gap in the sources is a question to the client or an open point, never an invention.

**Structure**
5. Stable numbered plan (`templates/dat-plan.md`); a non-applicable chapter is kept with the reason.
6. Decisions are traced as ADRs: context, real options, criteria, decision, consequences, revisit
   condition. The chosen option does not win on every criterion.
7. Each requirement that shapes the design is traced to the chapter that answers it. A requirement
   not covered appears as a deviation or a risk.

**Architecture content**
8. Several complementary views: context, logical/application, data flow, deployment. Each diagram
   has a number, a title, a legend and a paragraph that explains it.
9. Integrations: direction, protocol, auth, volume/frequency, real-time or batch, retry, error
   handling, data owner. Security explicit: authentication, authorisation, classification,
   encryption, secrets, audit, compliance.
10. Non-functional requirements carry a figure and the way it is met; "fast" is not a requirement.
11. Environments, promotion and testing (ATF) are described; run model has a RACI.

**Writing**
12. Short sentences, active voice, present tense: "Le flux crée l'incident", not "l'incident sera
    créé". One term, one meaning; define acronyms at first use; glossary in annex.
13. Tables for what can be enumerated (interfaces, roles, tables, risks); prose for justification.
14. Document language is the client's; ServiceNow terms stay in English (business rule, flow,
    update set, scope). No marketing wording, no unexplained superlatives.
15. Dated, versioned, with a visible status (Brouillon / Relu / Validé) and a change list; open
    decisions have an owner and a date.
16. Figures, names and dates come from a source; cite it in the traceability annex.
