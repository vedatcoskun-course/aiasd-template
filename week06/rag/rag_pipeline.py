"""
week06/rag/rag_pipeline.py
Starter RAG pipeline skeleton — fill in the TODOs.
"""

from pathlib import Path

# Week 6 dependencies:  pip install -r requirements/week06.txt
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer


def load_documents(folder: str) -> list[str]:
    """Load all .txt files from a folder and return their contents."""
    docs = []
    for path in Path(folder).glob("*.txt"):
        docs.append(path.read_text(encoding="utf-8"))
    return docs


def chunk_documents(docs: list[str], chunk_size: int = 500) -> list[str]:
    """Split documents into fixed-size chunks (naive approach)."""
    chunks = []
    for doc in docs:
        for i in range(0, len(doc), chunk_size):
            chunks.append(doc[i : i + chunk_size])
    return chunks


def build_index(chunks: list[str]):
    """Embed chunks and build a FAISS index. Returns (index, model, chunks)."""
    # TODO: uncomment and implement
    # model = SentenceTransformer("BAAI/bge-m3")
    # embeddings = model.encode(chunks, normalize_embeddings=True)
    # dim = embeddings.shape[1]
    # index = faiss.IndexFlatIP(dim)
    # index.add(embeddings)
    # return index, model, chunks
    raise NotImplementedError("Implement build_index in Week 6")


def retrieve(query: str, index, model, chunks: list[str], top_k: int = 3) -> list[str]:
    """Retrieve the top-k most relevant chunks for a query."""
    # TODO: uncomment and implement
    # q_emb = model.encode([query], normalize_embeddings=True)
    # _, ids = index.search(q_emb, top_k)
    # return [chunks[i] for i in ids[0]]
    raise NotImplementedError("Implement retrieve in Week 6")


def generate_answer(query: str, context_chunks: list[str], llm_client) -> str:
    """Build a prompt from retrieved chunks and call the LLM."""
    context = "\n\n---\n\n".join(context_chunks)
    prompt = (
        f"Answer the following question using ONLY the provided context.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )
    # TODO: replace with your LLM client call
    # response = llm_client.messages.create(...)
    return prompt  # placeholder
