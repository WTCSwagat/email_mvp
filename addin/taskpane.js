const BACKEND_URL = "https://advise-assist-api.onrender.com";
const FEEDBACK_FORM_URL = ""; // TODO: paste your Google Form link

// The current email's draft, already hydrated with the real names, ready to insert.
let hydratedDraft = "";

Office.onReady((info) => {
  if (info.host === Office.HostType.Outlook) {
    analyzeEmail();
    Office.context.mailbox.addHandlerAsync(Office.EventType.ItemChanged, analyzeEmail);
    document.getElementById("insertBtn").addEventListener("click", insertReply);
    document.getElementById("thumbUp").addEventListener("click", openFeedback);
    document.getElementById("thumbDown").addEventListener("click", openFeedback);
  }
});

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

  // Names are filled in LOCALLY — they never went to the model.
  const studentName = (item.from && item.from.displayName) || "there";
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
    const d = data.dars;
    const holds = (d.holds && d.holds.length) ? d.holds.join(", ") : "no holds";
    document.getElementById("darsLine1").innerText = `${studentName} · ${d.major || ""}`;
    document.getElementById("darsLine2").innerText = `${d.credits_in_progress} cr · ${d.gpa} GPA · ${holds}`;
    show("darsCard");
  } else {
    hide("darsCard");
  }

  // Draft + insert button (not on "no")
  if (decision !== "no" && hydratedDraft.trim()) {
    document.getElementById("draftText").innerText = hydratedDraft;
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

  hide("loading");
  show("result");
}

function insertReply() {
  Office.context.mailbox.item.displayReplyForm({
    htmlBody: hydratedDraft.replace(/\n/g, "<br>"),
  });
}

function openFeedback() {
  if (FEEDBACK_FORM_URL) window.open(FEEDBACK_FORM_URL, "_blank");
}

function show(id) { document.getElementById(id).classList.remove("hidden"); }
function hide(id) { document.getElementById(id).classList.add("hidden"); }

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
