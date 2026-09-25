import streamlit as st

from src.gemini import generate_response
from src.laya_engine import DecisionEngine
from src.rag import KnowledgeBase


st.set_page_config(
    page_title="AI Support Triage",
    page_icon="",
    layout="wide",
)


@st.cache_resource
def load_system():

    knowledge = KnowledgeBase()
    decision_engine = DecisionEngine()

    return knowledge, decision_engine


knowledge, decision_engine = load_system()


st.title("AI Support Triage")

st.caption(
    "Gemini + Laya + RAG"
)


message = st.text_area(
    "Customer message",
    height=180,
    placeholder=(
        "Example: I was charged twice "
        "for my subscription..."
    ),
)


if st.button(
    "Analyze Ticket",
    type="primary",
):

    if not message.strip():

        st.warning(
            "Enter a customer message."
        )

        st.stop()

    with st.spinner(
        "Running Laya decision + RAG + Gemini..."
    ):

        # -------------------------
        # 1. Laya
        # -------------------------

        decision = decision_engine.analyze(
            message
        )

        # -------------------------
        # 2. RAG
        # -------------------------

        documents = knowledge.search(
            message,
            top_k=3,
        )

        # -------------------------
        # 3. Gemini
        # -------------------------

        response = generate_response(
            message,
            decision,
            documents,
        )

    # -----------------------------
    # Decision
    # -----------------------------

    st.divider()

    st.subheader("Laya Decision")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Department",
            decision["department"],
        )

    with col2:

        st.metric(
            "Urgency",
            f"{decision['urgency']:.2f}",
        )

    with col3:

        st.metric(
            "Human probability",
            f"{decision['human_probability']:.1%}",
        )

    st.write(
        "Department probability:",
        f"{decision['department_probability']:.1%}",
    )

    # -----------------------------
    # RAG
    # -----------------------------

    st.subheader(
        "Retrieved Knowledge"
    )

    for document, metadata in documents:

        with st.expander(
            metadata["source"]
        ):

            st.write(document)

    # -----------------------------
    # Gemini
    # -----------------------------

    st.subheader(
        "Gemini Response"
    )

    st.info(response)

    # -----------------------------
    # Raw decision
    # -----------------------------

    with st.expander(
        "Raw Laya output"
    ):

        st.json(
            decision["raw"]
        )