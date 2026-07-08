"""Search SharePoint content via the Microsoft Graph Search API.

Illustrative sample — runs a keyword query against driveItem (files) and
returns lightweight hits (name, URL, snippet). In a real agent this is the
retrieval entry point: the user's question becomes the search query, and the
top hits are fetched and chunked before being passed to the model.
"""
from __future__ import annotations

from typing import Any

import requests

GRAPH_SEARCH_URL = "https://graph.microsoft.com/v1.0/search/query"


def search_documents(token: str, query: str, size: int = 10) -> list[dict[str, Any]]:
    """Return up to `size` document hits for `query` from the tenant.

    Permissions are honoured by Graph: an app only sees what its
    app-registration has been granted (and, with delegated auth, what the
    signed-in user can see).
    """
    body = {
        "requests": [
            {
                "entityTypes": ["driveItem"],
                "query": {"queryString": query},
                "from": 0,
                "size": size,
            }
        ]
    }
    resp = requests.post(
        GRAPH_SEARCH_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=30,
    )
    resp.raise_for_status()

    hits: list[dict[str, Any]] = []
    for container in resp.json().get("value", []):
        for group in container.get("hitsContainers", []):
            for hit in group.get("hits", []):
                res = hit.get("resource", {})
                hits.append(
                    {
                        "id": res.get("id"),
                        "name": res.get("name"),
                        "url": res.get("webUrl"),
                        "snippet": hit.get("summary", ""),
                    }
                )
    return hits


if __name__ == "__main__":
    from auth import get_graph_token

    results = search_documents(get_graph_token(), "supplier contract payment terms")
    for r in results:
        print(f"- {r['name']}  ->  {r['url']}")
