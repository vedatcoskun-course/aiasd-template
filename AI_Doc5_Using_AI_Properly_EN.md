# Using AI Properly in Software Development — using it, checking it, explaining your decisions

*AIASD · Atlas University · Fall 2026–27 · Prof. Dr. Vedat Coşkun*
*This document goes with `AI_Doc4`. `AI_Doc4` explains what the tools are and how to use
them well. This document explains what to do with what they give you. It arrives with
Week 3, and it is the only course reading in English and in Turkish (`AI_Doc2`–`AI_Doc4`
are in English). It is part of the final exam: the exam has questions on it.*

---

## 0. Four people, one assistant

Give the same prompt — *"Write me a login endpoint that sends a four-digit code by e-mail
and checks it"* — to four different people. The assistant gives each of them almost the
same answer: about forty lines of code. In Week 1, the four repositories look identical.
By Week 5, they no longer do, and that difference is the subject of this document.

The four people differ in two ways. The first is whether they have the **concepts of
software engineering**: what a requirement is, what an interface is, what the status code
`429` means, what a test proves, what a version is, and what a risk is. The second is
whether they have the **discipline of using an assistant**: they treat its output as a
claim, not a fact; they check it; they record the decision; and they know where not to use
it at all. This course assumes that your degree programme teaches the first, and it
teaches the second. It grades the two together.

