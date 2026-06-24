"""15 fake student emails for seeding the demo inbox.

Three groups:
  - DARS students (jordan.lee / priya.shah / marcus.bell): MUST be sent from those
    exact addresses so they match the keys in fake_dars.py -> personalized answers.
  - Fallback emails: sender doesn't matter (no DARS record) -> generic/KB answers.
  - One hyper-specific case -> should land as "no" (needs advisor judgment).

A send script (seed_inbox.py) can iterate this list. The @vols.utk.edu addresses
are cosmetic for the fallback group; only the 3 DARS addresses must be real senders
you control (or update the keys in fake_dars.py to whatever real addresses you use).
"""

FAKE_EMAILS = [
    # ---- DARS: jordan.lee (clean, full-time, no holds) -> "yes" ----
    {"sender": "jordan.lee@vols.utk.edu", "scenario": "DARS yes",
     "subject": "Dropping CHEM 120",
     "body": "Hi, I'm thinking about dropping CHEM 120 this semester — it's a lot harder than I expected. What happens if I drop it, and is it too late? Thanks, Jordan Lee"},
    {"sender": "jordan.lee@vols.utk.edu", "scenario": "DARS aid",
     "subject": "Will dropping a class hurt my scholarship?",
     "body": "I might drop one of my classes but I'm worried about my scholarship. Does dropping a class affect my financial aid? - Jordan"},

    # ---- DARS: priya.shah (advising hold) -> "partly" ----
    {"sender": "priya.shah@vols.utk.edu", "scenario": "DARS hold",
     "subject": "Trying to drop my stats class",
     "body": "I want to drop my statistics class but I think there's some kind of hold on my account. Can I still drop it? - Priya Shah"},
    {"sender": "priya.shah@vols.utk.edu", "scenario": "DARS major",
     "subject": "Declaring nursing",
     "body": "I'm currently pre-nursing and I want to officially declare the nursing major. What do I need to do, and do I qualify? Thanks, Priya"},

    # ---- DARS: marcus.bell (low GPA + bursar hold) -> "partly" ----
    {"sender": "marcus.bell@vols.utk.edu", "scenario": "DARS failing",
     "subject": "Failing thermodynamics",
     "body": "I'm failing my thermodynamics class and I'm pretty stressed. I don't know if I should drop it or push through. What are my options? - Marcus Bell"},
    {"sender": "marcus.bell@vols.utk.edu", "scenario": "DARS bursar/aid",
     "subject": "Bursar hold + worried about aid",
     "body": "There's a bursar hold on my account and I can't register. I'm also worried about losing my aid because of my grades. Help? - Marcus"},

    # ---- Fallback: no DARS record -> generic / KB answer ----
    {"sender": "taylor.morris@vols.utk.edu", "scenario": "fallback add_drop",
     "subject": "Drop deadline question",
     "body": "How late can I drop a class without it showing on my transcript?"},
    {"sender": "sam.rivera@vols.utk.edu", "scenario": "fallback major_change",
     "subject": "Switching to Computer Science",
     "body": "I want to switch from Psychology to Computer Science. How hard is it to change majors?"},
    {"sender": "jamie.chen@vols.utk.edu", "scenario": "fallback failing_class",
     "subject": "Struggling in BIOL 130",
     "body": "I think I'm going to fail BIOL 130. Are there tutoring options I can use?"},
    {"sender": "devon.parker@vols.utk.edu", "scenario": "fallback financial",
     "subject": "What does SAP mean?",
     "body": "I got an email saying my financial aid is at risk because of SAP. What does that mean and what do I do?"},
    {"sender": "casey.nguyen@vols.utk.edu", "scenario": "fallback mental_health",
     "subject": "Feeling overwhelmed",
     "body": "I've been really overwhelmed and anxious lately and it's affecting my classes. I don't know who to talk to."},
    {"sender": "riley.adams@vols.utk.edu", "scenario": "fallback general",
     "subject": "Planning next semester",
     "body": "Who do I talk to about planning my schedule for next semester?"},
    {"sender": "morgan.diaz@vols.utk.edu", "scenario": "fallback mental_health urgent",
     "subject": "Really struggling",
     "body": "I'm struggling a lot right now and feeling pretty hopeless. I don't know what to do."},
    {"sender": "alex.kim@vols.utk.edu", "scenario": "fallback general",
     "subject": "Academic calendar?",
     "body": "Where can I find the academic calendar and the registration dates for next term?"},

    # ---- Hyper-specific -> should land as "no" (needs advisor judgment) ----
    {"sender": "chris.taylor@vols.utk.edu", "scenario": "no (hyper-specific)",
     "subject": "Complicated situation",
     "body": "My situation is complicated — I had a family emergency, missed three weeks, my professor won't work with me, and I'm not sure whether to withdraw from everything or take an incomplete. What should I do?"},
]
