const BACKEND_URL = "https://advise-assist-api.onrender.com";
const FEEDBACK_FORM_URL = ""; // TODO: paste your Google Form link

const CATEGORY_DISPLAY = {
  add_drop:      { name: "Add/Drop",      color: "preset7",  hex: "#0078d4" },
  major_change:  { name: "Major Change",  color: "preset8",  hex: "#8764b8" },
  failing_class: { name: "Failing Class", color: "preset0",  hex: "#d13438" },
  financial:     { name: "Financial Aid", color: "preset3",  hex: "#986f0b" },
  mental_health: { name: "Mental Health", color: "preset4",  hex: "#107c10" },
  general:       { name: "General",       color: "preset10", hex: "#4a6572" },
};

// The current email's draft, already hydrated with the real names, ready to insert.
let hydratedDraft = "";

// ─── Responded tracking ──────────────────────────────────────────────────────
// Mark emails as handled, keyed by Outlook message id in localStorage. The id is
// unique per email (the shared sender doesn't matter), and it resets cleanly when
// the inbox is reseeded. Purely local to this browser — no extra permissions.
let currentItemId = null;
const RESPONDED_KEY = "advise_responded_ids";

function loadResponded() {
  try { return new Set(JSON.parse(localStorage.getItem(RESPONDED_KEY) || "[]")); }
  catch (e) { return new Set(); }
}
function isResponded(id) { return id ? loadResponded().has(id) : false; }
function markResponded(id) {
  if (!id) return;
  const s = loadResponded();
  s.add(id);
  localStorage.setItem(RESPONDED_KEY, JSON.stringify([...s]));
}

function updateRespondedUI() {
  document.getElementById("respondedBanner").classList.toggle("hidden", !isResponded(currentItemId));
}

// ─── Microsoft Graph auth (Office Dialog + MSAL) ─────────────────────────────
// Personal outlook.com accounts can't use Office SSO, and an MSAL popup
// (window.open) is blocked inside the task-pane iframe. So we open the sign-in
// in an Office dialog (fallbackauth.html) that runs MSAL and sends the token
// back via messageParent. The token is cached in memory for the session.
const GRAPH_BASE = "https://graph.microsoft.com/v1.0";
const AUTH_DIALOG_URL = "https://email-mvp-roan.vercel.app/addin/fallbackauth.html";
let cachedGraphToken = null;

function getGraphToken() {
  if (cachedGraphToken) return Promise.resolve(cachedGraphToken);
  return new Promise((resolve, reject) => {
    Office.context.ui.displayDialogAsync(
      AUTH_DIALOG_URL,
      { height: 60, width: 30, promptBeforeOpen: false },
      (result) => {
        if (result.status !== Office.AsyncResultStatus.Succeeded) {
          reject(new Error("Could not open the sign-in window."));
          return;
        }
        const dialog = result.value;
        dialog.addEventHandler(Office.EventType.DialogMessageReceived, (arg) => {
          dialog.close();
          let msg;
          try { msg = JSON.parse(arg.message); } catch (e) { reject(new Error("Sign-in failed.")); return; }
          if (msg.token) { cachedGraphToken = msg.token; resolve(msg.token); }
          else { reject(new Error(msg.error || "Sign-in failed.")); }
        });
        dialog.addEventHandler(Office.EventType.DialogEventReceived, () => {
          reject(new Error("Sign-in window was closed before completing."));
        });
      }
    );
  });
}

Office.onReady((info) => {
  if (info.host === Office.HostType.Outlook) {
    analyzeEmail();
    Office.context.mailbox.addHandlerAsync(Office.EventType.ItemChanged, analyzeEmail);
    document.getElementById("insertBtn").addEventListener("click", insertReply);
    document.getElementById("draftText").addEventListener("input", (e) => autoSizeDraft(e.target));
    document.getElementById("thumbUp").addEventListener("click", openFeedback);
    document.getElementById("thumbDown").addEventListener("click", openFeedback);
    document.getElementById("categorizeInboxBtn").addEventListener("click", categorizeInbox);
  }
});

// ─── Single-email analysis (existing feature) ────────────────────────────────

