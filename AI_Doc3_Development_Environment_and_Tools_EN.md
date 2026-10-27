# Development Environment and Tools

AI-Assisted Software Development · Atlas University · Fall 2026–2027

*Week 1 Pre-Reading · Prof. Dr. Vedat Coşkun*

# 1. Installing Python

This course uses Python 3.12. Any version from 3.10 upwards will work. The automated checks run on 3.12, so prefer 3.12.

## 1.1 Windows

1. Go to python.org/downloads and download the latest 3.12 installer.
2. Run the installer. On the first screen, tick the box labelled "Add python.exe to PATH" (PATH is the list of folders in which Windows looks for a program when you type its name). Many people forget this step.
3. Choose "Install Now".
4. Open PowerShell and check the installation with the command: python --version

> **⚠️ Warning:** If you skip the PATH checkbox, Windows will not find the python command, and nothing else in this document will work. To fix it, run the installer again and choose "Modify".

## 1.2 macOS

macOS comes with a Python that belongs to the operating system. Do not use that one for your own work. Instead, install your own copy:

```bash
brew install python@3.12
```

If you do not have Homebrew (a program that installs other programs on macOS from the terminal), install it from brew.sh first, and then run the line above.

Check the result:

```bash
python3 --version
```

> **📌 Note:** *On macOS the command is usually python3, not python. Both forms appear in this document; use whichever one your machine responds to.*

## 1.3 Linux

On Debian and Ubuntu:

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

The python3.12-venv package matters. Without it, virtual environments cannot be created.

# 2. Basic Terminal Commands

You will spend most of this term in the terminal (the text window in which you type commands instead of clicking). Six commands cover almost everything you need.

```bash
pwd # where am I?
ls # what is in this folder? (Windows: dir)
cd folder_name # go into a folder
cd .. # go up one level
mkdir new_folder # create a folder
cat file.txt # print a file (Windows: type)
```

> **✅ Tip:** A path that contains spaces must be written inside quotation marks, for example cd "My Documents". Many people make this mistake on Windows and macOS.

# 3. The python Command and the -m Flag

You will see commands written as python -m something rather than just something. The -m flag (an option added after the command name) tells Python to run a module from the environment you are currently in, instead of searching for a program on your system PATH.

```bash
pip install requests # uses whatever pip the system finds first
python -m pip install requests # uses the pip belonging to THIS python
```

The second form is safer. On a machine with several Python installations, the first form may install a package in a place where you never find it again. The second form installs it where you want it. Prefer python -m whenever a command offers both forms.

# 4. Virtual Environments

Every Python project should have its own dependency environment (its own private set of installed packages). A virtual environment creates an isolated Python installation inside your project folder, so that packages from other projects cannot interfere with it.

## 4.1 Why bother?

- Imagine that project A needs pandas 1.5 and project B needs pandas 2.0. If both are installed system-wide, only one version can exist at a time, and whichever project you install last breaks the other.

- With a virtual environment, each project uses its own version, and neither project notices the other.

- A requirements.txt file (a plain list of the packages and versions a project needs) then lets anyone else rebuild your exact environment.

## 4.2 Creating and activating

In your project folder, run:

```bash
python -m venv .venv
```

