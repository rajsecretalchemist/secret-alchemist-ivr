import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sa-ivr")

app = FastAPI()

@app.api_route("/answer", methods=["GET", "POST"])
async def answer(request: Request):
    logger.info("INBOUND CALL RECEIVED")
    xml = '<?xml version="1.0" encoding="UTF-8"?><Response><Speak voice="WOMAN" language="en-IN">Thank you for calling Secret Alchemist! For order-related or general queries, please email us at care at secret alchemist dot com. I Repeat C, A, R, E at Secret Alchemist dot com. You can also reach us on 77188 21521. Our team is available Monday to Friday, 10 AM to 6 PM. We look forward to hearing from you.</Speak><Hangup/></Response>'
    return HTMLResponse(content=xml, media_type="application/xml")

@app.api_route("/hangup", methods=["GET", "POST"])
async def hangup(request: Request):
    logger.info("CALL ENDED")
    return Response(status_code=200)