async function analyzeEmail() {
  const item = Office.context.mailbox.item;
  if (!item) return;
  showLoading();

  item.body.getAsync(Office.CoercionType.Text, async (bodyResult) => {
    if (bodyResult.status === Office.AsyncResultStatus.Failed) {
      showError("Could not read email body.");
      return;
    }
    try {
      const response = await fetch(`${BACKEND_URL}/process-email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email_text: bodyResult.value,
          subject: item.subject || "",
          sender: item.from?.emailAddress || "",
        }),
      });
      if (!response.ok) throw new Error("Backend error");
      const data = await response.json();
      render(data, item);
    } catch (err) {
      showError("Could not reach backend. Is it running?");
    }
  });
}

function render(data, item) {
  const decision = (data.decision || "no").toLowerCase();
  currentItemId = item.itemId || null;

  // Student name comes from the matched DARS record (emails are seeded into one
  // mailbox, so the "From" address is the same for all of them).
  const studentName =
    (data.dars && data.dars.name) || (item.from && item.from.displayName) || "there";
  const advisorName =
    (Office.context.mailbox.userProfile && Office.context.mailbox.userProfile.displayName) || "";
  hydratedDraft = (data.draft || "")
    .replaceAll("[name]", studentName)
    .replaceAll("[Advisor name]", advisorName);

  // Status banner
  const banner = document.getElementById("statusBanner");
  const status = {
    yes: ["banner-yes", "Answer ready to send"],
    partly: ["banner-partly", "Review before sending"],
    no: ["banner-no", "Needs your judgment"],
  }[decision] || ["banner-no", "Needs your judgment"];
  banner.className = `banner ${status[0]}`;
  document.getElementById("statusText").innerText = status[1];

  // Pills
  document.getElementById("categoryBadge").innerText = (data.category || "general").replace("_", "/").toUpperCase();
  const urgency = data.urgency || "routine";
  const urgEl = document.getElementById("urgencyBadge");
  urgEl.innerText = urgency.toUpperCase();
  urgEl.className = `badge urgency-${urgency}`;

  // DARS card — only when the student record was used
  if (data.used_record && data.dars) {
    renderDarsCard(data.dars, studentName);
    show("darsCard");
  } else {
    hide("darsCard");
  }

  // Draft + insert button (not on "no")
  if (decision !== "no" && hydratedDraft.trim()) {
    document.getElementById("draftText").value = hydratedDraft;
    show("draftSection");
    show("insertBtn");
  } else {
    hide("draftSection");
    hide("insertBtn");
  }

  // Checklist
  const checklist = data.checklist || [];
  const list = document.getElementById("checklistItems");
  list.innerHTML = "";
  if (checklist.length) {
    checklist.forEach((c) => {
      const li = document.createElement("li");
      li.innerText = c;
      list.appendChild(li);
    });
    show("checklistSection");
  } else {
    hide("checklistSection");
  }

  // Policy reference + no-draft note (shown when there's no draft)
  const ctx = data.context || {};
  document.getElementById("policyText").innerText = ctx.text || "";
  document.getElementById("policyLink").href = ctx.link || "#";
  if (decision === "no") {
    show("policySection");
    show("noDraftNote");
  } else {
    hide("policySection");
    hide("noDraftNote");
  }

  // Responded state (banner + button visibility)
  updateRespondedUI();

  hide("loading");
  show("result");

  // Size the draft textarea to its content (only meaningful once visible).
  if (!document.getElementById("draftSection").classList.contains("hidden")) {
    autoSizeDraft(document.getElementById("draftText"));
  }
}

function autoSizeDraft(el) {
  el.style.height = "auto";
  el.style.height = `${el.scrollHeight + 2}px`;
}

const DEGREE_HOURS = 120;

function renderDarsCard(d, studentName) {
  // Hold badge — only when there's an active hold
  const holdEl = document.getElementById("darsHold");
  if (d.holds && d.holds.length) {
    holdEl.innerText = `\u{1F512} ${d.holds.join(", ")}`;
    holdEl.classList.remove("hidden");
  } else {
    holdEl.classList.add("hidden");
  }

  // Name + major/standing
  document.getElementById("darsName").innerText = studentName;
  document.getElementById("darsMeta").innerText =
    [d.major, d.standing].filter(Boolean).join(" · ");

  // Stat tiles: GPA (red on probation), in-progress, completed
  const onProbation = typeof d.gpa === "number" && d.gpa < 2.0;
  const statsEl = document.getElementById("darsStats");
  statsEl.innerHTML = `
    <div class="dars-stat">
      <div class="dars-stat-num${onProbation ? " dars-stat-bad" : ""}">${d.gpa ?? "—"}</div>
      <div class="dars-stat-label">GPA${onProbation ? " · probation" : ""}</div>
    </div>
    <div class="dars-stat">
      <div class="dars-stat-num">${d.credits_in_progress ?? "—"}</div>
      <div class="dars-stat-label">in progress</div>
    </div>
    <div class="dars-stat">
      <div class="dars-stat-num">${d.credits_completed ?? "—"}</div>
      <div class="dars-stat-label">of ${DEGREE_HOURS} done</div>
    </div>`;

  // Progress bar toward graduation
  const progEl = document.getElementById("darsProgress");
  if (typeof d.credits_completed === "number") {
    const pct = Math.min(100, Math.round((d.credits_completed / DEGREE_HOURS) * 100));
    document.getElementById("darsBarFill").style.width = `${pct}%`;
    document.getElementById("darsProgressText").innerText =
      `${pct}% toward graduation` +
      (d.expected_graduation ? ` · expected ${d.expected_graduation}` : "");
    progEl.classList.remove("hidden");
  } else {
    progEl.classList.add("hidden");
  }

  // "Why it matters" — only for at-risk students that have it
  const whyEl = document.getElementById("darsWhy");
  if (d.why) {
    whyEl.innerHTML = `<span class="dars-why-label">⚠ Why it matters:</span> ${d.why}`;
    whyEl.classList.remove("hidden");
  } else {
    whyEl.classList.add("hidden");
  }
}

function insertReply() {
  // Use the current textarea contents so any advisor edits are included.
  const text = document.getElementById("draftText").value;
  Office.context.mailbox.item.displayReplyForm({
    htmlBody: text.replace(/\n/g, "<br>"),
  });
  // Inserting the reply is the "I'm handling this" moment — mark it done.
  markResponded(currentItemId);
  updateRespondedUI();
}

function openFeedback() {
  if (FEEDBACK_FORM_URL) window.open(FEEDBACK_FORM_URL, "_blank");
}

function show(id) { document.getElementById(id).classList.remove("hidden"); }
function hide(id) { document.getElementById(id).classList.add("hidden"); }

// ─── Categorize Inbox ─────────────────────────────────────────────────────────

async function categorizeInbox() {
  const btn = document.getElementById("categorizeInboxBtn");
  btn.disabled = true;
  btn.innerText = "Categorizing…";
  hideCategorizeError();

  let step = "sign-in";
  try {
    // Step 1: get a Graph token (Office sign-in dialog on first use, cached after)
    const token = await getGraphToken();

    // Step 2: fetch inbox messages (body as plain text)
    step = "reading inbox";
    const messages = await fetchInboxMessages(token, 50);

    // Step 3: batch-categorize via backend
    step = "categorizing";
    const emailPayload = messages.map((m) => ({
      id: m.id,
      subject: m.subject || "",
      body: (m.body && m.body.content) || "",
    }));

    const catResponse = await fetch(`${BACKEND_URL}/categorize-batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emails: emailPayload }),
    });
    if (!catResponse.ok) throw new Error("Categorization backend error");
    const catData = await catResponse.json();

    // Step 4: ensure Outlook master categories exist, then tag each email
    // (in small batches with retries so none get silently dropped to throttling).
    step = "creating categories";
    await ensureOutlookCategories(token);
    step = "tagging emails";
    const failed = await applyCategoriesInBatches(token, catData.results);

    // Silent success — the result shows as color tags in Outlook itself. Just a
    // brief confirmation on the button, no in-pane summary panel.
    if (failed > 0) {
      showCategorizeError(`${failed} email${failed > 1 ? "s" : ""} couldn't be tagged — click again to retry.`);
      btn.innerText = "Categorize Inbox";
    } else {
      btn.innerText = "✓ Categorized";
      setTimeout(() => { btn.innerText = "Categorize Inbox"; }, 2500);
    }
  } catch (err) {
    showCategorizeError(`(${step}) ${err.message || "Could not categorize inbox."}`);
    btn.innerText = "Categorize Inbox";
  } finally {
    btn.disabled = false;
  }
}

