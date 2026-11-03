#!/usr/bin/env python3
"""
Checks this week's deliverables — the same checks the instructor runs.

A run shows one week: the current one, or the week whose number you add. Under the
list, one line says how many checks of earlier weeks still fail, so a change that
breaks Week 1 does not pass silently in Week 7 — and the list does not grow by a
screenful every week. (The instructor's own capture still reads every week from 1 and
counts only the week it is marking.)

Which week is "current" is not yours to set. It is published by the course and
read from there on every run, so the checks you see are always the checks being
run against you. The CURRENT_WEEK_CACHE.txt file is only a cache of that number, refreshed
automatically, so this still works on a train with no signal.

Run it locally before you push:
    python .github/check_deliverables.py

To look at another week — say, to confirm Week 2 still passes:
    python .github/check_deliverables.py 2

Türkçe için sonuna `tr` ekle (her şey Türkçe yazılır; not hesabı aynı checker'la, İngilizce okunur):
    python .github/check_deliverables.py tr
    python .github/check_deliverables.py 2 tr
"""

from __future__ import annotations

import ast
import json
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Normally the repository this file sits in. AIASD_ROOT overrides it, which is
# how the self-update below keeps pointing at your repository while running a
# freshly downloaded copy of itself from a temporary file.
ROOT = (
    Path(os.environ["AIASD_ROOT"]).resolve()
    if os.environ.get("AIASD_ROOT")
    else Path(__file__).resolve().parent.parent
)

# A string the published checker must contain for us to trust and run it. If a
# proxy or a captive portal hands back an HTML error page, it will not have this.
MARKER = "AIASD-CHECKER-v1"  # AIASD-CHECKER-v1

PASS, FAIL = "PASS", "FAIL"
NOTYET = "NOT YET"   # VC, 21 Oct 2026: a check that has nothing to look at yet is listed, neither passed nor failed

# When a deliverable is due. Work that belongs in the lab, where you can still
# ask, is SESSION; work that is genuinely done alone afterwards — writing,
# diagrams, reflection — is DEADLINE.
#
# This is not cosmetic. Half the week's mark is taken at the end of the session,
# so checking for a diagram you were told to draw at home would mark everyone
# down for following the instructions.
SESSION, DEADLINE = "session", "deadline"

# One row per check: (week, what a pass says, PASS/FAIL, slot, what a failure says).
results: list[tuple[str, str, str, str, str]] = []


def check(week: int, name: str, ok: bool, detail: str = "", slot: str = SESSION) -> None:
    """`name` is the sentence shown when the check passes; `detail` is the sentence shown
    when it fails. Both are complete sentences with the file named in them, because
    each is printed alone on its line, after PASS or FAIL.

    A failure says what is needed, then 'Found: ...' with what is actually there, so a
    student who reads English slowly can still see both halves."""
    results.append((f"W{week}", name, PASS if ok else FAIL, slot, detail or name))


def later(week: int, name: str, why: str, slot: str = SESSION) -> None:
    """A check that cannot be judged yet (VC, 21 Oct 2026): listed with NOT YET and the reason, so the list is the same
    for everyone, but counted neither as passed nor as failed: the untouched starter earns no free ticks, and a
    number of checks that grows as the work grows does not confuse anyone."""
    results.append((f"W{week}", name, NOTYET, slot, why))


def pl(n: int, one: str, many: str | None = None) -> str:
    """The count with its noun in the right number: '1 entry', '3 entries'."""
    return f"{n} {one if n == 1 else (many or one + 's')}"


def read(path: str) -> str | None:
    p = ROOT / path
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None


def parses(path: str) -> bool:
    src = read(path)
    if src is None:
        return False
    try:
        ast.parse(src)
    except SyntaxError:
        return False
    return True


def ai_log_path(week: int) -> str:
    """Where this week's log lives.

    One file per week, inside the week's own folder, rather than one file at the
    root with twelve sections. A student's repository freezes the day they create
    it: a twelve-week scaffold written in Week 1 can never be changed afterwards,
    while a per-week file arrives with its week and can take whatever shape that
    week needs — including not existing, for a week that does not ask for one.
    """
    return f"week{week:02d}/ai_log_{week:02d}.md"


def ai_log_evidence(week: int) -> str:
    """The pasted exchange backing this week's claim — a fenced block with content.

    An untouched template block holds only an HTML comment, which is stripped here,
    so the placeholder does not count as evidence.
    """
    text = read(ai_log_path(week)) or ""
    blocks = re.findall(r"```[^\n]*\n(.*?)```", text, re.DOTALL)
    cleaned = [re.sub(r"<!--.*?-->", "", b, flags=re.DOTALL).strip() for b in blocks]
    return "\n".join(c for c in cleaned if c).strip()


def check_ai_log(week: int) -> None:
    """Every week: a filled-in reflection, and the exchange that backs it up.

    Due at the deadline, not at the end of the session: the honest version of
    this is written once the week's work has actually happened.
    """
    path = ai_log_path(week)
    check(
        week,
        f"{path} is filled in",
        len(ai_log_section(week)) > 80,
        f"{path} must be filled in, in your own words. Found: the section is empty or untouched.",
        DEADLINE,
    )
    evidence = ai_log_evidence(week)
    check(
        week,
        f"{path} holds the real conversation, pasted in the code block",
        len(evidence) >= 80,
        f"{path} must contain the real conversation, pasted inside the code block. "
        f"Found: {pl(len(evidence), 'character')} there.",
        DEADLINE,
    )


def ai_log_section(week: int) -> str:
    """What the student actually wrote in this week's log."""
    body = read(ai_log_path(week)) or ""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)  # evidence is checked apart
    # Drop the template's own headings and bold prompt labels — an untouched file
    # is then empty, which is what "not filled in" has to mean.
    body = re.sub(r"^\s*#.*$", "", body, flags=re.MULTILINE)
    # A line that is nothing but a bold label — with or without a colon — is the
    # template's own prompt, not an answer.
    body = re.sub(r"^\s*\*\*[^*]+\*\*:?\s*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^\s*>.*$", "", body, flags=re.MULTILINE)
    # A line that is only a [bracketed hint] is the scaffold's, not the student's.
    body = re.sub(r"^\s*(\d+\.\s*)?\[[^\]]*\]\s*$", "", body, flags=re.MULTILINE)
    return body.strip()


# ── per-week checks ──────────────────────────────────────────────────


def check_identity() -> None:
    """student.json — who you are. Nickname goes on the class board; the rest is
    for the official record and never leaves the instructor's machine."""
    raw = read("student.json")
    if raw is None:
        check(1, "student.json is in the repository root", False,
              "student.json is missing from the repository root. Restore it: it holds your student number and section.")
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        check(1, "student.json is valid JSON", False,
              f"student.json is not valid JSON ({exc}). Check the commas and the quotation marks.")
        return

    fields = ("student_id", "first_name", "last_name", "nickname", "section")
    missing = [f for f in fields if not str(data.get(f, "")).strip()]
    check(1, "student.json is fully filled in", not missing,
          f"student.json is not fully filled in. Empty fields: {', '.join(missing)}. Fill in every field.")
    if missing:
        return

    sid = str(data["student_id"]).strip()
    check(
        1,
        "student_id in student.json is a number",
        sid.isdigit() and len(sid) >= 5,
        f"student_id in student.json must be your student number, digits only. Found: {sid!r}.",
    )

    # One check, not three. Length and character set are the same requirement seen
    # from two angles, and a nickname that fails either fails for the same reason:
    # it cannot go on the board. Splitting it inflated a five-minute task into
    # three of the week's marks.
    nick = str(data["nickname"]).strip()
    usable = 2 <= len(nick) <= 20 and bool(re.fullmatch(r"[A-Za-z0-9_\-]+", nick))
    check(
        1,
        "nickname in student.json can go on the class board",
        usable,
        f"nickname in student.json must be 2-20 characters: letters, digits, - and _ only. Found: {nick!r}.",
    )

    section = str(data.get("section", "")).strip().lower()
    check(
        1,
        "section in student.json is 'en' or 'tr'",
        section in ("en", "tr"),
        f"section in student.json must be 'en' or 'tr'. Found: {section!r}. "
        "This is how your repository knows which week to check.",
    )


def week1() -> None:
    check_identity()
    proof = read("week01/setup_proof.md")
    check(
        1,
        "week01/setup_proof.md is there and long enough",
        bool(proof and len(proof) > 80),
        "week01/setup_proof.md is missing or too short. Create it and fill it in as the Week 1 assignment says.",
    )

    src = read("week01/hello.py")
    check(
        1,
        "week01/hello.py has no syntax error",
        parses("week01/hello.py"),
        "week01/hello.py is missing or has a syntax error. Create it, or run it to see the error.",
    )
    if src:
        try:
            tree = ast.parse(src)
        except SyntaxError:
            tree = None
        if tree is not None:
            nodes = list(ast.walk(tree))
            has_fstring = any(isinstance(n, ast.JoinedStr) for n in nodes)
            has_list = any(isinstance(n, (ast.List, ast.ListComp)) for n in nodes)
            has_for = any(isinstance(n, (ast.For, ast.comprehension)) for n in nodes)
            has_input = any(
                isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "input"
                for n in nodes
            )
            check(1, "week01/hello.py contains an f-string", has_fstring,
                  'week01/hello.py must contain an f-string, for example f"Hello {name}". Found: none.')
            check(1, "week01/hello.py contains a list", has_list,
                  'week01/hello.py must contain a list, for example names = ["Ada", "Alan"]. Found: none.')
            check(1, "week01/hello.py contains a for-loop", has_for,
                  "week01/hello.py must contain a for-loop, for example: for name in names: ... Found: none.")
            check(1, "week01/hello.py asks the user for input", has_input,
                  "week01/hello.py must ask the user for input with input(). Found: input() is never called.")

    notes = prose_words(read("week01/llm_notes.md") or "")
    check(
        1,
        "week01/llm_notes.md has about 300 words of your own",
        notes >= 250,
        f"week01/llm_notes.md must have about 300 words written by you. Found: {notes}. "
        "Headings, instructions and pasted blocks do not count.",
        DEADLINE,
    )

    gi = read(".gitignore") or ""
    check(
        1,
        ".gitignore covers .venv and .env",
        ".venv" in gi and ".env" in gi,
        ".gitignore must contain .venv and .env, so they are never committed. Add both lines.",
    )
    check(
        1,
        ".env.example is in the repository root",
        (ROOT / ".env.example").is_file(),
        ".env.example is missing. Create it with the NAMES of your settings only, never the secret values.",
    )
    check_ai_log(1)


PROPOSAL_SECTIONS = {  # number -> title start, as in the scaffold
    1: "Title", 2: "One-paragraph summary", 3: "Problem", 4: "Solution",
    5: "How it works", 6: "Technologies", 7: "Success criteria",
    8: "Market", 9: "Competitors", 10: "Comparison", 11: "Commercial potential",
    12: "Technical risks",
}


def proposal_sections() -> dict[int, dict]:
    """PROPOSAL.md split by its numbered `### N. Title (about L characters …)` headings.

    For each section: the character limit the heading declares, the prose under it
    (comments and fenced blocks removed) and whether a mermaid block sits under it.
    """
    text = read("PROPOSAL.md") or ""
    heads = list(re.finditer(r"^### (\d+)\. ([^(\n]+?)\s*\(about ([\d,]+) characters[^)]*\)", text, re.M))
    out: dict[int, dict] = {}
    for k, m in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else len(text)
        body = text[m.end():end]
        # the last section ends where the Change log begins - its lines are not §12's prose
        tail = re.search(r"^## Change log", body, re.M)
        if tail:
            body = body[:tail.start()]
        body = re.sub(r"^---\s*$|^## .*$", "", body, flags=re.M)  # part separators
        mermaid = any("%% EXAMPLE" not in blk for blk in re.findall(r"```mermaid\n(.*?)```", body, re.DOTALL))
        prose = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
        prose = re.sub(r"```.*?```", "", prose, flags=re.DOTALL)
        out[int(m.group(1))] = {
            "title": m.group(2).strip(),
            "limit": int(m.group(3).replace(",", "")),
            "chars": len(prose.strip()),
            "text": prose,
            "mermaid": mermaid,
        }
    return out


def check_proposal(week: int, numbers: range, slot: str) -> None:
    secs = proposal_sections()
    if not secs:
        check(week, "PROPOSAL.md is in the repository root with its headings", False,
              "PROPOSAL.md is missing, or its numbered headings were changed. Restore the headings from the template.", slot)
        return
    for n in numbers:
        sec = secs.get(n)
        label = f"PROPOSAL.md §{n} {PROPOSAL_SECTIONS.get(n, '')}".rstrip()
        if sec is None:
            check(week, f"{label} has its heading", False,
                  f"{label} has lost its heading, or the heading was changed. Restore the heading from the template.", slot)
            continue
        floor = 60 if n > 1 else 3
        if sec["chars"] < floor:
            check(week, f"{label} is written", False,
                  f"{label} is not written yet. Found: {pl(sec['chars'], 'character')}. Write your own text under that heading.", slot)
        else:
            # The length in the heading is an ideal, not a limit (decision of 30 Sep):
            # a longer section passes.
            check(week, f"{label} is written", True, "", slot)


def contributors(week: int) -> list[dict] | None:
    """The people who helped this week: weekNN/contributors_NN.json in Weeks 2-3; from Week 4
    the other members of the group in weekNN/group_NN.json, one file for both (6 Oct 2026)."""
    name, key = (f"group_{week:02d}.json", "members") if week >= 4 else (f"contributors_{week:02d}.json", "contributors")
    raw = read(f"week{week:02d}/{name}")
    if raw is None:
        return None
    try:
        data = json.loads(raw.lstrip("\ufeff"))
    except json.JSONDecodeError:
        return None
    items = data.get(key, data) if isinstance(data, dict) else data
    return items if isinstance(items, list) else None


def check_contributors(week: int, role: str, slot: str = SESSION) -> None:
    path = f"week{week:02d}/contributors_{week:02d}.json"
    items = contributors(week)
    if items is None:
        check(week, f"{path} is valid JSON", False,
              f"{path} is missing or is not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.", slot)
        return
    # Contributors are optional: none, one or two classmates (decided 4 Oct 2026). What
    # is listed must be real - a valid, distinct student number, the right role and a
    # sentence - but an empty list is a legitimate "I worked alone this week".
    # an untouched scaffold entry (no number, no sentence) is the same as no entry
    items = [i for i in items if isinstance(i, dict)
             and (str(i.get("student_id", "")).strip() or str(i.get("what", "")).strip())]
    ids = [str(i.get("student_id", "")).strip() for i in items]
    good_ids = [i for i in ids if re.fullmatch(r"\d{9}(-\d+)?", i)]
    check(week, f"{path} lists 0-2 classmates with valid numbers",
          len(ids) <= 2 and len(good_ids) == len(ids) and len(set(good_ids)) == len(good_ids),
          f"{path} may list at most two classmates, each with a valid 9-digit student number, all different. "
          f"Found: {pl(len(ids), 'entry', 'entries')}, {len(good_ids)} with a valid number.", slot)
    me = ""
    try:
        me = str(json.loads(read("student.json") or "{}").get("student_id", "")).strip()
    except json.JSONDecodeError:
        pass
    check(week, f"{path} does not list you", me == "" or me.split("-")[0] not in [g.split("-")[0] for g in good_ids],
          f"{path} must not list you. Your own student number is in it: remove that entry.", slot)
    roles_ok = all(str(i.get("role", "")).strip() == role for i in items if isinstance(i, dict))
    check(week, f"{path} gives everyone the role '{role}'", roles_ok,
          f"{path} must give everyone listed the role '{role}'. Found: a wrong or empty role.", slot)
    thin = [i for i in items if isinstance(i, dict) and len(str(i.get("what", "")).strip()) < 20]
    check(week, f"{path} says what each person did", not thin,
          f"{path} must say, for each person, what they did, in a real sentence. "
          f"Found: {pl(len(thin), 'entry', 'entries')} without one.", slot)


def week2() -> None:
    # In the lab: Part A of the proposal, two stakeholders, the first requirement list.
    check_proposal(2, range(1, 5), SESSION)
    check_contributors(2, "stakeholder", SESSION)

    raw = read("week02/requirements.json")
    ids: list[str] = []
    if raw is None:
        check(2, "week02/requirements.json is in the repository", False,
              "week02/requirements.json is missing. Run the checker online to fetch it, then fill it in.")
    else:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            check(2, "week02/requirements.json is valid JSON", False,
                  f"week02/requirements.json is not valid JSON ({exc}). Check the commas and the quotation marks.")
        else:
            items = data.get("requirements", data) if isinstance(data, dict) else data
            if not isinstance(items, list):
                items = []
            items = [i for i in items if isinstance(i, dict) and not i.get("dropped")]
            real = [i for i in items if str(i.get("description", "")).strip() not in ("", "…")]
            check(2, "week02/requirements.json has at least 8 filled-in requirements", len(real) >= 8,
                  f"week02/requirements.json needs at least 8 filled-in requirements. Found: {len(real)}.")
            ids = [str(i.get("id", "")).strip() for i in real]
            bad = [i for i in ids if not re.fullmatch(r"REQ-\d{3}", i)]
            dup = sorted({i for i in ids if ids.count(i) > 1})
            check(2, "every requirement id looks like REQ-001 and none is repeated", not bad and not dup and bool(ids),
                  "Every requirement id in week02/requirements.json must look like REQ-001, and none may be repeated. "
                  + ("Found: no requirements filled in yet." if not ids else f"Found: wrong ids {bad[:3]}, repeated ids {dup[:3]}."))
            f = sum(1 for i in real if i.get("functional") is True)
            nf = sum(1 for i in real if i.get("functional") is False)
            check(2, "week02/requirements.json has at least 5 functional and 3 non-functional requirements", f >= 5 and nf >= 3,
                  "week02/requirements.json needs at least 5 functional and 3 non-functional requirements. "
                  f"Found: {f} functional, {nf} non-functional.")
            phone = any(re.search(r"phone|mobile|390", str(i.get("description", "")), re.I)
                        for i in real if i.get("functional") is False)
            check(2, "the requirement about the phone screen is still there", phone,
                  "week02/requirements.json must keep a non-functional requirement about the phone screen. "
                  "Found: none that mentions it.")
            # By Saturday: every requirement prioritised and testable.
            prio = [str(i.get("priority", "")).strip().lower() for i in real]
            badp = [i.get("id") for i, pr in zip(real, prio) if pr not in ("must", "should", "could")]
            few = "Cannot pass yet: fewer than 8 requirements."
            check(2, "every requirement has a priority: must, should or could", len(real) >= 8 and not badp,
                  "Every requirement in week02/requirements.json must have a priority: must, should or could. "
                  + (few if len(real) < 8 else f"Found: missing or wrong in {badp[:4]}."), DEADLINE)
            check(2, "not every requirement is 'must'", len(real) >= 8 and any(pr in ("should", "could") for pr in prio),
                  "Not every requirement may be 'must': mark the ones that could be cut as should or could. "
                  + (few if len(real) < 8 else "Found: all of them are 'must'."), DEADLINE)
            thin = [i.get("id") for i in real if len(str(i.get("acceptance", "")).strip().strip("…")) < 25]
            check(2, "every requirement has an acceptance criterion", len(real) >= 8 and not thin,
                  "Every requirement must have an acceptance criterion, one sentence saying how to test it. "
                  + (few if len(real) < 8 else f"Found: missing or too short in {thin[:4]}."), DEADLINE)

    # By Saturday: the rest of Part A, the SRS, the log.
    check_proposal(2, range(5, 8), DEADLINE)
    secs = proposal_sections()
    s5 = secs.get(5, {})
    if s5:
        t = s5["text"].lower()
        check(2, "PROPOSAL.md §5 names mobile, web and server",
              all(k in t for k in ("mobile", "web", "server")),
              "PROPOSAL.md §5 must mention all three parts: mobile, web and server. Found: at least one is missing.", DEADLINE)
        check(2, "PROPOSAL.md §5 has its system context diagram", s5["mermaid"],
              "PROPOSAL.md §5 must contain the system context diagram, written as a ```mermaid block. Found: no such block.", DEADLINE)

    srs = read("week02/SRS.md") or ""
    prose = re.sub(r"<!--.*?-->", "", srs, flags=re.DOTALL)
    srs_filled = len(re.sub(r"```.*?```", "", prose, flags=re.DOTALL).strip()) > 600
    check(2, "week02/SRS.md is filled in", srs_filled,
          "week02/SRS.md must be filled in. Found: the file is missing, or it is still the template.", DEADLINE)
    blocks = [b for b in re.findall(r"```mermaid\n(.*?)```", prose, re.DOTALL) if "%% EXAMPLE" not in b]
    usecases = sum(len(re.findall(r"\(\[", b)) for b in blocks)
    check(2, "SRS.md has a use case diagram with at least 3 use cases", usecases >= 3,
          f"SRS.md must have a use case diagram with at least 3 use cases. Found: {usecases}.", DEADLINE)
    in_srs = set(re.findall(r"REQ-\d{3}", prose))
    # VC, 23 Oct 2026: requirements.json is the only place for the requirements. SRS §4 may be one line that
    # points to it instead of a copy of the list.
    s4 = re.search(r"(?ms)^##\s*4\b.*?(?=^##\s|\Z)", prose)
    # The starter already has the pointer line, so it counts only once the SRS itself is filled in.
    points = bool(srs_filled and s4 and "requirements.json" in s4.group(0))
    check(2, "SRS.md §4 points to requirements.json, or lists every REQ id", bool(ids) and (points or set(ids) <= in_srs),
          "SRS.md §4 must say that the requirements are in week02/requirements.json, or list every REQ id. "
          + ("Found: no requirements filled in yet." if not ids else f"Found: missing {', '.join(sorted(set(ids) - in_srs)[:4])}."), DEADLINE)
    check_ai_log(2)


def week3() -> None:
    """Pitch and review in the lab; Part B of the proposal and the hostile-reviewer log
    by Saturday. The pitch is read as it was pushed by the end of the lecture (11:45)."""
    # --- the pitch: six slides, each with the student's own words -----------------
    pitch = read("week03/PITCH_03.md")
    if pitch is None:
        check(3, "week03/PITCH_03.md is in the repository", False,
              "week03/PITCH_03.md is missing. Run the checker online to fetch it, then write it.")
    else:
        body = re.sub(r"<!--.*?-->", "", pitch, flags=re.DOTALL)
        slides = [x.strip() for x in re.split(r"^---\s*$", body, flags=re.M) if x.strip()]
        slides = [x for x in slides if not re.match(r"^marp:", x)]  # the front matter
        check(3, "PITCH_03.md has 7 slides", len(slides) == 7,
              f"PITCH_03.md must have 7 slides: your six and the fixed reviewers' slide. Found: {len(slides)}. "
              "Slides are separated by a line that contains only ---.")
        # not inside a drawing; an image ![alt](file) or a link [text](url) is not a hole
        holes = sum(len(re.findall(r"(?<!!)\[[^\]\n]{1,80}\](?!\()", re.sub(r"```.*?```", "", x, flags=re.DOTALL))) for x in slides[:6])
        check(3, "PITCH_03.md has no [bracketed] text left", holes == 0,
              f"PITCH_03.md still has {pl(holes, 'piece')} of [bracketed] text. Replace each one with your own words and "
              "delete the square brackets too: text left inside [ ] still counts as not filled in.")
        def slide(n):  # 1-based, after the title slide
            return slides[n] if len(slides) > n else ""
        check(3, "slide 2 tells the last time it happened", len(re.sub(r"\*\*[^*]+\*\*", "", slide(1)).strip()) > 120 and "[" not in slide(1),
              "Slide 2 must tell the last time this problem happened to you or in front of you: when, where, "
              "what you did instead, what it cost. Found: too short, or [brackets] left.")
        people = len([r for r in re.findall(r"^\|\s*\d\s*\|([^|\n]{3,})\|([^|\n]{3,})\|", slide(2), re.M) if "[" not in r[0] + r[1]])
        check(3, "slide 3 names five testers in its table", people >= 5,
              f"Slide 3 must list five testers, one name per row of its table. Found: {pl(people, 'filled-in row')}.")
        # slide 4: three requirements, the same id AND description as requirements.json
        reqs = {}
        try:
            rj = json.loads((read("week02/requirements.json") or "[]").lstrip("\ufeff"))
            for it in (rj.get("requirements", rj) if isinstance(rj, dict) else rj):
                if isinstance(it, dict) and it.get("id"):
                    reqs[str(it["id"]).strip()] = " ".join(str(it.get("description", "")).split()).lower()
        except json.JSONDecodeError:
            pass
        cited = re.findall(r"^\s*\d\.\s*(REQ-\d{3})\s*[—–-]+\s*(.+)$", slide(3), re.M)
        same = [rid for rid, desc in cited if rid in reqs and reqs[rid] and (
            " ".join(desc.split()).lower().rstrip(".") == reqs[rid].rstrip(".") or reqs[rid].rstrip(".") in " ".join(desc.split()).lower())]
        # VC, 23 Oct 2026: a requirement whose description changed later (a dated Change log line names
        # its id, e.g. a change request) still counts, so this Week 3 check does not fail for ever.
        prop = read("PROPOSAL.md") or ""
        mlog = re.search(r"^## Change log.*?$", prop, re.M)
        logtext = re.sub(r"<!--.*?-->", "", prop[mlog.end():], flags=re.DOTALL) if mlog else ""
        changed = set()
        for ln in logtext.splitlines():
            if not re.search(r"20\d\d-\d\d-\d\d", ln):
                continue
            changed |= set(re.findall(r"REQ-\d{3}", ln))
            for a, b in re.findall(r"REQ-(\d{3})\s*(?:to|\.\.|–|-)\s*REQ-(\d{3})", ln):
                changed |= {f"REQ-{k:03d}" for k in range(int(a), int(b) + 1)}
        same += [rid for rid, _ in cited if rid in reqs and rid in changed and rid not in same]
        check(3, "slide 4 lists three requirements copied from requirements.json", len(set(same)) >= 3,
              "Slide 4 must list three requirements copied word for word (id and description) from week02/requirements.json. "
              + (f"Found: {len(set(same))} of {len(cited)} listed match. Copy them, do not paraphrase."
                 if cited else "Found: none listed in the form: 1. REQ-001 — description."))
        dn = re.search(r"(does not|yapmaz)[ \t]*:?\**[ \t]*(.+)$", slide(3), re.I | re.M)  # one line only (24 Oct 2026)
        check(3, "slide 4 says what the app does not do", bool(dn and len(dn.group(2).strip()) > 15 and "[" not in dn.group(2)),
              'Slide 4 must say what the app does NOT do, in one sentence that starts with "It does not:" '
              '(in Turkish: "Yapmaz:"), the sentence from §4 of your proposal. Found: none.')
        def local_image(md: str) -> bool:
            """An image in the repository, linked from the slide. The link may be relative to
            week03/ (where PITCH_03.md is, so the preview shows it) or to the root (fixed 6 Oct 2026:
            only 'week03/...' counted, which the preview cannot show)."""
            srcs = re.findall(r"!\[[^\]]*\]\(\s*<?([^)>\s]+)", md)
            srcs += re.findall(r"<img[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", md, re.I)
            for src in srcs:
                src = urllib.parse.unquote(src.split("#")[0].split("?")[0]).strip()
                if not src or re.match(r"^[a-z][a-z0-9+.-]*:", src, re.I):
                    continue  # a web address is not a drawing of yours
                for base in (ROOT / "week03", ROOT):
                    f = (base / src.lstrip("/")).resolve()
                    if f.is_file() and ROOT.resolve() in f.parents:
                        return True
            return False
        img_ok = local_image(slide(4))
        boxes = len(re.findall(r"^\s*\+[-+=]+\+\s*$", slide(4), re.M)) >= 2
        check(3, "slide 5 shows the main screen", img_ok or boxes,
              "Slide 5 must show the main screen: link an image from your repository, or draw it with text lines like +-----+. "
              "Found: neither. If you linked an image, check that the file is committed and the path is right.")
        check(3, "slide 6 states one honest doubt", len(slide(5).strip()) > 60 and "[" not in slide(5),
              "Slide 6 must state one honest doubt: the question, and two lines on why you are unsure. "
              "Found: too short, or [brackets] left.")
    # --- the review: three reviewers, quoted sentences, a decision each -----------
    items = contributors(3) or []
    if not items:
        check(3, "week03/contributors_03.json is valid JSON", False,
              "week03/contributors_03.json is missing, empty or not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.")
    else:
        ids = [str(i.get("student_id", "")).strip() for i in items if isinstance(i, dict)]
        good = [i for i in ids if re.fullmatch(r"\d{9}(-\d+)?", i)]
        check(3, "contributors_03.json names three reviewers", len(good) == 3 and len(set(good)) == 3,
              "week03/contributors_03.json must name three different reviewers, each with a valid 9-digit student number. "
              f"Found: {pl(len(good), 'valid number')}.")
        me = ""
        try:
            me = str(json.loads(read("student.json") or "{}").get("student_id", "")).strip()
        except json.JSONDecodeError:
            pass
        # 24 Oct 2026: as in Week 4, these two are checked only once a reviewer is named; on the untouched file
        # (role already filled in, no number) they gave two free ticks.
        if good:
            check(3, "contributors_03.json does not list you", me == "" or me.split("-")[0] not in [g.split("-")[0] for g in good],
                  "week03/contributors_03.json must not list you. Your own student number is in it: remove that entry.")
            check(3, "contributors_03.json gives every reviewer the role 'reviewer'", all(str(i.get("role", "")).strip() == "reviewer" for i in items if isinstance(i, dict)),
                  "week03/contributors_03.json must give every reviewer the role 'reviewer'. Found: a wrong or empty role.")
        else:
            why = "It is checked once the file names your reviewers' student numbers."
            later(3, "contributors_03.json does not list you", why)
            later(3, "contributors_03.json gives every reviewer the role 'reviewer'", why)
        thin = [i for i in items if isinstance(i, dict) and len(str(i.get("what", "")).strip()) < 25]
        check(3, "contributors_03.json quotes what each reviewer said", not thin,
              f"week03/contributors_03.json must quote, for each reviewer, a real sentence they said. Found: {pl(len(thin), 'entry', 'entries')} without one.")
        undecided = [i for i in items if isinstance(i, dict) and (i.get("accepted") not in (True, False) or len(str(i.get("why", "")).strip()) < 15)]
        check(3, "contributors_03.json gives a decision and a reason for each reviewer", not undecided,
              "week03/contributors_03.json must say, for each reviewer, whether you accepted the comment (accepted: true or false) and why. "
              f"Found: {pl(len(undecided), 'entry', 'entries')} without a decision and a reason.")
    # --- Part A revised: the change log has started --------------------------------
    text = read("PROPOSAL.md") or ""
    m = re.search(r"^## Change log.*?$", text, re.M)
    log = re.sub(r"<!--.*?-->", "", text[m.end():], flags=re.DOTALL) if m else ""
    dated = re.findall(r"20\d\d-\d\d-\d\d", log)
    check(3, "PROPOSAL.md change log has a dated line", len(dated) >= 1,
          'PROPOSAL.md change log must have a dated line added after the review, like "2026-10-07 — §N: what you changed". Found: none.')
    # --- the group: the same list in every member's repository (added 5 Oct 2026). Whether
    # the lists of the members agree can only be seen across repositories, so that part is
    # the instructor's (grade.py groups); here: a list that can be right, and reviewers in it.
    gdata = load_json("week03/group_03.json")
    glist = gdata.get("group") if isinstance(gdata, dict) else None
    if not isinstance(glist, list):
        check(3, "week03/group_03.json is valid JSON", False,
              "week03/group_03.json is missing or is not valid JSON. Run the checker online to fetch it.")
    else:
        nums = [str(x).strip().split("-")[0] for x in glist if str(x).strip()]
        valid = [n for n in nums if re.fullmatch(r"\d{9}", n)]
        me = my_number()
        check(3, "group_03.json lists your group: 4 or 5 different numbers, yours included",
              len(valid) == len(nums) and len(set(valid)) == len(valid) and len(valid) in (4, 5) and (me == "" or me in valid),
              "week03/group_03.json must list your group: 4 or 5 different 9-digit student numbers, yours included. "
              f"Found: {pl(len(valid), 'valid number')} of {len(nums)}" + (". Your own number is missing." if me not in valid else "."))
        reviewers = [str(i.get("student_id", "")).strip().split("-")[0] for i in (contributors(3) or []) if isinstance(i, dict)]
        reviewers = [r for r in reviewers if re.fullmatch(r"\d{9}", r)]  # empty entries are not reviewers (6 Oct 2026)
        outside = [r for r in reviewers if r not in valid]
        check(3, "your three reviewers are members of your group", bool(reviewers) and not outside,
              f"Your reviewers must be members of your group (week03/group_03.json). Found: not in group_03.json: {outside[:3]}."
              if outside else
              "Your three reviewers must be members of your group (week03/group_03.json). Found: no reviewers in contributors_03.json yet.")
    # --- the main flow: the screens the Week 4 prototype is built from (added 5 Oct 2026;
    # the project is fixed at this push, and a project that cannot name its screens is not)
    sc = read("week03/screens_03.md")
    if sc is None:
        check(3, "week03/screens_03.md is in the repository", False,
              "week03/screens_03.md is missing. Run the checker online to fetch it, then fill it in.")
    else:
        body = re.sub(r"<!--.*?-->", "", sc, flags=re.DOTALL)
        rows = re.findall(r"^\|\s*\d+\s*\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\|\s*$", body, re.M)
        filled = [r for r in rows if "[" not in "".join(r) and r[0].strip()
                  and len(r[1].strip()) >= 5 and re.search(r"REQ-\d{3}", r[2])]
        check(3, "screens_03.md lists at least five screens of the main flow", len(filled) >= 5,
              "week03/screens_03.md must list at least five screens of the main flow, each with a name, what the user does there, and REQ ids. "
              f"Found: {len(filled)}.")
        unknown = sorted({rid for r in filled for rid in re.findall(r"REQ-\d{3}", r[2])} - set(requirement_index()))
        check(3, "screens_03.md names only requirements that exist in requirements.json", bool(filled) and not unknown,
              "week03/screens_03.md may name only requirements that exist in week02/requirements.json. "
              + (f"Found: not in that file: {unknown[:4]}." if unknown else "Found: no filled-in screens yet."))
    # --- Saturday: Part B, the store, the log ---------------------------------------
    check_proposal(3, range(8, 13), DEADLINE)
    s12 = (proposal_sections().get(12) or {}).get("text", "").lower()
    check(3, "PROPOSAL.md §12 names the store", any(k in s12 for k in ("google play", "app store", "appgallery", "galaxy store", "testflight", "play store")),
          "PROPOSAL.md §12 must name the store (S0), its fee and how long its review takes. Found: no store named.", DEADLINE)
    log3 = read("week03/ai_log_03.md") or ""
    prose = re.sub(r"<!--.*?-->|```.*?```", "", log3, flags=re.DOTALL)
    objections = len([m for m in re.findall(r"^\s*[123]\.\s+(\S.{2,})$", prose, re.M) if not m.startswith("[")])
    check(3, "week03/ai_log_03.md lists three numbered objections", objections >= 3,
          f"week03/ai_log_03.md must list the three objections the assistant gave you, numbered 1. 2. 3. Found: {objections}.", DEADLINE)
    check_ai_log(3)