| | Without the assistant discipline | With the assistant discipline |
|---|---|---|
| **Without the engineering concepts** | This person pastes those lines, sees that the code runs, and pushes it. The first real user does not receive the code and asks for a second one a few seconds later. The endpoint simply sends a second code; nobody had thought about that case. When the first bug appears, this person "fixes" it by asking the assistant again, without reading the answer. The commit history is a single commit made on Saturday night. The product works in the demonstration and nowhere else. | This person writes a careful prompt, does not trust the answer, and asks a second assistant the same question. But he or she cannot say *what* to check. This person does not know that "a user asks for a second code within a minute of the first" is a case the code must handle. He or she has never seen the HTTP status `429 Too Many Requests` (the server's way of saying "too many requests: wait, then try again"). This person cannot write an acceptance criterion, because nobody has taught the concept yet. The doubt is right, but nothing gets verified. |
| **With the engineering concepts** | This person knows exactly what the endpoint should do, but is in a hurry. He or she accepts the assistant's changes without reading them line by line. This person pastes a real tester's e-mail address into the prompt as test data. He or she does not notice that the e-mail library the assistant chose was last updated two years ago. The concepts are there, but this person does not apply them to the assistant's output, because "it compiled". Or this person refuses to use the assistant at all and is three weeks behind by Week 6. | This person reads those lines against requirement REQ-001 ("a new code within 60 seconds gets 429"). He or she sends two requests for the same address within a minute and sees that a second code is sent. This person rejects the code, adds a test for that case, and commits the fix on its own, with a message that names it. He or she writes four lines in the AI log, with both server responses pasted. It is the same assistant and the same prompt, but a different engineer. |

In this course, the login is the course's own module from Week 6 (`server/course_login.py`),
the same for everyone. It already answers `429` to a second code within 60 seconds. The
example shows why such a rule is needed. You use the same thinking on your own feature.

Nothing in the right-hand column needs a different assistant or a better prompt. It needs
three things: you know what the output must do, you check whether it does it, and you
leave a record that someone else can read. The eight techniques below are ways to do these
three things. The examples under each technique carry the labels of the two columns:
**Untrained user** and **Trained in this course**. Each pair shows the same situation,
handled by two different people.

A student who starts without the engineering concepts can still reach the right-hand
column. Every technique below names the concept it needs and the week in which the course
teaches that concept. The order matters: the concept comes first, and the assistant comes
second.

---

## 0.1 The one sentence

This course does not grade what the assistant produced. It grades how well **you
specified, checked, corrected and explained** what it produced. An assistant can write
every file of an assignment in ten minutes. Each week, two points are for human
involvement, and most of them come from your `ai_log`. They are given for three things: the
moment you caught the assistant being wrong, the evidence you pasted, and what you did
about it.

Each technique below is a way to create that moment on purpose, instead of waiting for it.
Each week's assignment names the technique it expects, and the table in §10 shows the
whole term. You may use any technique in any week. From Week 4, one of them is compulsory
each week; in Weeks 2 and 3 the technique was suggested. Each week's AI log names the
technique it uses.

The techniques work inside the weekly routine you already know:

- the checker before every push;
- the commits in the middle of each piece of work in the lecture, and the reading of your
  repository at the end of the lecture;
- the Saturday 23:59 deadline;
- the ids in your `requirements.json`, and the Change log at the end of `PROPOSAL.md`;
- your group of four, which meets in the weeks whose assignment asks for it;
- `weekNN/group_NN.json` (`contributors_NN.json` in Weeks 2–3).

None of the techniques asks for a new file or a new habit. They say what goes into the
files you already push.

### Where the assistant sits in the twelve weeks

The same assistant is a different tool in each phase of your project. The table below
shows what it does well in each phase, what it often gets wrong, and which technique
catches the error.

| Phase (weeks) | What it does well | What it often gets wrong | Technique that catches it |
|---|---|---|---|
| Proposal and requirements (2–3) | It produces lists and structure quickly: eight requirements in a minute. | It does not know your priorities or your users. It gives numbers (market size, review time) for which it has no source. It adds features you never asked for, such as payments in an app that takes no money. | §4, §3, §5 |
| Prototype, test cases and design (4–5) | It writes screen flows, test cases, the components of the design and the architecture diagram from a short description. | It forgets a constraint unless you repeat it in every prompt. It adds one component too many. It gives a job to the wrong component (for example, the check-in to the login instead of to the bookings). | §1 |
| Server, login and clients (5–7) | It writes routine code, endpoints, tests, and the code that connects the server and the clients. | It misses edge cases: for example, two users book the same room for the same time, and the code accepts both bookings instead of refusing the second with 409. It installs library versions that have been removed or renamed since, so `pip install` fails. When asked for one change, it also makes a second change it does not mention. | §2, §3, §6 |
| The three tiers and the chatbot (8) | It writes each tier (server, web, mobile) correctly on its own, and the server code that calls the chatbot's LLM API. | It does not make the three tiers agree with each other: the same field is `room_id` on the server and `roomId` in the app; the server returns a status code that no client handles. It may put the API key in the app instead of in the server's `.env`. | §7, §9 |
| Testing with people (9–10) | It writes test plans, bug-report templates and a list of likely failures. | It cannot know what your testers will actually do, because it has never met them. | §8 |
| Store and release (11) | It writes checklists and the text of the store listing. | It quotes store rules as they were a year ago, and the review time for an established account, not for a new one. | §3, §5 |
| Closure and defence (12–14) | It writes summaries and the first draft of the poster. | It cannot say why you decided what you decided; only you know this, and you will be asked. | §9 |

Read the table from top to bottom. The assistant is most useful where the work is generic.
It is least useful where the work is about *your* product and *your* people. This course
trusts it less and less in the same order.

---

## 1. Acceptance criteria first

**What.** Before you ask for anything, write down how you will know that the answer is
right. Two or three lines in your own words are enough, written *before* the prompt. Then
include them in the prompt.

**Why.** A request without a test is a request for something plausible: something that
looks right. Models are very good at producing plausible things. "Write me the components
of the design for StudyRoom" returns a tidy table with a `Server: payments` component.
"Write me the components of the design for StudyRoom: at most five, no money anywhere, the
REQ ids that each one serves, and the check-in handled by the bookings component" returns
something you can check line by line. And the check is already written.

**Untrained user.** *"I asked Claude for the components of my design. They looked fine, so
I used them."*

**Trained in this course.** *"My criteria before asking were: at most five components, no
payment, the REQ ids of each one, and the check-in in the bookings component. The first
answer had seven components, including `Server: invoices`. The second prompt, with the
criteria pasted in, gave five components. But it put the check-in in `Server: login`, not
in `Server: bookings`. That is wrong: a check-in belongs to one booking, and one user has
many bookings. I fixed it by hand; the final table is in `week05/DESIGN.md`."*

**In the log.** Record the criteria you wrote first, the answer measured against them, and
what failed.

**In this course.** Your criteria already exist: they are the ids in `requirements.json`.
Their meaning has been fixed since Week 3, and they are your baseline from the end of
Week 5. Paste into the prompt the REQ lines that the design or the code must meet. An
answer that breaks a REQ is the error of the week. An answer that needs a REQ you do not
have is never added silently. Until the baseline, it gets a dated line in the Change log of
`PROPOSAL.md`. From the Sunday after Week 5, it is a **change request**: one line in the
Change log that begins with `CR-` and the next number, names the change and the ids, and
lists every file it affects (§9).

---

## 2. Verify by running, not by reading

**What.** If something can run, verify it by running it: run the code, send the request,
open the page on a phone, paste the Mermaid source into the preview. Reading the output and
agreeing with it is not verification.

**Why.** Generated code looks correct much more often than it runs correctly. The
assistant has not run it either; it has only seen a lot of code that looked like it.

**Untrained user.** *"Copilot generated the booking endpoint. The code looks right."*

**Trained in this course.** *"I ran the endpoint. A second booking for the same room and
the same start time was accepted (201) instead of being refused. My REQ-002 says that a
busy slot is refused, and my `api.md` row says 409. The two responses are pasted below. I
fixed it with a check before the booking is saved, and test TC-002-02 now catches it."*

**In the log.** Record the command you ran and its output (untouched, under `TERMINAL:` in
the Evidence block), and the fix.

**In this course.** The first run is always `python .github/check_deliverables.py`: before
every push in the lecture, and before Saturday 23:59. A red check is
evidence, so paste it. From Week 6, also look at the **Actions** tab after each push: a
test that passes only on your laptop does not count. The second run is on your own phone:
the app must work at phone width in every week, not only in Week 10.

---

## 3. The hostile reviewer

**What.** Give the assistant your own work and a role: the investor who wants to say no,
the store reviewer who wants to reject the app, or the tester or attacker who wants to
break it. Ask for the three strongest objections, numbered. Then **answer one of them** in
the document, and **show that one of them is wrong**, with evidence.

**Why.** Ask a model "Is this good?", and it says yes. Ask it "Why will this fail?", and
it gives a list. About one item in three is a real problem that you had not seen. The
other two teach you to disagree with it, with reasons.

**Untrained user.** *"I asked ChatGPT to review my proposal. It gave useful feedback, which
I applied."*

**Trained in this course.** *"Objection 2 was: 'Nobody will enter a reservation by hand;
they will just walk in.' This is true for the ground-floor rooms, so I added a QR check-in
to §4. Objection 3 was: 'The library already has a booking system.' I checked: the Atlas
library has none (I asked at the desk on 2026-10-07). I kept the project and wrote the
check into §9."*

**In the log.** Record the three objections word for word, which one you answered and
where, and which one you showed to be wrong, with what evidence.

**In this course.** In the weeks whose assignment asks for it, you have two hostile
reviewers: people and the assistant. Their comments go into different files.

- The people are the ones the assignment names: your group of four in Week 3, and an
  attacker in Week 6 (from your group, or any classmate). In Week 3 their sentences, quoted,
  go into `contributors_03.json`, with your `accepted` (true or false) and `why`. In Week 6
  you write `tried` and `happened` in `group_06.json` yourself, in your own words, and later
  your `accepted` and `why`.
- The assistant's objections go into `ai_log_NN.md`.

Put the two side by side. Where the assistant and the people disagree, the people are
usually right about *your* users. The assistant is usually right about the market or the
technology. Say which case it is, and why, in the `why` field. In Week 3 the reviewers were
the people in the room (slide 7 of `PITCH_03.md`). In Week 11 the role is the store
reviewer, with the store's own review guidelines (Apple App Review Guidelines, Google Play
policies).

