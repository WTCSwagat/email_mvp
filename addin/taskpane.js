const BACKEND_URL = "https://arise-destinations-wiley-airline.trycloudflare.com";

Office.onReady((info) => {
  if (info.host === Office.HostType.Outlook) {
    analyzeEmail();
    Office.context.mailbox.addHandlerAsync(
      Office.EventType.ItemChanged,
      analyzeEmail
    );
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
