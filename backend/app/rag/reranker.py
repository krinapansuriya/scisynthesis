"""
RERANKER MODULE
===============
Hybrid reranking that combines:
  - FAISS semantic scores (from the vector store, L2 distance → 0-1)
  - BM25 lexical scores   (rank_bm25, keyword overlap)

Pipeline:
  FAISS retrieves top-N candidates  →  reranker scores each with BM25
  →  hybrid weighted score  →  return top-k

Weights:  60 % semantic  +  40 % lexical
This gives strong recall for paraphrased queries (semantic) while
still surfacing exact-match keywords (lexical).
"""

from typing import List, Dict, Any

from rank_bm25 import BM25Okapi


# ── Weighting ────────────────────────────────────────────────────────────────
SEMANTIC_WEIGHT = 0.6   # FAISS L2-derived score
LEXICAL_WEIGHT  = 0.4   # BM25 Okapi score


def _tokenize(text: str) -> List[str]:
    """Lowercase whitespace tokenizer — no heavy NLP dependencies needed."""
    return text.lower().split()


def rerank_chunks(
    query: str,
    chunks: List[Dict[str, Any]],
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Rerank a list of retrieved chunks using BM25 + FAISS hybrid scoring.

    Args:
        query:   The user's original query string.
        chunks:  Candidate chunks from FAISS retrieval.  Each dict must have:
                   - "text"            : str
                   - "relevance_score" : float  (0-1, already from FAISS)
                   - any other metadata fields (chunk_id, paper_id, …)
        top_k:   How many chunks to return after reranking.

    Returns:
        Top-k chunks sorted by hybrid score (descending).
        Each chunk gets its "relevance_score" updated to the hybrid value.
    """
    if not chunks:
        return []

    # Nothing to rerank if already at or below top_k
    if len(chunks) <= top_k:
        return chunks

    # ── Build BM25 corpus ────────────────────────────────────────────────────
    tokenized_corpus = [_tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = _tokenize(query)
    raw_bm25_scores = bm25.get_scores(tokenized_query)   # numpy array

    # Normalize BM25 scores to [0, 1]
    max_score = float(max(raw_bm25_scores)) if max(raw_bm25_scores) > 0 else 1.0
    norm_bm25 = [float(s) / max_score for s in raw_bm25_scores]

    # ── Combine scores ───────────────────────────────────────────────────────
    ranked: List[Dict[str, Any]] = []
    for i, chunk in enumerate(chunks):
        hybrid = (
            SEMANTIC_WEIGHT * chunk["relevance_score"]
            + LEXICAL_WEIGHT  * norm_bm25[i]
        )
        ranked.append({**chunk, "relevance_score": round(hybrid, 4)})

    # Sort by hybrid score (highest first) and return top-k
    ranked.sort(key=lambda x: x["relevance_score"], reverse=True)
    return ranked[:top_k]
