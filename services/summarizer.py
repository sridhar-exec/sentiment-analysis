import streamlit as st
from transformers import pipeline

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_tokens=400):
    summarizer = get_summarizer()
    if len(text) < 1000:
        return text
    summary = summarizer(text, max_length=max_tokens, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def detect_conversation_type(text):
    conversation_indicators = ["Agent:", "Customer:", "Representative:", "Caller:", "User:", "Support:"]
    for indicator in conversation_indicators:
        if indicator in text:
            return "conversation"
    return "monologue"