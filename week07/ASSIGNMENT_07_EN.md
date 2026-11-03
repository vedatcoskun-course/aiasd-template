# Week 7 Assignment: Your App on a Phone

## The week in five minutes

First, let us recall what we have done so far and where we are now. In Weeks 1, 2 and 3, you found a problem that you or the users around you have, and you wrote the requirements of these users. In Week 4, you drew the user screens of the project and wrote its test cases. In Week 5, you created the design and wrote the API contract; at this stage, your server answered 501. In Week 6, the first version of your project worked end to end, in the web client and on the server.

This week, the same version will run on a phone instead of the web. The server side normally stays as it is; if it must change, follow the order in the box "One server for the web and the phone".

```text
            web/book.html   ──┐
                              ├──►  POST /bookings   your server: one for both clients
 mobile/lib/book_screen.dart ─┘     the same token, the same answers
```

- Develop the mobile app with Flutter, React Native–Expo, Kotlin or Swift.
- The mobile app will call the same endpoints as your web page.
- Each screen must contain its requirement in a comment, for example `// serves: REQ-002`. This comment will connect the screen to its requirement. In this way, the phone screen will be added to the chain of the requirement as its ninth link.

What you do in the lecture

| Time | Your work | § |
|---|---|---|
| before the lecture | Your framework must be installed before you start. You must have done this in Week 6. To install it, follow the page of your framework: docs.flutter.dev/get-started/install for Flutter, docs.expo.dev/get-started/set-up-your-environment for Expo, Android Studio (developer.android.com/studio) for Kotlin, and Xcode from the Mac App Store for Swift. Section 3 of `AI_PLATFORMS_AND_STORES` shows which path your laptop and your phone allow. | - |
| 09:30 | Run the checker. The checker will bring the folder `week07/`. Then commit and push. | §1 |
| about 10:00 | Create your app in `mobile/`. Its id must be the package name of S2. The app must run on your phone or on an emulator. | §2 |
| about 10:45 | The login screen on the phone must talk to your server. Save a screenshot of it as `week07/phone_login.png`. | §3 |
| about 11:15 | Make the screen of the requirement that you built first in Week 6. This screen must send its requests to the endpoints of that requirement in `api.md`, for example `POST /bookings`. | §4 |
| 11:45 | Do the tester round: let a classmate run your test cases on your phone, and run their test cases on their phone. Write each run of your classmate into `mobile_runs.json`, and write their student number and their finding into `group_07.json`. Then push for the last time. | §5–§7 |

By Saturday 23:59

- Every functional `must` requirement must have a matching screen in `mobile/`. The screen must send requests to the endpoints of the requirement in `api.md` (§8).
- Every functional `must` requirement must have a test case that passed on the phone. Run every failed test case again (§9).
- The `id` of your app must be the package name of S2 (§10).
- Decide what to do with the finding of your tester (§11).
- Git must not hold the build folders of your app (§12).
- The tests must still be green on GitHub (§13).
- Write the AI log about one small change to your app (§15).

Grading: The lecture part will be graded out of 5 points. The part due on Saturday will also be graded out of 5 points. The details are in the section "How this week is graded", at the end of this assignment.

In the coming weeks, your product will include its chatbot. Your app will be complete on the server, the web and the phone, and your first build will go to the test track of the store. Real testers will join in Week 9, and real users will join in Week 10. After that, the store will review your app. Before the presentation, you will download your app from the store where you uploaded it, and install it.

Before Week 8, collect the e-mail addresses of your testers. A new personal Google Play account needs 12 testers for 14 days. Also open an account with the LLM API that you will use. The key of this account must go only into `.env`.

## The chain gets one more link

Each of your functional requirements is a chain of links. This week, the ninth link of the chain will form.

