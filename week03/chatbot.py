"""
week03/chatbot.py — a working chat interface.

Run with:
    streamlit run week03/chatbot.py

The one thing to internalise here: the model has no memory. Every turn, your
code re-sends the entire conversation. If you do not send it, it did not happen.
"""

import streamlit as st
from llm_client import LLMClient

st.set_page_config(page_title="AIASD Chatbot", page_icon="💬")
st.title("💬 Chatbot")

# ── Sidebar: backend selection ────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    backend = st.radio("Backend", ["ollama", "cloud"], help="Local model or cloud API")
    system_prompt = st.text_area(
        "System prompt",
        value="Sen yardımcı bir asistansın. Kısa ve net cevap ver.",
        height=120,
    )
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# ── Conversation state ────────────────────────────────────────────────
# TODO: initialise st.session_state.messages to [] the first time this runs.

# ── Render the history ────────────────────────────────────────────────
# TODO: loop over st.session_state.messages and display each one with
# st.chat_message(role) / st.markdown(content).

# ── The client ────────────────────────────────────────────────────────
# Rebuilt on every rerun, which is fine — it holds no state of its own.
# All the state lives in st.session_state.
client = LLMClient(backend=backend)

# ── Handle new input ──────────────────────────────────────────────────
if prompt := st.chat_input("Mesajınızı yazın..."):
    # TODO:
    # 1. append {"role": "user", "content": prompt} to the history
    # 2. display it
    # 3. reply = client.chat(st.session_state.messages, system_prompt)
    #    — note: the FULL history goes in, not just this message
    # 4. append {"role": "assistant", "content": reply} and display it
    pass
