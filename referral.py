REFERRAL_MAP = {
    "add_drop": {
        "office": "Registrar",
        "action": "Direct student to complete add/drop form before the posted deadline.",
        "link": "https://registrar.utk.edu/",
    },
    "major_change": {
        "office": "Academic Advising",
        "action": "Schedule a major change advising appointment.",
        "link": "https://advising.utk.edu/",
    },
    "failing_class": {
        "office": "Academic Support",
        "action": "Refer student to tutoring and academic support resources.",
        "link": "https://academicsupport.utk.edu/",
    },
    "financial": {
        "office": "One Stop Student Services",
        "action": "Direct student to One Stop for financial aid and scholarship questions.",
        "link": "https://onestop.utk.edu/",
    },
    "mental_health": {
        "office": "Counseling Center",
        "action": "Refer student to the UTK Counseling Center. If urgent, note crisis resources.",
        "link": "https://counselingcenter.utk.edu/",
    },
    "general": {
        "office": "One Stop Student Services",
        "action": "Direct student to One Stop for general advising questions.",
        "link": "https://onestop.utk.edu/",
    },
}


def get_referral(category: str) -> dict:
    return REFERRAL_MAP.get(category, REFERRAL_MAP["general"])
