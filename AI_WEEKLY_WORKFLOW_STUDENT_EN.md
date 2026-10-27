# Weekly Workflow — What You Do Each Week

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**

**Version 2 · 24 Oct 2026** — this document is revised during the term. When you run the
checker (`python .github/check_deliverables.py`), it brings the newest copy into your
repository by itself. So the copy in your repository (the folder of your project that git
tracks, both on your computer and on GitHub) is the current one. Add it with `git add .`,
as you do with every file that arrives.

> [!IMPORTANT]
> **What changed in version 2 (24 Oct 2026)**
>
> - Commits: in the lecture, commit each piece of work in the middle and again when it works, and
>   push every commit right away; outside the lecture at least
>   two commits with new work, pushed at least one hour apart; GitHub's push time counts (§2).
> - Never force push, and never let an assistant do it (§2, §4).
> - From the Sunday after Week 5, a change to `requirements.json` or `test_cases.json` is a
>   `CR-` line in the Change log of `PROPOSAL.md` (§3).
> - From Week 6, the lecture mark reads the GitHub Actions run (§2).
> - The roles in `group_NN.json`, week by week (§3).
> - In the AI log, the assistant's words appear only in **bold**, copied from the Evidence
>   block. The Evidence block has `ME:`, `AI:` and `TERMINAL:` parts (§3).
> - The Evidence block: paste the rounds that show the error; every part you keep is pasted
>   whole (§3).
> - The green tick shows the lab checks, the secret scan and ruff. The checker's 2 Saturday
>   points come from the "By Saturday" checks, read at 23:59 (§3).
> - GitHub also runs `ruff format --check .`, with ruff 0.15.11 (§4).
> - There is no weekly online group meeting any more. The assignment says when your group
>   meets (§3).
> - A small fix commit after a red run never lowers the commit point (§2, §4).
>
> The checker brings each new version by itself. This box lists what changed since the
> version before.

This document describes the routine that does not change. The *content* of each week
differs, because each week's assignment arrives in that week's folder, but the *rhythm*
is always the same.
Come back here when you are stuck.

---

## At a glance

| When | What you do | Points |
|------|-------------|--------|
| Before the lecture | Read `weekNN/ASSIGNMENT_NN_EN.md` | — |
| During the lecture (3 h) | Work, and push often (a push sends your saved work from your computer to GitHub) | — |
| End of the lecture | Push by 11:45. The lecture mark reads your last commit pushed by the end of the lecture (I take a snapshot: a copy of your repository exactly as it is at that moment) | 5 |
| After the lecture | Finish the rest and write `ai_log_NN.md` | — |
| By Saturday 23:59 | **Push again.** I take a second snapshot of your repository | 5 |

Each week is worth ten points, split evenly between two moments: **five measured at the
end of the lecture, five at the Saturday deadline.** Both halves are read from GitHub, so
both need a push (a push is the `git push` command, which sends the commits on your
computer to your repository on GitHub). **Week 1 is the one exception:** it is worth five
points, nothing is read at the end of the first lecture, and all five are read from your
repository at Saturday 23:59. Work that is finished but not pushed scores exactly the
same as work that was never done.

It is deliberate that half the week's mark depends on the lecture. The lecture is where
the work belongs: you are in the room, and you can still ask questions. The other half
rests on finishing the week's work, and on two things that a checker (the automatic
script that looks for the files each week requires; §2 shows how to run it) cannot see.
§3 describes those two things.

**The deadline is the same every week: Saturday 23:59.** There is nothing to work out,
because whatever is in your repository at Saturday midnight is what I grade. Most of the
work should happen in the lab, where you can ask questions; the days after the lecture
are for closing gaps, not for starting.

---

## Once, and never again

Three things have to be true before the first lecture starts, and none of them is part
of the course content: (a) you have a GitHub account, (b) you have your repository, and
(c) you have a computer that is allowed to push to that repository. The required
commands are on the [**Setup Card**](AI_SETUP_CARD_EN.md). The card has four steps, and
the last step tells you whether the other three worked.

The card also carries a table of the errors you are most likely to hit and of what each
one actually means. Keep it open; it is probably the only page you need for the
mechanics of git and GitHub.

---

## 1. Before the lecture of that week

Read `weekNN/ASSIGNMENT_NN_EN.md`. It arrives with the rest of the week's folder and
lists exactly which files that week requires. 

If there is pre-reading, read it before you arrive. 

---

## 2. During the lecture

### Know which half you are working on

From the root of your repository (the top folder of your project, the one that contains
the `.github` folder), run:

```bash
python .github/check_deliverables.py
```

It answers in two parts:

```
In the lab:     11 of 14 done
By Saturday:     0 of  3 done
```

The numbers above are only an example; the real numbers change from week to week. What
matters is which of the two lines you are reading.

