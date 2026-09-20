# Weekly Workflow — What You Do Each Week

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**

**Version 1 · 20 September 2026** — this document is revised during the term. It comes
down with the rest of each week's files when you fetch them, so the copy in your
repository is the current one as long as you keep pulling.

> [!IMPORTANT]
> **What changed in this version**
>
> Nothing yet — this is the first version. When I revise this document, this box
> lists what moved and the headings that changed carry a **`↻ changed in v2`** mark
> beside them. Both disappear in the version after, so anything marked is new to you.

This document describes the routine that does not change. The *content* of each week
differs — each week's assignment arrives in that week's folder — but the *rhythm* is
always the same.
Come back here when you are stuck.

---

## At a glance

| When | What you do | Points |
|------|-------------|--------|
| Before the lecture | Read `weekNN/ASSIGNMENT.md` | — |
| During the lecture (3 h) | Work, and push often | — |
| End of the lecture | One last push — I freeze the state | 5 |
| After the lecture | Finish the rest, write `ai_log_NN.md` | — |
| By Saturday 23:59 | **Push again.** I freeze the state a second time | 5 |

Ten points a week, split evenly between two moments: **five measured at the end of the
lecture, five at the Saturday deadline.** Both are read from GitHub, so both need a
push. Work that is finished but not pushed scores exactly the same as work that was
never done.

Half the week's mark riding on the lecture is deliberate. This is where the work
belongs — in the room, while you can still ask. The other half rests on finishing, and
on the two things a checker cannot see.

**The deadline is the same every week: Saturday 23:59.** There is nothing to work out —
whatever is in your repository at Saturday midnight is what I grade. Most of the work
should happen in the lab, where you can ask questions; the days after are for closing
gaps, not for starting.

---

## Once, and never again

Three things have to be true before the first lecture starts, and none of them are the
course: (a) a GitHub account, (b) your repository, and (c) a computer that is allowed to push to
it. The required commands are on the [**Setup Card**](SETUP_CARD.md) — four steps, and the last
one tells you whether the other three worked.

The card also carries a table of the errors you are most likely to hit and what each
one actually means. Keep it open; probably it is the only page you need for the mechanics.

---

## 1. Before the lecture of that week

Read `weekNN/ASSIGNMENT.md` — it comes down with the rest of the week's folder and
lists exactly which files that week requires. 

If there is pre-reading, read it before you arrive. 

---

## 2. During the lecture

### Know which half you are working on

From the root of your repository, run:

```bash
python .github/check_deliverables.py
```

It answers in two parts:

```
In the lab:     11 of 14 done
By Saturday:     0 of  3 done
```

The two numbers change from week to week; what matters is which line you are reading.

**In the lab** is what I read at the end of the lecture — half the week's mark. These
are the things worth doing while you are in a room with me and twenty-nine other
people who are stuck on the same thing.

**By Saturday** is the rest: the write-ups, the diagrams, `ai_log_NN.md`. Work that is
genuinely done alone. It does not fail the run during the week, because it is not due
yet — but it is half the mark too, and the snapshot on Sunday does read it.

If you find yourself writing `ai_log_NN.md` during the lab, you have the week backwards.

### Work, and push often

Commit as the work progresses rather than in one enormous lump at the end. The message
should say what you did:

```bash
git add .
git commit -m "week01: hello.py reads a name and prints the list"
git push
```

Messages like "update", "fix" or "asdf" cost you the commit-hygiene point.

### Run the checks yourself

The same command, as often as you like:

```bash
python .github/check_deliverables.py
```

These are exactly the checks I will run. The output lists what is missing, one line at
a time. It is not a grade; it is a to-do list, and running it costs nothing.

### Push once more before the lecture ends

At the end of the lecture I freeze every repository as it stands and run the checks.
Work you have not pushed is invisible — it sits on your laptop and does not count.

The result is projected as an anonymised table; find your row by the nickname in your
`student.json`. That table is worth **5 points — half the week**.

### Attendance, and what happens if you are not here

**Bring your laptop every week**, with its charger and whatever cable it needs. This is a three-hour hands-on study opportunity.

**Attendance is mandatory.** The university allows you some weeks of absence across the
term, and that allowance already covers everything — illness, work, family, anything at
all. There is no second category on top of it, and there is no make-up procedure.

**A lecture you miss is a lecture I cannot mark.** Whatever the reason, those 5 points
are gone. I am not weighing reasons against each other, and that is deliberate: with
over a hundred students, a process for judging excuses turns into a process for judging
who explains themselves best.

