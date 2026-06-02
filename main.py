import logging
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sa-ivr")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.api_route("/answer", methods=["GET", "POST"])
async def answer(request: Request):
    logger.info("CALL RECEIVED")
    base_url = str(request.base_url).rstrip("/")
    audio_url = f"{base_url}/static/greetings.mp3"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
    <Hangup/>
</Response>"""
    logger.info(f"Returning XML with audio: {audio_url}")
    return Response(content=xml, media_type="application/xml")

@app.api_route("/hangup", methods=["GET", "POST"])
async def hangup(request: Request):
    logger.info("CALL ENDED")
    return Response(status_code=200)
