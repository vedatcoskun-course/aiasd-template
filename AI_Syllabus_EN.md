# Course Syllabus

**Department of Software Engineering · Atlas University** · version 2 · 2026-10-24

*Türkçesi: [`AI_Syllabus_TR.md`](AI_Syllabus_TR.md)*

| | |
|---|---|
| **Course Code** | 1413002043 |
| **Course Name** | AI – Assisted Software Development |
| **Year & Semester** | 2026 – 2027 Fall |
| **Instructor** | Prof. Dr. Vedat COSKUN |

## Course Description

Students use AI as a disciplined engineering instrument across the software development life cycle. Each student builds one product alone for the whole term. The product consists of a mobile client, a web client and a server, and users log in with a 4-digit code sent by e-mail (the course's login module, the same in every project). The student publishes the product on a public app store: Google Play, Huawei AppGallery, Samsung Galaxy Store or Apple App Store. The app may be native (written in the platform's own language) or hybrid (written once for both platforms), and the student makes that choice.

The course grades the evaluation, not the generation: it does not grade what the assistant produced, but how well the student specified, checked, corrected and accounted for it. Every week's work is pushed to the student's own GitHub repository, which the student creates from the course template (a ready-made repository that GitHub copies for the student), and the work is checked automatically on every push.

## Course Objectives

On completing the course the student can:

