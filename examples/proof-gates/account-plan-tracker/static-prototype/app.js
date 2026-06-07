const accounts = sampleAccounts.map((account) => ({
  ...account,
  accountSnapshot: [...account.accountSnapshot],
  buyingSignals: [...account.buyingSignals],
  updateNeeded: account.updateNeeded.map((item) => ({ ...item })),
  blockers: account.blockers.map((blocker) => ({ ...blocker })),
  actions: account.actions.map((action) => ({ ...action }))
}));
let selectedAccountId = accounts[0].id;
let actionSequence = 1;

const accountCards = document.getElementById("accountCards");
const accountCount = document.getElementById("accountCount");
const readyCount = document.getElementById("readyCount");
const needsUpdateCount = document.getElementById("needsUpdateCount");
const blockedAccountCount = document.getElementById("blockedAccountCount");
const openActionCount = document.getElementById("openActionCount");
const completedActionCount = document.getElementById("completedActionCount");
const progressHeadline = document.getElementById("progressHeadline");
const selectedOpenCount = document.getElementById("selectedOpenCount");
const selectedBlockedCount = document.getElementById("selectedBlockedCount");
const selectedCompletedCount = document.getElementById("selectedCompletedCount");
const selectedUpdateCount = document.getElementById("selectedUpdateCount");
const selectedReviewStatus = document.getElementById("selectedReviewStatus");
const detailName = document.getElementById("detailName");
const detailSegment = document.getElementById("detailSegment");
const detailHealth = document.getElementById("detailHealth");
const nextMoveTitle = document.getElementById("nextMoveTitle");
const nextMoveReason = document.getElementById("nextMoveReason");
const nextMoveOwner = document.getElementById("nextMoveOwner");
const nextMoveTiming = document.getElementById("nextMoveTiming");
const nextMoveHealth = document.getElementById("nextMoveHealth");
const primaryActionButton = document.getElementById("primaryActionButton");
const updateNeededList = document.getElementById("updateNeededList");
const blockerList = document.getElementById("blockerList");
const knownContext = document.getElementById("knownContext");
const signals = document.getElementById("signals");
const decision = document.getElementById("decision");
const owner = document.getElementById("owner");
const actionList = document.getElementById("actionList");
const actionForm = document.getElementById("actionForm");
const actionTitle = document.getElementById("actionTitle");
const actionOwner = document.getElementById("actionOwner");
const actionDue = document.getElementById("actionDue");
const actionStatus = document.getElementById("actionStatus");
const actionNote = document.getElementById("actionNote");
const reviewStatus = document.getElementById("reviewStatus");
const outcome = document.getElementById("outcome");
const feedback = document.getElementById("feedback");

const actionStatuses = ["planned", "in_progress", "blocked", "completed", "deferred"];
const blockerStatuses = ["active", "reviewing", "resolved"];

function selectedAccount() {
  return accounts.find((account) => account.id === selectedAccountId) || accounts[0];
}

function healthClass(health) {
  const normalized = health.toLowerCase();
  if (normalized.includes("ready") || normalized.includes("complete")) return "ready";
  if (normalized.includes("blocked")) return "blocked";
  if (normalized.includes("paused")) return "paused";
  return "review";
}

function reviewClass(status) {
  const normalized = status.toLowerCase();
  if (normalized.includes("accepted")) return "accepted";
  if (normalized.includes("completed")) return "completed";
  if (normalized.includes("rejected")) return "rejected";
  return "needs";
}

function actionClass(status) {
  if (status === "completed") return "completed";
  if (status === "blocked") return "blocked";
  if (status === "in_progress") return "active";
  return "planned";
}

function readableStatus(status) {
  return status.replace(/_/g, " ");
}

function allActions() {
  return accounts.flatMap((account) => account.actions);
}

function openActions(actions) {
  return actions.filter((action) => action.status !== "completed" && action.status !== "deferred");
}

function blockedActions(actions) {
  return actions.filter((action) => action.status === "blocked");
}

function completedActions(actions) {
  return actions.filter((action) => action.status === "completed");
}

function activeBlockers(account) {
  return account.blockers.filter((blocker) => blocker.status !== "resolved");
}

function pendingUpdates(account) {
  return account.updateNeeded.filter((item) => !item.done);
}

function primaryButtonText(account) {
  if (account.planHealth === "Blocked") return "Review blocker";
  if (account.planHealth === "Needs Update") return "Update plan";
  if (account.planHealth === "Complete") return "Review results";
  if (account.planHealth === "Paused") return "Keep paused";
  return "Mark in progress";
}

