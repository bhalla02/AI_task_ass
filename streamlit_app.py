import streamlit as st
from backend.orchestrator import MathMentorOrchestrator
from streamlit_mic_recorder import mic_recorder
import os

st.set_page_config(page_title="Math Mentor", layout="wide")

st.title("🧠 Reliable Math Mentor")
st.markdown("RAG + Multi-Agent + Symbolic Verification")

orchestrator = MathMentorOrchestrator()

os.makedirs("data", exist_ok=True)

# Initialize session state
if "uploaded_file_path" not in st.session_state:
    st.session_state.uploaded_file_path = None

# -----------------------
# INPUT MODE
# -----------------------

st.header("Choose Input Mode")

input_mode = st.radio(
    "Select how you want to provide the problem:",
    ["Text", "Image", "Audio"]
)

user_input = None

# -----------------------
# TEXT INPUT
# -----------------------

if input_mode == "Text":

    user_input = st.text_area(
        "Type your JEE-style math question:",
        height=120,
        placeholder="Example: Find derivative of x^2 sin(x)"
    )

# -----------------------
# IMAGE INPUT
# -----------------------

elif input_mode == "Image":

    uploaded_file = st.file_uploader(
        "Upload a math problem image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:

        file_path = f"data/{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        st.session_state.uploaded_file_path = file_path

# -----------------------
# AUDIO INPUT (MIC)
# -----------------------

elif input_mode == "Audio":

    st.subheader("🎤 Ask Your Question")

    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        just_once=True,
        key="audio_recorder"
    )

    if audio:

        audio_bytes = audio["bytes"]

        audio_path = "data/mic_audio.wav"

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        st.audio(audio_bytes)

        st.session_state.uploaded_file_path = audio_path

# -----------------------
# SOLVE BUTTON
# -----------------------

solve_button = st.button("Solve")

# -----------------------
# PROCESS INPUT
# -----------------------

if solve_button:

    if input_mode == "Text":

        if not user_input:
            st.warning("Please enter a problem.")
            st.stop()

        input_type = "text"
        input_data = user_input

    elif input_mode == "Image":

        file_path = st.session_state.get("uploaded_file_path")

        if not file_path:
            st.warning("Please upload an image.")
            st.stop()

        input_type = "image"
        input_data = file_path

    elif input_mode == "Audio":

        file_path = st.session_state.get("uploaded_file_path")

        if not file_path:
            st.warning("Please record audio first.")
            st.stop()

        input_type = "audio"
        input_data = file_path

    with st.spinner("Solving..."):
        result = orchestrator.run_pipeline(input_type, input_data)

# -----------------------
# HANDLE HITL EXTRACTION
# -----------------------

    if result["status"] == "needs_review":

        st.warning("⚠️ Human verification required.")

        extracted_text = st.text_area(
            "Edit extracted text before solving:",
            result.get("extracted_text", "")
        )

        if st.button("Solve with Edited Text"):

            with st.spinner("Re-solving..."):

                result = orchestrator.run_pipeline(
                    input_type="text",
                    input_data=extracted_text
                )

# -----------------------
# HANDLE PARSER CLARIFICATION
# -----------------------

    if result["status"] == "needs_clarification":

        st.warning("⚠️ Clarification required before solving.")

        st.json(result["trace"]["parser"])

# -----------------------
# SUCCESS OUTPUT
# -----------------------

    elif result["status"] == "success":

        col1, col2 = st.columns([2, 1])

        with col1:

            st.subheader("✅ Final Answer")
            st.success(result["final_answer"])

            st.subheader("📝 Step-by-Step Solution")

            for i, step in enumerate(result["solution_steps"], 1):
                st.markdown(f"**Step {i}:** {step}")

        with col2:

            st.subheader("📊 Confidence")

            confidence_value = result["confidence"]

            st.progress(min(confidence_value, 1.0))

            if confidence_value > 0.8:
                st.success(f"Confidence: {confidence_value}")
            elif confidence_value > 0.6:
                st.warning(f"Confidence: {confidence_value}")
            else:
                st.error(f"Confidence: {confidence_value}")

            if result["verified"]:
                st.success("✔ Verified Symbolically")
            else:
                st.error("✘ Verification Failed")

            st.subheader("📚 Retrieved Sources")

            for source in result["used_sources"]:
                st.markdown(f"- {source}")

# -----------------------
# FEEDBACK
# -----------------------

        st.subheader("🗳 Feedback")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Correct"):
                st.success("Feedback saved!")

        with col2:
            if st.button("❌ Incorrect"):
                feedback_text = st.text_input("What was wrong?")

# -----------------------
# TRACE PANEL
# -----------------------

        with st.expander("🔍 System Execution Trace"):

            trace = result["trace"]

            stages = [
                "multimodal",
                "parser",
                "router",
                "solver",
                "verifier",
                "explainer"
            ]

            cols = st.columns(len(stages))

            for i, stage in enumerate(stages):

                with cols[i]:

                    if stage in trace:
                        st.success(stage.upper())
                    else:
                        st.error(stage.upper())

            st.divider()

            for stage in stages:

                if stage in trace:

                    st.subheader(stage.capitalize())

                    with st.expander(f"View {stage} details"):

                        st.json(trace[stage])