# ── Week 4: clickable prototype, test cases, walk-through ────────────

WEEK4_FROM = "2026-10-12"  # the Monday of Week 4: the walk-through's Change log lines are dated from here
RUN_WEEK = 0  # the last week this run checks; main() sets it
STORES = {  # the name in store.json -> words that name the same store in PROPOSAL.md §12
    "google play": ("google play", "play store"),
    "huawei appgallery": ("appgallery", "huawei"),
    "samsung galaxy store": ("galaxy store", "samsung"),
    "apple app store": ("app store", "apple", "testflight"),
}


def load_json(path: str):
    raw = read(path)
    if raw is None:
        return None
    try:
        return json.loads(raw.lstrip("﻿"))
    except json.JSONDecodeError:
        return None


def filled(value) -> str:
    """The text of a field, or "" if it is empty or still the scaffold's '…'."""
    text = str(value if value is not None else "").strip()
    return "" if text.strip(".…") == "" else text


def my_number() -> str:
    data = load_json("student.json")
    return str(data.get("student_id", "")).strip().split("-")[0] if isinstance(data, dict) else ""


def requirement_index() -> dict[str, dict]:
    """week02/requirements.json by id, dropped requirements included."""
    data = load_json("week02/requirements.json")
    items = data.get("requirements", data) if isinstance(data, dict) else data
    out: dict[str, dict] = {}
    for it in items if isinstance(items, list) else []:
        rid = str(it.get("id", "")).strip() if isinstance(it, dict) else ""
        if re.fullmatch(r"REQ-\d{3}", rid):
            out[rid] = it
    return out


def test_cases() -> list[dict] | None:
    data = load_json("week04/test_cases.json")
    items = data.get("test_cases", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return None
    # an untouched scaffold entry (all '…') is the same as no entry
    return [t for t in items if isinstance(t, dict)
            and (filled(t.get("title")) or filled(t.get("expected")))]


def prototype_screens() -> dict[str, str]:
    """week04/prototype/*.html by file name."""
    folder = ROOT / "week04" / "prototype"
    if not folder.is_dir():
        return {}
    return {p.name: p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(folder.glob("*.html")) if p.is_file()}


def screen_links(html: str) -> set[str]:
    """Every screen a page leads to: an href, a form action or a quoted name in a script."""
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.DOTALL)  # a commented-out link is not a link
    names = re.findall(r"""["']\s*(?:\./)?([\w.\-]+\.html)(?:[?#][^"']*)?\s*["']""", html)
    return {n for n in names if not n.lower().startswith(("http", "www"))}


def visible_text(html: str) -> str:
    html = re.sub(r"<!--.*?-->|<script.*?</script>|<style.*?</style>", " ", html, flags=re.DOTALL | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def serves(html: str) -> list[str]:
    m = re.search(r"<!--\s*serves:(.*?)-->", html, re.DOTALL | re.I)
    if not m or "[" in m.group(1):  # the starter's [placeholder] names nothing yet
        return []
    return re.findall(r"REQ-\d{3}", m.group(1))


def round_of(run: dict) -> int:
    """The walk-through round of a run: 1 unless it says 2 (as 2, "2", 2.0 or "round 2")."""
    m = re.search(r"\d+", str(run.get("round", "1")))
    return int(m.group()) if m else 1


def check_collaborator(week: int, role: str, slot: str = SESSION, who: str = "collaborator") -> list[str]:
    """Your collaborator in weekNN/group_NN.json: one classmate of your choice, from any group, who runs
    your test cases on your prototype (VC, 11 Oct 2026; before that the file held the other members of the
    group, 6 Oct). The file keeps its name and its "members" list, with exactly one entry; returns their number.
    who: how the messages call them ("tester" in Week 7)."""
    path = f"week{week:02d}/group_{week:02d}.json"
    your = "your tester" if who == "tester" else "your collaborator"
    items = contributors(week)
    if items is None:
        check(week, f"{path} is valid JSON", False,
              f"{path} is missing or is not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.", slot)
        return []
    items = [i for i in items if isinstance(i, dict)]
    ids = [str(i.get("student_id", "")).strip() for i in items]
    good = [i for i in ids if re.fullmatch(r"\d{9}(-\d+)?", i)]
    check(week, f"{path} names {your}", len(items) == 1 and len(good) == 1,
          f"{path} must name {your}: exactly one entry, with a valid 9-digit student number. "
          f"Found: {pl(len(items), 'entry', 'entries')}, {len(good)} with a valid number.", slot)
    me = my_number()
    # VC, 13 Oct 2026: these two are checked only once a collaborator is named. On the untouched file (role
    # already filled in, no number) they passed and gave two free ticks to a file nobody had written.
    if good:
        check(week, f"{path} does not list you", me == "" or me not in [g.split("-")[0] for g in good],
              f"{path} must not list you. Your own student number is in it: remove that entry.", slot)
        check(week, f"{path} gives everyone the role '{role}'", bool(items) and all(str(i.get("role", "")).strip() == role for i in items),
              f"{path} must give everyone the role '{role}'. Found: a wrong or empty role.", slot)
    else:
        why = f"It is checked once the file names {your}'s student number."
        later(week, f"{path} does not list you", why)
        later(week, f"{path} gives everyone the role '{role}'", why)
    thin = [i for i in items if len(str(i.get("what", "")).strip()) < 25]
    check(week, f"{path} quotes what {your} found or said", bool(items) and not thin,
          f"{path} must quote a real sentence that {your} found or said. Found: {pl(len(thin), 'entry', 'entries')} without one.", slot)
    undecided = [i for i in items if i.get("accepted") not in (True, False) or len(str(i.get("why", "")).strip()) < 15]
    check(week, f"{path} gives a decision and a reason", bool(items) and not undecided,
          f"{path} must say whether you accepted what {your} found (accepted: true or false) and why. "
          f"Found: {pl(len(undecided), 'entry', 'entries')} without a decision and a reason.", DEADLINE)
    return [g.split("-")[0] for g in good]


def week4() -> None:
    """A clickable prototype and test cases in the lab, run on the prototype by the student's
    collaborator (one classmate of their choice, 11 Oct 2026; before that the group);
    by Saturday the fixes, a second round, the updated requirements, S1 and the log.

    The prototype comes before the design on purpose (decided 4 Oct 2026): nobody writes
    every requirement without seeing the product, and a missing screen costs minutes
    today against a server change and two clients in Week 8. The requirements and the
    test cases become the baseline at the end of Week 5.
    """
    reqs = requirement_index()
    live = {r: it for r, it in reqs.items() if not it.get("dropped")}
    musts = sorted(r for r, it in live.items()
                   if str(it.get("priority", "")).strip().lower() == "must" and filled(it.get("description")))

    # --- the prototype ---------------------------------------------------------------
    screens = prototype_screens()
    if not screens:
        check(4, "week04/prototype/ has screens", False,
              "week04/prototype/ has no .html files. Run the checker online to bring the starter screens.")
        check(4, "the prototype has at least 7 screens", False,
              "The prototype must have at least 7 screens by Saturday: the full flow. Found: none yet.", DEADLINE)
    else:
        check(4, "week04/prototype/index.html is there", "index.html" in screens,
              "The first screen must be week04/prototype/index.html. Found: no such file.")
        check(4, "the prototype has at least 5 screens", len(screens) >= 5,
              "The prototype must have at least 5 screens: the 3 starter screens and at least 2 of yours. "
              f"Found: {pl(len(screens), '.html file')} in week04/prototype/.")
        broken = sorted({f"{name} → {to}" for name, html in screens.items() for to in screen_links(html) if to not in screens})
        check(4, "every link in the prototype leads to a screen that exists", bool(screens) and not broken,
              f"Every link in the prototype must lead to a screen that exists. Found: broken links {broken[:3]}.")
        seen, todo = set(), ["index.html"] if "index.html" in screens else []
        while todo:
            name = todo.pop()
            if name in seen or name not in screens:
                continue
            seen.add(name)
            todo.extend(screen_links(screens[name]))
        unreachable = sorted(set(screens) - seen)
        check(4, "every screen can be reached from index.html", bool(screens) and not unreachable,
              f"Every screen must be reachable by links starting from index.html. Found: no link leads to {unreachable[:3]}.")
        holes = sorted(n for n, html in screens.items() if re.search(r"\[[^\]\n]{1,80}\]", visible_text(html)))
        check(4, "the prototype has no [bracketed] text left", bool(screens) and not holes,
              "The prototype screens still have [bracketed] text. Replace it with your own words and delete the square "
              f"brackets too. Found in: {holes[:3]}.")
        check(4, "the prototype has at least 7 screens", len(screens) >= 7,
              f"The prototype must have at least 7 screens by Saturday: the full flow. Found: {len(screens)}.", DEADLINE)
        unnamed = sorted(n for n, html in screens.items() if not serves(html) or any(r not in reqs for r in serves(html)))
        check(4, "every screen names the requirements it serves", bool(screens) and not unnamed,
              "Every screen must say which requirements it serves, in a line like <!-- serves: REQ-001, REQ-004 -->, "
              f"with ids that exist in requirements.json. Found: missing or wrong in {unnamed[:3]}.", DEADLINE)
        if RUN_WEEK <= 4:  # the prototype is not kept up to date once Week 5 starts
            shown = {r for html in screens.values() for r in serves(html)}
            missing = [r for r in musts if live[r].get("functional") is True and r not in shown]
            check(4, "every functional must requirement has a screen", bool(screens) and not missing,
                  "Every functional requirement marked 'must' needs a screen that serves it. "
                  f"Found: no screen serves {missing[:4]}.", DEADLINE)

    # --- the test cases --------------------------------------------------------------
    cases = test_cases()
    if cases is None:
        check(4, "week04/test_cases.json is valid JSON", False,
              "week04/test_cases.json is missing or is not valid JSON. Run the checker online to fetch it.")
        cases = []
    else:
        ids = [str(t.get("id", "")).strip() for t in cases]
        bad = [i for i in ids if not re.fullmatch(r"TC-\d{3}-\d{2}", i)]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        check(4, "test case ids look like TC-001-01 and none is repeated", bool(ids) and not bad and not dup,
              "Test case ids must look like TC-001-01 (the requirement number, then a counter), with no repeats. "
              + ("Found: no test cases yet." if not ids else f"Found: wrong ids {bad[:3]}, repeated ids {dup[:3]}."))
        wrong = [i for i, t in zip(ids, cases)
                 if str(t.get("req", "")).strip() not in reqs or i[3:6] != str(t.get("req", "")).strip()[4:]]
        check(4, "every test case tests a requirement that exists", bool(ids) and not wrong,
              "Every test case must name a requirement that exists in week02/requirements.json, and the number in its id must match it. "
              + ("Found: no test cases yet." if not ids else f"Found: wrong in {wrong[:3]}."))
        thin = [i for i, t in zip(ids, cases)
                if not (isinstance(t.get("steps"), list) and t["steps"] and all(filled(s) for s in t["steps"]))
                or len(filled(t.get("expected"))) < 15]
        check(4, "every test case has steps and an expected result", bool(ids) and not thin,
              "Every test case needs steps and an expected result of at least 15 characters. "
              + ("Found: no test cases yet." if not ids else f"Found: missing in {thin[:3]}."))
    active = [t for t in cases if not t.get("dropped")]
    covered = {str(t.get("req", "")).strip() for t in active}
    uncovered = [r for r in musts if r not in covered]
    check(4, "every must requirement has a test case", bool(musts) and not uncovered,
          "Every requirement marked 'must' needs at least one test case. "
          + ("Found: no 'must' requirements in requirements.json." if not musts else f"Found: none for {uncovered[:4]}."))
    per_req = {r: sum(1 for t in active if str(t.get("req", "")).strip() == r) for r in covered}
    check(4, "at least three requirements have a second test case", sum(1 for n in per_req.values() if n >= 2) >= 3,
          "At least three requirements need a second test case, for when something goes wrong. "
          f"Found: {sum(1 for n in per_req.values() if n >= 2)} with two or more.",
          DEADLINE)

    # --- the walk-through and the testers ----------------------------------------------
    testers = check_collaborator(4, "collaborator")
    data = load_json("week04/walkthrough_04.json")
    runs = data.get("runs", data) if isinstance(data, dict) else data
    if not isinstance(runs, list):
        check(4, "week04/walkthrough_04.json is valid JSON", False,
              "week04/walkthrough_04.json is missing or is not valid JSON. Run the checker online to fetch it.")
        runs = []
    runs = [r for r in runs if isinstance(r, dict) and (filled(r.get("tc")) or filled(r.get("tester")))]
    round1 = [r for r in runs if round_of(r) == 1]
    count: dict[str, int] = {}
    for r in round1:
        t = str(r.get("tester", "")).strip().split("-")[0]
        if re.fullmatch(r"\d{9}", t):
            count[t] = count.get(t, 0) + 1
    me = my_number()
    busiest = max((n for t, n in count.items() if t != me), default=0)
    check(4, "walk-through: your collaborator ran at least four test cases", busiest >= 4,
          "Your collaborator must run at least four of your test cases in round 1 of the walk-through, "
          f"each run recorded under their student number. Found: {pl(busiest, 'run')} by the tester with the most.")
    none = "Found: no runs recorded in week04/walkthrough_04.json yet."
    outside = sorted(set(count) - set(testers))
    check(4, "walk-through: every run is by your collaborator (group_04.json)",
          bool(count) and bool(testers) and not outside,
          "Every run in the walk-through must be by your collaborator, the student named in week04/group_04.json. "
          + (none if not runs else f"Found: not your collaborator: {outside[:3]}." if outside else "Found: no collaborator in group_04.json."))
    main_runs = [r for r in round1 if str(r.get("tc", "")).strip()[3:6] != "001"]
    check(4, "walk-through: round 1 has at least two runs outside the login",
          len(main_runs) >= 2,
          "Round 1 must have at least two runs of test cases outside the login (REQ-001): run test cases of your main flow. "
          + (none if not runs else f"Found: {len(main_runs)}."))
    known = {str(t.get("id", "")).strip() for t in cases}
    unknown = sorted({str(r.get("tc", "")).strip() for r in runs} - known)
    check(4, "walk-through: every run names a test case from test_cases.json", bool(runs) and not unknown,
          "Every run in the walk-through must name a test case that exists in week04/test_cases.json. "
          + (none if not runs else f"Found: not in test_cases.json: {unknown[:3]}."))
    odd = [r for r in runs if str(r.get("result", "")).strip().lower() not in ("pass", "fail", "blocked")
           or (str(r.get("result", "")).strip().lower() in ("fail", "blocked") and len(str(r.get("note", "")).strip()) < 15)]
    check(4, "walk-through: each result is pass, fail or blocked, with a note for fail and blocked",
          bool(runs) and not odd,
          "Every run must have a result (pass, fail or blocked), and a note of at least 15 characters for fail and blocked. "
          + (none if not runs else f"Found: {pl(len(odd), 'run')} without a valid result, or a fail or blocked without a note."))
    dropped = {str(t.get("id", "")).strip() for t in cases if t.get("dropped")}
    failed = {str(r.get("tc", "")).strip() for r in round1 if str(r.get("result", "")).strip().lower() == "fail"}
    rerun = {str(r.get("tc", "")).strip() for r in runs if round_of(r) == 2}
    open_fails = sorted(failed - rerun - dropped)
    check(4, "walk-through: every failed test case was run again in round 2", bool(runs) and not open_fails,
          "Every failed test case must be run again in round 2 after the fix, or dropped with a Change log line. "
          + (none if not runs else f"Found: no round 2 for {open_fails[:3]}."), DEADLINE)

    # --- what the walk-through changed: the Change log ---------------------------------
    text = read("PROPOSAL.md") or ""
    m = re.search(r"^## Change log.*?$", text, re.M)
    log = re.sub(r"<!--.*?-->", "", text[m.end():], flags=re.DOTALL) if m else ""
    lines = [ln for ln in log.splitlines()
             if any(d >= WEEK4_FROM for d in re.findall(r"20\d\d-\d\d-\d\d", ln))
             and re.search(r"REQ-\d{3}|TC-\d{3}-\d{2}", ln)]
    check(4, "PROPOSAL.md change log has a line from the walk-through that names the ids", bool(lines),
          f"PROPOSAL.md change log must have a line dated {WEEK4_FROM} or later that names a REQ or TC id. Found: none.", DEADLINE)

    # --- S1: the developer account -------------------------------------------------------
    st = load_json("week04/store.json")
    if not isinstance(st, dict):
        check(4, "week04/store.json is valid JSON", False,
              "week04/store.json is missing or is not valid JSON. Run the checker online to fetch it.", DEADLINE)
    else:
        name = " ".join(str(st.get("store", "")).lower().split())
        check(4, "store.json names the store", name in STORES,
              "week04/store.json must name the store: one of 'Google Play', 'Huawei AppGallery', 'Samsung Galaxy Store', "
              "'Apple App Store'. Found: something else, or empty.", DEADLINE)
        s1 = st.get("S1") if isinstance(st.get("S1"), dict) else {}
        ok = (re.fullmatch(r"20\d\d-\d\d-\d\d", str(s1.get("date", "")).strip()) and filled(s1.get("developer_name"))
              and str(s1.get("status", "")).strip().lower() in ("applied", "verified"))
        check(4, "store.json S1 is filled in", bool(ok),
              "week04/store.json S1 must have a date like 2026-10-13, your developer name, and a status of 'applied' or "
              "'verified'. Found: one of them missing or wrong.", DEADLINE)
        # a Windows path (week04\\store_s1.png) is the same file: the checker found it on the student's Windows
        # machine and missed it on the instructor's Mac (Sezgin Coçar, 19 Oct 2026)
        ev = str(s1.get("evidence", "")).strip().replace("\\", "/")
        ev_ok = (bool(ev) and ".." not in ev and not Path(ev).is_absolute() and ":" not in ev
                 and ((ROOT / ev).is_file() or (ROOT / "week04" / ev).is_file()))
        check(4, "store.json S1 screenshot is saved", ev_ok,
              "The file named in 'evidence' in week04/store.json S1 must be saved in week04/. Found: no such file.", DEADLINE)
        s12 = (proposal_sections().get(12) or {}).get("text", "").lower()
        check(4, "store.json and PROPOSAL.md §12 name the same store",
              name in STORES and any(k in s12 for k in STORES[name]),
              "week04/store.json and PROPOSAL.md §12 must name the same store. Change one of them, and add a Change log line.", DEADLINE)

    # --- the log: acceptance criteria first ----------------------------------------------
    check(4, "week04/ai_log_04.md names the requirements it gave the assistant",
          bool(re.search(r"REQ-\d{3}", ai_log_section(4))),
          "week04/ai_log_04.md must name the REQ ids you gave the assistant, outside the comments and the evidence block. "
          "Found: no REQ id.", DEADLINE)
    check_ai_log(4)


# ── Week 5: design, API contract, server skeleton, tests first ─────────────────────────────
# Decided 18 Oct 2026 (VC): FastAPI for everyone; the login rows of api.md written by hand
# before any code; the server is read without running it (ast), because the instructor's
# capture must never execute a student's code; the tests are counted by name, not run.

HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
# Routers of server/ that no include_router call brings in (route_defs fills it): their routes do not count,
# because the running server would answer 404 (VC, 24 Oct 2026). Shown as "bookings.router" in the messages.
NOT_INCLUDED: list[str] = []
REQ_HEADS = {"req", "reqs", "req id", "req ids", "requirement", "requirements", "gereksinim", "gereksinimler"}


def _head(cell: str) -> str:
    return re.sub(r"[`*_]", "", cell).strip().lower()


def _col(head: list[str], *starts: str, exact: set[str] | None = None) -> int:
    """The index of the first column whose header is in `exact` or starts with one of `starts`."""
    for i, h in enumerate(head):
        if (exact and h in exact) or (starts and h.startswith(starts)):
            return i
    return -1


def md_table(text: str | None, *starts: str) -> tuple[list[str], list[list[str]]]:
    """The first markdown table that has a column starting with one of `starts`: its headers
    (lower case) and its rows. HTML comments are dropped first."""
    lines = re.sub(r"<!--.*?-->", "", text or "", flags=re.DOTALL).splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith("|"):
            continue
        head = [_head(c) for c in s.strip("|").split("|")]
        if _col(head, *starts) < 0:
            continue
        rows = []
        for ln in lines[i + 1:]:
            r = ln.strip()
            if not r.startswith("|"):
                break
            cells = [c.strip() for c in r.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            rows.append(cells + [""] * (len(head) - len(cells)))
        return head, rows
    return [], []


def design_components() -> list[dict]:
    """The rows of the Components table of week05/DESIGN.md; a [bracketed] row is the scaffold's."""
    head, rows = md_table(read("week05/DESIGN.md"), "component", "bileşen")
    c = _col(head, "component", "bileşen")
    w = _col(head, "what", "does", "ne yapar", "görev")
    q = _col(head, exact=REQ_HEADS)
    out = []
    for r in rows:
        name = r[c] if c >= 0 else ""
        if not filled(name) or "[" in name:
            continue
        out.append({"name": name, "what": r[w] if w >= 0 else "",
                    "reqs": re.findall(r"REQ-\d{3}", r[q]) if q >= 0 else []})
    return out


def norm_path(p: str) -> str:
    """A path as the two sides are compared: no backticks, a changing part is {}, no trailing /."""
    p = re.sub(r"[`*]", "", p).strip().split("?")[0].strip()
    p = re.sub(r"\{[^}]*\}|<[^>]*>|:[A-Za-z_]\w*", "{}", p)
    return p.rstrip("/") if len(p) > 1 else p


def api_endpoints() -> list[dict]:
    """The rows of week05/api.md that name a method and a path; a [bracketed] row is the scaffold's."""
    head, rows = md_table(read("week05/api.md"), "method", "metot", "metod", "yöntem")
    m_ = _col(head, "method", "metot", "metod", "yöntem")
    p_ = _col(head, "path", "yol")
    cols = {"request": _col(head, "request", "istek"), "response": _col(head, "response", "cevap", "yanıt"),
            "errors": _col(head, "error", "hata"), "req": _col(head, exact=REQ_HEADS)}
    out = []
    for r in rows:
        method = re.sub(r"[`*]", "", r[m_]).strip().upper() if m_ >= 0 else ""
        raw = r[p_] if p_ >= 0 else ""
        if method not in HTTP_METHODS or "[" in raw or not norm_path(raw).startswith("/"):
            continue
        get = {k: (r[i] if i >= 0 else "") for k, i in cols.items()}
        out.append({"key": f"{method} {norm_path(raw)}", "request": get["request"], "response": get["response"],
                    "errors": get["errors"], "reqs": re.findall(r"REQ-\d{3}", get["req"])})
    return out


def server_routes() -> dict[str, str]:
    """'METHOD /path' -> file, for every route in server/ (tests excluded)."""
    return {k: v[0] for k, v in route_defs().items()}


def route_defs() -> dict[str, tuple[str, ast.AST | None]]:
    """'METHOD /path' -> (file, the function that answers it), for every route in server/ (tests excluded). Read
    with ast: nothing of the student's code is run. Knows @app.get(...), APIRouter(prefix=...) and
    app.include_router(router, prefix=...). From Week 6 the course's login (server/course_login.py), once
    server/main.py brings it in, adds the three endpoints of server/login_contract.json (function: None)."""
    folder = ROOT / "server"
    if not folder.is_dir():
        return {}
    trees = {}
    for p in sorted(folder.rglob("*.py")):
        rel = p.relative_to(folder).parts
        if "tests" in rel or ".venv" in rel or "__pycache__" in rel or rel == ("course_login.py",):
            continue
        try:
            trees[p] = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue

    def text(node):
        return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None

    def kw(call, name):
        return next((text(k.value) for k in call.keywords if k.arg == name), None)

    included: dict[tuple, str] = {}
    for tree in trees.values():
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "include_router" and node.args):
                a = node.args[0]
                if isinstance(a, ast.Attribute) and isinstance(a.value, ast.Name):
                    included[(a.value.id, a.attr)] = kw(node, "prefix") or ""
                elif isinstance(a, ast.Name):
                    included[(None, a.id)] = kw(node, "prefix") or ""
    # Imported names: "from server.bookings import router as br" + include_router(br) brings in bookings.router;
    # "import server.bookings as b" + include_router(b.router) the same.
    for tree in trees.values():
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                stem = node.module.split(".")[-1]
                for al in node.names:
                    if (None, al.asname or al.name) in included:
                        included.setdefault((stem, al.name), included[(None, al.asname or al.name)])
            elif isinstance(node, ast.Import):
                for al in node.names:
                    if al.asname:
                        stem = al.name.split(".")[-1]
                        for (mod, var), pre in list(included.items()):
                            if mod == al.asname:
                                included.setdefault((stem, var), pre)
    NOT_INCLUDED.clear()
    out: dict[str, tuple[str, ast.AST | None]] = {}
    for p, tree in trees.items():
        routers: dict[str, str] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                f = node.value.func
                if (f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")) == "APIRouter":
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            routers[target.id] = kw(node.value, "prefix") or ""
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for d in node.decorator_list:
                if not (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
                        and d.func.attr.upper() in HTTP_METHODS and isinstance(d.func.value, ast.Name)):
                    continue
                route = text(d.args[0]) if d.args else kw(d, "path")
                if route is None:
                    continue
                var = d.func.value.id
                prefix = ""
                if var in routers:
                    if (p.stem, var) not in included and (None, var) not in included:
                        name = f"{p.stem}.{var}"
                        if name not in NOT_INCLUDED:
                            NOT_INCLUDED.append(name)
                        continue
                    prefix = included.get((p.stem, var), included.get((None, var), "")) + routers[var]
                out[f"{d.func.attr.upper()} {norm_path(prefix + route)}"] = (str(p.relative_to(ROOT)), node)
    if (ROOT / "server" / "course_login.py").is_file() and course_login_included():
        data, bad = login_contract()
        if data is not None and not bad:
            for k in ("request_code", "login", "me"):
                method, route = data[k].strip().split(None, 1)
                out.setdefault(f"{method.upper()} {norm_path(route.strip())}", ("server/course_login.py", None))
    return out


def tc_test_ids() -> list[str]:
    """The test case ids in the names of the tests in server/tests/: test_TC_001_02_... -> TC-001-02."""
    folder = ROOT / "server" / "tests"
    ids = []
    for p in sorted(folder.rglob("*.py")) if folder.is_dir() else []:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                m = re.match(r"test_TC_(\d{3})_(\d{2})(?:_|$)", node.name, re.I)
                if m:
                    ids.append(f"TC-{m.group(1)}-{m.group(2)}")
    return ids


def week5() -> None:
    """The design and the API contract; the server skeleton in server/ with a route for every row
    of api.md; the login tests written from the test cases before the code (they fail until
    Week 6). On Saturday the requirements and the test cases become the baseline (no check:
    the deadline capture is the record)."""
    reqs = requirement_index()
    live = {r: it for r, it in reqs.items() if not it.get("dropped")}
    musts = sorted(r for r, it in live.items()
                   if str(it.get("priority", "")).strip().lower() == "must" and filled(it.get("description")))

    # --- the design --------------------------------------------------------------------
    design = read("week05/DESIGN.md")
    comps = design_components()
    good = [c for c in comps if c["reqs"] and all(r in reqs for r in c["reqs"]) and len(filled(c["what"])) >= 10]
    check(5, "week05/DESIGN.md has at least four components, each with what it does and the requirements it serves",
          len(good) >= 4,
          "week05/DESIGN.md is missing. Run the checker online to bring it." if design is None else
          "week05/DESIGN.md must have at least four components in its table, each with what it does and the REQ ids "
          f"it serves, ids that exist in requirements.json. Found: {pl(len(good), 'complete row')}.")
    served = {r for c in comps for r in c["reqs"]}
    missing = [r for r in musts if live[r].get("functional") is True and r not in served]
    check(5, "every functional must requirement is served by a component in week05/DESIGN.md",
          bool(musts) and not missing,
          "Every functional requirement marked 'must' needs a component in week05/DESIGN.md that serves it. "
          + ("Found: no 'must' requirements in requirements.json." if not musts else f"Found: no component serves {missing[:4]}."),
          DEADLINE)
    blocks = re.findall(r"```mermaid[^\n]*\n(.*?)```", design or "", re.DOTALL)
    arrows = max((len(re.findall(r"-\.->|==+>|--+>", re.sub(r"(?m)^\s*%%.*$", "", b))) for b in blocks), default=0)
    check(5, "week05/DESIGN.md has the architecture as a Mermaid diagram", arrows >= 2,
          "week05/DESIGN.md must draw the architecture as a Mermaid diagram: your components, with at least two arrows "
          f"between them. Found: {pl(arrows, 'arrow')}.", DEADLINE)

    # --- the API contract ----------------------------------------------------------------
    api = read("week05/api.md")
    eps = api_endpoints()
    login = [e for e in eps if "REQ-001" in e["reqs"]]
    check(5, "week05/api.md has the login endpoints (REQ-001)", len(login) >= 2,
          "week05/api.md is missing. Run the checker online to bring it." if api is None else
          "week05/api.md must have at least two endpoints that serve REQ-001, the login: one that asks for a code and "
          f"one that logs in with it. Found: {len(login)}.")
    named = sorted({r for e in eps for r in e["reqs"]})
    unknown = [r for r in named if r not in reqs]
    check(5, "every REQ id in week05/api.md exists in requirements.json", bool(named) and not unknown,
          "Every REQ id in week05/api.md must exist in week02/requirements.json. "
          + ("Found: no REQ ids yet." if not named else f"Found: not there: {unknown[:3]}."))
    thin = [e["key"] for e in eps if e["reqs"] and not (
        filled(e["request"]) and re.search(r"\b2\d\d\b", e["response"]) and re.search(r"\b[45]\d\d\b", e["errors"]))]
    check(5, "every endpoint in week05/api.md gives its request, its response and its errors",
          any(e["reqs"] for e in eps) and not thin,
          "Every endpoint in week05/api.md that serves a requirement must give its request, its response with a 2xx "
          "status code, and at least one error with its 4xx or 5xx code. "
          + ("Found: no endpoint that serves a requirement." if not any(e["reqs"] for e in eps) else f"Found: incomplete: {thin[:3]}."),
          DEADLINE)

    # --- the server ------------------------------------------------------------------------
    src = read("server/main.py")
    routes = server_routes()
    # Like the collaborator checks of Week 4: the untouched starter must not earn free ticks, so these two
    # count once the server has a route of the student's own; a missing or broken file always shows.
    if src is None or not parses("server/main.py") or set(routes) - {"GET /health"}:
        check(5, "server/main.py is valid Python", src is not None and parses("server/main.py"),
              "server/main.py must be there and be valid Python. "
              + ("Found: no such file. Run the checker online to bring the starter." if src is None else "Found: a syntax error."))
        check(5, "server/main.py creates the FastAPI app", bool(src) and re.search(r"\bFastAPI\s*\(", src or "") is not None,
              "server/main.py must create the app with FastAPI(...). Found: no FastAPI( in it.")
    else:
        why = "It is checked once server/ has a route of your own besides /health."
        later(5, "server/main.py is valid Python", why)
        later(5, "server/main.py creates the FastAPI app", why)
    keys = {e["key"] for e in eps}
    serving = any(e["reqs"] for e in eps)
    unbuilt = sorted(keys - set(routes))
    check(5, "every endpoint in week05/api.md has its route in server/", serving and not unbuilt,
          "Every endpoint in week05/api.md must have a route in server/ with the same method and path; it may answer 501 "
          "until it is built. " + ("Found: no endpoint that serves a requirement in week05/api.md yet." if not serving
                                   else f"Found: no route for {unbuilt[:3]}; server/main.py does not include "
                                   f"{', '.join(NOT_INCLUDED)}." if NOT_INCLUDED
                                   else f"Found: no route for {unbuilt[:3]}."))
    own = set(routes) - {"GET /health"}
    undocumented = sorted(set(routes) - keys)
    check(5, "every route in server/ has its row in week05/api.md", bool(own) and not undocumented,
          "Every route in server/ must be a row of week05/api.md, with the same method and path. "
          + ("Found: no routes in server/ besides /health." if not own else f"Found: not in api.md: {undocumented[:3]}."), DEADLINE)

    # --- the tests, named by test case ids -------------------------------------------------
    ids = tc_test_ids()
    check(5, "server/tests has a test named by a test case id", bool(ids),
          "server/tests/ must have at least one test whose name begins with a test case id, such as "
          "test_TC_001_01_a_code_is_sent. Found: none.")
    distinct = sorted(set(ids))
    check(5, "server/tests has at least three tests named by different test case ids", len(distinct) >= 3,
          f"server/tests/ must have at least three tests named by different test case ids. Found: {len(distinct)}.",
          DEADLINE)
    known = {str(c.get("id", "")).strip() for c in (test_cases() or [])}
    strangers = [i for i in distinct if i not in known]
    check(5, "every test case id in server/tests exists in test_cases.json", bool(distinct) and not strangers,
          "Every test case id in a test name in server/tests/ must exist in week04/test_cases.json. "
          + ("Found: no tests named by a test case id." if not distinct else f"Found: not there: {strangers[:3]}."),
          DEADLINE)

    # --- the log: verify by running ---------------------------------------------------------
    check(5, "week05/ai_log_05.md holds the output of a test run",
          bool(re.search(r"\b\d+ (passed|failed)\b", ai_log_evidence(5))),
          "week05/ai_log_05.md must hold, in the Evidence block, the output of a test run as your terminal showed it, "
          "down to its last line, such as '1 failed, 1 passed'. Found: no such line.", DEADLINE)
    check_ai_log(5)


# ── Week 6: the login comes ready; your own must requirements end to end ─────────────────────────────
# (VC, 21-22 Oct 2026; claude-private/week06_spec.md, its CHANGE OF COURSE part)

COURSE_LOGIN = "server/course_login.py"  # the course's login module (course-owned from Week 6)


def course_login_included() -> bool:
    """server/main.py brings in the course's login: app.include_router(course_login.router). Read with ast
    (from server import course_login, import server.course_login as x, from server.course_login import router
    as y): nothing of the student's code is run."""
    try:
        tree = ast.parse(read("server/main.py") or "")
    except SyntaxError:
        return False
    mods: set[str] = set()
    routers: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for a in node.names:
                if a.name == "course_login" and mod in ("server", ""):
                    mods.add(a.asname or a.name)
                elif mod.split(".")[-1] == "course_login" and a.name == "router":
                    routers.add(a.asname or a.name)
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[-1] == "course_login":
                    mods.add(a.asname or a.name)
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "include_router" and node.args):
            a = node.args[0]
            if isinstance(a, ast.Name) and a.id in routers:
                return True
            if isinstance(a, ast.Attribute) and a.attr == "router" and ast.unparse(a.value) in mods:
                return True
    return False


def route_unbuilt(node) -> bool:
    """A route that still answers 501 (HTTPException(501), status_code=501, HTTP_501_NOT_IMPLEMENTED,
    NotImplementedError) or does nothing (only a docstring, pass or ...). None is the course's login: built."""
    if node is None:
        return False
    body = [s for s in node.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    if not body or all(isinstance(s, ast.Pass) for s in body):
        return True
    for n in ast.walk(ast.Module(body=body, type_ignores=[])):
        if isinstance(n, ast.Constant) and type(n.value) is int and n.value == 501:
            return True
        if isinstance(n, ast.Attribute) and n.attr == "HTTP_501_NOT_IMPLEMENTED":
            return True
        if isinstance(n, ast.Name) and n.id == "NotImplementedError":
            return True
    return False


def web_pages() -> dict[Path, tuple[str, str]]:
    """Every page in web/: (its HTML, its HTML with the text of the local scripts it loads). Read as text."""
    web = ROOT / "web"
    out: dict[Path, tuple[str, str]] = {}
    if not web.is_dir():
        return out
    home = web.resolve()
    for p in sorted(web.rglob("*.html")):
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        text = html
        for src in re.findall(r"""<script[^>]*\bsrc\s*=\s*["']([^"']+)["']""", html, re.I):
            src = src.split("?")[0].split("#")[0]
            if re.match(r"[a-z][a-z0-9+.-]*:|//", src, re.I):
                continue
            tries = [web / src[5:]] if src.startswith("/web/") else []
            tries.append(web / src.lstrip("/") if src.startswith("/") else p.parent / src)
            for t in tries:
                try:
                    t = t.resolve()
                    if home in t.parents and t.is_file():
                        text += "\n" + t.read_text(encoding="utf-8", errors="replace")
                        break
                except OSError:
                    continue
        out[p] = (html, text)
    return out


def calls_fetch(text: str) -> bool:
    return re.search(r"\bfetch\s*\(", re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)) is not None


def calls_path(text: str, key: str) -> bool:
    """A page names an endpoint's path: every fixed part of it (/courses/{}/announcements: /courses and
    /announcements) is in its text."""
    pieces = [s.strip("/") for s in key.split(" ", 1)[-1].split("{}") if s.strip("/")]
    return bool(pieces) and all("/" + s in text for s in pieces)


def must_requirements() -> tuple[set[str], set[str]]:
    """(must, functional must): the ids of week02/requirements.json marked 'must', dropped ones left out."""
    reqs = requirement_index()
    musts = {r for r, it in reqs.items() if not it.get("dropped")
             and str(it.get("priority", "")).strip().lower() == "must" and filled(it.get("description"))}
    return musts, {r for r in musts if reqs[r].get("functional") is True}


LOGIN_TESTS = {  # the course's login tests (course_tests/test_login_contract.py): number -> (what it shows, when due)
    "01": ("a code is sent to a valid e-mail", SESSION),
    "02": ("something that is not an e-mail is refused", SESSION),
    "03": ("the right code gives a token", SESSION),
    "04": ("a wrong code is refused", SESSION),
    "05": ("the token opens me", SESSION),
    "06": ("me is refused without a token or with a wrong one", SESSION),
    "07": ("a code works only once", DEADLINE),
    "08": ("a code expires after 10 minutes", DEADLINE),
    "09": ("a new code within a minute is refused, and allowed after it", DEADLINE),
    "10": ("three wrong codes lock the login for 15 minutes", DEADLINE),
}
CONTRACT_KEYS = ("request_code", "login", "me", "email_field", "code_field", "token_field")
SMTP_NAMES = ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM")
_TESTS: dict | None = None
_WORST = {"passed": 0, "skipped": 1, "failed": 2, "error": 3}


def _junit(path: Path) -> dict[str, tuple[str, str]]:
    """{test id: (outcome, message)} from a pytest junit file: LOGIN_NN for the course's tests, TC-NNN-NN for
    yours (test_TC_001_02_...). Several tests with one id: the worst outcome stands."""
    import xml.etree.ElementTree as ET
    out: dict[str, tuple[str, str]] = {}
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return out
    for tc in root.iter("testcase"):
        name = tc.get("name", "")
        m = re.match(r"test_LOGIN_(\d\d)", name)
        n = re.match(r"test_TC_(\d{3})_(\d{2})", name, re.I)
        key = f"LOGIN_{m.group(1)}" if m else (f"TC-{n.group(1)}-{n.group(2)}" if n else None)
        if not key:
            continue
        outcome, msg = "passed", ""
        for tag, word in (("error", "error"), ("failure", "failed"), ("skipped", "skipped")):
            el = tc.find(tag)
            if el is not None:
                outcome, msg = word, " ".join(str(el.get("message") or "").split())[:160]
                break
        if key not in out or _WORST[outcome] > _WORST[out[key][0]]:
            out[key] = (outcome, msg)
    return out


def _official_course_tests() -> list[str]:
    """GitHub Actions only: put the course's own course_tests/ and server/course_login.py in place before they
    run, whatever the repository holds (the files are checked against the manifest's sha256). The test files
    written, to be run by name so that no other file in the folder joins them; [] if that could not be done."""
    try:
        with urllib.request.urlopen(MANIFEST_URL, timeout=10) as response:
            manifest = response.read().decode("utf-8")
    except (urllib.error.URLError, OSError, TimeoutError, UnicodeDecodeError):
        return []
    done: list[str] = []
    for line in manifest.splitlines():
        parts = line.strip().split("  ", 1)
        if len(parts) != 2 or ".." in parts[1] or not (parts[1].startswith("course_tests/")
                                                       or parts[1] in COURSE_FILE_FROM):
            continue
        try:
            with urllib.request.urlopen(RAW_BASE + urllib.parse.quote(parts[1]), timeout=10) as response:
                data = response.read()
        except (urllib.error.URLError, OSError, TimeoutError):
            return []
        if hashlib.sha256(data).hexdigest() != parts[0]:
            return []
        try:
            target = ROOT / parts[1]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        except OSError:
            return []
        if Path(parts[1]).name.startswith("test_") and parts[1].endswith(".py"):
            done.append(parts[1])
    return done


def _ci_course_requirements(week: int) -> None:
    """GitHub Actions only: when the repository's requirements file did not install pytest, fastapi and freezegun,
    install the course's own requirements file for the week, so that the tests can run (VC, 1 Nov 2026: some
    repositories still hold the old week06/requirements.txt of the template of 24-26 Sep, and their tests never
    ran). The student's own packages stay installed; this only adds what the tests need."""
    try:
        missing = subprocess.run([sys.executable, "-c", "import pytest, fastapi, freezegun"], cwd=ROOT,
                                 capture_output=True, timeout=60).returncode != 0
    except (subprocess.TimeoutExpired, OSError):
        missing = True
    if not missing:
        return
    for w in dict.fromkeys((week, 6)):
        try:
            with urllib.request.urlopen(RAW_BASE + f"week{w:02d}/requirements.txt", timeout=10) as response:
                text = response.read().decode("utf-8")
        except (urllib.error.URLError, OSError, TimeoutError, UnicodeDecodeError):
            continue
        if "pytest" not in text or "fastapi" not in text:
            continue
        req = Path(tempfile.gettempdir()) / f"aiasd_course_requirements_{w:02d}.txt"
        try:
            req.write_text(text, encoding="utf-8")
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(req)], cwd=ROOT,
                           capture_output=True, timeout=600)
        except (subprocess.TimeoutExpired, OSError):
            return
        print("  " + say("Your week{w}/requirements.txt did not install pytest, fastapi and freezegun, so the course's "
                         "own file was installed for the tests. Replace your file with the course's "
                         "week{w}/requirements.txt.", w=f"{w:02d}"))
        print()
        return


