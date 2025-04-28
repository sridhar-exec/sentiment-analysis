# app.py

import streamlit as st
from transformers import pipeline

# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

st.title("🧠 Simple Sentiment Analyzer")
st.write("Enter some text and know the sentiment!")

# Text input box
user_input = st.text_area("Enter text here:")

# When user clicks Analyze button
if st.button("Analyze Sentiment"):
    if user_input:
        result = sentiment_pipeline(user_input)[0]
        st.write(f"**Label:** {result['label']}")
        st.write(f"**Confidence:** {round(result['score'] * 100, 2)}%")
    else:
        st.warning("Please enter some text.")