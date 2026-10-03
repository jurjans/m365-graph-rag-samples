# m365-graph-rag-samples

Small, runnable patterns for grounding an LLM answer in **Microsoft 365** data: the unglamorous plumbing behind a private AI assistant on SharePoint and Microsoft Graph.

They show, in simplified form, the kind of plumbing behind [**Answergrove**](https://ksj.lv/en/answergrove/), our private AI assistant that answers your team's questions from your own SharePoint documents and lists, with the document, page and version it came from. Answergrove is [available on Microsoft Marketplace](https://marketplace.microsoft.com/en-us/product/saas/siaksj.answergrove). The samples are **illustrative**, so you can see that "private AI on M365" is real engineering, not a wrapper demo.

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
- An LLM endpoint: the sample calls Anthropic Claude, and an Azure OpenAI variant is noted in [`src/rag.py`](src/rag.py).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your tenant / client / secret
```

## Why this matters

A private AI assistant on SharePoint is only credible if the retrieval is real: answers cite their source, and permissions are respected. In Answergrove, SharePoint permissions are checked before anything is shown, and the language models are Azure OpenAI in the EU Data Zone. It works alongside Microsoft 365 Copilot in the same tenant.

## About

Answergrove is built and delivered by [**SIA KSJ**](https://ksj.lv/), Latvia (EU), a member of the Microsoft AI Cloud Partner Program. Maintained by [Kaspars Jurjāns](https://www.linkedin.com/in/kasparsjurjans1969/) (PL-600, PL-200, AZ-104). Contact: kaspars@jurjans.dev

The samples in this repository are MIT licensed: see [LICENSE](LICENSE).
