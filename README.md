# AIASD Project — Student Repository

**AI-Assisted Software Development · Atlas University · Fall 2026–2027**
**Prof. Dr. Vedat Coşkun**

---

## How to use this repository

This is your personal project repository for the entire 12-week course.
You create it from the template on Week 1 and commit to it every week.

| Week | Deliverables |
|------|-------------|
| 1 | `week01/setup_proof.md`, `week01/hello.py`, `week01/llm_notes.md` |
| 2 | `week02/PRD.md`, `week02/SRS.md`, `week02/requirements.json`, use case diagram |
| 3 | Local models + chatbot: `llm_client.py`, `embedder.py`, `chatbot.py`, `model_notes.md`, `prompts.md` |
| 4 | `design.md`, sequence diagram, architecture diagram, Streamlit skeleton |
| 5 | Working prototype (core feature) |
| 6 | Data flow diagram, RAG pipeline |
| 7 | UI completion + full integration |
| 8 | Activity diagram, debugging + refactoring |
| 9 | Tests + `ruff` clean + Ragas evaluation |
| 10 | Selenium UI tests + GitHub Actions CI |
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

Dependencies arrive week by week so you are not downloading gigabytes in Week 1.
The root `requirements.txt` is the minimum; heavier weeks have their own file:

```bash
pip install -r requirements/week03.txt   # Ollama, APIs, embeddings
pip install -r requirements/week06.txt   # + FAISS
pip install -r requirements/week09.txt   # + pytest, ruff, ragas
pip install -r requirements/week10.txt   # + Selenium
```

---

## Repository rules

- Commit **at minimum once per week**, before the session.
- `ai_log.md` must be updated every week — this is graded.
- Do **not** commit `.venv/`, `__pycache__/`, or API keys.
- Run `ruff check .` before committing — it is part of the Week 9 grade and catches the unused imports AI tends to leave behind.
- Use `.env` for secrets and keep it in `.gitignore`.
