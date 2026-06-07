const sampleAccounts = [
  {
    id: "acct-northstar",
    name: "Northstar Kitchens",
    segment: "Mid-market food service",
    owner: "Maya Chen",
    planStatus: "Ready for outreach",
    reviewStatus: "Accepted",
    recommendedNextStep: "Draft an expansion follow-up tied to recent event attendance and the equipment refresh initiative.",
    result: "No action yet",
    reviewNotes: "Initial recommendation accepted for proof review.",
    accountSnapshot: [
      "Regional operator with 42 locations.",
      "Known facilities leader attended a fake industry event.",
      "Existing buying committee includes operations and finance personas."
    ],
    gapsBlockers: [
      "Confirm current vendor contract timing.",
      "Find executive sponsor for rollout discussion."
    ],
    buyingSignals: ["Event attendance", "Recent activity", "Expansion interest", "Prior meeting"],
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
        title: "Draft reviewed follow-up for facilities leader",
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
    planStatus: "Persona gap",
    reviewStatus: "Needs more context",
    recommendedNextStep: "Pause outreach until the economic buyer and technical evaluator are identified.",
    result: "No action yet",
    reviewNotes: "Persona gap needs review before account can be worked.",
    accountSnapshot: [
      "Account is in target manufacturing segment.",
      "Fake interest marker suggests warehouse automation research.",
      "Prior meeting notes mention operations pain."
    ],
    gapsBlockers: [
      "Economic buyer is unknown.",
      "Technical evaluator is unknown.",
      "No confirmed decision timeline."
    ],
    buyingSignals: ["Warehouse automation interest", "Persona gap", "Prior meeting"],
    actions: [
      {
        id: "act-copperline-1",
        title: "Identify economic buyer candidate",
        owner: "Andre Patel",
        due: "Tomorrow",
        status: "in_progress",
        note: "Do not recommend outreach until the buyer gap is resolved."
      },
      {
        id: "act-copperline-2",
        title: "Find technical evaluator evidence",
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
    planStatus: "Research refresh needed",
    reviewStatus: "Revised",
    recommendedNextStep: "Refresh account research before recommending a new play.",
    result: "Plan revised",
    reviewNotes: "Reviewer changed next step from outreach to research refresh.",
    accountSnapshot: [
      "Account was previously high priority.",
      "Last fake activity is older than 90 days.",
      "Open opportunity was marked inactive in sample notes."
    ],
    gapsBlockers: [
      "No recent stakeholder activity.",
      "No current initiative confirmed."
    ],
    buyingSignals: ["Stale activity", "No recent touch", "Inactive opportunity"],
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
        title: "Decide whether opportunity should stay active",
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
    planStatus: "Blocked for review",
    reviewStatus: "Rejected",
    recommendedNextStep: "Resolve ownership and opportunity conflicts before any next step is planned.",
    result: "Recommendation rejected",
    reviewNotes: "Reviewer flagged conflicting owner information; suppress until clarified.",
    accountSnapshot: [
      "Fake account has active opportunity marker.",
      "Two possible owners appear in manual sample notes.",
      "Prior meeting exists but next step is unclear."
    ],
    gapsBlockers: [
      "Correct owner is unknown.",
      "Opportunity stage is inconsistent.",
      "Recent account priority is not trusted."
    ],
    buyingSignals: ["Possible opportunity", "Prior meeting", "Ownership conflict"],
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
    planStatus: "Plan ready",
    reviewStatus: "Completed",
    recommendedNextStep: "Prioritize account and send reviewed recap with creative operations benchmark offer.",
    result: "Action completed",
    reviewNotes: "Completed in prototype review; next version should track meeting quality.",
    accountSnapshot: [
      "Account has complete fake persona map.",
      "Recent activity indicates workflow redesign interest.",
      "Prior meeting identified a clear operational pain."
    ],
    gapsBlockers: [
      "No missing context for MVP review."
    ],
    buyingSignals: ["Recent activity", "Prior meeting", "Workflow redesign interest", "Event attendance"],
    actions: [
      {
        id: "act-emberlane-1",
        title: "Send reviewed recap with benchmark offer",
        owner: "Priya Morgan",
        due: "Completed in sample",
        status: "completed",
        note: "Fake completed action used to test result review."
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
