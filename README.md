# Sentiment Analysis and Insight Extraction from Audio

This project uses Whisper, HuggingFace Transformers, and LLMs to transcribe audio, clean text, perform sentiment analysis, and extract key insights using Falcon.

## 📦 Setup

```bash
pip install -r requirements.txt
```

## 🚀 Run

Make sure you have the `harvard.wav` file in your directory.

```bash
python main.py
```

## ✨ Features

- Transcribe audio using OpenAI Whisper
- Preprocess and clean text
- Analyze sentiment with VADER and DistilBERT
- Summarize using FLAN-T5
- Extract key insights using Falcon-7B
