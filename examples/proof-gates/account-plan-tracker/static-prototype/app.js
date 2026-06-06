const accounts = sampleAccounts.map((account) => ({
  ...account,
  knownContext: [...account.knownContext],
  missingContext: [...account.missingContext],
  signals: [...account.signals],
  actions: account.actions.map((action) => ({ ...action }))
}));
let selectedAccountId = accounts[0].id;
let actionSequence = 1;

const accountCards = document.getElementById("accountCards");
const accountCount = document.getElementById("accountCount");
const readyCount = document.getElementById("readyCount");
const reviewCount = document.getElementById("reviewCount");
const acceptedCount = document.getElementById("acceptedCount");
const openActionCount = document.getElementById("openActionCount");
const blockedActionCount = document.getElementById("blockedActionCount");
const completedActionCount = document.getElementById("completedActionCount");
const selectedActionCount = document.getElementById("selectedActionCount");
const detailName = document.getElementById("detailName");
const detailSegment = document.getElementById("detailSegment");
const detailState = document.getElementById("detailState");
const knownContext = document.getElementById("knownContext");
const missingContext = document.getElementById("missingContext");
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

function selectedAccount() {
  return accounts.find((account) => account.id === selectedAccountId) || accounts[0];
}

function stateClass(state) {
  if (state.includes("ready") || state.includes("plan_ready")) return "ready";
  if (state.includes("blocked")) return "blocked";
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

function allActions() {
  return accounts.flatMap((account) => account.actions);
}

function openActions(actions) {
  return actions.filter((action) => action.status !== "completed" && action.status !== "deferred");
}

function renderSummary() {
  const actions = allActions();
  accountCount.textContent = accounts.length;
  readyCount.textContent = accounts.filter((account) => account.state.includes("ready")).length;
  reviewCount.textContent = accounts.filter((account) => account.reviewStatus === "Needs more context").length;
  acceptedCount.textContent = accounts.filter((account) => account.reviewStatus === "Accepted" || account.reviewStatus === "Completed").length;
  openActionCount.textContent = openActions(actions).length;
  blockedActionCount.textContent = actions.filter((action) => action.status === "blocked").length;
  completedActionCount.textContent = actions.filter((action) => action.status === "completed").length;
  selectedActionCount.textContent = selectedAccount().actions.length;
}

function renderCards() {
  accountCards.innerHTML = "";
  accounts.forEach((account) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `account-card ${account.id === selectedAccountId ? "active" : ""}`;
    button.innerHTML = `
      <div class="card-top">
        <div>
          <span class="card-name">${account.name}</span>
          <span class="card-meta">${account.segment}</span>
        </div>
        <span class="review-pill ${reviewClass(account.reviewStatus)}">${account.reviewStatus}</span>
      </div>
      <p class="card-meta">${account.state}</p>
      <p class="card-meta">${openActions(account.actions).length} open action(s)</p>
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

function updateAction(actionId, field, value) {
  const account = selectedAccount();
  const action = account.actions.find((item) => item.id === actionId);
  if (!action) return;
  action[field] = value;
  renderSummary();
  renderCards();
  renderActions(account);
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
      .map((status) => `<option value="${status}" ${status === action.status ? "selected" : ""}>${status}</option>`)
      .join("");

    card.innerHTML = `
      <div class="action-card-header">
        <div>
          <h4>${action.title}</h4>
          <p class="card-meta">Owner: ${action.owner || "Unassigned"} · Timing: ${action.due || "Not set"}</p>
        </div>
        <span class="action-pill ${actionClass(action.status)}">${action.status}</span>
      </div>
      <div class="action-controls">
        <label>
          <span>Status</span>
          <select data-action-field="status" data-action-id="${action.id}">${options}</select>
        </label>
        <label>
          <span>Owner</span>
          <input data-action-field="owner" data-action-id="${action.id}" type="text" value="${action.owner}" placeholder="Human owner">
        </label>
        <label>
          <span>Timing</span>
          <input data-action-field="due" data-action-id="${action.id}" type="text" value="${action.due}" placeholder="Due / timing">
        </label>
      </div>
      <label class="action-note-label">
        <span>Execution note</span>
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

function renderDetail() {
  const account = selectedAccount();
  detailName.textContent = account.name;
  detailSegment.textContent = account.segment;
  detailState.textContent = account.state;
  detailState.className = `state-pill ${stateClass(account.state)}`;
  renderList(knownContext, account.knownContext);
  renderList(missingContext, account.missingContext);
  renderSignals(account.signals);
  decision.textContent = account.decision;
  owner.textContent = account.owner;
  renderActions(account);
  reviewStatus.value = account.reviewStatus;
  outcome.value = account.outcome;
  feedback.value = account.feedback;
}

function updateSelectedAccount(field, value) {
  const account = selectedAccount();
  account[field] = value;
  renderSummary();
  renderCards();
}

function render() {
  renderSummary();
  renderCards();
  renderDetail();
}

reviewStatus.addEventListener("change", (event) => {
  updateSelectedAccount("reviewStatus", event.target.value);
});

outcome.addEventListener("input", (event) => {
  updateSelectedAccount("outcome", event.target.value);
});

feedback.addEventListener("input", (event) => {
  updateSelectedAccount("feedback", event.target.value);
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
