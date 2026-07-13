import logging
import asyncio
from telethon import TelegramClient, events
from src.core.config import config
from src.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class TelegramIngestor:
    def __init__(self):
        self.api_id = config.TELEGRAM_API_ID
        self.api_hash = config.TELEGRAM_API_HASH
        
        if not self.api_id or not self.api_hash:
            logger.warning("Telegram API ID or Hash is missing in .env. Telegram ingestor will not start.")
            self.client = None
            return
            
        # Initialize client with a session file stored locally
        self.client = TelegramClient('telegram_session', self.api_id, self.api_hash)
        
        @self.client.on(events.NewMessage(incoming=True))
        async def handler(event):
            sender = await event.get_sender()
            sender_id = getattr(sender, 'username', getattr(sender, 'id', 'unknown'))
            
            logger.info(f"New Telegram message from {sender_id}")
            
            await event_bus.publish("new_message", {
                "platform": "telegram",
                "identifier": f"@{sender_id}" if isinstance(sender_id, str) else str(sender_id),
                "text": event.message.text
            })

    async def start(self):
        if self.client:
            logger.info("Starting Telegram Ingestor...")
            await self.client.start()
            logger.info("Telegram Ingestor running.")
            # Run until disconnected
            await self.client.run_until_disconnected()

telegram_ingestor = TelegramIngestor()
