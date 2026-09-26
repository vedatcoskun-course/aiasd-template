# AIASD Project — Student Repository

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**
**Prof. Dr. Vedat Coşkun**

*Türkçesi: [`AI_README_TR.md`](AI_README_TR.md)*

---

## How to use this repository

This is your personal project repository for the entire 12-week course.
You create it from the template on Week 1 and commit to it every week.

Each week arrives with its own assignment, in its own folder, telling you exactly
what to build and hand in. The whole term on two pages — what each week teaches, what you
push and when — is [`AI_SKELETON_EN.md`](AI_SKELETON_EN.md). The term builds one product, yours: a
mobile client, a web client and a server, published on a public app store of your choice,
defended at the end of term from the store-installed app.

Most weeks also ask for an AI log — `weekNN/ai_log_NN.md`, inside that week's folder.

### What is in here now, and what is not

Right now this repository holds the files that live here all term, plus `week01/`.
There is no `week02/` folder and there should not be — **you create each week's folder
when that week's assignment tells you to.** Putting the file in the right place is part
of the work, and the checker names the exact path it is looking for when you get it
wrong.

At the root, and staying there all term:

| | |
|---|---|
| `app.py` | Your application. Empty for now; it grows week by week into the whole thing |
| `week01/ASSIGNMENT_01_EN.md`, `_TR.md` | What this week asks for, in both languages. It arrives with the week's folder and is the only place the tasks are written |
| `week01/ai_log_01.md` | This week's AI log, in this week's folder. Every week has one, and it arrives with the week |
| `student.json` | Who you are. Fill it in once, in Week 1 |
| `requirements.txt`, `weekNN/requirements.txt` | Dependencies, arriving week by week |
| `.github/` | The checks that run on every push |
| `CURRENT_WEEK.txt` | Bookkeeping the checker manages. Do not edit it. A `CURRENT_WEEK_CACHE.txt` file appears next to it the first time you run the checker — that is its offline cache, it is not tracked by git, and you can ignore it |

A few weeks hand you a scaffold rather than making you build it from nothing. When
that happens the assignment opens with one command, and you run it **before** you
create anything in that folder:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git
git fetch template
git checkout template/main -- week06
```

The first line is only needed once, ever. If you run this after you have already
written files in that folder, it overwrites them — so run it first, or not at all.

**Start here:** [`AI_SETUP_CARD_EN.md`](AI_SETUP_CARD_EN.md) / [`AI_SETUP_CARD_TR.md`](AI_SETUP_CARD_TR.md)
— every command you will run all term, on one page, plus what the common errors mean. Do
its four setup steps before Week 1.

**New here?** The whole weekly routine — what to do before, during and after each
lecture, how the marks are split, and what to try when you are stuck — is written out
step by step in [`AI_WEEKLY_WORKFLOW_STUDENT_EN.md`](AI_WEEKLY_WORKFLOW_STUDENT_EN.md) /
[`AI_WEEKLY_WORKFLOW_STUDENT_TR.md`](AI_WEEKLY_WORKFLOW_STUDENT_TR.md).

**Read before Week 1** — the three pre-readings and the paper are at the root:
`AI_Doc2` AI Technical Background, `AI_Doc3` Development Environment and Tools,
`AI_Doc4` Working with AI Tools, and `AI_Doc1`, the Transformer paper. The lecture
is a twenty-minute summary of them. Later readings arrive the same way, numbered in order.

Both sections receive the same files. The assignments, the setup card and the workflow
come in two languages, `_EN` and `_TR` — read yours and ignore the other. The readings (`AI_DocN`)
are in English. Folder and file names the checker looks for (`week01/`, `hello.py`,
`student.json`) are the same for everyone.

---

## Running the app

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Dependencies arrive week by week so you are not downloading gigabytes in Week 1.
The root `requirements.txt` is the minimum; a heavier week has its own
`weekNN/requirements.txt`, and that week's assignment tells you when to install it:

```bash
pip install -r weekNN/requirements.txt
```

---

## Who you are — `student.json`

Fill this in on Week 1, at the repo root:

```json
{
  "student_id": "20210042",
  "first_name": "Ayşe",
  "last_name": "Yılmaz",
  "nickname": "kaplumbaga",
  "section": "en"
}
```

Your **section** is `en` if you are in the English section, `tr` if you are in the
Turkish one. Get this wrong and the checker will test you against the other section's
week, so check it before you push.

Your **nickname** is what appears on the class board projected at the end of each
lecture, so you can find your own row at a glance. Letters, digits, `-` and `_`,
2–20 characters. Choose whatever you like, and pick something you will still
recognise in December.

Keep this repository **private** while the course runs. It carries your student
number and name.

---

## Automatic checks

Every push runs the same checks your instructor runs. You see a green tick or a red
cross on your commit in GitHub, and you can see exactly which check failed.

**There is nothing for you to switch on.** The checker asks the course which week it
is on, every time it runs, so what you see is always what is being run against you.
The `CURRENT_WEEK_CACHE.txt` file at the repo root is just a cache of that number — it updates itself,
and you never need to touch it.

The output comes in two parts, because the week has two deadlines:

```
In the lab:     11 of 13 done
By Saturday:     2 of  8 done
```

**In the lab** is what the end-of-lecture snapshot reads — five of the week's ten
points. **By Saturday** is everything else: the write-ups, the diagrams, `ai_log_NN.md`.
Items in the second group do not fail the run while the week is still open; they are
not due yet. Nothing in the first group is something you should be doing at home.
(Week 1 is the exception: nothing is read at the end of the first lecture; its five
points are all read on Saturday.)

Weeks are checked cumulatively — Week 3 also re-checks Weeks 1 and 2. If a later
change breaks something earlier, you want to hear about it from CI, not in December.

To look at one week on its own, say to confirm Week 2 still passes:

```bash
AIASD_WEEK=2 python .github/check_deliverables.py
```

Run the checks locally before you push:

```bash
python .github/check_deliverables.py
```

A red cross is not a grade. It is a list of what is still missing, and it is far
better to see it on Tuesday than after the deadline.

**The secret scan runs on every push, at every week.** If an API key reaches the
repository the check fails loudly — remove it, rotate the key immediately, and
remember that a committed key is an automatic 10-point deduction.

---

## Repository rules

- Commit **at least three times a week, spread across the week** — one push on Saturday night costs the commit-discipline point.
- Fill in that week's `ai_log_NN.md` — every week has one, and a person reads it.
- Do **not** commit `.venv/`, `__pycache__/`, or API keys.
- Run `ruff check .` before committing — it catches the unused imports AI tends to leave behind.
- Use `.env` for secrets and keep it in `.gitignore`.
- Your app must work on a phone as well as a laptop. Narrow your browser window to ~390px now and then — if something is cut off or scrolls sideways, fix it while the page is small, not in Week 10.
