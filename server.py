from __future__ import annotations

from pathlib import Path
import socket

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
    host = "127.0.0.1"
    desired_port = 7860

    def _find_free_port(start_port: int, max_tries: int = 50) -> int:
        """Pick the first available TCP port on localhost."""
        for p in range(start_port, start_port + max_tries):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.bind((host, p))
                s.listen(1)
                return p
            except OSError:
                continue
            finally:
                try:
                    s.close()
                except Exception:
                    pass
        raise RuntimeError(f"No free port found in range {start_port}..{start_port + max_tries - 1}")

    # Pre-check whether the port is already bound; this helps pinpoint EADDRINUSE.
    port_in_use = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, desired_port))
        sock.listen(1)
    except OSError as e:
        port_in_use = True
    finally:
        try:
            sock.close()
        except Exception:
            pass

    port = desired_port
    if port_in_use:
        # If 7860 is taken, choose another port so the app can still start.
        port = _find_free_port(desired_port + 1, max_tries=50)

    try:
        uvicorn.run(app, host=host, port=port, reload=False)
    except OSError as e:
        raise

