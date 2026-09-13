"""
app.py — Streamlit application entry point
AI-Assisted Software Development · Atlas University · Fall 2026–2027

Replace this scaffold with your own project as the weeks progress.
"""

import streamlit as st

# ── Page configuration ────────────────────────────────────────────
# layout="centered" keeps a single, narrow column — the layout that survives a phone
# screen. layout="wide" looks better on your laptop and breaks on a 390px screen, so
# only reach for it if you have tested what it does when narrow.
st.set_page_config(
    page_title="My AI Project",  # TODO: replace with your project name
    page_icon="🤖",
    layout="centered",
)

# ── Header ────────────────────────────────────────────────────────
st.title("My AI-Assisted Application")
st.caption("AIASD · Atlas University · Fall 2026–2027")

st.info(
    "This is the starter scaffold. Replace this file with your project code "
    "as you progress through the weekly deliverables."
)

# ── Week 1 smoke-test ─────────────────────────────────────────────
st.subheader("Week 1 — Environment check")

user_input = st.text_input("Enter any text to test your setup:")
if user_input:
    st.success(f"✓ Streamlit is working. You typed: **{user_input}**")

st.divider()
st.write("**Next steps:** open `week01/hello.py` and run it from your terminal.")
