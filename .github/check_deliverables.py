#!/usr/bin/env python3
"""
Checks this week's deliverables — the same checks the instructor runs.

Every week from 1 up to the current one is verified, not just the latest. That is
deliberate: a change that breaks Week 3 should not pass silently in Week 7.

Which week is "current" is not yours to set. It is published by the course and
read from there on every run, so the checks you see are always the checks being
run against you. The WEEK file is only a cache of that number, refreshed
automatically, so this still works on a train with no signal.

Run it locally before you push:
    python .github/check_deliverables.py

To look at one specific week — say, to confirm Week 2 still passes:
    AIASD_WEEK=2 python .github/check_deliverables.py
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
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

# When a deliverable is due. Work that belongs in the lab, where you can still
# ask, is SESSION; work that is genuinely done alone afterwards — writing,
# diagrams, reflection — is DEADLINE.
#
# This is not cosmetic. Half the week's mark is taken at the end of the session,
# so checking for a diagram you were told to draw at home would mark everyone
# down for following the instructions.
SESSION, DEADLINE = "session", "deadline"

results: list[tuple[str, str, str, str]] = []


def check(
    week: int, name: str, ok: bool, detail: str = "", slot: str = SESSION
) -> None:
    results.append((f"W{week}", name, PASS if ok else f"{FAIL} — {detail}", slot))


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


def ai_log_evidence(week: int) -> str:
    """The pasted exchange backing this week's claim — a fenced block with content.

    An untouched template block holds only an HTML comment, which is stripped here,
    so the placeholder does not count as evidence.
    """
    text = read("ai_log.md") or ""
    match = re.search(
        rf"^##\s*Week\s*{week}\b(.*?)(?=^##\s*Week\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""
    blocks = re.findall(r"```[^\n]*\n(.*?)```", match.group(1), re.DOTALL)
    cleaned = [re.sub(r"<!--.*?-->", "", b, flags=re.DOTALL).strip() for b in blocks]
    return "\n".join(c for c in cleaned if c).strip()


def check_ai_log(week: int) -> None:
    """Every week: a filled-in reflection, and the exchange that backs it up.

    Due at the deadline, not at the end of the session: the honest version of
    this is written once the week's work has actually happened.
    """
    check(
        week,
        f"ai_log.md Week {week} filled in",
        len(ai_log_section(week)) > 80,
        "section empty or untouched",
        DEADLINE,
    )
    evidence = ai_log_evidence(week)
    check(
        week,
        f"ai_log.md Week {week} evidence pasted",
        len(evidence) >= 80,
        f"{len(evidence)} characters in the code block — paste the real exchange",
        DEADLINE,
    )


def ai_log_section(week: int) -> str:
    """Return the body of the Week N section of ai_log.md."""
    text = read("ai_log.md") or ""
    pattern = rf"^##\s*Week\s*{week}\b(.*?)(?=^##\s*Week\s|\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    body = re.sub(r"<!--.*?-->", "", match.group(1), flags=re.DOTALL)
    # Drop the template's own bold prompt labels — an untouched section is empty.
    body = re.sub(r"^\s*\*\*.*?:\*\*\s*$", "", body, flags=re.MULTILINE)
    return body.strip()


# ── per-week checks ──────────────────────────────────────────────────


def check_identity() -> None:
    """student.json — who you are. Nickname goes on the class board; the rest is
    for the official record and never leaves the instructor's machine."""
    raw = read("student.json")
    if raw is None:
        check(1, "student.json present", False, "file missing from repo root")
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        check(1, "student.json is valid JSON", False, str(exc))
        return

    fields = ("student_id", "first_name", "last_name", "nickname", "section")
    missing = [f for f in fields if not str(data.get(f, "")).strip()]
    check(
        1, "student.json fully filled in", not missing, f"empty: {', '.join(missing)}"
    )
    if missing:
        return

    sid = str(data["student_id"]).strip()
    check(
        1,
        "student_id looks like a number",
        sid.isdigit() and len(sid) >= 5,
        f"got {sid!r}",
    )

    nick = str(data["nickname"]).strip()
    check(
        1,
        "nickname is 2-20 characters",
        2 <= len(nick) <= 20,
        f"{len(nick)} characters",
    )
    check(
        1,
        "nickname has no spaces or odd characters",
        bool(re.fullmatch(r"[A-Za-z0-9_\-]+", nick)),
        "use letters, digits, - and _ only",
    )

    check(
        1,
        "nickname is not the student id",
        nick != sid,
        "the board would not be anonymous",
    )

    section = str(data.get("section", "")).strip().lower()
    check(
        1,
        "section is 'en' or 'tr'",
        section in ("en", "tr"),
        f"got {section!r} — this is how your repo knows which week to check",
    )


