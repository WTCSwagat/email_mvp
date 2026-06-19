const BACKEND_URL = "https://advise-assist-api.onrender.com";

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

      // Stash PII-free fields for the referral-draft request.
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
      document.getElementById("referralOffice").innerText = `\u2192 ${data.referral.office}`;
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

    // Fill placeholders LOCALLY — these names never leave the client.
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
