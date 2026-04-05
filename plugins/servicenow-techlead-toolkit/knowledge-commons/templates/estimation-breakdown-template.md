# Estimation Breakdown Template

Standard output format for the Estimation Wizard skill.
Used for story-point or work-day sizing of ServiceNow requirements.

---

WORK BREAKDOWN — [Feature / Requirement Title]

Input:         [Requirement reference, Jira ticket ID, or TDD title]
Sizing method: [Story points (Fibonacci) / Work days]
Date:          [Estimation date]

----------------------------------------------------------

WORK BREAKDOWN

  #   Task                                        Estimate    Confidence    Notes
  -   -----------------------------------------   ----------  ------------  -----------------------
  1   [Artifact type: description]                [X pts]     Confident
  2   [Artifact type: description]                [X pts]     Uncertain     [Assumption noted]
  3   [Artifact type: description]                [X pts]     High risk
      Spike recommended before sprint commit                  --            [Reason for spike]

  Sub-tasks are included in parent estimates unless marked separately.

  TOTAL (realistic):   [X pts / X days]
  Range:               Optimistic [X] — Pessimistic [X]


DEPENDENCIES

  #   Dependency                                            Type
  -   ---------------------------------------------------   ----------------
  1   [Cross-task or cross-team dependency]                 Blocking
  2   [...]                                                 Non-blocking


HIDDEN RISKS
Assumptions that could inflate scope if proved wrong:

  1. [Assumption] — potential impact if wrong: [+X pts / +X days]
  2. [...]


RECOMMENDATION
[1–2 sentences. Is this ready for sprint commitment?
Note any spikes required. Flag if Requirement Stress-Tester should be run first.]