async function fetchInboxMessages(token, count) {
  const url =
    `${GRAPH_BASE}/me/mailFolders/inbox/messages` +
    `?$top=${count}&$select=id,subject,body`;
  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      "Prefer": 'outlook.body-content-type="text"',
    },
  });
  if (!response.ok) throw new Error("Could not fetch inbox messages.");
  const data = await response.json();
  return data.value || [];
}

async function ensureOutlookCategories(token) {
  // Fetch existing master categories as name -> {id, color}.
  const listResp = await fetch(`${GRAPH_BASE}/me/outlook/masterCategories`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const existing = {};
  if (listResp.ok) {
    const listData = await listResp.json();
    (listData.value || []).forEach((c) => { existing[c.displayName] = c; });
  }

  // Create missing categories, and FIX the color on any that already exist with
  // the wrong color — Outlook pre-creates categories grey, so without this they'd
  // never pick up our intended preset color. Done ONE AT A TIME with retries: the
  // masterCategories endpoint throttles hard, so firing all at once left most grey.
  for (const { name, color } of Object.values(CATEGORY_DISPLAY)) {
    const cur = existing[name];
    if (!cur) {
      await categoryWrite(`${GRAPH_BASE}/me/outlook/masterCategories`, "POST", { displayName: name, color }, token);
    } else if (cur.color !== color) {
      await categoryWrite(`${GRAPH_BASE}/me/outlook/masterCategories/${cur.id}`, "PATCH", { color }, token);
    }
  }
}

// Create/update a master category, retrying on throttling (429) or transient errors.
async function categoryWrite(url, method, body, token, attempt = 0) {
  try {
    const resp = await fetch(url, {
      method,
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (resp.ok) return true;
    if ((resp.status === 429 || resp.status >= 500) && attempt < 4) {
      const ra = parseInt(resp.headers.get("Retry-After"), 10);
      const waitMs = Number.isFinite(ra) ? ra * 1000 : 400 * 2 ** attempt;
      await new Promise((r) => setTimeout(r, waitMs));
      return categoryWrite(url, method, body, token, attempt + 1);
    }
    return false;
  } catch (e) {
    if (attempt < 4) {
      await new Promise((r) => setTimeout(r, 400 * 2 ** attempt));
      return categoryWrite(url, method, body, token, attempt + 1);
    }
    return false;
  }
}

// Tag emails in small concurrent batches (not all at once) so Graph doesn't
// throttle us. Returns how many ultimately failed after retries.
async function applyCategoriesInBatches(token, results, batchSize = 4) {
  let failed = 0;
  for (let i = 0; i < results.length; i += batchSize) {
    const slice = results.slice(i, i + batchSize);
    const outcomes = await Promise.all(
      slice.map((r) => applyOutlookCategory(token, r.id, r.category))
    );
    failed += outcomes.filter((ok) => !ok).length;
  }
  return failed;
}

// Apply one category. Returns true on success; retries on throttling (429) or
// transient server/network errors with backoff. Returns false if it gives up.
async function applyOutlookCategory(token, messageId, category, attempt = 0) {
  const catInfo = CATEGORY_DISPLAY[category] || CATEGORY_DISPLAY.general;
  try {
    const resp = await fetch(`${GRAPH_BASE}/me/messages/${messageId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ categories: [catInfo.name] }),
    });
    if (resp.ok) return true;
    if ((resp.status === 429 || resp.status >= 500) && attempt < 3) {
      const retryAfter = parseInt(resp.headers.get("Retry-After"), 10);
      const waitMs = Number.isFinite(retryAfter) ? retryAfter * 1000 : 500 * 2 ** attempt;
      await new Promise((r) => setTimeout(r, waitMs));
      return applyOutlookCategory(token, messageId, category, attempt + 1);
    }
    return false;
  } catch (e) {
    if (attempt < 3) {
      await new Promise((r) => setTimeout(r, 500 * 2 ** attempt));
      return applyOutlookCategory(token, messageId, category, attempt + 1);
    }
    return false;
  }
}

function hideCategorizeError() {
  document.getElementById("categorize-error").classList.add("hidden");
}

function showCategorizeError(msg) {
  const el = document.getElementById("categorize-error");
  el.innerText = msg;
  el.classList.remove("hidden");
}

function showLoading() {
  hide("result");
  hide("error");
  show("loading");
}

function showError(msg) {
  hide("loading");
  const el = document.getElementById("error");
  el.innerText = msg;
  show("error");
}