function renderSummary() {
  const actions = allActions();
  accountCount.textContent = accounts.length;
  readyCount.textContent = accounts.filter((account) => account.planHealth === "Ready").length;
  needsUpdateCount.textContent = accounts.filter((account) => account.planHealth === "Needs Update" || pendingUpdates(account).length > 0).length;
  blockedAccountCount.textContent = accounts.filter((account) => account.planHealth === "Blocked" || activeBlockers(account).length > 0).length;
  openActionCount.textContent = openActions(actions).length;
  completedActionCount.textContent = completedActions(actions).length;
}

function renderSelectedProgress(account) {
  const open = openActions(account.actions).length;
  const blocked = blockedActions(account.actions).length;
  const completed = completedActions(account.actions).length;
  const updates = pendingUpdates(account).length;
  progressHeadline.textContent = `${account.actions.length} action${account.actions.length === 1 ? "" : "s"} tracked`;
  selectedOpenCount.textContent = open;
  selectedBlockedCount.textContent = blocked;
  selectedCompletedCount.textContent = completed;
  selectedUpdateCount.textContent = updates;
  selectedReviewStatus.textContent = `Review: ${account.reviewStatus}`;
}

function renderCards() {
  accountCards.innerHTML = "";
  accounts.forEach((account) => {
    const openCount = openActions(account.actions).length;
    const updateCount = pendingUpdates(account).length;
    const blockerCount = activeBlockers(account).length;
    const button = document.createElement("button");
    button.type = "button";
    button.className = `account-card ${account.id === selectedAccountId ? "active" : ""}`;
    button.innerHTML = `
      <div class="card-top">
        <div>
          <span class="card-name">${account.name}</span>
          <span class="card-meta">${account.segment}</span>
        </div>
        <span class="state-pill ${healthClass(account.planHealth)}">${account.planHealth}</span>
      </div>
      <p class="next-card-move">${account.nextMove}</p>
      <div class="card-footer">
        <span class="card-meta">${openCount} open</span>
        ${updateCount ? `<span class="attention-dot">${updateCount} update${updateCount === 1 ? "" : "s"}</span>` : ""}
        ${blockerCount ? `<span class="blocker-dot">${blockerCount} blocker${blockerCount === 1 ? "" : "s"}</span>` : ""}
      </div>
    `;
    button.addEventListener("click", () => {
      selectedAccountId = account.id;
      render();
    });
    accountCards.appendChild(button);
  });
}

function renderList(target, items) {
  target.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  });
}

function renderSignals(items) {
  signals.innerHTML = "";
  items.forEach((item) => {
    const chip = document.createElement("span");
    chip.className = "signal-chip";
    chip.textContent = item;
    signals.appendChild(chip);
  });
}

function renderNextMove(account) {
  nextMoveTitle.textContent = account.nextMove;
  nextMoveReason.textContent = account.nextMoveReason;
  nextMoveOwner.textContent = account.nextMoveOwner;
  nextMoveTiming.textContent = account.nextMoveTiming;
  nextMoveHealth.textContent = account.planHealth;
  primaryActionButton.textContent = primaryButtonText(account);
  primaryActionButton.className = `primary-action ${healthClass(account.planHealth)}`;
}

function renderUpdates(account) {
  updateNeededList.innerHTML = "";

  if (account.updateNeeded.length === 0) {
    const empty = document.createElement("p");
    empty.className = "positive-empty";
    empty.textContent = "No plan updates needed right now.";
    updateNeededList.appendChild(empty);
    return;
  }

  account.updateNeeded.forEach((item) => {
    const label = document.createElement("label");
    label.className = `checklist-item ${item.done ? "done" : ""}`;
    label.innerHTML = `
      <input type="checkbox" data-update-id="${item.id}" ${item.done ? "checked" : ""}>
      <span>
        <strong>${item.label}</strong>
        <small>${item.note}</small>
      </span>
    `;
    label.querySelector("input").addEventListener("change", (event) => {
      item.done = event.target.checked;
      render();
    });
    updateNeededList.appendChild(label);
  });
}

function renderBlockers(account) {
  blockerList.innerHTML = "";

  if (activeBlockers(account).length === 0) {
    const empty = document.createElement("p");
    empty.className = "positive-empty";
    empty.textContent = "No active blockers for this plan.";
    blockerList.appendChild(empty);
    return;
  }

  activeBlockers(account).forEach((blocker) => {
    const card = document.createElement("article");
    card.className = "blocker-card";
    const options = blockerStatuses
      .map((status) => `<option value="${status}" ${status === blocker.status ? "selected" : ""}>${status}</option>`)
      .join("");
    card.innerHTML = `
      <div class="blocker-header">
        <h4>${blocker.title}</h4>
        <span class="blocker-dot">${blocker.status}</span>
      </div>
      <p><strong>Why it matters:</strong> ${blocker.reason}</p>
      <p><strong>Suggested resolution:</strong> ${blocker.suggestedResolution}</p>
      <label>
        <span>Status</span>
        <select data-blocker-id="${blocker.id}">${options}</select>
      </label>
    `;
    card.querySelector("select").addEventListener("change", (event) => {
      blocker.status = event.target.value;
      render();
    });
    blockerList.appendChild(card);
  });
}

