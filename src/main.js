const STORAGE_KEY = "research-hub-state-v1";
const MAX_DOCUMENT_BYTES = 1_500_000;
const STATUS_OPTIONS = [
  "Draft",
  "Under Review",
  "Waiting for Recommendations",
  "Revisions Required",
  "Accepted",
  "Published",
  "On Hold"
];

const DEFAULT_GUIDELINES = [
  {
    id: "guideline-nature",
    journal: "Nature",
    url: "https://www.nature.com/nature/for-authors/formatting-guide",
    wordLimit: "Main text typically up to 3,000 words",
    citationStyle: "Numbered references",
    notes: "A concise abstract is required and methods often go to supplementary information."
  },
  {
    id: "guideline-ieee",
    journal: "IEEE Transactions",
    url: "https://journals.ieeeauthorcenter.ieee.org/",
    wordLimit: "Varies by journal",
    citationStyle: "IEEE",
    notes: "Use IEEE templates and follow strict figure resolution requirements."
  },
  {
    id: "guideline-plos",
    journal: "PLOS ONE",
    url: "https://journals.plos.org/plosone/s/submission-guidelines",
    wordLimit: "No strict word limit",
    citationStyle: "Vancouver style",
    notes: "Data availability statement and ethics statements are mandatory when relevant."
  }
];

const elements = {
  overviewGrid: document.getElementById("overview-grid"),
  collaboratorForm: document.getElementById("collaborator-form"),
  collaboratorsList: document.getElementById("collaborators-list"),
  researchForm: document.getElementById("research-form"),
  researchCollaborator: document.getElementById("research-collaborator"),
  researchStatus: document.getElementById("research-status"),
  researchGuideline: document.getElementById("research-guideline"),
  searchInput: document.getElementById("search-input"),
  statusFilter: document.getElementById("status-filter"),
  researchList: document.getElementById("research-list"),
  guidelineForm: document.getElementById("guideline-form"),
  guidelinesList: document.getElementById("guidelines-list")
};

const state = loadState();

bindEvents();
renderAll();

function bindEvents() {
  elements.collaboratorForm.addEventListener("submit", handleAddCollaborator);
  elements.researchForm.addEventListener("submit", handleAddResearch);
  elements.guidelineForm.addEventListener("submit", handleAddGuideline);

  elements.collaboratorsList.addEventListener("click", handleCollaboratorActions);
  elements.researchList.addEventListener("click", handleResearchActions);
  elements.researchList.addEventListener("change", handleResearchStatusChange);
  elements.guidelinesList.addEventListener("click", handleGuidelineActions);

  elements.searchInput.addEventListener("input", renderResearchList);
  elements.statusFilter.addEventListener("change", renderResearchList);
}