def week1() -> None:
    check_identity()
    proof = read("week01/setup_proof.md")
    check(
        1,
        "week01/setup_proof.md present",
        bool(proof and len(proof) > 80),
        "missing or too short",
    )

    src = read("week01/hello.py")
    check(
        1,
        "week01/hello.py parses",
        parses("week01/hello.py"),
        "missing or has a syntax error",
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
                isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == "input"
                for n in nodes
            )
            check(1, "hello.py uses an f-string", has_fstring, "no f-string found")
            check(1, "hello.py uses a list", has_list, "no list literal found")
            check(1, "hello.py uses a for-loop", has_for, "no for-loop found")
            check(1, "hello.py reads input()", has_input, "input() is never called")

    notes = read("week01/llm_notes.md") or ""
    check(
        1,
        "week01/llm_notes.md ~300 words",
        len(notes.split()) >= 250,
        f"{len(notes.split())} words",
        DEADLINE,
    )

    gi = read(".gitignore") or ""
    check(
        1,
        ".gitignore covers .venv and .env",
        ".venv" in gi and ".env" in gi,
        "add them",
    )
    check(
        1,
        ".env.example present",
        (ROOT / ".env.example").is_file(),
        "create it (names only)",
    )
    check_ai_log(1)


def week2() -> None:
    prd = read("week02/PRD.md") or ""
    for heading in (
        "Problem Statement",
        "Target Audience",
        "Core Features",
        "Out of Scope",
    ):
        check(
            2,
            f"PRD.md has '{heading}'",
            heading.lower() in prd.lower(),
            "heading missing",
        )

    srs = read("week02/SRS.md") or ""
    check(2, "week02/SRS.md filled in", len(srs) > 400, "missing or too short")

    raw = read("week02/requirements.json")
    if raw is None:
        check(2, "requirements.json present", False, "file missing")
    else:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            check(2, "requirements.json is valid JSON", False, str(exc))
        else:
            items = (
                data.get("functional_requirements", data)
                if isinstance(data, dict)
                else data
            )
            if isinstance(data, dict):
                items = (data.get("functional_requirements") or []) + (
                    data.get("non_functional_requirements") or []
                )
            check(
                2,
                "requirements.json has ≥5 entries",
                len(items) >= 5,
                f"{len(items)} found",
            )
            ids = [i.get("id", "") for i in items if isinstance(i, dict)]
            bad = [i for i in ids if not re.fullmatch(r"REQ-\d{3}", i)]
            check(2, "IDs follow REQ-NNN", not bad and bool(ids), f"bad IDs: {bad[:3]}")
            missing = [
                i for i in items if isinstance(i, dict) and "description" not in i
            ]
            check(
                2,
                "every entry has a description",
                not missing,
                f"{len(missing)} without one",
            )

    uc = read("week02/use_cases/use_case_diagram.mmd") or ""
    check(
        2,
        "use case diagram is Mermaid",
        any(k in uc for k in ("graph", "flowchart")),
        "no graph/flowchart",
    )
    check_ai_log(2)


