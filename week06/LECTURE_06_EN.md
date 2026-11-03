# AIASD · Week 6 — Your Own Feature, End to End

*Atlas University · Fall 2026–27 · Prof. Dr. Vedat Coşkun*
*Presented from this page. Scroll one section at a time; each `---` is a slide.*

<!-- Instructor: zoom the browser to 150 % and collapse the GitHub header. Total ≈ 2 h 45 min:
20 min explanation + a short demonstration (wire the course login into a fresh server in three minutes,
/docs, the Actions tab) · the login wired and the first requirement chosen until about 10:00 · its
routes and tests until about 11:00 · commits and pushes in the middle of each piece · its page until about 11:25 · the attacker round 11:25–11:45 ·
the last push at 11:45 · the mark reads the last commit pushed by the end of the lecture. -->

---

## Today

1. Your project so far, and the chain every requirement of yours becomes
2. The login comes ready to use: connect it — until about **10:00**
3. Your first own requirement: its routes and its tests, green on GitHub — until about **11:00**
4. Its page: the prototype's screen, now real, behind the login
5. The attacker round: a groupmate tries to break your feature — until **11:45**
6. By Saturday: every functional `must`, real e-mail, S2, the hostile reviewer
7. How the week is graded

---

## Your project so far, and where it is going

- **Week 1:** your tools, and your first real conversations with AI assistants
- **Week 2:** a real problem, real people who have it, the first requirements
- **Week 3:** the pitch and the market; your project became final
- **Week 4:** screens, and a classmate who clicked through them
- **Week 5:** the design, the contract, a server that answers 501, tests that are still red
- **This week, your product does its own work for the first time:** on your server, in your tests on GitHub, on a page a logged-in user can use
- **Next:** the same feature on a phone (7) · the chatbot and the feature on all three clients, the first build (8) · real testers (9), real users (10), and in December your app, installed from a store

<!-- Instructor: ask two students which requirement their product exists for. That is the one they build first today. -->

---

## One requirement, from start to finish

| Link | Where it lives | Since |
|---|---|---|
| 1–2. The requirement, its use case | `requirements.json` · `SRS.md` | Week 2 |
| 3. Its screen, with `serves:` | `prototype/` | Week 4 |
| 4. Its test cases, with `"run"` | `test_cases.json` | Week 4 |
| 5. Its rows of the API contract | `api.md` | Week 5–6 |
| 6. **Its routes, working: no 501** | `server/` | **today** |
| 7. **Its tests, green in GitHub Actions** | `server/tests/` | **today** |
| 8. **Its page, with `fetch`** | `web/` | **today** |

**`requirements.json` is the source; every other link follows it.**

---

## The chain in StudyRoom

| Link | StudyRoom |
|---|---|
| Requirement, use case | REQ-002 — book a free room for 30 to 120 minutes · UC2 |
| Screen | `book.html`, `serves: REQ-002` |
| Test cases | TC-002-01 (`web`) · TC-002-02 busy slot refused (`server`) |
| API rows | `POST /bookings` → 201 · 409 · 422 · 401 |
| Route | `create_booking`, with `current_user` |
| Test | `test_TC_002_02_…` green in **Actions** |
| Page | `web/book.html`, `fetch("/bookings", …)` |

A link that turns out wrong is changed **first**, with its line in `PROPOSAL.md`.

---

## The login comes ready to use

- An e-mail address → a **4-digit code**: valid **10 minutes**, works **once**
- A new code **within a minute** → **429** · not an e-mail address → **422**
- A wrong or expired code → **401** · **3 wrong codes in a row** (a new code does not reset the count) → **429 for 15 minutes**
- The right code → a **token**; "me" with `Authorization: Bearer <token>` → **200**, else **401**

**`server/course_login.py`** does all of it. The same for everyone, checked by ten course tests.

**Why:** every app has the same login, and small mistakes in it are easy to make. You spend your week on what only **your** project does.

---

## Connecting it — fifteen to twenty minutes

```json
{ "request_code": "POST /auth/code", "login": "POST /auth/login", "me": "GET /auth/me",
  "email_field": "email", "code_field": "code", "token_field": "token",
  "test_email_domain": "example.com", "email_must_end_with": "", "app_name": "StudyRoom" }
```

1. `server/login_contract.json`, **by hand**, from your `api.md`: method, one space, path.
2. In `server/main.py`:

```python
from server import course_login

app.include_router(course_login.router)
```

3. **Delete your own three login stubs** (the 501 ones): if they stay, they answer first.
4. `python -m pytest course_tests -q` → **10 passed**.

---

## The course tests, and trying it at `/docs`

```bash
python -m pytest course_tests -q
AIASD_CODE_FILE=login_code.txt uvicorn server.main:app --reload          # macOS, Linux
$env:AIASD_CODE_FILE="login_code.txt"; uvicorn server.main:app --reload  # PowerShell
```

