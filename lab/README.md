# Lab Environment

Personal AI security lab. Everything runs locally; all testing targets only these systems.

## Architecture

```
Mac host (M1, 8 GB)
├── Ollama (native, Metal GPU, 127.0.0.1:11434)
│   ├── gemma3:1b         chat model (default)
│   ├── qwen3:1.7b        chat + tool calling (agent labs, wk 9+)
│   └── nomic-embed-text  embeddings
└── Docker Compose (lab/)
    ├── app     FastAPI RAG app   127.0.0.1:8000
    └── chroma  vector DB 0.6.3   127.0.0.1:8001
```

Ollama runs on the host rather than in Docker because Docker on macOS can't use the Metal GPU.

## Run

```bash
brew services start ollama          # if not running
cd lab && docker compose up -d --build
curl localhost:8000/health          # {"app":"ok","chroma":"ok","ollama":"ok"}
```

Try it:

```bash
curl -X POST localhost:8000/ingest -H 'content-type: application/json' \
  -d '{"id":"policy-1","text":"Employees get 20 vacation days per year."}'
curl -X POST localhost:8000/ask -H 'content-type: application/json' \
  -d '{"question":"How many vacation days do employees get?"}'
```

Stop: `docker compose down` (add `-v` to wipe the vector DB).

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Checks app, Chroma, Ollama |
| POST | `/ingest` | `{id, text}` → embed + store |
| POST | `/ask` | `{question}` → retrieve top 3 → answer |

## Security baseline (already applied)

| Control | Where |
|---|---|
| Ports bound to `127.0.0.1` only | compose `ports` |
| Non-root user (uid 10001) | Dockerfile |
| Read-only root filesystem + tmpfs `/tmp` | compose `read_only` |
| All Linux capabilities dropped | compose `cap_drop: ALL` |
| `no-new-privileges` | compose `security_opt` |
| Pinned image + dependency versions | compose, requirements.txt |
| Input length limits | pydantic models in `main.py` |

## Known weaknesses (intentional — fixed in P2, weeks 7–8)

- No authentication or per-user retrieval ACLs
- Retrieved documents are trusted and concatenated straight into the prompt (indirect prompt injection)
- No logging / audit trail
- Model output returned unfiltered
