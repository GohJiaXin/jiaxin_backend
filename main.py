import os

import cohere
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel


# Load environment variables from a local .env file (if present)
load_dotenv()


# Request body schema
class ChatRequest(BaseModel):
    prompt: str


# Response body schema
class ChatResponse(BaseModel):
    response: str


app = FastAPI()

# Get Cohere API key from environment
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")

if not COHERE_API_KEY:
    # Fail fast with a clear error if the key is missing
    raise RuntimeError(
        "Cohere API key not found. Set COHERE_API_KEY (or CO_API_KEY) in your "
        "environment or in a .env file in the project root."
    )

# Initialize Cohere client once
co = cohere.ClientV2(api_key=COHERE_API_KEY)


@app.get("/")
def health():
    return {"status": "Ok! This is working woohoo!"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_prompt = request.prompt

    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": user_prompt}],
    )

    final_response = response.message.content[0].text

    return ChatResponse(response=f"Cohere said this: {final_response}")