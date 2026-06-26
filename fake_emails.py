"""27 fake student emails for seeding the demo inbox.

Each body STARTS with the student's name so the backend can detect which student
it is (get_dars in fake_dars.py scans the text for a known name). This matters
because browser-seeded emails all arrive from one address, so we match on the
NAME in the body, not the sender address.

Every email has a matching DARS record (fake_dars.py) AND a canned answer keyed by
subject (demo_answers.py) — so the whole inbox runs deterministically on the demo
branch with no LLM calls. Mental-health emails are kept to two and are NOT
auto-drafted (handled in main.py). The last email is a FERPA case: a parent asking
for grades; the body names the son (Marcus Carter), whose record the advisor may
see but must not disclose without the student's written consent.
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
    
     # ---- Transfer credit / AP credit questions ----
    {"name": "Nadia Osei", "sender": "nadia.osei@vols.utk.edu", "scenario": "transfer_credit",
    "subject": "AP credit not showing up",
    "body": "Hi, my name is Nadia Osei. I took AP Chemistry in high school and scored a 4, but it's not showing on my transcript or DARS. Did it get applied?"},

    # ---- Repeat/grade replacement ----
    {"name": "Ethan Brooks", "sender": "ethan.brooks@vols.utk.edu", "scenario": "grade_replacement",
    "subject": "Retaking a class I failed",
    "body": "Hi, my name is Ethan Brooks. I failed MATH 141 last semester and want to retake it. Will the new grade replace the old one, or will both show on my GPA?"},

    # ---- Incomplete grade request ----
    {"name": "Fatima Hassan", "sender": "fatima.hassan@vols.utk.edu", "scenario": "incomplete_grade",
    "subject": "Requesting an incomplete",
    "body": "Hi, my name is Fatima Hassan. I've had some serious family issues this semester and may not be able to finish my coursework on time. Can I request an incomplete grade, and how does that work?"},

    # ---- Academic probation ----
    {"name": "Derek Simmons", "sender": "derek.simmons@vols.utk.edu", "scenario": "academic_probation",
    "subject": "Got a letter about academic probation",
    "body": "Hi, my name is Derek Simmons. I got a letter saying I'm on academic probation. What does that actually mean and what do I have to do to get off it?"},

    # ---- Overload / credit hour limit ----
    {"name": "Leila Park", "sender": "leila.park@vols.utk.edu", "scenario": "credit_overload",
    "subject": "Can I take 21 credit hours?",
    "body": "Hi, my name is Leila Park. I want to take 21 credit hours next semester so I can graduate early. Do I need special permission for that?"},

    # ---- Graduation application / audit ----
    {"name": "Owen Murphy", "sender": "owen.murphy@vols.utk.edu", "scenario": "graduation_audit",
    "subject": "Am I on track to graduate in May?",
    "body": "Hi, my name is Owen Murphy. I'm a senior and I want to make sure I'm on track to graduate in May. Who do I talk to and what does the graduation application process look like?"},

    # ---- Double major / second major ----
    {"name": "Simone Grant", "sender": "simone.grant@vols.utk.edu", "scenario": "double_major",
    "subject": "Adding a second major",
    "body": "Hi, my name is Simone Grant. I'm a sophomore majoring in Economics and I want to add Political Science as a second major. Is that possible, and how do I do it?"},

    # ---- Minor declaration ----
    {"name": "Aiden Flores", "sender": "aiden.flores@vols.utk.edu", "scenario": "minor_declaration",
    "subject": "How do I add a minor?",
    "body": "Hi, my name is Aiden Flores. I want to add a Spanish minor to my degree plan. What's the process for that and does it affect my graduation timeline?"},

    # ---- Waitlist question ----
    {"name": "Brianna Scott", "sender": "brianna.scott@vols.utk.edu", "scenario": "waitlist",
    "subject": "Stuck on waitlist for a required class",
    "body": "Hi, my name is Brianna Scott. I'm number 6 on the waitlist for PSYC 301, which I need for my major. What are my chances of getting in, and what should I do if I don't?"},

    # ---- Study abroad / transfer implications ----
    {"name": "Lucas Reyes", "sender": "lucas.reyes@vols.utk.edu", "scenario": "study_abroad",
    "subject": "Study abroad and my financial aid",
    "body": "Hi, my name is Lucas Reyes. I'm thinking about studying abroad next fall. Will my UTK financial aid still apply, and will those courses count toward my degree?"},

    # ---- Hyper-specific -> "no" (needs advisor judgment) ----
    {"name": "Imani Walker", "sender": "imani.walker@vols.utk.edu", "scenario": "no (hyper-specific)",
    "subject": "Disputing a final grade",
    "body": "Hi, my name is Imani Walker. I believe my professor calculated my final grade incorrectly — I should have gotten a B but got a D. I have all my graded work saved. How do I formally dispute this?"},

    # ---- Ferpa Issues -> Just added for now
    {"name": "Linda Carter (parent)",
    "sender": "lindacarter1972@gmail.com",
    "scenario": "FERPA (parent request)",
    "subject": "My son's grades",
    "body": "Hi, my name is Linda Carter and I'm the mother of Marcus Carter, a sophomore at UTK. Marcus hasn't been returning my calls and I'm very worried about him. His father and I are paying for his tuition and we just want to know if he's passing his classes and if everything is okay. Can you please tell me how he's doing academically? I don't understand why this information would be kept from his own parents."},

]