def _run_pytest(args: list[str], isolated: bool) -> tuple[dict, str]:
    """One pytest run; ({test id: (outcome, message)}, why it could not run). The course's tests run isolated:
    `python -I`, no conftest.py, no pytest settings of the repository and no installed pytest plugins, so
    nothing in it can change them."""
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / "results.xml"
        cmd = [sys.executable] + (["-I"] if isolated else []) + ["-m", "pytest", *args, "-q", "-p", "no:cacheprovider",
                                                                f"--junitxml={xml}"]
        if isolated:
            ini = Path(tmp) / "pytest.ini"
            ini.write_text("[pytest]\n", encoding="utf-8")
            cmd += ["--noconftest", "-c", str(ini), "--rootdir", str(ROOT)]
        try:
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180,
                               env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
                                    **({"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"} if isolated else {})})
        except (subprocess.TimeoutExpired, OSError):
            return {}, "the tests did not finish within 3 minutes"
        if not xml.is_file():
            tail = [x for x in (p.stdout + p.stderr).splitlines() if x.strip()]
            return {}, "pytest could not start" + (f": {tail[-1][:120]}" if tail else "")
        return _junit(xml), ""


def _run_tests() -> dict:
    """Your run and GitHub Actions: run the course's login tests and your tests in server/tests."""
    ci = bool(os.environ.get("GITHUB_ACTIONS"))
    official: list[str] = []
    if ci:
        week = RUN_WEEK if isinstance(RUN_WEEK, int) and RUN_WEEK > 0 else 6
        req = next((f"week{w:02d}/requirements.txt" for w in (week, 6, 5)
                    if (ROOT / f"week{w:02d}/requirements.txt").is_file()), None)
        if req:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", req], cwd=ROOT,
                               capture_output=True, timeout=600)
            except (subprocess.TimeoutExpired, OSError):
                pass
        official = _official_course_tests()
        _ci_course_requirements(week)
    result: dict = {"ran": False, "why": "", "outcomes": {}}
    try:
        probe = subprocess.run([sys.executable, "-c", "import pytest, fastapi, freezegun"], cwd=ROOT,
                               capture_output=True, timeout=60).returncode
    except (subprocess.TimeoutExpired, OSError):
        probe = 1
    if probe != 0:
        result["why"] = say("pytest, fastapi or freezegun is not installed: run pip install -r week06/requirements.txt "
                            "in your virtual environment, then run the checker again")
    else:
        outcomes: dict = {}
        whys: list[str] = []
        for args, isolated in ((official or ["course_tests"], True), (["server/tests"], False)):
            if (ROOT / args[0]).exists():
                got, why = _run_pytest(args, isolated)
                outcomes.update(got)
                if why:
                    whys.append(why)
        result = {"ran": not whys or bool(outcomes), "why": "; ".join(whys), "outcomes": outcomes}
    if ci:  # machine-readable lines in the GitHub Actions log: the instructor's capture reads these
        # The tag is made after the tests ran, so nothing they started can print lines that pass for these.
        tag = hashlib.sha256(os.urandom(16)).hexdigest()[:12]
        print(f"AIASD-RESULTS {tag} {'official' if official else 'local'}")
        if result["outcomes"]:
            for key in sorted(result["outcomes"]):
                outcome, msg = result["outcomes"][key]
                print(f"AIASD-TEST {tag} {key} {outcome}" + (f" {msg}" if msg and outcome != "passed" else ""))
        else:
            print(f"AIASD-TESTS-NOT-RUN {tag} {result['why'] or 'no tests were found'}")
        print()
    return result


def _ci_results() -> dict:
    """The instructor's capture: the results come from the GitHub Actions run of the commit read, never from
    running a student's code here (AIASD_CI_LOG is that run's log; AIASD_CI_UNTRUSTED says why it cannot be used,
    AIASD_CI_WHY why there is no log). Only the lines carrying the tag of the run's one AIASD-RESULTS line count."""
    untrusted = os.environ.get("AIASD_CI_UNTRUSTED", "").strip()
    if untrusted:
        return {"ran": False, "why": untrusted, "outcomes": {}}
    path = os.environ.get("AIASD_CI_LOG", "").strip()
    if not path or not Path(path).is_file():
        why = os.environ.get("AIASD_CI_WHY", "").strip() or "no GitHub Actions run for the commit read"
        return {"ran": False, "why": why, "outcomes": {}}
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    tags = [m.group(1) for m in (re.search(r"AIASD-RESULTS (\w+) (?:official|local)\s*$", x) for x in lines) if m]
    if len(tags) > 1:
        return {"ran": False, "outcomes": {},
                "why": "the GitHub Actions log of the commit read holds more than one set of test results"}
    tag = tags[0] if tags else None
    outcomes: dict[str, tuple[str, str]] = {}
    not_run = ""
    for line in lines if tag else []:
        m = re.search(rf"AIASD-TEST {tag} (\S+) (passed|failed|error|skipped)(?: (.*))?$", line)
        if m:
            outcomes[m.group(1)] = (m.group(2), (m.group(3) or "").strip())
            continue
        m = re.search(rf"AIASD-TESTS-NOT-RUN {tag} (.*)$", line)
        if m:
            not_run = m.group(1).strip()
    if outcomes:
        return {"ran": True, "why": "", "outcomes": outcomes}
    return {"ran": False, "outcomes": {},
            "why": ("in GitHub Actions, " + not_run) if not_run else "the GitHub Actions run of the commit read holds no test results"}


def test_results() -> dict:
    """{"ran": bool, "why": str, "outcomes": {test id: (outcome, message)}}, worked out once per run."""
    global _TESTS
    if _TESTS is None:
        _TESTS = _ci_results() if os.environ.get("AIASD_SLOT") else _run_tests()
    return _TESTS


def login_contract() -> tuple[dict | None, list[str]]:
    """server/login_contract.json and the keys still missing or not filled in."""
    data = load_json("server/login_contract.json")
    if not isinstance(data, dict):
        return None, []
    bad = [k for k in CONTRACT_KEYS if not isinstance(data.get(k), str) or not data[k].strip() or "[" in data[k]]
    bad += [k for k in ("request_code", "login", "me") if k not in bad
            and not re.fullmatch(r"(GET|POST|PUT|PATCH|DELETE) /\S*", data[k].strip(), re.I)]
    return data, bad


def check_attackers(week: int) -> None:
    """weekNN/group_NN.json from Week 6: the groupmates who tried to break your work, your own feature and the
    login (the hostile reviewer, Doc5 §3), what each tried and what happened, typed by you; by Saturday whether you
    fix it and why."""
    path = f"week{week:02d}/group_{week:02d}.json"
    items = contributors(week)
    if items is None:
        check(week, f"{path} is valid JSON", False,
              f"{path} is missing or is not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.")
        why = f"It is checked once {path} is there."
        later(week, f"{path} names the groupmate who attacked your work", why)
        later(week, f"{path} does not list you", why)
        later(week, f"{path} gives everyone the role 'attacker'", why)
        later(week, f"{path} says what each attacker tried and what happened", why)
        later(week, f"{path} says for each finding whether you fix it, and why", why, DEADLINE)
        return
    items = [i for i in items if isinstance(i, dict)]
    good = [str(i.get("student_id", "")).strip() for i in items
            if re.fullmatch(r"\d{9}(-\d+)?", str(i.get("student_id", "")).strip())]
    check(week, f"{path} names the groupmate who attacked your work", bool(items) and len(good) == len(items),
          f"{path} must name each groupmate who tried to break your work, with a valid 9-digit student number. "
          f"Found: {pl(len(items), 'entry', 'entries')}, {len(good)} with a valid number.")
    me = my_number()
    if good:
        check(week, f"{path} does not list you", me == "" or me not in [g.split("-")[0] for g in good],
              f"{path} must not list you. Your own student number is in it: remove that entry.")
        check(week, f"{path} gives everyone the role 'attacker'",
              all(str(i.get("role", "")).strip() == "attacker" for i in items),
              f"{path} must give everyone the role 'attacker'. Found: a wrong or empty role.")
    else:
        why = "It is checked once the file names the student number of the groupmate who attacked your work."
        later(week, f"{path} does not list you", why)
        later(week, f"{path} gives everyone the role 'attacker'", why)
    thin = [i for i in items if len(str(i.get("tried", "")).strip()) < 25 or len(str(i.get("happened", "")).strip()) < 15]
    check(week, f"{path} says what each attacker tried and what happened", bool(items) and not thin,
          f"{path} must say, in your own words, what each attacker tried (tried) and what your server or your page did (happened). "
          f"Found: {pl(len(thin), 'entry', 'entries')} without both.")
    undecided = [i for i in items if i.get("accepted") not in (True, False) or len(str(i.get("why", "")).strip()) < 15]
    check(week, f"{path} says for each finding whether you fix it, and why", bool(items) and not undecided,
          f"{path} must say for each attacker's finding whether you fix it (accepted: true or false) and why. "
          f"Found: {pl(len(undecided), 'entry', 'entries')} without a decision and a reason.", DEADLINE)


def week6() -> None:
    """The login comes ready (server/course_login.py): fill in server/login_contract.json and bring it in. Then the
    week is your own functional must requirements, end to end: the api.md row, its route working, its tests named by
    test case ids passing in GitHub Actions, and its prototype screen turned into a page of web/ that calls the
    server. By Saturday all of them, real e-mail, S2 and the attackers' findings decided."""
    musts, fmust = must_requirements()
    own = fmust - {"REQ-001"}
    eps = api_endpoints()
    own_rows = [e for e in eps if set(e["reqs"]) & own]
    defs = route_defs()
    res = test_results()
    tcs = test_cases() or []
    live_tcs = [c for c in tcs if not c.get("dropped")]
    pages = web_pages()
    web = ROOT / "web"

    # --- the login: the course's module, brought in with a few lines ---------------------------------------
    path = "server/login_contract.json"
    data, bad = login_contract()
    check(6, f"{path} is filled in", data is not None and not bad,
          f"{path} must give, written by hand, request_code, login and me (each a method and a path, such as "
          "POST /auth/code) and email_field, code_field and token_field. "
          + ("Found: no such file, or not valid JSON. Run the checker online to bring it." if data is None
             else f"Found: not filled in: {bad[:3]}."))
    have = (ROOT / COURSE_LOGIN).is_file()
    check(6, "server/main.py brings in the course's login (course_login.router)", have and course_login_included(),
          "server/main.py must bring in the login the course gives, with from server import course_login and "
          "app.include_router(course_login.router). Found: "
          + ("no server/course_login.py. Run the checker online to bring it." if not have
             else "no such line in server/main.py."))
    if data is not None and not bad:
        ends = []
        for k in ("request_code", "login", "me"):
            method, route = data[k].strip().split(None, 1)
            ends.append(f"{method.upper()} {norm_path(route.strip())}")
        keys = {e["key"] for e in eps}
        not_api = [v for v in ends if v not in keys]
        check(6, "the three login endpoints of server/login_contract.json are rows of week05/api.md", not not_api,
              f"Every endpoint in {path} must be a row of week05/api.md with the same method and path. "
              f"Found: not in week05/api.md: {not_api}.")
    else:
        later(6, "the three login endpoints of server/login_contract.json are rows of week05/api.md",
              "It is checked once server/login_contract.json is filled in.")

    # --- the course's login tests: run in GitHub Actions for the commit that is read ---------------------------
    for n, (what, slot) in LOGIN_TESTS.items():
        key = f"LOGIN_{n}"
        outcome, msg = res["outcomes"].get(key, ("", ""))
        if not res["ran"]:
            found = res["why"]
        elif not outcome:
            found = say("it did not run (see the tests' own output: python -m pytest course_tests -q)")
        else:
            found = outcome + (f": {msg}" if msg else "")
        check(6, f"course test {key}: {what}", outcome == "passed",
              f"Course test {key} ({what}) must pass. Found: {found}.", slot)

    # --- in the lab: the first of your own must requirements works --------------------------------------------
    working = [e["key"] for e in own_rows if e["key"] in defs and not route_unbuilt(defs[e["key"]][1])]
    check(6, "a route of one of your own must requirements works: it no longer answers 501", bool(working),
          "At least one row of week05/api.md that serves a functional must requirement of your own (not the login, "
          "REQ-001) must have its route in server/ working: no longer answering 501. Found: "
          + ("no functional must requirement besides REQ-001 in week02/requirements.json." if not own
             else "no row of week05/api.md serves one." if not own_rows
             else f"no working route; server/main.py does not include {', '.join(NOT_INCLUDED)}." if NOT_INCLUDED
             else "every such route still answers 501."))
    own_tc = sorted({str(c.get("id", "")).strip() for c in live_tcs if str(c.get("req", "")).strip() in musts - {"REQ-001"}})
    if not res["ran"]:
        ok, found = False, res["why"]
    elif not own_tc:
        ok, found = False, "no test case of a must requirement besides REQ-001 in week04/test_cases.json"
    else:
        ok = any(res["outcomes"].get(i, ("", ""))[0] == "passed" for i in own_tc)
        found = "none of their tests passes, or no test is named by one of their ids"
    check(6, "a test named by a test case of one of your own must requirements passes", ok,
          "At least one test in server/tests/ named by a test case of a must requirement of your own (not the login, "
          f"REQ-001), such as test_TC_002_02_..., must pass. Found: {found}.")
    calling = [p for p, (_, text) in pages.items()
               if calls_fetch(text) and any(calls_path(text, e["key"]) for e in own_rows)]
    check(6, "web/ has a page that calls a route of your own must requirements with fetch", bool(calling),
          "web/ must hold a page of your web client, made from its prototype screen, that calls with fetch a path of "
          "week05/api.md serving a functional must requirement of your own (not the login). Found: "
          + ("no web/ folder." if not web.is_dir() else "no page in web/." if not pages
             else "no row of week05/api.md serves such a requirement." if not own_rows
             else "no page or script there that calls fetch with one of those paths."))
    folder = ROOT / "server"
    src = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in folder.rglob("*.py")
                    if "tests" not in p.relative_to(folder).parts) if folder.is_dir() else ""
    serves_web = bool(re.search(r"StaticFiles\s*\(|HTMLResponse|FileResponse", src)) and "web" in src
    check(6, "server/ serves the pages of web/", serves_web,
          "server/ must serve the pages of web/ itself, with StaticFiles (app.mount), an HTMLResponse or a "
          "FileResponse, so that the web client and the server share one address. Found: neither.")

    # --- by Saturday: every functional must requirement, end to end ----------------------------------------------
    fm_rows = [e for e in eps if set(e["reqs"]) & fmust]
    still = [e["key"] for e in fm_rows if e["key"] not in defs or route_unbuilt(defs[e["key"]][1])]
    check(6, "every row of week05/api.md that serves a functional must requirement has a working route",
          bool(fm_rows) and not still,
          "Every row of week05/api.md that serves a functional must requirement must have its route in server/, no "
          "longer answering 501. Found: "
          + ("no row of week05/api.md serves a functional must requirement." if not fm_rows
             else f"missing or still 501: {still[:4]}; server/main.py does not include {', '.join(NOT_INCLUDED)}."
             if NOT_INCLUDED else f"missing or still 501: {still[:4]}."), DEADLINE)
    server_tc = sorted({str(c.get("id", "")).strip() for c in live_tcs if str(c.get("req", "")).strip() in musts
                        and str(c.get("run", "")).strip().lower() == "server"})
    if not res["ran"]:
        ok, found = False, res["why"]
    elif not server_tc:
        ok, found = False, 'no test case of a must requirement with "run": "server"'
    else:
        failing = [i for i in server_tc if res["outcomes"].get(i, ("", ""))[0] != "passed"]
        ok, found = not failing, f"no passing test for {failing[:4]}"
    check(6, 'every test case of a must requirement with run "server" has a test that passes', ok,
          'Every test case of a must requirement with "run": "server" in week04/test_cases.json must have a test in '
          f"server/tests/ named by its id, such as test_TC_002_02_..., that passes. Found: {found}.", DEADLINE)
    shown = {r for _, (html, text) in pages.items() if calls_fetch(text) for r in serves(html)}
    no_page = sorted(fmust - shown)
    check(6, "every functional must requirement has a page in web/ that calls the server", bool(fmust) and not no_page,
          "Every functional must requirement needs a page in web/ that names it in a line like <!-- serves: REQ-002 --> "
          "and calls the server with fetch. Found: "
          + ("no functional must requirement in week02/requirements.json." if not fmust
             else f"no such page for {no_page[:4]}."), DEADLINE)

    norun = [str(c.get("id", "?")) for c in live_tcs if str(c.get("run", "")).strip().lower() not in ("server", "web", "manual")]
    check(6, "every test case in week04/test_cases.json says how it is run", bool(tcs) and not norun,
          'Every test case in week04/test_cases.json must say how it is run: "run": "server", "web" or "manual". Found: '
          + (f"missing or wrong in {norun[:4]}." if tcs else "no test cases."), DEADLINE)

    if (ROOT / ".git").exists():
        try:
            tracked = bool(subprocess.run(["git", "ls-files", ".env"], cwd=ROOT, capture_output=True, text=True,
                                          timeout=30).stdout.strip())
        except (subprocess.TimeoutExpired, OSError):
            tracked = False
    else:
        tracked = bool(os.environ.get("AIASD_SLOT")) and (ROOT / ".env").is_file()
    ignore = [ln.strip() for ln in (read(".gitignore") or "").splitlines()]
    listed = any(x in (".env", "/.env", ".env*", "*.env", "**/.env") for x in ignore)
    check(6, ".env is not in the repository, and .gitignore lists it", not tracked and listed,
          ".env must never be committed, and .gitignore must list it. Found: "
          + ("it is in the repository. Remove it with git rm --cached .env and change the password it held."
             if tracked else ".gitignore does not list .env."), DEADLINE)
    example = read(".env.example") or ""
    names = {}
    for ln in example.splitlines():
        if ln.strip() and not ln.strip().startswith("#") and "=" in ln:
            k, v = ln.split("=", 1)
            names[k.strip()] = v.strip()
        elif ln.strip() and not ln.strip().startswith("#"):
            names[ln.strip()] = ""
    missing = [n for n in SMTP_NAMES if n not in names]
    pw = names.get("SMTP_PASSWORD", "")
    pw_value = bool(pw) and not re.fullmatch(r"[<\[(].*[>\])]|your[-_ ].*|changeme|x{3,}|\.\.\.|…", pw, re.I)
    check(6, ".env.example names the e-mail settings, without the password", not missing and not pw_value,
          ".env.example must list the names of your e-mail settings, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD "
          "and SMTP_FROM, with no password after SMTP_PASSWORD=. Found: "
          + (f"missing: {missing}." if missing else "a value after SMTP_PASSWORD=."), DEADLINE)
    shots = [p for p in (ROOT / "week06").glob("email_code.*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")] \
        if (ROOT / "week06").is_dir() else []
    check(6, "week06/email_code.png shows the e-mail with the code", bool(shots),
          "week06/ must hold email_code.png (or .jpg): a screenshot of the e-mail with the login code that your "
          "server sent by real e-mail. Found: no such file.", DEADLINE)

    # --- S2: the app record in the store ------------------------------------------------------------------
    st = load_json("week04/store.json")
    s2 = st.get("S2") if isinstance(st, dict) and isinstance(st.get("S2"), dict) else {}
    ok2 = (re.fullmatch(r"20\d\d-\d\d-\d\d", str(s2.get("date", "")).strip()) and filled(s2.get("app_name"))
           and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+", str(s2.get("package", "")).strip()))
    check(6, "store.json S2 is filled in", bool(ok2),
          "week04/store.json S2 must have the date the app record was created, like 2026-10-31, the app's name in the "
          "store (app_name) and its package name or bundle id (package), such as com.example.studyroom. "
          "Found: one of them missing or wrong.", DEADLINE)
    ev = str(s2.get("evidence", "")).strip().replace("\\", "/")
    ev_ok = (bool(ev) and ".." not in ev and not Path(ev).is_absolute() and ":" not in ev
             and ((ROOT / ev).is_file() or (ROOT / "week04" / ev).is_file()))
    check(6, "store.json S2 screenshot is saved", ev_ok,
          "The file named in 'evidence' in week04/store.json S2 must be saved in week04/. Found: no such file.", DEADLINE)

    # --- the group: the hostile reviewer, on your own feature and the login ----------------------------------
    check_attackers(6)
    check_ai_log(6)


# ── Week 7: the mobile client ─────────────────────────────────────────

MOBILE_BUILD = ("node_modules", "build", ".dart_tool", ".gradle", "Pods", ".expo")  # folders a framework builds again
MOBILE_SOURCE = {".dart", ".js", ".jsx", ".ts", ".tsx", ".kt", ".java", ".swift"}
MOBILE_NAMES = {"flutter": "Flutter", "expo": "React Native–Expo", "gradle": "Kotlin", "xcode": "Swift"}
_MOBILE: dict | None = None


def mobile_project() -> dict:
    """mobile/, read once: {"framework": "Flutter", ... or "", "sources": {path: text}, "ids": [app ids]}.

    The framework is told by the files its own tool writes, at most one folder down (Xcode puts the project in a
    folder of its own): pubspec.yaml (Flutter, first: it has android/ and ios/ too), package.json with expo or
    react-native, a Gradle build (Kotlin), an .xcodeproj (Swift). The app ids are every applicationId of a Gradle
    build, android.package and ios.bundleIdentifier of app.json or app.config, and PRODUCT_BUNDLE_IDENTIFIER of an
    Xcode project (its test targets left out). Build folders and hidden folders are never read."""
    global _MOBILE
    if _MOBILE is not None:
        return _MOBILE
    base = ROOT / "mobile"
    marks: set[str] = set()
    sources: dict[Path, str] = {}
    ids: list[str] = []
    if base.is_dir():
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in MOBILE_BUILD and not d.startswith("."))
            folder = Path(dirpath)
            depth = len(folder.relative_to(base).parts)
            names = set(filenames)
            if folder.suffix == ".xcodeproj" and depth <= 2:
                marks.add("xcode")
            if depth <= 1:
                if "pubspec.yaml" in names:
                    marks.add("flutter")
                if names & {"settings.gradle", "settings.gradle.kts", "build.gradle", "build.gradle.kts"}:
                    marks.add("gradle")
                if "package.json" in names:
                    try:
                        pkg = json.loads((folder / "package.json").read_text(encoding="utf-8", errors="replace"))
                    except (OSError, json.JSONDecodeError):
                        pkg = {}
                    deps = {}
                    for k in ("dependencies", "devDependencies"):
                        if isinstance(pkg, dict) and isinstance(pkg.get(k), dict):
                            deps.update(pkg[k])
                    if "expo" in deps or "react-native" in deps:
                        marks.add("expo")
            for name in filenames:
                p = folder / name
                try:
                    if p.stat().st_size > 1_000_000:
                        continue
                    text = None
                    if p.suffix.lower() in MOBILE_SOURCE or name in (
                            "build.gradle", "build.gradle.kts", "project.pbxproj", "app.json") or (
                            depth <= 1 and name.startswith("app.config.")):
                        text = p.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if text is None:
                    continue
                if p.suffix.lower() in MOBILE_SOURCE and not name.startswith("app.config."):
                    sources[p] = text
                if name in ("build.gradle", "build.gradle.kts"):
                    ids += re.findall(r"(?<![\w.])applicationId\s*=?\s*[\"']([^\"']+)[\"']", text)
                elif name == "project.pbxproj":
                    ids += [i for i in re.findall(r"PRODUCT_BUNDLE_IDENTIFIER\s*=\s*\"?([^\";\s]+)\"?\s*;", text)
                            if "$(" not in i and not i.lower().endswith("tests")]
                elif name == "app.json" and depth <= 1:
                    try:
                        conf = json.loads(text)
                    except json.JSONDecodeError:
                        conf = {}
                    conf = conf.get("expo", conf) if isinstance(conf, dict) else {}
                    for side, key in (("android", "package"), ("ios", "bundleIdentifier")):
                        part = conf.get(side) if isinstance(conf, dict) else None
                        if isinstance(part, dict) and isinstance(part.get(key), str) and part[key].strip():
                            ids.append(part[key].strip())
                elif name.startswith("app.config."):
                    ids += re.findall(r"\b(?:package|bundleIdentifier)\s*:\s*[\"']([^\"']+)[\"']", text)
    framework = next((MOBILE_NAMES[k] for k in ("flutter", "expo", "gradle", "xcode") if k in marks), "")
    _MOBILE = {"framework": framework, "sources": sources, "ids": ids}
    return _MOBILE