This creates a hidden directory called .venv. The course template uses that name, so you should use it too.

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (Command Prompt)
.venv\Scripts\activate.bat
```

> **⚠️ Windows:** If PowerShell says "running scripts is disabled on this system", run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, and then activate again. Or use Command Prompt with `.venv\Scripts\activate.bat`.

Once the environment is active, your prompt changes:

```
(.venv) $
```

> **📌 Note:** *If "(.venv)" appears at the start of your prompt, the environment is active, and python -m pip install will now put packages only into it.*

## 4.3 The "externally-managed-environment" error

On macOS and Linux, python -m pip install may refuse to run and show this message:

```
error: externally-managed-environment
× This environment is externally managed
```

This is not a fault; it is a protection. The operating system uses its own Python for its own system tools, and installing packages into that Python can break them. For that reason, the installation is blocked.

The fix is simple: install into your virtual environment rather than into the system. If you are seeing this error, you have almost certainly forgotten to activate the environment.

```bash
source .venv/bin/activate # activate first
python -m pip install package_name # then install
```

How do you check? Look at whether your prompt starts with (.venv). If it does not, the environment is not active. Each new terminal window needs to be activated again: you create the environment once, but you activate it every time.

> **⚠️ Warning:** The error message suggests the option --break-system-packages. Do not use it. It damages the system Python, and the problems it causes later are hard to trace. The virtual environment is the correct answer.

## 4.4 Installing and freezing packages

With the environment active, install a package:

```bash
python -m pip install requests
```

To see what is installed in the active environment, run `pip freeze`. It prints one line for each package, with its exact version. (The test in §8 shows it.)

In this course the requirements files come from the course: `requirements.txt` at the root of your repository, and `weekNN/requirements.txt` in a week that needs new packages. To install from one of them, run:

```bash
python -m pip install -r requirements.txt
```

Do not run `pip freeze > requirements.txt`: it overwrites the course's file. Add your own packages to the week's requirements file only when the assignment says so.

## 4.5 Deactivating

To leave the virtual environment, run:

```bash
deactivate
```

> **⚠️ Warning:** The .venv folder is large (30–100 MB). Never push it to GitHub. The course template already excludes it in .gitignore (the file that tells git which files to ignore).

# 5. Installing VS Code

1. Go to code.visualstudio.com, download the build for your operating system, and install it.
2. Open VS Code and click the Extensions icon on the left (Ctrl+Shift+X).
3. Search for "Python" and install Microsoft's Python extension.
4. Open your project folder through the menu: File → Open Folder.
5. Select the Python interpreter at the bottom right of the window, and choose the one inside your .venv.

> **✅ Tip:** The VS Code terminal (Ctrl+`) picks up the active virtual environment automatically, so you do not need to activate it again there.

> **ℹ️ Signing in with GitHub:** On first start, VS Code offers to sign in with GitHub (for
> Settings Sync or Copilot). This step is optional, because the course works from the
> terminal. If you accept, sign in with **the same GitHub account as your course repository**:
> VS Code then also handles `git push` for you, without asking for a password or token.
> If you sign in with a different account, your pushes can go to the wrong place. For
> example, a student signs in to VS Code with a personal account and pushes from the editor.
> The commits then land in a repository that the course never sees.

# 6. The Tools You Will Use

You do not need to install any of these tools now. Each one arrives in the week that uses it, together with that week's assignment. This section helps you recognise the tools before the term starts: what each tool is for, and where in your project it will appear.

For each tool, four questions are answered: what is it, where is it used in this project, how is it installed, and what is the smallest example that works?

## 6.1 HTML, CSS and JavaScript

### Weeks 4–12 · the web client

### What is it?

HTML says what is on a page. CSS says how it looks. JavaScript makes the page react: for example, it sends a request to your server when the user taps a button.

### Where is it used in this project?

- In Week 4 you build a clickable prototype: one HTML file for each screen, in `week04/prototype/`.
- In Week 6 these screens become the real web client, in `web/`. Each page calls your server with `fetch`, and your FastAPI server serves the pages.
- The mobile client comes in Week 7, with the framework that you choose (`AI_PLATFORMS_AND_STORES`).

### Installation

```
Nothing to install — a browser and VS Code are enough.
```

### Smallest working example

```html
<!-- serves: REQ-006 -->
<button id="check">Check the server</button>
<p id="result"></p>
<script>
  document.getElementById("check").onclick = async () => {
    const response = await fetch("/health");
    const data = await response.json();
    document.getElementById("result").textContent = data.status;
  };
</script>
```

> **✅ Tip:** Look at every page 390 px wide: press F12, then the phone icon. If anything is cut off or scrolls sideways, fix it now. Repairing it in Week 10 costs much more.

### Why this tool?

The pages of your prototype become the pages of your web client. You do not learn a new tool for the web, and there is no build step. So your time goes to what is assessed: the chain from a requirement to a working, tested feature.

## 6.2 FastAPI and uvicorn

### Weeks 5–12 · the server

### What is it?

FastAPI is a Python library for writing web servers. You write one Python function for each endpoint (a method and a path, for example `GET /health`), and FastAPI turns what the function returns into JSON. uvicorn is the program that runs the server.

