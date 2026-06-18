// Client-side PII scrubber — proof of concept.
//
// Two layers, mirroring the Python backend (scrubber.py):
//   Layer 1: deterministic regex for structured PII (email, phone, SSN, ID,
//            GPA, DOB, graded scores, amounts). Fast, auditable, runs always.
//   Layer 2: transformers.js NER (Xenova/bert-base-NER) for names/orgs. This is
//            the part that replaces the server-side spaCy model and lets the
//            raw email never leave the device.
//
// Loaded as an ES module. The transformers.js import pulls the model from the
// HF CDN on first use (~100MB, cached afterwards) — see scrub_test.html for a
// harness that measures that load time.
//
// CAVEAT for Outlook on Mac: the phone regex uses a lookbehind (?<!\d), which
// older WKWebView builds don't support. Test on the target webview before
// shipping; a capture-group rewrite is the fallback if it throws.

import {
  pipeline,
  env,
} from "https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2";

// Don't look for local model files — fetch from the HF hub/CDN.
env.allowLocalModels = false;

// ── Layer 1: regex ──────────────────────────────────────────────────────────

function bucketGpa(gpa) {
  // Convert a GPA into a severity bucket instead of redacting the number flat.
  if (gpa < 1.5) return "[GPA: critically low]";
  if (gpa < 2.0) return "[GPA: below standing]";
  if (gpa < 2.5) return "[GPA: marginal]";
  return "[GPA: standard]";
}

export function scrubRegex(text) {
  // SSN (XXX-XX-XXXX) before the bare 9-digit ID rule so it isn't half-matched.
  text = text.replace(/\b\d{3}-\d{2}-\d{4}\b/g, "[SSN]");

  // Date of birth only: needs a birth word right before the date, so policy
  // deadlines ("drop by 3/15") are left untouched.
  text = text.replace(
    /\b(born|birth\s*date|DOB|date of birth)\b[^0-9\n]{0,15}\d{1,2}[/-]\d{1,2}[/-]\d{2,4}/gi,
    "[DOB]"
  );

  text = text.replace(/\b\d{9}\b/g, "[STUDENT_ID]");

  // GPA: allow a few words between "GPA" and the number ("GPA dropped to 1.8"),
  // but stop before crossing another digit so we don't grab the wrong value.
  text = text.replace(/GPA\b[^0-4\n]{0,25}?([0-4]\.\d{1,2})/gi, (_m, n) =>
    bucketGpa(parseFloat(n))
  );
  text = text.replace(/\b([0-4]\.\d{1,2})\s*(GPA|grade point)/gi, (_m, n) =>
    bucketGpa(parseFloat(n))
  );

  text = text.replace(/[\w.-]+@[\w.-]+\.\w+/g, "[EMAIL]");

  // (?<!\d)...(?!\d) instead of \b so the leading "(" of "(865)" is included.
  text = text.replace(
    /(?<!\d)(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)/g,
    "[PHONE]"
  );

  text = text.replace(/\$[\d,]+(\.\d{2})?/g, "[AMOUNT]");

  // Grade fractions, but only with a grade word nearby ("got a 45/100"), so a
  // deadline date like "3/15/2025" isn't mistaken for a grade. Keep the prefix
  // word, redact just the fraction.
  text = text.replace(
    /(\b(?:scored?|got|grade[ds]?|earned|received|made|mark[eds]*)\b[^/\n0-9]{0,15})\d{1,3}\s*(?:\/|out of)\s*\d{1,3}\b/gi,
    (_m, prefix) => prefix + "[GRADE]"
  );

  return text;
}

// ── Layer 2: NER ──────────────────────────────────────────────────────────────

let nerPromise = null;

export function initNER() {
  // Lazily build (and cache) the token-classification pipeline. First call
  // triggers the model download; subsequent calls reuse it.
  if (!nerPromise) {
    nerPromise = pipeline("token-classification", "Xenova/bert-base-NER");
  }
  return nerPromise;
}

function mergeEntities(tokens) {
  // Collapse B-/I- token tags and ## subwords into whole-entity spans using the
  // char offsets the fast tokenizer provides.
  const merged = [];
  for (const t of tokens) {
    if (t.start == null || t.end == null) continue; // offsets unavailable
    const type = t.entity.split("-").pop(); // PER | ORG | LOC | MISC
    const isBegin = t.entity.startsWith("B-");
    const last = merged[merged.length - 1];
    if (!isBegin && last && last.type === type && t.start <= last.end + 1) {
      last.end = t.end;
    } else {
      merged.push({ type, start: t.start, end: t.end });
    }
  }
  return merged;
}

const LABELS = { PER: "[PERSON]", ORG: "[ORG]" };

export async function scrubNER(text) {
  const ner = await initNER();
  const tokens = await ner(text);

  // Don't redact inside placeholders the regex layer already inserted.
  const placeholders = [...text.matchAll(/\[[^\]]+\]/g)].map((m) => [
    m.index,
    m.index + m[0].length,
  ]);

  const entities = mergeEntities(tokens)
    .filter((e) => LABELS[e.type])
    .filter(
      (e) => !placeholders.some(([s, end]) => e.start < end && e.end > s)
    )
    .sort((a, b) => b.start - a.start); // redact right-to-left to keep offsets valid

  for (const e of entities) {
    text = text.slice(0, e.start) + LABELS[e.type] + text.slice(e.end);
  }
  return text;
}

// ── Combined ────────────────────────────────────────────────────────────────

export async function scrubPII(text) {
  // Regex first (so names sit in clean context), then NER for names/orgs.
  return scrubNER(scrubRegex(text));
}
