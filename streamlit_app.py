import streamlit as st
import os
import requests
import time
from dotenv import load_dotenv

from prompts.prompts import get_prompt_template
from services.aws_service import upload_to_s3, start_transcription_job, wait_for_transcription, fetch_transcript_text_s3
from services.summarizer import summarize_text, detect_conversation_type

# Load environment variables
load_dotenv()

BUCKET_NAME = os.getenv('MY_BUCKET_NAME')

st.title("🎵 Audio to Text + Smart LLM Insights")

uploaded_file = st.file_uploader("Upload your audio file", type=["wav", "mp3", "flac"])

if uploaded_file:
    st.write(f"File name: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
    st.session_state['uploaded_file'] = uploaded_file

if 'uploaded_file' in st.session_state:
    if st.button("Upload to S3"):
        uploaded_file_url = upload_to_s3(st.session_state['uploaded_file'], BUCKET_NAME)

        if uploaded_file_url:
            st.session_state['uploaded_file_url'] = uploaded_file_url
            st.session_state['uploaded_file_name'] = st.session_state['uploaded_file'].name
            st.session_state['uploaded'] = True

if st.session_state.get('uploaded'):
    if st.button("Start Transcription and Get Insights"):
        file_name = st.session_state['uploaded_file_name']
        transcription_job_name = start_transcription_job(file_name)

        if transcription_job_name:
            transcript_uri = wait_for_transcription(transcription_job_name)

            if transcript_uri:
                transcript_text = fetch_transcript_text_s3(transcription_job_name)
                st.subheader("📜 Transcribed Text:")
                st.write(transcript_text)

                if transcript_text:
                    st.subheader("🤖 Generating Smart LLM Insights...")
                    with st.spinner('⏳ Thinking...'):

                        conv_type = detect_conversation_type(transcript_text)
                        prompt_template = get_prompt_template(conv_type)
                        summarized_text = summarize_text(transcript_text)
                        final_prompt = prompt_template.replace("{transcript_text}", summarized_text)

                        try:
                            LLM_start_time = time.time()

                            response = requests.post(
                                "http://16.171.71.224:5000/analyze",
                                headers={"Content-Type": "application/json"},
                                json={"prompt": final_prompt}
                            )

                            LLM_end_time = time.time()
                            LLM_duration = LLM_end_time - LLM_start_time

                            if response.status_code == 200:
                                llama_output = response.json().get("summary", "No output received.")
                                st.subheader("🔍 LLM Model Analysis:")
                                st.write(llama_output)

                                st.success(f"✅ LLM Insights generated in {LLM_duration:.2f} seconds.")
                            else:
                                st.error(f"❌ Error from LLM API: {response.text}")

                        except Exception as e:
                            st.error(f"❌ Failed to reach LLM API: {e}")