function loadState() {
  const fallback = {
    collaborators: [],
    research: [],
    guidelines: structuredClone(DEFAULT_GUIDELINES)
  };
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return fallback;
  }

  try {
    const parsed = JSON.parse(raw);
    return {
      collaborators: Array.isArray(parsed.collaborators) ? parsed.collaborators : [],
      research: Array.isArray(parsed.research) ? parsed.research : [],
      guidelines:
        Array.isArray(parsed.guidelines) && parsed.guidelines.length > 0
          ? parsed.guidelines
          : structuredClone(DEFAULT_GUIDELINES)
    };
  } catch {
    return fallback;
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function renderAll() {
  renderStatusSelects();
  renderCollaboratorOptions();
  renderGuidelineOptions();
  renderOverview();
  renderCollaboratorsList();
  renderResearchList();
  renderGuidelinesList();
}

function renderStatusSelects() {
  const researchStatusOptions = STATUS_OPTIONS.map((status) => `<option value="${status}">${status}</option>`).join("");
  elements.researchStatus.innerHTML = researchStatusOptions;
  elements.researchStatus.value = "Draft";

  const filterOptions = ['<option value="all">All statuses</option>']
    .concat(STATUS_OPTIONS.map((status) => `<option value="${status}">${status}</option>`))
    .join("");
  elements.statusFilter.innerHTML = filterOptions;
}

function renderCollaboratorOptions() {
  if (state.collaborators.length === 0) {
    elements.researchCollaborator.innerHTML = '<option value="">No collaborator assigned</option>';
    return;
  }

  const options = ['<option value="">No collaborator assigned</option>']
    .concat(
      state.collaborators.map(
        (collaborator) =>
          `<option value="${collaborator.id}">${escapeHtml(collaborator.name)} (${escapeHtml(collaborator.role)})</option>`
      )
    )
    .join("");

  elements.researchCollaborator.innerHTML = options;
}

function renderGuidelineOptions() {
  const options = ['<option value="">No specific guideline</option>']
    .concat(
      state.guidelines.map(
        (guideline) => `<option value="${guideline.id}">${escapeHtml(guideline.journal)}</option>`
      )
    )
    .join("");

  elements.researchGuideline.innerHTML = options;
}

function renderOverview() {
  const underReviewCount = state.research.filter(
    (item) => item.status === "Under Review" || item.status === "Waiting for Recommendations"
  ).length;
  const publishedCount = state.research.filter((item) => item.status === "Published").length;
  const revisionsCount = state.research.filter((item) => item.revisions.length > 0).length;
  const cards = [
    { label: "Total research items", value: state.research.length },
    { label: "Collaborators", value: state.collaborators.length },
    { label: "In review workflow", value: underReviewCount },
    { label: "Published", value: publishedCount },
    { label: "With revisions logged", value: revisionsCount }
  ];

  elements.overviewGrid.innerHTML = cards
    .map(
      (card) => `
      <article class="stat-card">
        <p>${card.label}</p>
        <strong>${card.value}</strong>
      </article>
    `
    )
    .join("");
}

function renderCollaboratorsList() {
  if (state.collaborators.length === 0) {
    elements.collaboratorsList.innerHTML = '<p class="empty-state">No collaborators yet.</p>';
    return;
  }

  elements.collaboratorsList.innerHTML = state.collaborators
    .map(
      (collaborator) => `
      <article class="list-row">
        <div>
          <h3>${escapeHtml(collaborator.name)}</h3>
          <p>${escapeHtml(collaborator.email)} · ${escapeHtml(collaborator.role)}</p>
        </div>
        <button class="btn danger" data-action="remove-collaborator" data-id="${collaborator.id}" type="button">
          Remove
        </button>
      </article>
    `
    )
    .join("");
}

function renderResearchList() {
  const statusFilter = elements.statusFilter.value;
  const query = elements.searchInput.value.trim().toLowerCase();

  const filteredResearch = state.research
    .filter((item) => statusFilter === "all" || item.status === statusFilter)
    .filter((item) => {
      if (!query) {
        return true;
      }
      const blob = [item.title, item.journal, item.summary, getCollaboratorName(item.leadCollaboratorId)]
        .join(" ")
        .toLowerCase();
      return blob.includes(query);
    })
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());

  if (filteredResearch.length === 0) {
    elements.researchList.innerHTML = '<p class="empty-state">No research records match your filters.</p>';
    return;
  }

  elements.researchList.innerHTML = filteredResearch
    .map((item) => {
      const statusClassName = `status-${item.status.toLowerCase().replace(/\s+/g, "-")}`;
      const revisionItems =
        item.revisions.length === 0
          ? "<li>No revisions logged yet.</li>"
          : item.revisions
              .slice()
              .reverse()
              .map((revision) => `<li><strong>${formatDate(revision.at)}</strong> - ${escapeHtml(revision.note)}</li>`)
              .join("");
      const guideline = getGuideline(item.guidelineId);
      const guidelineText = guideline ? guideline.journal : "None";
      const documentMarkup = item.document
        ? `<a class="inline-link" href="${item.document.dataUrl}" download="${escapeHtml(item.document.name)}">Download: ${escapeHtml(item.document.name)}</a>`
        : "<span class=\"muted\">No file uploaded</span>";

      return `
      <article class="research-card">
        <div class="research-heading">
          <div>
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(item.journal)} · Lead: ${escapeHtml(getCollaboratorName(item.leadCollaboratorId))}</p>
          </div>
          <span class="status-badge ${statusClassName}">${escapeHtml(item.status)}</span>
        </div>
        <p>${escapeHtml(item.summary)}</p>
        <p class="meta-line">
          Guideline: ${escapeHtml(guidelineText)} · Last updated: ${formatDate(item.updatedAt)}
        </p>
        <p class="meta-line">${documentMarkup}</p>
        <div class="row-controls">
          <label>
            Update status
            <select class="inline-status-select" data-id="${item.id}">
              ${STATUS_OPTIONS.map(
                (status) =>
                  `<option value="${status}" ${status === item.status ? "selected" : ""}>${status}</option>`
              ).join("")}
            </select>
          </label>
          <button class="btn subtle" data-action="add-revision" data-id="${item.id}" type="button">
            Add revision note
          </button>
          <button class="btn danger" data-action="remove-research" data-id="${item.id}" type="button">
            Remove
          </button>
        </div>
        <details>
          <summary>Revision history (${item.revisions.length})</summary>
          <ul class="revision-list">${revisionItems}</ul>
        </details>
      </article>
    `;
    })
    .join("");
}

function renderGuidelinesList() {
  if (state.guidelines.length === 0) {
    elements.guidelinesList.innerHTML = '<p class="empty-state">No guidelines configured.</p>';
    return;
  }

  elements.guidelinesList.innerHTML = state.guidelines
    .map(
      (guideline) => `
      <article class="guideline-card">
        <div class="guideline-header">
          <h3>${escapeHtml(guideline.journal)}</h3>
          <button class="btn danger" data-action="remove-guideline" data-id="${guideline.id}" type="button">
            Remove
          </button>
        </div>
        <p><strong>Word limit:</strong> ${escapeHtml(guideline.wordLimit || "Not specified")}</p>
        <p><strong>Citation style:</strong> ${escapeHtml(guideline.citationStyle || "Not specified")}</p>
        <p>${escapeHtml(guideline.notes || "No additional notes.")}</p>
        ${
          guideline.url
            ? `<a class="inline-link" href="${escapeHtml(guideline.url)}" target="_blank" rel="noreferrer">Open submission page</a>`
            : ""
        }
      </article>
    `
    )
    .join("");
}

