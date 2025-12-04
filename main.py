from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import cohere

load_dotenv()

# Request body schema
class ChatRequest(BaseModel):
    prompt: str

# Response body schema
class ChatResponse(BaseModel):
    response: str

app = FastAPI()
co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

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