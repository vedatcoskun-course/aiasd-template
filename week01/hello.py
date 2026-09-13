"""
Week 1 — hello.py
Smoke-test your Python environment and make a first API call.

Run with:
    python week01/hello.py
"""

import sys

# ── 1. Python version check ───────────────────────────────────────
print(f"Python {sys.version}")
assert sys.version_info >= (3, 10), "Please use Python 3.10 or newer."
print("✓ Python version OK")

# ── 2. Import check ───────────────────────────────────────────────
try:
    import streamlit
    print(f"✓ streamlit {streamlit.__version__}")
except ImportError:
    print("✗ streamlit not installed — run: pip install -r requirements.txt")

try:
    import anthropic
    print(f"✓ anthropic SDK installed")
except ImportError:
    print("✗ anthropic not installed")

try:
    import ollama
    print(f"✓ ollama SDK installed")
except ImportError:
    print("✗ ollama not installed")

# ── 3. Optional: Ollama local call ───────────────────────────────
# Uncomment after running: ollama pull qwen2.5:3b
#
# import ollama
# response = ollama.chat(
#     model="qwen2.5:3b",
#     messages=[{"role": "user", "content": "Say hello in one sentence."}],
# )
# print("\nOllama response:", response["message"]["content"])

print("\nAll checks done. Edit app.py and run: streamlit run app.py")
