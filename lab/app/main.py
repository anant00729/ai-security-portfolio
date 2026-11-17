"""Minimal RAG app — week 1 smoke-test target.

Deliberately plain: no auth, no output encoding, no retrieval ACLs.
It becomes the base for P2 (vulnerable → hardened) in weeks 7-8.
"""

import os

import chromadb
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemma3:1b")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text")
CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8001"))
COLLECTION = "docs"
TOP_K = 3
LLM_TIMEOUT_S = 120

app = FastAPI(title="ai-sec-lab")


def get_collection():
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return client.get_or_create_collection(COLLECTION)


class Doc(BaseModel):
    id: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=20_000)


class Question(BaseModel):
    question: str = Field(min_length=1, max_length=2_000)


async def embed(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=LLM_TIMEOUT_S) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/api/embed", json={"model": EMBED_MODEL, "input": text}
        )
    if resp.status_code != 200:
        raise HTTPException(502, f"Embedding backend error: {resp.status_code}")
    return resp.json()["embeddings"][0]


async def generate(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=LLM_TIMEOUT_S) as client:
        resp = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": CHAT_MODEL, "prompt": prompt, "stream": False},
        )
    if resp.status_code != 200:
        raise HTTPException(502, f"LLM backend error: {resp.status_code}")
    return resp.json().get("response", "")


@app.get("/health")
async def health():
    status = {"app": "ok"}
    try:
        get_collection().count()
        status["chroma"] = "ok"
    except Exception as exc:  # report, don't crash the health check
        status["chroma"] = f"error: {type(exc).__name__}"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{OLLAMA_URL}/api/tags")
        status["ollama"] = "ok" if r.status_code == 200 else f"http {r.status_code}"
    except httpx.HTTPError as exc:
        status["ollama"] = f"error: {type(exc).__name__}"
    return status


@app.post("/ingest")
async def ingest(doc: Doc):
    vector = await embed(doc.text)
    get_collection().upsert(ids=[doc.id], documents=[doc.text], embeddings=[vector])
    return {"ingested": doc.id}


@app.post("/ask")
async def ask(q: Question):
    vector = await embed(q.question)
    hits = get_collection().query(query_embeddings=[vector], n_results=TOP_K)
    context = "\n---\n".join(hits["documents"][0]) if hits["documents"] else ""
    prompt = (
        "Answer the question using only the context.\n\n"
        f"Context:\n{context}\n\nQuestion: {q.question}\nAnswer:"
    )
    return {"answer": await generate(prompt), "sources": hits["ids"][0]}
