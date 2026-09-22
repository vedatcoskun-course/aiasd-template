# Working with AI tools — what they are, what they cost, and how to spend them

*Methodology reading. Part I is a map of the tools as they stand at the start of the
2026–27 autumn term; Part II is the working habits, which change far more slowly. The
facts in Part I — model names, prices, limits — were checked against the vendors' own
pages on 20 September 2026 and will be wrong by spring. Treat them as a snapshot, and
treat the pattern behind them as the thing to learn. This document is handed out as Doc 4 and is also presented in
Week 1 as a slide deck; the two say the same things in the same order, so that a student
who reads this and a student who listened heard the same course.*

*It is one of three Week 1 readings, and each has one job. **Doc 2, AI Technical
Background**, explains how the machine works — neurons, attention, tokens, embeddings,
sampling, RAG. **Doc 3, Development Environment and Tools**, sets up your machine and
walks through every tool you will use. This one is about the tools as products: what
they are, what they cost, how they ration you, and how to spend them well. Where the
three touch, this document points at the other two rather than repeating them.*

---

# Part I · The map

## 1. Three consequences of how a language model works

Doc 2 (§8–9) explains the mechanism: a model takes a sequence of tokens and returns a
probability for the next one, and everything you experience is that step repeated. This
document takes the mechanism as read and draws out the three consequences that decide
how the products behave and what they cost. If the previous sentence was not obvious,
read Doc 2's sections 6 to 9 first; they are short.

**It has no memory.** The model is a fixed set of weights. It does not learn from your
conversation, does not remember yesterday, and does not know what you said three turns
ago unless the application puts those turns back in front of it. The "memory" features
some products advertise are the application saving notes and re-inserting them. This is
why a long conversation costs more every turn — see Part II.

**It has a window.** A model can only attend to so many tokens at once: the *context
window*. Current frontier models offer 200 thousand to a million tokens, which sounds
unlimited and is not — a large codebase, or a long chat with pasted files, fills it, and
the model's quality degrades well before the hard limit. The window is a budget, not a
capacity.

**It is trained to a date.** The weights were frozen months before you use them. Ask
about anything after that date and the model either does not know, or — worse —
answers confidently from a world that no longer exists. Products bolt web search on top
to compensate; the model itself is a photograph.

"Reasoning" or "thinking" models are the same mechanism made to write out intermediate
steps before answering, and given more compute to do it. They are better at problems
with a right answer — a proof, a bug, a schedule — and slower and dearer at everything.
Most vendors now let you choose how much effort to spend per question. You should choose
consciously.

## 2. Four kinds of tool, not four brands

The names you will hear — Claude, ChatGPT, Gemini, Copilot, Cursor, Replit, Ollama — are
not four competitors selling the same thing. They are different *kinds* of product,
and the useful question is which kind you need for the task in front of you.

| Kind | What it is | Examples | Good for | Poor at |
|---|---|---|---|---|
| **Chat application** | A conversation in a browser or app; the model sees what you paste | Claude, ChatGPT, Gemini | Explaining, drafting, reviewing a pasted snippet, design discussion | Anything that needs your whole project in view |
| **Coding agent** | The model runs in your project folder or terminal, reads and edits files, runs commands, opens pull requests | Claude Code, Codex, GitHub Copilot's agent, Cursor | Multi-file changes, tests, refactors, "make CI green" | Vague goals — it will do *something*, quickly |
| **Cloud development environment with an agent** | A whole IDE and hosting in the browser, with an agent that builds and deploys | Replit | Getting a prototype live in an afternoon with nothing installed | Understanding what it built; costs scale with ambition |
| **Local model runtime** | Runs open-weight models on your own machine; nothing leaves it | Ollama (also LM Studio, llama.cpp) | Privacy, offline work, learning what a model *is*, embedding pipelines | Frontier-level quality; anything your laptop's memory cannot hold |

You will use at least three of the four this term: chat applications from Week 1,
Ollama from Week 3, and a coding agent from the moment your project has more than one
file.

## 3. The vendors, and the models inside them

