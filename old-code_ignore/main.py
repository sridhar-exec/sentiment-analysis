from utils.text_preprocessing import preprocess_text
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import whisper
import torch

# I am loading the whisper model here to transcribe sample audio
model = whisper.load_model("base")
result = model.transcribe("harvard.wav")
raw_text = result["text"]
print("Raw Transcript:", raw_text)

# a very basic preprocessing and cleaning of text
cleaned_text = preprocess_text(raw_text)
print("Cleaned Text:", cleaned_text)

# loading the DISTILBERT pre-trained model to do sentiment-analysis - this model suits larger paragraphs of text
sentiment_pipeline = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
sentiment_result = sentiment_pipeline(cleaned_text)
print("DistilBERT Sentiment:", sentiment_result)

# loading the VADER analyzer pre-trained model to do sentiment-analysis - this model suits smaller instances of text
vaderAnalyzer = SentimentIntensityAnalyzer()
vader_result = vaderAnalyzer.polarity_scores(cleaned_text)
print("VADER Sentiment:", vader_result)

# using a pre-trained small generative model to summarize - results are not so good
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")
summary_prompt = f"Analyze and summarize: {cleaned_text}"
llm_result = qa_pipeline(summary_prompt, max_length=100)
print("FLAN Summary:", llm_result[0]['generated_text'])

# using FALCON 7B, an open source readily available LLM to extract insights from text - it's decent but repeats points in output, not ideal for us
def extract_insights(transcript):
    model_name = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    prompt = f"""
    Do not repeat points.
    You are an investigator analyzing this call:
    {transcript}
    Provide key insights in bullet points.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# a sample call_transcript to see how well the models perform
call_transcript = """
Customer: I never requested a new SIM, but I got an SMS saying my number is being ported.
Rep: Did you receive any unauthorized OTPs?
Customer: Yes, and now my phone has no signal.
"""

# outputs
print("Extracted Insights:", extract_insights(call_transcript))
print("VADER on call:", vaderAnalyzer.polarity_scores(call_transcript))
print("DistilBERT on call:", sentiment_pipeline(call_transcript))
