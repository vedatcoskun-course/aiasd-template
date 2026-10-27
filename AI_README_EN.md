# AIASD Project — Student Repository

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**
**Prof. Dr. Vedat Coşkun**

*Türkçesi: [`AI_README_TR.md`](AI_README_TR.md)*

---

## How to use this repository

This is your personal project repository (the folder of your project that git tracks,
on your computer and on GitHub) for the entire 12-week course. You create it from the
course template (a ready-made repository that GitHub copies for you) in Week 1, and you
commit to it every week (a commit is a saved snapshot of your files, recorded by git).

Each week arrives with its own assignment, in its own folder, and the assignment tells
you exactly what to build and what to hand in. [`AI_SKELETON_EN.md`](AI_SKELETON_EN.md)
describes the whole term on two pages: it says what each week teaches, what you push
(to push means to send your commits from your computer to GitHub) and when. During the
term you build one product, and it is yours: a mobile client, a web client and a
server. You publish it on a public app store of your choice, and at the end of the term
you defend it from the app that you installed from that store.

[`AI_OVERVIEW_EN.md`](AI_OVERVIEW_EN.md) lists the parts of your project (requirements, use cases,
screens, test cases, design, API contract, server, clients), how they must agree, and what must change
together when you change one of them.

Every week asks for an AI log (a written record of how you used an AI assistant
that week). The log is the file `weekNN/ai_log_NN.md`, inside that week's folder.

### How each week's files arrive

You do not create the week folders yourself. The checker brings them. (The checker is
the automatic script that looks for the files each week requires; see "Automatic checks"
below.) Each time you run `python .github/check_deliverables.py`, it:

- brings the folder of a new week when that week is published (`week02/`, `week03/` …),
  with its assignment and its starter files;
- brings every course document (`AI_*`) that changed at the root;
- from Week 6, also brings `course_tests/` and `server/course_login.py`, and
  `server/login_contract.json` if you do not have it;
- brings the `PROPOSAL.md` scaffold to the root (Week 2) and the `server/` starter
  (Week 5), only if you do not have them yet;
- never changes a file that you already have in a week folder.

Do not edit `course_tests/` or `course_login.py`: the checker puts the course's copy back,
and GitHub always uses it.

The new files are untracked until you run `git add .`, and the checker lists them. Write
your work into the files that arrive. Do not rename or move them: the checker looks for
each file at its exact path, and it names that path when a file is missing.

The following files and folders stay in your repository all term:

| | |
|---|---|
| `server/`, `web/` | Your product: the server (from Week 5) and the web client (from Week 6). The mobile client joins them in Week 7 |
| `week01/ASSIGNMENT_01_EN.md`, `_TR.md` | These files say what this week asks for, in both languages. They arrive together with the week's folder, and they are the only place where the tasks are written |
| `week01/ai_log_01.md` | This file is this week's AI log, and it sits in this week's folder. Every week has one, and it arrives together with the week |
| `student.json` | This file says who you are. Fill it in once, in Week 1 |
| `requirements.txt`, `weekNN/requirements.txt` | These files list the dependencies (the Python packages your app needs). They arrive week by week |
| `.github/` | This folder holds the checks that run on every push |
| `CURRENT_WEEK.txt` | The course writes this file; do not edit it. The first time you run the checker, a file called `CURRENT_WEEK_CACHE.txt` appears next to it. That file is the checker's offline cache (a saved copy of the week number). The template's `.gitignore` already keeps it out of git |

