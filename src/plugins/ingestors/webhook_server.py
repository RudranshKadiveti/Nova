import logging
import asyncio
from fastapi import FastAPI, Request
from src.core.event_bus import event_bus
import uvicorn

logger = logging.getLogger(__name__)

app = FastAPI(title="AI Assistant Webhook Ingestors")

# --- WhatsApp Route ---
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    payload = await request.json()
    try:
        if "messages" in payload.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
            message = payload["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message.get("from")
            text = message.get("text", {}).get("body", "")
            
            logger.info(f"New WhatsApp message from {sender}")
            await event_bus.publish("new_message", {
                "platform": "whatsapp",
                "identifier": sender,
                "text": text
            })
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error parsing WhatsApp payload: {e}")
        return {"status": "error"}

# --- Zoom Route ---
@app.post("/webhook/zoom")
async def zoom_webhook(request: Request):
    payload = await request.json()
    try:
        event_type = payload.get("event")
        if event_type == "meeting.invitation_created" or event_type == "meeting.created":
            obj = payload.get("payload", {}).get("object", {})
            host_email = obj.get("host_email")
            topic = obj.get("topic")
            start_time = obj.get("start_time")
            join_url = obj.get("join_url")
            
            logger.info(f"New Zoom meeting invite from {host_email}")
            
            # Format it as natural language so the AI can extract it, 
            # or directly publish as a structured event.
            text = f"Zoom Meeting Invite: {topic}. Starts at {start_time}. Link: {join_url}"
            
            await event_bus.publish("new_message", {
                "platform": "zoom",
                "identifier": host_email,
                "text": text
            })
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error parsing Zoom payload: {e}")
        return {"status": "error"}

from src.core.database import SessionLocal
from src.core.models import Sender
from fastapi.responses import HTMLResponse

@app.get("/sender/approve", response_class=HTMLResponse)
async def approve_sender(id: int):
    db = SessionLocal()
    try:
        sender = db.query(Sender).filter(Sender.id == id).first()
        if sender:
            sender.action_rule = "auto-sync"
            db.commit()
            logger.info(f"User approved sender: {sender.identifier}")
            
            # Fire confirmation notification
            from src.plugins.capabilities.notifier import notifier
            notifier.send_notification(title="Sender Approved ✅", msg=f"All future messages from {sender.identifier} will be processed automatically.")
            
            return f"<html><body><h2>Success!</h2><p>{sender.identifier} has been approved. You may close this window.</p></body></html>"
        return f"<html><body><h2>Error</h2><p>Sender not found.</p></body></html>"
    finally:
        db.close()

@app.get("/sender/ignore", response_class=HTMLResponse)
async def ignore_sender(id: int):
    db = SessionLocal()
    try:
        sender = db.query(Sender).filter(Sender.id == id).first()
        if sender:
            sender.action_rule = "ignore"
            db.commit()
            logger.info(f"User ignored sender: {sender.identifier}")
            return f"<html><body><h2>Ignored!</h2><p>{sender.identifier} has been blacklisted. You may close this window.</p></body></html>"
        return f"<html><body><h2>Error</h2><p>Sender not found.</p></body></html>"
    finally:
        db.close()

class WebhookServer:
    async def start(self):
        logger.info("Starting Central Webhook Server on port 8085 (WhatsApp, Zoom)...")
        config = uvicorn.Config(app, host="0.0.0.0", port=8085, log_level="warning")
        server = uvicorn.Server(config)
        try:
            await server.serve()
        except SystemExit:
            logger.error("Failed to start webhook server (port might be in use).")
        except Exception as e:
            logger.error(f"Webhook server error: {e}")

webhook_server = WebhookServer()