def mobile_serves(text: str) -> list[str]:
    """The requirements a source file of mobile/ names in a comment: // serves: REQ-002 (also /* serves: … */)."""
    out: list[str] = []
    for m in re.finditer(r"(?://|/\*)\s*serves:([^\n]*)", text, re.I):
        if "[" not in m.group(1):  # the [placeholder] of an example names nothing
            out += re.findall(r"REQ-\d{3}", m.group(1))
    return out


def mobile_tracked_build() -> list[str]:
    """The build folders of mobile/ that are in git: by git ls-files; in the instructor's capture of a snapshot
    without .git, every file there is a committed one."""
    if (ROOT / ".git").exists():
        try:
            files = subprocess.run(["git", "ls-files", "-z", "mobile"], cwd=ROOT, capture_output=True, text=True,
                                   timeout=60).stdout.split("\0")
        except (subprocess.TimeoutExpired, OSError):
            return []
    elif os.environ.get("AIASD_SLOT") and (ROOT / "mobile").is_dir():
        files = [p.relative_to(ROOT).as_posix() for p in (ROOT / "mobile").rglob("*") if p.is_file()]
    else:
        return []
    return sorted({part for f in files if f for part in f.split("/")[1:-1] if part in MOBILE_BUILD})


# ── live feedback on the commits of the week (VC, 1 Nov 2026) ─────────────────────────────────────────────
# Only in the student's own run on their computer, from Week 7: no mark is read from it (the marks read GitHub).
LIVE_FROM = 7
LIVE_AGENT = re.compile(r"claude|anthropic|copilot|cursor|codex|openai|devin|\[bot\]|gemini|windsurf|aider", re.I)
LIVE_TRAILER = re.compile(r"^\s*(co-authored-by|generated-by):.*(claude|anthropic|copilot|codex|cursor|openai|gemini|devin|"
                          r"aider|\[bot\])|generated (with|by) \[?(claude|copilot|codex|cursor|gemini)", re.I | re.M)


def _git_out(*args: str) -> str | None:
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, errors="replace", timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None
    return p.stdout if p.returncode == 0 else None


def live_pieces(week: int) -> tuple[list, set]:
    """The pieces of the week's lecture work as (name, test on a repository path), and the screen files."""
    if week != 7:
        return [], set()
    screens: dict[str, list[str]] = {}
    for path, text in mobile_project()["sources"].items():
        reqs = mobile_serves(text)
        if reqs:
            screens[Path(path).relative_to(ROOT).as_posix()] = reqs
    login = {p for p, r in screens.items() if "REQ-001" in r}
    own = {p for p, r in screens.items() if "REQ-001" not in r}

    def app(p: str) -> bool:
        return p.startswith("mobile/") and p not in screens and not set(p.split("/")) & set(MOBILE_BUILD)

    def tester(p: str) -> bool:
        return p in ("week07/mobile_runs.json", "week07/group_07.json")

    return [("the app in mobile/", app), ("the login screen", lambda p: p in login),
            ("the screen of your requirement", lambda p: p in own), ("the tester round", tester)], set(screens)


def _filled_at(sha: str, path: str) -> bool:
    """A course JSON file at a commit holds something the student wrote (the course's copy has only empty values)."""
    if not path.endswith(".json"):
        return True
    text = _git_out("show", f"{sha}:{path}") or ""
    return bool(re.search(r'"(?:tc|tester|student_id|device|result|note|what|why)"\s*:\s*"[^"\s]', text))


def _routes_at(rev: str) -> set[str] | None:
    """The routes of server/ at a revision ('METHOD /path'), read as route_defs reads them, the login's own endpoints
    left out. The files are only parsed (ast), never run. None when git cannot be read; an empty set when the
    revision has no server/."""
    global ROOT
    import io
    import tarfile
    try:
        p = subprocess.run(["git", "archive", "--format=tar", rev, "server"], cwd=ROOT, capture_output=True, timeout=60)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if p.returncode != 0:
        return set()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
                for m in tf.getmembers():
                    parts = m.name.split("/")
                    if m.isfile() and m.name.endswith(".py") and not m.name.startswith("/") and ".." not in parts:
                        dest = Path(tmp).joinpath(*parts)
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(tf.extractfile(m).read())
        except (tarfile.TarError, OSError):
            return None
        old, kept = ROOT, list(NOT_INCLUDED)
        ROOT = Path(tmp)
        try:
            return {k for k, (_, node) in route_defs().items() if node is not None}
        finally:
            ROOT = old
            NOT_INCLUDED[:] = kept


def _routes_now() -> set[str]:
    """The routes of server/ as they are on disk now, the login's own endpoints left out."""
    kept = list(NOT_INCLUDED)
    try:
        return {k for k, (_, node) in route_defs().items() if node is not None}
    finally:
        NOT_INCLUDED[:] = kept


def live_commits(week: int) -> list[str]:
    """The commits of this week on this computer, piece by piece: what the commit point will look for (each piece
    in at least two commits, the first while it is unfinished; each new screen and each new route in its own commit,
    VC 2 Nov 2026; also the changes not yet committed that would add two or more). Commits since
    the last Saturday 23:59, by the time on this computer; a commit of a coding agent is left out."""
    import datetime as _dt
    if week < LIVE_FROM or os.environ.get("GITHUB_ACTIONS") or os.environ.get("AIASD_SLOT") or not (ROOT / ".git").exists():
        return []
    if (_git_out("rev-parse", "--is-shallow-repository") or "").strip() == "true":
        return []
    pieces, screens = live_pieces(week)
    if not pieces:
        return []
    now = _dt.datetime.now()
    start = (now - _dt.timedelta(days=(now.weekday() - 5) % 7 or 7)).replace(hour=23, minute=59, second=0, microsecond=0)
    log = _git_out("log", f"--since={start:%Y-%m-%d %H:%M}", "--numstat", "--format=\x1e%h\x1f%an <%ae> %cn <%ce>\x1f%B\x1f")
    if log is None:
        return []
    counts = {name: 0 for name, _ in pieces}
    agent, multi = 0, []
    # VC, 2 Nov 2026: one new screen and one new route per commit. A screen is new in the commit where its file
    # first gets its '// serves:' line (the files a framework's tool creates do not count until then; a move is not
    # new); a route is new when its 'METHOD /path' was not in server/ before the commit.
    renamed: dict[str, dict] = {}
    status = _git_out("log", f"--since={start:%Y-%m-%d %H:%M}", "-M", "--name-status", "--format=\x1e%h") or ""
    for block in status.split("\x1e")[1:]:
        lines = block.strip().splitlines()
        if lines:
            renamed[lines[0].strip()] = {ln.split("\t")[2]: ln.split("\t")[1] for ln in lines[1:]
                                         if ln.startswith("R") and ln.count("\t") == 2}
    serving_cache: dict[str, set[str]] = {}

    def serving(rev: str) -> set[str]:
        """The files of mobile/ that hold a '// serves:' line at a revision (build folders left out)."""
        if rev not in serving_cache:
            found = _git_out("grep", "-l", "-E", r"(//|/\*)[[:space:]]*serves:", rev, "--", "mobile") or ""
            files = {ln.split(":", 1)[1] if ln.startswith(rev + ":") else ln for ln in found.splitlines() if ln}
            serving_cache[rev] = {f for f in files if not set(f.split("/")) & set(MOBILE_BUILD)}
        return serving_cache[rev]

    def new_screens_in(sha: str) -> list[str]:
        before = serving(sha + "^")
        out = []
        for f in sorted(serving(sha) - before):
            if renamed.get(sha, {}).get(f) in before:
                continue   # moved, not new
            if mobile_serves(_git_out("show", f"{sha}:{f}") or ""):   # an example's [placeholder] names nothing
                out.append(f)
        return out
    route_cache: dict[str, set[str] | None] = {}

    def routes(rev: str) -> set[str] | None:
        if rev not in route_cache:
            route_cache[rev] = _routes_at(rev)
        return route_cache[rev]
    for block in log.split("\x1e")[1:]:
        head, _, stats = block.rpartition("\x1f")
        sha, who, msg = (head.split("\x1f", 2) + ["", "", ""])[:3]
        if LIVE_AGENT.search(who) or LIVE_TRAILER.search(msg):
            agent += 1
            continue
        changed = []
        for ln in stats.splitlines():
            parts = ln.split("\t")
            if len(parts) == 3 and (parts[0] == "-" or parts[0].isdigit() and int(parts[0]) > 0):
                changed.append(parts[2])
        for name, test in pieces:
            if any(test(p) and (name != "the tester round" or _filled_at(sha, p)) for p in changed):
                counts[name] += 1
        new_screens = new_screens_in(sha) if any(p.startswith("mobile/") for p in changed) else []
        if len(new_screens) > 1:
            multi.append((sha, "screens", [Path(p).name for p in new_screens]))
        if any(p.startswith("server/") and p.endswith(".py") and "/tests/" not in p for p in changed):
            after, before = routes(sha), routes(sha + "^")
            if after is not None and before is not None and len(after - before) > 1:
                multi.append((sha, "routes", sorted(after - before)))
    out = [say("Your commits this week, piece by piece (read on this computer; your mark reads GitHub):")]
    for name, _ in pieces:
        n = counts[name]
        if n >= 2:
            out.append("  ✓ " + say("{piece}: {n} commits", piece=say(name), n=n))
        elif n == 1:
            out.append("  · " + say("{piece}: 1 commit. Commit it again when it works.", piece=say(name)))
        else:
            out.append("  · " + say("{piece}: no commit yet.", piece=say(name)))
    for sha, kind, names in multi:
        out.append("  ! " + (say("Commit {sha} adds {k} new screens: {names}. Each new screen must have its own commit; a commit that adds two or more costs the commit point.", sha=sha, k=len(names), names=", ".join(names))
                             if kind == "screens" else
                             say("Commit {sha} adds {k} new routes: {names}. Each new route must have its own commit; a commit that adds two or more costs the commit point.", sha=sha, k=len(names), names=", ".join(names))))
    # Before the commit, while splitting is still easy: what the changes not yet committed would add.
    st = _git_out("status", "--porcelain", "-uall", "--", "mobile") or ""
    moved_from = {ln[3:].split(" -> ", 1)[1].strip('"'): ln[3:].split(" -> ", 1)[0].strip('"')
                  for ln in st.splitlines() if ln[:1] == "R" and " -> " in ln[3:]}
    head_serving = serving("HEAD")
    pending_screens = sorted(Path(f).name for f in screens if f not in head_serving and moved_from.get(f) not in head_serving)
    if len(pending_screens) > 1:
        out.append("  ! " + say("Your changes not yet committed add {k} new screens: {names}. Commit them one at a time.", k=len(pending_screens), names=", ".join(pending_screens)))
    head = routes("HEAD")
    if head is not None:
        pending_routes = sorted(_routes_now() - head)
        if len(pending_routes) > 1:
            out.append("  ! " + say("Your changes not yet committed add {k} new routes: {names}. Commit them one at a time; git add -p lets you take the lines of one route first.", k=len(pending_routes), names=", ".join(pending_routes)))
    ahead = _git_out("rev-list", "--count", "@{upstream}..HEAD")
    if ahead is None:
        ahead = _git_out("rev-list", "--count", "origin/main..HEAD")
    if ahead and ahead.strip().isdigit() and int(ahead) > 0:
        n = int(ahead)
        out.append("  ! " + (say("1 commit is not pushed yet. Push it now: git push") if n == 1 else
                             say("{n} commits are not pushed yet. Push them now: git push", n=n)))
    if agent:
        out.append("  · " + (say("1 commit by a coding agent is not counted.") if agent == 1 else
                             say("{n} commits by a coding agent are not counted.", n=agent)))
    return out


def is_commit(sha: str) -> bool | None:
    """Whether sha is a commit of this repository; None when there is no history to look in (no .git, or a shallow
    clone, as in GitHub Actions)."""
    if not (ROOT / ".git").exists():
        return None
    try:
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True,
                                 text=True, timeout=30).stdout.strip() == "true"
        if shallow:
            return None
        return subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"], cwd=ROOT, capture_output=True,
                              timeout=30).returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return None


def week7() -> None:
    """The mobile client: an app in mobile/ (Flutter, React Native–Expo, Kotlin or Swift) that calls the same server,
    with the same token. In the lecture: the app, the login screen on the phone (phone_login.png), a screen of your own
    feature, and the tester round (mobile_runs.json and group_07.json, typed by you). By Saturday: every functional must
    requirement on the phone and tested there, the app id = the package of S2, no build files in git, the tests still
    green, and the AI log (small diffs, AI_Doc5 §6)."""
    musts, fmust = must_requirements()
    own = fmust - {"REQ-001"}
    eps = api_endpoints()
    mob = mobile_project()
    src = mob["sources"]
    code = "\n".join(src.values())
    there = (ROOT / "mobile").is_dir()

    # --- in the lecture: the app, the login on the phone, a screen of your own feature ------------------------
    check(7, "mobile/ holds your app, made with Flutter, React Native–Expo, Kotlin or Swift", bool(mob["framework"]),
          "mobile/, at the root of your repository, must hold your app, created with the tool of your framework: "
          "Flutter (pubspec.yaml), React Native–Expo (package.json with expo or react-native), Kotlin (a Gradle build) "
          "or Swift (an Xcode project). Found: " + ("no mobile/ folder." if not there else "none of these."))

    data, bad = login_contract()
    login_keys = []
    if data is not None and not bad:
        for k in ("request_code", "login", "me"):
            method, route = data[k].strip().split(None, 1)
            login_keys.append(f"{method.upper()} {norm_path(route.strip())}")
    login_files = [p for p, text in src.items() if "REQ-001" in mobile_serves(text)]
    not_called = [k for k in login_keys if not calls_path(code, k)]
    check(7, "mobile/ has a login screen with serves: REQ-001 that sends requests to your three login endpoints",
          bool(login_files) and bool(login_keys) and not not_called,
          "mobile/ must have a login screen whose source file names REQ-001 in a comment like // serves: REQ-001, and "
          "your app must send requests to the three endpoints of server/login_contract.json (request_code, login and "
          "me). Write the path of each endpoint with its /, as in week05/api.md. Found: "
          + ("no mobile/ folder." if not there
             else "no source file in mobile/ (.dart, .js, .ts, .kt, .java or .swift)." if not src
             else "no source file in mobile/ names REQ-001 in a serves: comment." if not login_files
             else "server/login_contract.json is not filled in." if not login_keys
             else f"no request to: {not_called}."))
    shots = [p for p in (ROOT / "week07").glob("phone_login.*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")] \
        if (ROOT / "week07").is_dir() else []
    check(7, "week07/phone_login.png shows the login on the phone", bool(shots),
          "week07/ must hold phone_login.png (or .jpg): a screenshot of the phone, or of the emulator, that shows the "
          "logged-in user's address after the login. Found: no such file.")

    own_rows = [e for e in eps if set(e["reqs"]) & own]
    screens = {r for text in src.values() for r in mobile_serves(text)} & own
    calling = [r for r in screens if any(calls_path(code, e["key"]) for e in own_rows if r in e["reqs"])]
    check(7, "mobile/ has a screen of one of your own must requirements that sends requests to its endpoints",
          bool(calling),
          "mobile/ must have a screen of one of your own functional must requirements (not the login, REQ-001): its "
          "source file names the requirement in a comment like // serves: REQ-002, and your app sends requests to an "
          "endpoint of week05/api.md that serves it. Found: "
          + ("no mobile/ folder." if not there
             else "no source file in mobile/ (.dart, .js, .ts, .kt, .java or .swift)." if not src
             else "no functional must requirement besides REQ-001 in week02/requirements.json." if not own
             else "no source file in mobile/ names one of them in a serves: comment." if not screens
             else "the app sends no request to their endpoints in week05/api.md."))

    # --- in the lecture: the tester round --------------------------------------------------------------------
    testers = check_collaborator(7, "tester", who="tester")
    tester = testers[0] if testers else ""
    cases = test_cases() or []
    known = {str(c.get("id", "")).strip() for c in cases}
    live = {str(c.get("id", "")).strip(): str(c.get("req", "")).strip() for c in cases if not c.get("dropped")}
    dropped = known - set(live)

    def req_of(tc: str) -> str:
        return live.get(tc) or (f"REQ-{tc[3:6]}" if re.fullmatch(r"TC-\d{3}-\d{2}", tc) else "")

    raw = load_json("week07/mobile_runs.json")
    runs = raw.get("runs", raw) if isinstance(raw, dict) else raw
    if not isinstance(runs, list):
        check(7, "week07/mobile_runs.json is valid JSON", False,
              "week07/mobile_runs.json is missing or is not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.")
        runs = []
    runs = [r for r in runs if isinstance(r, dict) and (filled(r.get("tc")) or filled(r.get("tester")))]
    tc_of = {id(r): str(r.get("tc", "")).strip() for r in runs}
    result = {id(r): str(r.get("result", "")).strip().lower() for r in runs}
    round1 = [r for r in runs if round_of(r) == 1]
    by_tester = [r for r in round1 if tester and str(r.get("tester", "")).strip().split("-")[0] == tester]
    no_runs7 = "Found: no runs recorded in week07/mobile_runs.json yet."
    check(7, "mobile_runs.json: your tester ran at least three test cases on your phone", len(by_tester) >= 3,
          "Your tester, the student named in week07/group_07.json, must run at least three of your test cases on your "
          "phone in round 1, each run recorded under their student number. "
          + (no_runs7 if not runs else "Found: no tester in week07/group_07.json." if not tester
             else f"Found: {pl(len(by_tester), 'run')} by your tester in round 1."))
    outside = [r for r in by_tester if req_of(tc_of[id(r)]) not in ("", "REQ-001")]
    check(7, "mobile_runs.json: at least one of your tester's runs is outside the login", bool(outside),
          "At least one of your tester's runs in round 1 must be a test case outside the login (REQ-001): a test case "
          "of your own feature. " + (no_runs7 if not runs else "Found: none."))
    unknown = sorted({tc_of[id(r)] for r in runs} - known)
    check(7, "mobile_runs.json: every run names a test case from test_cases.json", bool(runs) and not unknown,
          "Every run in week07/mobile_runs.json must name a test case that exists in week04/test_cases.json. "
          + (no_runs7 if not runs else f"Found: not in test_cases.json: {unknown[:3]}."))
    odd = [r for r in runs if result[id(r)] not in ("pass", "fail", "blocked") or not filled(r.get("device"))
           or (result[id(r)] in ("fail", "blocked") and len(str(r.get("note", "")).strip()) < 15)]
    check(7, "mobile_runs.json: every run names the device and has a result, with a note for fail and blocked",
          bool(runs) and not odd,
          "Every run in week07/mobile_runs.json must name the phone or the emulator (device) and have a result (pass, fail or "
          "blocked), with a note of at least 15 characters for fail and blocked. "
          + (no_runs7 if not runs else f"Found: {pl(len(odd), 'run')} without a device or a valid result, or a fail or "
             "blocked without a note."))

    # --- by Saturday: every functional must requirement on the phone, and tested there -------------------------
    served = {r for text in src.values() for r in mobile_serves(text)}
    no_screen = sorted(fmust - served)
    check(7, "every functional must requirement has a screen in mobile/", bool(fmust) and not no_screen,
          "Every functional must requirement needs a screen in mobile/ whose source file names it in a comment like "
          "// serves: REQ-002. Found: "
          + ("no functional must requirement in week02/requirements.json." if not fmust
             else f"no such screen for {no_screen[:4]}."), DEADLINE)
    fm_rows = [e for e in eps if set(e["reqs"]) & fmust]
    uncalled = [e["key"] for e in fm_rows if not calls_path(code, e["key"])]
    check(7, "your app sends requests to every endpoint of week05/api.md that serves a functional must requirement",
          bool(fm_rows) and not uncalled,
          "Your app in mobile/ must send requests to every endpoint of week05/api.md that serves a functional must "
          "requirement. Write the path of each endpoint with its /, as in api.md. Found: "
          + ("no row of week05/api.md serves a functional must requirement." if not fm_rows
             else f"no request to: {uncalled[:4]}."), DEADLINE)
    passed = {req_of(tc_of[id(r)]) for r in runs if result[id(r)] == "pass" and tc_of[id(r)] in live}
    untested = sorted(fmust - passed)
    check(7, "every functional must requirement has a test case that passed on the phone", bool(fmust) and not untested,
          "Every functional must requirement needs at least one of its test cases with a pass in week07/mobile_runs.json. Found: "
          + ("no functional must requirement in week02/requirements.json." if not fmust
             else f"no pass for {untested[:4]}."), DEADLINE)
    failed = {tc_of[id(r)] for r in round1 if result[id(r)] == "fail"}
    rerun = {tc_of[id(r)] for r in runs if round_of(r) == 2}
    open_fails = sorted(failed - rerun - dropped)
    check(7, "mobile_runs.json: every failed test case was run again in round 2", bool(runs) and not open_fails,
          "Every test case that failed on the phone in round 1 must be run again in round 2 after the fix, or dropped "
          "with a change request. " + (no_runs7 if not runs else f"Found: no round 2 for {open_fails[:3]}."), DEADLINE)

    st = load_json("week04/store.json")
    s2 = st.get("S2") if isinstance(st, dict) and isinstance(st.get("S2"), dict) else {}
    package = str(s2.get("package", "")).strip()
    wrong = sorted({i for i in mob["ids"] if i != package})
    check(7, "the app id in mobile/ is the package of S2 in week04/store.json",
          bool(package) and bool(mob["ids"]) and not wrong,
          "The id of your app (applicationId in build.gradle, android.package and ios.bundleIdentifier in app.json, or "
          "PRODUCT_BUNDLE_IDENTIFIER in Xcode) must be the package name of S2 in week04/store.json. Found: "
          + ("no package in S2 of week04/store.json." if not package else "no app id in mobile/." if not mob["ids"]
             else f"{wrong[:3]}, not {package}."), DEADLINE)
    tracked = mobile_tracked_build()
    check(7, "no build files of mobile/ are in git", there and not tracked,
          "mobile/ must not have in git the folders your framework builds again (node_modules, build, .dart_tool, "
          ".gradle, Pods, .expo): add them to mobile/.gitignore, then git rm -r --cached mobile/<the folder>. Found: "
          + ("no mobile/ folder." if not there else f"in git: {tracked}."), DEADLINE)

    # --- by Saturday: the server and the web stay green -------------------------------------------------------
    res = test_results()
    if not res["ran"]:
        ok, found = False, res["why"]
    else:
        red = [f"LOGIN_{n}" for n in LOGIN_TESTS if res["outcomes"].get(f"LOGIN_{n}", ("", ""))[0] != "passed"]
        ok, found = not red, f"not passing: {red[:4]}"
    check(7, "all ten course tests still pass", ok,
          f"All ten course tests (course_tests/) must still pass. Found: {found}.", DEADLINE)
    server_tc = sorted({str(c.get("id", "")).strip() for c in cases if not c.get("dropped")
                        and str(c.get("req", "")).strip() in musts and str(c.get("run", "")).strip().lower() == "server"})
    if not res["ran"]:
        ok, found = False, res["why"]
    elif not server_tc:
        ok, found = False, 'no test case of a must requirement with "run": "server"'
    else:
        failing = [i for i in server_tc if res["outcomes"].get(i, ("", ""))[0] != "passed"]
        ok, found = not failing, f"no passing test for {failing[:4]}"
    check(7, 'every test case of a must requirement with run "server" still has a test that passes', ok,
          'Every test case of a must requirement with "run": "server" in week04/test_cases.json must still have a test '
          f"in server/tests/ named by its id that passes. Found: {found}.", DEADLINE)

    # --- by Saturday: the AI log, small diffs ------------------------------------------------------------------
    log = ai_log_section(7)
    shas = re.findall(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])", log)
    # without the history, a commit id must have a letter: a student number or a date is not one
    named = [s for s in shas if is_commit(s) or (is_commit(s) is None and re.search(r"[a-f]", s))]
    check(7, "week07/ai_log_07.md names the commit of the change you accepted", bool(named),
          "week07/ai_log_07.md must name the commit of the change you accepted: the first 7 characters of its commit "
          "id, outside the comments and the Evidence block. Found: "
          + ("no commit id." if not shas else f"{shas[:2]}, not a commit of this repository."), DEADLINE)
    check(7, "week07/ai_log_07.md holds the git diff of the change", bool(re.search(
          r"^\s*(diff --git |@@ -\d)", ai_log_evidence(7), re.M)),
          "week07/ai_log_07.md must hold, in the Evidence block, the git diff of the change as your terminal showed it "
          "(the lines that start with diff --git and @@). Found: none.", DEADLINE)
    check_ai_log(7)


CHECKS = {1: week1, 2: week2, 3: week3, 4: week4, 5: week5, 6: week6, 7: week7}


# ── secrets: this one runs for every week ────────────────────────────

SECRET_PATTERNS = [
    (r"sk-ant-[A-Za-z0-9\-_]{10,}", "Anthropic API key"),
    (r"AIza[0-9A-Za-z\-_]{30,}", "Google API key"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI-style API key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub token"),
]


SECRET_SKIP = {".git", ".venv", "venv", *MOBILE_BUILD}  # never walked into: git's own files, packages, build output
SECRET_SUFFIXES_BEFORE_7 = {".py", ".md", ".txt", ".json", ".toml", ".yml", ".yaml", ".mmd", ""}
# From Week 7 (VC, 31 Oct 2026) the app's own code too: a key in an app is a key in every copy of the app.
# Weeks 1-6 keep the old list, so a capture of an earlier week reads what the students were told then.
SECRET_SUFFIXES = SECRET_SUFFIXES_BEFORE_7 | {*MOBILE_SOURCE, ".kts", ".gradle", ".xml", ".plist", ".properties"}


def _secret_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SECRET_SKIP]
        for name in filenames:
            yield Path(dirpath) / name


def check_secrets() -> bool:
    """Scan the text files of the repository for anything that looks like a live key."""
    clean = True
    suffixes = SECRET_SUFFIXES if RUN_WEEK >= 7 else SECRET_SUFFIXES_BEFORE_7
    for path in _secret_files():
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        # Firebase's files for the app (Android, iOS): their API key only names the Firebase project
        if path.name in {"check_deliverables.py", ".env.example", "google-services.json", "GoogleService-Info.plist"}:
            continue
        if path.name == ".env" or path.name.startswith(".env."):
            continue  # keys belong in .env (git ignores it); only files that can be committed are scanned
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, text):
                rel = path.relative_to(ROOT)
                print("  " + say("SECRET  {rel} — looks like a {label}", rel=rel, label=label))
                clean = False
    return clean


# ── Türkçe: `python .github/check_deliverables.py tr` ─────────────────────────────────────
# The checker speaks English by default and for the instructor's capture (AIASD_SLOT set: always
# English). A student can ask for Turkish by adding `tr` (also `2 tr`, `tr 2`). The Turkish is
# NOT written beside each check: it is looked up here, by the English sentence the check
# printed, so the instructor's tools (grading/tr_checks.py → the Turkish block of an issue)
# read the very same table. One entry per sentence the checker can print — the PASS sentence and
# every FAIL sentence of a check:  (English template, Turkish template).
#   {name} stands for any text in the sentence and is available in the Turkish template under
#   the same name ({n} is a number); {{ and }} are literal braces. First match wins, so a
#   more specific sentence goes before a general one. A sentence without an entry is shown in
#   English and counted at the end of the run. When you change a sentence in a check above,
#   change its entry here; `aiasd-claude/scripts/check_tr_coverage.py` lists the ones that
#   no longer match. Weeks in TR_WEEKS are fully covered; a later week is shown in English.

TR_WEEKS = frozenset({1, 2, 3, 4, 5, 6, 7})

