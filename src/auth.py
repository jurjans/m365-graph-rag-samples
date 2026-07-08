"""App-only Microsoft Graph auth (client credentials).

Illustrative sample — acquires an application token for Microsoft Graph using
MSAL, without a signed-in user. This is the auth model a background AI agent
uses to read tenant content it has been granted access to.

Requires an Entra ID app registration with application permissions
(e.g. Sites.Read.All, Files.Read.All) and admin consent.
"""
from __future__ import annotations

import os

import msal

GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
AUTHORITY = "https://login.microsoftonline.com/{tenant_id}"


def get_graph_token(
    tenant_id: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
) -> str:
    """Return an application access token for Microsoft Graph.

    Falls back to TENANT_ID / CLIENT_ID / CLIENT_SECRET environment variables.
    Prefer a certificate or Managed Identity in production over a client secret.
    """
    tenant_id = tenant_id or os.environ["TENANT_ID"]
    client_id = client_id or os.environ["CLIENT_ID"]
    client_secret = client_secret or os.environ["CLIENT_SECRET"]

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=AUTHORITY.format(tenant_id=tenant_id),
        client_credential=client_secret,
    )

    # MSAL caches tokens in-memory and reuses them until they near expiry.
    result = app.acquire_token_for_client(scopes=GRAPH_SCOPE)

    if "access_token" not in result:
        raise RuntimeError(
            f"Token request failed: {result.get('error')} - "
            f"{result.get('error_description')}"
        )
    return result["access_token"]


if __name__ == "__main__":
    token = get_graph_token()
    print(f"Acquired Graph token ({len(token)} chars).")
