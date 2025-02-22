import streamlit as st
import os
from text_processor import extract_text
from script_generator import generate_script
from tts_engine import text_to_speech
from utils import validate_file, get_file_extension
import base64

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env.

def main():
    st.set_page_config(
        page_title="Document to Podcast Converter",
        page_icon="🎙️",
        layout="wide"
    )

    # Load custom CSS
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("🎙️ Document to Podcast Converter")
    st.markdown("Transform your documents into engaging podcasts with AI")

    # Initialize session state
    if 'processed_text' not in st.session_state:
        st.session_state.processed_text = None
    if 'generated_script' not in st.session_state:
        st.session_state.generated_script = None
    if 'audio_file' not in st.session_state:
        st.session_state.audio_file = None

    # File upload section
    st.header("1. Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, DOCX, or TXT)",
        type=['pdf', 'docx', 'txt']
    )

    if uploaded_file:
        if validate_file(uploaded_file):
            with st.spinner("Processing document..."):
                file_extension = get_file_extension(uploaded_file.name)
                st.session_state.processed_text = extract_text(uploaded_file, file_extension)
                st.success("Document processed successfully!")
        else:
            st.error("Invalid file. Please upload a PDF, DOCX, or TXT file under 10MB.")

    # Podcast customization section
    st.header("2. Customize Your Podcast")

    tone = st.selectbox(
        "Select podcast tone",
        ["Professional", "Insightful", "Funny", "Brainrot"]
    )

    # Generate script button
    if st.session_state.processed_text and st.button("Generate Podcast Script"):
        with st.spinner("Generating script..."):
            st.session_state.generated_script = generate_script(
                st.session_state.processed_text,
                tone=tone
            )
            st.success("Script generated successfully!")

    # Display generated script
    if st.session_state.generated_script:
        st.header("3. Generated Script")
        st.text_area(
            "Preview",
            st.session_state.generated_script,
            height=400,
            disabled=True
        )

        # Generate audio button
        if st.button("Convert to Audio"):
            with st.spinner("Converting to audio... This may take a few minutes."):
                st.session_state.audio_file = text_to_speech(
                    st.session_state.generated_script,
                    tone
                )
                st.success("Audio generated successfully!")

    # Audio playback and download section
    if st.session_state.audio_file:
        st.header("4. Listen & Download")

        # Audio player
        st.audio(st.session_state.audio_file, format='audio/mp3')

        # Download button
        def get_download_link(audio_data):
            b64 = base64.b64encode(audio_data).decode()
            return f'<a href="data:audio/mp3;base64,{b64}" download="podcast.mp3">Download Podcast</a>'

        st.markdown(
            get_download_link(st.session_state.audio_file),
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()