TR_RULES: list[tuple[str, str]] = [
    # --- every week: the AI log ---------------------------------------------------------------
    ("{p} must be filled in, in your own words. Found: the section is empty or untouched.",
     "{p} kendi sözlerinle doldurulmalı. Bulunan: bölüm boş ya da hiç dokunulmamış."),
    ("{p} must contain the real conversation, pasted inside the code block. Found: {n} {u} there.",
     "{p} içinde gerçek konuşma, kod bloğunun içine yapıştırılmış olarak bulunmalı. Bulunan: orada {n} karakter."),
    ("{p} holds the real conversation, pasted in the code block",
     "{p} içinde gerçek konuşma kod bloğuna yapıştırılmış"),
    ("{p} is filled in", "{p} dolu"),
    # --- Week 1: student.json ------------------------------------------------------------------
    ("student.json is missing from the repository root. Restore it: it holds your student number and section.",
     "student.json reponun kök klasöründe yok. Geri yükle: öğrenci numaranı ve şubeni içerir."),
    ("student.json is not valid JSON ({e}). Check the commas and the quotation marks.",
     "student.json geçerli bir JSON değil ({e}). Virgüllere ve tırnak işaretlerine bak."),
    ("student.json is not fully filled in. Empty fields: {f}. Fill in every field.",
     "student.json tam doldurulmamış. Boş alanlar: {f}. Her alanı doldur."),
    ("student.json is fully filled in", "student.json tam dolu"),
    ("student_id in student.json must be your student number, digits only. Found: {v}.",
     "student.json içindeki student_id öğrenci numaran olmalı, yalnızca rakamlardan oluşmalı. Bulunan: {v}."),
    ("student_id in student.json is a number", "student.json içindeki student_id bir sayı"),
    ("nickname in student.json must be 2-20 characters: letters, digits, - and _ only. Found: {v}.",
     "student.json içindeki nickname 2-20 karakter olmalı: yalnızca harf, rakam, - ve _ . Bulunan: {v}."),
    ("nickname in student.json can go on the class board",
     "student.json içindeki nickname sınıf panosuna konabilir"),
    ("section in student.json must be 'en' or 'tr'. Found: {v}. This is how your repository knows which week to check.",
     "student.json içindeki section 'en' ya da 'tr' olmalı. Bulunan: {v}. Reponun hangi haftayı kontrol edeceğini böyle bilir."),
    ("section in student.json is 'en' or 'tr'", "student.json içindeki section 'en' ya da 'tr'"),
    # --- Week 1: the files ---------------------------------------------------------------------
    ("week01/setup_proof.md is missing or too short. Create it and fill it in as the Week 1 assignment says.",
     "week01/setup_proof.md eksik ya da çok kısa. 1. hafta ödevinde yazdığı gibi oluştur ve doldur."),
    ("week01/setup_proof.md is there and long enough", "week01/setup_proof.md var ve yeterince uzun"),
    ("week01/hello.py is missing or has a syntax error. Create it, or run it to see the error.",
     "week01/hello.py eksik ya da sözdizimi hatası var. Oluştur ya da hatayı görmek için çalıştır."),
    ("week01/hello.py has no syntax error", "week01/hello.py içinde sözdizimi hatası yok"),
    ('week01/hello.py must contain an f-string, for example f"Hello {{name}}". Found: none.',
     'week01/hello.py içinde bir f-string olmalı, örneğin f"Hello {{name}}". Bulunan: yok.'),
    ("week01/hello.py contains an f-string", "week01/hello.py içinde f-string var"),
    ('week01/hello.py must contain a list, for example names = ["Ada", "Alan"]. Found: none.',
     'week01/hello.py içinde bir liste olmalı, örneğin names = ["Ada", "Alan"]. Bulunan: yok.'),
    ("week01/hello.py contains a list", "week01/hello.py içinde liste var"),
    ("week01/hello.py must contain a for-loop, for example: for name in names: ... Found: none.",
     "week01/hello.py içinde bir for döngüsü olmalı, örneğin: for name in names: ... Bulunan: yok."),
    ("week01/hello.py contains a for-loop", "week01/hello.py içinde for döngüsü var"),
    ("week01/hello.py must ask the user for input with input(). Found: input() is never called.",
     "week01/hello.py kullanıcıdan input() ile girdi istemeli. Bulunan: input() hiç çağrılmıyor."),
    ("week01/hello.py asks the user for input", "week01/hello.py kullanıcıdan girdi istiyor"),
    ("week01/llm_notes.md must have about 300 words written by you. Found: {n}. Headings, instructions and pasted blocks do not count.",
     "week01/llm_notes.md içinde senin yazdığın yaklaşık 300 kelime olmalı. Bulunan: {n}. Başlıklar, yönergeler ve yapıştırılmış bloklar sayılmaz."),
    ("week01/llm_notes.md has about 300 words of your own",
     "week01/llm_notes.md içinde kendi yazdığın yaklaşık 300 kelime var"),
    (".gitignore must contain .venv and .env, so they are never committed. Add both lines.",
     ".gitignore içinde .venv ve .env bulunmalı, böylece asla commit edilmezler. İki satırı da ekle."),
    (".gitignore covers .venv and .env", ".gitignore .venv ve .env'i kapsıyor"),
    (".env.example is missing. Create it with the NAMES of your settings only, never the secret values.",
     ".env.example eksik. Yalnızca ayarlarının ADLARIYLA oluştur, gizli değerleri asla yazma."),
    # --- the proposal (Weeks 2, 3) -------------------------------------------------------------
    ("PROPOSAL.md is missing, or its numbered headings were changed. Restore the headings from the template.",
     "PROPOSAL.md eksik ya da numaralı başlıkları değiştirilmiş. Başlıkları şablondan geri yükle."),
    ("PROPOSAL.md is in the repository root with its headings",
     "PROPOSAL.md reponun kök klasöründe ve başlıkları yerinde"),
    ("{l} has lost its heading, or the heading was changed. Restore the heading from the template.",
     "{l} başlığını kaybetmiş ya da başlık değiştirilmiş. Başlığı şablondan geri yükle."),
    ("{l} has its heading", "{l} başlığı yerinde"),
    ("{l} is not written yet. Found: {n} {u}. Write your own text under that heading.",
     "{l} henüz yazılmamış. Bulunan: {n} karakter. Bu başlığın altına kendi metnini yaz."),
    ("{l} is written", "{l} yazılmış"),
    # --- classmates and group files (Weeks 2, 3, 4) -------------------------------------------
    ("{p} is missing or is not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.",
     "{p} eksik ya da geçerli bir JSON değil. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır; virgüllere ve tırnak işaretlerine de bak."),
    ("{p} is missing, empty or not valid JSON. Run the checker online to fetch it, and check the commas and quotation marks.",
     "{p} eksik, boş ya da geçerli bir JSON değil. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır; virgüllere ve tırnak işaretlerine de bak."),
    ("{p} is missing or is not valid JSON. Run the checker online to fetch it.",
     "{p} eksik ya da geçerli bir JSON değil. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır."),
    ("{p} is valid JSON", "{p} geçerli bir JSON"),
    ("{p} may list at most two classmates, each with a valid 9-digit student number, all different. Found: {n} {u}, {m} with a valid number.",
     "{p} en fazla iki sınıf arkadaşı içerebilir; her birinin geçerli 9 haneli öğrenci numarası olmalı ve hepsi farklı olmalı. Bulunan: {n} giriş, {m} tanesinde geçerli numara var."),
    ("{p} lists 0-2 classmates with valid numbers", "{p} geçerli numaralı 0-2 sınıf arkadaşı içeriyor"),
    ("{p} must not list you. Your own student number is in it: remove that entry.",
     "{p} içinde sen yer almamalısın. Kendi öğrenci numaran listede: o girişi sil."),
    ("{p} does not list you", "{p} içinde sen yoksun"),
    ("{p} must give everyone listed the role '{r}'. Found: a wrong or empty role.",
     "{p} içinde listelenen herkesin rolü '{r}' olmalı. Bulunan: yanlış ya da boş bir rol."),
    ("{p} must give everyone the role '{r}'. Found: a wrong or empty role.",
     "{p} içinde herkesin rolü '{r}' olmalı. Bulunan: yanlış ya da boş bir rol."),
    ("{p} gives everyone the role '{r}'", "{p} içinde herkesin rolü '{r}'"),
    ("{p} must say, for each person, what they did, in a real sentence. Found: {n} {u} without one.",
     "{p} içinde her kişi için ne yaptığı gerçek bir cümleyle yazılmalı. Bulunan: {n} giriş bunu içermiyor."),
    ("{p} says what each person did", "{p} içinde her kişinin ne yaptığı yazılmış"),
    # --- Week 2: requirements, SRS ------------------------------------------------------------
    ("week02/requirements.json is missing. Run the checker online to fetch it, then fill it in.",
     "week02/requirements.json eksik. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır, sonra doldur."),
    ("{p} is in the repository", "{p} repoda"),
    ("week02/requirements.json is not valid JSON ({e}). Check the commas and the quotation marks.",
     "week02/requirements.json geçerli bir JSON değil ({e}). Virgüllere ve tırnak işaretlerine bak."),
    ("week02/requirements.json needs at least 8 filled-in requirements. Found: {n}.",
     "week02/requirements.json içinde en az 8 dolu gereksinim olmalı. Bulunan: {n}."),
    ("week02/requirements.json has at least 8 filled-in requirements",
     "week02/requirements.json içinde en az 8 dolu gereksinim var"),
    ("Every requirement id in week02/requirements.json must look like REQ-001, and none may be repeated. Found: no requirements filled in yet.",
     "week02/requirements.json içindeki her gereksinim id'si REQ-001 gibi görünmeli ve hiçbiri tekrarlanmamalı. Bulunan: henüz dolu gereksinim yok."),
    ("Every requirement id in week02/requirements.json must look like REQ-001, and none may be repeated. Found: wrong ids {a}, repeated ids {b}.",
     "week02/requirements.json içindeki her gereksinim id'si REQ-001 gibi görünmeli ve hiçbiri tekrarlanmamalı. Bulunan: yanlış id'ler {a}, tekrarlanan id'ler {b}."),
    ("every requirement id looks like REQ-001 and none is repeated",
     "her gereksinim id'si REQ-001 gibi ve hiçbiri tekrarlanmıyor"),
    ("week02/requirements.json needs at least 5 functional and 3 non-functional requirements. Found: {f} functional, {g} non-functional.",
     "week02/requirements.json içinde en az 5 işlevsel ve 3 işlevsel olmayan gereksinim olmalı. Bulunan: {f} işlevsel, {g} işlevsel olmayan."),
    ("week02/requirements.json has at least 5 functional and 3 non-functional requirements",
     "week02/requirements.json içinde en az 5 işlevsel ve 3 işlevsel olmayan gereksinim var"),
    ("week02/requirements.json must keep a non-functional requirement about the phone screen. Found: none that mentions it.",
     "week02/requirements.json içinde telefon ekranıyla ilgili işlevsel olmayan bir gereksinim kalmalı. Bulunan: bunu anan yok."),
    ("the requirement about the phone screen is still there", "telefon ekranıyla ilgili gereksinim hala yerinde"),
    ("Every requirement in week02/requirements.json must have a priority: must, should or could. Cannot pass yet: fewer than 8 requirements.",
     "week02/requirements.json içindeki her gereksinimin bir önceliği olmalı: must, should ya da could. Henüz geçemez: 8'den az gereksinim var."),
    ("Every requirement in week02/requirements.json must have a priority: must, should or could. Found: missing or wrong in {x}.",
     "week02/requirements.json içindeki her gereksinimin bir önceliği olmalı: must, should ya da could. Bulunan: eksik ya da yanlış olanlar {x}."),
    ("every requirement has a priority: must, should or could", "her gereksinimin önceliği var: must, should ya da could"),
    ("Not every requirement may be 'must': mark the ones that could be cut as should or could. Cannot pass yet: fewer than 8 requirements.",
     "Her gereksinim 'must' olamaz: çıkarılabilecek olanları should ya da could olarak işaretle. Henüz geçemez: 8'den az gereksinim var."),
    ("Not every requirement may be 'must': mark the ones that could be cut as should or could. Found: all of them are 'must'.",
     "Her gereksinim 'must' olamaz: çıkarılabilecek olanları should ya da could olarak işaretle. Bulunan: hepsi 'must'."),
    ("not every requirement is 'must'", "her gereksinim 'must' değil"),
    ("Every requirement must have an acceptance criterion, one sentence saying how to test it. Cannot pass yet: fewer than 8 requirements.",
     "Her gereksinimin bir kabul ölçütü olmalı: nasıl test edileceğini söyleyen tek cümle. Henüz geçemez: 8'den az gereksinim var."),
    ("Every requirement must have an acceptance criterion, one sentence saying how to test it. Found: missing or too short in {x}.",
     "Her gereksinimin bir kabul ölçütü olmalı: nasıl test edileceğini söyleyen tek cümle. Bulunan: eksik ya da çok kısa olanlar {x}."),
    ("every requirement has an acceptance criterion", "her gereksinimin kabul ölçütü var"),
    ("PROPOSAL.md §5 must mention all three parts: mobile, web and server. Found: at least one is missing.",
     "PROPOSAL.md §5 üç parçanın hepsini anmalı: mobile, web ve server. Bulunan: en az biri eksik."),
    ("PROPOSAL.md §5 names mobile, web and server", "PROPOSAL.md §5 mobile, web ve server'ı anıyor"),
    ("PROPOSAL.md §5 must contain the system context diagram, written as a ```mermaid block. Found: no such block.",
     "PROPOSAL.md §5 içinde ```mermaid bloğu olarak yazılmış sistem bağlam diyagramı bulunmalı. Bulunan: böyle bir blok yok."),
    ("PROPOSAL.md §5 has its system context diagram", "PROPOSAL.md §5 içinde sistem bağlam diyagramı var"),
    ("week02/SRS.md must be filled in. Found: the file is missing, or it is still the template.",
     "week02/SRS.md doldurulmalı. Bulunan: dosya eksik ya da hala şablon."),
    ("SRS.md must have a use case diagram with at least 3 use cases. Found: {n}.",
     "SRS.md içinde en az 3 use case içeren bir use case diyagramı olmalı. Bulunan: {n}."),
    ("SRS.md has a use case diagram with at least 3 use cases",
     "SRS.md içinde en az 3 use case'li bir use case diyagramı var"),
    ("SRS.md §4 must say that the requirements are in week02/requirements.json, or list every REQ id. Found: no requirements filled in yet.",
     "SRS.md §4, gereksinimlerin week02/requirements.json içinde olduğunu söylemeli ya da her REQ id'sini listelemeli. Bulunan: henüz dolu gereksinim yok."),
    ("SRS.md §4 must say that the requirements are in week02/requirements.json, or list every REQ id. Found: missing {x}.",
     "SRS.md §4, gereksinimlerin week02/requirements.json içinde olduğunu söylemeli ya da her REQ id'sini listelemeli. Bulunan: eksik olanlar {x}."),
    ("SRS.md §4 points to requirements.json, or lists every REQ id",
     "SRS.md §4 requirements.json'u gösteriyor ya da her REQ id'sini listeliyor"),
    # --- student.json / .env.example in the repository root (Week 1 passes) ---------------------
    ("{p} is in the repository root", "{p} reponun kök klasöründe"),
    # --- Week 3: the pitch ----------------------------------------------------------------------
    ("week03/PITCH_03.md is missing. Run the checker online to fetch it, then write it.",
     "week03/PITCH_03.md eksik. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır, sonra yaz."),
    ("PITCH_03.md must have 7 slides: your six and the fixed reviewers' slide. Found: {n}. "
     "Slides are separated by a line that contains only ---.",
     "PITCH_03.md 7 slayttan oluşmalı: senin altı slaydın ve sabit reviewer slaydı. Bulunan: {n}. "
     "Slaytlar yalnızca --- yazan bir satırla ayrılır."),
    ("PITCH_03.md has 7 slides", "PITCH_03.md 7 slayttan oluşuyor"),
    ("PITCH_03.md still has {n} {u} of [bracketed] text. Replace each one with your own words and "
     "delete the square brackets too: text left inside [ ] still counts as not filled in.",
     "PITCH_03.md içinde hala [köşeli parantez] içinde {n} parça metin var. Her birini kendi sözlerinle değiştir "
     "ve köşeli parantezleri de sil: [ ] içinde kalan metin hala doldurulmamış sayılır."),
    ("PITCH_03.md has no [bracketed] text left", "PITCH_03.md içinde [köşeli parantezli] metin kalmamış"),
    ("Slide 2 must tell the last time this problem happened to you or in front of you: when, where, "
     "what you did instead, what it cost. Found: too short, or [brackets] left.",
     "Slayt 2'de bu sorunun en son sana ya da gözünün önünde ne zaman yaşandığı anlatılmalı: ne zaman, nerede, "
     "onun yerine ne yaptığın, bedeli ne oldu. Bulunan: çok kısa ya da [köşeli parantez] kalmış."),
    ("slide 2 tells the last time it happened", "slayt 2 sorunun en son ne zaman yaşandığını anlatıyor"),
    ("Slide 3 must list five testers, one name per row of its table. Found: {n} {u}.",
     "Slayt 3'te beş tester yazılmalı, tablonun her satırında bir isim. Bulunan: {n} dolu satır."),
    ("slide 3 names five testers in its table", "slayt 3 tablosunda beş tester'ın adı var"),
    ("Slide 4 must list three requirements copied word for word (id and description) from "
     "week02/requirements.json. Found: {x} of {y} listed match. Copy them, do not paraphrase.",
     "Slayt 4'te week02/requirements.json dosyasından kelimesi kelimesine kopyalanmış üç gereksinim (id ve açıklama) "
     "listelenmeli. Bulunan: listelenen {y} gereksinimden {x} tanesi eşleşiyor. Kopyala, kendi sözlerinle yazma."),
    ("Slide 4 must list three requirements copied word for word (id and description) from "
     "week02/requirements.json. Found: none listed in the form: 1. REQ-001 — description.",
     "Slayt 4'te week02/requirements.json dosyasından kelimesi kelimesine kopyalanmış üç gereksinim (id ve açıklama) "
     "listelenmeli. Bulunan: \"1. REQ-001 — açıklama\" biçiminde yazılmış hiçbiri yok."),
    ("slide 4 lists three requirements copied from requirements.json",
     "slayt 4 requirements.json dosyasından kopyalanmış üç gereksinimi listeliyor"),
    ('Slide 4 must say what the app does NOT do, in one sentence that starts with "It does not:" '
     '(in Turkish: "Yapmaz:"), the sentence from §4 of your proposal. Found: none.',
     'Slayt 4\'te uygulamanın NE YAPMADIĞI tek cümleyle yazılmalı; cümle "Yapmaz:" ile başlamalı '
     '(İngilizce yazarsan "It does not:"). Bu, önerinin 4. bölümündeki cümledir. Bulunan: yok.'),
    ("slide 4 says what the app does not do", "slayt 4 uygulamanın ne yapmadığını söylüyor"),
    ("Slide 5 must show the main screen: link an image from your repository, or draw it with text lines like "
     "+-----+. Found: neither. If you linked an image, check that the file is committed and the path is right.",
     "Slayt 5'te ana ekran gösterilmeli: reponda bulunan bir görseli bağla ya da +-----+ gibi metin çizgileriyle çiz. "
     "Bulunan: ikisi de yok. Görsel bağladıysan dosyanın commit edildiğini ve yolun doğru olduğunu kontrol et."),
    ("slide 5 shows the main screen", "slayt 5 ana ekranı gösteriyor"),
    ("Slide 6 must state one honest doubt: the question, and two lines on why you are unsure. "
     "Found: too short, or [brackets] left.",
     "Slayt 6'da dürüst bir kuşku yazılmalı: soru ve neden emin olmadığına dair iki satır. "
     "Bulunan: çok kısa ya da [köşeli parantez] kalmış."),
    ("slide 6 states one honest doubt", "slayt 6 dürüst bir kuşku belirtiyor"),
    # --- Week 3: the review ---------------------------------------------------------------------
    ("week03/contributors_03.json must name three different reviewers, each with a valid 9-digit student number. "
     "Found: {n} {u}.",
     "week03/contributors_03.json içinde üç farklı reviewer yazılmalı, her birinin geçerli 9 haneli öğrenci numarasıyla. "
     "Bulunan: {n} geçerli numara."),
    ("contributors_03.json names three reviewers", "contributors_03.json üç reviewer'ı adlandırıyor"),
    ("week03/contributors_03.json must give every reviewer the role 'reviewer'. Found: a wrong or empty role.",
     "week03/contributors_03.json içinde her reviewer'ın rolü 'reviewer' olmalı. Bulunan: yanlış ya da boş bir rol."),
    ("contributors_03.json gives every reviewer the role 'reviewer'",
     "contributors_03.json içinde her reviewer'ın rolü 'reviewer'"),
    ("week03/contributors_03.json must quote, for each reviewer, a real sentence they said. "
     "Found: {n} {u} without one.",
     "week03/contributors_03.json içinde her reviewer için söylediği gerçek bir cümle alıntılanmalı. "
     "Bulunan: {n} giriş bunu içermiyor."),
    ("contributors_03.json quotes what each reviewer said",
     "contributors_03.json her reviewer'ın söylediğini alıntılıyor"),
    ("week03/contributors_03.json must say, for each reviewer, whether you accepted the comment "
     "(accepted: true or false) and why. Found: {n} {u} without a decision and a reason.",
     "week03/contributors_03.json içinde her reviewer için yorumu kabul edip etmediğin (accepted: true ya da false) "
     "ve nedeni yazılmalı. Bulunan: {n} girişte karar ve neden yok."),
    ("contributors_03.json gives a decision and a reason for each reviewer",
     "contributors_03.json her reviewer için karar ve neden veriyor"),
    # --- Week 3: the change log, the group, the screens ------------------------------------------
    ('PROPOSAL.md change log must have a dated line added after the review, like '
     '"2026-10-07 — §N: what you changed". Found: none.',
     'PROPOSAL.md değişiklik günlüğüne, gözden geçirmeden sonra eklenmiş tarihli bir satır konmalı, örneğin '
     '"2026-10-07 — §N: neyi değiştirdin". Bulunan: yok.'),
    ("PROPOSAL.md change log has a dated line", "PROPOSAL.md değişiklik günlüğünde tarihli bir satır var"),
    ("week03/group_03.json must list your group: 4 or 5 different 9-digit student numbers, yours included. "
     "Found: {n} {u} of {m}. Your own number is missing.",
     "week03/group_03.json grubunu listelemeli: 4 ya da 5 farklı 9 haneli öğrenci numarası, seninki de dahil. "
     "Bulunan: {m} numaradan {n} tanesi geçerli. Kendi numaran eksik."),
    ("week03/group_03.json must list your group: 4 or 5 different 9-digit student numbers, yours included. "
     "Found: {n} {u} of {m}.",
     "week03/group_03.json grubunu listelemeli: 4 ya da 5 farklı 9 haneli öğrenci numarası, seninki de dahil. "
     "Bulunan: {m} numaradan {n} tanesi geçerli."),
    ("group_03.json lists your group: 4 or 5 different numbers, yours included",
     "group_03.json grubunu listeliyor: 4 ya da 5 farklı numara, seninki de dahil"),
    ("Your reviewers must be members of your group (week03/group_03.json). "
     "Found: not in group_03.json: {x}.",
     "Reviewer'ların grubunun üyesi olması gerekir (week03/group_03.json). "
     "Bulunan: group_03.json içinde olmayanlar: {x}."),
    ("Your three reviewers must be members of your group (week03/group_03.json). "
     "Found: no reviewers in contributors_03.json yet.",
     "Üç reviewer'ın da grubunun üyesi olması gerekir (week03/group_03.json). "
     "Bulunan: contributors_03.json içinde henüz reviewer yok."),
    ("your three reviewers are members of your group", "üç reviewer'ın da grubunun üyesi"),
    ("week03/screens_03.md is missing. Run the checker online to fetch it, then fill it in.",
     "week03/screens_03.md eksik. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır, sonra doldur."),
    ("week03/screens_03.md must list at least five screens of the main flow, each with a name, "
     "what the user does there, and REQ ids. Found: {n}.",
     "week03/screens_03.md ana akışın en az beş ekranını listelemeli; her biri için ad, kullanıcının orada ne yaptığı "
     "ve REQ id'leri yazılmalı. Bulunan: {n}."),
    ("screens_03.md lists at least five screens of the main flow",
     "screens_03.md ana akışın en az beş ekranını listeliyor"),
    ("week03/screens_03.md may name only requirements that exist in week02/requirements.json. "
     "Found: not in that file: {x}.",
     "week03/screens_03.md yalnızca week02/requirements.json içinde bulunan gereksinimleri anabilir. "
     "Bulunan: o dosyada olmayanlar: {x}."),
    ("week03/screens_03.md may name only requirements that exist in week02/requirements.json. "
     "Found: no filled-in screens yet.",
     "week03/screens_03.md yalnızca week02/requirements.json içinde bulunan gereksinimleri anabilir. "
     "Bulunan: henüz dolu bir ekran yok."),
    ("screens_03.md names only requirements that exist in requirements.json",
     "screens_03.md yalnızca requirements.json içinde bulunan gereksinimleri anıyor"),
    # --- Week 3: Saturday ------------------------------------------------------------------------
    ("PROPOSAL.md §12 must name the store (S0), its fee and how long its review takes. "
     "Found: no store named.",
     "PROPOSAL.md §12'de mağaza (S0), ücreti ve incelemesinin ne kadar sürdüğü yazılmalı. "
     "Bulunan: adı geçen bir mağaza yok."),
    ("PROPOSAL.md §12 names the store", "PROPOSAL.md §12 mağazayı adlandırıyor"),
    ("week03/ai_log_03.md must list the three objections the assistant gave you, numbered 1. 2. 3. "
     "Found: {n}.",
     "week03/ai_log_03.md içinde asistanın sana verdiği üç itiraz 1. 2. 3. diye numaralanarak listelenmeli. "
     "Bulunan: {n}."),
    ("week03/ai_log_03.md lists three numbered objections", "week03/ai_log_03.md üç numaralı itirazı listeliyor"),
    # --- group file of Week 4: the collaborator ----------------------------------------------------
    ("{p} must name your collaborator: exactly one entry, with a valid 9-digit student number. Found: {n} {u}, {m} with a valid number.",
     "{p} içinde collaborator'ın yazılmalı: tam olarak tek bir giriş ve geçerli 9 haneli öğrenci numarası. "
     "Bulunan: {n} giriş, geçerli numarası olan {m}."),
    ("{p} names your collaborator", "{p} collaborator'ını adlandırıyor"),
    ("{p} must quote a real sentence that your collaborator found or said. Found: {n} {u} without one.",
     "{p} içinde collaborator'ının bulduğu ya da söylediği gerçek bir cümle alıntılanmalı. Bulunan: {n} giriş bunu içermiyor."),
    ("{p} quotes what your collaborator found or said", "{p} collaborator'ının bulduğunu ya da söylediğini alıntılıyor"),
    ("{p} must say whether you accepted what your collaborator found (accepted: true or false) and why. "
     "Found: {n} {u} without a decision and a reason.",
     "{p} içinde collaborator'ının bulduğunu kabul edip etmediğin (accepted: true ya da false) ve nedeni yazılmalı. "
     "Bulunan: {n} girişte karar ve neden yok."),
    ("{p} gives a decision and a reason", "{p} karar ve neden veriyor"),
    # --- Week 4: the prototype -------------------------------------------------------------------
    ("week04/prototype/ has no .html files. Run the checker online to bring the starter screens.",
     "week04/prototype/ içinde .html dosyası yok. Başlangıç ekranlarını getirmek için checker'ı internete bağlıyken çalıştır."),
    ("week04/prototype/ has screens", "week04/prototype/ içinde ekranlar var"),
    ("The prototype must have at least 7 screens by Saturday: the full flow. Found: none yet.",
     "Prototipte Cumartesi'ye kadar en az 7 ekran olmalı: akışın tamamı. Bulunan: henüz hiç yok."),
    ("The prototype must have at least 7 screens by Saturday: the full flow. Found: {n}.",
     "Prototipte Cumartesi'ye kadar en az 7 ekran olmalı: akışın tamamı. Bulunan: {n}."),
    ("the prototype has at least 7 screens", "prototipte en az 7 ekran var"),
    ("The first screen must be week04/prototype/index.html. Found: no such file.",
     "İlk ekran week04/prototype/index.html olmalı. Bulunan: böyle bir dosya yok."),
    ("week04/prototype/index.html is there", "week04/prototype/index.html var"),
    ("The prototype must have at least 5 screens: the 3 starter screens and at least 2 of yours. "
     "Found: {n} {u} in week04/prototype/.",
     "Prototipte en az 5 ekran olmalı: 3 başlangıç ekranı ve senin en az 2 ekranın. "
     "Bulunan: week04/prototype/ içinde {n} .html dosyası."),
    ("the prototype has at least 5 screens", "prototipte en az 5 ekran var"),
    ("Every link in the prototype must lead to a screen that exists. Found: broken links {x}.",
     "Prototipteki her bağlantı var olan bir ekrana gitmeli. Bulunan: kırık bağlantılar {x}."),
    ("every link in the prototype leads to a screen that exists",
     "prototipteki her bağlantı var olan bir ekrana gidiyor"),
    ("Every screen must be reachable by links starting from index.html. Found: no link leads to {x}.",
     "Her ekrana index.html'den başlayan bağlantılarla ulaşılabilmeli. Bulunan: şuna giden bağlantı yok: {x}."),
    ("every screen can be reached from index.html", "her ekrana index.html'den ulaşılabiliyor"),
    ("The prototype screens still have [bracketed] text. Replace it with your own words and delete the square "
     "brackets too. Found in: {x}.",
     "Prototip ekranlarında hala [köşeli parantezli] metin var. Kendi sözlerinle değiştir ve köşeli parantezleri de sil. "
     "Bulunduğu yer: {x}."),
    ("the prototype has no [bracketed] text left", "prototipte [köşeli parantezli] metin kalmamış"),
    ("Every screen must say which requirements it serves, in a line like <!-- serves: REQ-001, REQ-004 -->, "
     "with ids that exist in requirements.json. Found: missing or wrong in {x}.",
     "Her ekran hangi gereksinimlere hizmet ettiğini <!-- serves: REQ-001, REQ-004 --> gibi bir satırla söylemeli; "
     "id'ler requirements.json içinde bulunmalı. Bulunan: eksik ya da yanlış olanlar {x}."),
    ("every screen names the requirements it serves", "her ekran hizmet ettiği gereksinimleri belirtiyor"),
    ("Every functional requirement marked 'must' needs a screen that serves it. Found: no screen serves {x}.",
     "'must' işaretli her işlevsel gereksinimin ona hizmet eden bir ekranı olmalı. Bulunan: şuna hizmet eden ekran yok: {x}."),
    ("every functional must requirement has a screen", "'must' işaretli her işlevsel gereksinimin bir ekranı var"),
    # --- Week 4: the test cases -----------------------------------------------------------------
    ("Test case ids must look like TC-001-01 (the requirement number, then a counter), with no repeats. "
     "Found: no test cases yet.",
     "Test senaryosu id'leri TC-001-01 gibi görünmeli (gereksinim numarası, sonra bir sayaç), tekrar olmamalı. "
     "Bulunan: henüz test senaryosu yok."),
    ("Test case ids must look like TC-001-01 (the requirement number, then a counter), with no repeats. "
     "Found: wrong ids {a}, repeated ids {b}.",
     "Test senaryosu id'leri TC-001-01 gibi görünmeli (gereksinim numarası, sonra bir sayaç), tekrar olmamalı. "
     "Bulunan: yanlış id'ler {a}, tekrarlanan id'ler {b}."),
    ("test case ids look like TC-001-01 and none is repeated",
     "test senaryosu id'leri TC-001-01 gibi ve hiçbiri tekrarlanmıyor"),
    ("Every test case must name a requirement that exists in week02/requirements.json, and the number in its id "
     "must match it. Found: no test cases yet.",
     "Her test senaryosu week02/requirements.json içinde var olan bir gereksinimi anmalı ve id'sindeki numara "
     "onunla eşleşmeli. Bulunan: henüz test senaryosu yok."),
    ("Every test case must name a requirement that exists in week02/requirements.json, and the number in its id "
     "must match it. Found: wrong in {x}.",
     "Her test senaryosu week02/requirements.json içinde var olan bir gereksinimi anmalı ve id'sindeki numara "
     "onunla eşleşmeli. Bulunan: yanlış olanlar {x}."),
    ("every test case tests a requirement that exists", "her test senaryosu var olan bir gereksinimi test ediyor"),
    ("Every test case needs steps and an expected result of at least 15 characters. Found: missing in {x}.",
     "Her test senaryosunun adımları ve en az 15 karakterlik beklenen bir sonucu olmalı. Bulunan: eksik olanlar {x}."),
    ("Every test case needs steps and an expected result of at least 15 characters. Found: no test cases yet.",
     "Her test senaryosunun adımları ve en az 15 karakterlik beklenen bir sonucu olmalı. Bulunan: henüz test senaryosu yok."),
    ("every test case has steps and an expected result", "her test senaryosunun adımları ve beklenen sonucu var"),
    ("Every requirement marked 'must' needs at least one test case. Found: no 'must' requirements in requirements.json.",
     "'must' işaretli her gereksinimin en az bir test senaryosu olmalı. Bulunan: requirements.json içinde 'must' gereksinim yok."),
    ("Every requirement marked 'must' needs at least one test case. Found: none for {x}.",
     "'must' işaretli her gereksinimin en az bir test senaryosu olmalı. Bulunan: şunlar için hiç yok: {x}."),
    ("every must requirement has a test case", "her must gereksinimin bir test senaryosu var"),
    ("At least three requirements need a second test case, for when something goes wrong. "
     "Found: {n} with two or more.",
     "En az üç gereksinimin, bir şeyin ters gittiği durum için ikinci bir test senaryosu olmalı. "
     "Bulunan: iki ya da daha fazla senaryosu olan {n} gereksinim."),
    ("at least three requirements have a second test case", "en az üç gereksinimin ikinci bir test senaryosu var"),
    # --- Week 4: the walk-through ------------------------------------------------------------------
    ("Your collaborator must run at least four of your test cases in round 1 of the walk-through, "
     "each run recorded under their student number. Found: {n} {u} by the tester with the most.",
     "Collaborator'ın 1. turda test senaryolarından en az dördünü çalıştırmalı ve her çalıştırma onun öğrenci numarasıyla "
     "kaydedilmeli. Bulunan: en çok çalıştıran tester {n} çalıştırma yapmış."),
    ("walk-through: your collaborator ran at least four test cases",
     "walk-through: collaborator'ın en az dört test senaryosu çalıştırmış"),
    ("Every run in the walk-through must be by your collaborator, the student named in week04/group_04.json. "
     "Found: no collaborator in group_04.json.",
     "Walk-through'daki her çalıştırma collaborator'ına ait olmalı, yani week04/group_04.json içinde adı geçen öğrenciye. "
     "Bulunan: group_04.json içinde collaborator yok."),
    ("Every run in the walk-through must be by your collaborator, the student named in week04/group_04.json. "
     "Found: no runs recorded in week04/walkthrough_04.json yet.",
     "Walk-through'daki her çalıştırma collaborator'ına ait olmalı, yani week04/group_04.json içinde adı geçen öğrenciye. "
     "Bulunan: week04/walkthrough_04.json içinde henüz kayıtlı çalıştırma yok."),
    ("Every run in the walk-through must be by your collaborator, the student named in week04/group_04.json. "
     "Found: not your collaborator: {x}.",
     "Walk-through'daki her çalıştırma collaborator'ına ait olmalı, yani week04/group_04.json içinde adı geçen öğrenciye. "
     "Bulunan: collaborator'ın olmayanlar: {x}."),
    ("walk-through: every run is by your collaborator (group_04.json)",
     "walk-through: her çalıştırma collaborator'ına ait (group_04.json)"),
    ("Round 1 must have at least two runs of test cases outside the login (REQ-001): run test cases of your main flow. "
     "Found: no runs recorded in week04/walkthrough_04.json yet.",
     "1. turda giriş (REQ-001) dışındaki test senaryolarından en az iki çalıştırma olmalı: ana akışının test senaryolarını çalıştır. "
     "Bulunan: week04/walkthrough_04.json içinde henüz kayıtlı çalıştırma yok."),
    ("Round 1 must have at least two runs of test cases outside the login (REQ-001): run test cases of your main flow. "
     "Found: {n}.",
     "1. turda giriş (REQ-001) dışındaki test senaryolarından en az iki çalıştırma olmalı: ana akışının test senaryolarını çalıştır. "
     "Bulunan: {n}."),
    ("walk-through: round 1 has at least two runs outside the login",
     "walk-through: 1. turda giriş dışında en az iki çalıştırma var"),
    ("Every run in the walk-through must name a test case that exists in week04/test_cases.json. "
     "Found: no runs recorded in week04/walkthrough_04.json yet.",
     "Walk-through'daki her çalıştırma week04/test_cases.json içinde var olan bir test senaryosunu anmalı. "
     "Bulunan: week04/walkthrough_04.json içinde henüz kayıtlı çalıştırma yok."),
    ("Every run in the walk-through must name a test case that exists in week04/test_cases.json. "
     "Found: not in test_cases.json: {x}.",
     "Walk-through'daki her çalıştırma week04/test_cases.json içinde var olan bir test senaryosunu anmalı. "
     "Bulunan: test_cases.json içinde olmayanlar: {x}."),
    ("walk-through: every run names a test case from test_cases.json",
     "walk-through: her çalıştırma test_cases.json içinden bir test senaryosunu anıyor"),
    ("Every run must have a result (pass, fail or blocked), and a note of at least 15 characters for fail and "
     "blocked. Found: no runs recorded in week04/walkthrough_04.json yet.",
     "Her çalıştırmanın bir sonucu (pass, fail ya da blocked) olmalı; fail ve blocked için en az 15 karakterlik bir not "
     "da olmalı. Bulunan: week04/walkthrough_04.json içinde henüz kayıtlı çalıştırma yok."),
    ("Every run must have a result (pass, fail or blocked), and a note of at least 15 characters for fail and "
     "blocked. Found: {n} {u} without a valid result, or a fail or blocked without a note.",
     "Her çalıştırmanın bir sonucu (pass, fail ya da blocked) olmalı; fail ve blocked için en az 15 karakterlik bir not "
     "da olmalı. Bulunan: geçerli sonucu olmayan ya da notsuz fail/blocked olan {n} çalıştırma."),
    ("walk-through: each result is pass, fail or blocked, with a note for fail and blocked",
     "walk-through: her sonuç pass, fail ya da blocked ve fail/blocked için not var"),
    ("Every failed test case must be run again in round 2 after the fix, or dropped with a Change log line. "
     "Found: no round 2 for {x}.",
     "Kalan her test senaryosu düzeltmeden sonra 2. turda yeniden çalıştırılmalı ya da bir değişiklik günlüğü satırıyla "
     "çıkarılmalı. Bulunan: şunlar için 2. tur yok: {x}."),
    ("Every failed test case must be run again in round 2 after the fix, or dropped with a Change log line. "
     "Found: no runs recorded in week04/walkthrough_04.json yet.",
     "Kalan her test senaryosu düzeltmeden sonra 2. turda yeniden çalıştırılmalı ya da bir değişiklik günlüğü satırıyla "
     "çıkarılmalı. Bulunan: week04/walkthrough_04.json içinde henüz kayıtlı çalıştırma yok."),
    ("walk-through: every failed test case was run again in round 2",
     "walk-through: kalan her test senaryosu 2. turda yeniden çalıştırılmış"),
    ("PROPOSAL.md change log must have a line dated {d} or later that names a REQ or TC id. Found: none.",
     "PROPOSAL.md değişiklik günlüğünde {d} ya da sonrası tarihli, bir REQ ya da TC id'si anan bir satır olmalı. "
     "Bulunan: yok."),
    ("PROPOSAL.md change log has a line from the walk-through that names the ids",
     "PROPOSAL.md değişiklik günlüğünde walk-through'dan gelen, id'leri anan bir satır var"),
    # --- Week 4: S1 and the log ----------------------------------------------------------------------
    ("week04/store.json must name the store: one of 'Google Play', 'Huawei AppGallery', 'Samsung Galaxy Store', "
     "'Apple App Store'. Found: something else, or empty.",
     "week04/store.json içinde mağaza yazılmalı: 'Google Play', 'Huawei AppGallery', 'Samsung Galaxy Store' ya da "
     "'Apple App Store'. Bulunan: başka bir şey ya da boş."),
    ("store.json names the store", "store.json mağazayı adlandırıyor"),
    ("week04/store.json S1 must have a date like 2026-10-13, your developer name, and a status of 'applied' or "
     "'verified'. Found: one of them missing or wrong.",
     "week04/store.json içindeki S1'de 2026-10-13 gibi bir tarih, geliştirici adın ve 'applied' ya da 'verified' "
     "durumu olmalı. Bulunan: biri eksik ya da yanlış."),
    ("The file named in 'evidence' in week04/store.json S1 must be saved in week04/. Found: no such file.",
     "week04/store.json S1 içindeki 'evidence' alanında adı geçen dosya week04/ içine kaydedilmeli. "
     "Bulunan: böyle bir dosya yok."),
    ("store.json S1 screenshot is saved", "store.json S1 ekran görüntüsü kaydedilmiş"),
    ("week04/store.json and PROPOSAL.md §12 must name the same store. Change one of them, and add a Change log line.",
     "week04/store.json ile PROPOSAL.md §12 aynı mağazayı yazmalı. Birini değiştir ve bir değişiklik günlüğü satırı ekle."),
    ("store.json and PROPOSAL.md §12 name the same store", "store.json ile PROPOSAL.md §12 aynı mağazayı yazıyor"),
    ("week04/ai_log_04.md must name the REQ ids you gave the assistant, outside the comments and the evidence block. "
     "Found: no REQ id.",
     "week04/ai_log_04.md içinde asistana verdiğin REQ id'leri yorumların ve kanıt bloğunun dışında yazılmalı. "
     "Bulunan: hiç REQ id'si yok."),
    ("week04/ai_log_04.md names the requirements it gave the assistant",
     "week04/ai_log_04.md asistana verilen gereksinimleri anıyor"),
    # --- Week 5: design, API contract, server skeleton, tests -----------------------------
    ("week05/DESIGN.md is missing. Run the checker online to bring it.",
     "week05/DESIGN.md eksik. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır."),
    ("week05/DESIGN.md must have at least four components in its table, each with what it does and the REQ ids "
     "it serves, ids that exist in requirements.json. Found: {n} {u}.",
     "week05/DESIGN.md tablosunda en az dört bileşen olmalı; her birinin ne yaptığı ve hizmet ettiği, "
     "requirements.json içinde bulunan REQ id'leri yazılı olmalı. Bulunan: {n} tam satır."),
    ("week05/DESIGN.md has at least four components, each with what it does and the requirements it serves",
     "week05/DESIGN.md en az dört bileşen içeriyor; her birinin ne yaptığı ve hizmet ettiği gereksinimler yazılı"),
    ("Every functional requirement marked 'must' needs a component in week05/DESIGN.md that serves it. "
     "Found: no 'must' requirements in requirements.json.",
     "'must' işaretli her işlevsel gereksinime week05/DESIGN.md içinde hizmet eden bir bileşen gerekir. "
     "Bulunan: requirements.json içinde 'must' gereksinim yok."),
    ("Every functional requirement marked 'must' needs a component in week05/DESIGN.md that serves it. "
     "Found: no component serves {x}.",
     "'must' işaretli her işlevsel gereksinime week05/DESIGN.md içinde hizmet eden bir bileşen gerekir. "
     "Bulunan: {x} gereksinimlerine hiçbir bileşen hizmet etmiyor."),
    ("every functional must requirement is served by a component in week05/DESIGN.md",
     "'must' işaretli her işlevsel gereksinime week05/DESIGN.md içinde bir bileşen hizmet ediyor"),
    ("week05/DESIGN.md must draw the architecture as a Mermaid diagram: your components, with at least two arrows "
     "between them. Found: {n} {u}.",
     "week05/DESIGN.md mimariyi bir Mermaid diyagramı olarak çizmeli: bileşenlerin ve aralarında en az iki ok. "
     "Bulunan: {n} ok."),
    ("week05/DESIGN.md has the architecture as a Mermaid diagram",
     "week05/DESIGN.md mimariyi bir Mermaid diyagramı olarak içeriyor"),
    ("week05/api.md is missing. Run the checker online to bring it.",
     "week05/api.md eksik. Dosyayı getirmek için checker'ı internete bağlıyken çalıştır."),
    ("week05/api.md must have at least two endpoints that serve REQ-001, the login: one that asks for a code and "
     "one that logs in with it. Found: {n}.",
     "week05/api.md içinde REQ-001'e, yani girişe hizmet eden en az iki endpoint olmalı: biri kod ister, diğeri o "
     "kodla giriş yapar. Bulunan: {n}."),
    ("week05/api.md has the login endpoints (REQ-001)", "week05/api.md giriş endpoint'lerini (REQ-001) içeriyor"),
    ("Every REQ id in week05/api.md must exist in week02/requirements.json. Found: no REQ ids yet.",
     "week05/api.md içindeki her REQ id'si week02/requirements.json içinde bulunmalı. Bulunan: henüz hiç REQ id'si yok."),
    ("Every REQ id in week05/api.md must exist in week02/requirements.json. Found: not there: {x}.",
     "week05/api.md içindeki her REQ id'si week02/requirements.json içinde bulunmalı. Bulunan: orada olmayanlar: {x}."),
    ("every REQ id in week05/api.md exists in requirements.json",
     "week05/api.md içindeki her REQ id'si requirements.json içinde var"),
    ("Every endpoint in week05/api.md that serves a requirement must give its request, its response with a 2xx "
     "status code, and at least one error with its 4xx or 5xx code. Found: no endpoint that serves a requirement.",
     "week05/api.md içinde bir gereksinime hizmet eden her endpoint isteğini, 2xx durum koduyla cevabını ve 4xx ya "
     "da 5xx koduyla en az bir hatasını vermeli. Bulunan: bir gereksinime hizmet eden endpoint yok."),
    ("Every endpoint in week05/api.md that serves a requirement must give its request, its response with a 2xx "
     "status code, and at least one error with its 4xx or 5xx code. Found: incomplete: {x}.",
     "week05/api.md içinde bir gereksinime hizmet eden her endpoint isteğini, 2xx durum koduyla cevabını ve 4xx ya "
     "da 5xx koduyla en az bir hatasını vermeli. Bulunan: eksik olanlar: {x}."),
    ("every endpoint in week05/api.md gives its request, its response and its errors",
     "week05/api.md içindeki her endpoint isteğini, cevabını ve hatalarını veriyor"),
    ("server/main.py must be there and be valid Python. Found: no such file. Run the checker online to bring the starter.",
     "server/main.py bulunmalı ve geçerli Python olmalı. Bulunan: böyle bir dosya yok. Başlangıç dosyalarını getirmek "
     "için checker'ı internete bağlıyken çalıştır."),
    ("server/main.py must be there and be valid Python. Found: a syntax error.",
     "server/main.py bulunmalı ve geçerli Python olmalı. Bulunan: bir sözdizimi hatası."),
    ("server/main.py is valid Python", "server/main.py geçerli Python"),
    ("It is checked once server/ has a route of your own besides /health.",
     "server/ içinde /health dışında kendi route'un olunca kontrol edilir."),
    ("It is checked once the file names your collaborator's student number.",
     "Dosya collaborator'ının öğrenci numarasını verince kontrol edilir."),
    ("It is checked once the file names your reviewers' student numbers.",
     "Dosya reviewer'larının öğrenci numaralarını verince kontrol edilir."),
    ("server/main.py must create the app with FastAPI(...). Found: no FastAPI( in it.",
     "server/main.py uygulamayı FastAPI(...) ile oluşturmalı. Bulunan: içinde FastAPI( yok."),
    ("server/main.py creates the FastAPI app", "server/main.py FastAPI uygulamasını oluşturuyor"),
    ("Every endpoint in week05/api.md must have a route in server/ with the same method and path; it may answer 501 "
     "until it is built. Found: no endpoint that serves a requirement in week05/api.md yet.",
     "week05/api.md içindeki her endpoint'in server/ içinde aynı metot ve yolla bir route'u olmalı; route, yapılana "
     "kadar 501 ile cevap verebilir. Bulunan: week05/api.md içinde henüz bir gereksinime hizmet eden endpoint yok."),
    ("Every endpoint in week05/api.md must have a route in server/ with the same method and path; it may answer 501 "
     "until it is built. Found: no route for {x}; server/main.py does not include {r}.",
     "week05/api.md içindeki her endpoint'in server/ içinde aynı metot ve yolla bir route'u olmalı; route, yapılana "
     "kadar 501 ile cevap verebilir. Bulunan: route'u olmayanlar: {x}; server/main.py şunları içermiyor (include_router): {r}."),
    ("Every endpoint in week05/api.md must have a route in server/ with the same method and path; it may answer 501 "
     "until it is built. Found: no route for {x}.",
     "week05/api.md içindeki her endpoint'in server/ içinde aynı metot ve yolla bir route'u olmalı; route, yapılana "
     "kadar 501 ile cevap verebilir. Bulunan: route'u olmayanlar: {x}."),
    ("every endpoint in week05/api.md has its route in server/",
     "week05/api.md içindeki her endpoint'in server/ içinde route'u var"),
    ("Every route in server/ must be a row of week05/api.md, with the same method and path. "
     "Found: no routes in server/ besides /health.",
     "server/ içindeki her route, aynı metot ve yolla week05/api.md içinde bir satır olmalı. Bulunan: server/ içinde "
     "/health dışında route yok."),
    ("Every route in server/ must be a row of week05/api.md, with the same method and path. Found: not in api.md: {x}.",
     "server/ içindeki her route, aynı metot ve yolla week05/api.md içinde bir satır olmalı. Bulunan: api.md içinde "
     "olmayanlar: {x}."),
    ("every route in server/ has its row in week05/api.md", "server/ içindeki her route'un week05/api.md içinde satırı var"),
    ("server/tests/ must have at least one test whose name begins with a test case id, such as "
     "test_TC_001_01_a_code_is_sent. Found: none.",
     "server/tests/ içinde adı bir test case id'siyle başlayan en az bir test olmalı, örneğin "
     "test_TC_001_01_a_code_is_sent. Bulunan: hiç yok."),
    ("server/tests has a test named by a test case id", "server/tests içinde bir test case id'siyle adlandırılmış bir test var"),
    ("server/tests/ must have at least three tests named by different test case ids. Found: {n}.",
     "server/tests/ içinde farklı test case id'leriyle adlandırılmış en az üç test olmalı. Bulunan: {n}."),
    ("server/tests has at least three tests named by different test case ids",
     "server/tests içinde farklı test case id'leriyle adlandırılmış en az üç test var"),
    ("Every test case id in a test name in server/tests/ must exist in week04/test_cases.json. "
     "Found: no tests named by a test case id.",
     "server/tests/ içindeki test adlarında geçen her test case id'si week04/test_cases.json içinde bulunmalı. "
     "Bulunan: test case id'siyle adlandırılmış test yok."),
    ("Every test case id in a test name in server/tests/ must exist in week04/test_cases.json. Found: not there: {x}.",
     "server/tests/ içindeki test adlarında geçen her test case id'si week04/test_cases.json içinde bulunmalı. "
     "Bulunan: orada olmayanlar: {x}."),
    ("every test case id in server/tests exists in test_cases.json",
     "server/tests içindeki her test case id'si test_cases.json içinde var"),
    ("week05/ai_log_05.md must hold, in the Evidence block, the output of a test run as your terminal showed it, "
     "down to its last line, such as '1 failed, 1 passed'. Found: no such line.",
     "week05/ai_log_05.md, Evidence bloğunda bir test çalıştırmasının çıktısını terminalinin gösterdiği gibi, son "
     "satırına kadar içermeli; örneğin '1 failed, 1 passed'. Bulunan: böyle bir satır yok."),
    ("week05/ai_log_05.md holds the output of a test run", "week05/ai_log_05.md bir test çalıştırmasının çıktısını içeriyor"),
    # Week 6 (VC, 22 Oct 2026)
    ('It is checked once {p} is there.',
     '{p} gelince kontrol edilir.'),
    ('course test LOGIN_01: a code is sent to a valid e-mail',
     'ders testi LOGIN_01: geçerli bir e-postaya kod gönderiliyor'),
    ('Course test LOGIN_01 (a code is sent to a valid e-mail) must pass. Found: {f}.',
     'LOGIN_01 ders testi (geçerli bir e-postaya kod gönderiliyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_02: something that is not an e-mail is refused',
     'ders testi LOGIN_02: e-posta olmayan bir değer reddediliyor'),
    ('Course test LOGIN_02 (something that is not an e-mail is refused) must pass. Found: {f}.',
     'LOGIN_02 ders testi (e-posta olmayan bir değer reddediliyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_03: the right code gives a token',
     'ders testi LOGIN_03: doğru kod bir token veriyor'),
    ('Course test LOGIN_03 (the right code gives a token) must pass. Found: {f}.',
     'LOGIN_03 ders testi (doğru kod bir token veriyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_04: a wrong code is refused',
     'ders testi LOGIN_04: yanlış kod reddediliyor'),
    ('Course test LOGIN_04 (a wrong code is refused) must pass. Found: {f}.',
     'LOGIN_04 ders testi (yanlış kod reddediliyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_05: the token opens me',
     "ders testi LOGIN_05: token me'yi açıyor"),
    ('Course test LOGIN_05 (the token opens me) must pass. Found: {f}.',
     "LOGIN_05 ders testi (token me'yi açıyor) geçmeli. Bulunan: {f}."),
    ('course test LOGIN_06: me is refused without a token or with a wrong one',
     "ders testi LOGIN_06: token olmadan ya da yanlış token'la me reddediliyor"),
    ('Course test LOGIN_06 (me is refused without a token or with a wrong one) must pass. Found: {f}.',
     "LOGIN_06 ders testi (token olmadan ya da yanlış token'la me reddediliyor) geçmeli. Bulunan: {f}."),
    ('course test LOGIN_07: a code works only once',
     'ders testi LOGIN_07: bir kod yalnızca bir kez çalışıyor'),
    ('Course test LOGIN_07 (a code works only once) must pass. Found: {f}.',
     'LOGIN_07 ders testi (bir kod yalnızca bir kez çalışıyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_08: a code expires after 10 minutes',
     'ders testi LOGIN_08: bir kodun süresi 10 dakikada doluyor'),
    ('Course test LOGIN_08 (a code expires after 10 minutes) must pass. Found: {f}.',
     'LOGIN_08 ders testi (bir kodun süresi 10 dakikada doluyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_09: a new code within a minute is refused, and allowed after it',
     'ders testi LOGIN_09: bir dakika içinde yeni kod isteği reddediliyor, sonra kabul ediliyor'),
    ('Course test LOGIN_09 (a new code within a minute is refused, and allowed after it) must pass. Found: {f}.',
     'LOGIN_09 ders testi (bir dakika içinde yeni kod isteği reddediliyor, sonra kabul ediliyor) geçmeli. Bulunan: {f}.'),
    ('course test LOGIN_10: three wrong codes lock the login for 15 minutes',
     "ders testi LOGIN_10: üç yanlış kod login'i 15 dakika kilitliyor"),
    ('Course test LOGIN_10 (three wrong codes lock the login for 15 minutes) must pass. Found: {f}.',
     "LOGIN_10 ders testi (üç yanlış kod login'i 15 dakika kilitliyor) geçmeli. Bulunan: {f}."),
    ('server/login_contract.json is filled in',
     'server/login_contract.json dolduruldu'),
    ('server/login_contract.json must give, written by hand, request_code, login and me (each a method and a path, such as POST /auth/code) and email_field, code_field and token_field. Found: no such file, or not valid JSON. Run the checker online to bring it.',
     "server/login_contract.json elle yazılmış request_code, login ve me (her biri bir metot ve bir yol, örneğin POST /auth/code) ile email_field, code_field ve token_field değerlerini vermeli. Bulunan: böyle bir dosya yok ya da geçerli JSON değil. Getirmek için checker'ı internete bağlıyken çalıştır."),
    ('server/login_contract.json must give, written by hand, request_code, login and me (each a method and a path, such as POST /auth/code) and email_field, code_field and token_field. Found: not filled in: {x}.',
     'server/login_contract.json elle yazılmış request_code, login ve me (her biri bir metot ve bir yol, örneğin POST /auth/code) ile email_field, code_field ve token_field değerlerini vermeli. Bulunan: doldurulmamış: {x}.'),
    ('the three login endpoints of server/login_contract.json are rows of week05/api.md',
     "server/login_contract.json içindeki üç login endpoint'i week05/api.md içinde satır olarak var"),
    ('Every endpoint in server/login_contract.json must be a row of week05/api.md with the same method and path. Found: not in week05/api.md: {x}.',
     'server/login_contract.json içindeki her endpoint week05/api.md içinde aynı metot ve yolla bir satır olmalı. Bulunan: week05/api.md içinde olmayanlar: {x}.'),
    ('It is checked once server/login_contract.json is filled in.',
     'server/login_contract.json doldurulunca kontrol edilir.'),
    # Week 6 after the change of course (VC, 22 Oct 2026): the login comes ready; your own must requirements
    ("server/main.py brings in the course's login (course_login.router)",
     "server/main.py dersin login'ini içeri alıyor (course_login.router)"),
    ("server/main.py must bring in the login the course gives, with from server import course_login and "
     "app.include_router(course_login.router). Found: no server/course_login.py. Run the checker online to bring it.",
     "server/main.py dersin verdiği login'i from server import course_login ve app.include_router(course_login.router) "
     "ile içeri almalı. Bulunan: server/course_login.py yok. Getirmek için checker'ı internete bağlıyken çalıştır."),
    ("server/main.py must bring in the login the course gives, with from server import course_login and "
     "app.include_router(course_login.router). Found: no such line in server/main.py.",
     "server/main.py dersin verdiği login'i from server import course_login ve app.include_router(course_login.router) "
     "ile içeri almalı. Bulunan: server/main.py içinde böyle bir satır yok."),
    ("a route of one of your own must requirements works: it no longer answers 501",
     "kendi must gereksinimlerinden birinin route'u çalışıyor: artık 501 dönmüyor"),
    ("At least one row of week05/api.md that serves a functional must requirement of your own (not the login, "
     "REQ-001) must have its route in server/ working: no longer answering 501. Found: no functional must "
     "requirement besides REQ-001 in week02/requirements.json.",
     "week05/api.md içinde kendi işlevsel must gereksinimlerinden birine (login, yani REQ-001 dışında) hizmet eden en "
     "az bir satırın server/ içindeki route'u çalışmalı: artık 501 dönmemeli. Bulunan: week02/requirements.json "
     "içinde REQ-001 dışında işlevsel must gereksinim yok."),
    ("At least one row of week05/api.md that serves a functional must requirement of your own (not the login, "
     "REQ-001) must have its route in server/ working: no longer answering 501. Found: no row of week05/api.md "
     "serves one.",
     "week05/api.md içinde kendi işlevsel must gereksinimlerinden birine (login, yani REQ-001 dışında) hizmet eden en "
     "az bir satırın server/ içindeki route'u çalışmalı: artık 501 dönmemeli. Bulunan: week05/api.md içinde böyle "
     "bir gereksinime hizmet eden satır yok."),
    ("At least one row of week05/api.md that serves a functional must requirement of your own (not the login, "
     "REQ-001) must have its route in server/ working: no longer answering 501. Found: no working route; "
     "server/main.py does not include {r}.",
     "week05/api.md içinde kendi işlevsel must gereksinimlerinden birine (login, yani REQ-001 dışında) hizmet eden en "
     "az bir satırın server/ içindeki route'u çalışmalı: artık 501 dönmemeli. Bulunan: çalışan route yok; "
     "server/main.py şunları içermiyor (include_router): {r}."),
    ("At least one row of week05/api.md that serves a functional must requirement of your own (not the login, "
     "REQ-001) must have its route in server/ working: no longer answering 501. Found: every such route still "
     "answers 501.",
     "week05/api.md içinde kendi işlevsel must gereksinimlerinden birine (login, yani REQ-001 dışında) hizmet eden en "
     "az bir satırın server/ içindeki route'u çalışmalı: artık 501 dönmemeli. Bulunan: bu route'ların hepsi şu an "
     "501 dönüyor."),
    ("a test named by a test case of one of your own must requirements passes",
     "kendi must gereksinimlerinden birinin test case'iyle adlandırılmış bir test geçiyor"),
    ("At least one test in server/tests/ named by a test case of a must requirement of your own (not the login, "
     "REQ-001), such as test_TC_002_02_..., must pass. Found: no test case of a must requirement besides REQ-001 "
     "in week04/test_cases.json.",
     "server/tests/ içinde kendi must gereksinimlerinden birinin (login, yani REQ-001 dışında) test case'iyle "
     "adlandırılmış en az bir test, örneğin test_TC_002_02_..., geçmeli. Bulunan: week04/test_cases.json içinde "
     "REQ-001 dışında bir must gereksinimin test case'i yok."),
    ("At least one test in server/tests/ named by a test case of a must requirement of your own (not the login, "
     "REQ-001), such as test_TC_002_02_..., must pass. Found: none of their tests passes, or no test is named by "
     "one of their ids.",
     "server/tests/ içinde kendi must gereksinimlerinden birinin (login, yani REQ-001 dışında) test case'iyle "
     "adlandırılmış en az bir test, örneğin test_TC_002_02_..., geçmeli. Bulunan: bunların hiçbir testi geçmiyor ya "
     "da hiçbir test onların id'leriyle adlandırılmamış."),
    ("At least one test in server/tests/ named by a test case of a must requirement of your own (not the login, "
     "REQ-001), such as test_TC_002_02_..., must pass. Found: {f}.",
     "server/tests/ içinde kendi must gereksinimlerinden birinin (login, yani REQ-001 dışında) test case'iyle "
     "adlandırılmış en az bir test, örneğin test_TC_002_02_..., geçmeli. Bulunan: {f}."),
    ("web/ has a page that calls a route of your own must requirements with fetch",
     "web/ içinde kendi must gereksinimlerinin bir route'unu fetch ile çağıran bir sayfa var"),
    ("web/ must hold a page of your web client, made from its prototype screen, that calls with fetch a path of "
     "week05/api.md serving a functional must requirement of your own (not the login). Found: no web/ folder.",
     "web/ içinde web istemcinin, prototip ekranından yapılmış bir sayfası olmalı; bu sayfa week05/api.md içinde "
     "kendi işlevsel must gereksinimlerinden birine (login dışında) hizmet eden bir yolu fetch ile çağırmalı. "
     "Bulunan: web/ klasörü yok."),
    ("web/ must hold a page of your web client, made from its prototype screen, that calls with fetch a path of "
     "week05/api.md serving a functional must requirement of your own (not the login). Found: no page in web/.",
     "web/ içinde web istemcinin, prototip ekranından yapılmış bir sayfası olmalı; bu sayfa week05/api.md içinde "
     "kendi işlevsel must gereksinimlerinden birine (login dışında) hizmet eden bir yolu fetch ile çağırmalı. "
     "Bulunan: web/ içinde sayfa yok."),
    ("web/ must hold a page of your web client, made from its prototype screen, that calls with fetch a path of "
     "week05/api.md serving a functional must requirement of your own (not the login). Found: no row of "
     "week05/api.md serves such a requirement.",
     "web/ içinde web istemcinin, prototip ekranından yapılmış bir sayfası olmalı; bu sayfa week05/api.md içinde "
     "kendi işlevsel must gereksinimlerinden birine (login dışında) hizmet eden bir yolu fetch ile çağırmalı. "
     "Bulunan: week05/api.md içinde böyle bir gereksinime hizmet eden satır yok."),
    ("web/ must hold a page of your web client, made from its prototype screen, that calls with fetch a path of "
     "week05/api.md serving a functional must requirement of your own (not the login). Found: no page or script "
     "there that calls fetch with one of those paths.",
     "web/ içinde web istemcinin, prototip ekranından yapılmış bir sayfası olmalı; bu sayfa week05/api.md içinde "
     "kendi işlevsel must gereksinimlerinden birine (login dışında) hizmet eden bir yolu fetch ile çağırmalı. "
     "Bulunan: orada bu yollardan biriyle fetch çağıran bir sayfa ya da script yok."),
    ("every row of week05/api.md that serves a functional must requirement has a working route",
     "week05/api.md içinde işlevsel bir must gereksinime hizmet eden her satırın çalışan bir route'u var"),
    ("Every row of week05/api.md that serves a functional must requirement must have its route in server/, no "
     "longer answering 501. Found: no row of week05/api.md serves a functional must requirement.",
     "week05/api.md içinde işlevsel bir must gereksinime hizmet eden her satırın server/ içinde route'u olmalı ve "
     "artık 501 dönmemeli. Bulunan: week05/api.md içinde işlevsel bir must gereksinime hizmet eden satır yok."),
    ("Every row of week05/api.md that serves a functional must requirement must have its route in server/, no "
     "longer answering 501. Found: missing or still 501: {x}; server/main.py does not include {r}.",
     "week05/api.md içinde işlevsel bir must gereksinime hizmet eden her satırın server/ içinde route'u olmalı ve "
     "artık 501 dönmemeli. Bulunan: eksik ya da şu an 501 dönenler: {x}; server/main.py şunları içermiyor "
     "(include_router): {r}."),
    ("Every row of week05/api.md that serves a functional must requirement must have its route in server/, no "
     "longer answering 501. Found: missing or still 501: {x}.",
     "week05/api.md içinde işlevsel bir must gereksinime hizmet eden her satırın server/ içinde route'u olmalı ve "
     "artık 501 dönmemeli. Bulunan: eksik ya da şu an 501 dönenler: {x}."),
    ('every test case of a must requirement with run "server" has a test that passes',
     'run değeri "server" olan, must bir gereksinimin her test case\'inin geçen bir testi var'),
    ('Every test case of a must requirement with "run": "server" in week04/test_cases.json must have a test in '
     'server/tests/ named by its id, such as test_TC_002_02_..., that passes. Found: no test case of a must '
     'requirement with "run": "server".',
     'week04/test_cases.json içinde "run": "server" olan, must bir gereksinimin her test case\'inin server/tests/ '
     'içinde kendi id\'siyle adlandırılmış ve geçen bir testi olmalı; örneğin test_TC_002_02_.... Bulunan: '
     '"run": "server" olan, must bir gereksinimin test case\'i yok.'),
    ('Every test case of a must requirement with "run": "server" in week04/test_cases.json must have a test in '
     'server/tests/ named by its id, such as test_TC_002_02_..., that passes. Found: no passing test for {x}.',
     'week04/test_cases.json içinde "run": "server" olan, must bir gereksinimin her test case\'inin server/tests/ '
     'içinde kendi id\'siyle adlandırılmış ve geçen bir testi olmalı; örneğin test_TC_002_02_.... Bulunan: '
     'şunların geçen testi yok: {x}.'),
    ('Every test case of a must requirement with "run": "server" in week04/test_cases.json must have a test in '
     'server/tests/ named by its id, such as test_TC_002_02_..., that passes. Found: {f}.',
     'week04/test_cases.json içinde "run": "server" olan, must bir gereksinimin her test case\'inin server/tests/ '
     'içinde kendi id\'siyle adlandırılmış ve geçen bir testi olmalı; örneğin test_TC_002_02_.... Bulunan: {f}.'),
    ("every functional must requirement has a page in web/ that calls the server",
     "her işlevsel must gereksinimin web/ içinde sunucuyu çağıran bir sayfası var"),
    ("Every functional must requirement needs a page in web/ that names it in a line like <!-- serves: REQ-002 --> "
     "and calls the server with fetch. Found: no functional must requirement in week02/requirements.json.",
     "Her işlevsel must gereksinimin web/ içinde onu <!-- serves: REQ-002 --> gibi bir satırda adlandıran ve "
     "sunucuyu fetch ile çağıran bir sayfası olmalı. Bulunan: week02/requirements.json içinde işlevsel must "
     "gereksinim yok."),
    ("Every functional must requirement needs a page in web/ that names it in a line like <!-- serves: REQ-002 --> "
     "and calls the server with fetch. Found: no such page for {x}.",
     "Her işlevsel must gereksinimin web/ içinde onu <!-- serves: REQ-002 --> gibi bir satırda adlandıran ve "
     "sunucuyu fetch ile çağıran bir sayfası olmalı. Bulunan: şunlar için böyle bir sayfa yok: {x}."),
    ('server/ serves the pages of web/',
     'server/ web/ sayfalarını sunuyor'),
    ('server/ must serve the pages of web/ itself, with StaticFiles (app.mount), an HTMLResponse or a FileResponse, so that the web client and the server share one address. Found: neither.',
     'server/, web/ sayfalarını kendisi sunmalı: StaticFiles (app.mount), bir HTMLResponse ya da bir FileResponse ile; böylece web istemcisi ile sunucu aynı adresi paylaşır. Bulunan: hiçbiri.'),
    ('.env is not in the repository, and .gitignore lists it',
     ".env repo'da yok ve .gitignore onu listeliyor"),
    ('.env must never be committed, and .gitignore must list it. Found: it is in the repository. Remove it with git rm --cached .env and change the password it held.',
     ".env asla commit edilmemeli ve .gitignore onu listelemeli. Bulunan: repo'da var. git rm --cached .env ile çıkar ve içindeki şifreyi değiştir."),
    ('.env must never be committed, and .gitignore must list it. Found: .gitignore does not list .env.',
     ".env asla commit edilmemeli ve .gitignore onu listelemeli. Bulunan: .gitignore .env'yi listelemiyor."),
    ('.env.example names the e-mail settings, without the password',
     '.env.example e-posta ayarlarının adlarını şifre olmadan veriyor'),
    ('.env.example must list the names of your e-mail settings, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD and SMTP_FROM, with no password after SMTP_PASSWORD=. Found: missing: {x}.',
     '.env.example e-posta ayarlarının adlarını listelemeli: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD ve SMTP_FROM; SMTP_PASSWORD= sonrasında şifre olmamalı. Bulunan: eksik: {x}.'),
    ('.env.example must list the names of your e-mail settings, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD and SMTP_FROM, with no password after SMTP_PASSWORD=. Found: a value after SMTP_PASSWORD=.',
     '.env.example e-posta ayarlarının adlarını listelemeli: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD ve SMTP_FROM; SMTP_PASSWORD= sonrasında şifre olmamalı. Bulunan: SMTP_PASSWORD= sonrasında bir değer var.'),
    ('week06/email_code.png shows the e-mail with the code',
     'week06/email_code.png kodun geldiği e-postayı gösteriyor'),
    ('week06/ must hold email_code.png (or .jpg): a screenshot of the e-mail with the login code that your server sent by real e-mail. Found: no such file.',
     'week06/ içinde email_code.png (ya da .jpg) olmalı: sunucunun gerçek e-postayla gönderdiği login kodunu gösteren e-postanın ekran görüntüsü. Bulunan: böyle bir dosya yok.'),
    ('store.json S2 is filled in',
     'store.json S2 dolduruldu'),
    ("week04/store.json S2 must have the date the app record was created, like 2026-10-31, the app's name in the store (app_name) and its package name or bundle id (package), such as com.example.studyroom. Found: one of them missing or wrong.",
     "week04/store.json içindeki S2'de uygulama kaydının oluşturulduğu tarih (2026-10-31 gibi), uygulamanın mağazadaki adı (app_name) ve paket adı ya da bundle id'si (package, örneğin com.example.studyroom) olmalı. Bulunan: biri eksik ya da yanlış."),
    ('store.json S2 screenshot is saved',
     'store.json S2 ekran görüntüsü kaydedilmiş'),
    ("The file named in 'evidence' in week04/store.json S2 must be saved in week04/. Found: no such file.",
     "week04/store.json S2 içindeki 'evidence' alanında adı geçen dosya week04/ içine kaydedilmeli. Bulunan: böyle bir dosya yok."),
    ('every test case in week04/test_cases.json says how it is run',
     'week04/test_cases.json içindeki her test case nasıl çalıştırıldığını söylüyor'),
    ('Every test case in week04/test_cases.json must say how it is run: "run": "server", "web" or "manual". Found: missing or wrong in {x}.',
     'week04/test_cases.json içindeki her test case nasıl çalıştırıldığını söylemeli: "run": "server", "web" ya da "manual". Bulunan: eksik ya da yanlış olanlar: {x}.'),
    ('Every test case in week04/test_cases.json must say how it is run: "run": "server", "web" or "manual". Found: no test cases.',
     'week04/test_cases.json içindeki her test case nasıl çalıştırıldığını söylemeli: "run": "server", "web" ya da "manual". Bulunan: test case yok.'),
    ('{p} names the groupmate who attacked your work',
     "{p} çalışmana saldıran grup arkadaşını adlandırıyor"),
    ('{p} must name each groupmate who tried to break your work, with a valid 9-digit student number. Found: {n} {u}, {m} with a valid number.',
     "{p} çalışmanı kırmaya çalışan her grup arkadaşını geçerli 9 haneli öğrenci numarasıyla yazmalı. Bulunan: {n} giriş, {m} tanesinde geçerli numara var."),
    ('It is checked once the file names the student number of the groupmate who attacked your work.',
     "Dosya çalışmana saldıran grup arkadaşının öğrenci numarasını verince kontrol edilir."),
    ('{p} says what each attacker tried and what happened',
     '{p} her saldırganın ne denediğini ve ne olduğunu söylüyor'),
    ('{p} must say, in your own words, what each attacker tried (tried) and what your server or your page did (happened). Found: {n} {u} without both.',
     "{p} her saldırganın ne denediğini (tried) ve sunucunun ya da sayfanın ne yaptığını (happened) kendi sözlerinle söylemeli. Bulunan: {n} giriş ikisini birden içermiyor."),
    ('{p} says for each finding whether you fix it, and why',
     '{p} her bulgu için düzeltip düzeltmeyeceğini ve nedenini söylüyor'),
    ("{p} must say for each attacker's finding whether you fix it (accepted: true or false) and why. Found: {n} {u} without a decision and a reason.",
     '{p} her saldırganın bulgusu için düzeltip düzeltmeyeceğini (accepted: true ya da false) ve nedenini söylemeli. Bulunan: {n} giriş karar ve neden içermiyor.'),
    # --- Week 7: the mobile client ----------------------------------------------------------------
    ('{p} must name your tester: exactly one entry, with a valid 9-digit student number. Found: {n} {u}, {m} with a valid number.',
     '{p} içinde testçin yazılmalı: tam olarak tek bir giriş ve geçerli 9 haneli öğrenci numarası. Bulunan: {n} giriş, geçerli numarası olan {m}.'),
    ('{p} names your tester',
     '{p} testçini adlandırıyor'),
    ("It is checked once the file names your tester's student number.",
     'Dosya testçinin öğrenci numarasını verince kontrol edilir.'),
    ('{p} must quote a real sentence that your tester found or said. Found: {n} {u} without one.',
     '{p} içinde testçinin bulduğu ya da söylediği gerçek bir cümle alıntılanmalı. Bulunan: {n} giriş bunu içermiyor.'),
    ('{p} quotes what your tester found or said',
     '{p} testçinin bulduğunu ya da söylediğini alıntılıyor'),
    ('{p} must say whether you accepted what your tester found (accepted: true or false) and why. Found: {n} {u} without a decision and a reason.',
     '{p} içinde testçinin bulduğunu kabul edip etmediğin (accepted: true ya da false) ve nedeni yazılmalı. Bulunan: {n} girişte karar ve neden yok.'),
    ('mobile/ holds your app, made with Flutter, React Native–Expo, Kotlin or Swift',
     'mobile/ içinde Flutter, React Native–Expo, Kotlin ya da Swift ile yapılmış uygulaman var'),
    ('mobile/, at the root of your repository, must hold your app, created with the tool of your framework: Flutter (pubspec.yaml), React Native–Expo (package.json with expo or react-native), Kotlin (a Gradle build) or Swift (an Xcode project). Found: no mobile/ folder.',
     "Reponun kökündeki mobile/ klasöründe uygulaman olmalı, framework'ünün kendi aracıyla oluşturulmuş: Flutter (pubspec.yaml), React Native–Expo (expo ya da react-native içeren package.json), Kotlin (bir Gradle build'i) ya da Swift (bir Xcode projesi). Bulunan: mobile/ klasörü yok."),
    ('mobile/, at the root of your repository, must hold your app, created with the tool of your framework: Flutter (pubspec.yaml), React Native–Expo (package.json with expo or react-native), Kotlin (a Gradle build) or Swift (an Xcode project). Found: none of these.',
     "Reponun kökündeki mobile/ klasöründe uygulaman olmalı, framework'ünün kendi aracıyla oluşturulmuş: Flutter (pubspec.yaml), React Native–Expo (expo ya da react-native içeren package.json), Kotlin (bir Gradle build'i) ya da Swift (bir Xcode projesi). Bulunan: bunların hiçbiri yok."),
    ('mobile/ has a login screen with serves: REQ-001 that sends requests to your three login endpoints',
     "mobile/ içinde serves: REQ-001 içeren ve üç giriş endpoint'ine istek gönderen bir giriş ekranı var"),
    ('mobile/ must have a login screen whose source file names REQ-001 in a comment like // serves: REQ-001, and your app must send requests to the three endpoints of server/login_contract.json (request_code, login and me). Write the path of each endpoint with its /, as in week05/api.md. Found: no mobile/ folder.',
     "mobile/ içinde, kaynak dosyası REQ-001'i // serves: REQ-001 gibi bir yorumda adlandıran bir giriş ekranı olmalı; uygulaman da server/login_contract.json içindeki üç endpoint'e (request_code, login ve me) istek göndermeli. Her endpoint'in yolunu week05/api.md içindeki gibi / ile yaz. Bulunan: mobile/ klasörü yok."),
    ('mobile/ must have a login screen whose source file names REQ-001 in a comment like // serves: REQ-001, and your app must send requests to the three endpoints of server/login_contract.json (request_code, login and me). Write the path of each endpoint with its /, as in week05/api.md. Found: no source file in mobile/ (.dart, .js, .ts, .kt, .java or .swift).',
     "mobile/ içinde, kaynak dosyası REQ-001'i // serves: REQ-001 gibi bir yorumda adlandıran bir giriş ekranı olmalı; uygulaman da server/login_contract.json içindeki üç endpoint'e (request_code, login ve me) istek göndermeli. Her endpoint'in yolunu week05/api.md içindeki gibi / ile yaz. Bulunan: mobile/ içinde kaynak dosyası yok (.dart, .js, .ts, .kt, .java ya da .swift)."),
    ('mobile/ must have a login screen whose source file names REQ-001 in a comment like // serves: REQ-001, and your app must send requests to the three endpoints of server/login_contract.json (request_code, login and me). Write the path of each endpoint with its /, as in week05/api.md. Found: no source file in mobile/ names REQ-001 in a serves: comment.',
     "mobile/ içinde, kaynak dosyası REQ-001'i // serves: REQ-001 gibi bir yorumda adlandıran bir giriş ekranı olmalı; uygulaman da server/login_contract.json içindeki üç endpoint'e (request_code, login ve me) istek göndermeli. Her endpoint'in yolunu week05/api.md içindeki gibi / ile yaz. Bulunan: mobile/ içinde REQ-001'i bir serves: yorumunda adlandıran kaynak dosyası yok."),
    ('mobile/ must have a login screen whose source file names REQ-001 in a comment like // serves: REQ-001, and your app must send requests to the three endpoints of server/login_contract.json (request_code, login and me). Write the path of each endpoint with its /, as in week05/api.md. Found: server/login_contract.json is not filled in.',
     "mobile/ içinde, kaynak dosyası REQ-001'i // serves: REQ-001 gibi bir yorumda adlandıran bir giriş ekranı olmalı; uygulaman da server/login_contract.json içindeki üç endpoint'e (request_code, login ve me) istek göndermeli. Her endpoint'in yolunu week05/api.md içindeki gibi / ile yaz. Bulunan: server/login_contract.json doldurulmamış."),
    ('mobile/ must have a login screen whose source file names REQ-001 in a comment like // serves: REQ-001, and your app must send requests to the three endpoints of server/login_contract.json (request_code, login and me). Write the path of each endpoint with its /, as in week05/api.md. Found: no request to: {x}.',
     "mobile/ içinde, kaynak dosyası REQ-001'i // serves: REQ-001 gibi bir yorumda adlandıran bir giriş ekranı olmalı; uygulaman da server/login_contract.json içindeki üç endpoint'e (request_code, login ve me) istek göndermeli. Her endpoint'in yolunu week05/api.md içindeki gibi / ile yaz. Bulunan: istek gönderilmeyenler: {x}."),
    ('week07/phone_login.png shows the login on the phone',
     'week07/phone_login.png telefondaki girişi gösteriyor'),
    ("week07/ must hold phone_login.png (or .jpg): a screenshot of the phone, or of the emulator, that shows the logged-in user's address after the login. Found: no such file.",
     'week07/ içinde phone_login.png (ya da .jpg) olmalı: girişten sonra giriş yapan kullanıcının adresini gösteren, telefonun ya da emülatörün ekran görüntüsü. Bulunan: böyle bir dosya yok.'),
    ('mobile/ has a screen of one of your own must requirements that sends requests to its endpoints',
     "mobile/ içinde kendi must gereksinimlerinden birinin, endpoint'lerine istek gönderen bir ekranı var"),
    ('mobile/ must have a screen of one of your own functional must requirements (not the login, REQ-001): its source file names the requirement in a comment like // serves: REQ-002, and your app sends requests to an endpoint of week05/api.md that serves it. Found: no mobile/ folder.',
     "mobile/ içinde kendi işlevsel must gereksinimlerinden birinin (giriş, yani REQ-001 dışında) bir ekranı olmalı: kaynak dosyası gereksinimi // serves: REQ-002 gibi bir yorumda adlandırır ve uygulaman week05/api.md içinde ona hizmet eden bir endpoint'e istek gönderir. Bulunan: mobile/ klasörü yok."),
    ('mobile/ must have a screen of one of your own functional must requirements (not the login, REQ-001): its source file names the requirement in a comment like // serves: REQ-002, and your app sends requests to an endpoint of week05/api.md that serves it. Found: no source file in mobile/ (.dart, .js, .ts, .kt, .java or .swift).',
     "mobile/ içinde kendi işlevsel must gereksinimlerinden birinin (giriş, yani REQ-001 dışında) bir ekranı olmalı: kaynak dosyası gereksinimi // serves: REQ-002 gibi bir yorumda adlandırır ve uygulaman week05/api.md içinde ona hizmet eden bir endpoint'e istek gönderir. Bulunan: mobile/ içinde kaynak dosyası yok (.dart, .js, .ts, .kt, .java ya da .swift)."),
    ('mobile/ must have a screen of one of your own functional must requirements (not the login, REQ-001): its source file names the requirement in a comment like // serves: REQ-002, and your app sends requests to an endpoint of week05/api.md that serves it. Found: no functional must requirement besides REQ-001 in week02/requirements.json.',
     "mobile/ içinde kendi işlevsel must gereksinimlerinden birinin (giriş, yani REQ-001 dışında) bir ekranı olmalı: kaynak dosyası gereksinimi // serves: REQ-002 gibi bir yorumda adlandırır ve uygulaman week05/api.md içinde ona hizmet eden bir endpoint'e istek gönderir. Bulunan: week02/requirements.json içinde REQ-001 dışında işlevsel must gereksinim yok."),
    ('mobile/ must have a screen of one of your own functional must requirements (not the login, REQ-001): its source file names the requirement in a comment like // serves: REQ-002, and your app sends requests to an endpoint of week05/api.md that serves it. Found: no source file in mobile/ names one of them in a serves: comment.',
     "mobile/ içinde kendi işlevsel must gereksinimlerinden birinin (giriş, yani REQ-001 dışında) bir ekranı olmalı: kaynak dosyası gereksinimi // serves: REQ-002 gibi bir yorumda adlandırır ve uygulaman week05/api.md içinde ona hizmet eden bir endpoint'e istek gönderir. Bulunan: mobile/ içinde bunlardan birini bir serves: yorumunda adlandıran kaynak dosyası yok."),
    ('mobile/ must have a screen of one of your own functional must requirements (not the login, REQ-001): its source file names the requirement in a comment like // serves: REQ-002, and your app sends requests to an endpoint of week05/api.md that serves it. Found: the app sends no request to their endpoints in week05/api.md.',
     "mobile/ içinde kendi işlevsel must gereksinimlerinden birinin (giriş, yani REQ-001 dışında) bir ekranı olmalı: kaynak dosyası gereksinimi // serves: REQ-002 gibi bir yorumda adlandırır ve uygulaman week05/api.md içinde ona hizmet eden bir endpoint'e istek gönderir. Bulunan: uygulama, week05/api.md içindeki endpoint'lerinin hiçbirine istek göndermiyor."),
    ('mobile_runs.json: your tester ran at least three test cases on your phone',
     'mobile_runs.json: testçin telefonunda en az üç test case çalıştırmış'),
    ('Your tester, the student named in week07/group_07.json, must run at least three of your test cases on your phone in round 1, each run recorded under their student number. Found: no runs recorded in week07/mobile_runs.json yet.',
     "Testçin, yani week07/group_07.json içinde adı geçen öğrenci, 1. turda telefonunda test case'lerinden en az üçünü çalıştırmalı; her çalıştırma onun öğrenci numarasıyla kaydedilmeli. Bulunan: week07/mobile_runs.json içinde henüz kayıtlı çalıştırma yok."),
    ('Your tester, the student named in week07/group_07.json, must run at least three of your test cases on your phone in round 1, each run recorded under their student number. Found: no tester in week07/group_07.json.',
     "Testçin, yani week07/group_07.json içinde adı geçen öğrenci, 1. turda telefonunda test case'lerinden en az üçünü çalıştırmalı; her çalıştırma onun öğrenci numarasıyla kaydedilmeli. Bulunan: week07/group_07.json içinde testçi yok."),
    ('Your tester, the student named in week07/group_07.json, must run at least three of your test cases on your phone in round 1, each run recorded under their student number. Found: {n} {u} by your tester in round 1.',
     "Testçin, yani week07/group_07.json içinde adı geçen öğrenci, 1. turda telefonunda test case'lerinden en az üçünü çalıştırmalı; her çalıştırma onun öğrenci numarasıyla kaydedilmeli. Bulunan: 1. turda testçinin {n} çalıştırması."),
    ("mobile_runs.json: at least one of your tester's runs is outside the login",
     'mobile_runs.json: testçinin çalıştırmalarından en az biri girişin dışında'),
    ("At least one of your tester's runs in round 1 must be a test case outside the login (REQ-001): a test case of your own feature. Found: no runs recorded in week07/mobile_runs.json yet.",
     "Testçinin 1. turdaki çalıştırmalarından en az biri girişin (REQ-001) dışında bir test case olmalı: kendi özelliğinin bir test case'i. Bulunan: week07/mobile_runs.json içinde henüz kayıtlı çalıştırma yok."),
    ("At least one of your tester's runs in round 1 must be a test case outside the login (REQ-001): a test case of your own feature. Found: none.",
     "Testçinin 1. turdaki çalıştırmalarından en az biri girişin (REQ-001) dışında bir test case olmalı: kendi özelliğinin bir test case'i. Bulunan: yok."),
    ('mobile_runs.json: every run names a test case from test_cases.json',
     "mobile_runs.json: her çalıştırma test_cases.json içinden bir test case'i anıyor"),
    ('Every run in week07/mobile_runs.json must name a test case that exists in week04/test_cases.json. Found: no runs recorded in week07/mobile_runs.json yet.',
     "week07/mobile_runs.json içindeki her çalıştırma, week04/test_cases.json içinde var olan bir test case'i anmalı. Bulunan: week07/mobile_runs.json içinde henüz kayıtlı çalıştırma yok."),
    ('Every run in week07/mobile_runs.json must name a test case that exists in week04/test_cases.json. Found: not in test_cases.json: {x}.',
     "week07/mobile_runs.json içindeki her çalıştırma, week04/test_cases.json içinde var olan bir test case'i anmalı. Bulunan: test_cases.json içinde olmayanlar: {x}."),
    ('mobile_runs.json: every run names the device and has a result, with a note for fail and blocked',
     'mobile_runs.json: her çalıştırma cihazı anıyor ve bir sonucu var; fail ve blocked için not var'),
    ('Every run in week07/mobile_runs.json must name the phone or the emulator (device) and have a result (pass, fail or blocked), with a note of at least 15 characters for fail and blocked. Found: no runs recorded in week07/mobile_runs.json yet.',
     'week07/mobile_runs.json içindeki her çalıştırma telefonu ya da emülatörü (device) anmalı ve bir sonucu (pass, fail ya da blocked) olmalı; fail ve blocked için en az 15 karakterlik bir not gerekir. Bulunan: week07/mobile_runs.json içinde henüz kayıtlı çalıştırma yok.'),
    ('Every run in week07/mobile_runs.json must name the phone or the emulator (device) and have a result (pass, fail or blocked), with a note of at least 15 characters for fail and blocked. Found: {n} {u} without a device or a valid result, or a fail or blocked without a note.',
     'week07/mobile_runs.json içindeki her çalıştırma telefonu ya da emülatörü (device) anmalı ve bir sonucu (pass, fail ya da blocked) olmalı; fail ve blocked için en az 15 karakterlik bir not gerekir. Bulunan: cihazı ya da geçerli sonucu olmayan veya notsuz fail ya da blocked olan {n} çalıştırma.'),
    ('every functional must requirement has a screen in mobile/',
     'her işlevsel must gereksinimin mobile/ içinde bir ekranı var'),
    ('Every functional must requirement needs a screen in mobile/ whose source file names it in a comment like // serves: REQ-002. Found: no functional must requirement in week02/requirements.json.',
     'Her işlevsel must gereksinimin mobile/ içinde, kaynak dosyası onu // serves: REQ-002 gibi bir yorumda adlandıran bir ekranı olmalı. Bulunan: week02/requirements.json içinde işlevsel must gereksinim yok.'),
    ('Every functional must requirement needs a screen in mobile/ whose source file names it in a comment like // serves: REQ-002. Found: no such screen for {x}.',
     'Her işlevsel must gereksinimin mobile/ içinde, kaynak dosyası onu // serves: REQ-002 gibi bir yorumda adlandıran bir ekranı olmalı. Bulunan: şunlar için böyle bir ekran yok: {x}.'),
    ('your app sends requests to every endpoint of week05/api.md that serves a functional must requirement',
     "uygulaman, week05/api.md içinde işlevsel bir must gereksinime hizmet eden her endpoint'e istek gönderiyor"),
    ('Your app in mobile/ must send requests to every endpoint of week05/api.md that serves a functional must requirement. Write the path of each endpoint with its /, as in api.md. Found: no row of week05/api.md serves a functional must requirement.',
     "mobile/ içindeki uygulaman, week05/api.md içinde işlevsel bir must gereksinime hizmet eden her endpoint'e istek göndermeli. Her endpoint'in yolunu api.md içindeki gibi / ile yaz. Bulunan: week05/api.md içinde işlevsel bir must gereksinime hizmet eden satır yok."),
    ('Your app in mobile/ must send requests to every endpoint of week05/api.md that serves a functional must requirement. Write the path of each endpoint with its /, as in api.md. Found: no request to: {x}.',
     "mobile/ içindeki uygulaman, week05/api.md içinde işlevsel bir must gereksinime hizmet eden her endpoint'e istek göndermeli. Her endpoint'in yolunu api.md içindeki gibi / ile yaz. Bulunan: istek gönderilmeyenler: {x}."),
    ('every functional must requirement has a test case that passed on the phone',
     "her işlevsel must gereksinimin telefonda geçmiş bir test case'i var"),
    ('Every functional must requirement needs at least one of its test cases with a pass in week07/mobile_runs.json. Found: no functional must requirement in week02/requirements.json.',
     "Her işlevsel must gereksinimin week07/mobile_runs.json içinde pass almış en az bir test case'i olmalı. Bulunan: week02/requirements.json içinde işlevsel must gereksinim yok."),
    ('Every functional must requirement needs at least one of its test cases with a pass in week07/mobile_runs.json. Found: no pass for {x}.',
     "Her işlevsel must gereksinimin week07/mobile_runs.json içinde pass almış en az bir test case'i olmalı. Bulunan: şunlar için pass yok: {x}."),
    ('mobile_runs.json: every failed test case was run again in round 2',
     'mobile_runs.json: kalan her test case 2. turda yeniden çalıştırılmış'),
    ('Every test case that failed on the phone in round 1 must be run again in round 2 after the fix, or dropped with a change request. Found: no runs recorded in week07/mobile_runs.json yet.',
     '1. turda telefonda kalan her test case, düzeltmeden sonra 2. turda yeniden çalıştırılmalı ya da bir change request ile bırakılmalı. Bulunan: week07/mobile_runs.json içinde henüz kayıtlı çalıştırma yok.'),
    ('Every test case that failed on the phone in round 1 must be run again in round 2 after the fix, or dropped with a change request. Found: no round 2 for {x}.',
     '1. turda telefonda kalan her test case, düzeltmeden sonra 2. turda yeniden çalıştırılmalı ya da bir change request ile bırakılmalı. Bulunan: şunlar için 2. tur yok: {x}.'),
    ('the app id in mobile/ is the package of S2 in week04/store.json',
     "mobile/ içindeki uygulama kimliği, week04/store.json içindeki S2'nin paketi"),
    ('The id of your app (applicationId in build.gradle, android.package and ios.bundleIdentifier in app.json, or PRODUCT_BUNDLE_IDENTIFIER in Xcode) must be the package name of S2 in week04/store.json. Found: no package in S2 of week04/store.json.',
     "Uygulamanın kimliği (build.gradle içinde applicationId, app.json içinde android.package ve ios.bundleIdentifier ya da Xcode'da PRODUCT_BUNDLE_IDENTIFIER), week04/store.json içindeki S2'nin paket adı olmalı. Bulunan: week04/store.json içindeki S2'de paket yok."),
    ('The id of your app (applicationId in build.gradle, android.package and ios.bundleIdentifier in app.json, or PRODUCT_BUNDLE_IDENTIFIER in Xcode) must be the package name of S2 in week04/store.json. Found: no app id in mobile/.',
     "Uygulamanın kimliği (build.gradle içinde applicationId, app.json içinde android.package ve ios.bundleIdentifier ya da Xcode'da PRODUCT_BUNDLE_IDENTIFIER), week04/store.json içindeki S2'nin paket adı olmalı. Bulunan: mobile/ içinde uygulama kimliği yok."),
    ('The id of your app (applicationId in build.gradle, android.package and ios.bundleIdentifier in app.json, or PRODUCT_BUNDLE_IDENTIFIER in Xcode) must be the package name of S2 in week04/store.json. Found: {x}, not {y}.',
     "Uygulamanın kimliği (build.gradle içinde applicationId, app.json içinde android.package ve ios.bundleIdentifier ya da Xcode'da PRODUCT_BUNDLE_IDENTIFIER), week04/store.json içindeki S2'nin paket adı olmalı. Bulunan: {x}; {y} değil."),
    ('no build files of mobile/ are in git',
     "mobile/ build dosyalarının hiçbiri git'te değil"),
    ('mobile/ must not have in git the folders your framework builds again (node_modules, build, .dart_tool, .gradle, Pods, .expo): add them to mobile/.gitignore, then git rm -r --cached mobile/<the folder>. Found: no mobile/ folder.',
     "mobile/, framework'ünün yeniden üretebildiği klasörleri (node_modules, build, .dart_tool, .gradle, Pods, .expo) git'te tutmamalı: onları mobile/.gitignore dosyasına ekle, sonra git rm -r --cached mobile/<klasör>. Bulunan: mobile/ klasörü yok."),
    ('mobile/ must not have in git the folders your framework builds again (node_modules, build, .dart_tool, .gradle, Pods, .expo): add them to mobile/.gitignore, then git rm -r --cached mobile/<the folder>. Found: in git: {x}.',
     "mobile/, framework'ünün yeniden üretebildiği klasörleri (node_modules, build, .dart_tool, .gradle, Pods, .expo) git'te tutmamalı: onları mobile/.gitignore dosyasına ekle, sonra git rm -r --cached mobile/<klasör>. Bulunan: git'te olanlar: {x}."),
    ('all ten course tests still pass',
     'on ders testinin hepsi hala geçiyor'),
    ('All ten course tests (course_tests/) must still pass. Found: not passing: {x}.',
     'On ders testinin (course_tests/) hepsi hala geçmeli. Bulunan: geçmeyenler: {x}.'),
    ('All ten course tests (course_tests/) must still pass. Found: {f}.',
     'On ders testinin (course_tests/) hepsi hala geçmeli. Bulunan: {f}.'),
    ('every test case of a must requirement with run "server" still has a test that passes',
     'run değeri "server" olan, must bir gereksinimin her test case\'inin hala geçen bir testi var'),
    ('Every test case of a must requirement with "run": "server" in week04/test_cases.json must still have a test in server/tests/ named by its id that passes. Found: no test case of a must requirement with "run": "server".',
     'week04/test_cases.json içinde "run": "server" olan, must bir gereksinimin her test case\'inin server/tests/ içinde kendi id\'siyle adlandırılmış ve hala geçen bir testi olmalı. Bulunan: "run": "server" olan, must bir gereksinimin test case\'i yok.'),
    ('Every test case of a must requirement with "run": "server" in week04/test_cases.json must still have a test in server/tests/ named by its id that passes. Found: no passing test for {x}.',
     'week04/test_cases.json içinde "run": "server" olan, must bir gereksinimin her test case\'inin server/tests/ içinde kendi id\'siyle adlandırılmış ve hala geçen bir testi olmalı. Bulunan: şunların geçen testi yok: {x}.'),
    ('Every test case of a must requirement with "run": "server" in week04/test_cases.json must still have a test in server/tests/ named by its id that passes. Found: {f}.',
     'week04/test_cases.json içinde "run": "server" olan, must bir gereksinimin her test case\'inin server/tests/ içinde kendi id\'siyle adlandırılmış ve hala geçen bir testi olmalı. Bulunan: {f}.'),
    ('week07/ai_log_07.md names the commit of the change you accepted',
     "week07/ai_log_07.md kabul ettiğin değişikliğin commit'ini anıyor"),
    ('week07/ai_log_07.md must name the commit of the change you accepted: the first 7 characters of its commit id, outside the comments and the Evidence block. Found: no commit id.',
     "week07/ai_log_07.md kabul ettiğin değişikliğin commit'ini anmalı: commit kimliğinin ilk 7 karakteri, yorumların ve Evidence bloğunun dışında. Bulunan: commit kimliği yok."),
    ('week07/ai_log_07.md must name the commit of the change you accepted: the first 7 characters of its commit id, outside the comments and the Evidence block. Found: {x}, not a commit of this repository.',
     "week07/ai_log_07.md kabul ettiğin değişikliğin commit'ini anmalı: commit kimliğinin ilk 7 karakteri, yorumların ve Evidence bloğunun dışında. Bulunan: {x}; bu reponun bir commit'i değil."),
    ('week07/ai_log_07.md holds the git diff of the change',
     "week07/ai_log_07.md değişikliğin git diff'ini içeriyor"),
    ('week07/ai_log_07.md must hold, in the Evidence block, the git diff of the change as your terminal showed it (the lines that start with diff --git and @@). Found: none.',
     "week07/ai_log_07.md, Evidence bloğunda değişikliğin git diff'ini terminalinin gösterdiği gibi içermeli (diff --git ve @@ ile başlayan satırlar). Bulunan: yok."),
    # a course test the entries above do not name (they come first, so every LOGIN_NN of the table has its own Turkish)
    ('course test {k}: {w}', 'ders testi {k}: {w}'),
    ('Course test {k} ({w}) must pass. Found: {f}.', '{k} ders testi ({w}) geçmeli. Bulunan: {f}.'),
]