| Link | Where it lives | Since |
|---|---|---|
| 1 and 2. Requirements and use cases | `week02/requirements.json` and `week02/SRS.md` | Week 2 |
| 3. Screens, with `serves:` | `week04/prototype/` | Week 4 |
| 4. Test cases, each with `"run"` | `week04/test_cases.json` | Week 4 |
| 5. Rows of the API contract | `week05/api.md` | Weeks 5 and 6 |
| 6 and 7. Routes, and tests that are green on GitHub | `server/` and `server/tests/` | Week 6 |
| 8. The page in the web client | `web/` | Week 6 |
| 9. The screen in the mobile client; this screen sends requests to the same endpoints | `mobile/`, with `// serves: REQ-…` | This week |

`requirements.json` is still the source. The phone screen must do what the requirement and its test cases say, as the web page does. If the phone shows that a link is wrong, change that link first. Write a line about the change in `PROPOSAL.md`. For a requirement or a test case, this line is a change request, as in Week 6 §9.

### What you need to know this week

| Term | What it means |
|---|---|
| The mobile client | The mobile client is the app on the phone. It shows the screens and calls your server. Only your server decides. |
| `mobile/` | `mobile/` is the folder of your app. It is at the root of your repository, next to `server/` and `web/`. Create it with the tool of your framework (§2). |
| Emulator, simulator | An emulator or a simulator is a phone that runs as a program on your laptop. Android Studio has the Android emulator. Xcode has the iOS simulator, and Xcode runs only on a Mac. |
| The address of the server | The Android emulator reaches your server at `10.0.2.2`. The iOS simulator reaches it at `127.0.0.1`. A real phone reaches it at the address of your laptop on the Wi-Fi (§3). |
| `--host 0.0.0.0` | This option starts your server so that other devices on the network can reach it. Without the option, only your laptop reaches the server. |
| Endpoint, path | An endpoint is one row of `api.md`, such as `POST /bookings`. Its path is the part that starts with `/`, such as `/bookings`. Your app sends its requests to these endpoints, as your web page does. |
| Plain http | Your server speaks `http`, not `https`. Android and iOS refuse plain http, unless the app allows it (§3). |
| App id | The app id is the `applicationId` on Android and the bundle id on iOS. It is the package name that you chose for S2 in Week 6, such as `com.example.studyroom`. |
| `week07/mobile_runs.json` | This file records the test cases that ran on the phone. It works like the walk-through of Week 4. |
| The tester | The tester is a classmate from your Week 3 group. The tester runs your test cases on your phone in the lecture. |
| Small diff | A small diff is one change that you ask from an assistant. Read the change line by line before you accept it (`AI_Doc5` §6). Small diffs are the technique of this week. |

> ## Commit in the middle of the work, not at the end
>
> The times above show a pace. They are not push times. Commit each piece of work while it is still
> unfinished. For example, commit a screen that shows its fields but does not call the server yet. Commit
> the piece again when it works. Push every commit right away. A piece of work that arrives finished in one
> commit does not count for the commit point.
> A red check after you push unfinished work is normal and costs you nothing. The lecture mark reads only your
> last push at the end of the lecture.
>
> - **Your first push must reach GitHub before 09:30.** Run the checker at the start of the lecture. Then
>   commit and push. If your first push reaches GitHub after 09:30, I check by hand which computer you used
>   for your lecture work. The reason does not matter, and coming late is no exception.
> - Commit and push when I call it. During the lecture, I say "commit and push now" at moments that
>   I choose. Then everyone must commit and push at once. Each push must reach GitHub within 5 minutes.

> ## You must write the AI log entirely yourself
>
> Write `week07/ai_log_07.md` yourself, in your own words. The Evidence block and the bold quotes from the
> answer of the assistant (§15) are the only exceptions. Do not use an assistant for anything else in the
> log. Do not use it to write the log, to "improve" the log, or to correct your English. **A log that an
> assistant wrote earns 0.** Your English is not graded. A person reads every log.

> ## Two files that you will write
>
> `week07/mobile_runs.json` records each test case that your tester ran on your phone. It also records
> what the tester saw. `week07/group_07.json` names your tester and the most useful thing that the
> tester found. Later, it also holds your decision. Type both files while the tester round happens. No
> assistant writes, corrects or completes either file.

