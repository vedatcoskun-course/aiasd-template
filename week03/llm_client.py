"""
week03/llm_client.py — one interface, two backends.

The point of this module: the rest of your application should not know or care
whether the model is running on your laptop or in somebody's data centre.
Swapping backends must be a constructor argument, never a rewrite.

Fill in the TODOs. Keep the public signature exactly as given.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Talks to a local Ollama model or a cloud API behind one interface."""

    def __init__(self, backend: str = "ollama", model: str | None = None) -> None:
        if backend not in ("ollama", "cloud"):
            raise ValueError(f"backend must be 'ollama' or 'cloud', got {backend!r}")
        self.backend = backend
        # Pick a sensible default per backend; let the caller override.
        self.model = model or ("qwen2.5:3b" if backend == "ollama" else "claude-sonnet-4-5")

    def chat(self, messages: list[dict], system_prompt: str = "") -> str:
        """
        Send a conversation and return the model's reply as plain text.

        messages: [{"role": "user"|"assistant", "content": "..."}, ...]
                  The FULL history — the model has no memory of its own.
        """
        if self.backend == "ollama":
            return self._chat_ollama(messages, system_prompt)
        return self._chat_cloud(messages, system_prompt)

    # ── backends ──────────────────────────────────────────────────────

    def _chat_ollama(self, messages: list[dict], system_prompt: str) -> str:
        # TODO: import ollama, prepend the system prompt as a {"role": "system"}
        # message, call ollama.chat(model=self.model, messages=...), and return
        # response["message"]["content"].
        raise NotImplementedError("Implement the Ollama backend")

    def _chat_cloud(self, messages: list[dict], system_prompt: str) -> str:
        # TODO: use Claude or Gemini. Read the key with os.getenv(...) — never
        # hard-code it. For Claude the system prompt is a separate `system=`
        # argument, not a message.
        _ = os.getenv("ANTHROPIC_API_KEY")
        raise NotImplementedError("Implement the cloud backend")


if __name__ == "__main__":
    client = LLMClient(backend="ollama")
    print(client.chat([{"role": "user", "content": "Merhaba, kısaca kendini tanıt."}]))
