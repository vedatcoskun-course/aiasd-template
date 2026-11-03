# Week 7 — AI log

<!--
A HUMAN WRITES THE AI LOG, WITH NO EXCEPTIONS.
AI LOG'U İNSAN YAZAR, İSTİSNASIZ.

Write this file yourself, in your own words. The Evidence block and the bold quotes are the only
exceptions. Do not use an assistant to write the log, to "improve" it, or to correct its language. A log
that an assistant wrote earns 0. Your English or Turkish is not graded. A person reads the log.

Bu dosyayı kendiniz, kendi cümlelerinizle yazın. Evidence bloğu ve kalın alıntılar tek istisnadır.
Asistanı günlüğü yazmak, "düzeltmek" ya da dilini düzeltmek için kullanmayın. Asistanın yazdığı bir
günlük 0 puan alır. İngilizceniz ya da Türkçeniz notlanmaz. Günlüğü bir insan okur.

The log has two kinds of words, as in Weeks 4 to 6. Your own words are plain text. The words of the
assistant are **bold**. Use bold only where the words must come from the assistant: one line of its diff,
or one sentence of its answer, that you point at. Each bold phrase also appears in the Evidence block,
letter for letter. Do not use bold for anything else.

Günlükte, 4–6. haftalardaki gibi, iki tür söz vardır. Sizin sözleriniz düz yazıdır. Asistanın sözleri
**kalındır**. Kalın yazıyı yalnızca sözlerin asistandan gelmesi gereken yerde kullanın: işaret ettiğiniz,
diff'inden tek bir satır ya da cevabından tek bir cümle. Her kalın ifade, harfi harfine aynı biçimde,
Evidence bloğunda da bulunur. Kalın yazıyı başka hiçbir şey için kullanmayın.

This week's task is small diffs (AI_Doc5 §6) on your mobile client. ASSIGNMENT_07 §15 gives the steps.
1. Choose ONE change to your mobile client. Here are three examples. A screen shows the 409 message of
   the server. The app sends the user back to the login after a 401. The app keeps the address of the
   server in one constant.
2. Give the assistant the file, and ask for exactly this change and nothing else.
3. Before you accept anything, read ALL of the diff (git diff). Read also the lines that you did not
   ask for.
4. Keep the part that you asked for. Refuse every other change, even a good one.
5. Commit the accepted change on its own, with a message that names it. Write its commit id below.
   The first 7 characters of the id are enough.
6. Run the screen on the phone, and show that the change works.

A WEAK log says: "I asked the assistant to improve my booking screen. The new code was better, so I
accepted it."
A STRONG log says: "I asked for one change in book_screen.dart: after a 401, go back to the login screen. The diff
         did that, but it also changed **const server = 'http://192.168.1.40:8000';** in api.dart, an
         address I did not ask for, and it renamed my variable message to statusText. I kept only the
         401 part and put api.dart back with git restore. Commit 4e1a9c2 changes six lines of
         book_screen.dart and nothing else. On the emulator I restarted the server, so my token was no
         longer valid, and pressed Book: the app went back to the login screen."

Delete this comment when you are done.
-->

## The change I asked for

[Name the assistant and the file that you gave it. Write the one change that you asked for, in one or two sentences.]

## The change I received

[Write what the diff changed. Name the lines that you asked for and every other line that it touched.]

## What I refused, and why

[Write each change that you did not keep, and why. If the diff had nothing extra, write how you checked it.]

## The commit, and the phone

[Write the commit id (its first 7 characters) and its message. Write how you showed on the phone that the change works.]

## Evidence — the exchange and the diff

```text
ME:
[prompt]

AI:
[answer]

TERMINAL:
[git diff]
<!-- ME: holds your prompt. AI: holds the answer of the assistant. TERMINAL: holds the commands that
     you typed and their output. It holds at least the git diff of the change before you accepted it.
     Paste the rounds of the exchange that show the change. You may leave out whole rounds that do
     not show it. Paste every ME:, AI: or TERMINAL: part that you keep whole, exactly as it came.
     Remove nothing, and correct nothing, not even the grammar. For several rounds, repeat ME: and
     AI:. -->
```
