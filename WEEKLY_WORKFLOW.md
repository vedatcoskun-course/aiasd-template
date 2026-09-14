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
| During the session (3 h) | Set `WEEK`, work, push | 2 |
| End of the session | One last push — I freeze the state | ↑ same 2 |
| By Saturday 23:59 | Finish the rest, write `ai_log.md` | 3 |
| Every week | Consistency, `ai_log.md` quality, commit hygiene | 5 |

Ten points a week. Half comes from automated checks, half from my reading of your work.
That split is deliberate: the automated half proves the work exists and runs, but only a
person can tell whether you understood it.

**The deadline is the same every week: Saturday 23:59.** There is nothing to work out —
whatever is in your repository at Saturday midnight is what I grade. Most of the work
should happen in the lab, where you can ask questions; the days after are for closing
gaps, not for starting.

---

## 1. Before the session

Read the assignment on the LMS. It lists exactly which files that week requires.

If there is pre-reading — Week 1 has two documents — read it before you arrive. The
20 minutes I spend lecturing is a summary of that material. Turn up without having read
it and those 20 minutes will mean nothing to you.

---

## 2. During the session

### First, set the `WEEK` file

The `WEEK` file at the repository root tells the automated checker which week to look
at. Update it when you start the week:

```bash
echo 3 > WEEK        # for Week 3
```

Forget this and the checks never look at that week's files — your score at the end of
the session will read zero.

### Work, and push often

Commit as the work progresses rather than in one enormous lump at the end. The message
should say what you did:

```bash
git add .
git commit -m "week03: ollama backend of llm_client working"
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
`student.json`. That table is worth **2 points**.

---

## 3. After the session — until Saturday 23:59

Finish the rest of the week's work by Saturday midnight. I take a second snapshot on
Sunday morning; your state at the deadline decides the 3-point part.

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
git commit -m "week03: model_notes completed"
git push
```

The **Actions** tab of your repository on GitHub shows the result of every push. A green
tick means the automated part of that week is done — 3 points.

### The 5 points that are not automated

Half of the week's marks come from things the checker cannot see.

**Consistency with earlier weeks — 2 points.** Does this week's work actually follow
from the requirements and design you wrote in previous weeks? Changing your mind is
normal and healthy — but the change must be visible. A silently abandoned requirement
costs marks; a requirement dropped with a one-line justification in `ai_log.md` costs
nothing. That is what engineering looks like.

**`ai_log.md` quality — 2 points.** A concrete AI error, the pasted evidence, and how
you noticed.

**Commit hygiene — 1 point.** Meaningful messages, work spread across the week.

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
# starting the week
echo N > WEEK

# while working
python .github/check_deliverables.py     # show me what is missing
ruff check . --fix                       # clean the code
git add . && git commit -m "weekNN: ..." && git push

# environment
source .venv/bin/activate                # Windows: .venv\Scripts\activate
streamlit run app.py
```
