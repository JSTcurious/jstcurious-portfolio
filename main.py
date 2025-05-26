
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the homepage
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Serve the chat page
@app.get("/chat")
def serve_chat():
    return FileResponse("static/chat.html")
