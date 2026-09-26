# Setup Card — the whole thing on one page

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**

Keep this one open. Everything you need to run, all term, is on this page.

---

## Once, before Week 1

**1 · Create your repository.** On the course template, click **Use this template →
Create a new repository**. Name it `aiasd-project`. Set it to **Private** — the form
opens on Public. Then **Settings → Collaborators → Add people** and add `VedatCOSKUN`.

**2 · Let your computer talk to GitHub.** Passwords stopped working for this in 2021.
Do it once and never again:

```bash
brew install gh          # Windows: winget install GitHub.cli
gh auth login
```

Answer: `GitHub.com` → `HTTPS` → `Y` → `Login with a web browser`.

*Cannot install software on your machine?* Use a token instead: **Settings → Developer
settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**,
tick exactly one box — **`repo`** — and copy it. When git asks for a password, paste the
token. Treat it like a password to your whole account: never put it in a file, a chat,
or a commit.

**3 · Copy it to your machine.**

```bash
git clone https://github.com/<your-username>/aiasd-project.git
cd aiasd-project
```

**4 · Say who you are, and push.** Open `student.json`, fill in all five fields —
`section` is `en` or `tr` — then:

```bash
git add student.json
git commit -m "week01: student identity"
git push
```

**If that push works, you are done.** That is the whole test.

---

## Every week, the same four

```bash
python .github/check_deliverables.py

git add .
git commit -m "week01: what I did"
git push
```

Nothing else changes for twelve weeks. Only the commit message. Run the checker as
often as you like — it is a to-do list, not a grade, and running it costs nothing.

Two more, when a week needs them:

```bash
pip install -r weekNN/requirements.txt
streamlit run app.py
```

---

## Two remotes, two very different commands

Your repository has `origin` — your own copy on GitHub. Some weeks also hand you a
starter folder from the course template, and for that you add a second remote called
`template`. They are not interchangeable.

| | |
|---|---|
| `git pull` | From `origin`. Your own repository, on another machine or after an edit in the browser. Normal, everyday, safe. |
| `git pull template main` | **Never.** |

The template is a separate repository with no history in common with yours — your copy
was created from it, not cloned from it. Merging the two tries to reconcile every file
at once: your filled-in `student.json` against the blank one, your finished `hello.py`
against the stub, your work against the scaffold. You would spend the lecture
untangling conflicts, and a `git pull` that once succeeded keeps trying to do it again
every time.

Take the one path you actually want instead:

```bash
git remote add template https://github.com/vedatcoskun-course/aiasd-template.git   # once, ever
git fetch template
git checkout template/main -- week06
```

That copies exactly the path you name and touches nothing else. Run it **before** you
write anything in that folder — run it afterwards and it overwrites your work.

---

## When something goes wrong

> **Read the LAST line of an error, not the first.** Git prints the diagnosis at the
> bottom. The lines above it are context.

| What you see | What it means |
|---|---|
| `Authentication failed`<br>`could not read Username for 'https://github.com'` | GitHub does not know who you are. Run `gh auth login`. If it still fails, `gh auth status` — you may be signed in as the wrong account. |
| `Support for password authentication was removed` | Same cause. Your GitHub password is not usable here, and no amount of retyping it will help. |
| `! [rejected] main -> main (fetch first)` | GitHub has a commit you do not have — usually because you edited a file in the browser. `git pull --rebase`, then push again. |
| `nothing to commit, working tree clean` | Git sees no change. Either the editor did not save, or you are in the wrong folder. Run `pwd` and look. |
| `fatal: not a git repository` | You are outside the project. `cd` into `aiasd-project` and try again. |
| `index.lock ... File exists` | A git command was interrupted. `rm -f .git/index.lock` and retry. |
| Checker says *Cannot tell which week it is* | First run, with no network. Connect once and run it again; after that it works offline. |
| `command not found: python` | Try `python3` instead. On macOS that is usually the one that exists. |
| `refusing to merge unrelated histories` | You pulled from `template` instead of `origin`. Do not pass `--allow-unrelated-histories`; see the section above. |

---

**Still stuck?** Ask an AI assistant — but on git authentication specifically, be
sceptical. It changed in 2021 and most of the internet still describes the old way. If
you are told to use your GitHub password, or to run `git config credential.helper
store`, that advice is out of date. Ignore it and come back to this card.

The full weekly routine — what the marks are for, what happens at the end of each
lecture, what to do if you cannot be there — is in
[`AI_WEEKLY_WORKFLOW_STUDENT_EN.md`](AI_WEEKLY_WORKFLOW_STUDENT_EN.md).
