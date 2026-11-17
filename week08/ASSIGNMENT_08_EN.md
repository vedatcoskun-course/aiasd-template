# Week 8 Assignment: The Chatbot, and Your First Build for Testers

## 1. Rules and grading

### 1.1 Rules

- **Use one unshared computer and one unshared GitHub account.** You must work in the lecture on your
  own computer, and you must work after the lecture on the same computer. Only the computers that you listed
  in `student.json` count. Lecture work that you do on a computer that is not listed in `student.json`, or
  under another person's Git identity, earns nothing for the lecture.

- **Commit in the middle of the work, and never 'force push'.** Commit each piece of work while it is still unfinished, and commit it again when it works. Push every commit right away. A red check on unfinished work costs you nothing. A force push costs you the commit point of the week, whatever it changed.
- **Fill in the AI log without any AI help. If an assistant helps you with the AI log in any way, your
  AI log earns 0.** Do not use an assistant to write the log, to improve it, to translate it or to correct its
  language.

**Where an assistant helps this week, and where it cannot:**

| The work | The assistant |
|---|---|
| Write the code of `POST /chat` and of the chat screen. Read an error of the LLM API or of the build. | The assistant helps. |
| Draft the system prompt of your chatbot. | The assistant helps. You must decide the final text. |
| Choose what the chatbot does for your users. | The assistant cannot help. Your users and your requirements must decide. |
| Write the change request, the requirement and the test case of the chatbot. | The assistant cannot help. |
| Fill in S3 in `week04/store.json`. | The assistant cannot help. |
| Write `ai_log_08.md`. | The assistant cannot help in any way. If an assistant helps you, your AI log earns 0. |

### 1.2 How your performance will be graded

Your performance in the lecture will be graded out of 5 points. I will read the last commit that you pushed by the end of the lecture, and I will check the following:

- You listed your computers in `student.json` in a commit before your other lecture commits, and your first push reached GitHub before 09:30.
- You added the change request of the chatbot, with its requirement, its test case and its `api.md` row.
- `POST /chat` works on your server, and no key is in your repository.
- The chat screen in `mobile/` has its `serves:` line and shows the label "AI answer".

Your performance before Saturday 23:59 will be graded out of 5 points. I will read the last commit that reached GitHub by 23:59. GitHub's push time counts, not the time on a commit.

- Green checks will earn you 2 points.
- The AI log will earn you 2 points when it tells your real use of the whole week, matches your commits and shows how you checked the answers. It will earn you 1 point when it is too general or when it does not show how you checked the answers. It will earn you 0 points when an assistant wrote it, when your commits contradict it, or when it is empty.
- Commit discipline will earn you 1 point.

I will give you a warning first for a format error. If you repeat the same error in a later week, you will lose 1 point.

---

## 2. Semester plan at a glance

<table>
<tr><th width="10%" align="center">Week</th><th width="15%" align="center">Dates</th><th width="70%" align="left">What we do</th></tr>
<tr><td align="center">1</td><td align="center">22–23 Sep</td><td>You set up the tools, learned Git and GitHub, and took a first look at LLMs.</td></tr>
<tr><td align="center">2</td><td align="center">29–30 Sep</td><td>You wrote Proposal Part A, the requirements, and the SRS with its use cases.</td></tr>
<tr><td align="center">3</td><td align="center">6–7 Oct</td><td>You pitched your project in your group, wrote Proposal Part B and chose your store (S0).</td></tr>
<tr><td align="center">4</td><td align="center">13–14 Oct</td><td>You made the clickable prototype and wrote the test cases (S1).</td></tr>
<tr><td align="center">5</td><td align="center">20–21 Oct</td><td>You wrote the design and the API contract, and you started the server. Your requirements became your baseline.</td></tr>
<tr><td align="center">6</td><td align="center">27–28 Oct</td><td>Your feature worked end to end, on the server and on the web (S2).</td></tr>
<tr><td align="center">7</td><td align="center">3–4 Nov</td><td>Your app ran on the phone.</td></tr>
<tr><td align="center">–</td><td align="center">10–11 Nov</td><td>There is no lecture.</td></tr>
<tr><td align="center"><b>8</b></td><td align="center"><b>17–18 Nov</b></td><td><b>This week, your product will get its chatbot, your server will keep its data after a restart, and your first build will go to your testers (S3).</b> <i>Start early: see the list below.</i></td></tr>
<tr><td align="center">9</td><td align="center">24–25 Nov</td><td>Your testers will test your app in the beta test. You will write the tests of the chatbot and add the Report button to its answers (S4).</td></tr>
<tr><td align="center">10</td><td align="center">1–2 Dec</td><td>You will do the UAT, draw the deployment diagram and submit your app to the store (S5). <i>Start early: see the list below.</i></td></tr>
<tr><td align="center">11</td><td align="center">8–9 Dec</td><td>You will apply the review fixes, release your app on the store and write the final README (S6). <i>Start early: see the list below.</i></td></tr>
<tr><td align="center">12</td><td align="center">15–16 Dec</td><td>You will make the poster and rehearse the defence. <i>Start early: see the list below.</i></td></tr>
<tr><td align="center">13</td><td align="center">22–23 Dec</td><td>Students whose app is live on the store will present their projects.</td></tr>
<tr><td align="center">14</td><td align="center">29 Dec</td><td>The other students will present their projects.</td></tr>
</table>