- At `/docs`: ask for a code, read it in `login_code.txt`, log in, **Authorize** with the token, call "me". `login_code.txt` goes into `.gitignore`.
- "Fill in server/login_contract.json": a value is still in [brackets].
- "answered 422": the test address does not pass `email_must_end_with`. Fix `test_email_domain`.
- Saving a `.py` file restarts the server, and it forgets the tokens. After you change `login_contract.json`, stop it (Ctrl+C) and start it again.
- LOGIN_01–06: end of the lecture. LOGIN_07–10: Saturday.

<!-- Demonstration: wire the login into a fresh server live, in three minutes. -->

---

## Where an assistant helps this week

| Part | Assistant |
|---|---|
| The code of one route, with its requirement, acceptance criterion and `api.md` row in the prompt (one route, one commit) | **Helps** |
| A test from one of your test cases (you check it, line by line) | **Helps**, the approval is yours |
| The JavaScript of a page, with `fetch` | **Helps** |
| Reading a red test or a GitHub Actions log | **Helps** |

---

## … and where it does not help at all

| Part | Assistant |
|---|---|
| What a route does when the requirement is silent | **No help**: change the requirement first |
| `server/login_contract.json` | **No help**: by hand, from your `api.md` |
| `group_06.json`: what was tried, what happened, your decision | **No help** |
| Running the tests, reading what GitHub says | **No help**: you run, you look |
| The Change log lines and the change requests | **No help** |
| `ai_log_06.md` outside the Evidence block | **No help** |

<!-- Instructor: read the "No help" rows aloud. The new one is the first. -->

---

<h1 align="center">THE LOGIN CONTRACT<br>AND THE ATTACKER'S RECORD<br>YOU WRITE BY HAND.</h1>

<p align="center"><b>login_contract.json: copied from your api.md, by you.<br>group_06.json: typed by you while the attack happens.</b></p>

<p align="center">No assistant writes them, corrects them or completes them. Not even for the English.</p>

---

<h1 align="center">THE AI LOG IS WRITTEN<br>BY A HUMAN.</h1>

<p align="center"><b>Outside the Evidence block and its bold quotes: no assistant.<br>Not to write it. Not to improve it. Not even for the English.</b></p>

<h1 align="center">A log written by an assistant earns 0.</h1>

---

## Your lecture mark comes from GitHub, not from your laptop

On every push, **GitHub Actions** runs the checker. The checker runs the course tests and **your own tests**.

- For the lecture mark, I read **the GitHub run of your last commit pushed by the end of the lecture**.
- Push by **11:45**, open the **Actions** tab, and watch the run finish.
- A test that passes only on your laptop does not count.

**Never `git push --force`.** It deletes commits, and I grade your work from your history. CI is red because of a typo? Fix it in a **new** commit. A small fix never lowers the commit point.

---

## Now — until 10:00

1. Connect the login: the contract **by hand**, `course_login.router`, your stubs deleted.
2. `python -m pytest course_tests -q`: **10 passed**. Your TC-001 tests: with `AIASD_CODE_FILE` (assignment §1).
3. Your first own requirement: put its links side by side. Do they say the same thing?
4. A link missing or wrong (no `api.md` rows yet)? Fix it now, by hand, with its line in `PROPOSAL.md`.
5. `ruff check . --fix`, `ruff format .`, checker, commit, **push: mid-way and when done**.

<!-- Start the clock. Walk round: no assistant window open while login_contract.json is typed. -->

---

## Its routes, for real

```python
from server.course_login import current_user

bookings: list[dict] = []  # in memory for now; from Week 8 in a file or a database


@router.post("/bookings", status_code=201)
def create_booking(body: NewBooking, user: str = Depends(current_user)) -> dict:
    """REQ-002: a student books a free room for 30 to 120 minutes; a busy slot is refused."""
    if not 30 <= body.minutes <= 120:
        raise HTTPException(status_code=422, detail="A booking lasts 30 to 120 minutes.")
    if any(b["room"] == body.room and b["start"] == body.start for b in bookings):
        raise HTTPException(status_code=409, detail="This slot is already booked.")
    bookings.append({"id": len(bookings) + 1, **body.model_dump(), "by": user})
    return {"booking_id": len(bookings)}
```

Every error of the `api.md` row, with its status code, and **the message your test case expects**.

---

## Who may do it — the server decides

| Code | When | Example |
|---|---|---|
| **401** | not logged in | no token, or an unknown one |
| **403** | logged in, not allowed | someone else's booking · the instructor's action |
| **404** | no such thing | `/bookings/999` |
| **409** | it conflicts with existing data | the slot is already booked |
| **422** | missing, empty, wrong form | 500 minutes · a text of only spaces |

