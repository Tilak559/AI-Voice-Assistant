import streamlit as st
from ..core.assistant import AIAssistant

def init_session_state():
    if "ai" not in st.session_state:
        st.session_state.ai = None
    if "current_assistant" not in st.session_state:
        st.session_state.current_assistant = None

def main():
    st.set_page_config(page_title="AI Assistant Hub", layout="wide")
    init_session_state()

    # Sidebar for assistant selection and configuration
    with st.sidebar:
        st.title("🤖 Assistant Configuration")

        # Assistant selection
        assistant_type = st.selectbox(
            "Select Assistant Type", ["Restaurant", "Banking", "Healthcare", "Custom"]
        )

        # Custom context input
        custom_context = ""
        if assistant_type == "Custom":
            custom_context = st.text_area(
                "Enter Custom Context",
                "Enter specific instructions or context for your custom assistant...",
            )

    # Main content area
    st.title("🎙️ AI Assistant Hub")

    # Initialize or update assistant based on selection
    if (
        "ai" not in st.session_state
        or st.session_state.get("current_assistant") != assistant_type
    ):
        context_map = {
            "Restaurant": "You handle restaurant bookings, menu inquiries, and reviews.",
            "Banking": "You handle banking transactions, account inquiries, and financial advice.",
            "Healthcare": "You handle medical inquiries, appointment scheduling, and health advice.",
            "Custom": custom_context if assistant_type == "Custom" else "",
        }
        st.session_state.ai = AIAssistant(assistant_type, context_map[assistant_type])
        st.session_state.current_assistant = assistant_type

    # Create two columns for the main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 Conversation")
        # Record button
        if st.button("🎤 Start Recording"):
            audio_data, sample_rate = st.session_state.ai.record_audio()

            if audio_data is not None:
                with st.spinner("Transcribing..."):
                    transcript = st.session_state.ai.transcribe_audio(
                        audio_data, sample_rate
                    )

                if transcript:
                    st.info(f"You said: {transcript}")

                    with st.spinner("Getting AI response..."):
                        ai_response = st.session_state.ai.get_ai_response(transcript)

                    if ai_response:
                        st.success(f"AI Response: {ai_response}")

                        with st.spinner("Converting to speech..."):
                            audio_fp = st.session_state.ai.text_to_speech(ai_response)
                            if audio_fp:
                                st.audio(audio_fp)

    with col2:
        st.subheader("📝 Conversation History")
        if st.session_state.ai.conversation_history:
            for message in st.session_state.ai.conversation_history:
                role = "🧑" if message["role"] == "user" else "🤖"
                st.write(f"{role}: {message['content']}")

        if st.button("Clear History"):
            st.session_state.ai.conversation_history = []
            st.rerun()