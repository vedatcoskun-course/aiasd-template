# Development Environment and Tools

AI-Assisted Software Development · Atlas University · Fall 2026–2027

*Week 1 Pre-Reading · Prof. Dr. Vedat Coşkun*

# 1. Installing Python

This course uses Python 3.12. Anything from 3.10 upwards will work, but 3.12 is what the automated checks run, so it is the version to prefer.

## 1.1 Windows

1. Go to python.org/downloads and download the latest 3.12 installer.
2. Run the installer. On the first screen, tick "Add python.exe to PATH" — this is the step everyone forgets.
3. Choose "Install Now".
4. Open PowerShell and check: python --version

> **⚠️ Warning:** If you skip the PATH checkbox, Windows will not find the python command and nothing else in this document will work. Re-run the installer and choose "Modify" to fix it.

## 1.2 macOS

macOS ships with a Python that belongs to the operating system. Do not use it for your own work — install your own:

```bash
brew install python@3.12
```

If you do not have Homebrew, install it from brew.sh first, then run the line above.

Check the result:

```bash
python3 --version
```

> **📌 Note:** *On macOS the command is usually python3, not python. Both appear in this document; use whichever your machine responds to.*

## 1.3 Linux

On Debian and Ubuntu:

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

The python3.12-venv package matters — without it, virtual environments will not be created.

# 2. Basic Terminal Commands

You will live in the terminal this term. Six commands cover almost everything you need.

```bash
pwd # where am I?
ls # what is in this folder? (Windows: dir)
cd folder_name # go into a folder
cd .. # go up one level
mkdir new_folder # create a folder
cat file.txt # print a file (Windows: type)
```

> **✅ Tip:** A path with spaces must be quoted: cd "My Documents". This catches people out constantly on Windows and macOS.

# 3. The python Command and the -m Flag

You will see commands written as python -m something rather than just something. The -m flag tells Python to run a module from the environment you are currently in, instead of hunting for a program on your system PATH.

```bash
pip install streamlit # uses whatever pip the system finds first
python -m pip install streamlit # uses the pip belonging to THIS python
```

The second form is safer, and on a machine with several Python installations it is the difference between installing a package where you want it and installing it somewhere you will never find it again. Prefer python -m whenever a command offers both forms.

# 4. Virtual Environments

Every Python project should have its own dependency environment. A virtual environment creates an isolated Python installation inside your project folder, so packages from other projects cannot interfere.

## 4.1 Why bother?

- Project A needs pandas 1.5; project B needs pandas 2.0. Installed system-wide, they fight.

- With a virtual environment each project uses its own version and neither notices the other.

- requirements.txt then lets anyone else rebuild your exact environment.

## 4.2 Creating and activating

In your project folder:

```bash
python -m venv .venv
```

This creates a hidden directory called .venv. The course template uses that name; use it too.

Activate it:

```bash
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (Command Prompt)
.venv\Scripts\activate.bat
```

Once active, your prompt changes:

```
(.venv) $
```

> **📌 Note:** *If "(.venv)" appears at the start of your prompt the environment is active, and pip install will now put packages only into it.*

## 4.3 The "externally-managed-environment" error

On macOS and Linux, pip install may refuse with:

```
error: externally-managed-environment
× This environment is externally managed
```

This is not a fault, it is a guard. The operating system uses its own Python for system tooling, and installing packages into it can break things. So it is blocked.

The fix is simple: install into your virtual environment rather than into the system. If you are seeing this error, you have almost certainly forgotten to activate.

```bash
source .venv/bin/activate # activate first
pip install package_name # then install
```

How to check: does your prompt start with (.venv)? If not, the environment is not active. Each new terminal window needs activating again — you create the environment once, you activate it every time.

> **⚠️ Warning:** The error message suggests --break-system-packages. Do not use it. It pollutes the system Python and causes problems later that are difficult to trace back. The virtual environment is the correct answer.

## 4.4 Installing and freezing packages

With the environment active:

```bash
pip install anthropic python-dotenv
```

Record what is installed, so someone else can rebuild it:

```bash
pip freeze > requirements.txt
```

And to rebuild from that record on another machine:

```bash
pip install -r requirements.txt
```

## 4.5 Deactivating

To leave the virtual environment:

```bash
deactivate
```

> **⚠️ Warning:** The .venv folder is large (30–100 MB). Never push it to GitHub. The course template already excludes it in .gitignore.

# 5. Installing VS Code

