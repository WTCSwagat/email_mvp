import re

import spacy

nlp = spacy.load("en_core_web_sm")


def bucket_gpa(match):
    """Convert a GPA number into a severity bucket instead of redacting entirely."""
    gpa = float(match.group(1))
    if gpa < 1.5:
        return "[GPA: critically low]"
    if gpa < 2.0:
        return "[GPA: below standing]"
    if gpa < 2.5:
        return "[GPA: marginal]"
    return "[GPA: standard]"
    
    # havent added the rest of the buckets yet


def scrub_pii(text: str) -> str: 
    # Layer 1: Regex for structured PII.

    # this trying to find gpa in two different ways
    
    # SSN (XXX-XX-XXXX) before the bare 9-digit ID rule so it isn't half-matched.
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]", text)
    # Date of birth only: requires a birth-related word right before the date, so
    # policy deadlines ("drop by 3/15") are left untouched.
    text = re.sub(
        r"\b(born|birth\s*date|DOB|date of birth)\b[^0-9\n]{0,15}"
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        "[DOB]",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\b\d{9}\b", "[STUDENT_ID]", text)
    # GPA: allow a few words between "GPA" and the number ("GPA dropped to 1.8"),
    # but stop before crossing another digit so we don't grab the wrong value.
    text = re.sub(
        r"GPA\b[^0-4\n]{0,25}?([0-4]\.\d{1,2})",
        lambda match: bucket_gpa(match),
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\b([0-4]\.\d{1,2})\s*(GPA|grade point)",
        lambda match: bucket_gpa(match),
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL]", text)
    # (?<!\d)...(?!\d) instead of \b so the leading "(" of "(865)" is included.
    text = re.sub(
        r"(?<!\d)(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)",
        "[PHONE]",
        text,
    )
    text = re.sub(r"\$[\d,]+(\.\d{2})?", "[AMOUNT]", text)
    # Grade fractions, but only with a grade word nearby ("got a 45/100"), so we
    # don't mistake a deadline date like "3/15/2025" for a grade. Keep the prefix
    # word, redact just the fraction.
    text = re.sub(
        r"(\b(?:scored?|got|grade[ds]?|earned|received|made|mark[eds]*)\b[^/\n0-9]{0,15})"
        r"\d{1,3}\s*(?:/|out of)\s*\d{1,3}\b",
        r"\1[GRADE]",
        text,
        flags=re.IGNORECASE,
    )

    # Layer 2: spaCy NER for unstructured PII.
    placeholder_spans = [
        (match.start(), match.end()) for match in re.finditer(r"\[[^\]]+\]", text)
    ]
    doc = nlp(text)
    redacted = text
    for ent in reversed(doc.ents):
        overlaps_placeholder = any(
            ent.start_char < end and ent.end_char > start
            for start, end in placeholder_spans
        )
        if overlaps_placeholder:
            continue
        if ent.label_ in ["PERSON", "ORG"]:
            redacted = (
                redacted[: ent.start_char]
                + f"[{ent.label_}]"
                + redacted[ent.end_char :]
            )
    return redacted