1. **Write a project proposal.** The student starts from a real problem of their own and writes Part A: the problem and the solution, the stakeholders and the use cases. Part B analyses the market and the competitors, judges the commercial potential and lists the technical risks. The student pitches the proposal in five minutes (Weeks 2–3).
2. **Engineer requirements.** The student keeps the functional and non-functional requirements in one place, `week02/requirements.json`, and writes an SRS (Software Requirements Specification) with the use cases and the use case diagram. Every requirement carries an identifier of the form REQ-NNN, is traceable, and keeps its meaning once given. The requirements and the test cases enter a baseline at the end of Week 5; after that, every change is a change request (a `CR-` line in the Change log of `PROPOSAL.md`). Test cases are written from the acceptance criteria and walked through on the prototype (Weeks 2–5).
3. **Design and prototype.** The student draws four diagrams in Mermaid (a text notation for diagrams that GitHub draws inside a markdown file) in the repository: the system-context diagram and the use case diagram (Week 2), the architecture (Week 5) and the deployment diagram (Week 10). The student also builds a clickable prototype and revises it after peer review (Week 4).
4. **Develop a full-stack application.** The student builds a server with login by a 4-digit code sent by e-mail (the course's login module from Week 6), a web client and a mobile client, and the same feature runs on all three tiers. The product also gets a chatbot: the mobile client talks to the student's own server, and only the server calls a hosted LLM API (a large language model offered as a web service), with the key kept on the server (Weeks 5–8).
5. **Develop a mobile application.** The student builds the mobile client with Flutter, React Native–Expo, Kotlin or Swift, and the client runs on a phone and is ready for a store (Weeks 7–8).
6. **Use AI assistants as an engineering instrument.** The student prompts the assistant, verifies and corrects its output, documents its errors with evidence in a weekly AI log, and uses the assistant as a hostile reviewer of the student's own work. The course grades the evaluation, not the generation (every week).
7. **Practise version control and continuous integration.** The student commits and pushes in small steps, lets automatic checks run on GitHub, keeps the code quality up with ruff (a tool that reports style and error problems in Python code) and keeps secrets such as passwords out of the repository (every week: CI, continuous integration, runs on every push from Week 1, and the tests run in CI from Week 6).
8. **Run formal testing.** The student writes unit and integration tests, runs a beta test with enrolled testers, keeps a bug list, writes a test report, and runs a User Acceptance Test (a session in which real users try the product and say whether it meets their needs) with real users (Weeks 5–7, 9–10).
9. **Publish an application on a store.** The student follows the S0–S6 track (Weeks 3–11): they choose the store (S0), open a developer account (S1), create the app record (S2), upload a build and enrol the testers (S3), run the beta test on the test track (S4), submit the app (S5), and apply the review fixes and release the app (S6).
10. **Review and collaborate.** The student takes part in reviews in a fixed group of four (in the weeks that the assignment names), records the feedback as quotes with an accept or reject decision and a reason, and contributes to classmates' work as a stakeholder, a reviewer or a tester (from Week 3).
11. **Defend the product.** The student installs the app from the store in front of the examiner, justifies the decisions in the code and the documents, and prepares a poster and a presentation (Weeks 12–14).

## Course Material

The course template and the weekly assignments are at github.com/vedatcoskun-course/aiasd-template. Each week's `ASSIGNMENT_NN` is there in English and Turkish, and `AI_SETUP_CARD`, `AI_WEEKLY_WORKFLOW_STUDENT` and `AI_SKELETON` are at the root.

The pre-reading for Week 1 is the paper by Vaswani et al., "Attention Is All You Need" (2017), and three course documents in English: AI Technical Background; Development Environment and Tools; and Working with AI Tools. A fourth course document, Using AI Properly in Software Development (`AI_Doc5`), arrives with Week 3, in English and Turkish. It describes the eight techniques that the weekly AI log asks for (from Week 4 one technique is compulsory each week), and it is examinable. For Week 2 the students read two complete SDLC document sets (an exam-hall allocation system; a lift controller with a simulator) and the Platforms and Stores handout.

The tools are Python 3.12, Git/GitHub, VS Code, FastAPI for the server, HTML/CSS/JavaScript for the web client, two chat assistants of the student's choice on free tiers, a hosted LLM API of the student's choice for the product's chatbot, and one mobile framework (Flutter / React Native–Expo / Kotlin / Swift). Students bring their own laptop every week.

## Grading

| Item | Points | Explanation |
|---|---|---|
| Weekly Projects | 45 | 12 weeks × 10 points, scaled to 45 (Week 1 is worth 5 points, all read on Saturday). Each week:<br>• **Lecture, 5 points:** the automatic checks read the repository at the end of the lecture (from Week 6, the test results come from the GitHub Actions run).<br>• **Saturday 23:59, 5 points:** the automatic checks 2 · human involvement 2 (mostly the AI log, with the hand-written files the week names; marked by the instructor) · commit discipline 1 (marked by the instructor).<br>• **Commit discipline:** in the lecture, each piece of work committed in the middle and again when it works, every commit pushed right away (from Week 6; until Week 5, pushes near 10:00, 11:00 and 11:45), and from Week 7 the first push of the lecture before 09:30 (a later first push, coming late included, is checked by hand), and a commit and push within 5 minutes whenever the instructor calls for one; outside the lecture, at least two commits with new work, pushed at least one hour apart. GitHub's push time counts. A commit made by a coding agent never counts. The student never force pushes. Earlier weeks are consulted when something looks doubtful.<br>• Each classmate the week names (a contributor) earns 10% of the student's mark for that week.<br>• There is no make-up for a missed lecture. |
| Bonus-Store | up to 15 | Bonus for publishing. The store track S0–S6 is graded step by step, in the week each step is due: the student chooses the store (S0), opens a developer account (S1), creates the app record (S2), uploads a build and enrols the testers (S3), runs the beta test on the test track (S4), submits the app (S5), and the app goes live (S6). |
| Presentation | 15 | Project defence in Weeks 13–14. The student installs the app from the store in front of the examiner and answers questions about the decisions in the code and the documents. The app is run from the store build, not from a development machine. |
| Final Exam | 40 | Written final exam in the university's exam period. It covers the SDLC documents, the AI-log practice and the technical material of the twelve weeks. |

**Term grade:** Weekly Projects (45) + Presentation (15) + Final Exam (40) = 100. The store bonus adds up to 15 points. The term grade is at most 100.

## In-Class Rules

- A minimum of 70% attendance is mandatory. Every reason for an absence must fit within the remaining 30% allowance. So please try to attend all classes from the beginning, to keep some flexibility for urgent issues later.
- Keep conversations during class to a minimum. Extended or disruptive discussions are not permitted. A student who violates this rule will be asked to change their seat or to leave the room.
- Phone calls, text messages, instant messages, e-mail and general web surfing are not allowed during class time. Computers may be used only to follow the material of the class.
- Voice or video recording during the class is strictly forbidden.
- Cheating or academic dishonesty in any form will be dealt with according to the applicable legal rules.
- Any attempt to change your mark by anything other than your own work is cheating, whatever the method.

## Course Plan

| Week | Date | Subject |
|---|---|---|
| 1 | 22/09 · 23/09 | Foundations: the students set up the tools, learn Git/GitHub and meet LLMs (large language models) and transformers for the first time |
| 2 | 29/09 · 30/09 | Proposal Part A, the requirements (`requirements.json`) and the SRS (use cases and the use case diagram): the students describe the problem and the solution, name the stakeholders and write the use cases |
| 3 | 06/10 · 07/10 | Pitch and review in groups of four; Proposal Part B, in which the students analyse the market and competitors, judge the commercial potential and list the risks; the store is chosen (S0); from here a requirement id never changes its meaning |
| 4 | 13/10 · 14/10 | Clickable prototype and test cases: the students write test cases from their acceptance criteria, walk through them on the prototype and update the requirements; the developer account is registered (S1) |
| 5 | 20/10 · 21/10 | Design and API contract; development starts with the server skeleton and the first automated tests; requirements and test cases become the baseline (after it, every change is a change request) |
| 6 | 27/10 · 28/10 | The project's own feature, end to end: the course's login (a 4-digit code sent by e-mail) is wired in, and every functional `must` requirement works on the server, passes its tests in CI and has its page in the web client, from requirement to web page; the app record is created (S2) |
| 7 | 03/11 · 04/11 | The mobile client: the login screen runs on a phone and talks to the server; tests |
| 8 | 10/11 · 11/11 | The product's chatbot runs in the mobile client through the server and a hosted LLM API, and enters the requirements as a change request; the project's own core feature runs on all three tiers; the first build goes onto a test track, and the testers are enrolled on it (S3); from now on the server keeps its data across a restart (in a file or a database of the student's choice) |
| 9 | 17/11 · 18/11 | Beta test with the testers enrolled in Week 8: the students keep a bug list and write a test report (S4) |
| 10 | 24/11 · 25/11 | UAT and submission: the students write the UAT report and the deployment diagram, and the app is submitted for review (S5) |
| 11 | 01/12 · 02/12 | Release and hardening: the students apply the review fixes, the app goes live on the store and the final README is written (S6) |
| 12 | 08/12 · 09/12 | Closure: poster and defence rehearsal |
| 13 | 15/12 · 16/12 | **Project defence (presentations)** |
| 14 | 22/12 · 23/12 | **Project defence (presentations)** |
| | | **Final Exam** |

*Note: the weekly plan may be modified according to the progress of the class.*
