import os
import cohere
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

app = FastAPI()

# Initialize Cohere client once
co = cohere.ClientV2(api_key=os.getenv("rfsM0XhnKGtolqxREqTYfcJ6FOGwBcWxlPpljPPR"))

@app.get("/math")
def health():
    return {"status": "Ok! This is working woohoo!", "answer": 1 + 1}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    ai_response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": request.prompt}],
    )

    # Extract the text safely
    reply_text = ai_response.message.content[0].text

    return ChatResponse(response=reply_text)

@app.post("/paid-chat", response_model=ChatResponse)
async def paid_chat(request: Request, body: ChatRequest):
    payment_ok = request.headers.get("x-payment-ok") == "true"

    if not payment_ok:
        return JSONResponse(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            content={
                "payment_instructions": {
                    "amount": "0.01 USDC",
                    "currency": "USDC",
                    "chain": "Base",
                    "payment_address": "0xABC..."
                }
            }
        )

    ai_response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": body.prompt}],
    )

    reply_text = ai_response.message.content[0].text

    return ChatResponse(response=reply_text)
