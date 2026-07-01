"""24 fake student emails for seeding the demo inbox.

Each body STARTS with the student's name so the backend can detect which student
it is (get_dars in fake_dars.py scans the text for a known name). This matters
because browser-seeded emails all arrive from one address, so we match on the
NAME in the body, not the sender address.

Every name has a matching record in fake_dars.py and a canned answer in
demo_answers.py. Mental-health emails are NOT auto-drafted (handled in
main.py). The last email is a FERPA parent request.
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
    {"name": "Sam Rivera", "sender": "sam.rivera@vols.utk.edu", "scenario": "major_change",
     "subject": "Switching to Computer Science",
     "body": "Hi, my name is Sam Rivera. I want to switch from Psychology to Computer Science. How hard is it to change majors?"},
    {"name": "Jamie Chen", "sender": "jamie.chen@vols.utk.edu", "scenario": "failing_class",
     "subject": "Struggling in BIOL 130",
     "body": "Hi, my name is Jamie Chen. I think I'm going to fail BIOL 130. Are there tutoring options I can use?"},
    {"name": "Devon Parker", "sender": "devon.parker@vols.utk.edu", "scenario": "financial",
     "subject": "What does SAP mean?",
     "body": "Hi, my name is Devon Parker. I got an email saying my financial aid is at risk because of SAP. What does that mean and what do I do?"},

    # ---- Mental health -> NOT auto-drafted ----
    {"name": "Casey Nguyen", "sender": "casey.nguyen@vols.utk.edu", "scenario": "mental_health",
     "subject": "Feeling overwhelmed",
     "body": "Hi, my name is Casey Nguyen. I've been really overwhelmed and anxious lately and it's affecting my classes. I don't know who to talk to."},

    # ---- Hyper-specific -> should land as "no" (needs advisor judgment) ----
    {"name": "Chris Taylor", "sender": "chris.taylor@vols.utk.edu", "scenario": "no (hyper-specific)",
     "subject": "Complicated situation",
     "body": "Hi, my name is Chris Taylor. My situation is complicated — I had a family emergency, missed three weeks, my professor won't work with me, and I'm not sure whether to withdraw from everything or take an incomplete. What should I do?"},

    # ---- New scenarios (added incrementally) ----
    {"name": 'Nadia Osei', "sender": 'nadia.osei@vols.utk.edu', "scenario": 'transfer_credit',
     "subject": 'AP credit not showing up',
     "body": "Hi, my name is Nadia Osei. I took AP Chemistry in high school and scored a 4, but it's not showing on my transcript or DARS. Did it get applied?"},
    {"name": 'Ethan Brooks', "sender": 'ethan.brooks@vols.utk.edu', "scenario": 'grade_replacement',
     "subject": 'Retaking a class I failed',
     "body": 'Hi, my name is Ethan Brooks. I failed MATH 141 last semester and want to retake it. Will the new grade replace the old one, or will both show on my GPA?'},
    {"name": 'Fatima Hassan', "sender": 'fatima.hassan@vols.utk.edu', "scenario": 'incomplete_grade',
     "subject": 'Requesting an incomplete',
     "body": "Hi, my name is Fatima Hassan. I've had some serious family issues this semester and may not be able to finish my coursework on time. Can I request an incomplete grade, and how does that work?"},
    {"name": 'Derek Simmons', "sender": 'derek.simmons@vols.utk.edu', "scenario": 'academic_probation',
     "subject": 'Got a letter about academic probation',
     "body": "Hi, my name is Derek Simmons. I got a letter saying I'm on academic probation. What does that actually mean and what do I have to do to get off it?"},
    {"name": 'Leila Park', "sender": 'leila.park@vols.utk.edu', "scenario": 'credit_overload',
     "subject": 'Can I take 21 credit hours?',
     "body": 'Hi, my name is Leila Park. I want to take 21 credit hours next semester so I can graduate early. Do I need special permission for that?'},
    {"name": 'Owen Murphy', "sender": 'owen.murphy@vols.utk.edu', "scenario": 'graduation_audit',
     "subject": 'Am I on track to graduate in May?',
     "body": "Hi, my name is Owen Murphy. I'm a senior and I want to make sure I'm on track to graduate in May. Who do I talk to and what does the graduation application process look like?"},
    {"name": 'Simone Grant', "sender": 'simone.grant@vols.utk.edu', "scenario": 'double_major',
     "subject": 'Adding a second major',
     "body": "Hi, my name is Simone Grant. I'm a sophomore majoring in Economics and I want to add Political Science as a second major. Is that possible, and how do I do it?"},
    {"name": 'Brianna Scott', "sender": 'brianna.scott@vols.utk.edu', "scenario": 'waitlist',
     "subject": 'Stuck on waitlist for a required class',
     "body": "Hi, my name is Brianna Scott. I'm number 6 on the waitlist for PSYC 301, which I need for my major. What are my chances of getting in, and what should I do if I don't?"},
    {"name": 'Lucas Reyes', "sender": 'lucas.reyes@vols.utk.edu', "scenario": 'study_abroad',
     "subject": 'Study abroad and my financial aid',
     "body": "Hi, my name is Lucas Reyes. I'm thinking about studying abroad next fall. Will my UTK financial aid still apply, and will those courses count toward my degree?"},
    {"name": 'Imani Walker', "sender": 'imani.walker@vols.utk.edu', "scenario": 'no (hyper-specific)',
     "subject": 'Disputing a final grade',
     "body": 'Hi, my name is Imani Walker. I believe my professor calculated my final grade incorrectly — I should have gotten a B but got a D. I have all my graded work saved. How do I formally dispute this?'},
    {"name": 'Linda Carter (parent)', "sender": 'lindacarter1972@gmail.com', "scenario": 'FERPA (parent request)',
     "subject": "My son's grades",
     "body": "Hi, my name is Linda Carter and I'm the mother of Marcus Carter, a sophomore at UTK. Marcus hasn't been returning my calls and I'm very worried about him. His father and I are paying for his tuition and we just want to know if he's passing his classes and if everything is okay. Can you please tell me how he's doing academically? I don't understand why this information would be kept from his own parents."},

    # ---- Swagat Khot (real transfer scenarios: AP credit + Governor's School credit) ----
    {"name": "Swagat Khot", "sender": "swagat.khot@vols.utk.edu", "scenario": "ap_credit_gen_ed",
     "subject": "AP Art History credit toward Arts & Humanities requirement",
     "body": "Hi, my name is Swagat Khot. I'm writing to ask whether my AP Art History score of 4 can be applied toward the Arts & Humanities (VC) requirement. If it doesn't automatically count, I'd like to know whether it's possible to petition and what the process would be."},
    {"name": "Swagat Khot", "sender": "swagat.khot@vols.utk.edu", "scenario": "transfer_credit_governors_school",
     "subject": "Governor's School credits - where do they fit?",
     "body": "Hi, my name is Swagat Khot. I'll be having my pre-transfer advising meeting soon. I was also wondering how my Governor's School credits can be applied toward my coursework at UTK. Could you please let me know where these credits may fit?"},
]
