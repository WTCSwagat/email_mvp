const BACKEND_URL = "https://advise-assist-api.onrender.com";

const CATEGORY_DISPLAY = {
  add_drop:      { name: "Add/Drop",      color: "preset7",  hex: "#0078d4" },
  major_change:  { name: "Major Change",  color: "preset8",  hex: "#8764b8" },
  failing_class: { name: "Failing Class", color: "preset0",  hex: "#d13438" },
  financial:     { name: "Financial Aid", color: "preset3",  hex: "#986f0b" },
  mental_health: { name: "Mental Health", color: "preset4",  hex: "#107c10" },
  general:       { name: "General",       color: "preset12", hex: "#69797e" },
};

// PII-free fields from the last analysis, reused when drafting a reply.
let lastAnalysis = {
  category: "general",
  canonical_question: "",
  policy_context: "",
};

Office.onReady((info) => {
  if (info.host === Office.HostType.Outlook) {
    analyzeEmail();
    Office.context.mailbox.addHandlerAsync(
      Office.EventType.ItemChanged,
      analyzeEmail
    );
    document
      .getElementById("draftReplyBtn")
      .addEventListener("click", draftReferralReply);
    document
      .getElementById("categorizeInboxBtn")
      .addEventListener("click", categorizeInbox);
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

      lastAnalysis = {
        category: data.category || "general",
        canonical_question: data.canonical_question || "",
        policy_context: (data.context && data.context.text) || "",
      };

      document.getElementById("categoryBadge").innerText = data.category
        .replace("_", "/")
        .toUpperCase();
      document.getElementById("urgencyBadge").innerText = data.urgency.toUpperCase();
      document.getElementById("urgencyBadge").className = `urgency-${data.urgency}`;
      document.getElementById("policyText").innerText = data.context.text;
      document.getElementById("policyLink").href = data.context.link;
      document.getElementById("referralOffice").innerText = `→ ${data.referral.office}`;
      document.getElementById("referralAction").innerText = data.referral.action;
      document.getElementById("referralLink").href = data.referral.link;

      document.getElementById("loading").classList.add("hidden");
      document.getElementById("result").classList.remove("hidden");
    } catch (err) {
      showError("Could not reach backend. Is it running?");
    }
  });
}

async function draftReferralReply() {
  const btn = document.getElementById("draftReplyBtn");
  const originalLabel = btn.innerText;
  btn.disabled = true;
  btn.innerText = "Drafting…";

  try {
    const response = await fetch(`${BACKEND_URL}/draft-reply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: lastAnalysis.category,
        canonical_question: lastAnalysis.canonical_question,
        policy_context: lastAnalysis.policy_context,
      }),
    });

    if (!response.ok) throw new Error("Draft error");
    const data = await response.json();

    const item = Office.context.mailbox.item;
    const studentName = (item.from && item.from.displayName) || "there";
    const advisorName =
      (Office.context.mailbox.userProfile &&
        Office.context.mailbox.userProfile.displayName) ||
      "";

    const draft = (data.draft || "")
      .replaceAll("[name]", studentName)
      .replaceAll("[Advisor name]", advisorName);

    item.displayReplyForm({ htmlBody: draft.replace(/\n/g, "<br>") });
  } catch (err) {
    showError("Could not draft a reply. Is the backend running?");
  } finally {
    btn.disabled = false;
    btn.innerText = originalLabel;
  }
}

// ─── Categorize Inbox ─────────────────────────────────────────────────────────

async function categorizeInbox() {
  const btn = document.getElementById("categorizeInboxBtn");
  btn.disabled = true;
  btn.innerText = "Categorizing…";

  hideCategorizeResults();
  showCategorizeLoading();

  try {
    // Step 1: get REST token
    const token = await getRestToken();
    const restUrl = Office.context.mailbox.restUrl;

    // Step 2: fetch 25 inbox messages (body as plain text)
    const messages = await fetchInboxMessages(restUrl, token, 25);

    // Step 3: batch-categorize via backend
    const emailPayload = messages.map((m) => ({
      id: m.Id,
      subject: m.Subject || "",
      body: (m.Body && m.Body.Content) || "",
    }));

    const catResponse = await fetch(`${BACKEND_URL}/categorize-batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emails: emailPayload }),
    });
    if (!catResponse.ok) throw new Error("Categorization backend error");
    const catData = await catResponse.json();

    // Step 4: ensure Outlook master categories exist, then tag each email
    await ensureOutlookCategories(restUrl, token);
    await Promise.all(
      catData.results.map((r) => applyOutlookCategory(restUrl, token, r.id, r.category))
    );

    // Step 5: render summary
    renderCategorySummary(catData.results);
  } catch (err) {
    showCategorizeError(err.message || "Could not categorize inbox.");
  } finally {
    btn.disabled = false;
    btn.innerText = "Categorize Inbox";
    hideCategorizeLoading();
  }
}

