from __future__ import annotations

from pathlib import Path
import os

import gradio as gr
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from gradio.routes import mount_gradio_app

from gradio_app import demo

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
ASSETS_DIR = BASE_DIR / "assets"

app = FastAPI(title="AI Doctor")

# Serve landing page static assets (CSS/JS/images).
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend_static")
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/")
def index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


# Enable Gradio queuing for smoother UX with longer inference.
try:
    demo.queue()
except Exception:
    # Some Gradio versions may not support queue() depending on the mounting mode.
    pass

mount_gradio_app(app, demo, path="/app")


if __name__ == "__main__":
    # Render expects services to listen on `0.0.0.0` and the injected `PORT` env var.
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host=host, port=port, reload=False)