### Where is it used in this project?

- In Week 5 you write the server skeleton in `server/main.py`. Each route answers 501 ("not built yet") until its week. `week05/FASTAPI_CARD_EN.md` explains FastAPI on one page.
- From Week 6 the routes work: the login is the course's module (`server/course_login.py`), and your own feature runs on your server.
- The web client (§6.1), the mobile client (Week 7) and the chatbot (Week 8) all talk to this server.

### Installation

```bash
python -m pip install -r week05/requirements.txt
```

Week 5's requirements file brings FastAPI, uvicorn and pytest. Later weeks have their own file with more packages.

### Smallest working example

```python
# server/main.py
from fastapi import FastAPI

app = FastAPI(title="My project")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
```

Run it from the root of your repository:

```bash
uvicorn server.main:app --reload
```

> **✅ Tip:** Open http://127.0.0.1:8000/docs in your browser. FastAPI lists every route there. A route that is not in the list does not exist, whatever the assistant said.

## 6.3 python-dotenv

### Weeks 6–12 · security

### What is it?

python-dotenv keeps passwords and API keys out of your code. It reads them from a file called .env at start-up and puts them into environment variables (named values that the operating system makes available to a running program).

### Where is it used in this project?

It is used from Week 6, when the server needs the password of the e-mail account that sends the login code. In Week 8 the `.env` file also holds the API key of your chatbot. The rule of this course: passwords and keys are never written into code.

### Installation

```bash
python -m pip install -r week06/requirements.txt
```

### Smallest working example

```python
# .env (NEVER pushed to the repository):
# SMTP_PASSWORD=abcd efgh ijkl mnop
import os

from dotenv import load_dotenv

load_dotenv()
password = os.getenv("SMTP_PASSWORD")
```

> **✅ Tip:** Keep a .env.example file in the repository that contains the variable names and no values, so that anyone who clones your project knows what they need to fill in.

## 6.4 pytest

### Weeks 5–12 · tests

### What is it?

pytest is the most widely used Python testing library. You write small functions that check that your code does what you expect. pytest runs them all and reports what passed and what did not.

### Where is it used in this project?

- In Week 5 you write your first tests, in `server/tests/`. Each test is named by a test case id, for example `test_TC_001_01_a_code_is_sent`.
- From Week 6, the course tests (`course_tests/`) and your own tests run on GitHub on every push (§6.5).
- Tests are the most concrete way to check whether AI-written code is correct.

### Installation

```bash
python -m pip install -r week05/requirements.txt
```

### Smallest working example

```python
# server/tests/test_health.py
from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_health_answers_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Run it with:

```bash
python -m pytest -v
```

> **✅ Tip:** The file name must start with test_, and so must each function, because that is how pytest finds them.

## 6.5 GitHub Actions

### Weeks 1–12 · continuous integration

### What is it?

GitHub Actions is GitHub's automation system. Every time you push, it runs commands on GitHub's own servers. It shows a green tick when everything passes and a red cross when something fails. The commands are in a YAML file (a configuration file in a simple text format) in `.github/workflows/`.

### Where is it used in this project?

Your repository already has this file: `.github/workflows/check.yml`. Do not change it. On every push it runs two jobs:

- **Weekly deliverables:** the checker. From Week 6 it also runs the tests (§6.4).
- **Lint and format:** ruff (§6.6).

Open the **Actions** tab of your repository to see the result. From Week 6, your lecture mark reads this run.

### Installation

```
Nothing to install — the file is already in your repository.
```

### Smallest working example

```yaml
# .github/workflows/check.yml (a part of it)
jobs:
  deliverables:
    name: Weekly deliverables
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Check this week's deliverables
        run: python .github/check_deliverables.py
