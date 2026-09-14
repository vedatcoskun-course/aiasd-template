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
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PASS, FAIL = "PASS", "FAIL"
results: list[tuple[str, str, str]] = []


def check(week: int, name: str, ok: bool, detail: str = "") -> None:
    results.append((f"W{week}", name, PASS if ok else f"{FAIL} — {detail}"))


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
    """Every week: a filled-in reflection, and the exchange that backs it up."""
    check(
        week,
        f"ai_log.md Week {week} filled in",
        len(ai_log_section(week)) > 80,
        "section empty or untouched",
    )
    evidence = ai_log_evidence(week)
    check(
        week,
        f"ai_log.md Week {week} evidence pasted",
        len(evidence) >= 80,
        f"{len(evidence)} characters in the code block — paste the real exchange",
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

    fields = ("student_id", "first_name", "last_name", "nickname")
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
    )
    check_ai_log(3)


def week4() -> None:
    check(4, "week04/app.py parses", parses("week04/app.py"), "missing or syntax error")
    app = read("week04/app.py") or ""
    check(4, "app.py imports streamlit", "streamlit" in app, "not imported")

    seq = read("week04/sequence/sequence_diagram.mmd") or ""
    check(
        4,
        "sequence diagram is Mermaid",
        "sequenceDiagram" in seq,
        "no sequenceDiagram keyword",
    )

    arch = read("week04/architecture/architecture_diagram.mmd") or ""
    check(
        4,
        "architecture diagram is Mermaid",
        any(k in arch for k in ("graph", "flowchart")),
        "no graph/flowchart",
    )

    design = read("week04/design.md") or ""
    check(
        4,
        "week04/design.md ≥300 chars",
        len(design.strip()) >= 300,
        f"{len(design.strip())} chars",
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


def published_week() -> int | None:
    """The week the course says it is on. None if it cannot be reached."""
    try:
        with urllib.request.urlopen(COURSE_WEEK_URL, timeout=5) as response:
            return int(response.read().decode("utf-8").strip().splitlines()[0])
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
    current, source = resolve_week()

    print("=" * 64)
    print("  Secret scan")
    print("=" * 64)
    secrets_ok = check_secrets()
    print(
        "  no API keys found\n"
        if secrets_ok
        else "  KEYS FOUND — remove them and rotate them NOW\n"
    )

    if current < 1:
        print(f"Week 0 ({source}) — nothing to check yet.")
        print(
            "The course has not started checking deliverables. Nothing for you to do."
        )
        return 0 if secrets_ok else 1

    print(f"Checking weeks 1-{current}  ({source})\n")

    for week in range(1, current + 1):
        if week in CHECKS:
            CHECKS[week]()

    width = max(len(name) for _, name, _ in results) if results else 0
    current_week = None
    for wk, name, status in results:
        if wk != current_week:
            print("=" * 64)
            print(f"  Week {wk[1:]}")
            print("=" * 64)
            current_week = wk
        mark = "✓" if status == PASS else "✗"
        print(f"  {mark}  {name.ljust(width)}   {status}")

    failed = [r for r in results if r[2] != PASS]
    print("\n" + "-" * 64)
    print(
        f"  {len(results) - len(failed)} passed, {len(failed)} failed  "
        f"(weeks 1-{current}, {source})"
    )
    print("-" * 64)

    if not secrets_ok:
        print("\nA secret was found in the repository. This is an automatic 10-point")
        print("deduction. Remove it, rotate the key, and never commit it again.")

    return 0 if (not failed and secrets_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
