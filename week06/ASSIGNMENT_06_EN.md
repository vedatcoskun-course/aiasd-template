# Week 6 Assignment — Your Own Feature, End to End

**Due:** the lecture part pushed by 11:45 · the rest Saturday 23:59 · Commit to your project repository

## Your project so far, and where it is going

Five weeks ago, your project was only an idea. Look at it now:

- **Week 1:** your tools, and your first real conversations with two AI assistants.
- **Week 2:** a real problem, real people who have it, and the first list of what your product must do.
- **Week 3:** you presented it to your group and looked at the market. The project became final.
- **Week 4:** it became screens, and a classmate clicked through them with your test cases.
- **Week 5:** it became software: its parts, the API contract, a server that answers every endpoint
  (most of them with 501), and red tests that wait for this week.

This week, your product does its own work for the first time. This is not about the login. The login
is the same in every project, so the course gives it to you ready to use. You connect it to your server
in about twenty minutes. The week is for what **only your project does**: your own functional `must`
requirements. You wrote them in Week 2 and drew them in Week 4. In Week 5, your API contract got the
login rows. This week it gets their rows too, if they are missing (§2). By Saturday, each of them:

- works on your server;
- has tests that pass on GitHub;
- has a page in your web client where a logged-in user can do it.

In Week 7, the same feature runs on a phone. In Week 8, your product gets its chatbot and works on all
three clients. Its first build goes to the store's test track. Then come real testers (Week 9), real
users (Week 10) and the store's review. In December, you install your own app from a store.

## One requirement, from start to finish

Each of your functional `must` requirements has eight links, like a chain. You already have the first
four. You have link 5 (the `api.md` rows) for the login. For your own feature, you write it now if it
is missing (§2). Then you add the last three links, and the chain is complete.

| Link | Where it lives | Since |
|---|---|---|
| 1. The requirement, with its acceptance criterion | `week02/requirements.json` | Week 2 |
| 2. Its use case | `week02/SRS.md` | Week 2 |
| 3. Its screen | `week04/prototype/`, with `<!-- serves: REQ-… -->` | Week 4 |
| 4. Its test cases, each with `"run"` | `week04/test_cases.json` | Week 4 |
| 5. Its rows of the API contract | `week05/api.md` | Week 5 (login) · now (your feature) |
| 6. Its routes, working: no longer 501 | `server/` | **this week** |
| 7. Its tests, named by test case id, **green in GitHub Actions** | `server/tests/` | **this week** |
| 8. Its page of the web client, calling the server with `fetch` | `web/`, with `<!-- serves: REQ-… -->` | **this week** |

**`requirements.json` is the source. Every other link follows it.**

It is also the only place for the requirements. Do not copy them into `SRS.md`. In SRS §4 and §5, one line is
enough: "The requirements are in `week02/requirements.json`." The SRS keeps your use cases (§3).

- The route does what the requirement and its acceptance criterion say. It does not do what is easiest
  to build, or what an assistant suggests.
- The test checks what the test case expects.
- The page is the prototype's screen, now real.

Sometimes, while you build, you find that a link is wrong. For example, a test case expects something
that the requirement does not say, or the page needs a list that `api.md` does not have. Then change that
link first, with its line in `PROPOSAL.md` (§9). After that, change the code. Never change the
requirement only to make it fit the code.

A small example from StudyRoom, the course's sample project:

| Link | StudyRoom |
|---|---|
| Requirement | REQ-002 — A student books a free study room for 30 to 120 minutes; a busy slot is refused. |
| Use case | UC2 — Book a room: choose a room, a start time and a length; the app confirms or says the slot is busy. |
| Screen | `book.html` — `<!-- serves: REQ-002 -->` |
| Test cases | TC-002-01 (a free slot is booked, `run: web`), TC-002-02 (a busy slot is refused, `run: server`) |
| API rows | `POST /bookings` → 201 · 409 slot busy · 422 length outside 30–120 · 401 not logged in |
| Route | `server/bookings.py`: `create_booking`, with `current_user` |
| Test | `test_TC_002_02_a_busy_slot_is_refused`, green in the Actions tab |
| Page | `web/book.html` — `<!-- serves: REQ-002 -->`, `fetch("/bookings", …)` |

### What you need to know this week