Each vendor sells a *family* of models, tiered by size and price. The tiers matter more
than the brand names: the largest model in one family is usually closer to the largest
in another than it is to the smallest in its own.

### Anthropic — Claude

Four current models, all with text and image input, a 200K–1M token window:

| Model | Positioning | API price, per million tokens in / out |
|---|---|---|
| Claude Fable 5.1 | Smartest; demanding reasoning and long agentic work; slower | $10 / $50 |
| Claude Opus 5 | The recommended default for complex coding | $5 / $25 |
| Claude Sonnet 5 | Speed and intelligence balanced; the workhorse | $2 / $10 |
| Claude Haiku 4.5 | Fastest and cheapest; 200K window | $1 / $5 |

Read the price column as a ratio, not a bill: the top model costs **ten times** the
bottom one for the same conversation. On a subscription you do not pay per token, but
your usage allowance drains at that ratio. Asking the smartest model to rename a
variable is not wrong; it is ten times the price of asking the fastest one.

Consumer plans: **Free** (chat, web search, files, artifacts); **Pro** at $17–20 a month
(adds Claude Code, projects, the larger models, more usage); **Max** from $100 (5× or 20×
Pro's usage). The same account and the same allowance cover the chat app, the desktop
app and Claude Code — a heavy Claude Code afternoon empties your chat allowance too.

### OpenAI — ChatGPT

The same shape: a free tier on the mid-size model, a paid **Plus** tier adding the
frontier models and reasoning modes, and an expensive **Pro** tier with roughly five
times Plus's usage and the largest context. The model names change faster than any
other vendor's; at the time of writing the free tier runs GPT-5.6 and Plus adds GPT-6.
Codex is OpenAI's coding agent, with limited access on the free tier.

### Google — Gemini

Free tier on the fast model (Flash) with rationed access to the large one (Pro).
**AI Plus** at about $5 doubles the free limits; **AI Pro** at about $20 gives 4× and
full access to Gemini 3 Pro; **AI Ultra** from $100 gives up to 20×. Google's advantage
is integration — Docs, Drive, Gmail, Android — and a very large context window.

**Students:** Google has offered a free year of AI Pro to college students. Eligibility
is by country and changes; check the current offer before assuming it applies in Turkey.

### GitHub Copilot

The coding assistant inside VS Code, JetBrains and GitHub itself. **Free** tier: 2,000
completions a month and a small chat/agent allowance, on models including Claude Haiku
4.5 and GPT-5 mini. **Pro** at $10: unlimited completions plus a monthly credit for the
premium models. **Pro+** at $39: the largest models, four times the usage.

**Students:** the GitHub Student Developer Pack includes **Copilot Student** — unlimited
completions, an allowance of AI credits, limited chat and agent use — free while you are
a verified student. If you have not claimed the pack yet, do it this week; it is the
single best-value item in this document.

### Replit

Not a model vendor but a cloud IDE whose **Agent** uses the frontier models above to
build and deploy applications. **Core** at $18–20 a month includes about $20 of model
usage; **Pro** at $90–100 includes $100 and parallel agents. Replit is where "I had an
idea at lunch and it was live at dinner" happens. It is also where students most often
hand in something they cannot explain. Use it, and read what it wrote.

### Ollama — and the open-weight models

Ollama is a program you install. `ollama run llama3.1` downloads an open-weight model
and answers you from your own machine; nothing is sent anywhere. Local models are free,
for ever, with no session limit. (Ollama also sells a cloud tier, $20 a month for $60 of
hosted usage, for models too large to run at home.)

The models are the open-weight families:

| Family | Publisher | Sizes you will meet |
|---|---|---|
| Llama 3.x | Meta | 1B, 3B, 8B, 70B |
| Qwen 2.5 / 3 | Alibaba | 0.6B to 235B |
| Gemma 3 | Google | 270M to 27B |
| Mistral | Mistral AI | 7B and up |
| DeepSeek-R1 | DeepSeek | 1.5B (distilled) to 671B |
| Phi 3 / 4 | Microsoft | 3.8B, 14B |

The "B" is billions of parameters, and it is the number that decides whether a model
runs on your laptop at all. A model quantised to 4 bits needs roughly **0.6 GB of memory
per billion parameters**, plus room to work (Doc 2 §11 explains quantisation). The
course's one rule, the same in every document and every slide: **16 GB of RAM → a 7–8B
model; 8 GB → a 3B model; less → 1.5B.** In the table:

| Model size | Memory needed | Runs on |
|---|---|---|
| 1–3B | 1–3 GB | Anything; fast; noticeably limited |
| 7–8B | 5–6 GB | Any laptop with 16 GB RAM; the sweet spot for this course |
| 14B | 9–10 GB | A 16 GB machine, uncomfortably; 24 GB, well |
| 27–32B | 18–22 GB | 32 GB machines, or Apple Silicon with unified memory |
| 70B | 40+ GB | Not a laptop |

Speed follows memory bandwidth. Apple Silicon Macs are unusually good at this because
their GPU shares the system memory; a Windows laptop without a discrete GPU will run an
8B model at a few words per second, which is usable for a chatbot and painful for a
long generation.

An 8B local model is not a frontier model and will not become one. What it is: yours,
private, free, and honest about what a language model actually is when nobody has
wrapped it in a product. Week 3 is built on that.

## 4. What money buys

It is tempting to read the three price points — free, about $20, about $100 — as three
sizes of the same bucket. They are not. Tokens are the *last* thing a subscription buys.
The first things are capabilities, and they are the same seven at every vendor: Claude
Free / Pro / Max, ChatGPT Free / Plus / Pro, Gemini Free / AI Pro / Ultra, Copilot Free
/ Pro / Pro+.

| What changes | Free | About $20 a month | About $100 a month |
|---|---|---|---|
| **Which models** — the tier decides intelligence before anything else | The mid model; the frontier one rationed or absent | The frontier model, and the reasoning modes | The same models at higher effort, and the newest ones first |
| **A coding agent** — the difference between advice and work done in your files | A taste: limited Codex, Copilot's 2,000 completions | Claude Code, Codex, Copilot's agent | Several agents in parallel; 4× and more agent usage |
| **Memory of your project** — what you stop re-typing every conversation | Paste it again each time | Projects, memory, custom GPTs, connectors | The same, with the largest context (ChatGPT Pro: 400K) |
| **Where it can act** — the chat window is the smallest room it works in | The chat window | Your editor, your browser, Docs and Office | The same |
| **Output and context size** — how much it reads at once and how much it may say | Standard | Standard | Higher output limits, the largest windows |
| **When everyone is online** — capacity is finite and somebody goes last | Last in the queue | Normal | Priority at peak hours |
| **How much you can use** — the token axis, one of seven | One unit | Roughly five units | Five to twenty times the $20 tier |

Read the rows top to bottom, because that is their order of importance for this course.

**Which models.** On a free tier you are usually talking to the mid-size model, and the
frontier one is rationed. So a judgement of the form "this AI is not very good", made on
a free tier, is a judgement about the mid model. Say which model you used when you
report a result; it is half the result.

**A coding agent.** This is the row that matters most here. An agent is not a better
chat; it is a different kind of tool — it reads your files, edits them, runs your tests.
Every vendor puts it behind the first paid tier. The one exception is Copilot Student,
which is why §6 tells you to claim the pack before Week 2.

**Memory of your project.** Projects, memory and connectors are what stop you re-typing
your setup in every conversation. They are also, on Claude, the cached content that does
not count against your allowance — so this row and the last row are related.

**Where it can act.** The paid tiers move the model out of the chat window and into your
editor, your browser and your documents. That is a change of kind, not of degree: the
model can now see what you see instead of what you paste.

**Output and context size, and the queue.** These two only change at the top tier. They
matter to someone running long agent jobs on a deadline afternoon, when everyone else
is also online. They do not matter to a student in Week 2.

**How much you can use.** The token axis is the one everybody talks about, and it is
last on purpose. Multiply the free allowance by five and you have the $20 tier; by
another five to twenty and you have the $100 tier. It is real, and it is the smallest of
the seven differences in kind.

## 5. The limits, and why they are shaped the way they are

Every hosted assistant rations you, and the rationing has the same two-layer shape
everywhere, because everyone is solving the same problem: a few users who never stop
would otherwise consume the capacity meant for everyone.

**The session window.** Claude's is the clearest example: a **five-hour window** opens
with your first message and closes five hours later, whether you used it or not. Within
it you have a fixed allowance. Hit it, and you wait for the window to end. Gemini and
ChatGPT ration per-model over shorter rolling windows; the mechanism differs, the
experience is the same — a wall, then a countdown.

**The weekly cap.** On paid plans, a second allowance sits above the sessions and resets
every seven days. It exists to stop the pattern "use every session to the wall, all
week". If you are on a paid plan, this is the one that bites during a project deadline.

**What drains them.** Not messages — *tokens*, weighted by model. Concretely, from the
vendors' own guidance: long conversations (the whole history is re-sent every turn),
attachments and images, the larger models, tool use such as web search and code
execution, and long generations. A screenshot of an error costs more than the error;
the smartest model costs ten times the fastest; turn forty costs turns one to
thirty-nine again. Part II is entirely about this.

**What does not.** On Claude, content in a Project is cached and does not count when
reused — which is exactly why Part II tells you to put your standing facts in one.
Copilot's code completions never touch its credit allowance. Ollama has no meter at all.

One practical note: the Claude allowance is shared across the chat app and Claude Code.
Students who discover Claude Code in Week 4 tend to discover the session wall the same
afternoon. That is not a malfunction. It is the tool telling you that an agent reading
your whole project is expensive, and that you should tell it *which* files.

## 6. What this course expects you to have

You do not need to pay for anything.

- **Two chat assistants** on their free tiers — Week 1 asks you to use two and compare
  them, and it does not matter which two.
- **GitHub Copilot Student**, free through the Student Developer Pack. Claim it before
  Week 2.
- **Ollama** with one 7–8B model, installed before Week 3. If your laptop has 8 GB of
  RAM, install a 3B model and tell me; we will work around it.
- **A coding agent** from Week 4 or so. Copilot's agent is included in the student plan.
  Claude Code and Codex need a paid plan or API credits; use them if you have them, not
  because you think you must.

If you do pay for one thing, pay for the tool you will use most hours a week, not the
one with the best benchmark. For most students in this course that is a coding agent,
not a chat app.

## 7. How to read the next announcement

Everything in sections 3 to 5 will have changed by the time you read this in a later
term. What will not have changed:

- Vendors sell **tiers**, and the top tier costs about ten times the bottom.
- Limits are **token-weighted** and **two-layered** — a short window and a long one.
- Whatever you paste is re-sent every turn.
- Open-weight models trail the frontier by a year or so and are free for ever; the
  parameter count decides whether they run on your machine.
- The student offers are the best deal on the page and the first thing to check.

When a new model is announced, ask: which tier is it replacing, what does it cost
relative to the tier below, and what is the window. Those three numbers tell you how to
use it. The benchmark chart does not.

---

# Part II · The habits

## 8. Why your assistant runs out, and what it costs you

Every assistant you will use this term — Claude, ChatGPT, Gemini, Copilot — charges the
same currency: **tokens**. A token is roughly three quarters of a word, or a few
characters of code. Your usage limit is measured in tokens, not in messages, so "how
many questions can I ask today" has no fixed answer. Ten careless questions can cost
more than a hundred careful ones.

The part that surprises people is that a conversation has no memory of its own. The
model does not remember your earlier turns; the application **re-sends the entire
conversation** with every new message. Turn 40 of a long session pays for turns 1
through 39 all over again.

That single fact explains most of what follows.

---

## 9. The one habit that matters more than all the others

**Start a new conversation when you start a new task.**

A forty-turn thread about your Week 2 requirements, followed by "now help me with a CSS
bug", pays for all forty turns on every message about CSS — and the model is worse at
the CSS, because it is reading forty turns of irrelevant context looking for the point.

You are not being frugal at the model's expense here. Short, focused conversations get
better answers. Long ones drift: the assistant keeps referring back to decisions you
abandoned twenty turns ago.

A rough rule: when you catch yourself writing "forget what I said earlier about…",
that conversation is over. Open a new one and paste in the three facts that still
matter.

---

## 10. Feed it text, not pictures of text

A page of plain text costs a few hundred tokens. **The same page as a screenshot or a
scanned PDF costs one to two orders of magnitude more**, because an image is charged by
its area, not by how much it says. And the model has to read the letters out of the
pixels before it can think about them, so you pay more for a worse starting point.

In practice:

| Instead of | Do this |
|---|---|
| A screenshot of a red error in your terminal | Copy the error text and paste it |
| A screenshot of your code | Paste the code, or give the file |
| A scanned PDF of a paper | Find the text version, or paste the two paragraphs you care about |
| A photo of the whiteboard | Type the six lines that were on it |

Screenshots are the right tool for exactly one thing: when the **layout** is the
question. "Why is this button overlapping on a narrow screen" is a picture. "Why does
this traceback happen" is text, always.

---

## 11. Ask for the format you are actually going to use

Markdown is the cheapest thing an assistant can produce, because it is simply text. A
`.docx` or `.xlsx` is a zip archive of XML: the assistant cannot write one directly, so
it writes a *program* that builds one — and every later change means running that
program again, or reading the file back in to see what is inside it.

So: get the content right in markdown, and convert once, at the end, when nobody is
going to ask for another revision.

The same applies in reverse. Handing an assistant a `.docx` to read means it has to
unpack the thing before it can see a single sentence. If you wrote it, you probably have
the text somewhere cheaper.

This is not an argument against Word files. It is an argument against *iterating* in
Word files.

---

## 12. Point, don't paste

If your assistant can see your files — Claude Code, Copilot in an editor, anything with
a project folder — tell it **where** to look instead of pasting the contents. It reads
the twenty lines it needs rather than the two thousand you pasted.

When it cannot see your files, paste the smallest thing that contains the answer: the
function, not the module; the failing test, not the suite.

And when you want a change to a long file, ask for **the change**, not the file. "Show
me the diff for the `render` function" costs a fraction of "rewrite `app.py` with this
fixed" — and it is far easier to review, which is the part that actually protects you.

---

## 13. Batch your questions

Because the whole conversation is re-sent each turn, three follow-up messages cost
noticeably more than one message containing three questions. If you already know you
have four things to ask about the same code, ask all four at once.

The corollary: think before you send. A vague question produces a vague answer, and then
you pay again for the clarification. Week 1's assignment asks you to notice this by
asking the same question twice, once vaguely and once with the constraints spelled out.
The cost difference is as real as the quality difference.

---

## 14. Write down what you keep re-explaining

If you find yourself typing "this is a Streamlit app, Python 3.12, and I am using FAISS
for retrieval" at the start of every conversation, put it in a file the assistant reads
automatically — `CLAUDE.md`, a project instruction, a pinned note, depending on the
tool. You stop paying for it in every new thread, and you stop forgetting to mention it.

Your `ai_log_NN.md` is doing something related and worth more: it is the record of what
went wrong and how you caught it. That one is for you and for Week 12, not for the
model.

---

## 15. What does not help

- **"Be brief."** Worth adding when you want a short answer, but the output is the small
  half of the bill. Your conversation history is the large half.
- **Compressing your wording.** Dropping "please" saves a token. Starting a fresh
  conversation saves thousands.
- **Avoiding the assistant to save quota.** The point of this course is to use these
  tools well. Being economical means not paying for waste — forty irrelevant turns, a
  screenshot of text, a file pasted whole — not asking fewer real questions.

---

## 16. The short version

1. New task, new conversation.
2. Text, never a picture of text.
3. Markdown while you iterate; convert at the end.
4. Point at files; ask for diffs, not rewrites.
5. Ask your four questions in one message.
6. Put the standing facts in a file.