**Start early.** Some work of the coming weeks will take days, not hours, so I kindly ask you to start it early:

- **Week 8:** You will need at least 12 testers, and at least 6 of them must be your classmates. Google Play requires your testers to stay on your test track for 14 days in a row before you can apply for production.
- **Week 10:** You will need the store listing of your app: its icon, its screenshots, its descriptions and the address of your privacy text. You will also need a few real users for the UAT.
- **Weeks 10 and 11:** The review of your app by the store can take several days, and this time is your responsibility. Submit your app in Week 10 as planned, so that you have time to apply the review fixes in Week 11. The other 3 points of the presentation in Week 13 also require that you submitted your app by Saturday 5 Dec 23:59.
- **Week 12:** You will need the screenshots of your app and your architecture diagram for your poster.

---

## 3. This week

### 3.1 This week at a glance

Since Week 6, your project has worked end to end: on the server and on the web, and since last week also on the phone. This week, your product will get its chatbot, and your first build will go to your testers.

The chatbot shall run through your own server. The phone shall never talk to the LLM API. Only your server shall talk to it, and only your server shall hold the key.

```text
start  the chat screen in mobile/
  ↓    POST /chat
  ↓    your server
  ↓    the LLM API of your choice (the key is only in server/.env)
  ↓    your server
  ↓    the chat screen shows the answer as "AI answer"
```

- Your requirements became fixed as your baseline at the end of Week 5, and the chatbot was not among them. So you must add the chatbot as a change request: you must add a new requirement, its test case and its row in `api.md` (§4.2).
- The phone and the web shall keep calling the same server, as they did in Week 7.



**What you do in the lecture**

<table>
<tr><th width="15%" align="left">Time</th><th width="75%" align="left">Your work</th><th width="10%" align="center">§</th></tr>
<tr><td>before the class</td><td>Open an account with the LLM API of your choice, and create its key. Do this before the lecture day, for example at home.</td><td align="center">4.3</td></tr>
<tr><td>before any other commit</td><td>Add a list of your computers to <code>student.json</code>. For each computer, write its name (the command in §4.1 shows it), the Git e-mail that you use on it, whose computer it is, and who else uses it. Commit this change on its own (<code>week08: my computer</code>). You can do this before the lecture. The issue "Prepare for Week 8" in your repository shows how.</td><td align="center">4.1</td></tr>
<tr><td>09:30</td><td>Run the checker: it brings <code>week08/</code>. Commit the course files, and push both commits right away.</td><td align="center">4.1</td></tr>
<tr><td>about 10:00</td><td>Write the chatbot as a change request: add its requirement, its test case and its <code>api.md</code> row.</td><td align="center">4.2</td></tr>
<tr><td>about 10:45</td><td>Make <code>POST /chat</code> work on your server.</td><td align="center">4.3</td></tr>
<tr><td>about 11:30</td><td>Make the chat screen in <code>mobile/</code>.</td><td align="center">4.4</td></tr>
<tr><td>11:45</td><td>Push for the last time.</td><td align="center">4.5</td></tr>
</table>

Your lecture performance will be graded out of 5 points, and Saturday performance will be graded out of 5 points. The details are in §1.2.

**Next week, your testers will work from a test plan that is made from your own files**: your requirements, your screens and your test cases. Keep these files consistent this week.

### 3.2 What you are going to learn this week

This week, you are going to learn:

- how a server calls an LLM API safely, with the key kept out of the code and out of the app;
- how to protect a chatbot with the login, a daily limit and the data of the user only;
- how to put a first build on the test track of a store.

You will also use these new terms:

| Term | What it means |
|---|---|
| LLM API | An LLM API is a service on the internet that answers a text with a text, such as the Gemini, OpenAI, Anthropic or Groq API. Your server sends it a message and gets an answer back. |
| API key | The API key is the password of your LLM API account. Whoever has the key can spend the money of your account. The key must stay only in `server/.env`. |
| `.env` | `.env` is the file of your server that holds passwords and keys. It is listed in `.gitignore`, so it never reaches GitHub (`AI_Doc3`, python-dotenv). `server/.env.example` holds only the names, such as `LLM_API_KEY=`. |
| System prompt | The system prompt is the instructions that your server sends to the model before the message of the user. It says what the chatbot is for, and what it must not do. |
| Daily limit | The daily limit is the number of messages that one user can send in one day. After the limit, your server shall answer 429. |
| Test track | The test track is the part of the store where a build goes to testers before it goes to the public. On Google Play, the test track is called closed testing. |
| S3 | S3 is the third store step. In S3, your first build is on the test track, and your testers are enrolled on it. |

### 3.3 What the checker brings this week

When you run the checker at the start of the lecture (§4.1), it brings the new folder `week08/` into your repository. The folder holds three files:

- `ASSIGNMENT_08_EN.md` and `ASSIGNMENT_08_TR.md`: this assignment, in English and in Turkish;
- `ai_log_08.md`: the form of your AI log, which you will fill in on Saturday (§5.5).

The checker itself also gets new checks this week. It will check the list of your computers in `student.json`, the change request of the chatbot, `POST /chat` on your server and the chat screen in `mobile/`. On Saturday, it will also check S3 in `week04/store.json` and the address of your privacy text.

---

## 4. Your work in the lecture

### 4.1 Your computers, the course files and the first push, before 09:30

Do these three steps in this order at the start of the lecture.

**Step 1. Update `student.json`.** `student.json` is in the root folder of your repository, the file in which you wrote your student number in Week 1. First, open a terminal in your project folder, and run these two commands. The first one shows the name of your computer, and the second one shows your Git e-mail.

<table>
<tr><th width="50%" align="left">On a Mac</th><th width="50%" align="left">On Windows or Linux</th></tr>
<tr>
<td>

```bash
scutil --get LocalHostName
git config user.email
```

</td>
<td>

```bash
hostname
git config user.email
```

</td>
</tr>
</table>

The e-mail must be the e-mail of your own GitHub account. If it is not, set your own name and e-mail first, and then run the two commands again:

```bash
git config --global user.name "Your Name"
git config --global user.email "the e-mail of your GitHub account"
```

Then add the list of your computers to `student.json`, after the `"section"` line, and put a comma at the end of that line. Write the two outputs into it:

```json
  "computers": [
    {
      "hostname": "the name of your computer",
      "git_email": "the output of git config user.email",
      "owner": "your student number",
      "also_used_by": "",
      "why": ""
    }
  ]
```

- In `"hostname"`, write the name of your computer as the first command showed it, for example `"Ayses-MacBook-Air"` or `"DESKTOP-4F7K2Q1"`.
- In `"git_email"`, write the output of `git config user.email`, for example `"vedat.coskun@atlas.edu.tr"`.
- In `"owner"`, write your student number if the computer is yours, for example `"123456789"`. If it belongs to another student, write that student's number. If it belongs to someone who is not a student, write who it is, for example `"my father"`.
- In `"also_used_by"`, write the student number of every other student who also uses this computer, or who else uses it, for example `"my sister"`. Leave it empty when nobody else uses it. A classmate in this course may never use it.
- Leave `"why"` empty when you use only one computer. If you really need a second computer, for example a desktop at home, add a second entry for it, and write in `"why"` why you need it.

Then commit this change on its own:

```bash
git add student.json
git commit -m "week08: my computer"
```