function getRestToken() {
  return new Promise((resolve, reject) => {
    Office.context.mailbox.getCallbackTokenAsync({ isRest: true }, (result) => {
      if (result.status === Office.AsyncResultStatus.Succeeded) {
        resolve(result.value);
      } else {
        reject(new Error("Could not get mailbox access token."));
      }
    });
  });
}

async function fetchInboxMessages(restUrl, token, count) {
  const url =
    `${restUrl}/v2.0/me/MailFolders/Inbox/Messages` +
    `?$top=${count}&$select=Id,Subject,Body`;
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

async function ensureOutlookCategories(restUrl, token) {
  // Fetch existing master categories
  const listResp = await fetch(`${restUrl}/v2.0/me/outlook/masterCategories`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const existingNames = new Set();
  if (listResp.ok) {
    const listData = await listResp.json();
    (listData.value || []).forEach((c) => existingNames.add(c.displayName));
  }

  // Create any that are missing
  await Promise.all(
    Object.values(CATEGORY_DISPLAY).map(async ({ name, color }) => {
      if (existingNames.has(name)) return;
      await fetch(`${restUrl}/v2.0/me/outlook/masterCategories`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ displayName: name, color }),
      });
    })
  );
}

async function applyOutlookCategory(restUrl, token, messageId, category) {
  const catInfo = CATEGORY_DISPLAY[category] || CATEGORY_DISPLAY.general;
  await fetch(`${restUrl}/v2.0/me/Messages/${messageId}`, {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ Categories: [catInfo.name] }),
  });
}

function renderCategorySummary(results) {
  // Group by category
  const counts = {};
  for (const r of results) {
    counts[r.category] = (counts[r.category] || 0) + 1;
  }

  const summaryEl = document.getElementById("categorize-summary");
  summaryEl.innerHTML = "";

  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  for (const [cat, count] of sorted) {
    const info = CATEGORY_DISPLAY[cat] || CATEGORY_DISPLAY.general;
    const row = document.createElement("div");
    row.className = "cat-row";
    row.innerHTML = `
      <span class="cat-dot" style="background:${info.hex}"></span>
      <span class="cat-name">${info.name}</span>
      <span class="cat-count">${count}</span>
    `;
    summaryEl.appendChild(row);
  }

  document.getElementById("categorize-results").classList.remove("hidden");
}

// ─── State helpers ────────────────────────────────────────────────────────────

function showCategorizeLoading() {
  document.getElementById("categorize-loading").classList.remove("hidden");
  document.getElementById("categorize-error").classList.add("hidden");
}

function hideCategorizeLoading() {
  document.getElementById("categorize-loading").classList.add("hidden");
}

function hideCategorizeResults() {
  document.getElementById("categorize-results").classList.add("hidden");
  document.getElementById("categorize-error").classList.add("hidden");
}

function showCategorizeError(msg) {
  const el = document.getElementById("categorize-error");
  el.innerText = msg;
  el.classList.remove("hidden");
}

function showLoading() {
  document.getElementById("result").classList.add("hidden");
  document.getElementById("error").classList.add("hidden");
  document.getElementById("loading").classList.remove("hidden");
}

function showError(msg) {
  document.getElementById("loading").classList.add("hidden");
  const el = document.getElementById("error");
  el.innerText = msg;
  el.classList.remove("hidden");
}