def week3() -> None:
    for mod in ("llm_client", "embedder", "chatbot"):
        check(
            3,
            f"week03/{mod}.py parses",
            parses(f"week03/{mod}.py"),
            "missing or syntax error",
        )

    emb = read("week03/embedder.py") or ""
    if emb:
        try:
            names = {
                n.name
                for n in ast.walk(ast.parse(emb))
                if isinstance(n, ast.FunctionDef)
            }
        except SyntaxError:
            names = set()
        check(3, "embedder defines encode()", "encode" in names, "function not found")
        check(
            3,
            "embedder defines cosine_similarity()",
            "cosine_similarity" in names,
            "not found",
        )

    bot = read("week03/chatbot.py") or ""
    check(3, "chatbot imports streamlit", "streamlit" in bot, "not imported")
    check(
        3,
        "chatbot keeps history in session_state",
        "session_state" in bot,
        "history not persisted",
    )

    prompts = read("week03/prompts.md") or ""
    n = len(re.findall(r"^##\s+\S", prompts, re.MULTILINE))
    check(3, "prompts.md has ≥5 prompts", n >= 5, f"{n} sections found")

    notes = read("week03/model_notes.md") or ""
    check(
        3,
        "model_notes.md ≥400 chars",
        len(notes.strip()) >= 400,
        f"{len(notes.strip())} chars",
        DEADLINE,
    )
    check(
        3,
        "model_notes.md shows the raw HTTP call",
        "11434" in notes or "api/generate" in notes,
        "paste the curl command and what came back",
        DEADLINE,
    )
    check_ai_log(3)


def week4() -> None:
    """Prototype and peer round in the lab; diagrams and write-up afterwards.

    The clickable prototype comes before the diagrams on purpose. It is the
    cheapest place to find out the flow is wrong — cheaper than discovering it
    after the architecture is drawn, when the temptation is to bend the
    prototype to fit the picture rather than the other way round.
    """
    check(4, "week04/app.py parses", parses("week04/app.py"), "missing or syntax error")
    app = read("week04/app.py") or ""
    check(4, "app.py imports streamlit", "streamlit" in app, "not imported")
    check(
        4,
        "app.py has more than one page or view",
        len(re.findall(r"st\.(tabs|sidebar|page_link|radio|selectbox)", app)) >= 1,
        "a prototype people can click needs somewhere to click to",
    )

    feedback = read("week04/feedback.md") or ""
    check(
        4,
        "week04/feedback.md present",
        len(feedback.strip()) >= 200,
        "what three people told you when they clicked your prototype",
    )
    check(
        4,
        "feedback.md records what you changed",
        bool(re.search(r"chang|fix|mov|renam|remov|add", feedback, re.IGNORECASE)),
        "say what you changed, and what you deliberately did not",
        DEADLINE,
    )

    seq = read("week04/sequence/sequence_diagram.mmd") or ""
    check(
        4,
        "sequence diagram is Mermaid",
        "sequenceDiagram" in seq,
        "no sequenceDiagram keyword",
        DEADLINE,
    )

    arch = read("week04/architecture/architecture_diagram.mmd") or ""
    check(
        4,
        "architecture diagram is Mermaid",
        any(k in arch for k in ("graph", "flowchart")),
        "no graph/flowchart",
        DEADLINE,
    )

    design = read("week04/design.md") or ""
    check(
        4,
        "week04/design.md ≥300 chars",
        len(design.strip()) >= 300,
        f"{len(design.strip())} chars",
        DEADLINE,
    )
    check_ai_log(4)


CHECKS = {1: week1, 2: week2, 3: week3, 4: week4}


# ── secrets: this one runs for every week ────────────────────────────