A **NOT YET** line waits for something that it names. It is neither passed nor failed, and
it does not count in "x of y".

**In the lab** is the line that I read at the end of the lecture, and it is worth half
the week's mark. These items are worth doing while you are in a room with me and with,
say, twenty-nine other people who are stuck on the same thing.

**By Saturday** is the rest of the week: the write-ups, the diagrams and `ai_log_NN.md`
(your weekly log of the work you did with the AI assistant; §3 explains it). This is
work that you genuinely do alone. It does not make the check fail during the week,
because it is not due yet; but it is the other half of the mark, and the Saturday
snapshot does read it.

If you are writing `ai_log_NN.md` during the lab, you are doing things in the wrong order:
the log comes after the lab work.

### Work, and push often

Commit as the work progresses (a commit is one saved step in git's history, made with
`git commit`), rather than committing everything in one enormous lump at the end. The
message of each commit should say what you did:

```bash
git add .
git commit -m "week01: hello.py reads a name and prints the list"
git push
```

A message such as "update", "fix" or "asdf" says nothing about what happened, and
messages like these cost you the commit-discipline point (§3 describes it).

**The commit and push rule:**

- **In the lecture:** commit each piece of work in the middle, whatever state it is in, commit it
  again when it works, and push every commit right away. A piece that arrives finished in one
  commit does not count.
- **Outside the lecture:** at least two commits with new work, pushed at least one hour
  apart.
- GitHub's push time counts, not the date on a commit.
- A commit made by a coding agent never counts.
- **Never force push**, and never let an assistant do it (§4).

