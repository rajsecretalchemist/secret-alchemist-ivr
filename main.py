import logging
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sa-ivr")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

AUDIO_URL = "https://secret-alchemist-ivr-production.up.railway.app/static/greeting_final.mp3"
@app.api_route("/answer", methods=["GET", "POST"])
async def answer(request: Request):
    logger.info("CALL RECEIVED")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{AUDIO_URL}</Play>
    <Hangup/>
</Response>"""
    return Response(content=xml, media_type="application/xml")

@app.api_route("/hangup", methods=["GET", "POST"])
async def hangup(request: Request):
    logger.info("CALL ENDED")
    return Response(status_code=200)
