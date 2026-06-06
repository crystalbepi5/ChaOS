const sampleAccounts = [
  {
    id: "acct-northstar",
    name: "Northstar Kitchens",
    segment: "Mid-market food service",
    owner: "Maya Chen",
    state: "account_ready_for_outreach",
    reviewStatus: "Accepted",
    decision: "Recommend play: send expansion-focused outreach tied to recent event attendance and open equipment refresh initiative.",
    outcome: "No action yet",
    feedback: "Initial recommendation accepted for proof review.",
    knownContext: [
      "Regional operator with 42 locations.",
      "Known facilities leader attended a fake industry event.",
      "Existing buying committee includes operations and finance personas."
    ],
    missingContext: [
      "Confirm current vendor contract timing.",
      "Find executive sponsor for rollout discussion."
    ],
    signals: ["Event attendance", "Recent activity", "Intent signal", "Prior meeting"],
    actions: [
      {
        id: "act-northstar-1",
        title: "Confirm vendor contract timing",
        owner: "Maya Chen",
        due: "This week",
        status: "planned",
        note: "Use public notes and prior meeting recap before drafting outreach."
      },
      {
        id: "act-northstar-2",
        title: "Draft expansion outreach for facilities leader",
        owner: "Maya Chen",
        due: "After contract timing is checked",
        status: "planned",
        note: "Human review required before any message is sent."
      }
    ]
  },
  {
    id: "acct-copperline",
    name: "Copperline Robotics",
    segment: "Manufacturing automation",
    owner: "Andre Patel",
    state: "account_has_persona_gap",
    reviewStatus: "Needs more context",
    decision: "Request missing context before outreach: identify economic buyer and technical evaluator.",
    outcome: "No action yet",
    feedback: "Persona gap needs review before account can be worked.",
    knownContext: [
      "Account is in target manufacturing segment.",
      "Fake intent signal suggests interest in warehouse automation.",
      "Prior meeting notes mention operations pain."
    ],
    missingContext: [
      "Economic buyer is unknown.",
      "Technical evaluator is unknown.",
      "No confirmed decision timeline."
    ],
    signals: ["Intent signal", "Persona gap", "Prior meeting"],
    actions: [
      {
        id: "act-copperline-1",
        title: "Identify economic buyer candidate",
        owner: "Andre Patel",
        due: "Tomorrow",
        status: "in_progress",
        note: "Do not recommend outreach until the buyer/persona gap is resolved."
      },
      {
        id: "act-copperline-2",
        title: "Find technical evaluator signal",
        owner: "Andre Patel",
        due: "This week",
        status: "blocked",
        note: "Blocked until reviewer confirms acceptable evidence source."
      }
    ]
  },
  {
    id: "acct-brightforge",
    name: "Brightforge Labs",
    segment: "Biotech services",
    owner: "Sam Rivera",
    state: "account_has_stale_activity",
    reviewStatus: "Revised",
    decision: "Assign next action: refresh account research before recommending a play.",
    outcome: "Plan revised",
    feedback: "Reviewer changed next step from outreach to research refresh.",
    knownContext: [
      "Account was previously high priority.",
      "Last fake activity is older than 90 days.",
      "Open opportunity was marked inactive in sample notes."
    ],
    missingContext: [
      "No recent stakeholder activity.",
      "No current initiative confirmed."
    ],
    signals: ["Stale account", "No recent touch", "Open opportunity"],
    actions: [
      {
        id: "act-brightforge-1",
        title: "Refresh account research",
        owner: "Sam Rivera",
        due: "Today",
        status: "in_progress",
        note: "Research refresh comes before a new recommendation."
      },
      {
        id: "act-brightforge-2",
        title: "Decide whether stale opportunity should remain active",
        owner: "Sam Rivera",
        due: "After research refresh",
        status: "planned",
        note: "Reviewer must decide before account returns to outreach queue."
      }
    ]
  },
  {
    id: "acct-civicpeak",
    name: "CivicPeak Software",
    segment: "Public sector SaaS",
    owner: "Jordan Ellis",
    state: "account_blocked_needs_review",
    reviewStatus: "Rejected",
    decision: "Route to human review because account ownership and active opportunity status conflict.",
    outcome: "Recommendation rejected",
    feedback: "Reviewer flagged conflicting owner information; suppress until clarified.",
    knownContext: [
      "Fake account has active opportunity marker.",
      "Two possible owners appear in manual sample notes.",
      "Prior meeting exists but next step is unclear."
    ],
    missingContext: [
      "Correct owner is unknown.",
      "Opportunity stage is inconsistent.",
      "Recent account priority is not trusted."
    ],
    signals: ["Open opportunity", "Prior meeting", "Persona gap"],
    actions: [
      {
        id: "act-civicpeak-1",
        title: "Resolve owner conflict",
        owner: "Jordan Ellis",
        due: "Before any account action",
        status: "blocked",
        note: "No outreach action may be planned until ownership is clarified."
      }
    ]
  },
  {
    id: "acct-emberlane",
    name: "Emberlane Studios",
    segment: "Creative operations",
    owner: "Priya Morgan",
    state: "account_plan_ready",
    reviewStatus: "Completed",
    decision: "Prioritize account and assign next action: send recap with creative operations benchmark offer.",
    outcome: "Action completed",
    feedback: "Completed in prototype review; next version should track meeting quality.",
    knownContext: [
      "Account has complete fake persona map.",
      "Recent activity indicates workflow redesign interest.",
      "Prior meeting identified a clear operational pain."
    ],
    missingContext: [
      "No missing context for MVP review."
    ],
    signals: ["Recent activity", "Prior meeting", "Intent signal", "Event attendance"],
    actions: [
      {
        id: "act-emberlane-1",
        title: "Send recap with benchmark offer",
        owner: "Priya Morgan",
        due: "Completed in sample",
        status: "completed",
        note: "Fake completed action used to test outcome review."
      },
      {
        id: "act-emberlane-2",
        title: "Capture meeting quality after response",
        owner: "Priya Morgan",
        due: "After reply",
        status: "deferred",
        note: "Wait for response before judging play quality."
      }
    ]
  }
];