**Step 2. Bring `week08/`.** Run the checker. It brings `week08/`. Then commit the course files.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week08: course files"
```

**Step 3. Push right away.** Push both commits immediately, before 09:30.

```bash
git push
```

The checker also reads the name of your computer and your `git config user.email`, and it tells you if this computer is not listed in `student.json`.

### 4.2 The chatbot as a change request

First, decide in one sentence what your chatbot does for your users. The chatbot shall serve your product. For example, it answers questions about the bookings of the user, or it suggests a weekly plan from the records of the user. A chatbot that only chats about anything does not count.

Your requirements became your baseline in Week 5, so a new requirement is a change request (Week 6 §9). Make the three changes below, and name all three in one line of the Change log in `PROPOSAL.md`.

- **Add the requirement.** Add a functional `must` requirement to `week02/requirements.json` with the next free id. Its acceptance criterion must say what the chatbot answers, that only a logged-in user can use it, that it uses only the data of this user, and how many messages a user can send in a day.
- **Add the test case.** Add at least one test case for the requirement to `week04/test_cases.json`, with `"run": "manual"`. A person must run this test case on the phone this week. The tests that run on the server, with a fake model in place of the LLM API, come in Week 9.
- **Add the `api.md` row.** Add the row of `POST /chat` to `week05/api.md`. The request shall hold the message of the user, and the answer shall hold the answer of the chatbot. The errors shall be 401 without a token, 429 after the daily limit, and 503 when the LLM API does not answer.

Here is an example of the Change log line: *"2026-11-17 — CR-03: the chatbot. New REQ-012 (must), new TC-012-01 (manual), new api.md row POST /chat; affects week02/requirements.json, week04/test_cases.json, week05/api.md."*

### 4.3 `POST /chat` on your server

- **Get your key before the class.** Open an account with the LLM API of your choice, and create a key. The sign-up can take some time, so do it before the lecture day, for example at home.
- **Keep the key only in `server/.env`.** Put the key into `server/.env` as `LLM_API_KEY=...`, and read it with `os.getenv("LLM_API_KEY")`. Never write the key into your code, into your app or into a file that you commit. Add `LLM_API_KEY=` without a value to `server/.env.example`. The checker looks for keys in every file of your repository.
- **Require the login.** Without a valid token, the route shall answer 401, as your other routes do.
- **Send the model only the data of the user.** If the chatbot answers questions about records, send the model only the records of the logged-in user. Never send the data of other users, e-mail addresses or passwords.
- **Limit the messages of each user.** Count the messages of each user per day. After the limit in your requirement, your server shall answer 429 with a message that the user can read.
- **Handle a failure of the LLM API.** Your server shall wait at most 20 seconds for the LLM API. If the API does not answer, or if it answers with an error, your route shall answer 503 with a message. The server shall not crash.

You will choose the LLM API. You do not need to pay: the Gemini API, Groq and GitHub Models have free tiers that need no credit card. If you choose a paid API, its cost is yours. A free tier may let the provider use what you send, so never send personal data to it.

### 4.4 The chat screen in `mobile/`

- The source file of the screen shall name the requirement of the chatbot: `// serves: REQ-0NN`.
- The screen shall send the message to `POST /chat` with the token, as your other screens do.
- The screen shall show each answer of the chatbot with the label **AI answer**, so the user knows that a model wrote it.
- The screen shall show the messages of 429 and 503 to the user.

Commit the screen while it is still unfinished, for example when it shows the field and the button but does not call the server yet. Commit it again when it works.

### 4.5 Push, and check the result on GitHub

Run `ruff check . --fix` and `ruff format .`. Then run the checker, commit and push. Open the Actions tab, and check the run. The lecture mark reads the last commit that you pushed by the end of the lecture.

---

## 5. Your work by Saturday 23:59

### 5.1 Your own feature is complete on all three clients

Every functional `must` requirement shall work on the server, on the web and on the phone. Each requirement needs a route with a green test, a page in `web/` and a screen in `mobile/`, and each of them needs its `serves:` line. Your feature must be complete before your testers see it next week.

**Complete first what is still missing from Weeks 5, 6 and 7.** Run the checker: it lists every route, test, page and screen that is still missing. The checker checks the work of every earlier week again each Saturday, so a missing part lowers your checker points every week until you complete it. Your testers can only test the parts that work.

### 5.2 Your data stays after a restart

Until now, your server could keep its data in memory. From this week, your server shall keep its data in a file or in a database of your choice, for example in SQLite. Try it: start the server, add a record, stop the server, start it again, and check that the record is still there. Write in one line of `week05/DESIGN.md` where your server keeps its data, and add a dated line to the Change log.

### 5.3 S3: your first build on the test track

Every student must enrol at least 12 testers, whatever the store is, and at least 6 of them must be your classmates. A classmate can be your tester only if their phone can install your app from your store: an Android phone for Google Play, Huawei AppGallery or Samsung Galaxy Store, and an iPhone for the App Store. First, collect the e-mail addresses of your testers. Google Play needs the e-mail address of the Google account of each tester.

Then upload your first build to the test track of your store, and enrol your testers on it.

