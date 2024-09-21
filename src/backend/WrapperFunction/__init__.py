import azure.functions as func

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

class LoginCredentials(BaseModel):
    username: str
    password: str

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
