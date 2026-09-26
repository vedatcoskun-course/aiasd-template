# AIASD — The Term at a Glance

**AI-Assisted Software Development · Atlas University · Fall 2026–2027 · Prof. Dr. Vedat Coşkun**

*Türkçesi: [`AI_SKELETON_TR.md`](AI_SKELETON_TR.md)*

This is the whole term on two pages: what each week teaches, what you do in the room, what
you finish by Saturday, and what arrives in your repository. It is shown in the first lecture
and lives in your repository. It may change during the term; every change is logged at the
end of this file, the way you log changes to your own proposal.

## What holds every week

- You build **one project, alone, for the whole term**: a mobile client, a web client and a
  server, with login by e-mail code and/or OTP, **published on a public app store** by the
  end — which store, and native or hybrid, is your choice (`AI_PLATFORMS_AND_STORES_EN/TR.md`). The defence
  in Weeks 13–14 is run from the store-installed app.
- **Your project includes a chatbot about itself**, built in Weeks 6–7 with open-weight
  models you run yourself — BGE-M3 for embeddings, Qwen via Ollama for answers — over your
  own documents and data, reachable from both clients. No cloud model APIs for this feature.
- **10 points a week**: 5 read from your repository at the end of the lecture, 5 at Saturday
  23:59. Week 1 is worth 5, all read on Saturday. Term grade: weekly projects 60 · store
  bonus 15 · presentation (the defence, Weeks 13–14) 15 · final exam 40.
- **Two people help you every week** from Week 2, in the role that week names, and you record
  them in `weekNN/contributors_NN.json`. They earn a bonus from your mark; you earn one from
  theirs. Rotate: at least one new name each week.
- **You prove the human work**: yours in `weekNN/ai_log_NN.md`, theirs beside their names.
  Two of the Saturday points depend on that proof.
- **`PROPOSAL.md` lives at the root** and may change in any week — with a dated line in its
  change log. A silent change costs; a logged one is engineering.
- **Publishing is graded step by step** (S0–S6 in the plan), in the week each step is due.
  Nothing about the store can be done in the last week.
- **Every diagram is Mermaid**, inside the markdown file. GitHub draws it; the checker reads it.

How the points are computed, what the checker looks for, and the fine print of the bonus are
in `AI_WEEKLY_WORKFLOW_STUDENT_EN.md` / `_TR.md`.

## Weekly plan

### What happens each week

| Week | Content | In class | After class | Notes |
|---|---|---|---|---|
| 1 | Course intro; tools; Git; first contact with LLMs | • The assignment is explained step by step<br>• nothing is built yet | Install tools, create the private repo from the template, add the Collaborator, fill in student.json, write hello.py, explore two LLMs | • Worth 5 pts, all on Saturday (3 auto · 1 commits · 1 AI log)<br>• No contributors this week |
| 2 | Proposal Part A + Requirements (SRS) | • Write problem and solution<br>• interview two stakeholders<br>• start the requirement list | • Finish proposal Part A<br>• write the SRS with its diagrams | • Proposal lives at the root, revisable any week with a change-log line<br>• Role: stakeholder |
| 3 | Design + Proposal Part B | • Architecture<br>• market and competitors<br>• design reviewed by two | • Design document with its diagrams and the data model<br>• commercial potential<br>• technical risks incl. store choice | • S0: proposal §12 names store, fee, lead time<br>• Role: design-reviewer |
| 4 | Clickable prototype | • Build the main flow<br>• two testers walk it | • Complete the screen flow<br>• register the developer account | • S1: register today, verification takes days<br>• Role: prototype-tester |
| 5 | Prototype revision; development starts | • Revise the prototype on feedback<br>• server skeleton runs locally | Login by e-mail code / OTP working end to end | Role: prototype-tester (revision) |
| 6 | Chatbot I — the engine | • Ollama + Qwen running<br>• BGE-M3 embeddings over the project's own documents<br>• a chat endpoint on the server answers a question about the project | • Retrieval tuned (chunking, top-k)<br>• model notes: models tried, what they got wrong<br>• create the app record in the store | • S2: app record / bundle id<br>• Role: code-reviewer |
| 7 | Chatbot II — in the clients | Chat screen in the web client talking to the server | • Chat screen in the mobile client<br>• tests<br>• CI | • First feature live on all three tiers<br>• Role: chat-tester |
| 8 | Development — the project's own feature | The project's core feature on all three clients | • Feature complete<br>• upload the first build to a test track | • S3 starts the store's mandatory test period<br>• Role: test-user |
| 9 | Beta test | • Enrol testers on the track<br>• open the bug list | • Fix bugs<br>• write the test report | • Beta testers must match the store's testers<br>• Role: beta-tester |
| 10 | UAT + submission | Run the UAT session with participants | • UAT report<br>• deployment diagram<br>• submit for review | • S5 leaves a week for rejection and resubmit<br>• Role: uat-participant |
| 11 | Release + hardening | • Apply review fixes<br>• release-tester installs from the store | • Go live<br>• final README | • S6: live<br>• Role: release-tester |
| 12 | Closure | • Poster draft reviewed<br>• defence rehearsal | Final poster | • The defence itself is in Weeks 13–14, run from the store install<br>• Role: poster-reviewer |

