# AIASD — The Term at a Glance

**AI-Assisted Software Development · Atlas University · Fall 2026–2027 · Prof. Dr. Vedat Coşkun**

*Türkçesi: [`AI_SKELETON_TR.md`](AI_SKELETON_TR.md)*

This document is the whole term on two pages: it says what each week teaches, what you do
in the room, what you finish by Saturday, and what arrives in your repository. It is shown
in the first lecture and it lives in your repository. It may change during the term, and
every change is logged at the end of this file, in the same way that you log changes to
your own proposal.

## What holds every week

- You build **one project, alone, for the whole term**. The project is a mobile client, a
  web client and a server, with login by a 4-digit code sent by e-mail (from Week 6 the
  course's login module, the same in every project), and it is **published on a public
  app store** by the end of the term. Which store you use, and whether the app is native or hybrid, is
  your choice (`AI_PLATFORMS_AND_STORES_EN/TR.md`). The defence in Week 13 (in the EN section, Weeks 13–14) is run from
  the store-installed app.
- You earn **10 points a week**: 5 are read from your repository at the end of the lecture,
  and 5 at Saturday 23:59. Week 1 is worth 5, and all of them are read on Saturday. The
  term grade is made up of weekly projects 60 · store bonus 15 · presentation (the
  defence, Week 13; EN section Weeks 13–14) 15 · final exam 40.
- **In Week 3 you form a group of four** (five when the class does not divide by four) in
  the lecture. Your group of Week 3 stays your group; the assignment says in which weeks it
  meets and what for. In Week 3 the other members are your reviewers in
  `week03/contributors_03.json`. `weekNN/group_NN.json` holds the people that week's
  assignment names, with that week's role (the exact English word, in the Notes column
  below; in Week 5 nobody: you work alone). The people you name earn a bonus from your mark,
  and you earn one from theirs. In Week 2, contributors are optional.
- **You prove the human work**: you prove yours in `weekNN/ai_log_NN.md`, and your helpers
  prove theirs beside their names. Two of the Saturday points depend on that proof.
- **`PROPOSAL.md` lives at the root** and may change in any week, provided that you add a
  dated line to its change log. A silent change costs points; a logged change is
  engineering. **The project itself is fixed at the end of the Week 3 lecture (11:45)**: from
  then on its details may change, but not its problem or its product.
- **Change requests:** from the Sunday after Week 5 (the baseline), every change to
  `requirements.json` or `test_cases.json`, a dropped requirement included, is one line in
  the Change log of `PROPOSAL.md` that begins with `CR-` and the next number, names the
  change and the ids, and lists every file it affects.
- **Publishing is graded step by step** (the steps S0–S6 in the plan), in the week in
  which each step is due. Nothing about the store can be done in the last week.
- **Every diagram is Mermaid** (a text notation for diagrams), written inside the markdown
  file. GitHub draws it, and the checker reads it.

How the points are computed, what the checker looks for, and the fine print of the bonus
are in `AI_WEEKLY_WORKFLOW_STUDENT_EN.md` / `_TR.md`.

## Weekly plan

### What happens each week