# Messages of the run itself (not of a check), same {name} fields; Turkish only when `tr` was asked for.
TR_UI = {
    "pytest, fastapi or freezegun is not installed: run pip install -r week06/requirements.txt in your virtual environment, then run the checker again":
        "pytest, fastapi ya da freezegun kurulu değil: sanal ortamında pip install -r week06/requirements.txt çalıştır, sonra checker'ı yeniden çalıştır",
    "Your week{w}/requirements.txt did not install pytest, fastapi and freezegun, so the course's own file was installed for the tests. Replace your file with the course's week{w}/requirements.txt.":
        "week{w}/requirements.txt dosyan pytest, fastapi ve freezegun'u kurmadı; bu yüzden testler için dersin kendi dosyası kuruldu. Dosyanı dersin week{w}/requirements.txt dosyasıyla değiştir.",
    "it did not run (see the tests' own output: python -m pytest course_tests -q)":
        "çalışmadı (testlerin kendi çıktısına bak: python -m pytest course_tests -q)",
    "Secret scan": "Gizli anahtar taraması",
    "no API keys found": "API anahtarı bulunamadı",
    "KEYS FOUND — remove them and rotate them NOW": "ANAHTAR BULUNDU — hemen sil ve yenile",
    "This is an automatic 10-point deduction. Remove the key, rotate it": "Bu otomatik 10 puan kesintisidir. Anahtarı sil, sağlayıcıda yenile",
    "at the provider, and never commit one again.": "ve bir daha asla anahtar commit etme.",
    "SECRET  {rel} — looks like a {label}": "GİZLİ  {rel} — şuna benziyor: {label}",
    "WARNING: could not reach the course on GitHub, so this run uses the": "UYARI: GitHub'daki derse ulaşılamadı, bu yüzden bu çalıştırma",
    "checker copy stored in your repository, which may be out of date.": "reponda duran checker kopyasını kullanıyor; güncel olmayabilir.",
    "Connect to the network and run it again before trusting the list.": "Listeye güvenmeden önce internete bağlan ve yeniden çalıştır.",
    "(using the current checker published by the course)": "(dersin yayımladığı güncel checker kullanılıyor)",
    "Course files brought into this repository (add them with `git add .`):": "Dersin dosyaları bu repoya getirildi (`git add .` ile ekle):",
    "Cannot tell which week it is.": "Hangi haftada olduğumuz anlaşılamıyor.",
    "The course could not be reached and there is no cached week number\nyet — this is the first run on this machine, offline. Connect once\nand run it again; after that it works without a network.":
        "Derse ulaşılamadı ve henüz önbellekte bir hafta numarası yok —\nbu makinedeki ilk çalıştırma ve internet yok. Bir kez bağlan ve\nyeniden çalıştır; sonrasında internetsiz de çalışır.",
    "Week 0 ({source}) — nothing to check yet.": "Hafta 0 ({source}) — henüz kontrol edilecek bir şey yok.",
    "The course has not started checking deliverables. Nothing for you to do.": "Ders henüz teslimleri kontrol etmeye başlamadı. Yapman gereken bir şey yok.",
    "Give one week number, for example: python .github/check_deliverables.py 2": "Tek bir hafta numarası ver, örneğin: python .github/check_deliverables.py 2 tr",
    "Weeks start at 1.": "Haftalar 1'den başlar.",
    "Week {n} has not started yet. The course is at week {current}.": "{n}. hafta henüz başlamadı. Ders {current}. haftada.",
    "Checking week {shown}  ({source})": "{shown}. hafta kontrol ediliyor  ({source})",
    "To check another week, add its number: python .github/check_deliverables.py {other}": "Başka bir haftayı kontrol etmek için numarasını ekle: python .github/check_deliverables.py {other} tr",
    "published by the course": "dersin yayımladığı",
    "cached — the course could not be reached": "önbellekten — derse ulaşılamadı",
    "There are no checks for week {shown} yet.": "{shown}. hafta için henüz kontrol yok.",
    "Was due at the end of the session": "Oturum sonunda teslim edilmesi gerekiyordu",
    "Due at the end of the session": "Oturum sonunda teslim",
    "Was due Saturday 23:59": "Cumartesi 23:59'a kadar teslim edilmesi gerekiyordu",
    "Due by Saturday 23:59": "Cumartesi 23:59'a kadar teslim",
    "In the lab:     {a} of {b} done": "Derste:           {a} / {b} tamam",
    'Your commits this week, piece by piece (read on this computer; your mark reads GitHub):':
        "Bu haftaki commit'lerin, iş iş (bu bilgisayardan okundu; notun GitHub'dan okunur):",
    "the app in mobile/":
        "mobile/ içindeki uygulama",
    "the login screen":
        "giriş ekranı",
    "the screen of your requirement":
        "gereksiniminin ekranı",
    "the tester round":
        "testçi turu",
    "{piece}: {n} commits":
        "{piece}: {n} commit",
    "{piece}: 1 commit. Commit it again when it works.":
        "{piece}: 1 commit. Çalışınca yeniden commit et.",
    "{piece}: no commit yet.":
        "{piece}: henüz commit yok.",
    "Commit {sha} adds {k} new screens: {names}. Each new screen must have its own commit; a commit that adds two or more costs the commit point.":
        "{sha} commit'i {k} yeni ekran ekliyor: {names}. Her yeni ekranın kendi commit'i olmalı; iki ya da daha fazlasını ekleyen bir commit, commit puanına mal olur.",
    "Commit {sha} adds {k} new routes: {names}. Each new route must have its own commit; a commit that adds two or more costs the commit point.":
        "{sha} commit'i {k} yeni route ekliyor: {names}. Her yeni route'un kendi commit'i olmalı; iki ya da daha fazlasını ekleyen bir commit, commit puanına mal olur.",
    "Your changes not yet committed add {k} new screens: {names}. Commit them one at a time.":
        "Henüz commit etmediğin değişiklikler {k} yeni ekran ekliyor: {names}. Bunları tek tek commit et.",
    "Your changes not yet committed add {k} new routes: {names}. Commit them one at a time; git add -p lets you take the lines of one route first.":
        "Henüz commit etmediğin değişiklikler {k} yeni route ekliyor: {names}. Bunları tek tek commit et; git add -p ile önce tek bir route'un satırlarını alabilirsin.",
    "1 commit is not pushed yet. Push it now: git push":
        "1 commit henüz push edilmedi. Şimdi push et: git push",
    "{n} commits are not pushed yet. Push them now: git push":
        "{n} commit henüz push edilmedi. Şimdi push et: git push",
    '1 commit by a coding agent is not counted.':
        "Bir kodlama ajanının 1 commit'i sayılmaz.",
    '{n} commits by a coding agent are not counted.':
        "Bir kodlama ajanının {n} commit'i sayılmaz.",
    "\n  A red result while a piece is still unfinished is normal and costs you nothing.\n  Commit and push it anyway. The lecture mark reads only your last push at the end\n  of the lecture, and the Saturday mark reads your final state.":
        "\n  Bir parça henüz bitmemişken kırmızı görmen normaldir ve sana puan kaybettirmez.\n  Yine de commit ve push et. Ders puanı yalnızca dersin sonundaki son push'unu,\n  Cumartesi puanı ise son durumunu okur.",
    "By Saturday:    {a} of {b} done": "Cumartesiye dek:  {a} / {b} tamam",
    "Earlier weeks, checks still failing: {listing} — see one with: python .github/check_deliverables.py {n}":
        "Önceki haftalarda hala eksik olan kontroller: {listing} — birine bakmak için: python .github/check_deliverables.py {n} tr",
    "\n  {n} still to do before Saturday 23:59. Those do not fail this run —\n  they are not due yet. The lab items are what the end-of-session mark reads.":
        "\n  Cumartesi 23:59'a kadar yapılacak {n} madde var. Bunlar bu çalıştırmada kalmış sayılmaz —\n  henüz süreleri gelmedi. Oturum sonu notu yalnızca ders içi maddeleri okur.",
    "PASS": "TAMAM",
    "FAIL": "EKSİK",
    "NOT YET": "BEKLİYOR",
    "({k} not yet)": "({k} bekliyor)",
    "{n} line(s) above have no Turkish yet and are shown in English.": "Yukarıdaki {n} satırın henüz Türkçesi yok, İngilizce gösterildi.",
}