What stays open is the other half. Do the lecture's work in your own time, push it
before Saturday midnight, and you earn those five exactly as everyone else does. Missing
a lecture costs you that lecture, not the week.

---

## 3. After the lecture — until Saturday 23:59

Finish the rest of the week's work by Saturday midnight. I take a second snapshot at that time; your state at the deadline decides the other 5 points.

### `ai_log_NN.md` — do not skip it

One file per week, inside that week's folder — `week01/ai_log_01.md` and so on. It
arrives with the rest of the documents in the week folder. Fill in: which assistant you used, what it got right, what you had to
correct, and what you learned.

**The Evidence block is required.** Paste the actual exchange under your claim — the
prompt you sent and the wrong answer you got — inside the code fence. Not the whole
conversation: the ten or fifteen lines that show the error. A claim with an empty
Evidence block earns nothing.

Why: anyone can write "the AI made a mistake and I fixed it". A real model output is
hard to fabricate convincingly — invented transcripts read too cleanly and their errors
are conveniently easy to spot. And choosing which part of a long conversation counts as
evidence is itself the skill being assessed.

If you would rather keep the whole conversation, save it as `weekNN/transcript.md`. I do
not read those by default, but I will read it when a log entry does not add
up.

This file is worth 2 points.

### Keep going until the checks are green

```bash
python .github/check_deliverables.py
git add .
git commit -m "week01: llm_notes written up"
git push
```

The **Actions** tab of your repository on GitHub shows the result of every push. A green
tick on your Saturday state is worth **2 points**.

### The 3 points that are not automated

**Consistency and commit discipline — 1 point.** Does this week's work actually follow
from the requirements and design you wrote in previous weeks, and does your commit
history show work spread across the week rather than one last-minute dump? Changing your
mind is normal and healthy — but the change must be visible. A silently abandoned
requirement costs the mark; a requirement dropped with a one-line justification in
`ai_log_NN.md` costs nothing. That is what engineering looks like.

**`ai_log_NN.md` quality — 2 points.** A concrete AI error, the pasted evidence, and how
you noticed.

An LLM can produce every file an assignment asks for. What it cannot do is make those
files agree with the ten weeks around them, or notice its own mistakes on your behalf.
That is what is actually being assessed.

---

## 4. Rules that apply every week

**Never put an API key in your code.** It lives in `.env`, and `.env` is in
`.gitignore`. If a key reaches the repository the automatic scan catches it and you lose
**10 points**. Once a key has been pushed, deleting it is not enough — it stays in the
git history. You must revoke that key and issue a new one.

**Keep the code clean.** Before pushing:

```bash
ruff check .          # list problems
ruff check . --fix    # fix what can be fixed automatically
ruff format .         # format
```

AI-generated code frequently leaves unused imports behind; `ruff` catches them instantly.

**Your app must work on a phone.** Narrow your browser to about 390 pixels now and then.
If something is cut off or scrolls sideways, fix it while the window is small — not in
Week 10.

**Do not break earlier weeks.** The checks are cumulative: in Week 5, Weeks 1 to 4 are
re-checked. If a change breaks something older, CI tells you.

---

## When you are stuck

**CI is red and I do not understand why.** Open the **Actions** tab on GitHub and click
the failed run. It says which check failed and why, line by line. The same output comes
from `python .github/check_deliverables.py` locally.

**The checks pass locally but fail on GitHub.** Usually a file you did not push. Run
`git status`.

**`ruff` is clean locally but not in CI.** A version mismatch. Install the version
pinned in `requirements/week09.txt`, not whichever one you happen to have.

**Ollama will not run / the model will not download.** Drop to a smaller model. If none
of them work, use the cloud backend and write down why in `model_notes.md` — that is an
acceptable outcome. Do not lose the week to it.

**I broke something and cannot undo it.** Do not panic; git remembers everything:

```bash
git log --oneline           # commit history
git diff                    # what has changed right now
git checkout -- file.py     # restore one file to the last commit
```

**Still stuck?** Ask in the lecture, or ask an AI — but verify what it tells you, and
record the exchange in `ai_log_NN.md`. That is precisely what this course is about.

---

## Command summary

```bash
# while working
python .github/check_deliverables.py     # show me what is missing
AIASD_WEEK=2 python .github/check_deliverables.py   # just one week, if you want
ruff check . --fix                       # clean the code
git add . && git commit -m "weekNN: ..." && git push

# environment
source .venv/bin/activate                # Windows: .venv\Scripts\activate
streamlit run app.py
```