---

## 4. Cross-examination: two assistants, one prompt

**What.** Give two different assistants exactly the same prompt and the same source text.
Compare the two answers with each other and with what you already know.

**Why.** Where two models agree, you have a candidate, not a fact. Where they disagree, at
least one of them is wrong. Finding out which one is the fastest way to a real error with
real evidence. This is the Week 2 technique, and it stays useful for the whole term.

**Untrained user.** *"Both gave similar requirements, so I merged them."*

**Trained in this course.** *"Claude wrote: 'The reservation expires after 15 minutes
without check-in.' Gemini wrote: 'after 2 hours.' Neither asked me. The right number is in
my §3: the problem is rooms held all afternoon by people who have left, so 15 minutes is
correct. I made it REQ-004 with my own acceptance criterion."*

**In the log.** Record the prompt once, the two answers (each one pasted whole under `AI:`,
exactly as it came; see the Evidence block in §9), and the decision.

**In this course.** This was the Week 2 exercise: the same §3–§4 went to two assistants,
each gave eight requirements, and you found one wrong requirement. Use the technique again
whenever two answers cost little and the truth is in your own documents: for example, the
design in Week 5 and the test plan in Week 9. The two assistants must be two of the ones
you chose in Week 1 (`week01/ASSIGNMENT_01` §5); the free tiers are enough.

