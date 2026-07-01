const sampleAccounts = [
  {
    id: "acct-northstar",
    name: "Northstar Kitchens",
    segment: "Mid-market food service",
    owner: "Maya Chen",
    planHealth: "Ready",
    reviewStatus: "Accepted",
    nextMove: "Confirm vendor contract timing",
    nextMoveReason: "The account is ready to work, but contract timing should shape the outreach angle.",
    nextMoveOwner: "Maya Chen",
    nextMoveTiming: "This week",
    recommendedNextStep: "Draft an expansion follow-up tied to recent event attendance and the equipment refresh initiative.",
    result: "No action yet",
    reviewNotes: "Initial recommendation accepted for proof review.",
    accountSnapshot: [
      "Regional operator with 42 locations.",
      "Known facilities leader attended a fake industry event.",
      "Existing buying committee includes operations and finance personas."
    ],
    buyingSignals: ["Event attendance", "Recent activity", "Expansion interest", "Prior meeting"],
    updateNeeded: [
      { id: "upd-northstar-contract", label: "Confirm vendor contract timing", done: false, note: "Needed before final outreach copy." },
      { id: "upd-northstar-sponsor", label: "Find executive sponsor", done: false, note: "Improves confidence in expansion path." }
    ],
    blockers: [],
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
    planHealth: "Blocked",
    reviewStatus: "Needs more context",
    nextMove: "Identify economic buyer candidate",
    nextMoveReason: "Persona gap is blocking safe outreach.",
    nextMoveOwner: "Andre Patel",
    nextMoveTiming: "Tomorrow",
    recommendedNextStep: "Pause outreach until the economic buyer and technical evaluator are identified.",
    result: "No action yet",
    reviewNotes: "Persona gap needs review before account can be worked.",
    accountSnapshot: [
      "Account is in target manufacturing segment.",
      "Fake interest marker suggests warehouse automation research.",
      "Prior meeting notes mention operations pain."
    ],
    buyingSignals: ["Warehouse automation interest", "Prior meeting", "Operations pain"],
    updateNeeded: [
      { id: "upd-copperline-buyer", label: "Add economic buyer", done: false, note: "Needed before outreach." },
      { id: "upd-copperline-evaluator", label: "Confirm technical evaluator", done: false, note: "Needed to avoid guessing the buying committee." },
      { id: "upd-copperline-timeline", label: "Confirm decision timeline", done: false, note: "Needed to judge urgency." }
    ],
    blockers: [
      {
        id: "blk-copperline-persona",
        title: "Economic buyer unknown",
        reason: "The account cannot be worked safely until the buying committee is clearer.",
        suggestedResolution: "Find likely economic buyer and technical evaluator before drafting outreach.",
        status: "active"
      }
    ],
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
    planHealth: "Needs Update",
    reviewStatus: "Revised",
    nextMove: "Refresh account research",
    nextMoveReason: "Recent activity is stale, so a new play would be based on weak context.",
    nextMoveOwner: "Sam Rivera",
    nextMoveTiming: "Today",
    recommendedNextStep: "Refresh account research before recommending a new play.",
    result: "Plan revised",
    reviewNotes: "Reviewer changed next step from outreach to research refresh.",
    accountSnapshot: [
      "Account was previously high priority.",
      "Last fake activity is older than 90 days.",
      "Open opportunity was marked inactive in sample notes."
    ],
    buyingSignals: ["Stale activity", "No recent touch", "Inactive opportunity"],
    updateNeeded: [
      { id: "upd-brightforge-research", label: "Refresh account research", done: false, note: "Needed before the account returns to outreach queue." },
      { id: "upd-brightforge-oppty", label: "Confirm whether opportunity is still active", done: false, note: "Current opportunity status is not trusted." }
    ],
    blockers: [
      {
        id: "blk-brightforge-stale",
        title: "Account activity is stale",
        reason: "The last useful activity is older than 90 days.",
        suggestedResolution: "Refresh research and confirm whether the opportunity is still alive.",
        status: "active"
      }
    ],
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
    planHealth: "Blocked",
    reviewStatus: "Rejected",
    nextMove: "Resolve owner conflict",
    nextMoveReason: "Conflicting owner and opportunity details make the plan untrustworthy.",
    nextMoveOwner: "Jordan Ellis",
    nextMoveTiming: "Before any account action",
    recommendedNextStep: "Resolve ownership and opportunity conflicts before any next step is planned.",
    result: "Recommendation rejected",
    reviewNotes: "Reviewer flagged conflicting owner information; suppress until clarified.",
    accountSnapshot: [
      "Fake account has active opportunity marker.",
      "Two possible owners appear in manual sample notes.",
      "Prior meeting exists but next step is unclear."
    ],
    buyingSignals: ["Possible opportunity", "Prior meeting", "Ownership conflict"],
    updateNeeded: [
      { id: "upd-civicpeak-owner", label: "Resolve account owner", done: false, note: "Needed before any action is assigned." },
      { id: "upd-civicpeak-stage", label: "Confirm opportunity stage", done: false, note: "Needed before plan health can be trusted." }
    ],
    blockers: [
      {
        id: "blk-civicpeak-owner",
        title: "Owner conflict",
        reason: "Two possible owners appear in the sample notes.",
        suggestedResolution: "Confirm the correct owner and pause work until ownership is clear.",
        status: "active"
      },
      {
        id: "blk-civicpeak-opportunity",
        title: "Opportunity stage is inconsistent",
        reason: "The account has an opportunity marker, but the stage is not trusted.",
        suggestedResolution: "Confirm whether the opportunity is active before prioritizing the account.",
        status: "active"
      }
    ],
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
    planHealth: "Complete",
    reviewStatus: "Completed",
    nextMove: "Capture meeting quality after response",
    nextMoveReason: "The first action is complete; learning should now be captured so the play can improve.",
    nextMoveOwner: "Priya Morgan",
    nextMoveTiming: "After reply",
    recommendedNextStep: "Prioritize account and send reviewed recap with creative operations benchmark offer.",
    result: "Action completed",
    reviewNotes: "Completed in prototype review; next version should track meeting quality.",
    accountSnapshot: [
      "Account has complete fake persona map.",
      "Recent activity indicates workflow redesign interest.",
      "Prior meeting identified a clear operational pain."
    ],
    buyingSignals: ["Recent activity", "Prior meeting", "Workflow redesign interest", "Event attendance"],
    updateNeeded: [
      { id: "upd-emberlane-learning", label: "Capture meeting quality", done: false, note: "Needed after response to judge whether the play worked." }
    ],
    blockers: [],
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