```

> **✅ Tip:** If a run turns red, fix the problem and push a new commit. Never force push.

## 6.6 ruff

### Weeks 1–12 · code quality

### What is it?

ruff is one tool that does two jobs. It inspects Python code (a linter: a program that looks for mistakes and bad style), and it formats the code (a formatter: a program that rearranges its layout). It finds unused imports, undefined names, wrong indentation and much more, and it fixes most of these problems for you. It is very fast.

### Where is it used in this project?

It runs on GitHub on every push, in the "Lint and format" job (§6.5). Both `ruff check .` and `ruff format --check .` must pass, or the run turns red. Run them on your laptop before you push.

### Installation

```bash
python -m pip install ruff==0.15.11
```

You need it from Week 1, because it runs on every push. Install this exact version: it is the one that GitHub uses.

### Smallest working example

```bash
ruff check . # list problems
ruff check . --fix # fix what can be fixed
ruff format . # format the code
ruff format --check . # only check whether it is formatted
```

> **✅ Tip:** The settings live in ruff.toml at the repository root. AI-generated code often leaves unused imports behind, and ruff catches them at once. This makes it very useful in AI-assisted development.

## 6.7 Mermaid

### Weeks 2, 5, 10 · diagrams

### What is it?

Mermaid is a syntax for writing diagrams as text instead of drawing them. You write "A goes to B", and Mermaid draws the picture. GitHub renders Mermaid inside .mmd and .md files directly.

### Where is it used in this project?

Every diagram of the course is written in Mermaid. There are four:

- the system context diagram (`PROPOSAL.md` §5, Week 2);
- the use case diagram (`week02/SRS.md` §3, Week 2);
- the architecture (`week05/DESIGN.md`, Week 5);
- the deployment diagram (Week 10).

The course asks for no other diagrams.

### Installation

```
Nothing to install — preview at mermaid.live and commit the file.
```

### Smallest working example

```
flowchart LR
    web[Web client] --> server[Server]
    mobile[Mobile client] --> server
    server --> db[(Database)]
    server --> mail[E-mail service]
```

> **✅ Tip:** Because the diagram is text, it is versioned by git, so you can see what changed and when. A diagram drawn in a graphics program gives you none of that.

## 6.8 Summary: Which Tool, Which Week?

Keep this table as a reference for the term.

| Tool | What it does | Weeks |
|---|---|---|
| **HTML, CSS, JavaScript** | The prototype, then the web client | 4–12 |
| **FastAPI + uvicorn** | The server | 5–12 |
| **python-dotenv** | Passwords and keys | 6–12 |
| **pytest** | Tests | 5–12 |
| **ruff** | Linting and formatting, on every push | 1–12 |
| **GitHub Actions** | Continuous integration, on every push | 1–12 |
| **Mermaid** | Diagrams | 2, 5, 10 |

> **✅ Tip:** Do not install all of these now. Each one arrives in its own week, with the assignment that needs it. For now it is enough to know what each one is for.

# 7. Installing Git

Git keeps the history of your project and sends your work to GitHub. Install it once:

- **Windows:** download the installer from git-scm.com and run it. The default choices are fine.
- **macOS:** run `xcode-select --install` in the terminal (or `brew install git` if you use Homebrew).
- **Linux (Debian and Ubuntu):** run `sudo apt install git`.

Then run these three commands once. They tell Git who you are and how `git pull` works:

```bash
git config --global user.name "Your Name"
git config --global user.email "the e-mail of your GitHub account"
git config --global pull.rebase false
```

> **📌 Note:** *Use the e-mail address of your GitHub account, so that GitHub links your commits to you. Without the first two lines, Git may refuse your first commit with "Please tell me who you are". The third line stops `git pull` from failing with "Need to specify how to reconcile divergent branches".*

# 8. Checklist Before the First Session

### Each of the following must produce output. If one does not, fix it before class. Otherwise you will only watch other people work in the session.

```bash
python --version # 3.10 or newer, 3.12 preferred
pip --version
git --version
```

Virtual environment test. Type one command at a time. Where a comment shows a Windows PowerShell form, use that form on Windows:

```bash
mkdir test_env
cd test_env
python -m venv .venv
source .venv/bin/activate # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install requests
python -c "import requests; print('OK')"
pip freeze # lists requests and the packages it needs, with their versions
deactivate
cd ..
rm -rf test_env # Windows PowerShell: Remove-Item -Recurse -Force test_env
```

> **✅ Tip:** If that prints "OK", your virtual environment and pip are working, and you are ready for Week 1.
