# Sentiment Analysis and Insight Extraction from Audio

This project uses AWS Transcribe, HuggingFace Transformers, and LLM hosted on EC2 to transcribe audio, perform sentiment analysis, and extract key insights.

## 📦 Setup

```bash
pip install -r requirements.txt
```

## 🚀 Run

```bash
streamlit run streamlit_app.py
```

## ✨ Features

- Browse from files and upload audio into S3 bucket 
- Transcribe audio using AWS Transcribe and store results in S3
- Fetch transcripts from S3 and call the LLM model hosted in EC2
- LLM model extracts insights based on prompts for the audio transcripts