import azure.functions as func

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
#from openai import AzureOpenAI
#import os
#from dotenv import load_dotenv


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

### VARS ###
#load_dotenv()
#
#OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
#AZURE_ENDPOINT = "https://my-static-app-openai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2023-03-15-preview"
#MODEL = "gpt-4o"
#
#if not OPENAI_API_KEY:
#    raise ValueError("OPENAI_API_KEY is not set")

### UTILS ###

async def stream_test_func():
    for i in range(100):
        yield f"Message {i}\n"

#def get_client():
#    return AzureOpenAI(
#        api_key=OPENAI_API_KEY,
#        api_version="2024-05-13",
#        azure_endpoint=AZURE_ENDPOINT
#    )
#
#async def chat(prompt: str, client: AzureOpenAI):
#    async for chunk in client.chat.completions.create(
#        model=MODEL,
#        messages=[
#            {"role": "user", "content": prompt}
#        ],
#        stream=True
#    ):
#        if content := chunk.choices[0].delta.content:
#            yield content




### MODELS ###

class Item(BaseModel):
    name: str
    description: str = None

class LoginCredentials(BaseModel):
    username: str
    password: str

#class ChatPrompt(BaseModel):
#    prompt: str = Field(..., min_length=1, max_length=1000)


### API ROUTES ###

@app.get("/")
async def root():
    return {"message": "Welcome to the API root"}

@app.post("/webhook")
async def webhook(payload: dict) -> dict:
    return {"status": "ok", "payload": payload}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from fastapi on azure functions"}

@app.get("/api/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post("/api/items")
async def create_item(item: Item):
    return {"item": item, "message": "item was created"}

@app.post("/api/auth")
async def authenticate(credentials: LoginCredentials):
    if credentials.username == "test" and credentials.password == "test":
        return {"status": "authenticated", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Auth failed")

@app.get("/api/stream/test")
async def stream_test():
    return StreamingResponse(stream_test_func())

#@app.post("/api/chat")
#async def chat_route(prompt: ChatPrompt, client: AzureOpenAI = Depends(get_client)):
#    return StreamingResponse(chat(prompt.prompt, client), media_type="text/plain")