**Offline?** If the checker cannot reach GitHub, you can bring a week's files by hand.
Do it before you write anything in them:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git
git fetch template
git checkout template/main -- week06 course_tests server/course_login.py
```

You need the first line only once in the whole term. The last line overwrites the files
and folders that it names. So run it first, or do not run it at all. If you do not have
`server/login_contract.json` yet, add it to the end of the last line.

**Start here:** [`AI_SETUP_CARD_EN.md`](AI_SETUP_CARD_EN.md) / [`AI_SETUP_CARD_TR.md`](AI_SETUP_CARD_TR.md)
is one page that holds every command you will run all term, together with an
explanation of what the common errors mean. Do its four setup steps before Week 1.

**New here?** The whole weekly routine is written out step by step in
[`AI_WEEKLY_WORKFLOW_STUDENT_EN.md`](AI_WEEKLY_WORKFLOW_STUDENT_EN.md) /
[`AI_WEEKLY_WORKFLOW_STUDENT_TR.md`](AI_WEEKLY_WORKFLOW_STUDENT_TR.md). It says what you
do before, during and after each lecture, how the marks are split, and what to try when
you are stuck.

**Read before Week 1.** The three pre-readings and the paper are at the root. The
pre-readings are `AI_Doc2` AI Technical Background, `AI_Doc3` Development Environment
and Tools, and `AI_Doc4` Working with AI Tools. The paper is `AI_Doc1`, the Transformer
paper (the research paper behind today's AI assistants). The lecture is a twenty-minute
summary of these four documents. Later readings arrive in the same way, numbered in
order. `AI_Doc5` Using AI Properly in Software Development arrives with Week 3. It
describes the eight techniques that your weekly AI log asks for, and each week's log
names the technique that it uses. From Week 4, one technique is compulsory each week, and
this document is in the final exam.

Both sections receive the same files. The assignments, the setup card and the workflow
come in two languages, marked `_EN` and `_TR`. Read the one in your language and ignore
the other. The readings (`AI_DocN`) are in English, except `AI_Doc5`, which is in English
and Turkish. The folder and file names that the
checker looks for (`week01/`, `hello.py`, `student.json`) are the same for everyone.

---

## Running the server

```bash
python -m venv .venv
source .venv/bin/activate                         # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -r weekNN/requirements.txt  # the newest week that has one
uvicorn server.main:app --reload
```

The server arrives in Week 5. Then open http://127.0.0.1:8000/health in your browser: it
answers `{"status": "ok"}`. http://127.0.0.1:8000/docs lists every endpoint.

Dependencies arrive week by week, so that you do not download gigabytes of packages in
Week 1. The root `requirements.txt` is the minimum. A heavier week has its own
`weekNN/requirements.txt`, and that week's assignment tells you when to install it:

```bash
python -m pip install -r weekNN/requirements.txt
```

---

## Who you are — `student.json`

Fill in this file in Week 1, at the repo root:

```json
{
  "student_id": "230500000",
  "first_name": "Ayşe",
  "last_name": "Yılmaz",
  "nickname": "kaplumbaga",
  "section": "en"
}
```

Your **section** is `en` if you are in the English section, and it is `tr` if you are
in the Turkish one. If you get this wrong, the checker tests you against the other
section's week, so check it before you push.

Your **nickname** is the name that appears on the class board, which is projected at
the end of each lecture, so that you can find your own row at a glance. It may contain
letters, digits, `-` and `_`, and it must be 2–20 characters long. Choose whatever you
like, but pick something that you will still recognise in December.

Keep this repository **private** while the course runs, because it carries your student
number and your name.

---

## Automatic checks

Every push runs the same checks that your instructor runs. You see a green tick or a
red cross next to your commit in GitHub, and you can see exactly which check failed.

**There is nothing for you to switch on.** Every time the checker runs, it asks the
course which week it is, so what you see is always what is being run against you. The
`CURRENT_WEEK_CACHE.txt` file at the repo root is only a cache of that week number. It
updates itself, and you never need to touch it.

The output comes in two parts, because the week has two deadlines:

```
In the lab:     11 of 13 done
By Saturday:     2 of  8 done
```

**In the lab** is the part that the end-of-lecture snapshot reads (the snapshot is a
copy of your repository exactly as it is at that moment). Push by 11:45. The lecture
mark reads your last commit pushed by the end of the lecture (from Week 6, also its Actions run). This
part is worth five of the week's ten points. **By Saturday** is everything else, which means the write-ups, the
diagrams and `ai_log_NN.md`. Items in the second group do not fail the run while the
week is still open, because they are not due yet. Nothing in the first group is
something that you should be doing at home. (Week 1 is the exception: nothing is read
at the end of the first lecture, and all five of its points are read on Saturday.)

A **NOT YET** line waits for something that it names. It is neither passed nor failed, and
it does not count in "x of y".

**From Week 6, the lecture mark reads GitHub Actions.** The test results in your lecture
mark come from the GitHub Actions run of the last commit you pushed before the end of the
lecture. A test that passes only on your laptop does not count. Look at the **Actions** tab
after each push.

The checker shows one week: the current one. Under the list, one line tells you how many
checks of earlier weeks still fail, so a later change that breaks something earlier does
not stay unnoticed until December. (CI, the automatic checks that GitHub runs on every
push, runs the same checker and also looks at the current week.)

To look at another week, for example to confirm that Week 2 still passes, add its number:

```bash
python .github/check_deliverables.py 2
```

Run the checks locally (on your own computer) before you push:

```bash
python .github/check_deliverables.py
```

A red cross is not a grade. It is a list of what is still missing, and it is far better
to see that list on Tuesday than after the deadline.

**The secret scan runs on every push, at every week.** The secret scan searches your
files for API keys and tokens (not passwords). If an API key (a secret string that lets a program use a
service in your name) reaches the repository, the check fails. Remove the key,
rotate it immediately (that is, cancel the old key and create a new one), and remember
that a committed key is an automatic 10-point deduction.

---

## Repository rules

- **Commits and pushes:**
  - **In the lecture:** commit each piece of work in the middle, commit it again when it works, and push every commit right away. A piece that arrives finished in one commit does not count.
  - **Outside the lecture:** at least two commits with new work, pushed at least one hour apart.
  - GitHub's push time counts, not the date on a commit. A commit made by a coding agent never counts.
  - **Never force push**, and never let an assistant do it. If git refuses your push, run `git pull`, then `git push`.
  - A commit does not need to be a finished part. One push on Saturday night and nothing else costs you the commit-discipline point.
- Fill in that week's `ai_log_NN.md`. Every week has one, and a person reads it.
- Do **not** commit `.venv/`, `.env`, `__pycache__/`, `CURRENT_WEEK_CACHE.txt` or API keys. The template's `.gitignore` (the list of files that git must never commit) already lists the first four: keep them in it.
- Run `ruff check .` and `ruff format .` before committing (`ruff` is a tool that reports common mistakes in Python code and formats it). It catches the unused imports that AI tends to leave behind. On every push, GitHub's "Lint and format" job runs `ruff check .` and also `ruff format --check .`. The root `requirements.txt` installs the same version (`ruff==0.15.11`).
- Use `.env` (a small file that holds secret values) for secrets.
- Your app must work on a phone as well as on a laptop. Narrow your browser window to ~390px now and then. If something is cut off or scrolls sideways, fix it while the page is small, not in Week 10.