| | What it is |
|---|---|
| **`server/course_login.py`** | The course's login. It is one file, the same for everyone. It answers on your three login paths. You read it, but you never change it. |
| **`server/login_contract.json`** | A few lines that you write. They tell the course's login and the course tests your three login paths and the names of your fields. |
| **Token, Bearer header** | After the right code the server gives a **token**, a long random string. The client sends it with every request in the header `Authorization: Bearer <token>`. |
| **`current_user`** | It comes from `course_login`. Put `user: str = Depends(current_user)` in a route. Then the route runs only for a logged-in user, and `user` is their e-mail address. Without a token, the answer is 401. |
| **401, 403, 404, 409, 422** | 401: not logged in. 403: logged in, but not allowed (someone else's data, an instructor's action). 404: no such thing. 409: it conflicts with data that is already there. 422: a field is missing, empty or has the wrong form. |
| **`AIASD_CODE_FILE`** | An environment variable. When it is set, the login writes the code into that file and does not send an e-mail. You use it in the lecture and in tests. |
| **`TestClient`** | Talks to your app in a test without a network, as in Week 5. |
| **`fetch`** | The JavaScript function a web page uses to send a request to the server and read the answer. |
| **`StaticFiles`** | The part of FastAPI that serves the pages of `web/`. Then the pages and the server have the same address. |
| **`sessionStorage`** | Where a web page keeps the token while the tab is open. |
| **`.env`, `.gitignore`, SMTP** | `.env` holds your e-mail settings and password. It stays on your computer only. `.gitignore` keeps it out of git. SMTP is the way a program sends e-mail. |
| **CI, GitHub Actions** | The checks that run on GitHub after every push. From this week, they also run the tests. Your lecture mark uses their result. |
| **The course tests** | `course_tests/`: ten tests of the login, the same for everyone. They check that you connected the login correctly. |

## When is what due

| When | What you do | Where |
|---|---|---|
| **Before the lecture** | Run the checker once; `pip install -r week06/requirements.txt`; `python -m pytest course_tests -q` (ten stop with an error: "Fill in server/login_contract.json"). Make the list of your functional `must` requirements, and choose the one you build first | the box below |
| **In the lecture, until about 10:00** | The login connected: `login_contract.json` by hand, `course_login.router` in `main.py`, your own login stubs deleted. Your first requirement chosen, and its `api.md` rows checked (or written, §2) | §1–§2 |
| **In the lecture, until about 11:00** | Its routes working, with `current_user` where it needs a user; its tests named by its test cases, **green on GitHub** | §3–§4 |
| **In the lecture, until 11:45** | Its prototype screen as a page of `web/` that calls those routes, behind the login · the attacker round, typed into `group_06.json` | §5–§7 |
| **By Saturday 23:59** | **Every** functional `must` requirement end to end · the code by real e-mail · all tests green on GitHub · S2 · `"run"` on every test case · your decision on each finding · `ai_log_06.md` | §8–§16 |

> ## Commit in the middle of the work, not at the end
>
> The times above are a pace, not push times. Commit each piece of work while it is still
> unfinished, for example a route that answers but does not check the user yet, a test that is
> written but still red, or a page that shows the screen but does not call the server yet. Commit it
> again when it works, and push every commit right away. Your history shows how each file grew; a
> piece that arrives finished in one commit does not count for the commit point.

> ## The AI log is written by a human. No exceptions.
>
> You write `week06/ai_log_06.md` yourself, in your own words. Outside the Evidence block and the
> bold quotes of the assistant's answer (§15), you use no assistant: not to write it, not to "improve"
> it, not even for the English. **A log written by an assistant earns 0.** Your English is not graded.
> A person reads every log.

> ## Two files you write by hand
>
> **`server/login_contract.json`**: your three login endpoints and your field names, copied by
> you from your `api.md`. **`week06/group_06.json`**: what your groupmate tried and what your server
> did. You type it while it happens. Later you add your decisions. No assistant writes, corrects or
> completes either file.

> ## The login comes ready to use, and it works the same way in every project
>
> - The user gives an e-mail address and gets a **4-digit code**, valid for **10 minutes**,
>   that works **once**.
> - The same address asking for a new code **within a minute** gets **429**.
> - A wrong or expired code gets **401**. Something that is not an e-mail address gets **422**.
> - After **3 wrong codes in a row** (a new code does not reset the count), every login for that
>   address gets **429 for 15 minutes**, even with the right code.
> - The right code gives a **token**. Your "me" endpoint, with `Authorization: Bearer <token>`,
>   answers **200** with the address; without a token, or with a wrong one, **401**.
>
> `server/course_login.py` does all of this. You do not write a login this week. You connect the
> course's login (§1), and the ten course tests check that you did it. If your REQ-001 or its test
> cases say something else (for example, a 6-digit code), change them with a change request (§9).