| Week | Content | In class | After class | Notes |
|---|---|---|---|---|
| 1 | Course intro; tools; Git; first contact with LLMs (large language models) | • The assignment is explained step by step<br>• nothing is built yet | Install the tools, create the private repo from the template, add the Collaborator, fill in student.json, write hello.py and explore two LLMs | • The week is worth 5 pts, all read on Saturday (3 auto · 1 commits · 1 AI log)<br>• There are no contributors this week |
| 2 | Proposal Part A + requirements (`requirements.json`, the only place for them) + SRS (the use cases and the use case diagram) | • Write the problem and the solution<br>• interview up to two stakeholders (optional)<br>• start the requirement list | • Finish proposal Part A<br>• write the SRS + use case diagram (its §4 and §5 point to `requirements.json`) | • The proposal lives at the root, and you may revise it in any week with a change-log line<br>• Role: stakeholder |
| 3 | Pitch, review, Proposal Part B | • Form your group of four<br>• present your pitch in the group; the other three write their answers<br>• revise Part A and start the change log<br>• list the screens of the main flow; the project is fixed at the end of the lecture (11:45) | • Write Part B: market, competitors, comparison, commercial potential, technical risks with the store choice<br>• AI log: the assistant as a hostile reviewer<br>• make every acceptance criterion testable for Week 4 | • S0: §12 of the proposal names the store, the fee and the review time<br>• From Saturday a requirement id never changes its meaning; the list stays open until the baseline at the end of Week 5<br>• Role: reviewer; the group stays for the term |
| 4 | Clickable prototype and test cases | • Build the main flow as plain HTML screens<br>• write a test case for every must requirement<br>• your collaborator (one classmate you choose) runs them on the prototype (the walk-through); what they say, you write by hand | • Fix what failed; round 2 with your collaborator, online<br>• update the requirements and the test cases<br>• complete the screen flow<br>• open the developer account | • S1: apply on the day of the lecture, because the identity check takes days<br>• Role: collaborator |
| 5 | Design and API contract; development starts | • Write the design (the components and the REQ ids they serve)<br>• write the login rows of the API contract<br>• the server skeleton runs locally | • Write the API contract (every endpoint of the server)<br>• write the login tests from your test cases, named by their TC ids, before the code: they fail until the login exists in Week 6 | • On Saturday the requirements and the test cases become your baseline; after that a change goes through a change request (a `CR-` line in the Change log of `PROPOSAL.md`)<br>• No group work this week: you work alone, and there is no contributors' bonus |
| 6 | Your own feature, end to end | • The course's login wired in: `server/login_contract.json` by hand, the course tests LOGIN_01–06 pass on GitHub<br>• one functional `must` requirement of your own works on the server (no more 501), its tests, named by its test cases, pass on GitHub, and its prototype screen is a page of the web client, behind the login<br>• a groupmate attacks your feature and the login | • Every functional `must` requirement end to end: its `api.md` rows answer, its test cases with `run: server` have tests that pass on GitHub, and a page in `web/` serves it<br>• the course tests LOGIN_07–10 pass on GitHub<br>• the code arrives by real e-mail (`.env` stays out of the repository)<br>• your decision on each of the attackers' findings (`accepted`, `why`)<br>• create the app record in the store<br>• every test case says how it is run<br>• AI log: the assistant as a hostile reviewer of your feature | • The chain of every requirement: requirement → use case → screen → test case → `api.md` row → route → test green in GitHub Actions → web page; `requirements.json` is the source<br>• the login is the course's (`server/course_login.py`), the same for everyone<br>• S2: the app record / bundle id (the unique name under which the store knows your app)<br>• the lecture mark reads the GitHub Actions run<br>• Role: attacker |
| 7 | The mobile client | The login and a screen of your own feature run on a phone or an emulator and talk to the server | • Every functional `must` requirement on the phone too<br>• run the mobile test cases on a phone and record them (`run`: manual)<br>• the server and web tests stay green in GitHub Actions | • The login and your feature are live on all three tiers<br>• Role: tester |
| 8 | Development — the chatbot, and your feature complete | • The chatbot runs end to end: `POST /chat` on the server calls a hosted LLM API of your choice, and the mobile client has the chat screen<br>• the chatbot enters the requirements as a change request (your next CR number) | • Your own feature complete on all three clients<br>• upload the first build to a test track and enrol the testers on it (S3): 12 or more for a new personal Google Play account, so that the 14 days end before the submission in Week 10 | • The API key lives only in the server's `.env`: never in the app, never in the repository<br>• the cost of a paid API is yours; free tiers exist<br>• S3 starts the store's mandatory test period<br>• from Week 8 the server keeps its data across a restart: in a file or a database of your choice (SQLite comes with Python)<br>• Role: test-user |
| 9 | Beta test | • Run the beta test with the testers enrolled in Week 8<br>• open the bug list | • Fix the bugs<br>• write the test report<br>• the chatbot's tests, with a fake model instead of the real API<br>• the Report button on the chatbot's answers | • S4: the beta test runs on the store's test track (Week 9), with the testers enrolled at S3<br>• The beta testers must be the same people as the store's testers<br>• Role: beta-tester |
| 10 | UAT (User Acceptance Test, a session in which real users try the product) + submission | Run the UAT session with the participants | • Write the UAT report<br>• draw the deployment diagram<br>• submit the app for review | • S5 leaves a week for a rejection and a resubmission<br>• Role: uat-participant |
| 11 | Release + hardening | • Apply the review fixes<br>• the release-tester installs the app from the store | • Go live<br>• write the final README | • S6: the app is live<br>• Role: release-tester |
| 12 | Closure | • The poster draft is reviewed<br>• defence rehearsal | Finish the final poster | • The defence itself is in Week 13 (in the EN section, Weeks 13–14), and it is run from the store install<br>• Role: poster-reviewer |