function updateAction(actionId, field, value) {
  const account = selectedAccount();
  const action = account.actions.find((item) => item.id === actionId);
  if (!action) return;
  action[field] = value;
  render();
}

function renderActions(account) {
  actionList.innerHTML = "";

  if (account.actions.length === 0) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No local actions are tracked for this account yet.";
    actionList.appendChild(empty);
    return;
  }

  account.actions.forEach((action) => {
    const card = document.createElement("article");
    card.className = "action-card";

    const options = actionStatuses
      .map((status) => `<option value="${status}" ${status === action.status ? "selected" : ""}>${readableStatus(status)}</option>`)
      .join("");

    card.innerHTML = `
      <div class="action-card-header">
        <div>
          <h4>${action.title}</h4>
          <p class="card-meta">Owner: ${action.owner || "Unassigned"} | Timing: ${action.due || "Not set"}</p>
        </div>
        <span class="action-pill ${actionClass(action.status)}">${readableStatus(action.status)}</span>
      </div>
      <div class="action-controls">
        <label>
          <span>Progress</span>
          <select data-action-field="status" data-action-id="${action.id}">${options}</select>
        </label>
        <label>
          <span>Owner</span>
          <input data-action-field="owner" data-action-id="${action.id}" type="text" value="${action.owner}" placeholder="Human owner">
        </label>
        <label>
          <span>Timing</span>
          <input data-action-field="due" data-action-id="${action.id}" type="text" value="${action.due}" placeholder="Timing">
        </label>
      </div>
      <label class="action-note-label">
        <span>Note / blocker</span>
        <textarea data-action-field="note" data-action-id="${action.id}" rows="3">${action.note}</textarea>
      </label>
    `;

    card.querySelectorAll("[data-action-field]").forEach((control) => {
      const eventName = control.tagName === "SELECT" ? "change" : "input";
      control.addEventListener(eventName, (event) => {
        updateAction(event.target.dataset.actionId, event.target.dataset.actionField, event.target.value);
      });
    });

    actionList.appendChild(card);
  });
}

function applyPrimaryAction() {
  const account = selectedAccount();

  if (account.planHealth === "Blocked") {
    const blocker = activeBlockers(account)[0];
    if (blocker) blocker.status = "reviewing";
  } else if (account.planHealth === "Needs Update") {
    const update = pendingUpdates(account)[0];
    if (update) update.done = true;
  } else if (account.planHealth === "Complete") {
    reviewStatus.value = "Completed";
    account.reviewStatus = "Completed";
  } else {
    const action = account.actions.find((item) => item.title === account.nextMove) || openActions(account.actions)[0];
    if (action && action.status !== "completed") action.status = "in_progress";
  }

  render();
}

function renderDetail() {
  const account = selectedAccount();
  detailName.textContent = account.name;
  detailSegment.textContent = account.segment;
  detailHealth.textContent = account.planHealth;
  detailHealth.className = `state-pill ${healthClass(account.planHealth)}`;
  renderNextMove(account);
  renderSelectedProgress(account);
  renderUpdates(account);
  renderBlockers(account);
  renderActions(account);
  renderList(knownContext, account.accountSnapshot);
  renderSignals(account.buyingSignals);
  decision.textContent = account.recommendedNextStep;
  owner.textContent = account.owner;
  reviewStatus.value = account.reviewStatus;
  outcome.value = account.result;
  feedback.value = account.reviewNotes;
}

function updateSelectedAccount(field, value) {
  const account = selectedAccount();
  account[field] = value;
  render();
}

function render() {
  renderSummary();
  renderCards();
  renderDetail();
}

primaryActionButton.addEventListener("click", applyPrimaryAction);

reviewStatus.addEventListener("change", (event) => {
  updateSelectedAccount("reviewStatus", event.target.value);
});

outcome.addEventListener("input", (event) => {
  updateSelectedAccount("result", event.target.value);
});

feedback.addEventListener("input", (event) => {
  updateSelectedAccount("reviewNotes", event.target.value);
});

actionForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const account = selectedAccount();
  const title = actionTitle.value.trim();

  if (!title) {
    actionTitle.focus();
    return;
  }

  account.actions.push({
    id: `act-local-${Date.now()}-${actionSequence}`,
    title,
    owner: actionOwner.value.trim() || account.owner,
    due: actionDue.value.trim() || "Not set",
    status: actionStatus.value,
    note: actionNote.value.trim() || "Added locally during prototype review."
  });
  actionSequence += 1;

  actionForm.reset();
  actionStatus.value = "planned";
  render();
});

render();