> ## Your lecture mark comes from GitHub, not from your laptop
>
> When you push, GitHub Actions runs the checker. The checker runs the course tests and your own
> tests. For your lecture mark, I take the result of this run for your last commit pushed by the
> end of the lecture. Push by 11:45. Then open the **Actions** tab and watch the run finish. A test that passes
> only on your laptop does not count.

> ## Never force push. A small fix never costs you anything.
>
> `git push --force` deletes commits from your history. I read this history to grade your work. If CI
> turns red because of a ruff error or a typo, fix it and push the fix as a **new** commit. A small fix
> commit never lowers the commit point.

> **Your group meets again, for one thing:** the attacker round of §6. The rest of the week
> you work alone, on your own project, on your own computer.

> **Before the lecture:** run `python .github/check_deliverables.py` once. It brings `week06/`,
> the folder `course_tests/`, the file `server/course_login.py` and, if you do not have it
> yet, `server/login_contract.json`. Then, with your virtual environment active:
>
> ```bash
> pip install -r week06/requirements.txt
> python -m pytest course_tests -q
> ```
>
> All ten tests stop with an error ("Fill in server/login_contract.json"). This is the starting point.
> Then open `week02/requirements.json`. Write down every requirement with `"functional": true` and
> `"priority": "must"`, except REQ-001 (the login). This list is your work for the week. Choose the
> one you build first: the main reason why your product exists. If `week05/api.md` has no rows yet
> for this requirement, see §2.

---

## What arrives with this week

