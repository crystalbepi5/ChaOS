const accounts = sampleAccounts.map((account) => ({ ...account }));
let selectedAccountId = accounts[0].id;

const accountCards = document.getElementById("accountCards");
const accountCount = document.getElementById("accountCount");
const readyCount = document.getElementById("readyCount");
const reviewCount = document.getElementById("reviewCount");
const acceptedCount = document.getElementById("acceptedCount");
const detailName = document.getElementById("detailName");
const detailSegment = document.getElementById("detailSegment");
const detailState = document.getElementById("detailState");
const knownContext = document.getElementById("knownContext");
const missingContext = document.getElementById("missingContext");
const signals = document.getElementById("signals");
const decision = document.getElementById("decision");
const owner = document.getElementById("owner");
const reviewStatus = document.getElementById("reviewStatus");
const outcome = document.getElementById("outcome");
const feedback = document.getElementById("feedback");

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

function renderSummary() {
  accountCount.textContent = accounts.length;
  readyCount.textContent = accounts.filter((account) => account.state.includes("ready")).length;
  reviewCount.textContent = accounts.filter((account) => account.reviewStatus === "Needs more context").length;
  acceptedCount.textContent = accounts.filter((account) => account.reviewStatus === "Accepted" || account.reviewStatus === "Completed").length;
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

render();