`current_user` says **who** asks. Hiding a button is not security: the **route** answers 403. Does the page need a list that `api.md` does not have? **Add the row first.**

---

## What the assistant will "help" with

| It offers | Why it is wrong | What catches it |
|---|---|---|
| A field nobody asked for (`is_admin`, `price`) | no requirement asks for it | your review of the prompt's answer |
| The ownership check left out "for simplicity" | anyone changes anyone's data | the attacker round · a 403 test |
| An error turned into 200 with a message | the client thinks it worked | your test case's status code |
| Its own idea of the rule ("up to 4 hours") | the requirement says 120 minutes | your test case's values |

**One route at a time.** The requirement, its acceptance criterion and the `api.md` row in the prompt. Read the whole answer.

---

## Its tests — named by its test cases

```python
from server.course_login import auth_header_for_tests


def someone(name: str) -> dict[str, str]:
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

One test per test case with `"run": "server"` · a **new address** in every test · **two users** when the test case is about who may do what.

---

## Now — until 11:00

1. The routes of your first requirement: no longer 501, `current_user` where it needs a user.
2. `"run"` on its test cases first; then one test for each with `"run": "server"`, named by its id.
3. `python -m pytest server/tests -q` green on your laptop.
4. Ruff, checker, commit, **push: mid-way and when done**.
5. The **Actions** tab: `AIASD-TEST … TC-002-02 passed`?

---

## Its page — the prototype's screen, made real

Copy its screen from `week04/prototype/` into `web/`: you create it at the root, next to `server/`. Keep its look and its `<!-- serves: REQ-… -->` line.

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
```

The fixed data of the prototype → what the server answers. The server's refusals → the words of your test cases. The server's text → `textContent`, never `innerHTML`.

---

## Behind the login, served by your server

- `web/login.html` = the prototype's `index.html` + `code.html`, with `serves: REQ-001, REQ-006` and `style.css`.
- Call the login paths with `fetch` directly, not `api()`. On 401, show "Wrong code".
- No token → every page goes to the login.

```python
from pathlib import Path

from fastapi.staticfiles import StaticFiles

WEB = Path(__file__).resolve().parent.parent / "web"
if WEB.is_dir():
    app.mount("/web", StaticFiles(directory=WEB, html=True), name="web")
```

Open http://127.0.0.1:8000/web/login.html at **390 px**, log in, use your feature. A mounted folder needs no `api.md` row.

---

## What the prototype only pretended is now real

| In the prototype | On the real page |
|---|---|
| A switch "Student / Instructor" | the role comes from **the login** |
| A fixed code, a fixed list | the server makes them |
| Every click "works" | the server can say **no**: 403, 409, 422 |

A test case whose steps still name what only the prototype had ("tap Instructor in the view strip", "room 3 is always free") is changed with **one change request** for all of them.

---

## The attacker round — about 11:25 to 11:45

Your Week 3 group meets again, with one job: **break each other's feature**.

The owner's server runs on the owner's laptop. The attacker logs in there with **their own address** and tries:

- **someone else's data** with their own token: change the id in the address
- **an action that is not theirs**: the instructor's, the owner's
- **an empty text, only spaces, a very long text**, a number out of range
- **the same thing twice**; and the login: wrong codes, no token

Nobody from your group here? Work with any classmate. Then change roles.

---

## `week06/group_06.json` — the owner types it, by hand

```json
{
  "student_id": "123456789",
  "role": "attacker",
  "tried": "Logged in as mia, they sent DELETE /bookings/1, Deniz's booking, with curl.",
  "happened": "200: Deniz's booking was gone."
}
```

One entry for each attacker. `accepted` and `why` wait until Saturday: first see whether the finding is real.

**The attacker uses your laptop only to attack.** Nobody commits on a classmate's laptop.

---

## Now — until 11:45

1. The page of your first requirement in `web/`, behind the login, at 390 px.
2. The attacker round, both ways.
3. `group_06.json`: one entry for each attacker, typed by you.
4. Ruff, checker, commit, **push: mid-way and when done**; the **Actions** tab: watch your run finish.

Push by 11:45. The lecture mark reads your last commit pushed by the end of the lecture, and its Actions run.

---

## Commit discipline

**In the lecture:** commit each piece of work **in the middle**, again when it works, and push every commit right away. A piece that arrives finished in one commit does not count.

**Outside the lecture:** at least two commits with new work, **pushed at least one hour apart**. GitHub's push time counts, not the date on a commit. A commit made by a coding agent never counts.

A small fix commit (a typo, a ruff error) never lowers the point. One commit at the end scores nothing. **Never force push**, and never let an assistant do it.

---

## By Saturday 23:59

