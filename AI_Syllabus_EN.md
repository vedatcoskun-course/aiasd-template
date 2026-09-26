# Course Syllabus

**Department of Software Engineering · Atlas University** · version 1 · 2026-09-21

*Türkçesi: [`AI_Syllabus_TR.md`](AI_Syllabus_TR.md)*

| | |
|---|---|
| **Course Code** | 1413002043 |
| **Course Name** | AI – Assisted Software Development |
| **Year & Semester** | 2026 – 2027 Fall |
| **Instructor** | Prof. Dr. Vedat COSKUN |

## Course Description

Students use AI as a disciplined engineering instrument across the software development life cycle. Each student builds one product alone for the whole term — a mobile client, a web client and a server with login by e-mail code/OTP, plus a chatbot about the project itself running on open-weight models — and publishes it on a public app store (Google Play, Huawei AppGallery, Samsung Galaxy Store or Apple App Store; native or hybrid, the student's choice).

The course grades the evaluation, not the generation: not what the assistant produced, but how well the student specified, checked, corrected and accounted for it. Every week's work is pushed to the student's own GitHub repository, created from the course template, and is checked automatically on every push.

## Course Objectives

On completing the course the student can:

- write requirements, design and test documents for a real product and keep them consistent as the product changes (Mermaid diagrams in the repository);
- use AI assistants (Claude, Gemini, ChatGPT, Copilot, Ollama) productively and critically — prompt, verify, correct, and document errors in a weekly AI log with evidence;
- build and run a retrieval-augmented chatbot on open-weight models (Ollama/Qwen, BGE-M3) over the project's own documents;
- work with Git/GitHub daily: small commits, CI checks, code quality (ruff), secrets kept out of the repository;
- take an application through a store's publication track — developer account, test track, testers, review, release — and defend the shipped product orally.

## Course Material

Course template and weekly assignments: github.com/vedatcoskun-course/aiasd-template (each week's `ASSIGNMENT_NN` in English and Turkish; `AI_SETUP_CARD`, `AI_WEEKLY_WORKFLOW_STUDENT` and `AI_SKELETON` at the root).

Pre-reading, Week 1: Vaswani et al., "Attention Is All You Need" (2017); AI Technical Background; Development Environment and Tools; Working with AI Tools. Week 2: two complete SDLC document sets (exam-hall allocation; lift controller with simulator); Platforms and Stores handout.

Tools: Python 3.12, Git/GitHub, VS Code, Streamlit, Ollama with an open-weight model, two chat assistants of the student's choice on free tiers, a mobile framework (Flutter / React Native–Expo / Kotlin / Swift). Students bring their own laptop every week.

## Grading

| Item | Points | Explanation |
|---|---|---|
| Weekly Projects | 60 | 12 weeks × 10 points, scaled to 60. Each week: 5 points read from the repository at the end of the lecture, 5 at Saturday 23:59 (Week 1: 5 points, all on Saturday). Automatic checks plus the instructor's marks for the AI log and commit discipline. No make-up for a missed lecture. |
| Bonus-Store | 15 | Bonus for publishing: the store track S0–S6 (store chosen, developer account, app record, test-track build, testers, submission, live) is graded step by step in the week each step is due, and the classmates who help each week (contributors) earn a share of the student's mark. |
| Presentation | 15 | Project defence in Weeks 13–14: the student installs the app from the store in front of the examiner and answers questions about the decisions in the code and the documents. Run from the store build, not from a development machine. |
| Final Exam | 40 | Written final exam in the university's exam period, covering the SDLC documents, the AI-log practice and the technical material of the twelve weeks. |

## In-Class Rules

- A minimum of 70% attendance is mandatory. All reasons must be accounted for within the remaining 30% allowance. So, please try to attend all classes as the beginning to allow you some flexibility for urgent issues.
- Minimize conversations during class. Extended or disruptive discussions are not permitted. Violators will be asked to change their seat or leave the room.
- Phone calls, text messages, instant messages, email, and general web surfing are not allowed during class time. Computers may only be used to follow the material in class.
- Voice or video recording during the class is strictly forbidden.
- Cheating or academic dishonesty in any form will be dealt with according to applicable legal rules.

## Course Plan

| Week | Date | Subject |
|---|---|---|
| 1 | 22/09 · 23/09 | Foundations — tools, Git/GitHub, first contact with LLMs and transformers |
| 2 | 29/09 · 30/09 | Proposal Part A + Requirements (SRS) — problem, solution, stakeholders, use cases |
| 3 | 06/10 · 07/10 | Design + Proposal Part B — architecture, data model, market, risks; store chosen (S0) |
| 4 | 13/10 · 14/10 | Clickable prototype; developer account registered (S1) |
| 5 | 20/10 · 21/10 | Prototype revision; development starts — server skeleton, login by e-mail code / OTP |
| 6 | 27/10 · 28/10 | Chatbot I — the engine: Ollama + Qwen, BGE-M3 embeddings, chat endpoint; app record (S2) |
| 7 | 03/11 · 04/11 | Chatbot II — in the web and mobile clients; tests; CI |
| 8 | 10/11 · 11/11 | The project's own core feature on all three tiers; first build on a test track (S3) |
| 9 | 17/11 · 18/11 | Beta test — testers enrolled, bug list, test report (S4) |
| 10 | 24/11 · 25/11 | UAT and submission — UAT report, deployment diagram, submitted for review (S5) |
| 11 | 01/12 · 02/12 | Release and hardening — review fixes, live on the store, final README (S6) |
| 12 | 08/12 · 09/12 | Closure — poster, defence rehearsal |
| 13 | 15/12 · 16/12 | **Project defence (presentations)** |
| 14 | 22/12 · 23/12 | **Project defence (presentations)** |
| | | **Final Exam** |

*Note: the weekly plan may be modified according to the progress of the class.*