### File flow — what the student receives and what she pushes

Assignments come as `_EN` and `_TR`, and the suffix is omitted below. The readings (`AI_DocN`) are in English, except `AI_Doc5`, which is in English and Turkish. The lecture deck is not a file in the repository.

| Week | Handed out (arrives in `weekNN/`, or root) | Pushed by end of lecture (5) | Pushed by Saturday (5) |
|---|---|---|---|
| 1 | • `AI_Doc1`–`AI_Doc4` pre-reading (root)<br>• `week01/ASSIGNMENT_01`<br>• the scaffolds (files that arrive with headings but no content) `llm_notes.md`, `ai_log_01.md`<br>• root: `student.json`, `README`, `SETUP_CARD`, `WEEKLY_WORKFLOW_STUDENT` | — | • `student.json`<br>• `week01/setup_proof.md`<br>• `hello.py`<br>• `llm_notes.md`<br>• `ai_log_01.md` (all 5 pts) |
| 2 | • `week02/ASSIGNMENT_02`<br>• root `PROPOSAL.md` scaffold<br>• `week02/SRS.md` scaffold<br>• `requirements.json` scaffold<br>• `contributors_02.json`<br>• `ai_log_02.md`<br>| • `PROPOSAL.md` §1–§4<br>• `week02/requirements.json` first list<br>• `contributors_02.json` | • `PROPOSAL.md` §5–§7<br>• `week02/SRS.md` + use case diagram<br>• `requirements.json` final<br>• `ai_log_02.md` |
| 3 | • `week03/ASSIGNMENT_03`<br>• `PITCH_03.md`<br>• `group_03.json`<br>• `contributors_03.json`<br>• `screens_03.md`<br>• `ai_log_03.md`<br>• root `AI_Doc5` | • `PITCH_03.md` (before the lecture)<br>• `group_03.json` (the same list for every member)<br>• `contributors_03.json` (three reviewers)<br>• `PROPOSAL.md` Part A revised + change log<br>• `screens_03.md` (the main flow) | • `PROPOSAL.md` §8–§12<br>• `requirements.json` updated<br>• `ai_log_03.md` |
| 4 | • `week04/ASSIGNMENT_04`<br>• `prototype/` with three starter screens<br>• `test_cases.json`, `walkthrough_04.json` and `store.json` scaffolds<br>• `group_04.json` (your collaborator)<br>• `ai_log_04.md` | • `week04/prototype/` (at least five screens)<br>• `test_cases.json` (every must)<br>• `walkthrough_04.json` (round 1)<br>• `group_04.json` | • the full screen flow (at least seven screens)<br>• round 2; `requirements.json` and `test_cases.json` updated<br>• `week04/store.json` S1<br>• `ai_log_04.md` |
| 5 | • `week05/ASSIGNMENT_05`<br>• `DESIGN.md` and `api.md` scaffolds<br>• the server starter<br>• `ai_log_05.md` | • `week05/DESIGN.md`, first version<br>• the login rows of `api.md`<br>• the server skeleton | • `week05/api.md`<br>• the login tests, named by TC id<br>• `ai_log_05.md` |
| 6 | • `week06/ASSIGNMENT_06`<br>• `server/course_login.py`, `course_tests/` and `server/login_contract.json`<br>• `group_06.json`<br>• `ai_log_06.md` | • `server/login_contract.json`; the login wired in<br>• one functional `must` requirement of your own: its routes, its tests, its page in `web/`<br>• `group_06.json` | • every functional `must` requirement end to end: routes, tests, pages<br>• course tests LOGIN_07–10 green on GitHub<br>• the code by real e-mail, `.env.example`, `email_code.png`<br>• `group_06.json`: `accepted` and `why` for each finding<br>• `store.json` S2<br>• `"run"` in `test_cases.json`<br>• `ai_log_06.md` |
| 7 | • `week07/ASSIGNMENT_07`<br>• `group_07.json`<br>• `ai_log_07.md` | • the login and a screen of your own feature in the mobile client<br>• `group_07.json` | • every functional `must` requirement in the mobile client<br>• the mobile test runs recorded<br>• the tests green in GitHub Actions<br>• `ai_log_07.md` |
| 8 | • `week08/ASSIGNMENT_08`<br>• `ai_log_08.md` | • the chatbot: `POST /chat` and the chat screen of the mobile client<br>• the change request line | • your own feature complete on all three clients<br>• `store.json` S3 (first build, track, testers enrolled)<br>• `ai_log_08.md` |
| 9 | • `week09/ASSIGNMENT_09`<br>• test report scaffold<br>• `group_09.json`<br>• `ai_log_09.md` | • the beta test with the testers enrolled in Week 8<br>• the bug list | • the fixes<br>• the test report<br>• the chatbot's tests and the Report button<br>• `store.json` S4<br>• `ai_log_09.md` |
| 10 | • `week10/ASSIGNMENT_10`<br>• UAT report scaffold<br>• `group_10.json`<br>• `ai_log_10.md` | • the UAT findings<br>• `group_10.json` | • the UAT report<br>• the deployment diagram<br>• `store.json` S5<br>• `ai_log_10.md` |
| 11 | • `week11/ASSIGNMENT_11`<br>• final README scaffold<br>• `group_11.json`<br>• `ai_log_11.md` | • the review fixes<br>• `group_11.json` | • `store.json` S6 (store URL + web URL)<br>• the final README<br>• `ai_log_11.md` |
| 12 | • `week12/ASSIGNMENT_12`<br>• poster spec<br>• `group_12.json`<br>• `ai_log_12.md` | • the poster draft<br>• `group_12.json` | • the final poster<br>• `ai_log_12.md`<br>• the defence from the store install |

