from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Sender
from .event_bus import event_bus
import logging
import asyncio

logger = logging.getLogger(__name__)

class SenderManager:
    def __init__(self):
        event_bus.subscribe("new_message", self.handle_new_message)

    def get_or_create_sender(self, db: Session, platform: str, identifier: str) -> Sender:
        sender = db.query(Sender).filter(
            Sender.platform == platform, 
            Sender.identifier == identifier
        ).first()

        if not sender:
            sender = Sender(platform=platform, identifier=identifier, action_rule="ask")
            db.add(sender)
            db.commit()
            db.refresh(sender)
            self.ask_user_preference(platform, identifier, sender.id)
            
        return sender

    def ask_user_preference(self, platform: str, identifier: str, sender_id: int):
        title = "New Sender Detected 🛡️"
        message = f"Detected a new sender: {identifier} on {platform}. Should I process their messages?"
        
        try:
            from src.plugins.capabilities.notifier import notifier
            actions = [
                {"label": "Approve", "launch": f"http://localhost:8085/sender/approve?id={sender_id}"},
                {"label": "Ignore", "launch": f"http://localhost:8085/sender/ignore?id={sender_id}"}
            ]
            notifier.send_notification(title=title, msg=message, actions=actions)
            logger.info(f"Interactive Notification sent for new sender: {identifier}")
        except Exception as e:
            logger.error(f"Failed to send interactive OS notification: {e}")

    async def handle_new_message(self, data: dict):
        platform = data.get("platform")
        identifier = data.get("identifier")
        message_text = data.get("text")
        
        db = SessionLocal()
        try:
            sender = self.get_or_create_sender(db, platform, identifier)
            
            if sender.action_rule == "auto-sync":
                await event_bus.publish("process_event", {
                    "sender_id": sender.id,
                    "text": message_text,
                    "platform": platform
                })
            elif sender.action_rule == "ignore":
                logger.info(f"Ignoring message from {identifier} based on rules.")
            elif sender.action_rule == "ask":
                logger.info(f"Sender {identifier} is still pending rule configuration. Holding message.")
        finally:
            db.close()

sender_manager = SenderManager()