1. Go to code.visualstudio.com, download the build for your operating system and install it.
2. Open VS Code and click the Extensions icon on the left (Ctrl+Shift+X).
3. Search for "Python" and install Microsoft's Python extension.
4. Open your project folder: File → Open Folder.
5. Select the Python interpreter at the bottom right — choose the one inside your .venv.

> **✅ Tip:** The VS Code terminal (Ctrl+`) picks up the active virtual environment automatically, so you do not need to activate it again there.

# 6. The Tools You Will Use

You do not need to install any of these now. Each one arrives in the week that uses it, alongside that week's assignment. The purpose here is that you recognise the toolkit before the term starts: what each tool is for, and where in your project it will appear.

For each one: what is it, where is it used in this project, how is it installed, and what is the smallest example that works?

## 6.1 Streamlit

### Weeks 3–12 · the entire interface

### What is it?

A library for writing web interfaces in Python. No HTML, no CSS, no JavaScript — you write plain Python and Streamlit turns it into a page in the browser. Save the file and the page reloads itself.

### Where is it used in this project?

Every user interface in your project. The chatbot in Week 3, the application skeleton in Week 4, every screen after that.

### Installation

```bash
pip install streamlit
```

### Smallest working example

```python
import streamlit as st
st.title("Hello")
name = st.text_input("Your name:")
if name:
    st.write(f"Hello {name}!")
```

Run it with:

```bash
streamlit run app.py
```

> **✅ Tip:** Streamlit re-runs the whole script on every interaction. Anything that must survive goes in st.session_state — that is where the chat history lives.
> **✅ Tip:** Your application must also open on a phone and look right there — that is a course requirement. Practical rule: use layout="centered" in set_page_config, keep content in one column, avoid wide fixed-width tables. To test, narrow your browser window to roughly 390 pixels. If anything is cut off or scrolls sideways, fix it now; repairing it in Week 10 costs far more.

### Why this tool?

Why Streamlit? Because this course is not about interface engineering. Streamlit lets you write the interface in pure Python: no HTML, no CSS, no JavaScript, no build step. Every hour not spent fighting a frontend toolchain is an hour spent on what is actually assessed — the chain from requirements to architecture to testable code. And because the whole class is on one stack, the Week 10 interface tests and the Week 11 one-command deployment are possible at all, and you can get real help when you are stuck. Engineering teams standardise on one stack for exactly these reasons. If you want to use something else, come and talk to me in Week 2 — the door is not closed, but it carries extra responsibility.

## 6.2 Anthropic Claude API

### Weeks 2–12 · cloud LLM

### What is it?

The official SDK for reaching Claude models from Python. It sends your request over the internet to Anthropic's servers and returns the answer as text. Powerful, but it needs an API key and costs money per call.

### Where is it used in this project?

The cloud option in your Week 3 chatbot, the core AI feature of your project in Week 5, and the generation step of your RAG pipeline in Week 6.

### Installation

```bash
pip install anthropic
```

### Smallest working example

```python
import anthropic
client = anthropic.Anthropic() # reads the key from .env
reply = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Hello"}],
)
print(reply.content[0].text)
```

> **✅ Tip:** Never write an API key into your code and never push one to GitHub. The key lives in .env, and .env is listed in .gitignore. A key committed to the repository costs 10 points.

## 6.3 Google Gemini API

### Weeks 2–12 · comparison

### What is it?

The SDK for Google's Gemini models. Functionally similar to Claude; it is here so that you see how a different provider does the same job. It has a free usage tier.

### Where is it used in this project?

Side-by-side comparison exercises — the same prompt to two models. Also so that you are not dependent on a single provider.

### Installation

```bash
pip install google-generativeai
```

### Smallest working example

```python
import google.generativeai as genai
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
print(model.generate_content("Hello").text)
```

> **✅ Tip:** Two different answers to the same question is the quickest way to see that a model does not "know" the truth — it produces a probable piece of text.

## 6.4 Ollama

### Weeks 3–12 · local models

### What is it?

A program that runs language models on your own computer. No internet, no API key, no cost — in exchange you work with smaller and slower models. It runs a server in the background at localhost:11434 and your Python code talks to it.

### Where is it used in this project?

The local option in your Week 3 chatbot, and anywhere the data must not leave the machine.

### Installation

```bash
Install the program from ollama.com, then:
pip install ollama
ollama pull qwen2.5:3b
```

### Smallest working example

```python
import ollama
reply = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "Hello"}],
)
print(reply["message"]["content"])
```

> **✅ Tip:** Choose the model size to fit your machine: qwen2.5:3b for 8 GB RAM or more, qwen2.5:1.5b for 4–8 GB, qwen2.5:0.5b below that. In the Week 3 assignment you will write down which you chose and why.

## 6.5 sentence-transformers and BGE-M3

### Weeks 3, 6 · embeddings

### What is it?

A library and a model that turn text into a list of numbers — a vector. BGE-M3 is multilingual and handles Turkish well. Note carefully: this is not an LLM. It does not generate text; it converts meaning into numbers.

### Where is it used in this project?

The similarity experiment in Week 3, and the document-retrieval step of RAG in Week 6. Question and documents go into the same space, and the nearest ones are found.

### Installation

```bash
pip install sentence-transformers
```

### Smallest working example

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-m3")
v = model.encode(["the cat is asleep", "kitty is napping", "it is raining"],
                 normalize_embeddings=True)
print(v @ v.T) # similarity matrix
```

