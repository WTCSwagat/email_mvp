"""Pre-written 'perfect' answers for the demo emails, keyed by subject.

When an incoming email's subject matches one of these, main.py returns this canned
response directly — NO Groq calls — so the demo is perfect, instant, and works with
no API key / rate-limit / cold-start risk. Novel emails (no match) still use the
live AI pipeline, so the product is genuinely real — this just de-risks the script.

Keys MUST match the subjects in fake_emails.py exactly. Drafts use the student's
first name directly and keep [Advisor name] for the add-in to fill in locally.
"""

LINK = {
    "add_drop": "https://onestop.utk.edu/registration-records/add-drop-classes/",
    "major_change": "https://advising.utk.edu/",
    "failing_class": "https://academicsupport.utk.edu/",
    "financial": "https://financialaid.utk.edu/sap/",
    "mental_health": "https://counselingcenter.utk.edu/",
    "general": "https://onestop.utk.edu/",
}


def _ctx(category, text):
    return {"text": text, "link": LINK[category], "source": "verified knowledge base"}


DEMO_ANSWERS = {
    # ── Jordan Lee — Biology (prereq chain) ─────────────────────────────────────
    "Dropping CHEM 120": {
        "category": "add_drop", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Jordan,\n\nThanks for checking before you decide — this one has a bigger "
            "ripple than it looks. CHEM 120 is the prerequisite for CHEM 130 (spring), "
            "which is the prerequisite for Organic Chemistry (CHEM 350) and then Cell "
            "Biology (BIOL 330). Dropping CHEM 120 now means you can't take CHEM 130 in "
            "the spring, which pushes the whole chemistry sequence — and the upper-division "
            "biology courses that depend on it — back about a year, likely delaying "
            "graduation past Spring 2027.\n\nYou're also at 13 credit hours right now; "
            "dropping CHEM 120 (4 hrs) would put you at 9, below full-time. Before you "
            "decide, let's meet to see whether staying in with tutoring at the Math & "
            "Science Center keeps you on track.\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Confirm this term's add/drop deadline",
                      "Check full-time/aid impact of dropping below 12 hours with One Stop"],
        "context": _ctx("add_drop",
            "Students may drop without a 'W' until the posted add/drop deadline. Dropping "
            "below 12 hours ends full-time status. Course prerequisites are sequential, so "
            "dropping a gateway course can delay later required courses and graduation."),
    },
    "Will dropping CHEM 120 hurt my scholarship?": {
        "category": "financial", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Jordan,\n\nGood question to ask first. You're enrolled in 13 credit hours; "
            "dropping CHEM 120 (4 hrs) brings you to 9 — below the 12-hour full-time "
            "threshold. Most scholarships and financial aid require full-time enrollment, "
            "so dropping below 12 could put your scholarship and aid at risk this term.\n\n"
            "If you do need to drop CHEM 120, one option is to add another course before "
            "the add/drop deadline to stay at 12+ hours. I'd confirm the specifics with One "
            "Stop before dropping, since aid terms vary. Happy to walk through it together."
            "\n\nBest,\n[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("financial",
            "Most aid and scholarships require full-time enrollment (12+ hours). Dropping "
            "below 12 can affect eligibility for the term; verify specifics with One Stop."),
    },

    # ── Priya Shah — Pre-Nursing (hold + GPA gate) ─────────────────────────────
    "Trying to drop my stats class": {
        "category": "add_drop", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Priya,\n\nThanks for reaching out — two things to know before you drop "
            "STAT 201. First, there's an Advising Hold on your account, and it has to be "
            "cleared before any registration change (including a drop) can go through — "
            "let's meet so I can lift it. Second, STAT 201 is a required prerequisite for "
            "admission to the upper-division nursing program, so dropping it now would "
            "remove a prereq and push your nursing application back a full cycle (it runs "
            "once a year).\n\nGiven that, I'd encourage us to look at whether staying in "
            "with some support is workable. Can you stop by so we can clear the hold and "
            "talk it through?\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Meet to clear the Advising Hold before any drop can be processed"],
        "context": _ctx("add_drop",
            "An active Advising Hold blocks registration changes until cleared. Prerequisite "
            "courses are required for program admission; dropping one can delay an "
            "application cycle."),
    },
    "Declaring nursing": {
        "category": "major_change", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Priya,\n\nI'm glad you're thinking about declaring nursing. Here's where "
            "things stand: admission to upper-division nursing is competitive and requires "
            "a minimum 3.0 GPA plus the prerequisite block (Anatomy & Physiology I & II, "
            "Microbiology, Statistics, Nutrition). Your GPA is currently 2.71 — below the "
            "3.0 minimum — and you still have BIOL 239 and MICR 210 remaining.\n\nSo the "
            "path is doable, but we'd want a plan to raise your GPA above 3.0 and finish "
            "the prereqs before the application cycle. Let's meet to map it out semester by "
            "semester and talk through GPA-recovery options.\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Map a GPA-recovery plan to reach the 3.0 nursing minimum"],
        "context": _ctx("major_change",
            "Upper-division nursing admission is competitive: minimum 3.0 GPA plus completed "
            "prerequisites (A&P I/II, microbiology, statistics, nutrition). Applications are "
            "annual."),
    },

    # ── Marcus Bell — Mechanical Engineering (probation + prereqs) ──────────────
    "Failing thermodynamics": {
        "category": "failing_class", "urgency": "urgent", "decision": "partly",
        "draft": (
            "Hi Marcus,\n\nThank you for reaching out — let's get ahead of this together. "
            "A few important things from your record: Thermodynamics (ME 231) is a "
            "prerequisite for both Heat Transfer (ME 321) and Fluid Mechanics (ME 366), "
            "which gate the senior capstone (ME 450) — so failing or dropping ME 231 would "
            "delay graduation by about two semesters. There's also a Bursar Hold blocking "
            "any registration change until it's cleared, and because your GPA is 1.94 "
            "(below the 2.0 minimum) you're on academic probation, so a failing grade would "
            "deepen that.\n\nBefore deciding to drop or push through, let's meet this week — "
            "I can connect you with tutoring through Engineering Advising and we can build a "
            "recovery plan. You don't have to figure this out alone.\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Clear the Bursar Hold before any registration change",
                      "Connect with Engineering tutoring/academic support this week"],
        "context": _ctx("failing_class",
            "A GPA below 2.0 results in academic probation. Core engineering courses are "
            "sequential prerequisites, so failing one can delay graduation. Tutoring and "
            "academic support are available."),
    },
    "Bursar hold + worried about aid": {
        "category": "financial", "urgency": "urgent", "decision": "partly",
        "draft": (
            "Hi Marcus,\n\nI hear you — let's tackle both pieces. The Bursar Hold is "
            "blocking your registration; that's resolved through the Bursar's office "
            "(usually an outstanding balance), and One Stop can tell you exactly what's "
            "needed to clear it. On aid: your GPA is 1.94, below the Satisfactory Academic "
            "Progress (SAP) minimum, so your financial aid is genuinely at risk — but "
            "students who lose aid for SAP can file an appeal, and I can help with that. "
            "You're also at 12 hours; dropping below 12 would end full-time status and "
            "compound the issue.\n\nLet's meet this week to clear the hold, start a SAP "
            "appeal if needed, and build a plan.\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Contact the Bursar's office to clear the hold",
                      "Start a financial-aid SAP appeal with One Stop"],
        "context": _ctx("financial",
            "Financial aid requires Satisfactory Academic Progress (minimum GPA + "
            "completion rate). Students who lose aid can file a SAP appeal. A Bursar Hold "
            "blocks registration until resolved."),
    },

    # ── General fallback students (concise, solid) ──────────────────────────────
    "Drop deadline question": {
        "category": "add_drop", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Taylor,\n\nGreat question. You can drop a course without a 'W' on your "
            "transcript up until the posted add/drop deadline — typically the first two "
            "weeks of the semester. After that, a dropped course shows as a 'W' until the "
            "later withdrawal deadline. The exact dates are on the One Stop add/drop page. "
            "Just note that dropping below 12 hours affects full-time status. Happy to help "
            "you check the dates for your classes.\n\nBest,\n[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("add_drop",
            "Courses can be dropped without a 'W' until the posted add/drop deadline; after "
            "that a 'W' applies until the withdrawal deadline."),
    },
    "Switching to Computer Science": {
        "category": "major_change", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Sam,\n\nHappy to help you explore the switch to Computer Science. Changing "
            "majors goes through the destination department's advising office, and some "
            "programs (CS included) have entry requirements or GPA thresholds — so the "
            "first step is meeting with a CS advisor to confirm eligibility and map which "
            "of your current credits apply to the new degree. Want me to help set that up "
            "and review how the change affects your timeline?\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Confirm CS entry requirements with the CS advising office",
                      "Review which completed credits apply to the CS degree"],
        "context": _ctx("major_change",
            "Major changes are processed through the destination department; some programs "
            "are restricted or GPA-gated and require meeting an advisor first."),
    },
    "Struggling in BIOL 130": {
        "category": "failing_class", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Jamie,\n\nThanks for reaching out early — that's the best time to turn "
            "things around. UTK offers free tutoring and supplemental instruction for "
            "intro science courses through the Student Success Center; I'd start there this "
            "week. If things don't improve, we can talk through options before the "
            "withdrawal deadline. Let's set a quick check-in — you've got this.\n\nBest,\n"
            "[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("failing_class",
            "Free tutoring and academic support are available early; the withdrawal "
            "deadline is the cutoff for dropping with a 'W'."),
    },
    "What does SAP mean?": {
        "category": "financial", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Devon,\n\nGood question. SAP stands for Satisfactory Academic Progress — "
            "the standard you maintain to keep financial aid, including a minimum GPA and a "
            "minimum course-completion rate. If your aid is flagged at risk, one of those "
            "likely slipped. The good news: if you lose aid for SAP, you can file an "
            "appeal. I'd contact One Stop to see which requirement is at issue and your "
            "options — happy to help you prepare an appeal.\n\nBest,\n[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("financial",
            "Satisfactory Academic Progress (SAP) requires a minimum GPA and completion "
            "rate to keep aid; students who fall short can file an appeal."),
    },
    "Planning next semester": {
        "category": "general", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Riley,\n\nI'd be glad to help you plan next semester. The best starting "
            "point is your degree audit (DARS), which shows what you've completed and "
            "what's left — we can build your schedule around remaining requirements and "
            "any courses offered only certain terms. Want to set up a quick advising "
            "appointment? Registration dates are on the academic calendar in the "
            "meantime.\n\nBest,\n[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("general",
            "Schedule planning is best done from the student's degree audit (DARS) and the "
            "academic calendar for registration windows."),
    },
    "Academic calendar?": {
        "category": "general", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Alex,\n\nYou can find the academic calendar — registration windows, "
            "add/drop and withdrawal deadlines, and breaks — on the One Stop / Registrar "
            "site. Registration opens based on class standing, and your enrollment time "
            "ticket shows your exact date. Let me know if you'd like help planning around "
            "those dates.\n\nBest,\n[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("general",
            "The academic calendar lists registration windows and deadlines; registration "
            "timing is based on class standing (time ticket)."),
    },

    # ── Mental health — NO auto-draft (advisor responds personally) ────────────
    "Feeling overwhelmed": {
        "category": "mental_health", "urgency": "urgent", "decision": "no",
        "draft": "",
        "checklist": ["Respond personally and warmly",
                      "Share the UTK Counseling Center — free, confidential, 24/7 support"],
        "context": _ctx("mental_health",
            "The UTK Counseling Center offers free, confidential counseling and 24/7 crisis "
            "support. Respond personally; if the student may be in immediate danger, treat "
            "it as urgent and surface crisis resources right away."),
    },
    "Really struggling": {
        "category": "mental_health", "urgency": "critical", "decision": "no",
        "draft": "",
        "checklist": ["Reach out personally and promptly",
                      "Share the UTK Counseling Center 24/7 crisis line; if any risk of harm, escalate immediately"],
        "context": _ctx("mental_health",
            "Language suggesting hopelessness should be treated as urgent. The UTK "
            "Counseling Center provides 24/7 crisis support. Respond personally and "
            "promptly; if there is any risk of harm, escalate to crisis resources right away."),
    },

    # ── Hyper-specific — needs the advisor ─────────────────────────────────────
    "Complicated situation": {
        "category": "general", "urgency": "urgent", "decision": "no",
        "draft": "",
        "checklist": ["Meet with the student to understand the full situation",
                      "Discuss medical/hardship withdrawal vs. an Incomplete",
                      "Loop in the Dean of Students if it's a documented hardship"],
        "context": _ctx("general",
            "Documented emergencies may qualify for a hardship/medical withdrawal or an "
            "Incomplete, handled case-by-case with the instructor and the Dean of Students. "
            "This needs the advisor's judgment."),
    },

    # ── Nadia Osei — AP credit not posted ──────────────────────────────────────
    "AP credit not showing up": {
        "category": "general", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Nadia,\n\nGood catch. A score of 4 on AP Chemistry does earn UTK credit "
            "(it generally maps to CHEM 120), but it only posts once the official College "
            "Board score report reaches our Admissions/Registrar office — a self-reported "
            "score on your application isn't enough. Right now I don't see any AP credit on "
            "your record, which usually means the official report hasn't arrived.\n\nThe "
            "fix is to log in to College Board (apscores.org) and send your official scores "
            "to the University of Tennessee, Knoxville. Once it's processed, the credit "
            "should appear on your DARS. Want me to double-check it landed in a couple "
            "weeks?\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Have the student send official AP scores from College Board to UTK",
                      "Re-check DARS after processing to confirm the credit posted"],
        "context": _ctx("general",
            "AP credit is awarded per the UTK AP credit chart once an OFFICIAL College "
            "Board score report is received; self-reported scores do not post credit."),
    },

    # ── Ethan Brooks — grade replacement / course repeat ───────────────────────
    "Retaking a class I failed": {
        "category": "general", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Ethan,\n\nGood news on this one. Under UTK's course-repeat (grade-"
            "replacement) policy, when you retake MATH 141 the most recent grade is the one "
            "that counts in your GPA — so a passing grade would replace the F in the GPA "
            "calculation. The original attempt still appears on your transcript marked as "
            "repeated; it just stops dragging your GPA down.\n\nA couple of things to know: "
            "grade replacement applies to a limited number of repeats, so it's worth "
            "confirming MATH 141 is eligible before you register. Retaking it should give "
            "your GPA a solid lift. Want me to help you fit it into next term's "
            "schedule?\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Confirm MATH 141 is within the allowed grade-replacement limit with One Stop"],
        "context": _ctx("general",
            "UTK's course-repeat policy counts the most recent grade in the GPA for an "
            "allowed number of repeats; the original grade remains on the transcript "
            "marked as repeated."),
    },

    # ── Fatima Hassan — incomplete grade request ───────────────────────────────
    "Requesting an incomplete": {
        "category": "general", "urgency": "urgent", "decision": "partly",
        "draft": (
            "Hi Fatima,\n\nI'm so sorry you're dealing with this — let's look at your "
            "options. An Incomplete ('I') can be a good fit, but it has conditions: it's "
            "meant for students who have completed most of the course and just need more "
            "time to finish the remaining work because of circumstances like yours, and it "
            "requires your instructor's agreement on what's left and a deadline to "
            "finish.\n\nThe first step is talking with each instructor about where you "
            "stand in their class. If an Incomplete isn't the right fit, there may be other "
            "paths (like a hardship withdrawal), and the Dean of Students can help with "
            "documentation. Can we meet this week to figure out the best route?\n\nBest,\n"
            "[Advisor name]"
        ),
        "checklist": ["Student to discuss remaining work and a deadline with each instructor",
                      "If an Incomplete won't work, explore a hardship withdrawal via the Dean of Students"],
        "context": _ctx("general",
            "An Incomplete is granted at the instructor's discretion when most coursework "
            "is done and the rest can be finished by an agreed deadline; documented "
            "hardships may alternatively qualify for a withdrawal."),
    },

    # ── Derek Simmons — academic probation ─────────────────────────────────────
    "Got a letter about academic probation": {
        "category": "failing_class", "urgency": "urgent", "decision": "partly",
        "draft": (
            "Hi Derek,\n\nThanks for reaching out — probation sounds scarier than it is, "
            "and it's very recoverable. It means your cumulative GPA dropped below the 2.0 "
            "minimum (yours is currently 1.85). You're still enrolled; it's essentially a "
            "warning with some guardrails. To return to good standing you'll need to raise "
            "your cumulative GPA back to 2.0+, and the university usually asks for an "
            "academic-recovery plan — sometimes with a cap on credit hours so you can focus."
            "\n\nLet's meet to build that plan: pick the right course load, line up tutoring "
            "through the Student Success Center, and map how many terms it'll take to get "
            "back above 2.0. You can absolutely turn this around.\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Meet to build an academic-recovery plan",
                      "Connect with Student Success Center tutoring",
                      "Consider a reduced credit load for the recovery term"],
        "context": _ctx("failing_class",
            "A cumulative GPA below 2.0 results in academic probation. Returning to good "
            "standing requires raising the cumulative GPA to 2.0+, often via a recovery "
            "plan and academic support."),
    },

    # ── Leila Park — credit overload ───────────────────────────────────────────
    "Can I take 21 credit hours?": {
        "category": "add_drop", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Leila,\n\nGreat ambition — and yes, this is doable for you. The standard "
            "full-time load is up to 18 hours; anything above that (your 21) is an overload "
            "and needs advisor/college approval, which typically requires a GPA around 3.0 "
            "or higher. Your 3.72 clears that easily, so approval should be a formality.\n\n"
            "One honest note: 21 hours is a heavy term, so let's make sure the mix isn't all "
            "your hardest courses at once. If you stop by I can approve the overload and we "
            "can sanity-check the schedule against your early-graduation goal.\n\nBest,\n"
            "[Advisor name]"
        ),
        "checklist": ["Process the overload approval (GPA requirement met)",
                      "Review course mix so the 21-hour term is balanced"],
        "context": _ctx("add_drop",
            "Loads above 18 hours are overloads requiring advisor/college approval and "
            "generally a minimum GPA (around 3.0). Standard full-time is 12-18 hours."),
    },

    # ── Owen Murphy — graduation check ─────────────────────────────────────────
    "Am I on track to graduate in May?": {
        "category": "general", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Owen,\n\nExciting — you're close! By the numbers you're on track: 108 hours "
            "completed plus 12 in progress puts you right at the 120 you need. Two things "
            "make it official, though. First, you have to file your graduation application "
            "by the posted deadline for the May ceremony — graduation isn't automatic. "
            "Second, let's run a final degree audit together to confirm there are no "
            "lingering requirements (a specific gen-ed, an upper-division hour count, etc.) "
            "hiding in the details.\n\nWant to set up a graduation check this week so we can "
            "file the application and clear you for May?\n\nBest,\n[Advisor name]"
        ),
        "checklist": ["File the graduation application before the posted deadline",
                      "Complete a final degree audit to confirm all requirements are met"],
        "context": _ctx("general",
            "Graduating requires filing a graduation application by the deadline and "
            "passing a final degree audit confirming all requirements are complete."),
    },

    # ── Simone Grant — second major ────────────────────────────────────────────
    "Adding a second major": {
        "category": "major_change", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Simone,\n\nLove that you want to do both — adding Political Science as a "
            "second major is absolutely possible. It's declared through the Political "
            "Science advising office, and you'd complete the requirements for both majors "
            "to graduate. The main thing to plan for is time: depending on how much overlap "
            "there is with your Economics requirements and gen-eds, a second major can add "
            "a semester or two.\n\nSince you're a sophomore, you're at a great point to map "
            "this out before it affects your timeline. Want to meet so we can sketch a "
            "combined four-year plan and then set you up with a PoliSci advisor?\n\nBest,\n"
            "[Advisor name]"
        ),
        "checklist": ["Declare the second major through the Political Science advising office",
                      "Map a combined plan to see the effect on graduation timeline"],
        "context": _ctx("major_change",
            "A second major is declared through that department; all requirements for both "
            "majors must be completed, which can extend the time to graduate."),
    },

    # ── Aiden Flores — minor declaration ───────────────────────────────────────
    "How do I add a minor?": {
        "category": "major_change", "urgency": "routine", "decision": "yes",
        "draft": (
            "Hi Aiden,\n\nHappy to help — adding a Spanish minor is one of the easier "
            "things to set up. You declare it through the Spanish department (in Modern "
            "Foreign Languages); they'll add it to your degree plan. A minor usually runs "
            "about 15-18 hours.\n\nWhether it pushes your graduation back really depends on "
            "overlap: some of those Spanish courses can double-count toward your "
            "electives or gen-ed requirements, in which case it adds little or nothing. If "
            "you want, send me your remaining requirements and I'll show you how the minor "
            "fits into your remaining electives.\n\nBest,\n[Advisor name]"
        ),
        "checklist": [],
        "context": _ctx("major_change",
            "A minor (typically 15-18 hours) is declared through the offering department; "
            "courses that overlap with electives or gen-eds may limit any added time."),
    },

    # ── Brianna Scott — waitlist ───────────────────────────────────────────────
    "Stuck on waitlist for a required class": {
        "category": "add_drop", "urgency": "urgent", "decision": "partly",
        "draft": (
            "Hi Brianna,\n\nBeing #6 isn't bad, but let's not leave it to luck. Waitlists "
            "clear automatically as enrolled students drop, and movement is usually best in "
            "the last days before the term and the first week of add/drop — so keep an eye "
            "on it during that window. There's no guarantee you'll reach the top, though, "
            "so let's line up backups.\n\nOptions: enroll in another required course now so "
            "your schedule stays full, watch for a second section of PSYC 301 opening, or "
            "I can reach out to the instructor about an overfill since it's required for "
            "your major. Want me to email the department on your behalf?\n\nBest,\n"
            "[Advisor name]"
        ),
        "checklist": ["Enroll in a backup required course to keep the schedule full",
                      "Ask the instructor/department about an overfill for a required course"],
        "context": _ctx("add_drop",
            "Waitlists clear automatically as seats open, with the most movement near the "
            "term start; there is no guarantee of placement, so backups are advised."),
    },

    # ── Lucas Reyes — study abroad + aid ───────────────────────────────────────
    "Study abroad and my financial aid": {
        "category": "financial", "urgency": "routine", "decision": "partly",
        "draft": (
            "Hi Lucas,\n\nGreat idea, and the answer is mostly yes — with some planning. "
            "For UTK-sponsored and exchange programs, your federal aid and most "
            "institutional aid generally still apply, since you stay enrolled at UTK. The "
            "amount can shift on some programs, so the Programs Abroad office plus One Stop "
            "can give you exact figures for the program you pick.\n\nOn credit: study-abroad "
            "courses can count toward your degree, but only if they're pre-approved before "
            "you go — that step is what protects your graduation timeline. Let's meet to "
            "match courses to your remaining requirements and get them approved, then loop "
            "in Programs Abroad. \n\nBest,\n[Advisor name]"
        ),
        "checklist": ["Confirm aid amounts for the specific program with One Stop / Programs Abroad",
                      "Get courses pre-approved to count toward the degree before departure"],
        "context": _ctx("financial",
            "On UTK-sponsored/exchange programs federal and most institutional aid "
            "typically still applies; study-abroad courses count toward the degree only "
            "when pre-approved."),
    },

    # ── Imani Walker — grade dispute (needs advisor judgment) ───────────────────
    "Disputing a final grade": {
        "category": "general", "urgency": "urgent", "decision": "no",
        "draft": "",
        "checklist": ["Have the student first contact the instructor to ask how the grade was calculated",
                      "If unresolved, escalate to the department head, then the college, within deadlines",
                      "Help the student document their graded work and the timeline"],
        "context": _ctx("general",
            "UTK has a formal grade-appeal process: the student must start with the "
            "instructor, then escalate to the department head and college within published "
            "deadlines. This needs the advisor to guide it, not an auto-reply."),
    },

    # ── Linda Carter (parent) — FERPA: must NOT share the student's records ─────
    "My son's grades": {
        "category": "general", "urgency": "urgent", "decision": "partly",
        "draft": (
            "Hi Ms. Carter,\n\nThank you for reaching out, and I completely understand your "
            "concern for Marcus. I do want to help, so I want to be upfront about what I "
            "can and can't do. Under a federal privacy law called FERPA, the university "
            "isn't able to share a student's academic records — grades, enrollment, or "
            "standing — with a parent without the student's written consent, even when a "
            "family is supporting them through school.\n\nThe good news is there's an easy "
            "path: Marcus can file a FERPA release authorizing us to discuss his records "
            "with you, and then I'd be glad to talk specifics. In the meantime, I'd "
            "encourage you to keep reaching out to him, and I'll also make a note to connect "
            "with him directly to check in. Please don't hesitate to ask about general "
            "resources I *can* share, like tutoring and the counseling center.\n\nBest,\n"
            "[Advisor name]"
        ),
        "checklist": ["Do NOT share grades/standing without a signed FERPA release on file",
                      "Point the parent to the FERPA release the student can file",
                      "Consider reaching out to the student directly to check in"],
        "context": _ctx("general",
            "FERPA prohibits disclosing a student's education records to a parent without "
            "the student's written consent, even if the parent pays tuition. Direct the "
            "parent to the student-signed FERPA release process."),
    },
}


def get_demo_answer(subject: str) -> dict | None:
    """Return the canned response for this subject, or None if it's not a demo email."""
    if not subject:
        return None
    return DEMO_ANSWERS.get(subject.strip())
