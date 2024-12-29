import streamlit as st
import sounddevice as sd
import numpy as np
from openai import OpenAI
from gtts import gTTS
import os
from scipy.io.wavfile import write
import tempfile
from dotenv import load_dotenv
import time
from io import BytesIO

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class AIAssistant:
    def __init__(self, role, context=""):
        self.conversation_history = []
        self.role = role
        self.context = context
        self.is_recording = False
        
    def record_audio(self):
        try:
            st.write("🎙️ Recording... Speak now!")
            duration = 5  # Record for 5 seconds
            sample_rate = 44100
            recording = sd.rec(int(duration * sample_rate), 
                             samplerate=sample_rate, channels=1)
            sd.wait()
            return recording, sample_rate
        except Exception as e:
            st.error(f"Recording error: {str(e)}")
            return None, None

    def transcribe_audio(self, audio_data, sample_rate):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                write(temp_audio.name, sample_rate, audio_data)
                with open(temp_audio.name, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                os.unlink(temp_audio.name)
                return transcript.text
        except Exception as e:
            st.error(f"Transcription error: {str(e)}")
            return None

    def get_ai_response(self, user_input):
        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            
            system_message = f"""You are a helpful {self.role} assistant. 
            Additional Context: {self.context}
            Please provide concise and relevant responses."""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    *self.conversation_history
                ]
            )
            
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            st.error(f"AI response error: {str(e)}")
            return None

    def text_to_speech(self, text):
        try:
            tts = gTTS(text=text, lang='en')
            audio_fp = BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            return audio_fp
        except Exception as e:
            st.error(f"Text-to-speech error: {str(e)}")
            return None

def main():
    st.set_page_config(page_title="AI Assistant Hub", layout="wide")
    
    # Sidebar for assistant selection and configuration
    with st.sidebar:
        st.title("🤖 Assistant Configuration")
        
        # Assistant selection
        assistant_type = st.selectbox(
            "Select Assistant Type",
            ["Restaurant", "Banking", "Healthcare", "Custom"]
        )
        
        # Custom context input
        if assistant_type == "Custom":
            custom_context = st.text_area(
                "Enter Custom Context",
                "Enter specific instructions or context for your custom assistant..."
            )
    
    # Main content area
    st.title("🎙️ AI Assistant Hub")
    
    # Initialize or update assistant based on selection
    if 'ai' not in st.session_state or st.session_state.get('current_assistant') != assistant_type:
        context_map = {
            "Restaurant": "You handle restaurant bookings, menu inquiries, and reviews.",
            "Banking": "You handle banking transactions, account inquiries, and financial advice.",
            "Healthcare": "You handle medical inquiries, appointment scheduling, and health advice.",
            "Custom": custom_context if assistant_type == "Custom" else ""
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
                    transcript = st.session_state.ai.transcribe_audio(audio_data, sample_rate)
                    
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

if __name__ == "__main__":
    main()