> ## One server for the web and the phone
>
> The phone must call the same endpoints as your web page. It must send the same fields and the same
> token. Sometimes the phone shows that the server must change: a bug that the web page did not reveal, or
> something that the phone needs and the server does not give. Then change the server for both clients, in
> this order: first the `api.md` row with a line in the Change log that says what changes and why (a
> change request if a requirement or a test case changes), then the route and its test, in a commit of its
> own. The web page must keep working, and every test must stay green. A server change that the phone
> revealed, written down with its reason, is a good sign: it shows that you really tested your work on the
> phone. Never make a second, phone-only version of an endpoint. The login is the login of the course, as
> in Week 6. The phone must use your three login endpoints.

> ## Never force push
>
> `git push --force` deletes commits from your history. I read this history to grade your work. If CI turns
> red because of a ruff error or a typo, fix the error. Then push the fix as a new commit. A small fix
> never costs you anything.
> **A force push costs you the commit point of that week, whatever it changed.** This includes `git push -f`,
> `git push --force-with-lease`, "Force Push" in VS Code and the "Force push origin" button of GitHub Desktop.

> Have these ready: You need the package name of S2, which is in `week04/store.json`. You also need your
> three login endpoints, which are in `server/login_contract.json`. If your phone belongs to the other platform,
> use the emulator or the simulator (`AI_PLATFORMS_AND_STORES` §3). An iPhone with Kotlin is one example,
> and an Android phone with Swift is another.

---

## What arrives with this week

- The folder `week07/` contains this assignment, `ai_log_07.md`, `group_07.json` and `mobile_runs.json`.
  `group_07.json` will contain your tester. `mobile_runs.json` will contain your test cases on the phone.
- The file `server/course_login.py` is updated. Only its comments changed: the e-mail examples now end in
  `.edu.tr`. This file belongs to the course; do not change it. When you run the checker, the checker downloads
  the new version of the file into your repository and writes it over the old one. You need to do nothing
  else; commit the changed file with your first commit.

Your Python packages do not change, and `week06/requirements.txt` stays. Your framework brings its own
packages into `mobile/`.

---

## Where an assistant helps this week, and where it does not

| The work | The assistant |
|---|---|
| Create the app in `mobile/`. Read an error of the build, the emulator or the network. | The assistant helps. |
| Write the code of one screen. The prompt must hold the requirement, its acceptance criterion, its `api.md` rows and its web page. Each screen must get its own commit. | The assistant helps. |
| Make one change to code that you already have. Read the change line by line before you accept it (§15). | The assistant helps. The approval is yours. |
| Choose what a screen does when the requirement does not say it. | The assistant does not help. The requirement decides. If the requirement says nothing, change the requirement first (Week 6 §9). |
| Ask for a new endpoint, or for a different answer of the server, only for the phone. | The assistant does not help. The server stays the same. A new need is a new row of `api.md`. |
| Write `week07/mobile_runs.json` and `week07/group_07.json`. | The assistant does not help. |
| Write the lines of the Change log and the change requests. | The assistant does not help. |
| Write `ai_log_07.md`, outside its Evidence block and its bold quotes. | The assistant does not help. |

---

## In the lecture: push by 11:45

The lecture has five parts:

1. Make the first push, and read "The week in five minutes". This part ends at about 09:30.
2. Create your app in `mobile/`, and run it. This part ends at about 10:00.
3. Make the login work on the phone. This part ends at about 10:45.
4. Make the screen of the requirement that you built first in Week 6. This part ends at about 11:15.
5. Do the tester round with a classmate. This part ends at 11:45.

In every part, commit and push while the work is still unfinished. Commit and push again when the piece
works.

### 1. The first push, before 09:30