- `week06/`: this assignment, the lecture, `group_06.json` (the attacker's record), `ai_log_06.md`
  and `requirements.txt` (last week's packages plus `freezegun`, `python-dotenv` and `ruff`).
- `server/course_login.py`: the course's login. It belongs to the course, like `course_tests/`. If you
  change it, the checker puts the original back. On GitHub, the course's own copy runs. Read it: its
  first lines say how to connect it.
- `course_tests/` at the root: the course's ten login tests. They belong to the course too.
- `server/login_contract.json`, if you do not have it yet: values in [brackets] for you to fill in.

---

## Where an assistant helps this week, and where it does not

| Part | Assistant |
|---|---|
| The code of one route, with its requirement, its acceptance criterion and its `api.md` row in the prompt (one route, one commit) | **Helps** |
| A test from one of your test cases (you check it against the test case, line by line) | **Helps**, the approval is yours |
| The JavaScript of a page, with `fetch` | **Helps** |
| Reading a red test or a GitHub Actions log | **Helps** |
| Choosing what a route does when the requirement does not say | **No help**: the requirement decides. If the requirement says nothing, change the requirement first (§9) |
| `server/login_contract.json` | **No help**: you copy it from your `api.md` by hand |
| `week06/group_06.json`: what the attacker tried, what happened, and your decision | **No help** |
| Running the tests, and reading what GitHub says | **No help**: you run them and you look |
| The Change log lines and the change requests | **No help** |
| `ai_log_06.md`, outside the Evidence block and its bold quotes | **No help** |

---

## In the lecture — pushed by 11:45

The lecture has four parts:

1. about twenty minutes of explanation;
2. the login and your first requirement (until about **10:00**);
3. its routes and its tests (until about **11:00**);
4. its page and the attacker round (until **11:45**).

In every part, commit and push while the work is still unfinished, and again when it works.

### 1. Connect the login — fifteen to twenty minutes

**When:** in the lecture, until about 10:00.

**Why the login comes ready to use.** Every project logs in the same way. It is also easy to make
small mistakes in a login (a code that never expires, a "me" that answers everyone). Writing it would
take your whole week, and you would learn little that your own feature does not teach you. So the course
gives you a login, checked by ten tests. You spend your week on the part that only you can build.

**Course files.** From Week 6 the checker also brings `course_tests/` and `server/course_login.py`, and
`server/login_contract.json` if you do not have it. Do not edit `course_tests/` or `course_login.py`: the
checker puts the course's copy back, and GitHub always uses it.

**Step 1 — `server/login_contract.json`, by hand.** Open your `week05/api.md`. Copy your three login endpoints exactly as they are in the table: the
method, one space, and the path. Then write the names of your fields:

```json
{
  "request_code": "POST /auth/code",
  "login": "POST /auth/login",
  "me": "GET /auth/me",
  "email_field": "email",
  "code_field": "code",
  "token_field": "token",
  "test_email_domain": "example.com",
  "email_must_end_with": "",
  "app_name": "StudyRoom"
}
```

- The login answers `{"token": "..."}` under your `token_field`, and "me" answers `{"email": "..."}`
  under your `email_field`. If your `api.md` says something else, change the row and write its Change log line.
- If your `api.md` has no "me" endpoint (the one that answers with the logged-in user), add its row now.
- `email_must_end_with`: fill it in only if your REQ-001 accepts only some addresses, such as `".edu.tr"`,
  or a list of endings. Then `test_email_domain` must be a domain that it accepts, such as
  `"student.example.edu.tr"`.
- `app_name` is the name that the e-mail with the code shows.

**Step 2 — `server/main.py`.** Two lines:

```python
from server import course_login

app.include_router(course_login.router)
```

**Step 3 — delete your own login stubs.** Delete the three routes from Week 5 that answer 501 on those
paths. If they stay, they answer before the course's login can.

**Step 4 — run it.**

```bash
python -m pytest course_tests -q                                          # ten pass
AIASD_CODE_FILE=login_code.txt uvicorn server.main:app --reload          # macOS, Linux
$env:AIASD_CODE_FILE="login_code.txt"; uvicorn server.main:app --reload  # Windows PowerShell
```

At `/docs`:

1. ask for a code with the body `{"email": "you@example.com"}` (use your field names from
   `login_contract.json`);
2. read it in `login_code.txt`;
3. log in with `{"email": "you@example.com", "code": "1234"}` (the 4 digits from the file), and copy
   the token;
4. press **Authorize** and paste the token;
5. call "me".

Add `login_code.txt` to `.gitignore`. After you change `login_contract.json`, restart the server: it
reads the file only when it starts.

> **Your Week 5 login tests.** With the course's login, a test must not send a real e-mail. Without
> `AIASD_CODE_FILE`, the login sends an e-mail with the settings in `.env`, or answers 503 when there
> are none (always on GitHub). So change each test like this:
>
> ```python
> from fastapi.testclient import TestClient
>
> from server.course_login import reset_for_tests
> from server.main import app
>
> client = TestClient(app)
>
>
> def test_TC_001_01_a_code_is_sent(monkeypatch, tmp_path):
>     reset_for_tests()
>     monkeypatch.setenv("AIASD_CODE_FILE", str(tmp_path / "code.txt"))
>     response = client.post("/auth/code", json={"email": "deniz@example.com"})
>     assert response.status_code == 200
>     assert (tmp_path / "code.txt").read_text().isdigit()
> ```
>
> - Use your own paths, and the field names of your `login_contract.json`.
> - Use an address that passes `email_must_end_with`.
> - To log in, read the code from the file.
> - Use a new address in each test, or call `reset_for_tests()` first.
> - The answers are the course's: `{"sent": true}`, 401, 429. A test checks only the status code
>   (200, 401, 429), not the text of the message.
> - A test that checks a rule the course's login does not have: change its test case first (§9).
>   Then change the test.
> - The course tests already cover the login. So a TC-001 test case may also be `"run": "manual"`, if
>   you do not keep a server test for it. But every `must` test case with `"run": "server"` needs a
>   passing test on Saturday.

### 2. Your first requirement — choose it, and check its chain

**When:** in the lecture, until about 10:00.

Take the requirement that you chose before the lecture. Before you write any code, put its links side
by side: the requirement and its acceptance criterion, its use case, its screen, its test cases and its
`api.md` rows. Check:

- Do they say the same thing?
- Does every test case have the `api.md` rows it needs?
- Does the screen show what the acceptance criterion promises?

If `api.md` has no rows yet for this requirement (Week 5 asked only for the login rows), write them now,
by hand, before any route code, with a dated Change log line.

If a link is missing or wrong, fix it now, with its line in `PROPOSAL.md` (§9).

### 3. Its routes, for real

**When:** in the lecture, until about 11:00.

In each of its routes, replace the 501 with the real work. This week, keep your data in memory: a
dictionary or a list in one module of `server/` is enough. From Week 8, when testers use your app, your
data must survive a restart of the server: keep it in a file or in a database of your choice (SQLite
comes with Python). A route that needs
a user asks for one with `current_user`:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from server.course_login import current_user

router = APIRouter()
bookings: list[dict] = []  # in memory for now; from Week 8 in a file or a database


class NewBooking(BaseModel):
    room: int
    start: str
    minutes: int


@router.post("/bookings", status_code=201)
def create_booking(body: NewBooking, user: str = Depends(current_user)) -> dict:
    """REQ-002: a student books a free room for 30 to 120 minutes; a busy slot is refused."""
    if not 30 <= body.minutes <= 120:
        raise HTTPException(status_code=422, detail="A booking lasts 30 to 120 minutes.")
    if any(b["room"] == body.room and b["start"] == body.start for b in bookings):
        raise HTTPException(status_code=409, detail="This slot is already booked.")
    booking = {
        "id": len(bookings) + 1,
        "room": body.room,
        "start": body.start,
        "minutes": body.minutes,
        "by": user,
    }
    bookings.append(booking)
    return {"booking_id": booking["id"]}
```

This example is `server/bookings.py`. Its routes answer only when `server/main.py` includes its router.
Add two lines there (the import at the top of the file, with the other imports):

```python
from server import bookings

app.include_router(bookings.router)
```

`ruff check . --fix` then joins your two imports from `server` into one line:
`from server import bookings, course_login`.

- **Every error of the `api.md` row, with its status code,** and with a message that the user
  understands. The route sends the message that your test case expects ("This slot is already booked.").
- **Who may do it.** `current_user` says who is asking. A user must not read or change another user's
  data. A student must not do what only an instructor or an owner may do. In both cases the answer is
  **403**. The server decides this; hiding a button on the page is not enough.
- **Text that is empty, or only spaces,** is empty: `.strip()` it before you check it.
- Maybe the page needs something that has no row in your `api.md` (for example, a list to show). Then
  add the row first, with its Change log line. After that, add the route.

Ask your assistant for one route at a time. Put the requirement, its acceptance criterion and the
`api.md` row in the prompt. Then read the whole answer. Assistants like to "help": they add a field that
nobody asked for, leave out a check "for simplicity", or turn an error into 200. Each of these breaks one
of your test cases.

### 4. Its tests, named by its test cases — green on GitHub

**When:** in the lecture, until about 11:00.

First add `"run"` to this requirement's test cases (§14). Then write one test in `server/tests/` for
each of them with `"run": "server"`. Name the test by the test case id:
`test_TC_002_02_a_busy_slot_is_refused`. Each `assert` is one expected result of the test case. The course's login helper logs a test user in through your real login (see
"Your own tests" below). Run `python -m pytest server/tests -q`, push, and watch the run in the
**Actions** tab. The line `AIASD-TEST … TC-002-02 passed` is what I read for the lecture mark.

### 5. Its page — the prototype's screen, made real

**When:** in the lecture, until 11:45.

Copy the requirement's screen from `week04/prototype/` into `web/`. Keep its look: it is your design.
Keep its `<!-- serves: REQ-… -->` line too. Then make it real:

- replace the fixed data of the prototype with the server's answers;
- send what the user does to the server with `fetch`, with the token.

```javascript
async function api(method, path, body) {
  const options = { method, headers: { Authorization: `Bearer ${sessionStorage.getItem("token")}` } };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }
  const response = await fetch(path, options);
  if (response.status === 401) location.href = "login.html";   // behind the login
  return { status: response.status, data: await response.json().catch(() => ({})) };
}

document.querySelector("#book").addEventListener("click", async () => {
  const { status, data } = await api("POST", "/bookings", { room: 3, start: "14:00", minutes: 60 });
  document.querySelector("#message").textContent = status === 201 ? "Booked." : data.detail;
});
```

- **`await` only inside an `async` function:** call `api()` in an `async` click handler, as above (or
  make the script `type="module"`).
- **Behind the login:** the page needs a token. The prototype's `index.html` and `code.html` become
  `web/login.html` (one page with both steps, or two pages that start at `login.html`). It keeps
  `<!-- serves: REQ-001, REQ-006 -->`. It calls your request_code and login paths with `fetch`
  directly, not with `api()`: `api()` sends a 401 back to `login.html`, so a wrong code would only
  reload the page. Show the 401 message instead ("Wrong code"). Then keep the token in
  `sessionStorage` and open your first page. Without a token, every page goes to the login.
- Copy `style.css` from `week04/prototype/` into `web/` too.
- **Show the server's refusals** in the words of your test cases ("This slot is already booked.").
- **What the prototype only pretended is now real:** the role comes from the login, not from a switch
  on the page. A code or an id comes from the server, not from the HTML. If the steps of a test case
  still name something that only the prototype had, change the test case (§9).
- Put the server's text on the page with `textContent`, never with `innerHTML`.

Your server serves the pages itself. Then the pages and the server have the same address:

```python
from pathlib import Path

from fastapi.staticfiles import StaticFiles

WEB = Path(__file__).resolve().parent.parent / "web"
if WEB.is_dir():
    app.mount("/web", StaticFiles(directory=WEB, html=True), name="web")
```

Open http://127.0.0.1:8000/web/login.html. Make the window 390 pixels wide, log in and use your
feature. A mounted folder is not an endpoint, so it needs no row in `api.md`. A route such as
`@app.get("/")` does need a row. With `--reload`, every save of a `.py` file restarts the server, and
the server forgets the tokens: log in again.

### 6. The attacker round — `week06/group_06.json`

**When:** in the lecture, about 11:25 to 11:45.

Your group from Week 3 meets again, with one job: **break each other's feature**. Work in pairs. The
owner's server runs on the owner's laptop. The attacker logs in there with their own address and tries
what the owner did not plan for:

- someone else's data with their own token (change the id in the address);
- an action that only an instructor or an owner may do, as an ordinary user;
- an empty text, or only spaces;
- a very long text, or a number out of range;
- the same thing twice;
- the login too (wrong codes, no token).

The owner watches and types, **by hand**, one entry for each attacker in `week06/group_06.json`:

- `student_id`: the attacker's 9-digit number; `role`: `"attacker"`;
- `tried`: what they tried, in one or two sentences, with the values;
- `happened`: what your server or your page did: the status code, the message, whether it worked.

Then change roles. If nobody from your group is in the lecture, work with any classmate. You write
everything in this file yourself, in your own words: no assistant, not even for the grammar. `accepted`
and `why` wait until Saturday (§13).

### 7. Push, and see it on GitHub

Run `ruff check . --fix` and `ruff format .` before you push (outside the venv, install it with
`pip install ruff==0.15.11`). The job **Lint and format** runs ruff on GitHub after every push.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week06: REQ-002 bookings, route and test"
git push
```

Then open your repository on GitHub. Open the **Actions** tab, the newest run and the job **Weekly
deliverables**. If it is red there, it is red for the lecture mark, even if your laptop shows green.

Commit each piece of work in the middle, commit it again when it works, and push every commit right
away. GitHub's push time counts, not the time on a commit. Push your last commit by 11:45, so that the
run has time to finish. The lecture mark reads your last commit pushed by the end of the lecture, and its Actions run.

---

## By Saturday 23:59

This part takes about 4 to 5 hours of work. Spread it over the days after the lecture.

### 8. Every functional must requirement, end to end

In the lecture you did this for one requirement. Now do it for **all** of your functional `must`
requirements. REQ-001 is one of them: its server part is the course's login, and its page is
`web/login.html` (§5). That page keeps `<!-- serves: REQ-001, REQ-006 -->` and calls the server with
`fetch`. For all of them:

- every `api.md` row that serves one of them answers for real, no longer with 501;
- every test case of a `must` requirement with `"run": "server"` has a test, named by its id, that
  passes on GitHub;
- every one of these requirements has a page in `web/` that names it in `<!-- serves: … -->` and calls
  the server with `fetch`.

One page may serve several requirements, as one screen of the prototype did. Requirements that are
`should` or `could` may still answer 501.

Some parts only a phone can do, such as a push notification or the camera. They come in Week 7. Build
the server's side now. On the page, write in an HTML comment what the phone will add.

### 9. When a link of the chain must change

When you build, you find out if the earlier links were right. Your requirements and test cases became
your **baseline** last Saturday. So:

- A change to `requirements.json` or `test_cases.json` is a **change request**. It is a Change log line
  in `PROPOSAL.md`. It begins with `CR-` and the next free number, names the change and the ids, and
  lists every file that the change affects.
- Test cases written for the prototype often name things that only the prototype had: "tap Instructor
  in the view strip", "room 3 is always free". The page is real now, so change their steps. One change
  request for all of them is enough: *"2026-10-27 — CR-01: TC-002-01 to TC-003-02: the steps no longer use the
  prototype's view switch and its fixed list of rooms; the role comes from the login and the rooms from
  the server; affects week04/test_cases.json."*
- A change to `api.md`, the use cases or the screens gets an ordinary dated Change log line.
- The course asks for `"run"` on every test case (§14). Adding it is **not** a change request.

### 10. The code by real e-mail

Without `AIASD_CODE_FILE`, the course's login sends the code by e-mail. It uses the settings in `.env`.
This file is at the root of your repository, on your computer only:

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=the 16-letter app password
SMTP_FROM=you@gmail.com
```

- For Gmail, the password is an **app password** (Google account → Security → 2-step verification on →
  App passwords), never your real password.
- `.gitignore` lists `.env`. **`.env` is never committed.** If you ever commit it, change the app password at
  once. Deleting the file is not enough, because it stays in the history.
- `.env.example` lists the same five names, **with nothing after `SMTP_PASSWORD=`**.
- Windows PowerShell: `$env:AIASD_CODE_FILE` stays set in that window. Close the window, or run
  `Remove-Item Env:AIASD_CODE_FILE`, before you test the real e-mail.
- Log in on your web page with your own address. When the e-mail arrives, take a screenshot of it in
  your mailbox. The sender and the code must show. Save it as **`week06/email_code.png`** (or `.jpg`).

Some networks block port 587. If the e-mail does not go out from the campus, try from home.

### 11. Every test green on GitHub

These tests must be green:

- all ten course tests (LOGIN_07, a code works only once, and LOGIN_08 to LOGIN_10, the rules about
  time, are read on Saturday);
- your Week 5 login tests, changed as in §1 (if you keep them);
- the tests of every `must` test case with `"run": "server"`.

### 12. S2 — your app's record in the store, `week04/store.json`

Create your app's record in your store's developer console. It has a name and a **package name**
(Google Play, Huawei, Samsung) or a **bundle id** (Apple). This is the unique name of your app in the
store, such as `com.example.studyroom`. Choose it with care: you can never change it. Google Play
does not ask for the package name yet: the first upload (S3, Week 8) fixes it. Choose it now anyway,
write it in S2, and use it as the `applicationId` in Week 7. Add S2 to `week04/store.json`, next to S1:

```json
"S2": { "date": "2026-10-31", "app_name": "StudyRoom", "package": "com.example.studyroom", "evidence": "store_s2.png" }
```

`evidence` names a screenshot of the record in your console, saved in `week04/`. Cover your address,
your ID number and your card details. Maybe the store has not accepted your developer account yet. Then
write in your AI log the date you applied and what the store says. The S2 check stays red until the
record exists.

### 13. The attacker's findings: your decision

For each entry of `group_06.json`, add:

- `accepted`: `true` if you change something because of it, `false` if not;
- `why`: one full sentence: what you changed, or why it was not a real problem.

When you fix a finding, add a test that would have caught it. Name it by the id of the test case it
belongs to. If no test case covers it, you need a change request (§9).

### 14. How each test case is run — `week04/test_cases.json`

Add `"run"` to every test case:

- `"server"` if a test in `server/tests/` runs it;
- `"web"` if it is run in the browser on your page;
- `"manual"` if a person runs it (on a phone, in the store, with a user).

### 15. The hostile reviewer — `week06/ai_log_06.md`

Your groupmate attacked your feature in the lecture. Now let an assistant do the same (`AI_Doc5` §3).
Give it the routes of your own feature and the requirements they serve. Ask for **the three strongest
attacks**, numbered. Try each attack yourself, against your running server or in a test. Then write in
the log:

- the three attacks (the assistant's words in bold);
- what your server did against each one;
- **the one you fixed**, and how;
- **the one that is wrong**, with the evidence (a status code, a test result).

Paste `ME:`, `AI:` and `TERMINAL:` (commands and their output, untouched) into the Evidence block.

Then compare the assistant's attacks with your groupmate's. Where do they agree? Which of the two found
something that the other missed?

**The AI log is written by a human: you.** Outside the Evidence block and the bold quotes no assistant is
used. **A log written by an assistant earns 0.**

### 16. Push again, checks green

Make several commits as you work. Each has some new work in it and a message that says what changed.
**Outside the lecture:** at least two commits with new work, pushed at least one hour apart. GitHub's
push time counts, not the date on a commit. A commit made by a coding agent never counts. **Never force
push**, and never let an assistant do it. Then go through the checklist below.

---

## Your own tests

```python
import uuid

from fastapi.testclient import TestClient

from server.course_login import auth_header_for_tests
from server.main import app

client = TestClient(app)


def someone(name: str) -> dict[str, str]:
    """A new user, logged in through the real login: the header with their token."""
    return auth_header_for_tests(client, f"{name}-{uuid.uuid4().hex[:8]}@example.com")


def test_TC_002_02_a_busy_slot_is_refused():
    deniz, mia = someone("deniz"), someone("mia")
    client.post("/bookings", json={"room": 3, "start": "14:00", "minutes": 60}, headers=deniz)

    response = client.post(
        "/bookings", json={"room": 3, "start": "14:00", "minutes": 60}, headers=mia
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "This slot is already booked."
```

- **`auth_header_for_tests`** asks for a code with `AIASD_CODE_FILE` set, so no e-mail is sent in a
  test. It logs the address in and gives you the header with the token. Use the domain of your
  `test_email_domain`.
- **A new address in each test**, as above: an address may ask for a new code only once a minute.
- **Two users** when the test case is about who may do what: one who owns the data, one who does not.
- **Only if one of your tests moves the clock** with freezegun: put these lines before
  `TestClient(app)`. TestClient runs each endpoint in a separate thread. Without these lines, freezegun
  does not change the clock in that thread:

  ```python
  import freezegun

  freezegun.configure(
      default_ignore_list=[
          m for m in freezegun.config.DEFAULT_IGNORE_LIST if m not in ("threading", "queue")
      ]
  )
  ```

---

## Deliverables checklist

**In the lecture, pushed by 11:45**
- [ ] `server/login_contract.json` — by hand; its three endpoints are rows of `api.md`; `course_login.router` in `main.py`; course tests LOGIN_01–06 green **on GitHub**
- [ ] One functional `must` requirement of your own: a route of it working, no longer 501
- [ ] A test named by one of its test cases, green **on GitHub**
- [ ] A page in `web/`, made from its prototype screen, that calls its routes with `fetch`, behind the login; served by your server
- [ ] `week06/group_06.json` — one entry for each attacker: number, role `attacker`, what they tried, what happened; typed by you

**By Saturday 23:59**
- [ ] Every `api.md` row of a functional `must` requirement answers for real (no 501)
- [ ] Every `must` test case with `"run": "server"` has a test named by its id, green on GitHub; all ten course tests green
- [ ] Every functional `must` requirement has a page in `web/` with `<!-- serves: … -->` and `fetch` (REQ-001: `login.html`)
- [ ] Every changed link has its line in `PROPOSAL.md` (a change request for requirements and test cases)
- [ ] The code by real e-mail; `.env` not committed and listed in `.gitignore`; `.env.example` with the five SMTP names and no password; `week06/email_code.png`
- [ ] `week04/store.json` — S2 with date, app name, package or bundle id, and its screenshot in `week04/`
- [ ] `week04/test_cases.json` — `"run"` on every test case
- [ ] `week06/group_06.json` — `accepted` and `why` for every finding
- [ ] `week06/ai_log_06.md` — the three attacks on your feature, what happened, the one you fixed, the one that is wrong; `ME:`, `AI:` and `TERMINAL:` (commands and their output, untouched) pasted into the Evidence block; written by you (an assistant's log earns 0)
- [ ] Checks green on GitHub; Weeks 1–5 still pass

---

## Not this week

No mobile client (Week 7). No database yet: your data, and the login's codes and tokens, live in memory.
They are lost when the server restarts. That is fine for now; from Week 8 your own data must survive a
restart (the login's codes and tokens may not: users simply log in again). No password, ever. No chatbot (Week 8). No
S3: you do not upload a build yet. `should` and `could` requirements may wait.

---

## How this week is graded

**End of the lecture — 5 points.** I read your last commit pushed by the end of the lecture and its GitHub Actions
run:

- the login connected (the contract, its rows in `api.md`, `course_login.router`, LOGIN_01–06);
- a working route of your own `must` requirement;
- a test of one of its test cases, passing on GitHub;
- its page in `web/`, served by your server;
- the attacker's record.

**Saturday 23:59 — 5 points.**

- Checks green on your final state: **2**.
- Human involvement: **2**. This means your `ai_log_06.md`, written by you (a log written by an
  assistant earns **0**), and the two files you write by hand: `login_contract.json`, and the
  attacker's record with your decisions.
- Commit discipline: **1**. In the lecture: each piece of work (the login, its routes, its tests, its
  page) in at least two pushed commits, the first while the piece is still unfinished. Outside the lecture: at least two commits with new work, pushed at least one
  hour apart. GitHub's push time counts, not the date on a commit. A commit made by a coding agent never
  counts.

**Contributors' bonus.** Each attacker you name earns the contributors' bonus (10% of your week's
mark), and you earn the same for your attacks.

**S2** is a graded step of the store bonus.

**One student, one computer, one GitHub account.** Commit from your own computer, under your own
account. Work done on a classmate's computer, or while logged in as a classmate, earns nothing for the
lecture. In the attacker round, the attacker uses your laptop only to attack. Nobody commits on a
classmate's laptop. If one day you really must commit from another computer, write it in that week's AI
log, with the day and the reason.
