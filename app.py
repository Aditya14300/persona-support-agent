import streamlit as st

from src.classifier import classify_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_adaptive_response

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    layout="wide"
)

st.title(
    "Persona Adaptive Customer Support Agent"
)

query = st.text_area(
    "Customer Message"
)

if st.button("Submit"):

    if not query.strip():
        st.warning(
            "Please enter a message."
        )

    else:

        with st.spinner(
            "Analyzing..."
        ):

            persona_result = (
                classify_persona(query)
            )

            persona = (
                persona_result["persona"]
            )

            rag = RAGPipeline()

            docs = rag.retrieve_context(
                query
            )

            result = (
                generate_adaptive_response(
                    query,
                    persona,
                    docs
                )
            )

        st.subheader(
            "Detected Persona"
        )

        st.json(
            persona_result
        )

        st.subheader(
            "Agent Response"
        )

        st.write(
            result["response"]
        )

        if result["escalated"]:

            st.subheader(
                "Human Handoff"
            )

            st.code(
                result["handoff"],
                language="json"
            )

        st.subheader(
            "Retrieved Sources"
        )

        for doc in docs:

            st.markdown(
                f"**{doc['source']}**"
            )

            st.write(
                doc["text"][:300]
            )