- **Every functional `must` requirement, end to end:** every `api.md` row answers (no 501) · every `must` test case with `"run": "server"` has its test, green on GitHub · a page in `web/` with `serves:` and `fetch` (REQ-001 too: `login.html`)
- **Every changed link** with its line in `PROPOSAL.md`
- **The code by real e-mail**; `.env` not committed; `.env.example`; `week06/email_code.png`
- **All ten course tests** green on GitHub
- **S2** in `week04/store.json` · **`"run"`** on every test case
- **Your decision** on each attacker finding · **`ai_log_06.md`**: the hostile reviewer

`should` and `could` may still answer 501. A part only a phone can do comes in Week 7.

---

## When a link of the chain must change

Your requirements and test cases became your **baseline** last Saturday.

| What changes | How |
|---|---|
| `requirements.json`, `test_cases.json` | a **change request**: `CR-` and the next free number, the ids, every file it affects |
| `api.md`, a use case, a screen | an ordinary dated Change log line |
| `"run"` on a test case | asked by the course: **not** a change request |

*"2026-10-27 — CR-01: TC-002-01 to TC-003-02: the steps no longer use the prototype's view switch and its fixed list of rooms; the role comes from the login and the rooms from the server; affects week04/test_cases.json."*

---

## The code by real e-mail — `.env`

```text
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=the 16-letter app password
SMTP_FROM=you@gmail.com
```

- Without `AIASD_CODE_FILE`, the login sends the e-mail. PowerShell: close the window, or `Remove-Item Env:AIASD_CODE_FILE`.
- **`.env` is never committed** (`.gitignore` lists it). Committed by mistake? Change the app password at once.
- `.env.example`: the five names, **no password**. Gmail: 2-step verification, then an **app password**.
- Screenshot the e-mail with the code: **`week06/email_code.png`**.

---

## S2, and how each test case is run

**S2** in `week04/store.json`, next to S1: your app's record in the store's console.

```json
"S2": { "date": "2026-10-31", "app_name": "StudyRoom", "package": "com.example.studyroom", "evidence": "store_s2.png" }
```

The package name or bundle id can **never** be changed. Google Play does not ask for the package name yet: the first upload (S3, Week 8) fixes it. Choose it now anyway, write it in S2, and use it as the `applicationId` in Week 7. Not accepted yet? Say so in the AI log.

**`"run"`** on every test case: `"server"` (a test in `server/tests/`), `"web"` (on your page), `"manual"` (a person: a phone, the store, a user).

---

## Your own tests

- `auth_header_for_tests` logs a test user in through the real login (no e-mail in a test).
- **A new address in every test**; **two users** when the test case is about who may do what.
- freezegun? Only if a test moves the clock; then the `freezegun.configure` line of the assignment.

**For every error in your `api.md` rows, write a test that checks it.** A test that stays green when the route forgets the error is not testing it.

---

## The AI log — the hostile reviewer, on your feature

Your groupmate attacked your feature. Now an assistant does (`AI_Doc5` §3).

1. Give it your feature's routes and their requirements: "the three strongest attacks, numbered."
2. **Try each one yourself**: against your server, or in a test.
3. What your server did against each, with the status code.
4. **The one you fixed**, and the test that now catches it.
5. **The one that is wrong**, and the evidence.
6. The assistant and your groupmate: who found what the other missed?

Your words plain, the assistant's words bold. Evidence block: `ME:`, `AI:`, `TERMINAL:`, untouched. **A log written by an assistant earns 0.**

---

## How Week 6 is graded — 10 points

| | Points | What |
|---|---|---|
| End of lecture (GitHub) | 5 | login (LOGIN_01–06), one own route working, one test green on GitHub, its page, the attacker's record |
| Saturday checker | 2 | every functional `must` end to end, real e-mail, all tests green, S2, `"run"`, decisions, AI log |
| Human involvement | 2 | the AI log by you; `login_contract.json` and `group_06.json` by hand |
| Commit discipline | 1 | 2 commits per piece, one mid-way; outside: two, an hour apart; no agent commits |

Bonus: 10% per attacker named and per attack made; S2 counts for the store bonus. **One student, one computer, one GitHub account.**

---

## Next week: the same feature, on a phone

**Week 7:** the mobile client. The login and the screens of your own feature, now on a phone. The same endpoints, unchanged, called from the phone. Its test cases are run on a phone and recorded.

**Week 8:** the chatbot, through your server and a hosted LLM API of your choice; your feature complete on the server, the web and the phone; the first build on the store's test track.

**Before Week 7:** the mobile framework of your choice installed (Flutter, React Native–Expo, Kotlin or Swift), and a phone or an emulator that runs its first app.

<!-- Instructor: the slides from "By Saturday" on are for the last minutes, after the 11:45 push. The mark reads the last commit pushed by the end of the lecture. -->
