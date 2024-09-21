import azure.functions as func

from fastapi import FastAPI

app = FastAPI()

@app.post("/webhook")
async def webhook(payload: dict) -> dict:
    return {"status": "ok", "payload": payload}

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return await func.AsgiMiddleware(app).handle_async(req, context)