LANG = "en"  # "tr" only in a student's own run that asked for it (see wanted_lang)
_UNTRANSLATED: set[str] = set()


def wanted_lang(argv: list[str] | None = None) -> str:
    """Turkish if the student added `tr` to the command line. The instructor's capture
    (AIASD_SLOT set) is always English: the grading reads the English sentences."""
    if os.environ.get("AIASD_SLOT", "").strip().lower() in (SESSION, DEADLINE):
        return "en"
    args = [a.strip().lower() for a in (sys.argv[1:] if argv is None else argv)]
    return "tr" if "tr" in args else "en"


def say(text: str, **kw) -> str:
    """A message of the run in the language asked for; English when there is no Turkish for it."""
    out = TR_UI.get(text) if LANG == "tr" else None
    out = out or text
    return out.format(**kw) if kw else out


_TR_COMPILED: list | None = None


def _compile_tr() -> list:
    global _TR_COMPILED
    if _TR_COMPILED is None:
        compiled = []
        for en, tr in TR_RULES:
            parts = []
            for tok in re.split(r"(\{\{|\}\}|\{\w+\})", " ".join(en.split())):
                if tok == "{{":
                    parts.append(re.escape("{"))
                elif tok == "}}":
                    parts.append(re.escape("}"))
                elif len(tok) > 2 and tok[0] == "{" and tok[-1] == "}":
                    pat = r"\d+" if tok == "{n}" else ".+?"
                    parts.append("(?P<%s>%s)" % (tok[1:-1], pat))
                else:
                    parts.append(re.escape(tok))
            compiled.append((re.compile("".join(parts)), tr))
        _TR_COMPILED = compiled
    return _TR_COMPILED


