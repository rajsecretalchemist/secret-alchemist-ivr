from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, HTMLResponse
from fastapi.staticfiles import StaticFiles
import logging

# ── logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)

# ── app ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Secret Alchemist IVR")

# Serve the audio file at  /static/greetings.mp3
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── health check ─────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def health():
    return "<h3>Secret Alchemist IVR is running ✅</h3>"


# ── answer webhook ────────────────────────────────────────────────────────────
@app.post("/answer")
async def answer(request: Request):
    """
    Vobiz calls this endpoint the moment someone dials your DID.
    We return XML that tells Vobiz to play the greeting and hang up.
    """
    form = await request.form()
    caller   = form.get("From", "unknown")
    call_uuid = form.get("CallUUID", "unknown")

    log.info(f"Incoming call | UUID={call_uuid} | From={caller}")

    # Build the public URL for the audio file.
    # Vobiz fetches this URL directly, so it must be reachable from the internet.
    base_url = str(request.base_url).rstrip("/")
    audio_url = f"{base_url}/static/greetings.mp3"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
    <Hangup/>
</Response>"""

    log.info(f"Returning XML for UUID={call_uuid} | audio={audio_url}")
    return Response(content=xml, media_type="application/xml")


# ── hangup webhook (optional — Vobiz sends this when the call ends) ───────────
@app.post("/hangup")
async def hangup(request: Request):
    """
    Vobiz notifies this endpoint after the call ends.
    No XML response needed — just log and return 200.
    """
    form = await request.form()
    call_uuid  = form.get("CallUUID", "unknown")
    duration   = form.get("Duration", "unknown")
    status     = form.get("CallStatus", "unknown")
    hangup_cause = form.get("HangupCause", "unknown")

    log.info(
        f"Call ended | UUID={call_uuid} | Status={status} "
        f"| Duration={duration}s | Cause={hangup_cause}"
    )
    return Response(status_code=200)
