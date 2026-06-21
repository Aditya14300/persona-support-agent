import json

from src.config import (
    CONFIDENCE_THRESHOLD,
    SENSITIVE_TOPICS
)


def should_escalate(
    user_query,
    context_chunks
):
    """
    Decide whether the issue should be escalated.
    """

    
    if not context_chunks:
        return True

    # Check retrieval confidence
    best_score = max(
        [
            chunk.get("score", 0)
            for chunk in context_chunks
        ],
        default=0
    )

    if best_score < CONFIDENCE_THRESHOLD and len(context_chunks) == 0:
        return True

    query_lower = user_query.lower()

    for topic in SENSITIVE_TOPICS:

        if topic.lower() in query_lower:
            return True

    return False


def generate_handoff_json(
    user_query,
    persona,
    context_chunks
):
    """
    Create structured handoff report for human agent.
    """

    confidence = 0

    if context_chunks:
        confidence = max(
            [
                chunk.get("score", 0)
                for chunk in context_chunks
            ]
        )

    handoff = {
        "persona": persona,
        "customer_issue": user_query,
        "retrieved_sources": [
            chunk.get("source", "unknown")
            for chunk in context_chunks
        ],
        "confidence_score": round(
            confidence,
            3
        ),
        "recommended_action":
        "Review customer issue and continue investigation."
    }

    return json.dumps(
        handoff,
        indent=4
    )