---

## 5. Make it cite, and let it say "I don't know"

**What.** Ask for the source of every factual claim: a document, a page, or a line of your
own code. Tell the assistant clearly that "I don't know" is an acceptable answer. Then
**open the source**.

**Why.** Models write references as easily as everything else, and some of those
references do not exist. A fact you did not check is not a fact you know.

**Untrained user.** *"According to the AI, Google Play review takes one to three days."*

**Trained in this course.** *"I asked for the source of 'one to three days'. It gave a Play
Console help page. I opened the page (2026-10-08): it says that review 'can take up to 7
days or longer for new developer accounts'. §12 now says 7 days and cites the page. I asked
Gemini the same question; it said that it did not have a current figure, which was the
better answer."*

**In the log.** Record the claim, the source the assistant gave, and what the source
actually says.

**In this course.** In Weeks 3 and 10, every number in `PROPOSAL.md` §8–§12 and in the UAT
report carries its source: the page or the person it came from, with a date. This includes
store fees, review times and market sizes.

---

## 6. Small diffs: one change at a time, and read it

**What.** Ask for one change, not a rewrite. Read all of the diff before you accept it,
also the lines you did not ask to change. Commit each accepted change on its own.

**Why.** Ask "Refactor this file", and you get back a file in which three things you did
not ask for have changed, one of them without telling you. You can take responsibility for a
diff that you can read in two minutes. Small diffs also make your commit history readable
when the week's commit-discipline point is given.

**Untrained user.** *"I asked Copilot to clean up `server/tests/test_login.py`, accepted the
result, and pushed."*

**Trained in this course.** *"I asked only for the unused imports to be removed. The diff
also changed the code length that test TC-001-01 checks, from four digits to six. I had
not asked for that, and the assistant did not mention it. I rejected that hunk (that part
of the diff) and kept the import changes. `ruff` confirms the result; commit `e41c…`
contains the import changes only."*

**In the log.** Record the change you asked for, the change you received, and what you
refused.

**In this course.** This is what the weekly commit-discipline point looks for:

- **In the lecture:** commit each piece of work in the middle, commit it again when it works,
  and push every commit right away.
- **First push before 09:30** (from Week 7): run the checker at the start of the lecture,
  then commit and push. If your first push arrives after 09:30 (coming late included), I check
  by hand which computer your lecture work was made on.
- **Commit and push when I call it** (from Week 7): at any moment in the lecture I may ask
  everyone to commit and push at once; your push should reach GitHub within 5 minutes.
- **Outside the lecture:** at least two commits with new work, pushed at least one hour
  apart.
- GitHub's push time counts, not the date on a commit. A commit made by a coding agent
  never counts.
- **Never force push**, and never let an assistant do it.

Name the change in each commit message (for example `week06: REQ-002 busy slot answers
409, test added`). One big commit on Saturday night, which could have been pasted in whole,
does not earn the point. Run `ruff check .` and `ruff format .` before every commit. A key
in a commit costs ten points, and you must revoke the key, as the workflow document says.

---

## 7. Consistency across the three tiers

**What.** When the same feature exists in the server, the web client and the mobile client,
give the assistant all three and ask it to find the inconsistencies. Then verify the one it
finds, and look for the one it missed.

**Why.** Three pieces of generated code each agree with themselves, but not with each
other: a field is named `room_id` on the server and `roomId` in the app, or the server can
return a status that no client handles. Models are good at finding these when you ask.
When you do not ask, they find nothing.

