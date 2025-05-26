from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import httpx, os

app = FastAPI()

# CORS setup for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can be restricted to your domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static assets and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Route: Homepage
@app.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route: Chat page
@app.get("/chat")
def chatpage(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Route: Projects page
@app.get("/projects")
def projectspage(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

# POST endpoint: Chatbot backend call to HF Inference API
@app.post("/chat")
async def chat_api(request: Request):
    body = await request.json()
    prompt = body.get("inputs", "")
    hf_token = os.getenv("HF_TOKEN")

    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.7
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
            headers=headers,
            json=payload
        )

    return JSONResponse(response.json())