Do this at the start of the lecture.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week07: course files"
git push
```

The checker brings `week07/`. This push shows that your lecture work starts on your own computer. Before this push, run `git config user.name` and `git config user.email`. They must show your own name and the e-mail of your GitHub account. A commit under another person's name or e-mail does not count as your work.

### 2. Your app in `mobile/`

Do this in the lecture, until about 10:00.

Create the app with the tool of your framework. Create it in a folder named `mobile` at the root of your
repository, next to `server/` and `web/`. The section "Your repository, folder by folder" of
`AI_README_EN.md` shows this place. Give the app the package name of S2 as its id. The table uses
`com.example.studyroom` as its example.

| Framework | How you create the app (in the root of your repository) | Where its id comes from |
|---|---|---|
| Flutter | Run `flutter create --org com.example --project-name studyroom mobile`. | Flutter makes the id from `--org` and `--project-name`. |
| React Native–Expo | Run `npx create-expo-app@latest mobile`. | Write the id in `app.json`, in `"android": {"package": …}` and in `"ios": {"bundleIdentifier": …}`. |
| Kotlin (Android Studio) | Choose New Project → Empty Activity. Set Save location to the `mobile` folder of your repository. | Write the id in Package name on the same page. |
| Swift (Xcode, only on a Mac) | Choose New Project → App (SwiftUI). Save the project in the `mobile` folder of your repository. | Write `com.example` in Organization Identifier and `studyroom` in Product Name. Xcode then shows `com.example.studyroom` as the Bundle Identifier. |

Run the new app on your phone or on the emulator before you change anything:

- With Flutter, run `flutter run`.
- With Expo, run `npx expo start`. Then scan the QR code with Expo Go, or press `a` for the Android
  emulator.
- With Kotlin or Swift, press the Run button of Android Studio or Xcode.

Commit and push when the app runs. If you have no Mac, you do not need an iOS build; the Android emulator or
an Android phone is enough.

**Never commit the build files.** Your framework writes large folders that it can build again:
`node_modules/`, `build/`, `.dart_tool/`, `.gradle/`, `Pods/` and `.expo/`. The tool of your framework
usually puts a `.gitignore` file into `mobile/`, and this file lists these folders. Before the first
commit, run `git status` and check that none of these folders appears. If one of them appears, add it to
`mobile/.gitignore`.

### 3. The login on the phone

Do this in the lecture, until about 10:45.

First, the phone must reach your server. Start the server so that other devices can reach it:

```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

| Where the app runs | The address of your server in the app |
|---|---|
| The Android emulator | `http://10.0.2.2:8000` |
| The iOS simulator (on a Mac) | `http://127.0.0.1:8000` |
| A real phone on the same Wi-Fi as your laptop | Use `http://`, then the address of your laptop, then `:8000`. On Windows, `ipconfig` shows the address as IPv4 Address. On macOS, `ipconfig getifaddr en0` shows it. |

- Put the address in one place in your app, as a constant. Then a new network needs a change in only
  one line.
- Windows asks whether Python can use the network. Allow it for private networks.
- Test the address first in the browser of the phone. Open `http://<the address>:8000/docs` there. If
  the browser of the phone does not open this page, the app cannot reach the server either.
- Some Wi-Fi networks do not let a phone reach a laptop. The campus network can be one of them. On such a
  network, turn on the hotspot of your phone and connect your laptop to it. You can also use the emulator.

Second, the app must be allowed to use plain http:

| Framework | What you add |
|---|---|
| Flutter or Kotlin, on Android | Add `<uses-permission android:name="android.permission.INTERNET"/>` to `AndroidManifest.xml`. Also add `android:usesCleartextTraffic="true"` to `<application>`. In Flutter, the file is `android/app/src/main/AndroidManifest.xml`. |
| Flutter or Swift, on iOS | In `Info.plist`, set `NSAppTransportSecurity` → `NSAllowsLocalNetworking` to YES. |
| Expo Go | You add nothing. |

Then make the login screen. The login screen must do what your `web/login.html` does. It must ask for
the e-mail and send a request to your request_code endpoint. Then it must ask for the code, send a request
to your login endpoint and keep the token. Keep the token in memory, in a variable of your app. After a restart, the user logs in again, and
this is fine for now. In the lecture, start the server with `AIASD_CODE_FILE` set, as in Week 6. The server then writes the code into that file on your laptop. Type the code on the phone yourself.

The source file of the screen must name the requirements that it serves, in a comment:
`// serves: REQ-001, REQ-006`. Write the path of each endpoint as `api.md` writes it, with its `/`, such as `/auth/code`. Write the paths in the
code of the screen or in your helper.

