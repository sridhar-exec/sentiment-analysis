import boto3
import os
import time
import random
import string
import json
import streamlit as st
from dotenv import load_dotenv
from utils.helpers import random_string

load_dotenv()

AWS_ACCESS_KEY = os.getenv('MY_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('MY_AWS_SECRET_KEY')
REGION_NAME = os.getenv('MY_REGION')
BUCKET_NAME = os.getenv('MY_BUCKET_NAME')

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  region_name=REGION_NAME)

transcribe = boto3.client('transcribe',
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=REGION_NAME)

def upload_to_s3(file, bucket_name):
    try:
        s3.upload_fileobj(file, bucket_name, file.name)
        st.success(f"✅ File uploaded to S3: {file.name}")
        return f"https://{bucket_name}.s3.{REGION_NAME}.amazonaws.com/{file.name}"
    except Exception as e:
        st.error(f"Error uploading to S3: {e}")
        return None

def start_transcription_job(file_name):
    base_job_name = file_name.split('.')[0] + "-transcription"
    unique_job_name = base_job_name + "-" + random_string()

    job_uri = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{file_name}"

    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=unique_job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat=file_name.split('.')[-1],
            LanguageCode='en-US',
            OutputBucketName=BUCKET_NAME
        )
        st.success(f"Transcription job '{unique_job_name}' started successfully!")
        return unique_job_name
    except Exception as e:
        st.error(f"Error starting transcription job: {e}")
        return None

def wait_for_transcription(job_name):
    with st.spinner('⏳ Waiting for transcription to complete...'):
        while True:
            response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']

            if status == 'COMPLETED':
                st.success("✅ Transcription completed!")
                transcript_file_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                return transcript_file_uri
            elif status == 'FAILED':
                st.error("❌ Transcription failed.")
                return None
            else:
                time.sleep(5)

def fetch_transcript_text_s3(job_name):
    output_key = job_name + '.json'
    try:
        s3_response = s3.get_object(Bucket=BUCKET_NAME, Key=output_key)
        json_content = s3_response['Body'].read().decode('utf-8')
        transcript_json = json.loads(json_content)
        transcript_text = transcript_json['results']['transcripts'][0]['transcript']
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript from S3: {e}")
        return None