### File flow — what the student receives and what she pushes

Assignments come as `_EN` and `_TR`; the suffix is omitted below. Readings (`AI_DocN`) are English. The lecture deck is not a file in the repository.

| Week | Handed out (arrives in `weekNN/`, or root) | Pushed by end of lecture (5) | Pushed by Saturday (5) |
|---|---|---|---|
| 1 | • `AI_Doc1`–`AI_Doc4` pre-reading (root)<br>• `week01/ASSIGNMENT_01`<br>• scaffolds `llm_notes.md`, `ai_log_01.md`<br>• root: `student.json`, `README`, `SETUP_CARD`, `WEEKLY_WORKFLOW_STUDENT` | — | • `student.json`<br>• `week01/setup_proof.md`<br>• `hello.py`<br>• `llm_notes.md`<br>• `ai_log_01.md` (all 5 pts) |
| 2 | • `week02/ASSIGNMENT_02`<br>• root `PROPOSAL.md` scaffold<br>• `week02/SRS.md` scaffold<br>• `requirements.json` scaffold<br>• `contributors_02.json`<br>• `ai_log_02.md`<br>| • `PROPOSAL.md` §1–§4<br>• `week02/requirements.json` first list<br>• `contributors_02.json` | • `PROPOSAL.md` §5–§7<br>• `week02/SRS.md` + diagrams<br>• `requirements.json` final<br>• `ai_log_02.md` |
| 3 | • `week03/ASSIGNMENT_03`<br>• `DESIGN.md` scaffold<br>• `contributors_03.json`<br>• `ai_log_03.md` | • `week03/DESIGN.md` architecture + diagram<br>• `PROPOSAL.md` §8–§10<br>• `contributors_03.json` | • `week03/DESIGN.md` diagrams + data model<br>• `PROPOSAL.md` §11–§12 + change log<br>• `ai_log_03.md` |
| 4 | • `week04/ASSIGNMENT_04`<br>• `store/store.json` scaffold<br>• `contributors_04.json`<br>• `ai_log_04.md` | • prototype link/file<br>• `contributors_04.json` | • full screen flow<br>• tester feedback log<br>• `week04/store/store.json` S1<br>• `ai_log_04.md` |
| 5 | • `week05/ASSIGNMENT_05`<br>• `contributors_05.json`<br>• `ai_log_05.md` | • revised prototype<br>• server skeleton<br>• `contributors_05.json` | • login working<br>• revision log<br>• `ai_log_05.md` |
| 6 | • `week06/ASSIGNMENT_06`<br>• `week06/requirements.txt` (Ollama client, sentence-transformers)<br>• `embedder.py`/`chat` scaffolds<br>• `model_notes.md` scaffold<br>• `contributors_06.json`<br>• `ai_log_06.md` | • `embedder.py`<br>• `chat` endpoint answering one question<br>• `contributors_06.json` | • retrieval over all project docs<br>• `week06/model_notes.md`<br>• `store.json` S2<br>• `ai_log_06.md` |
| 7 | • `week07/ASSIGNMENT_07`<br>• test + CI scaffold<br>• `contributors_07.json`<br>• `ai_log_07.md` | • chat screen in the web client<br>• `contributors_07.json` | • chat screen in the mobile client<br>• tests + CI green<br>• `ai_log_07.md` |
| 8 | • `week08/ASSIGNMENT_08`<br>• `contributors_08.json`<br>• `ai_log_08.md` | • core feature on all three clients<br>• `contributors_08.json` | • feature complete<br>• `store.json` S3 (first build, track)<br>• `ai_log_08.md` |
| 9 | • `week09/ASSIGNMENT_09`<br>• test report scaffold<br>• `contributors_09.json`<br>• `ai_log_09.md` | • testers enrolled (= `contributors_09.json`)<br>• bug list | • fixes<br>• test report<br>• `store.json` S4<br>• `ai_log_09.md` |
| 10 | • `week10/ASSIGNMENT_10`<br>• UAT report scaffold<br>• `contributors_10.json`<br>• `ai_log_10.md` | • UAT findings<br>• `contributors_10.json` | • UAT report<br>• deployment diagram<br>• `store.json` S5<br>• `ai_log_10.md` |
| 11 | • `week11/ASSIGNMENT_11`<br>• final README scaffold<br>• `contributors_11.json`<br>• `ai_log_11.md` | • review fixes<br>• `contributors_11.json` | • `store.json` S6 (store URL + web URL)<br>• final README<br>• `ai_log_11.md` |
| 12 | • `week12/ASSIGNMENT_12`<br>• poster spec<br>• `contributors_12.json`<br>• `ai_log_12.md` | • poster draft<br>• `contributors_12.json` | • final poster<br>• `ai_log_12.md`<br>• defence from the store install |

## Change log

- 21 Sep 2026 — v2, first version shown.
- 26 Sep 2026 — term grade per the syllabus (60 · 15 · 15 · 40, final exam); defence moved to Weeks 13–14.
- 26 Sep 2026 — store choice is the student's (any of four stores; native or hybrid), the Platforms and Stores handout (`AI_PLATFORMS_AND_STORES_EN/TR.md`) at the root; Week 1 readings are `AI_Doc1–4` at the root; `GRADING.md` reference replaced by the student workflow.
