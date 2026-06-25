"""15 fake student emails for seeding the demo inbox.

Each body STARTS with the student's name so the backend can detect which student
it is (get_dars in fake_dars.py scans the text for a known name). This matters
because browser-seeded emails all arrive from one address, so we match on the
NAME in the body, not the sender address.

Every name has a matching record in fake_dars.py. Mental-health emails are kept
to two and are NOT auto-drafted (handled in main.py).
"""

FAKE_EMAILS = [
    # ---- Jordan Lee (clean, full-time, no holds) -> "yes" ----
    {"name": "Jordan Lee", "sender": "jordan.lee@vols.utk.edu", "scenario": "DARS yes",
     "subject": "Dropping CHEM 120",
     "body": "Hi, my name is Jordan Lee. I'm thinking about dropping CHEM 120 this semester — it's a lot harder than I expected. What happens if I drop it, and is it too late?"},
    {"name": "Jordan Lee", "sender": "jordan.lee@vols.utk.edu", "scenario": "DARS aid",
     "subject": "Will dropping CHEM 120 hurt my scholarship?",
     "body": "Hi, this is Jordan Lee. If I drop CHEM 120 I'd be down to 9 credit hours — would that drop me below full-time and put my scholarship or financial aid at risk?"},

    # ---- Priya Shah (advising hold) -> "partly" ----
    {"name": "Priya Shah", "sender": "priya.shah@vols.utk.edu", "scenario": "DARS hold",
     "subject": "Trying to drop my stats class",
     "body": "Hi, my name is Priya Shah. I want to drop my statistics class but I think there's some kind of hold on my account. Can I still drop it?"},
    {"name": "Priya Shah", "sender": "priya.shah@vols.utk.edu", "scenario": "DARS major",
     "subject": "Declaring nursing",
     "body": "Hi, this is Priya Shah. I'm currently pre-nursing and I want to officially declare the nursing major. What do I need to do, and do I qualify?"},

    # ---- Marcus Bell (low GPA + bursar hold) -> "partly" ----
    {"name": "Marcus Bell", "sender": "marcus.bell@vols.utk.edu", "scenario": "DARS failing",
     "subject": "Failing thermodynamics",
     "body": "Hi, my name is Marcus Bell. I'm failing my thermodynamics class and I'm pretty stressed. I don't know if I should drop it or push through. What are my options?"},
    {"name": "Marcus Bell", "sender": "marcus.bell@vols.utk.edu", "scenario": "DARS bursar/aid",
     "subject": "Bursar hold + worried about aid",
     "body": "Hi, this is Marcus Bell. There's a bursar hold on my account and I can't register. I'm also worried about losing my aid because of my grades. Help?"},

    # ---- Other students (each has a DARS record too) ----
    {"name": "Taylor Morris", "sender": "taylor.morris@vols.utk.edu", "scenario": "add_drop",
     "subject": "Drop deadline question",
     "body": "Hi, my name is Taylor Morris. How late can I drop a class without it showing on my transcript?"},
    {"name": "Sam Rivera", "sender": "sam.rivera@vols.utk.edu", "scenario": "major_change",
     "subject": "Switching to Computer Science",
     "body": "Hi, my name is Sam Rivera. I want to switch from Psychology to Computer Science. How hard is it to change majors?"},
    {"name": "Jamie Chen", "sender": "jamie.chen@vols.utk.edu", "scenario": "failing_class",
     "subject": "Struggling in BIOL 130",
     "body": "Hi, my name is Jamie Chen. I think I'm going to fail BIOL 130. Are there tutoring options I can use?"},
    {"name": "Devon Parker", "sender": "devon.parker@vols.utk.edu", "scenario": "financial",
     "subject": "What does SAP mean?",
     "body": "Hi, my name is Devon Parker. I got an email saying my financial aid is at risk because of SAP. What does that mean and what do I do?"},
    {"name": "Riley Adams", "sender": "riley.adams@vols.utk.edu", "scenario": "general",
     "subject": "Planning next semester",
     "body": "Hi, my name is Riley Adams. Who do I talk to about planning my schedule for next semester?"},
    {"name": "Alex Kim", "sender": "alex.kim@vols.utk.edu", "scenario": "general",
     "subject": "Academic calendar?",
     "body": "Hi, my name is Alex Kim. Where can I find the academic calendar and the registration dates for next term?"},

    # ---- Mental health (max two) -> NOT auto-drafted ----
    {"name": "Casey Nguyen", "sender": "casey.nguyen@vols.utk.edu", "scenario": "mental_health",
     "subject": "Feeling overwhelmed",
     "body": "Hi, my name is Casey Nguyen. I've been really overwhelmed and anxious lately and it's affecting my classes. I don't know who to talk to."},
    {"name": "Morgan Diaz", "sender": "morgan.diaz@vols.utk.edu", "scenario": "mental_health urgent",
     "subject": "Really struggling",
     "body": "Hi, my name is Morgan Diaz. I'm struggling a lot right now and feeling pretty hopeless. I don't know what to do."},

    # ---- Hyper-specific -> should land as "no" (needs advisor judgment) ----
    {"name": "Chris Taylor", "sender": "chris.taylor@vols.utk.edu", "scenario": "no (hyper-specific)",
     "subject": "Complicated situation",
     "body": "Hi, my name is Chris Taylor. My situation is complicated — I had a family emergency, missed three weeks, my professor won't work with me, and I'm not sure whether to withdraw from everything or take an incomplete. What should I do?"},
]
