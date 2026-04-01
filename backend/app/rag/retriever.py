"""
RETRIEVER MODULE
================
Hybrid retrieval pipeline:

  1. Embed the query with Gemini embedding-001  (768-dim)
  2. FAISS vector search  →  top (top_k × 10) semantic candidates
  3. Filter by paper_ids if supplied
  4. BM25 + FAISS hybrid reranking  →  final top_k chunks

The 10× over-fetch in step 2 ensures the reranker has enough
candidates to pick from even when many are filtered out in step 3.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.chunk import DocumentChunk
from app.rag.embeddings import get_embedding
from app.rag.reranker import rerank_chunks       # NEW: hybrid reranker
from app.rag.vector_store import vector_store

# How many FAISS candidates to fetch per desired top_k result.
# Gives the reranker plenty of material without drowning it.
CANDIDATE_MULTIPLIER = 10


async def retrieve_chunks(
    query: str,
    db: AsyncSession,
    top_k: int = 5,
    paper_ids: Optional[List[int]] = None,
    apply_reranking: bool = True,          # set False to skip reranking (e.g. unit tests)
) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant document chunks for a query.

    Args:
        query:           Natural-language query string.
        db:              Async SQLAlchemy session.
        top_k:           Number of final chunks to return.
        paper_ids:       Restrict results to these paper IDs (cross-doc search
                         when None — searches the whole index).
        apply_reranking: Whether to run BM25 hybrid reranking.

    Returns:
        List of dicts, each containing:
            chunk_id, paper_id, text, page_number, relevance_score
    """
    # ── Step 1: embed query ──────────────────────────────────────────────────
    query_emb = get_embedding(query)

    # ── Step 2: FAISS over-fetch ─────────────────────────────────────────────
    # Fetch more than top_k so the reranker / filter has room to work.
    fetch_k = top_k * CANDIDATE_MULTIPLIER
    faiss_results = vector_store.search(query_emb, top_k=fetch_k)

    if not faiss_results:
        return []

    chunk_ids = [res[0] for res in faiss_results]

    # ── Step 3: DB lookup + optional paper_id filter ─────────────────────────
    stmt = select(DocumentChunk).where(DocumentChunk.id.in_(chunk_ids))
    if paper_ids:
        stmt = stmt.where(DocumentChunk.paper_id.in_(paper_ids))

    db_result = await db.execute(stmt)
    chunks = db_result.scalars().all()

    chunk_map = {chunk.id: chunk for chunk in chunks}

    # Build candidate list preserving FAISS-derived semantic scores
    candidates: List[Dict[str, Any]] = []
    for chunk_id, distance in faiss_results:
        if chunk_id not in chunk_map:
            continue
        chunk = chunk_map[chunk_id]
        # Convert L2 distance to a 0-1 similarity score
        # distance == 0  → perfect match (score 1.0)
        # distance == 2  → opposite vectors (score 0.0)
        semantic_score = max(0.0, 1.0 - (distance / 2.0))
        candidates.append({
            "chunk_id":       chunk.id,
            "paper_id":       chunk.paper_id,
            "text":           chunk.text,
            "page_number":    chunk.page_number,
            "relevance_score": semantic_score,
        })

    if not candidates:
        return []

    # ── Step 4: rerank ───────────────────────────────────────────────────────
    # Only rerank when we have more candidates than we need — avoids
    # unnecessary BM25 work for tiny result sets.
    if apply_reranking and len(candidates) > top_k:
        return rerank_chunks(query, candidates, top_k=top_k)

    return candidates[:top_k]