> **✅ Tip:** BGE-M3 downloads about 2.2 GB. If your machine cannot take it, use paraphrase-multilingual-MiniLM-L12-v2 (~470 MB) instead — weaker, but it works.

## 6.6 FAISS

### Week 6 · vector search

### What is it?

A library that finds, among thousands of vectors, the ones nearest to a query — fast. Built by Facebook AI. No database to install: it works in memory and saves to a file.

### Where is it used in this project?

The search layer of your RAG pipeline. Documents become embeddings, the embeddings go into FAISS, and when a user asks something the most relevant pieces come back out.

### Installation

```bash
pip install faiss-cpu
```

### Smallest working example

```python
import faiss
index = faiss.IndexFlatIP(1024) # 1024 = vector size
index.add(document_vectors)
scores, ids = index.search(question_vector, k=3)
```

> **✅ Tip:** IndexFlatIP computes cosine similarity on normalised vectors — which is why encode is called with normalize_embeddings=True.

## 6.7 python-dotenv

### Weeks 2–12 · security

### What is it?

Keeps API keys out of your code by reading them from a file called .env at start-up and putting them into environment variables.

### Where is it used in this project?

Every week that uses an API key. The unbreakable rule of this course: keys are not written into code.

### Installation

```bash
pip install python-dotenv
```

### Smallest working example

```python
# .env (NEVER pushed to the repository):
# ANTHROPIC_API_KEY=sk-ant-...
from dotenv import load_dotenv
import os
load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")
```

> **✅ Tip:** Keep a .env.example in the repository with the variable names and no values, so that anyone cloning your project knows what they need to fill in.

## 6.8 pytest

### Week 9 · unit testing

### What is it?

The most widely used Python testing library. You write small functions that assert your code does what you expect; pytest runs them all and reports what passed and what did not.

### Where is it used in this project?

Week 9, testing your project's helper functions. It is the most concrete way to measure whether AI-written code is actually correct.

### Installation

```bash
pip install pytest
```

### Smallest working example

```python
# test_text.py
from text import shorten
def test_shorten():
    assert shorten("hello world", 5) == "hello"
def test_short_text_unchanged():
    assert shorten("ok", 10) == "ok"
```

Run it with:

```bash
pytest -v
```

> **✅ Tip:** The file name must start with test_ and so must each function — that is how pytest finds them.

## 6.9 Ragas

### Week 9 · RAG quality

### What is it?

A library that measures the answer quality of RAG systems. It turns "is the answer good?" into numbers: is the answer grounded in the retrieved documents (faithfulness), were the retrieved documents relevant (context precision), does the answer address the question (answer relevancy).

### Where is it used in this project?

Week 9, evaluating the RAG pipeline you built in Week 6. Instead of "I think it works well" you will present a measured score.

### Installation

```bash
pip install ragas
```

### Smallest working example

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
result = evaluate(dataset,
                  metrics=[faithfulness, answer_relevancy])
print(result)
```

> **✅ Tip:** Ragas uses an LLM to do the evaluating, so measuring also costs API calls. Start with a small test set.

## 6.10 Selenium

### Week 10 · interface testing

### What is it?

A tool that drives a browser programmatically. It opens the page, clicks buttons, types into boxes and reads the result — it does automatically what a real user would do by hand.

### Where is it used in this project?

Week 10, testing your Streamlit interface: does the app open, can a user type something and get an answer, and does it all still work at phone width?

### Installation

```bash
pip install selenium
```

### Smallest working example

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()
driver.set_window_size(390, 844) # phone viewport
driver.get("http://localhost:8501")
box = driver.find_element(By.TAG_NAME, "input")
box.send_keys("hello")
driver.quit()
```