**Untrained user.** *"Everything works on all three."*

**Trained in this course.** *"I asked for mismatches across `server/bookings.py`,
`web/book.html` and `mobile/api.dart`. It found `checked_in` versus `checkedIn`, which was
real, and I fixed it. It missed that the server returns `409 Conflict` for a double
booking, while the mobile client treats every answer except a success as a 'network error'.
I found that by testing (technique 2) and added the handling."*

**In the log.** Record what the assistant found, what you verified, what it missed, and how
you found it.

**In this course.** Your own feature runs on the server and the web from Week 6, and on
the mobile client from Week 7. In Week 8 the chatbot joins them: your server calls a
hosted LLM API of your choice (a free tier is enough), and the mobile client gets the chat
screen. The chatbot enters your requirements by a change request. Its API key lives only
in the server's `.env`: never in the app, never in the repository. By the end of Week 8
your feature runs on all three tiers. If your group meets that week, bring the
mismatch you found: the others have the same three tiers and often the same kind of
mistake.

---

## 8. Predicted versus observed

**What.** Before a test with people (the Week 9 beta test and the Week 10 UAT), ask the
assistant what will go wrong, and write the prediction down. After the test, place the
testers' real bug list next to it.

**Why.** This is the clearest way in the course to measure what a model knows about your
users: usually something, never everything. The gap between the two lists shows that
testing with people was necessary. It is also the paragraph that makes your test report
worth reading.

**Untrained user.** *"The testers found some bugs, which I fixed."*

**Trained in this course.** *"Predicted (five items): the login code not arriving, a slow
list, and so on. Observed (nine items from 14 testers): two of the five predicted items
happened. The most frequent complaint, 'I cannot tell which room is mine on the map', was
in no prediction. The table is in my test report in `week09/`."*

**In the log.** Record the prediction (dated, before the test), the observed list, and the
overlap between them.

**In this course.** The store decides how many testers you need. A new personal Google
Play account needs at least 12 testers who stay in a closed test for 14 days in a row
before the app can be released. Enrol them at S3, in Week 8, so that the 14 days end
before the submission in Week 10. Your testers are the five people of your pitch (slide 3
of `PITCH_03.md`) plus classmates and friends (role beta-tester in Week 9). The User
Acceptance Test (UAT) is in Week 10, with the five people of your pitch.

The prediction is dated in `ai_log_08.md` before the Week 9 lecture. The testers' list is
kept in `week09/`, and the UAT report in `week10/`. The testers install the app from the
store's test track (S3–S4). When five real people cannot use your product, that is the
most important finding of the term. It is the reason for a rule of this course: your
product is usable by real people around you, and those people test it.

---

## 9. The decision record: what the log is for

Your `weekNN/ai_log_NN.md` is **not a chat transcript**, and it is not a diary of how much
you used AI. It is an engineering record of one decision per week, in four parts:

| Part | The question it answers | It fails when it says |
|---|---|---|
| **Used for** | Which assistant, which prompt, and on which of your files? | "I used ChatGPT for the proposal." |
| **Got right** | What did you keep, and why was it right? | "It was helpful." |
| **Got wrong** | One concrete error, produced by the technique of the week | "Some things were not relevant." |
| **Evidence and fix** | The pasted output, and the change you made by hand | Nothing is pasted; "I fixed it." |

Each week's scaffold gives its own headings, but they ask these four questions.

The **Evidence** block is the part a person reads first. It shows the error instead of
describing it. Paste the rounds of the exchange that show the error; you may leave out
whole rounds that do not. The parts are:

- your prompt under `ME:`;
- the assistant's answer under `AI:`;
- when the week asks for it, the commands you ran and their output under `TERMINAL:`.

Every `ME:`, `AI:` or `TERMINAL:` part you keep is pasted whole, exactly as it came: from
Week 4, nothing removed, nothing corrected, not even the grammar. A log with no evidence
earns nothing, however long it is.

