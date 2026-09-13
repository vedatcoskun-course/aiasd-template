# AIASD Project — Student Repository

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**
**Prof. Dr. Vedat Coşkun**

---

## How to use this repository

This is your personal project repository for the entire 12-week course.
You will fork it on Week 1 and commit to it every week.

| Week | Deliverables |
|------|-------------|
| 1 | `week01/llm_notes.md`, `week01/hello.py` |
| 2 | `week02/PRD.md`, `week02/SRS.md`, `week02/requirements.json`, use case diagram |
| 3 | Sequence diagram, basic app scaffold |
| 4 | Architecture diagram, module skeleton |
| 5 | Working prototype (core feature) |
| 6 | Data flow diagram, RAG pipeline |
| 7 | Unit + integration tests |
| 8 | Activity diagram, refactored code |
| 9 | Code quality pass, linting, docstrings |
| 10 | Polished Streamlit UI |
| 11 | Deployment diagram, Dockerfile or deploy config |
| 12 | Final app + demo video + peer review |

Each week you also update `ai_log.md` with a reflection on how you used AI.

---

## Running the app

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Repository rules

- Commit **at minimum once per week**, before the session.
- `ai_log.md` must be updated every week — this is graded.
- Do **not** commit `.venv/`, `__pycache__/`, or API keys.
- Use `.env` for secrets and keep it in `.gitignore`.
