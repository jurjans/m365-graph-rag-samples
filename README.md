# m365-graph-rag-samples

Small, runnable patterns for grounding an LLM answer in **Microsoft 365** data — the unglamorous plumbing behind a private AI agent on SharePoint and Microsoft Graph.

These are the building blocks of [**Answergrove**](https://ksj.lv/answergrove-copilot-alternativa/), our private, own-your-deployment Copilot alternative — extracted here as **illustrative** samples so you can see that "private AI on M365" is real engineering, not a wrapper demo.

> ⚠️ **Illustrative only.** These snippets use synthetic/demo data and are meant to show the shape of each pattern. They are not a production system and contain no client data.

## What's inside

| Pattern | File | What it shows |
|---|---|---|
| App-only Graph auth | [`src/auth.py`](src/auth.py) | Acquire a Microsoft Graph token with MSAL client credentials (no user in the loop) |
| SharePoint search | [`src/graph_search.py`](src/graph_search.py) | Query the Graph Search API for relevant documents in a tenant |
| Chunking | [`src/chunk.py`](src/chunk.py) | Turn a SharePoint page / document into overlapping, retrieval-friendly chunks |
| Grounded answer (RAG) | [`src/rag.py`](src/rag.py) | Retrieve context and ask an LLM to answer **only** from it, with source citations |

## Prerequisites

- A Microsoft 365 tenant and an **Entra ID app registration** with application permissions (`Sites.Read.All`, `Files.Read.All`) granted admin consent.
- Python 3.10+.
- An LLM endpoint — Anthropic Claude or Azure OpenAI (the RAG sample is written to swap either in).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your tenant / client / secret
```

## Why this matters

A "private Copilot alternative" is only credible if the retrieval is real: your documents stay in your tenant, answers cite their source, and permissions are respected. These patterns are the foundation of [**Answergrove**](https://ksj.lv/answergrove-copilot-alternativa/) — a private AI agent deployment for Microsoft 365.

## About

Built by [**SIA KSJ**](https://ksj.lv/) — a Microsoft 365 consultancy (EU). Maintained by [Kaspars Jurjāns](https://www.linkedin.com/in/kasparsjurjans1969/) (PL-600, PL-200, AZ-104).

MIT licensed — see [LICENSE](LICENSE).
