from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import os

app = FastAPI()

origins = ["http://localhost:3000"]  # Adjust this to match your frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_summary")
async def generate_summary(
    file: UploadFile = File(...),
    type: str = Form(...),
    summary_type: str = Form(...)):
    
    # Save the uploaded file (in a real scenario, you'd process it)
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Simulate processing time
    await asyncio.sleep(10)

    # In a real scenario, you'd generate the PDF here based on the file and summary_type
    # For this example, we'll just return a pre-made PDF
    pdf_path = "example_summary.pdf"

    # Check if the example PDF exists, if not create a simple one
    if not os.path.exists(pdf_path):
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, f"Summary of {file.filename}")
        c.drawString(100, 730, f"Document Type: {type}")
        c.drawString(100, 710, f"Summary Type: {summary_type}")
        c.drawString(100, 690, "This is an example summary.")
        c.save()

    return FileResponse(pdf_path, media_type='application/pdf', filename="generated_summary.pdf")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
