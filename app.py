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

# Initialize RAG only once
if "rag" not in st.session_state:

    rag = RAGPipeline()

    try:
        # Build index if empty
        if rag.vector_store._collection.count() == 0:
            rag.build_index()
    except Exception:
        rag.build_index()

    st.session_state.rag = rag

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

            rag = st.session_state.rag

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

        if not docs:
            st.warning(
                "No documents retrieved from knowledge base."
            )

        for doc in docs:

            st.markdown(
                f"**{doc['source']}**"
            )

            st.write(
                doc["text"][:300]
            )
