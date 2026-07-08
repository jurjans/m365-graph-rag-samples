"""Grounded answer: retrieve context, then answer only from it, with citations.

Illustrative sample — ties the other patterns together. It builds a prompt from
retrieved chunks, instructs the model to answer strictly from the provided
context (and to say when the answer isn't there), and asks for source markers.
This "answer only from context" discipline is what separates a grounded agent
from a chatbot that confidently makes things up.

The call is written against Anthropic Claude; an Azure OpenAI variant is noted
inline.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import anthropic

MODEL = "claude-sonnet-4-5"

SYSTEM = (
    "You are a knowledge assistant for a company's Microsoft 365 documents. "
    "Answer ONLY from the provided sources. If the answer is not in them, say "
    "you don't have that information. Cite the source number in square brackets, "
    "e.g. [2], for every claim."
)


@dataclass
class Source:
    number: int
    title: str
    text: str


def build_context(sources: list[Source]) -> str:
    return "\n\n".join(f"[{s.number}] {s.title}\n{s.text}" for s in sources)


def answer(question: str, sources: list[Source]) -> str:
    """Return a grounded, cited answer to `question` given `sources`."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Sources:\n{build_context(sources)}\n\n"
                    f"Question: {question}"
                ),
            }
        ],
    )
    # Azure OpenAI variant: swap the client for `openai.AzureOpenAI(...)` and use
    # client.chat.completions.create(model=<deployment>, messages=[{system},{user}]).
    return msg.content[0].text


if __name__ == "__main__":
    sources = [
        Source(1, "Piegades_ligums_v3_FINAL.pdf",
               "Payment terms are Net 30 from the invoice date, with a 2% "
               "discount for payment within 10 days (section 4.1)."),
        Source(2, "Onboarding_policy.docx",
               "New suppliers are approved by the finance lead within 5 days."),
    ]
    print(answer("What are the payment terms for the supplier contract?", sources))