At 10:00 and at 11:00 I look at the class board (the projected table that shows where
every student's repository stands) to see where everyone is. Push by 11:45: the lecture
mark reads your last commit pushed by the end of the lecture. A push costs nothing. A half-finished section that
is pushed is worth more than a finished one that is not.

### Run the checks yourself

Run the same command, as often as you like:

```bash
python .github/check_deliverables.py
```

These are exactly the checks that I will run. The output lists what is missing, one line
at a time. It is not a grade; it is a to-do list, and running it costs nothing.

### Push once more before the lecture ends

Push by 11:45. The lecture mark reads your last commit pushed by the end of the lecture (from Week 6,
also its Actions run). I take a snapshot of that commit (a copy of the repository exactly
as it is at that moment) and I run the checks on that snapshot. Work that you have not pushed is invisible: it sits on your
laptop and does not count.

The result is projected as an anonymised table (a table in which nobody's real name
appears); find your row by the nickname in your `student.json` (the file in your
repository that holds your details, including the nickname you chose). That table is
worth **5 points — half the week**.

**From Week 6, the lecture mark reads GitHub Actions.** The test results in your lecture
mark come from the GitHub Actions run of the last commit you pushed before the end of the
lecture. A test that passes only on your laptop does not count. Look at the **Actions** tab
after each push.

One student works on one computer with one GitHub account. Work done on a classmate's
machine or under a classmate's GitHub session earns nothing for the lecture.

**Commit discipline (1 point a week) is judged every week.** I read the rule above: the
three pushes in the lecture, and two pushes at least one hour apart outside it. I also ask
three questions:

- Did the work grow step by step?
- Is there real progress from one commit to the next?
- Was the text worked on, or was it pasted in finished?

Each commit has a message that says what changed. A commit does not need to be a finished
part. A single commit at the end of the week, or text that arrives in one piece, scores
nothing. A small fix commit after a red run never lowers the point. When something in a
week looks doubtful, I also look back at your earlier weeks before I decide. I may also ask
you a two-minute question about your project in any lecture.

### Attendance, and what happens if you are not here

**Bring your laptop every week**, with its charger and whatever cable it needs. The
lecture is a three-hour hands-on study opportunity.

**Attendance is mandatory.** The university allows you some weeks of absence across the
term, and that allowance already covers everything, whether the reason is illness, work,
family or anything else at all. There is no second category on top of it, and there is
no make-up procedure.

**A lecture you miss is a lecture I cannot mark.** Whatever the reason, those 5 points
are gone. I do not weigh reasons against each other, and that is deliberate: with over a
hundred students, a process for judging excuses turns into a process for judging who
explains themselves best.

What stays open is the other half. Do the lecture's work in your own time, push it
before Saturday midnight, and you earn those five points exactly as everyone else does.
Missing a lecture costs you that lecture, not the week.

---

## 3. After the lecture — until Saturday 23:59

Finish the rest of the week's work by Saturday midnight. I take a second snapshot at that
time, and your state at the deadline decides the other 5 points.

### `ai_log_NN.md` — do not skip it

You write one file per week, inside that week's folder, so Week 1 has
`week01/ai_log_01.md`, and so on. The file arrives with the rest of the documents in the
week folder, and you fill it in. You write which assistant you used, what it got right,
what you had to correct, and what you learned. **You write it yourself, in your own
words**: outside the Evidence block and the bold quotes no assistant is used, not even to
correct the language. Your English or Turkish is not graded; a log written by an assistant earns 0 points from Week 4 on, however polished it is (in Weeks 1–3 it earned at most 1 of the 2).

The assistant's words may appear in your log only in **bold**. Each bold phrase is copied
letter for letter from the Evidence block. Use bold for nothing else. Each week's log also
names the `AI_Doc5` technique that it uses (the week's AI log file says which one). From
Week 4 the technique is compulsory.

**The Evidence block is required.** Paste the real exchange inside the code fence (the
block between two lines of three backticks): under `ME:` the prompt you sent, under `AI:`
the answer exactly as it came, and, when the week asks for it, under `TERMINAL:` the
commands and their output, untouched. Paste the rounds of the exchange that show the error;
you may leave out whole rounds that do not. Every `ME:`, `AI:` or `TERMINAL:` part you keep
is pasted whole, exactly as it came: from Week 4, nothing removed, nothing corrected, not
even the grammar. A claim with an empty Evidence block earns nothing.

Why is this required? Anyone can write "the AI made a mistake and I fixed it". A real
model output is hard to fabricate convincingly, because invented transcripts read too
cleanly and their errors are conveniently easy to spot. And choosing which part of a
long conversation counts as evidence is itself the skill that is being assessed.

If you would rather keep the whole conversation, save it as `weekNN/transcript.md`. I do
not read those files by default, but I will read yours when a log entry is not clear to
me.

The AI log is the main part of the 2 human-involvement points, together with the
hand-written files the week names (Week 1: 1 point).

### Keep going until the checks are green

```bash
python .github/check_deliverables.py
git add .
git commit -m "week01: llm_notes written up"
git push
```

The **Actions** tab of your repository on GitHub shows the result of every push. After
every push GitHub runs two jobs, and this automatic run is called CI (continuous
integration): "Weekly deliverables" (the checker) and "Lint and format" (ruff). The green
tick shows the lab checks, the secret scan and ruff. The "By Saturday" checks do not turn
it red, because they are not due yet. The checker's **2 Saturday points** come from the
"By Saturday" checks, read at 23:59. So run the checker and read its "By Saturday" line.

### The 3 points that are not automated

**Consistency and commit discipline — 1 point.** Does this week's work actually follow
from the requirements and the design that you wrote in previous weeks, and does your
commit history show the work growing step by step rather than one last-minute dump? If you
changed your plan, did the change get a dated line in the change log of `PROPOSAL.md`?
Changing your mind is normal and healthy, but the change must be visible. The project
itself (its problem and its product) is fixed at the end of the Week 3 lecture (11:45);
after that, only its details change. A requirement that is silently abandoned costs the
mark.

From the Sunday after Week 5 (the baseline), every change to `requirements.json` or
`test_cases.json`, a dropped requirement included, is a **change request**: one line in the
Change log of `PROPOSAL.md` that begins with `CR-` and the next number, names the change
and the ids, and lists every file it affects. Example: "2026-10-28 — CR-01: REQ-002 now
allows 15-minute slots; affects requirements.json, test_cases.json (TC-002-02),
week05/api.md, server/bookings.py." Other changes (`api.md`, use cases, screens) get an
ordinary dated Change log line. A logged change costs nothing. That is what engineering
looks like.

**Human involvement — 2 points.** This is proof that people, and not only models, did this
week's work. Your own part is shown in `weekNN/ai_log_NN.md`: a concrete AI error, the
pasted evidence, and what you changed by hand. This log is the main part of the two
points, together with the hand-written files the week names (Week 1: 1 point). The
classmates who help you are recorded too, each with one sentence on what they did, plus
evidence of that work; the evidence can be their notes, their bug list, or a dated
paragraph in your log. In Week 2, up to two classmates may help you as stakeholders,
recorded in `week02/contributors_02.json`; they are optional, and working alone costs you
nothing. In Week 3 your three reviewers in the lecture are recorded in
`week03/contributors_03.json`. From Week 4 the people who help you are recorded in
`weekNN/group_NN.json`, in the role that the week's assignment names (the list is below).
Whatever you list must be real; names and nothing behind them is a list, not evidence, and
without evidence the contributors' bonus is not paid.

**Your group and `weekNN/group_NN.json`.** In Week 3 you form a group of four yourselves
(five when the class does not divide by four). Your group of Week 3 stays your group; the
assignment says in which weeks it meets and what for. `weekNN/group_NN.json` holds the
people that week's assignment names, with that week's role (the exact English word). In
Weeks 2 and 3 the people who help you are in `contributors_NN.json`.

| Week | Role |
|---|---|
| 2 | stakeholder |
| 3 | reviewer |
| 4 | collaborator |
| 5 | nobody (you work alone) |
| 6 | attacker |
| 7 | tester |
| 8 | test-user |
| 9 | beta-tester |
| 10 | uat-participant |
| 11 | release-tester |
| 12 | poster-reviewer |

For each person, you write what they did or said and what you did about it; the week's
assignment gives the fields. Nobody can write those entries for someone who was not there.

**Contributors earn a bonus.** A classmate who helps you earns 10% of your mark for that
week, for at most three contributions a week; the same applies to you when you help
them. In Week 2 the names are your choice; from Week 3 they are the people that the week's
assignment names. Weeks 1 and 5 have no contributors.

An LLM (a large language model, the kind of model behind AI assistants) can produce
every file that an assignment asks for. What it cannot do is make those files agree with
the ten weeks around them, or notice its own mistakes on your behalf. That is what is
actually being assessed.

---

## 4. Rules that apply every week

**Never put an API key in your code.** (An API key is the secret, password-like string
that lets your program use an external service.) The key lives in `.env` (a small file
of settings that only your own computer reads), and `.env` is listed in `.gitignore`
(the file that tells git which files must never be committed). If a key reaches the
repository, the automatic secret scan catches it (it finds API keys and tokens, not
passwords), and you lose **10 points**. Once a key has
been pushed, deleting it is not enough, because it stays in the git history. You must
revoke that key and issue a new one.

**Keep the code clean.** Before pushing, run `ruff` (a tool that finds and fixes style
problems in Python code):

```bash
ruff check .          # list problems
ruff check . --fix    # fix what can be fixed automatically
ruff format .         # format
```

AI-generated code frequently leaves unused imports behind (an import line that loads a
module which the code never uses); `ruff` catches them instantly.

GitHub's "Lint and format" job runs `ruff check .` and `ruff format --check .` on every
push, from Week 1. Use the same version as GitHub: `ruff==0.15.11`, which is in the root
`requirements.txt` (`python -m pip install -r requirements.txt`).

**Your app must work on a phone.** Narrow your browser window to about 390 pixels
(roughly the width of a phone screen) now and then. If something is cut off or scrolls
sideways, fix it while the window is small, not in Week 10.

**Never force push.** A force push (`git push --force`, or "Force Push" in VS Code)
deletes commits from your repository's history, and that history is part of the record of
your work that I read. Do not let an assistant do it for you either. If git refuses your
push, run `git pull` and then `git push` again (in VS Code: **Sync Changes**).
If `git pull` stops with "Need to specify how to reconcile divergent branches", run
`git config pull.rebase false` once, then `git pull` again. If git reports
a conflict and you are not sure what to do, ask in the lecture instead of forcing the push.
Your marks are read from GitHub's own record of when each push arrived, not from the dates
on your commits.
A small fix commit (a ruff error, a typo) never lowers the commit point: push it as a new
commit instead of changing an old one.

**Do not break earlier weeks.** The checks are cumulative: in Week 5, Weeks 1 to 4 are
re-checked. If a change breaks something older, CI (the automatic run of the checks on
GitHub; see §3) tells you.

---

## When you are stuck

**CI is red and I do not understand why.** Open the **Actions** tab on GitHub and click
the failed run. It says which check failed and why, line by line. The same output comes
from `python .github/check_deliverables.py` when you run it locally (on your own
computer).

**The checks pass locally but fail on GitHub.** The usual cause is a file that you did
not push. Run `git status` (it lists the files that have changed and have not yet been
committed or pushed). From Week 6 another cause is a course file that you changed
(`course_tests/`, `server/course_login.py`): GitHub always uses the course's copy. Do not
edit these files.

**`ruff` is clean locally but not in CI.** This is a version mismatch: your computer and
CI are running different versions of `ruff`. Install the version pinned in the root
`requirements.txt` (the list of the packages, with their exact versions, that the course
needs), not whichever one you happen to have: `python -m pip install -r requirements.txt` installs
`ruff==0.15.11`. Run `ruff format .` too, because GitHub also checks the format.

**I broke something and cannot undo it.** Do not panic, because git remembers
everything:

```bash
git log --oneline           # commit history
git diff                    # what has changed right now
git checkout -- file.py     # restore one file to the last commit
```

**Still stuck?** Ask in the lecture, or ask an AI. If you ask an AI, verify what it tells
you, and record the exchange in `ai_log_NN.md`. That is precisely what this course is
about.

---

## Command summary

```bash
# while working
python .github/check_deliverables.py     # show me what is missing
python .github/check_deliverables.py 2   # another week, if you want
ruff check . --fix                       # clean the code
ruff format .                            # format the code
git add . && git commit -m "weekNN: ..." && git push

# environment
source .venv/bin/activate                # Windows: .venv\Scripts\activate
uvicorn server.main:app --reload         # start the server (from Week 5)
```
