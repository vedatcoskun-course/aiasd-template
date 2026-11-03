"""The login, given by the course (REQ-001): the same for every project.

Course file: do not edit; the checker replaces it.
AIASD · Atlas University · Fall 2026-27 · Week 6

Wire it into your server in three steps:

1. Fill in server/login_contract.json by hand: your three login endpoints exactly as they are in
   week05/api.md (a method, one space, a path) and the names of the fields.
2. In server/main.py:

       from server import course_login

       app.include_router(course_login.router)

3. Delete your own Week 5 routes for those three endpoints (the ones that answer 501).

Your own routes that need a logged-in user ask for one with `current_user`:

       from fastapi import Depends

       from server.course_login import current_user

       @router.post("/courses")
       def create_course(body: NewCourse, user: str = Depends(current_user)) -> dict:
           ...   # user is the e-mail address of whoever is logged in

The rules (the course tests in course_tests/ check every one of them):
- a code has 4 digits, is valid for 10 minutes and works once;
- the same address asking for a new code within 60 seconds gets 429;
- a wrong code, or one older than 10 minutes, gets 401;
- after 3 wrong codes in a row (a new code does not start the count again) the address is locked
  for 15 minutes: every login for it gets 429;
- the right code gives a token; me with "Authorization: Bearer <token>" answers with the address;
  no token, or a wrong one, gets 401;
- something that is not an e-mail address gets 422.

The code is e-mailed with the settings in .env (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
SMTP_FROM; see .env.example). In the lecture and in the tests it is written instead to the file
named by the environment variable AIASD_CODE_FILE:

    AIASD_CODE_FILE=login_code.txt uvicorn server.main:app --reload

Everything is kept in memory: a restart of the server forgets the codes and the tokens.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import smtplib
import tempfile
import time
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

CONTRACT_FILE = Path(__file__).with_name("login_contract.json")
ENDPOINT = re.compile(r"(GET|POST|PUT|PATCH|DELETE) (/\S*)", re.IGNORECASE)
KEYS = ("request_code", "login", "me", "email_field", "code_field", "token_field")
EMAIL = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

CODE_LIFETIME = 10 * 60  # seconds a code is valid
RESEND_WAIT = 60  # seconds before the same address may ask for a new code
MAX_WRONG = 3  # wrong codes before the address is locked
LOCK_TIME = 15 * 60  # seconds the address stays locked
MAX_ADDRESS = 254  # characters an e-mail address may have (RFC 5321)


def read_contract() -> tuple[dict[str, Any], str]:
    """server/login_contract.json, and what is wrong with it ('' when it is filled in)."""
    try:
        data = json.loads(CONTRACT_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}, "server/login_contract.json is missing or is not valid JSON"
    if not isinstance(data, dict):
        return {}, "server/login_contract.json must be one JSON object"
    missing = [
        k for k in KEYS if not isinstance(data.get(k), str) or not data[k].strip() or "[" in data[k]
    ]
    missing += [
        k
        for k in ("request_code", "login", "me")
        if k not in missing and not ENDPOINT.fullmatch(data[k].strip())
    ]
    return data, (
        f"server/login_contract.json is not filled in: {', '.join(missing)}" if missing else ""
    )


CONTRACT, CONTRACT_PROBLEM = read_contract()


@dataclass
class _Pending:
    code: str
    sent_at: float


_pending: dict[str, _Pending] = {}  # e-mail address -> the code waiting to be used
_locked_until: dict[str, float] = {}  # e-mail address -> when its lock ends
_wrong: dict[str, int] = {}  # e-mail address -> wrong codes in a row, across new codes
_tokens: dict[str, str] = {}  # token -> e-mail address


def _field(name: str, default: str) -> str:
    value = str(CONTRACT.get(name) or "").strip()
    return default if not value or "[" in value else value


def _endings() -> list[str]:
    """Optional "email_must_end_with" in the contract: such as ".edu.tr", or a list of endings."""
    value = CONTRACT.get("email_must_end_with") or []
    return [
        str(v).strip().lower()
        for v in ([value] if isinstance(value, str) else value)
        if str(v).strip()
    ]


def _address(body: dict[str, Any]) -> str:
    raw = body.get(_field("email_field", "email"))
    if not isinstance(raw, str):
        raise HTTPException(status_code=422, detail=f"{_field('email_field', 'email')} is missing")
    email = raw.strip().lower()
    if len(email) > MAX_ADDRESS or not EMAIL.fullmatch(email):
        raise HTTPException(status_code=422, detail="Not an e-mail address")
    endings = _endings()
    if endings and not any(email.endswith(e) for e in endings):
        raise HTTPException(status_code=422, detail="This e-mail address is not accepted here")
    return email


def _deliver(email: str, code: str) -> None:
    """Writes the code to AIASD_CODE_FILE when it is set; otherwise e-mails it with the settings in .env."""
    code_file = os.environ.get("AIASD_CODE_FILE")
    if code_file:
        Path(code_file).write_text(code, encoding="utf-8")
        return
    password = os.environ.get("SMTP_PASSWORD")
    if not password:
        raise HTTPException(
            status_code=503, detail="E-mail is not set up: fill in .env (see .env.example)"
        )
    app_name = _field("app_name", "the app")
    message = EmailMessage()
    message["Subject"] = f"Your login code for {app_name}"
    message["From"] = os.environ.get("SMTP_FROM") or os.environ.get("SMTP_USER", "")
    message["To"] = email
    message.set_content(f"Your login code for {app_name} is {code}. It is valid for 10 minutes.")
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    try:
        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=15) as smtp:
            smtp.starttls()
            smtp.login(os.environ.get("SMTP_USER", ""), password)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        raise HTTPException(
            status_code=503, detail=f"The e-mail could not be sent: {error}"
        ) from error


def ask_for_code(body: Annotated[dict[str, Any], Body()]) -> dict:
    """REQ-001: sends a 4-digit code to the e-mail address (or writes it to AIASD_CODE_FILE)."""
    email = _address(body)
    now = time.time()
    if _locked_until.get(email, 0.0) > now:
        raise HTTPException(status_code=429, detail="Too many wrong codes: locked for 15 minutes")
    waiting = _pending.get(email)
    if waiting and now - waiting.sent_at < RESEND_WAIT:
        raise HTTPException(status_code=429, detail="Wait a minute before asking for a new code")
    code = f"{secrets.randbelow(10_000):04d}"
    _deliver(email, code)
    _pending[email] = _Pending(code=code, sent_at=now)
    return {"sent": True}


def log_in(body: Annotated[dict[str, Any], Body()]) -> dict:
    """REQ-001: checks the code and gives a token; three wrong codes lock the address for 15 minutes."""
    email = _address(body)
    raw = body.get(_field("code_field", "code"))
    if raw is None:
        raise HTTPException(status_code=422, detail=f"{_field('code_field', 'code')} is missing")
    now = time.time()
    if _locked_until.get(email, 0.0) > now:
        raise HTTPException(status_code=429, detail="Too many wrong codes: locked for 15 minutes")
    waiting = _pending.get(email)
    if waiting is None or now - waiting.sent_at > CODE_LIFETIME:
        _pending.pop(email, None)
        raise HTTPException(status_code=401, detail="Wrong code, or a code older than 10 minutes")
    if not secrets.compare_digest(str(raw).strip().encode(), waiting.code.encode()):
        _wrong[email] = _wrong.get(email, 0) + 1
        if _wrong[email] >= MAX_WRONG:
            _pending.pop(email, None)
            _wrong.pop(email, None)
            _locked_until[email] = now + LOCK_TIME
        raise HTTPException(status_code=401, detail="Wrong code")
    del _pending[email]  # a code works once
    _wrong.pop(email, None)
    token = secrets.token_urlsafe(24)
    _tokens[token] = email
    return {_field("token_field", "token"): token}


# "Authorization: Bearer <token>". Declared as a security scheme, so /docs shows an Authorize button.
_bearer = HTTPBearer(auto_error=False, description="The token from the login answer")


def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> str:
    """For your own routes: the e-mail address of the token in 'Authorization: Bearer <token>'; 401 without one.
    Use it as `user: str = Depends(current_user)`."""
    email = _tokens.get(credentials.credentials.strip()) if credentials else None
    if email is None:
        raise HTTPException(status_code=401, detail="Not logged in")
    return email


def me(email: Annotated[str, Depends(current_user)]) -> dict:
    """REQ-001: who is logged in, for the clients."""
    return {_field("email_field", "email"): email}


def _build_router() -> APIRouter:
    router = APIRouter(tags=["login (course)"])
    if CONTRACT_PROBLEM:  # nothing to serve yet: the course tests say what to fill in
        return router
    for key, endpoint in (("request_code", ask_for_code), ("login", log_in), ("me", me)):
        method, path = ENDPOINT.fullmatch(CONTRACT[key].strip()).groups()
        router.add_api_route(path, endpoint, methods=[method.upper()])
    return router


router = _build_router()


def reset_for_tests() -> None:
    """For your own tests: forgets every code, lock and token."""
    _pending.clear()
    _locked_until.clear()
    _wrong.clear()
    _tokens.clear()


def auth_header_for_tests(client: Any, email: str) -> dict[str, str]:
    """For your own tests: logs `email` in through a TestClient and returns the header that carries its token:

        headers = auth_header_for_tests(client, "mia@example.edu.tr")
        response = client.post("/courses", json={"name": "Databases 201"}, headers=headers)

    Use a different address in each test (an address may ask for a new code only once a minute)."""
    if CONTRACT_PROBLEM:
        raise AssertionError(CONTRACT_PROBLEM)
    request_method, request_path = ENDPOINT.fullmatch(CONTRACT["request_code"].strip()).groups()
    login_method, login_path = ENDPOINT.fullmatch(CONTRACT["login"].strip()).groups()
    before = os.environ.get("AIASD_CODE_FILE")
    with tempfile.TemporaryDirectory() as folder:
        code_file = Path(folder) / "code.txt"
        os.environ["AIASD_CODE_FILE"] = str(code_file)
        try:
            asked = client.request(
                request_method, request_path, json={_field("email_field", "email"): email}
            )
            if asked.status_code >= 300:
                raise AssertionError(
                    f"asking for a code for {email} answered {asked.status_code}: {asked.text[:200]}"
                )
            code = code_file.read_text(encoding="utf-8").strip()
        finally:
            if before is None:
                os.environ.pop("AIASD_CODE_FILE", None)
            else:
                os.environ["AIASD_CODE_FILE"] = before
    answer = client.request(
        login_method,
        login_path,
        json={_field("email_field", "email"): email, _field("code_field", "code"): code},
    )
    if answer.status_code != 200:
        raise AssertionError(
            f"logging in {email} answered {answer.status_code}: {answer.text[:200]}"
        )
    return {"Authorization": f"Bearer {answer.json()[_field('token_field', 'token')]}"}
