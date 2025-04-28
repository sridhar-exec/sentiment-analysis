from fastapi import FastAPI, Request
from llama_cpp import Llama
from pydantic import BaseModel

app = FastAPI()

# Load your model
llm = Llama(
    model_path="./mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4
)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/analyze")
async def analyze(request: PromptRequest):
    prompt_text = request.prompt

    output = llm(
        prompt_text,
        max_tokens=400,  # Can be tuned
        temperature=0.4  # Low temperature for factual summaries
    )

    response_text = output['choices'][0]['text'].strip()