function handleAddCollaborator(event) {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  const collaborator = {
    id: createId("collab"),
    name: String(formData.get("name") ?? "").trim(),
    email: String(formData.get("email") ?? "").trim(),
    role: String(formData.get("role") ?? "").trim()
  };

  if (!collaborator.name || !collaborator.email || !collaborator.role) {
    return;
  }

  state.collaborators.push(collaborator);
  saveState();
  event.currentTarget.reset();
  renderAll();
}

async function handleAddResearch(event) {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);

  const fileInput = document.getElementById("research-document");
  const file = fileInput.files?.[0];
  const document = await readDocument(file);

  const item = {
    id: createId("research"),
    title: String(formData.get("title") ?? "").trim(),
    journal: String(formData.get("journal") ?? "").trim(),
    leadCollaboratorId: String(formData.get("leadCollaboratorId") ?? ""),
    status: String(formData.get("status") ?? "Draft"),
    guidelineId: String(formData.get("guidelineId") ?? ""),
    summary: String(formData.get("summary") ?? "").trim(),
    document,
    revisions: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  if (!item.title || !item.summary || !item.journal) {
    return;
  }

  state.research.unshift(item);
  saveState();
  event.currentTarget.reset();
  elements.researchStatus.value = "Draft";
  renderAll();
}

function handleAddGuideline(event) {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  const guideline = {
    id: createId("guideline"),
    journal: String(formData.get("journal") ?? "").trim(),
    url: String(formData.get("url") ?? "").trim(),
    wordLimit: String(formData.get("wordLimit") ?? "").trim(),
    citationStyle: String(formData.get("citationStyle") ?? "").trim(),
    notes: String(formData.get("notes") ?? "").trim()
  };

  if (!guideline.journal) {
    return;
  }

  state.guidelines.unshift(guideline);
  saveState();
  event.currentTarget.reset();
  renderAll();
}

function handleCollaboratorActions(event) {
  const button = event.target.closest("button[data-action='remove-collaborator']");
  if (!button) {
    return;
  }
  const collaboratorId = button.dataset.id;
  state.collaborators = state.collaborators.filter((collaborator) => collaborator.id !== collaboratorId);
  for (const research of state.research) {
    if (research.leadCollaboratorId === collaboratorId) {
      research.leadCollaboratorId = "";
      research.updatedAt = new Date().toISOString();
    }
  }
  saveState();
  renderAll();
}

function handleResearchActions(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) {
    return;
  }

  const action = button.dataset.action;
  const researchId = button.dataset.id;
  const research = state.research.find((item) => item.id === researchId);
  if (!research) {
    return;
  }

  if (action === "remove-research") {
    state.research = state.research.filter((item) => item.id !== researchId);
  }

  if (action === "add-revision") {
    const note = window.prompt("Add a revision or update note:");
    if (note && note.trim()) {
      research.revisions.push({
        id: createId("revision"),
        at: new Date().toISOString(),
        note: note.trim()
      });
      research.updatedAt = new Date().toISOString();
    }
  }

  saveState();
  renderAll();
}

function handleResearchStatusChange(event) {
  const select = event.target.closest(".inline-status-select");
  if (!select) {
    return;
  }
  const research = state.research.find((item) => item.id === select.dataset.id);
  if (!research) {
    return;
  }
  research.status = select.value;
  research.updatedAt = new Date().toISOString();
  saveState();
  renderAll();
}

function handleGuidelineActions(event) {
  const button = event.target.closest("button[data-action='remove-guideline']");
  if (!button) {
    return;
  }
  const guidelineId = button.dataset.id;
  state.guidelines = state.guidelines.filter((guideline) => guideline.id !== guidelineId);
  for (const research of state.research) {
    if (research.guidelineId === guidelineId) {
      research.guidelineId = "";
      research.updatedAt = new Date().toISOString();
    }
  }
  saveState();
  renderAll();
}

function getCollaboratorName(collaboratorId) {
  if (!collaboratorId) {
    return "Unassigned";
  }
  const collaborator = state.collaborators.find((item) => item.id === collaboratorId);
  return collaborator ? collaborator.name : "Unassigned";
}

function getGuideline(guidelineId) {
  if (!guidelineId) {
    return null;
  }
  return state.guidelines.find((guideline) => guideline.id === guidelineId) ?? null;
}

async function readDocument(file) {
  if (!file) {
    return null;
  }
  if (file.size > MAX_DOCUMENT_BYTES) {
    window.alert("Document is too large for local browser storage. Use a file under 1.5 MB.");
    return null;
  }

  const dataUrl = await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(new Error("File reading failed."));
    reader.readAsDataURL(file);
  });

  return {
    name: file.name,
    type: file.type || "application/octet-stream",
    dataUrl
  };
}

function createId(prefix) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`;
}

function formatDate(isoString) {
  const parsed = new Date(isoString);
  if (Number.isNaN(parsed.getTime())) {
    return "Unknown date";
  }
  return parsed.toLocaleString();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
