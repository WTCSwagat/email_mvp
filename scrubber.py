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
    
    text = re.sub(r"\b\d{9}\b", "[STUDENT_ID]", text)
    text = re.sub(
        r"\bGPA\s*[:\-]?\s*([0-4]\.\d{1,2})",
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
    text = re.sub(
        r"\b(\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "[PHONE]",
        text,
    )
    text = re.sub(r"\$[\d,]+(\.\d{2})?", "[AMOUNT]", text)
    text = re.sub(r"\b\d{1,3}/\d{1,3}\b", "[GRADE]", text)

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