- On Google Play, the test track is a closed test. Google Play itself requires at least 12 testers for a new personal account, and they must stay enrolled for 14 days in a row before the app can be released. If you enrol them this week, the 14 days end before the submission in Week 10.
- Other stores have their own test tracks (`AI_PLATFORMS_AND_STORES`). Enrol your 12 testers there in the same way.

Then fill in S3 in `week04/store.json` yourself, and add a screenshot of the test track that shows your enrolled testers:

```json
  "S3": {
    "date": "2026-11-21",
    "track": "closed testing",
    "version": "1.0.0 (1)",
    "classmate_testers": ["123456789", "234567891", "345678912", "456789123", "567891234", "678912345"],
    "other_testers": ["Ayşe Yılmaz", "Mehmet Demir", "Elif Kaya", "Can Öztürk", "Zeynep Arslan", "Emre Şahin"],
    "privacy_url": "https://gist.github.com/your-name/...",
    "evidence": "store_s3.png"
  }
```

In `"classmate_testers"`, write the student numbers of your classmates who are your testers. In `"other_testers"`, write the first name and the surname of each of your other testers. Together, the two lists must hold at least 12 testers, and `"classmate_testers"` must hold at least 6. The e-mail addresses of your testers must never go into your repository.

### 5.4 Your privacy text

The privacy text of your app shall say that the messages of the chatbot go to your LLM API, and it shall name the provider. Write the text in `PRIVACY.md` at the root of your repository. Google Play asks for the privacy text as a web address that anyone can open without a login, and your repository is private. So publish the same text also on a public page, for example as a public GitHub Gist. Write the address of this page in S3 of `week04/store.json` (§5.3) and in the Play Console.

### 5.5 The AI log: `week08/ai_log_08.md`

From this week, the AI log must tell how you used AI assistants in the whole week, in all of your work. It must no longer describe one exercise or one example. I will compare the log with your commits and check that you really worked in the way that it describes. Fill it in yourself on Saturday:

1. **My assistants.** List each assistant that you used, its model, and whether it is free or paid. For a paid assistant, write the name of the plan.
2. **Every use of an assistant this week.** Write one row for each real use, in the order of the week, and not only the good ones. In the row, write what you asked, how you checked the answer, what you did with it (you kept it, changed it or refused it), and the commit where the result went.
3. **How I worked with assistants this week.** In a few sentences, describe your way of working over the whole week: when you turned to an assistant, how you usually checked its answers, and what you usually kept or refused.
4. **What I did without an assistant.** Write which part of the work you did yourself.
5. **Next week.** Write one thing that you will do differently next week.
6. **Before this course and now.** This part will not be graded, so I kindly ask you to write it honestly. Write how you used AI assistants for code before this course, and what you do differently now.

Short, plain sentences are enough. The log no longer has an Evidence block or bold quotes. A person reads the log and compares it with your commits. **You must write the AI log without any AI help. If an assistant helps you with the log in any way, your AI log earns 0.**

### 5.6 Commits, and green checks

- Outside the lecture, push at least two commits with new work, at least one hour apart.
- Each commit must add at most one new screen to `mobile/` and at most one new route to `server/`. The checker warns you before you commit.
- A commit that a coding agent made never counts.
- The ten course tests, and the tests of every `must` test case with `"run": "server"`, must stay green on GitHub. Never change `.github/workflows/check.yml` or `.github/check_deliverables.py`.
- Git must not hold the build folders of your app (Week 7 §12).


### 5.7 Revise all project documents as required each week

The requirements, the SRS with its use cases, every diagram, the screens with `serves:`, the test cases, `api.md`, `DESIGN.md`, the code and the tests must describe one product. When one of them changes, update the others in the same week, and write a line in the Change log. The checklist in §5.8 helps you.

### 5.8 Your documents: a checklist

Before your last push on Saturday, check that your documents describe your product as it is now:

- The diagram in §5 of `PROPOSAL.md` shows the parts that you have now. This week, it also shows your LLM API. The Change log has a line for every change of the week.
- Every requirement in `week02/requirements.json` belongs to a use case in `week02/SRS.md`, and the use case diagram shows every use case, the use case of the chatbot too.
- Every screen in `web/` and `mobile/` names an existing requirement in its `serves:` line.
- Every test case in `week04/test_cases.json` names an existing requirement, and its steps match your screens as they are now.
- Every route of your server has its row in `week05/api.md`, with the same path, request and status codes.
- The components and the architecture diagram in `week05/DESIGN.md` match your code. This week, they also show the LLM API and the place where your data is kept.
- Every change to a requirement or to a test case has its CR line.

The checker checks some of the links between the ids. Only you can check the diagrams and the texts.