The following code is a small helper in Flutter. Add its package first with `flutter pub add http`.

```dart
// mobile/lib/api.dart
import 'dart:convert';

import 'package:http/http.dart' as http;

const server = 'http://10.0.2.2:8000'; // the Android emulator; a real phone: your laptop's address
String? token; // in memory: log in again after a restart

Future<http.Response> call(String method, String path, [Map<String, dynamic>? body]) {
  final uri = Uri.parse('$server$path');
  final headers = {
    'Content-Type': 'application/json',
    if (token != null) 'Authorization': 'Bearer $token',
  };
  return method == 'POST'
      ? http.post(uri, headers: headers, body: jsonEncode(body ?? {}))
      : http.get(uri, headers: headers);
}
```

The following code is the same helper in React Native–Expo. Expo already has `fetch`.

```javascript
// mobile/api.js
export const SERVER = "http://192.168.1.23:8000"; // your laptop's address on the same Wi-Fi
let token = null;
export const setToken = (t) => { token = t; };

export async function api(method, path, body) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(SERVER + path, {
    method, headers, body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { status: response.status, data: await response.json().catch(() => ({})) };
}
```

Kotlin and Swift do the same with their own tools. Kotlin uses `HttpURLConnection` or OkHttp, and Swift
uses `URLSession`.

- A wrong code gets 401. Then the screen must show "Wrong code", as your web page does.
- After the login, the screen must show the address of the logged-in user. Send a request with the token to your "me"
  endpoint to get this address.

When the phone shows the logged-in address, take a screenshot on the phone or of the emulator. Save it as
`week07/phone_login.png` or as a `.jpg` file. Then commit and push.

### 4. The screen of your first requirement

Do this in the lecture, until about 11:15.

Take the requirement that you built first in Week 6. Make its screen on the phone. The screen must have the same fields and buttons as its web page, and it
must send its requests to the same endpoints.

```dart
// mobile/lib/book_screen.dart
// serves: REQ-002
final response = await call('POST', '/bookings', {'room': 3, 'start': '14:00', 'minutes': 60});
setState(() => message = response.statusCode == 201
    ? 'Booked.'
    : jsonDecode(response.body)['detail'] as String);
```

- The screen must show the refusals of the server in the words of your test cases, as the web page does.
- A 401 must send the user back to the login screen.
- The server decides, and the app only shows. If only the app checks a rule, nobody checks it, because
  a user can call your server without the app.
- The screen must follow your design, which is the screen of your prototype, on the width of a phone.

### 5. The tester round: `week07/mobile_runs.json`

Do this in the lecture, from about 11:15 to 11:45.

Your group from Week 3 meets again. Each of you becomes the tester of one groupmate. The app of the
owner runs on the phone or on the emulator of the owner. The tester must use the app like a user. The tester must run the test cases of the owner from
`week04/test_cases.json`:

- The tester must run at least three test cases, and at least one of them must be outside the login.
- The owner must watch and must not help.

Right after the turn, the owner must type each run into `week07/mobile_runs.json` by hand:

- `tc` is the id of the test case, and `tester` is the 9-digit number of the tester.
- `device` names the phone or the emulator, such as "Samsung A52, Android 14" or "Pixel 7 emulator".
- `round` is 1, and `result` is `pass`, `fail` or `blocked`.
- `note` must say in one full sentence what the tester saw. A `fail` run or a `blocked` run must have a note.

Then change roles. If nobody from your group is in the lecture, work with any classmate. The tester uses
your phone or your laptop only to test. Nobody commits on the computer of a classmate.

Your tester must be in the lecture with you. A tester who was not in the lecture counts as no tester and gets
no bonus. Push round 1 in the lecture: a round 1 that first reaches GitHub after the lecture counts as missing.
A tester round that you miss with the lecture cannot be made up.

### 6. Your tester: `week07/group_07.json`

Do this in the lecture, right after the tester round.

