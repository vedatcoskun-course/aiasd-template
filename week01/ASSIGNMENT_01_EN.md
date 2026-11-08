# Week 1 Assignment — Foundations: Environment, Git, and First Contact with LLMs

**Due:** Saturday 23:59 · Commit to your project repository

> **Before the lecture** read the three pre-reading documents at the root of your repository (`AI_Doc2`, `AI_Doc3`, `AI_Doc4`): *AI Technical
> Background* (concepts), *Development Environment and Tools* (environment and tools) and
> *Working with AI Tools* (what the tools cost and how to use them well).
> The lecture is a 20-minute summary of exactly that material.

---

## Tasks

### 1. Create your project repository from the template
Go to `https://github.com/vedatcoskun-course/aiasd-template` and click
**Use this template → Create a new repository**. Three things on that form:

**Repository name:** exactly `aiasd-project`. Lower case, one hyphen, nothing else. I
find your work by that name, so a different one means I do not find it.

**Visibility: Private.** ⚠️ **The form opens on Public.** You have to change it before
you press Create. If you leave it on Public, your student number and your name are on
the open internet. That is exactly what we want to avoid. If it happens, do not worry:
change it in Settings at once and tell me.

**Include all branches:** leave it off.

Then clone it to your laptop: follow steps 2 and 3 of `AI_SETUP_CARD_EN.md` (connect your
computer to GitHub once, then `git clone` your repository).

Now add me as a Collaborator: **Settings → Collaborators → Add people**, then search
for **`VedatCOSKUN`** — that exact spelling, no hyphen, it is the account that grades
you. Without this your repository is invisible to me and the week counts as not
submitted.

Adding me sends an invitation that I have to accept, so there is a short gap before I
can actually see anything. You do not need to do anything else — but if the end-of-lecture
board shows nothing for you, this is the first thing we check.

The repository is private on purpose: it carries your student number and name, and
those do not belong on the public internet. You are free to make it public after the
course ends.

### 2. Fill in `student.json`

The file is already there, at the root of the repository you just created, with every
value left empty. Do not create a new one — open that file and fill it in. Five fields,
all required:

```json
{
  "student_id": "230500000",
  "first_name": "Ayşe",
  "last_name": "Yılmaz",
  "nickname": "kaplumbaga",
  "section": "en"
}
```

The **nickname** is what appears on the class board projected at the end of each
lecture, so you can find your own row quickly. Letters, digits, `-` and `_` only,
2–20 characters. Beyond that it is your choice — pick
something you will still recognise in December.

**`section`** is `en` or `tr`, whichever section you are enrolled in. Your repository
uses it to ask the course which week to check you against; get it wrong and you will
be shown the wrong week's checks.

Your number and name are for the official grade record and never leave my machine.

### 3. Set up your Python environment
Follow sections 1–5 of *Development Environment and Tools*: Python 3.12, a virtual
environment, and VS Code with the Python extension.

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Record the proof in `week01/setup_proof.md` — terminal output or screenshots showing
`python --version`, `pip --version`, `git --version`, and the activated virtual environment.

### 4. Write `week01/hello.py`
A small script that demonstrates you can write Python, not just run it.
It must read a name with `input()`, and use **an f-string, a list, and a for-loop**.
Keep it short — ten lines is plenty.

**And make it do something only you would have thought of.** Not "hello, name" — that
is the example, and if thirty people hand in the example I learn nothing about any of
them. Make it about a list that means something to you: the courses you are taking
this term, the five stops on your way to campus, the players in a squad you follow,
the ingredients of something you cook. Ten lines is still plenty. The point is that
your file should be clearly yours before anyone reads the name at the top.

```
python week01/hello.py
```

### 5. Explore an LLM through its web interface
No API calls this week — no keys, no SDK. Pick **two different assistants** and open
them in the browser: Claude, Gemini, ChatGPT, Copilot, Codex — whichever two you can
reach. Spend 20 minutes prompting both.

Write `week01/llm_notes.md` **in your own words, minimum 300 words**, answering:
what is a transformer, what problem does the attention mechanism solve, and how does
an LLM generate the next token?

Write this file in your own sentences, not a model's. Later weeks say which other files
you write yourself.
I cannot tell by reading who wrote a text, and no tool can either. So the task is
built in a way that a pasted answer does not fit:

- **Anchor every explanation to your own session.** Quote the actual answer one of
  your two assistants gave you and say where it was vague, wrong or better than you
  expected. A model that was not in your conversation cannot write this paragraph.
- **Use your own `hello.py` as the example** when you explain tokens: how many tokens
  do you think your own ten lines are, and why is that not the same as the number of
  words?
- **End with what you still do not understand.** One honest paragraph. This is the
  part a language model is worst at, because it does not know what you are missing —
  and it is the part I read most carefully.