SECRET_PATTERNS = [
    (r"sk-ant-[A-Za-z0-9\-_]{10,}", "Anthropic API key"),
    (r"AIza[0-9A-Za-z\-_]{30,}", "Google API key"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI-style API key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub token"),
]


def check_secrets() -> bool:
    """Scan tracked text files for anything that looks like a live key."""
    clean = True
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "/.venv" in str(path):
            continue
        if path.suffix.lower() not in {
            ".py",
            ".md",
            ".txt",
            ".json",
            ".toml",
            ".yml",
            ".yaml",
            ".mmd",
            "",
        }:
            continue
        if path.name in {"check_deliverables.py", ".env.example"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, text):
                rel = path.relative_to(ROOT)
                print(f"  SECRET  {rel} — looks like a {label}")
                clean = False
    return clean


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

    tmp = Path(tempfile.gettempdir()) / "aiasd_check_deliverables.py"
    try:
        tmp.write_text(published, encoding="utf-8")
    except OSError:
        return

    print("  (using the current checker published by the course)\n")
    env = {
        **os.environ,
        "AIASD_NO_SELFUPDATE": "1",
        "AIASD_ROOT": str(ROOT),
    }
    raise SystemExit(
        subprocess.run(
            [sys.executable, str(tmp), *sys.argv[1:]], env=env, check=False
        ).returncode
    )


COURSE_WEEK_URL = (
    "https://raw.githubusercontent.com/vedatcoskun-course/aiasd-template"
    "/main/CURRENT_WEEK"
)


def cached_week() -> int:
    raw = (read("WEEK") or "0").strip().splitlines()
    try:
        return int(raw[0]) if raw and raw[0].strip() else 0
    except ValueError:
        return 0


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
                (ROOT / "WEEK").write_text(f"{published}\n", encoding="utf-8")
            except OSError:
                pass  # read-only checkout; the number is still correct
        return published, "published by the course"
    return cached_week(), "cached — the course could not be reached"


def main() -> int:
    maybe_update()
    current, source = resolve_week()

    print("=" * 64)
    print("  Secret scan")
    print("=" * 64)
    secrets_ok = check_secrets()
    if secrets_ok:
        print("  no API keys found\n")
    else:
        print("  KEYS FOUND — remove them and rotate them NOW")
        print("  This is an automatic 10-point deduction. Remove the key, rotate it")
        print("  at the provider, and never commit one again.\n")

    if current < 1:
        if source.startswith("cached"):
            print("Cannot tell which week it is.")
            print(
                "The course could not be reached and there is no cached week number\n"
                "yet — this is the first run on this machine, offline. Connect once\n"
                "and run it again; after that it works without a network."
            )
        else:
            print(f"Week 0 ({source}) — nothing to check yet.")
            print(
                "The course has not started checking deliverables. "
                "Nothing for you to do."
            )
        return 0 if secrets_ok else 1

    print(f"Checking weeks 1-{current}  ({source})\n")

    for week in range(1, current + 1):
        if week in CHECKS:
            CHECKS[week]()

    # Which slots this run is scored on. The instructor's end-of-session capture
    # passes AIASD_SLOT=session and is therefore blind to work that was never
    # due yet; the Saturday capture passes deadline and sees everything.
    scored = os.environ.get("AIASD_SLOT", "").strip().lower()
    if scored == SESSION:
        slots = [SESSION]
    elif scored == DEADLINE:
        slots = [SESSION, DEADLINE]
    else:
        slots = None  # a student's own run: show both, score the session

    def show(rows: list[tuple[str, str, str, str]], heading: str) -> None:
        if not rows:
            return
        width = max(len(name) for _, name, _, _ in rows)
        print("=" * 64)
        print(f"  {heading}")
        print("=" * 64)
        seen = None
        for wk, name, status, _ in rows:
            if wk != seen:
                print(f"  -- Week {wk[1:]} " + "-" * (58 - len(wk)))
                seen = wk
            mark = "✓" if status == PASS else "✗"
            print(f"  {mark}  {name.ljust(width)}   {status}")
        print()

    session_rows = [r for r in results if r[3] == SESSION]
    deadline_rows = [r for r in results if r[3] == DEADLINE]

    if slots is not None:
        rows = [r for r in results if r[3] in slots]
        show(rows, f"Weeks 1-{current}")
        failed = [r for r in rows if r[2] != PASS]
        print("-" * 64)
        print(
            f"  {len(rows) - len(failed)} passed, {len(failed)} failed  "
            f"(weeks 1-{current}, {scored})"
        )
        print("-" * 64)
        return 0 if (not failed and secrets_ok) else 1

    show(session_rows, "Due at the end of the session")
    show(deadline_rows, "Due by Saturday 23:59")

    s_bad = [r for r in session_rows if r[2] != PASS]
    d_bad = [r for r in deadline_rows if r[2] != PASS]
    print("-" * 64)
    print(
        f"  In the lab:     {len(session_rows) - len(s_bad)} of {len(session_rows)} done"
    )
    print(
        f"  By Saturday:    {len(deadline_rows) - len(d_bad)} of {len(deadline_rows)} done"
    )
    print(f"  (weeks 1-{current}, {source})")
    print("-" * 64)
    if d_bad and not s_bad:
        print(
            f"\n  {len(d_bad)} still to do before Saturday 23:59. Those do not fail "
            "this run —\n  they are not due yet. The lab items are what the "
            "end-of-session mark reads."
        )
    return 0 if (not s_bad and secrets_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