**The people in the loop.** The assistant is not your only reviewer, and it must not become
the only one. `weekNN/group_NN.json` (`contributors_NN.json` in Weeks 2–3) holds the people
that week's assignment names, with that week's role (the exact English word):
2 stakeholder · 3 reviewer · 4 collaborator · 5 nobody (you work alone) · 6 attacker · 7 tester · 8 test-user ·
9 beta-tester · 10 uat-participant · 11 release-tester · 12 poster-reviewer. Your group of
Week 3 stays your group; the assignment says in which weeks it meets and what for. When it
meets, bring that week's assistant error. The question "Did it fool you too?" is the
fastest cross-check there is. The entries in the file are those people: their words, or
what they did. The assistant has no entry there. One student, one computer, one GitHub
account: a log written on a classmate's computer is not yours. Questions to me are sent as an issue in your own
repository, which I read on Sundays.

### Four risks that are not about correctness

An answer can be correct and still be the wrong thing to ask for, or the wrong thing to
push. This project has four such risks, each in a particular week.

**Security.** Generated code likes to log things. In Week 6, a route that prints every
request with its token to the console "for debugging" leaks every login to anyone who can
read the server log. A route that never asks whose data it is lets any logged-in user read
or change everyone's data; the assistant that wrote it did not think of that user. An API
key in the repository costs ten points and must be revoked, whoever wrote the line. From
Week 8 this includes the chatbot's API key: it lives only in the server's `.env`. Read
generated code for what it *sends* and what it *stores*, not only for what it returns.

