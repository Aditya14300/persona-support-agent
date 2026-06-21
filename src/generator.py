from google import genai

from src.config import (
    GEMINI_API_KEY,
    CHAT_MODEL
)

from src.escalator import (
    should_escalate,
    generate_handoff_json
)

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_adaptive_response(
    user_query,
    persona,
    context_chunks
):

    if should_escalate(
        user_query,
        context_chunks
    ):

        return {
            "escalated": True,
            "response":
            "Your request has been escalated to a human support specialist.",
            "handoff":
            generate_handoff_json(
                user_query,
                persona,
                context_chunks
            )
        }

    context = "\n\n".join(
        [
            f"Source: {chunk['source']}\n{chunk['text']}"
            for chunk in context_chunks
        ]
    )

    if persona == "Technical Expert":

        persona_prompt = """
You are a Senior Technical Support Engineer.

Give:
- Detailed explanation
- Technical reasoning
- Configuration guidance
- Step-by-step troubleshooting

Use technical terminology when appropriate.
"""

    elif persona == "Frustrated User":

        persona_prompt = """
You are a helpful customer support specialist.

Start with empathy.

Use:
- Simple language
- Bullet points
- Easy actions

Avoid technical jargon.
"""

    else:

        persona_prompt = """
You are a Business Support Manager.

Focus on:
- Business impact
- Resolution timeline
- Operational outcome

Keep the answer concise.
"""

    system_prompt = f"""
{persona_prompt}

IMPORTANT RULES:

1. Answer only from the provided context.
2. Do not invent information.
3. If information is unavailable, say so.

CONTEXT:

{context}
"""

    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_query
                    }
                ]
            }
        ],
        config={
            "system_instruction":
            system_prompt,
            "temperature": 0.2
        }
    )

    return {
        "escalated": False,
        "response": response.text,
        "handoff": None
    }