> **✅ Tip:** Your Streamlit app must already be running in a separate terminal — Selenium connects to an existing page, it does not start your application for you.

## 6.11 GitHub Actions

### Week 10 · continuous integration

### What is it?

GitHub's automation system. Every time you push, it runs the commands you specify on GitHub's own servers — a green tick if your tests pass, a red cross if they do not. Nothing to install: you put a YAML file in .github/workflows/.

### Where is it used in this project?

Week 10, running your pytest suite automatically. It can also check that your weekly deliverables are complete — which is exactly what the checker in your repository already does.

### Installation

```
Nothing to install — adding a file to the repository is enough.
```

### Smallest working example

```yaml
# .github/workflows/test.yml
name: tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest
```

> **✅ Tip:** Indentation is meaningful in YAML and tab characters are rejected — use spaces only.

## 6.12 ruff

### Week 9 · code quality

### What is it?

A single tool that both inspects Python code (a linter) and formats it (a formatter). It finds unused imports, undefined names, inconsistent indentation and much else, and fixes most of it for you. Written in Rust, so it is very fast.

### Where is it used in this project?

Part of the Week 9 deliverable: ruff check . must report zero errors. You will also run it inside GitHub Actions, so every push is checked automatically.

### Installation

```bash
pip install ruff
```

### Smallest working example

```bash
ruff check . # list problems
ruff check . --fix # fix what can be fixed
ruff format . # format the code
ruff format --check . # only check whether it is formatted
```

> **✅ Tip:** Settings live in ruff.toml at the repository root. AI-generated code frequently leaves unused imports behind — ruff catches them immediately, which makes it particularly useful in AI-assisted development.

## 6.13 Mermaid

### Weeks 2, 4, 6, 8, 11 · diagrams

### What is it?

A syntax for writing diagrams as text instead of drawing them. You write "A goes to B" and Mermaid draws the picture. GitHub renders Mermaid inside .mmd and .md files directly.

### Where is it used in this project?

Every design document in the course: use case, sequence, architecture, data flow, activity and deployment diagrams.

### Installation

```
Nothing to install — preview at mermaid.live and commit the file.
```

### Smallest working example

```
sequenceDiagram
    actor User
    participant UI as Streamlit
    participant LLM
    User->>UI: types a question
    UI->>LLM: sends the request
    LLM-->>UI: returns an answer
    UI-->>User: displays it
```

> **✅ Tip:** Because the diagram is text, it is versioned by git — you can see what changed and when. A diagram drawn in a graphics program gives you none of that.

## 6.14 Summary: Which Tool, Which Week?

Keep this table as a reference for the term.

| Tool                           | What it does        | Weeks      |
| ---------------------------------- | ----------------------- | -------------- |
| **Streamlit**                      | Web interface           | 3–12           |
| **Claude API**                     | Cloud LLM               | 2–12           |
| **Gemini API**                     | Cloud LLM (comparison)  | 2–12           |
| **Ollama + Qwen**                  | Local LLM               | 3–12           |
| **sentence-transformers / BGE-M3** | Embeddings              | 3, 6           |
| **FAISS**                          | Vector search           | 6              |
| **python-dotenv**                  | API key handling        | 2–12           |
| **pytest**                         | Unit testing            | 9              |
| **Ragas**                          | RAG quality measurement | 9              |
| **ruff**                           | Linting and formatting  | 9              |
| **Selenium**                       | Interface testing       | 10             |
| **GitHub Actions**                 | Continuous integration  | 10             |
| **Mermaid**                        | Diagrams                | 2, 4, 6, 8, 11 |

> **✅ Tip:** Do not install all of these now. Each arrives in its own week, with the assignment that needs it. For now it is enough to know what each one is for.

# 7. Checklist Before the First Session

### Each of the following must produce output. If one does not, sort it out before class — otherwise you will spend the session watching other people work.

```bash
python --version # 3.10 or newer, 3.12 preferred
pip --version
git --version
```

Virtual environment test:

```bash
mkdir test_env && cd test_env
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install requests
python -c "import requests; print('OK')"
deactivate
cd .. && rm -rf test_env
```

> **✅ Tip:** If that prints "OK", your virtual environment and pip are working and you are ready for Week 1.
