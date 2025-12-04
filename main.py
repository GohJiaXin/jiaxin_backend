from fastapi import FastAPI, Request,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import cohere
class chatRequest(BaseModel):
    prompt: str
class chatResponse(BaseModel):
    response: str


app = FastAPI()
@app.get("/math")#this is an endpoint
def health():
    answer=1+1
    return {"status": "Ok! This is working woohoo!", "answer": answer}

@app.post("/chat", response_model=chatResponse)
def chat(request: chatRequest):
     return chatResponse(response=f"I will get smarter later!")

@app.post("/paid-chat", response_model=chatResponse)
async def paid_chat(request: Request, body: chatRequest):
    # Mock: check if header 'x-payment-ok' is set to 'true'
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
    
    return chatResponse(response="Paid‑for answer!")
co=cohere.ClientV2()
response = co.chat(
    model="command-a-03-2025",
    messages=[{"role": "user", "content": "Tell me about LLMs"}],
)

print(response)