# The reasons the instructor's capture gives for a GitHub Actions run (AIASD_CI_WHY / AIASD_CI_UNTRUSTED), in Turkish,
# so that a "Found:" in a Turkish sentence is Turkish too (VC, 1 Nov 2026). Matched from the start of the text.
CI_FOUND_TR = [
    ("the GitHub Actions run of the commit read had not finished when it was read",
     "okunan commit'in GitHub Actions çalıştırması okunduğunda henüz bitmemişti"),
    ("no GitHub Actions run for the commit read", "okunan commit için bir GitHub Actions çalıştırması yok"),
    ("the GitHub Actions run of the commit read did not start", "okunan commit'in GitHub Actions çalıştırması başlamadı"),
    ("the GitHub Actions run of the commit read holds no test results",
     "okunan commit'in GitHub Actions çalıştırmasında test sonucu yok"),
    ("the GitHub Actions run of the commit read has no 'Weekly deliverables' job",
     "okunan commit'in GitHub Actions çalıştırmasında 'Weekly deliverables' işi yok"),
    ("the log of the GitHub Actions run of the commit read could not be read",
     "okunan commit'in GitHub Actions çalıştırmasının kaydı okunamadı"),
    ("the GitHub Actions run of the commit read cannot be used: .github/workflows/check.yml is not a version the course published",
     "okunan commit'in GitHub Actions çalıştırması kullanılamıyor: .github/workflows/check.yml dersin yayımladığı bir sürüm değil"),
    ("the GitHub Actions run of the commit read cannot be used", "okunan commit'in GitHub Actions çalıştırması kullanılamıyor"),
    ("in GitHub Actions, pytest, fastapi or freezegun is not installed: run pip install -r week06/requirements.txt in your "
     "virtual environment, then run the checker again",
     "GitHub Actions'ta pytest, fastapi ya da freezegun kurulu değil: sanal ortamında pip install -r week06/requirements.txt "
     "çalıştır, sonra checker'ı yeniden çalıştır"),
    ("in GitHub Actions, pytest, fastapi or freezegun is not installed",
     "GitHub Actions'ta pytest, fastapi ya da freezegun kurulu değil"),
]


def _tr_field(value: str) -> str:
    for en, tr in CI_FOUND_TR:
        if value.startswith(en):
            rest = value[len(en):]
            return tr + (rest if not rest.strip() or rest.lstrip().startswith((":", "(")) else "")
    return value


def translate_sentence(sentence: str) -> str | None:
    """The Turkish text for one sentence the checker printed (PASS or FAIL), or None if the
    table has no entry for it."""
    s = " ".join((sentence or "").split())
    for rx, tr in _compile_tr():
        m = rx.fullmatch(s)
        if m:
            fields = {k: _tr_field(v) if isinstance(v, str) else v for k, v in m.groupdict().items()}
            return re.sub(r"\{\{|\}\}|\{(\w+)\}",
                          lambda t: "{" if t.group(0) == "{{" else "}" if t.group(0) == "}}" else fields.get(t.group(1), t.group(0)), tr)
    return None


def shown_sentence(text: str) -> str:
    """What a check line prints: the Turkish when asked for, the English sentence otherwise."""
    if LANG != "tr":
        return text
    out = translate_sentence(text)
    if out is None:
        _UNTRANSLATED.add(text)
        return text
    return out



# ── main ─────────────────────────────────────────────────────────────


CHECKER_URL = (
    "https://raw.githubusercontent.com/vedatcoskun-course/aiasd-template"
    "/main/.github/check_deliverables.py"
)


def maybe_update() -> None:
    """Run the current published checker instead of this frozen copy.

    A student repository is created from the template once and never updated
    again, so the copy sitting in it is the one from the week they started. By
    Week 8 it would be checking Week 1 and showing a green tick for work it does
    not know how to look at. The grade would still be right — that is computed
    with the instructor's own copy — but the feedback would be silently empty,
    which is worse than no feedback.

    So: fetch the published checker, and if it differs from this one, hand over
    to it. Anything that goes wrong — no network, a captive portal, a truncated
    file, a syntax error — means carrying on with the local copy.
    """
    if os.environ.get("AIASD_NO_SELFUPDATE"):
        return  # we are already the downloaded copy
    if os.environ.get("AIASD_WEEK") or os.environ.get("AIASD_SLOT"):
        return  # the instructor is grading, and grading runs its own copy

    try:
        with urllib.request.urlopen(CHECKER_URL, timeout=6) as response:
            published = response.read().decode("utf-8")
    except (urllib.error.URLError, OSError, TimeoutError, UnicodeDecodeError):
        # Offline, or GitHub unreachable from this network. The copy in the
        # repository may be weeks old and look for files the course no longer
        # asks for - say so loudly rather than let a stale list pass for the truth.
        print("  " + say("WARNING: could not reach the course on GitHub, so this run uses the"))
        print("  " + say("checker copy stored in your repository, which may be out of date."))
        print("  " + say("Connect to the network and run it again before trusting the list.") + "\n")
        return

    mine = Path(__file__).read_text(encoding="utf-8", errors="replace")
    if published == mine:
        return
    if MARKER not in published or len(published) < 4000:
        return
    try:
        compile(published, "check_deliverables.py", "exec")
    except SyntaxError:
        return

    # Keep the repository's own copy current too, so that an offline run later
    # falls back to a recent checker instead of the one from the week the
    # repository was created. Best effort: a read-only file is not an error.
    try:
        Path(__file__).write_text(published, encoding="utf-8")
    except OSError:
        pass

    tmp = Path(tempfile.gettempdir()) / "aiasd_check_deliverables.py"
    try:
        tmp.write_text(published, encoding="utf-8")
    except OSError:
        return

    print("  " + say("(using the current checker published by the course)") + "\n")
    env = {
        **os.environ,
        "AIASD_NO_SELFUPDATE": "1",
        "AIASD_ROOT": str(ROOT),
    }
    raise SystemExit(
        subprocess.run([sys.executable, str(tmp), *sys.argv[1:]], env=env, check=False).returncode
    )


COURSE_WEEK_URL = (
    "https://raw.githubusercontent.com/vedatcoskun-course/aiasd-template/main/CURRENT_WEEK.txt"
)


def cached_week() -> int:
    raw = (read("CURRENT_WEEK_CACHE.txt") or "0").strip().splitlines()
    try:
        return int(raw[0]) if raw and raw[0].strip() else 0
    except ValueError:
        return 0


def prose_words(md: str) -> int:
    """Count only what the student wrote themselves.

    A scaffold with headings, instructions and HTML comments can be hundreds of
    words before anyone has typed anything, and pasted model output is evidence,
    not prose. Counting the raw file would let a word-count check pass on an
    untouched template — so headings, quoted instructions, comments and fenced
    blocks are all removed before counting.
    """
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.DOTALL)
    md = re.sub(r"```.*?```", " ", md, flags=re.DOTALL)
    kept = []
    for line in md.splitlines():
        s = line.strip()
        if not s or s.startswith((">", "#", "|", "---", "***")):
            continue
        kept.append(s)
    return len(" ".join(kept).split())


def my_section() -> str:
    """The section this student is in, from their own student.json."""
    raw = read("student.json")
    if not raw:
        return ""
    try:
        return str(json.loads(raw).get("section", "")).strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return ""


def parse_published(text: str, section: str) -> int | None:
    """Read the published week for one section.

    The file carries a line per section — `en=3`, `tr=2` — because two sections
    drift apart the first time a holiday lands on one of their days. A bare
    number is the older single-section format and applies to everyone.
    """
    weeks: dict[str, int] = {}
    only = None
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            if value.strip().isdigit():
                weeks[key.strip().lower()] = int(value.strip())
        elif line.isdigit():
            only = int(line)
    if section and section in weeks:
        return weeks[section]
    if only is not None:
        return only
    if weeks and len(set(weeks.values())) == 1:
        # No section declared, but the sections happen to be in step, so the
        # answer is the same either way.
        return next(iter(weeks.values()))
    return None


def published_week() -> int | None:
    """The week the course says it is on. None if it cannot be reached."""
    try:
        with urllib.request.urlopen(COURSE_WEEK_URL, timeout=5) as response:
            return parse_published(response.read().decode("utf-8"), my_section())
    except (urllib.error.URLError, ValueError, IndexError, OSError, TimeoutError):
        return None


def resolve_week() -> tuple[int, str]:
    """Decide which week to check, and say where the number came from.

    Order matters. The published number wins over the local file, because the
    failure this prevents is a stale local file quietly checking Week 1 all
    through Week 5 and showing you a green tick you have not earned.
    """
    override = os.environ.get("AIASD_WEEK", "").strip()
    if override:
        try:
            return int(override), "AIASD_WEEK"
        except ValueError:
            print(f"AIASD_WEEK must be a number, not {override!r}")
            raise SystemExit(1) from None

    published = published_week()
    if published is not None:
        if published != cached_week():
            try:
                (ROOT / "CURRENT_WEEK_CACHE.txt").write_text(f"{published}\n", encoding="utf-8")
            except OSError:
                pass  # read-only checkout; the number is still correct
        return published, "published by the course"
    return cached_week(), "cached — the course could not be reached"


MANIFEST_URL = (
    "https://raw.githubusercontent.com/vedatcoskun-course/aiasd-template/main/AI_MANIFEST.txt"
)
RAW_BASE = "https://raw.githubusercontent.com/vedatcoskun-course/aiasd-template/main/"


ROOT_CODE_FROM = {"server": 5}  # code folders at the root of the template, and the week they arrive in
COURSE_CODE_FROM = {"course_tests": 6}  # code the course owns (VC, 22 Oct 2026): brought and put back like AI_* files
COURSE_FILE_FROM = {"server/course_login.py": 6}  # one file of the course inside server/ (VC, 22 Oct 2026): the same


def sync_course_files(current: int) -> None:
    """Bring the course's files into this repository, so nobody has to fetch the template.

    The template publishes AI_MANIFEST.txt: one line per file, `sha256  path`. Two
    kinds of entry, treated differently:

    - course documents at the root (`AI_*`, `AI_Doc2_media/…`): the course owns them,
      so a missing or changed one is (re)written here;
    - the course's tests (`course_tests/…`) and its login (`server/course_login.py`), from Week 6:
      the course owns them too, so they are (re)written like the documents;
    - a week's folder (`weekNN/…`), the `PROPOSAL.md` scaffold and the `server/` starter
      (from Week 5): yours once you have them, so a file is written only if it does not
      exist yet — never overwritten — and only for weeks the course has published.

    Whatever arrives is untracked until you `git add .`; the run says so. Offline,
    or under CI, nothing happens. Anything that goes wrong means carrying on.
    """
    if os.environ.get("GITHUB_ACTIONS") or os.environ.get("AIASD_WEEK") or os.environ.get("AIASD_SLOT"):
        return
    try:
        with urllib.request.urlopen(MANIFEST_URL, timeout=6) as response:
            manifest = response.read().decode("utf-8")
    except (urllib.error.URLError, OSError, TimeoutError, UnicodeDecodeError):
        return
    fetched: list[str] = []
    for line in manifest.splitlines():
        parts = line.strip().split("  ", 1)
        if len(parts) != 2 or ".." in parts[1] or parts[1].startswith("/"):
            continue
        digest, rel = parts
        target = ROOT / rel
        if rel.startswith("week"):
            m = re.match(r"week(\d{2})/", rel)
            if not m or int(m.group(1)) > current or target.exists():
                continue
        elif rel == "PROPOSAL.md":
            if current < 2 or target.exists():
                continue
        elif rel in COURSE_FILE_FROM or rel.split("/")[0] in COURSE_CODE_FROM:  # the course's, put back if changed
            if current < COURSE_FILE_FROM.get(rel, COURSE_CODE_FROM.get(rel.split("/")[0], 99)):
                continue
            if target.exists():
                try:
                    if hashlib.sha256(target.read_bytes()).hexdigest() == digest:
                        continue
                except OSError:
                    continue
        elif rel.split("/")[0] in ROOT_CODE_FROM:  # server/ from Week 5: yours once you have it
            if current < ROOT_CODE_FROM[rel.split("/")[0]] or target.exists():
                continue
        elif rel.startswith("AI_"):
            if target.exists():
                try:
                    if hashlib.sha256(target.read_bytes()).hexdigest() == digest:
                        continue
                except OSError:
                    continue
        else:
            continue
        try:
            with urllib.request.urlopen(RAW_BASE + urllib.parse.quote(rel), timeout=10) as response:
                data = response.read()
        except (urllib.error.URLError, OSError, TimeoutError):
            continue
        if hashlib.sha256(data).hexdigest() != digest:
            continue
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            fetched.append(rel)
        except OSError:
            continue
    if fetched:
        print("  " + say("Course files brought into this repository (add them with `git add .`):"))
        for rel in fetched:
            print(f"    + {rel}")
        print()


def week_to_show(args: list[str], current: int) -> tuple[int, str]:
    """The week a student's run prints: the one named on the command line, else the current one.

    Returns (week, "") or (0, the message to print). Showing every week since Week 1 made the
    list grow by a screenful each week, and an old, finished week buried the one that is due.
    """
    args = [a.strip() for a in args if a.strip() and a.strip().lower() not in ("tr", "en")]  # language words
    if not args:
        return current, ""
    if len(args) > 1 or not args[0].isdigit():
        return 0, say("Give one week number, for example: python .github/check_deliverables.py 2")
    n = int(args[0])
    if n < 1:
        return 0, say("Weeks start at 1.")
    if n > current:
        return 0, say("Week {n} has not started yet. The course is at week {current}.", n=n, current=current)
    return n, ""


def main() -> int:
    global RUN_WEEK, LANG
    LANG = wanted_lang()  # before anything is printed: the update warnings are said in it too
    maybe_update()
    current, source = resolve_week()
    RUN_WEEK = current
    sync_course_files(current)

    print("=" * 64)
    print("  " + say("Secret scan"))
    print("=" * 64)
    secrets_ok = check_secrets()
    if secrets_ok:
        print("  " + say("no API keys found") + "\n")
    else:
        print("  " + say("KEYS FOUND — remove them and rotate them NOW"))
        print("  " + say("This is an automatic 10-point deduction. Remove the key, rotate it"))
        print("  " + say("at the provider, and never commit one again.") + "\n")

    if current < 1:
        if source.startswith("cached"):
            print(say("Cannot tell which week it is."))
            print(say(
                "The course could not be reached and there is no cached week number\n"
                "yet — this is the first run on this machine, offline. Connect once\n"
                "and run it again; after that it works without a network."
            ))
        else:
            print(say("Week 0 ({source}) — nothing to check yet.", source=say(source)))
            print(say("The course has not started checking deliverables. Nothing for you to do."))
        return 0 if secrets_ok else 1

    # The instructor's capture sets AIASD_SLOT; it reads weeks 1..current and counts only the
    # week it asked for. A student's own run shows one week: the current one, or the one
    # named on the command line.
    scored = os.environ.get("AIASD_SLOT", "").strip().lower()
    grading = scored in (SESSION, DEADLINE)
    shown, problem = (current, "") if grading else week_to_show(sys.argv[1:], current)
    if problem:
        print(problem)
        return 2

    if grading:
        print(f"Checking weeks 1-{current}  ({source})\n")
        last = current
    else:
        print(say("Checking week {shown}  ({source})", shown=shown, source=say(source)))
        other = shown - 1 if shown > 1 else (shown + 1 if current > shown else 0)
        if other:
            print(say("To check another week, add its number: python .github/check_deliverables.py {other}", other=other))
        print()
        last = shown

    for week in range(1, last + 1):
        if week in CHECKS:
            CHECKS[week]()

    def show(rows: list[tuple[str, str, str, str, str]], heading: str, by_week: bool) -> None:
        """One line per check, the verdict first so a column of PASS and FAIL can be scanned,
        and nothing padded to a common width: a line is as long as its sentence."""
        if not rows:
            return
        print("=" * 64)
        print(f"  {heading}")
        print("=" * 64)
        seen = None
        for wk, name, status, _, detail in rows:
            if by_week and wk != seen:
                print(f"  -- Week {wk[1:]} " + "-" * (58 - len(wk)))
                seen = wk
            if status == PASS:
                print(f"  ✓ {say('PASS')}  {shown_sentence(name)}")
            elif status == NOTYET:
                print(f"  · {say('NOT YET')}  {shown_sentence(name)}. {shown_sentence(detail)}")
            else:
                print(f"  ✗ {say('FAIL')}  {shown_sentence(detail)}")
        print()

    if grading:
        slots = [SESSION] if scored == SESSION else [SESSION, DEADLINE]
        rows = [r for r in results if r[3] in slots]
        show(rows, f"Weeks 1-{current}", True)
        failed = [r for r in rows if r[2] == FAIL]
        waiting = [r for r in rows if r[2] == NOTYET]
        print("-" * 64)
        print(
            f"  {len(rows) - len(failed) - len(waiting)} passed, {len(failed)} failed"
            + (f", {len(waiting)} not yet" if waiting else "")
            + f"  (weeks 1-{current}, {scored})"
        )
        print("-" * 64)
        return 0 if (not failed and secrets_ok) else 1

    mine = [r for r in results if r[0] == f"W{shown}"]
    if not mine:
        print(say("There are no checks for week {shown} yet.", shown=shown))
        return 0 if secrets_ok else 1
    past = shown < current
    session_rows = [r for r in mine if r[3] == SESSION]
    deadline_rows = [r for r in mine if r[3] == DEADLINE]
    show(session_rows, say("Was due at the end of the session" if past else "Due at the end of the session"), False)
    show(deadline_rows, say("Was due Saturday 23:59" if past else "Due by Saturday 23:59"), False)

    s_bad = [r for r in session_rows if r[2] == FAIL]
    d_bad = [r for r in deadline_rows if r[2] == FAIL]
    s_wait = [r for r in session_rows if r[2] == NOTYET]
    d_wait = [r for r in deadline_rows if r[2] == NOTYET]
    older: dict[int, int] = {}
    for r in results:
        n = int(r[0][1:])
        if n < shown and r[2] == FAIL:
            older[n] = older.get(n, 0) + 1
    print("-" * 64)
    print("  " + say("In the lab:     {a} of {b} done", a=len(session_rows) - len(s_bad) - len(s_wait), b=len(session_rows) - len(s_wait))
          + ("  " + say("({k} not yet)", k=len(s_wait)) if s_wait else ""))
    print("  " + say("By Saturday:    {a} of {b} done", a=len(deadline_rows) - len(d_bad) - len(d_wait), b=len(deadline_rows) - len(d_wait))
          + ("  " + say("({k} not yet)", k=len(d_wait)) if d_wait else ""))
    if older:
        listing = " · ".join(f"week{n:02d}: {older[n]}" for n in sorted(older, reverse=True))
        print("  " + say(
            "Earlier weeks, checks still failing: {listing} — see one with: python .github/check_deliverables.py {n}",
            listing=listing, n=max(older)))
    print("-" * 64)
    if not past:
        live = live_commits(shown)
        if live:
            print("\n  " + "\n  ".join(live))
    if s_bad and not past:   # VC, 1 Nov 2026: a red run on unfinished work must not stop anyone from committing
        print(say("\n  A red result while a piece is still unfinished is normal and costs you nothing.\n  Commit and push it anyway. The lecture mark reads only your last push at the end\n  of the lecture, and the Saturday mark reads your final state."))
    if d_bad and not s_bad and not past:
        print(say(
            "\n  {n} still to do before Saturday 23:59. Those do not fail this run —\n"
            "  they are not due yet. The lab items are what the end-of-session mark reads.",
            n=len(d_bad)))
    if LANG == "tr" and _UNTRANSLATED:
        print("\n  " + say("{n} line(s) above have no Turkish yet and are shown in English.", n=len(_UNTRANSLATED)))
    return 0 if (not s_bad and secrets_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