A fluent, correct, general essay about transformers earns fewer marks than a rougher
one that is clearly about *your* twenty minutes. The term ends with a project
defence. In the defence, you must be able to explain everything you wrote.

While you are there, ask one of your questions **twice**: once vaguely, once with the
context and the constraints spelled out. Put both answers in `llm_notes.md` and say in
a sentence what changed. You are not being taught prompting techniques this week — you
are being asked to notice that the question shapes the answer. We come back to this
properly later in the term.

### 6. Find one thing the model got wrong
Ask both assistants the same factual question about a topic you know well.
Record the disagreement or the error in `llm_notes.md`. Every model hallucinates;
your job this term is to notice when.

### 7. Write `week01/ai_log_01.md`

The file is in `week01/`, next to the rest of this week's work. Which assistant you
used, what you asked, what it got right, and what you had to correct. The **Evidence** block is not optional: paste the actual exchange — your
prompt and the wrong answer — inside the code fence. Ten or fifteen lines, trimmed to
the part that shows the error.

A claim without the exchange behind it does not earn the marks. If you would rather
keep the whole conversation, save it as `week01/transcript.md`; I will not read it
unless something in your log does not add up.

### 8. Confirm your `.gitignore`
It must already contain `.venv`, `.env`, and `__pycache__`.
Create `.env.example` at the repo root — variable names only, never values.

### 9. Run the checks yourself

Your repository checks its own deliverables on every push, and there is nothing to
switch on: it asks the course which week it is on, so what you see is always what is
being run against you.

Run the same checks locally before you push:

```bash
python .github/check_deliverables.py
```

Every push also runs a second job, **"Lint and format"**. It checks your Python files with
ruff 0.15.11. Run it locally too:

```bash
pip install ruff==0.15.11
ruff check .
ruff format .
```

`ruff check .` lists problems in your code. `ruff format .` formats your files the way
the job expects.

Fix what they report. A red cross on GitHub is information, not a grade. It tells you
what is missing while you still have time to fix it.

### 10. Commit and push
```
git add .
git commit -m "week01: environment setup and first LLM exploration"
git push
```

The commit rule:

- At least two commits with new work, pushed at least one hour apart.
- GitHub's push time counts, not the date on a commit.
- A commit made by a coding agent never counts.
- **Never force push**, and never let an assistant do it.

From Week 2 you also push in the lecture, near 10:00, 11:00 and 11:45 (within 15 minutes
of each time), each push with new work.

### 11. Nothing to submit on the LMS this week

There is no form, no link to paste, no username to send me. Adding me as a Collaborator
**is** the submission — GitHub tells me who added me, and your `student.json` tells me
which student that is.

So two things matter most this week, and both are in task 1 and task 2: I have to be a
Collaborator, and your student number in `student.json` has to be correct. If either
one is wrong, I cannot see your work, however good it is.

If the board shown in Week 2 has nothing for you, say so in the room. It is
almost always one of those two, and both take a minute to fix.

---

## Deliverables checklist
- [ ] `student.json` — all five fields filled, `section` correct
- [ ] Repository is **private**, and I am added as a Collaborator
- [ ] `week01/setup_proof.md` — environment verified
- [ ] `week01/hello.py` — runs, uses an f-string, a list, and a for-loop
- [ ] `week01/llm_notes.md` — 300+ words in your own words, one model error, and the two phrasings of one question
- [ ] `week01/ai_log_01.md` — filled in, **including the pasted Evidence block**
- [ ] `.gitignore` covers `.venv`, `.env`, `__pycache__`; `.env.example` present
- [ ] Both jobs are green on GitHub: "Weekly deliverables" and "Lint and format"
- [ ] At least two commits with new work, pushed at least one hour apart
- [ ] Repository named exactly `aiasd-project`, under the username you submitted

---

## How this week is graded

This week is different from the other weeks. From Week 2 on, five points are read from
your repository at the end of each lecture and five at Saturday 23:59. In Week 1 nothing is
captured at the end of the lecture — most of you will not have a working environment yet,
and setup is not graded work. **This week is worth five points, all read from your
repository at Saturday 23:59:**

- **3** — the automated checks: repository from the template, private, I am a Collaborator,
  `student.json` complete, `setup_proof.md`, `hello.py` meeting its three requirements,
  `llm_notes.md` in your own words, `.gitignore` and `.env.example`, checks green.
- **1** — commit discipline: at least two commits with new work, pushed at least one hour
  apart (the rule in task 10). A coding agent's commit never counts.
- **1** — your `week01/ai_log_01.md`: a real session, a real model error, the pasted exchange.
  I read this one myself.

The deadline is the same every week: I grade what is in your repository at Saturday
23:59.

An LLM can produce every file this assignment asks for. What it cannot do is make those
files agree with the ten weeks around them, or notice its own mistakes for you. That is
what is actually being assessed.
