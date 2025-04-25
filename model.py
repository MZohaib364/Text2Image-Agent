from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

# Access the token
API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_image(req: PromptRequest):
    response = requests.post(API_URL, headers=headers, json={"inputs": req.prompt})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Model failed to generate image")

    # Save image to disk
    with open("generated.png", "wb") as f:
        f.write(response.content)

    return {"status": "success", "message": "Image generated", "file": "generated.png"}