Write one entry. The entry must hold the number of your tester and the role `"tester"`. In `what`, quote the
most useful thing that the tester found or said, in one full sentence. `accepted` and `why` wait until
Saturday (§11).

### 7. Push, and check the result on GitHub

Run `ruff check . --fix` and `ruff format .` before you push. Ruff reads only the Python files, so the
files of your app do not change its result.

```bash
python .github/check_deliverables.py
git add .
git commit -m "week07: tester round, mobile_runs.json"
git push
```

Open the Actions tab. The checks of Week 7 run there, and the tests of your server run there too. If a run
does not start and GitHub shows a message about billing or a spending limit, open
https://github.com/settings/billing and clear it. A run that never starts gives no test results.

Commit each piece of work in the middle, and commit it again when it works. Push every commit right away.
Push your last commit by 11:45. The lecture mark reads the last commit that you pushed by the end of the
lecture.

---

## By Saturday 23:59

### 8. Every functional must requirement must be complete

In the lecture, you did this for the login screen and for one more requirement. Now complete the work so that it covers all of your functional `must` requirements. Each requirement needs the following:

- The requirement must have a screen in `mobile/`. The source file of the screen must name the requirement in `// serves: REQ-…`.
- The screen must send requests to the endpoints of the requirement in `api.md`.
- The screen must show the answers and the refusals of the server, as the web page does.

One screen can serve several requirements. The `should` and `could` requirements can be completed next week.

Some parts do not work on the web and work only on a phone, such as the camera, notifications and the location. If a functional `must` requirement of yours needs one of them, develop that part on the phone this week. The server side has been ready since Week 6.

### 9. Every requirement must be tested on the phone

Add new runs to `week07/mobile_runs.json` until at least one test case of every functional `must` requirement gets a `pass` on the phone. After the lecture, run the test cases yourself or with your tester, online or in person. If you run them yourself, write your own number in `tester`.

- Every run after the lecture must have `round` 2.
- Every test case that failed in round 1 must run again in round 2, after the fix. You can also drop a test case with a change request (Week 6 §9).

### 10. The app id is your S2 package

The id of your app must be the package name in S2 of `week04/store.json`. The id is used in these places:

- In Flutter, the id is `applicationId` in `android/app/build.gradle(.kts)`.
- In Kotlin, the id is `applicationId` in `app/build.gradle(.kts)`.
- In Expo, the id is `android.package` and `ios.bundleIdentifier` in `app.json`.
- In Xcode, the id is `PRODUCT_BUNDLE_IDENTIFIER`.

Your first build goes to the store with this id in Week 8. After that, the id can never change.

### 11. The findings of the tester: your decision

Add `accepted` and `why` to `group_07.json`. If you change something because of the finding, set `accepted` to `true`. If you change nothing, set it to `false`. Write one full sentence in `why`. This sentence will contain what you changed, or why the finding was not a real problem. A change to a requirement or to a test case is a change request (Week 6 §9).

### 12. Build folders must not be committed to the repository

`git ls-files mobile` must not list `node_modules/`, `build/`, `.dart_tool/`, `.gradle/`, `Pods/` or `.expo/`. If you committed one of them, add it to `mobile/.gitignore`. Then run `git rm -r --cached mobile/<the folder>`, commit and push. The files stay on your computer.

### 13. The server and the web must stay green

While you develop the mobile app, never change the server side in a way that breaks a test. All ten course tests must stay green in GitHub Actions. The tests of every `must` test case with `"run": "server"` must stay green too. Your pages in `web/` must keep working. Never change `.github/workflows/check.yml` or `.github/check_deliverables.py`: a run of a changed workflow never counts for the marks.

### 14. How each new test case must be run

A new test case for the phone must come with a change request. Its `"run"` must be `"manual"`, because a person runs this test case on a phone.

### 15. Small diffs: `week07/ai_log_07.md`

The technique of this week is small diffs (`AI_Doc5` §6). Choose one change to your mobile client. Here are three examples. The screen shows the 409 message of the server. The app sends the user back to the login after a 401. The app keeps the address of the server in one constant.