**Personal data.** The five people on slide 3, your testers' names and e-mail addresses
(Weeks 8–9), and the student numbers in `contributors_NN.json` and `group_NN.json` are
personal data. Names and numbers stay in your repository files; never paste them into a
hosted assistant. Describe the person ("a second-year classmate who works in the
evenings"); do not paste the person.

**Stale knowledge.** Every model learned from data up to a certain date, and mobile
frameworks and store rules keep changing after that date. An assistant may write code for
an old version of the Expo SDK or the Flutter API, and the code will not compile. It may
quote a Play Console policy that has changed. Treat every version number and every store
rule it gives you as a claim. Check it against the official page, and note the date of
your check (§5). When the error message does not match what the assistant said would
happen, the model is out of date, not you.

**Provenance** (where the code comes from). Code from an assistant may be a close copy of
code that someone else published under a licence. You would then break that licence
without knowing it. The rule for this project is simple. No block longer than a function
goes into the repository if you did not write it and cannot explain it line by line. A
library enters through `requirements.txt`, with its name and version; it is not pasted in.
In the defence you will be asked why a block of code is there, and "the assistant wrote
it" is not an answer. The push is yours, so the code is yours.

The log also carries two further rules:

- **A changed plan is written down.** A requirement you drop, a tier you simplify, or a
  store you switch to gets one dated line in the Change log of `PROPOSAL.md`, with the
  reason. From the Sunday after Week 5 (the baseline), every change to `requirements.json`
  or `test_cases.json`, a dropped requirement included, is a **change request**: one line
  in the Change log that begins with `CR-` and the next number, names the change and the
  ids, and lists every file it affects. Other changes (`api.md`, use cases, screens) get an
  ordinary dated Change log line. Changing your mind is engineering; changing it silently
  is not.
- **Some things are not done with an assistant at all.** You alone write these: your pitch
  (`PITCH_03.md`), the last time the problem happened to you, the five people who will
  test your product, the sentences your reviewers or attackers wrote, and what you decided
  about them. They are about your life and your people. An assistant cannot know them, and
  I will ask about them. **The AI log itself is on this list.** You write `ai_log_NN.md`
  yourself, in your own words; do not use an assistant even to improve the language. Your
  English or Turkish is not graded. A log in plain, imperfect sentences earns full marks; a
  log written by an assistant earns 0 from Week 4 on (at most 1 in Weeks 1–3). The
  assistant's words belong in the Evidence block, exactly as it wrote them. Outside the
  Evidence block, they may appear only in **bold**: a phrase, one sentence or one line of
  its code that you point at, copied letter for letter from the Evidence block. Use bold
  for nothing else.

---

## 10. The term, technique by technique

| Week | Deliverable the technique serves | Technique of the week | Status |
|---|---|---|---|
| 2 | Proposal Part A, requirements | §4 Cross-examination | suggested |
| 3 | Proposal Part B | §3 The hostile reviewer (the investor) | suggested |
| 4 | Clickable prototype, test cases from the acceptance criteria | §1 Acceptance criteria first | compulsory |
| 5 | Design, API contract, server skeleton, login tests | §2 Verify by running | compulsory |
| 6 | Your own feature end to end: server, tests, web page (the course's login wired in) | §3 The hostile reviewer (the attacker) | compulsory |
| 7 | The mobile client: the login and your feature | §6 Small diffs | compulsory |
| 8 | The chatbot: your server calls a hosted LLM API, the mobile client has the chat screen; your feature on all three tiers | §7 Consistency across the tiers | compulsory |
| 9 | Beta test, bug list, test report | §8 Predicted versus observed | compulsory |
| 10 | UAT report, submission | §5 Make it cite, applied to your own claims | compulsory |
| 11 | Release, review fixes | §3 The hostile reviewer (the store reviewer) | compulsory |
| 12 | Closure, poster | No new technique: §9 The term's log in retrospect (which error cost the most) | compulsory |

In Weeks 2 and 3 the technique was suggested; from Week 4 it is compulsory. You may use any
other technique in any week, in addition to the week's technique. Each week's
`ai_log_NN.md` scaffold says which technique the week uses (in its task note), and the
week's `ASSIGNMENT_NN` refers to this document. The two human-involvement points of every
week come mostly from the AI log, together with the hand-written files the week names.
They are read against this table: the technique of the week, applied, with the evidence pasted. In the weeks that
name people, `group_NN.json` is read alongside it.

---

## 11. What you can do in Week 14 that you could not do in Week 1

Each line below is a claim you can test on yourself. Each one marks a point at which one of
the four people in §0 is separated from the others.

1. Given a product idea, you can state what it must do and what it must not do, as
   numbered requirements with acceptance criteria, and hand those to an assistant *before*
   it writes a single line (§1, Weeks 2–4).
2. You can read a few dozen generated lines and say which requirement each part serves and which
   case it does not handle (§1, §2, Week 5).
3. You can tell a running program from a plausible one, because you ran it, and you can
   produce the output that shows the difference (§2).
4. You can take three strong objections to your own work, answer one of them in the
   document, and show that one of them is wrong by citing a source (§3, Weeks 3, 6 and 11).
5. You can give two assistants the same task, compare their answers and find the wrong
   one, with the reason taken from your own documents (§4).
6. You can tell a cited fact from an invented one, because you opened the source and dated
   it (§5, Weeks 3 and 10).
7. You can accept the change you asked for and refuse the one you did not, within the same
   diff. Your history shows a week of named changes, not one big commit (§6, the weekly
   commit-discipline point).
8. You can find where three generated tiers disagree with each other, verify what the
   assistant found, and catch what it missed (§7, Week 8).
9. You can write down what will go wrong before real people test your product (the beta
   testers in Week 9, the five people of your pitch in the UAT in Week 10), and place their
   list next to yours afterwards (§8).
10. You can keep your users' and classmates' names, numbers and e-mail addresses out of a
    hosted assistant, and keep a key out of a repository, as a habit rather than as a rule
    (§9).
11. You can say which version number and which store rule given to you by an assistant is
    out of date, and where you checked (§9).
12. You can stand in front of an examiner, with the app installed from the store, and
    answer the question "Why is this here?" for any line of it. You can do this because the
    push was yours and the record exists (§9, Weeks 13–14).

The untrained user with an assistant can do none of these things and does not know it.
The engineer without the discipline can do most of them and does not do them. The aim of
the twelve weeks is that you do what the right-hand column of §0 does, as a habit.

---

## 12. The short version

Write the test before the prompt. Run whatever can be run. Ask why it will fail, not
whether it is good. Give two assistants the same prompt, and look where they disagree.
Make the assistant cite its source, and open the source. Change one thing at a time, and
read the diff. Ask where your three tiers disagree, and check what it missed. Put the
prediction next to the result. Write down the decision, paste the
evidence, and keep your own life and your people out of the assistant.

The push is yours, so the code is yours: in the defence, "the assistant wrote it" is not an
answer to "Why is this here?". An assistant that is never caught being wrong is not a good
assistant; it is an assistant that nobody checked.