## Change log

- 21 Sep 2026 — v2, first version shown.
- 26 Sep 2026 — term grade per the syllabus (60 · 15 · 15 · 40, final exam); defence moved to Weeks 13–14.
- 26 Sep 2026 — store choice is the student's (any of four stores; native or hybrid), the Platforms and Stores handout (`AI_PLATFORMS_AND_STORES_EN/TR.md`) at the root; Week 1 readings are `AI_Doc1–4` at the root; `GRADING.md` reference replaced by the student workflow.
- 4 Oct 2026 — Week 3 row and the contributors rule updated (pitch, groups of four, requirement ids permanent with the baseline at the end of Week 5).
- 4 Oct 2026 — Weeks 4 and 5 rewritten: Week 4 is the clickable prototype with test cases written from the acceptance criteria and run by the group; Week 5 is the design, the API contract, the server skeleton and the login, and the requirements and test cases become the baseline at its end. The `store.json` file lives in `week04/`.
- 5 Oct 2026 — Week 3: the project becomes fixed at the end of the lecture (11:45), and later only details may change, each with a change-log line; the screens of the main flow are listed in `week03/screens_03.md` during the lecture; the developer account (S1) may already be opened in Week 3; every member writes the same group list in `week03/group_03.json`.
- 6 Oct 2026 — From Week 4 the group and its contributions are one file, `weekNN/group_NN.json` (one entry for every other member); `contributors_NN.json` remains for Weeks 2–3. The Week 9 testers are listed in the test report.
- 18 Oct 2026 — The chatbot is removed from the course. Week 5 is split in two: Week 5 is the design, the API contract, the server skeleton and the login tests; Week 6 is the login by e-mail code on the server and in the web client (S2); Week 7 is the mobile client with the login, the tests and CI. Week 5 has no group work and no contributors' bonus.
- 20 Oct 2026 — The chatbot returns, through an API: in Week 8 the mobile client talks to the student's own server, and only the server calls a hosted LLM API of the student's choice (the key only in the server's `.env`). It enters the requirements as a change request; the project's core feature is completed by Saturday.
- 22 Oct 2026 — Week 6 written: the login works the same way in every project (a 4-digit code valid for 10 minutes and once, 429 for a new code within a minute, 401 for a wrong code, a 15-minute lock after three wrong codes), checked by ten course tests through `server/login_contract.json`; the lecture mark reads the GitHub Actions run; the web login page is the prototype's, served by the server; a groupmate attacks the login (role: attacker); by Saturday the code arrives by real e-mail and every test case says how it is run; S2.
- 22 Oct 2026 (evening) — Week 6 rewritten around the student's own feature: the login arrives ready as the course's module `server/course_login.py` (the same rules, wired in with `server/login_contract.json` by hand and checked by the ten course tests), and the week is the student's own functional `must` requirements end to end, each as one chain (requirement → use case → screen → test case → `api.md` row → working route → test green in GitHub Actions → web page; `requirements.json` is the source); the attacker round targets the student's feature. Week 7 brings the login and the feature to the phone; Week 8 completes the feature on all three clients next to the chatbot.
- 24 Oct 2026 — Plan correction: the testers are enrolled on the test track at S3, in Week 8 (12 or more for a new personal Google Play account, so that the 14 days end before the submission in Week 10); Week 9 runs the beta test with them. Also: the login is the 4-digit e-mail code (no OTP choice); the requirements live only in `requirements.json`, and the SRS holds the use cases and the use case diagram; change requests are `CR-` lines from the Sunday after Week 5; `group_NN.json` holds the people the week's assignment names, with the week's role (the group meets in the weeks the assignment names); Week 6 by Saturday also asks for LOGIN_07–10 and the decisions on the attackers' findings; `AI_Doc5` is in English and Turkish. Later the same day (VC): no fault check; from Week 8 the server keeps its data across a restart (a file or a database of the student's choice); Week 2 stakeholders are optional (0–2).
- 13 Nov 2026 — No lectures on 9–15 Nov: Weeks 8–13 are one week later (Week 8 on 17/18 Nov), and the defence is in Week 13 (22–23 Dec); the course ends on 23 Dec.
- 14 Nov 2026 — In the EN section, the defence takes Weeks 13 and 14 (22 and 29 Dec). The EN students whose app is live on the store and downloadable before the class starts on 22 Dec present then. The presentation itself is graded out of 12; a student whose app is live on the store and who presents in Week 13 gets the other 3 points (highest mark 15), and a student who presents in Week 14 can get at most 12.
- 14 Nov 2026 — The other 3 points of the presentation also require that the app was submitted to the store for review (S5) by Saturday 5 Dec 23:59. The time that the store takes for its review is the student's responsibility.
- 14 Nov 2026 — Week 8 is lighter: the chatbot's tests with a fake model and the Report button on its answers move to Week 9, and Week 8 has no group file. The privacy text is also published on a public page, because Google Play asks for a web address.