1. Ask the assistant for only this change. Give it the file, and say exactly what must change.
2. Read all of the diff before you accept it, and read the lines that you did not ask for in the same way. `git diff` shows the diff.
3. Keep the part that you asked for. Refuse every other change, even a good one.
4. Commit the accepted change on its own, with a message that names it. Write the commit id in the log. The first 7 characters of the id are enough.
5. Run the screen on the phone, and show that the change works.

In the log, write the change that you asked for and the change that you received. Write what you refused, and why. Write the commit. Paste `ME:`, `AI:` and `TERMINAL:` into the Evidence block. The `TERMINAL:` part holds the `git diff`, untouched.

You must write the AI log yourself. Outside the Evidence block and the bold quotes, do not use an assistant. **A log that an assistant wrote earns 0.**

### 16. Push again, with green checks

Make several commits as you work. **Each commit must add at most one new screen to `mobile/` and at most one new route to `server/`. A commit that adds two or more costs you the commit point of that week.** A screen is new in the commit where its file first gets its `// serves:` line, so the files that the tool of your framework creates do not count until then. A screen or a route that you only move, or whose code you change, is not new. The checker warns you when a commit, or your changes that are not committed yet, add two or more. Outside the lecture, push at least two commits with new work, at least one hour apart. A commit that a coding agent made never counts. Never force push, and never let an assistant do it. Then go through the checklist below.

---

## Deliverables checklist

In the lecture, pushed by 11:45
- [ ] Your first push must reach GitHub before 09:30.
- [ ] `mobile/` must hold your app, made with Flutter, React Native–Expo, Kotlin or Swift. Git must hold no build files.
- [ ] A login screen must have `// serves: REQ-001`, and the screen must send requests to your three login endpoints. `week07/phone_login.png` must show the logged-in address.
- [ ] The screen of one of your own functional `must` requirements must have its `// serves:` line, and the screen must send requests to its endpoints.
- [ ] `week07/mobile_runs.json` must have at least three runs by your tester in round 1, and one of them must be outside the login. You must write the file yourself.
- [ ] `week07/group_07.json` must contain your tester. The file must hold the number, the role `tester` and the finding.

By Saturday 23:59
- [ ] Every functional `must` requirement must have a screen in `mobile/` with `// serves:`, and the screen must send requests to its endpoints.
- [ ] Every functional `must` requirement must have a test case with a `pass` on the phone. Every failure of round 1 must run again in round 2.
- [ ] The app id must be the package of S2 in `week04/store.json`.
- [ ] `week07/group_07.json` must have `accepted` and `why`.
- [ ] Git must hold no build files.
- [ ] All ten course tests and every `must` test with `"run": "server"` must be green on GitHub.
- [ ] `week07/ai_log_07.md` must name the change that you asked for, the diff that you received, what you refused and the commit. Its Evidence block must hold `ME:`, `AI:` and `TERMINAL:`.
- [ ] The checks must be green on GitHub.

---

## How this week is graded

Your work in the lecture will be graded out of 5 points. I will read the last commit that you pushed by the end of the lecture, and I will check the following:

- Your app must be in `mobile/`.
- The login screen must send requests to your three login endpoints, and `phone_login.png` must show the logged-in address.
- The screen of your first requirement must send requests to its endpoints.
- `mobile_runs.json` must hold the runs of your tester, and `group_07.json` must hold the details of your tester.

Your work before Saturday 23:59 will be graded out of 5 points. I read the last commit that reached GitHub by 23:59. GitHub's push time counts, not the time on a commit.

- Green checks will earn you 2 points.
- Successful documents made with human involvement will earn 2 points. For this, you must fill in `ai_log_07.md` properly. You must also write `mobile_runs.json` and `group_07.json` by hand. Remember that these files earn 0 if an assistant made them.
- Commit discipline will be graded with 1 point.

The contributors' bonus. Your tester will get a bonus of 10% of your mark for the week.

**In the lecture, use your own computer.** You must do all of your lecture work on your own computer and with your own GitHub account. Otherwise, you will get zero for the lecture work, and, depending on what you did, your work can also be treated as cheating.
