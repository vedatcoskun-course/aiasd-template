# Weekly Workflow — What You Do Each Week

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**

This document describes the routine that does not change. The *content* of each week
differs — the assignment is posted on the LMS — but the *rhythm* is always the same.
Come back here when you are stuck.

---

## At a glance

| When | What you do | Points |
|------|-------------|--------|
| Before the session | Read the assignment | — |
| During the session (3 h) | Work, and push often | 5 |
| End of the session | One last push — I freeze the state | ↑ same 5 |
| By Saturday 23:59 | Finish the rest, write `ai_log.md` | 5 |

Ten points a week, split evenly between two moments: **five measured at the end of the
session, five at the Saturday deadline.**

Half the week's mark riding on the session is deliberate. This is where the work
belongs — in the room, while you can still ask. The other half rests on finishing, and
on the two things a checker cannot see.

**The deadline is the same every week: Saturday 23:59.** There is nothing to work out —
whatever is in your repository at Saturday midnight is what I grade. Most of the work
should happen in the lab, where you can ask questions; the days after are for closing
gaps, not for starting.

---

## 0. Before Week 1 — once, and never again

Three things have to be true before the first session starts, and none of them are the
course: a GitHub account, your repository, and a computer that is allowed to push to
it. The commands are on the [**Setup Card**](SETUP_CARD.md) — four steps, and the last
one tells you whether the other three worked.

Do them at home. If they are not done when you walk in, you will spend the session
watching other people work, and none of it is anything I can teach you in a room with
forty other people in it.

The card also carries a table of the errors you are most likely to hit and what each
one actually means. Keep it open; it is the only page you need for the mechanics.

---

## 1. Before the session

Read the assignment on the LMS. It lists exactly which files that week requires.

If there is pre-reading — Week 1 has two documents — read it before you arrive. The
20 minutes I spend lecturing is a summary of that material. Turn up without having read
it and those 20 minutes will mean nothing to you.

---

## 2. During the session

### There is no switch to flip

The checker asks the course which week it is on, every time it runs. You cannot forget
to set it, and you cannot be checked against the wrong week. The `WEEK` file at the
repository root caches that number for when you are offline; it updates itself.

### Know which half you are working on

Run the checker and it answers in two parts:

```
In the lab:     11 of 13 done
By Saturday:     2 of  8 done
```

**In the lab** is what I read at the end of the session — half the week's mark. These
are the things worth doing while you are in a room with me and twenty-nine other
people who are stuck on the same thing.

**By Saturday** is the rest: the write-ups, the diagrams, `ai_log.md`. Work that is
genuinely done alone. It does not fail the run during the week, because it is not due
yet — but it is half the mark too, and the snapshot on Sunday does read it.

If you find yourself writing `ai_log.md` during the lab, you have the week backwards.

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

Before pushing, run exactly the checks I will run:

```bash
python .github/check_deliverables.py
```

The output lists what is missing, one line at a time. It is not a grade; it is a
to-do list.

### Push once more before the session ends

At the end of the session I freeze every repository as it stands and run the checks.
Work you have not pushed is invisible — it sits on your laptop and does not count.

The result is projected as an anonymised table; find your row by the nickname in your
`student.json`. That table is worth **5 points — half the week**.

### If you cannot be there

Illness and emergencies happen and they should not cost you half a week's mark. There
is a procedure, and it has two deadlines.

**Within 2 hours of the end of the session**, email me at
`vedat.coskun@atlas.edu.tr` explaining why you were not there, with the supporting
documents attached. Not the next morning, not when you feel better — within two hours
of when the session ended.

**Within 24 hours**, do the session's work and push it.

If I accept the case, I will grade that session's work as though you had been in the
room, and enter those 5 points by hand. If I do not accept it, or the email does not
arrive in time, the session is marked on what was in your repository when I took the
snapshot — which, if you were not there, is nothing.

Two things this does not do. It does not excuse the work: you still produce it, and
still quickly, which is what the 24 hours is for. And it does not give you the room
back — the chance to ask while you are stuck is the part I cannot hand over
afterwards, whatever I do with the marks.

The short deadline is not bureaucracy. A reason given two hours after the fact is a
reason; the same reason given on Friday is a reconstruction, and I cannot tell the
difference between the two.

---

## 3. After the session — until Saturday 23:59

Finish the rest of the week's work by Saturday midnight. I take a second snapshot on
Sunday morning; your state at the deadline decides the other 5 points.

### `ai_log.md` — do not skip it

One file at the repository root, with a section already prepared for all twelve weeks.
Fill in that week's: which assistant you used, what it got right, **what you had to
correct**, and what you learned.

**The Evidence block is required.** Paste the actual exchange under your claim — the
prompt you sent and the wrong answer you got — inside the code fence. Not the whole
conversation: the ten or fifteen lines that show the error. A claim with an empty
Evidence block earns nothing.

Why: anyone can write "the AI made a mistake and I fixed it". A real model output is
hard to fabricate convincingly — invented transcripts read too cleanly and their errors
are conveniently easy to spot. And choosing which part of a long conversation counts as
evidence is itself the skill being assessed.

If you would rather keep the whole conversation, save it as `weekNN/transcript.md`. I do
not read those by default, but I reserve the right to ask when a log entry does not add
up.

This file is worth 2 points and a person reads it.

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
`ai_log.md` costs nothing. That is what engineering looks like.

**`ai_log.md` quality — 2 points.** A concrete AI error, the pasted evidence, and how
you noticed.

An LLM can produce every file an assignment asks for. What it cannot do is make those
files agree with the ten weeks around them, or notice its own mistakes on your behalf.
That is what is actually being assessed.

---

## The final project, and why it matters from Week 1

The weekly marks are 70% of your grade. The remaining 30% is the final project, and it
is worth knowing now how those marks are split — because it changes how you should work
all term.

| Criterion | Points |
|-----------|--------|
| Functionality — runs end to end, on desktop and phone | 8 |
| Traceability — requirement → code → test | 6 |
| Oral defence — five minutes of questions | 6 |
| Code quality — readable, `ruff` clean, no secrets, usable at phone width | 4 |
| Design documents — accurate to the code as built | 3 |
| `ai_log.md` across the term | 3 |

Traceability and the defence together are worth more than functionality. That is
deliberate: **a working application you cannot account for is a weaker result than a
modest one you understand completely.**

### The oral defence

In Week 12 I will ask you three questions about your own project, with your repository
open, for about five minutes. I am not testing your memory. I am finding out whether you
supervised this build or assembled its output — those two look identical on GitHub and
completely different in conversation.

I will not publish the questions, but here are the categories they come from:

- **A decision and its alternative.** Why this way, and what did you reject?
- **A failure and how you diagnosed it.** Not the fix — the path to finding the cause.
- **An AI error you caught.** How did you know it was wrong?
- **Trade-offs and limits.** What does your application do badly?
- **Change one thing.** With two more weeks, what would you fix first?

Notice that four of those five are answerable only from your own `ai_log.md` and your
own debugging history. If you keep that log honestly every week, you have already
prepared. If you fill it in from memory in December, you will not have.

### Traceability

I will pick three requirements from your Week 2 SRS at random and ask you to show me the
code that implements each one and the test that covers it. This is why the consistency
marks exist every week: the habit that earns them is the same habit that makes this
question easy.

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

**Still stuck?** Ask in the session, or ask an AI — but verify what it tells you, and
record the exchange in `ai_log.md`. That is precisely what this course is about.

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
