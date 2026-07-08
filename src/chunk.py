"""Chunk a document into overlapping, retrieval-friendly pieces.

Illustrative sample — strips HTML (a SharePoint page is HTML) and splits the
text into word-bounded chunks with overlap, so a relevant passage is never cut
in half between two chunks. Chunk size and overlap are the two knobs you tune
per document type (contracts chunk differently from wiki pages).
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    index: int


def strip_html(html: str) -> str:
    """Very small HTML -> text reducer (production code should use a parser)."""
    text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[Chunk]:
    """Split `text` into ~`chunk_size`-word chunks overlapping by `overlap` words."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks: list[Chunk] = []
    step = chunk_size - overlap
    for i, start in enumerate(range(0, len(words), step)):
        piece = words[start : start + chunk_size]
        if not piece:
            break
        chunks.append(Chunk(text=" ".join(piece), index=i))
        if start + chunk_size >= len(words):
            break
    return chunks


if __name__ == "__main__":
    sample_html = "<h1>Supplier contract</h1><p>Payment terms are Net 30 " * 200
    chunks = chunk_text(strip_html(sample_html))
    print(f"Produced {len(chunks)} chunks from the document.")
