import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.core.database import engine, Base
from src.core.event_bus import event_bus
from src.core.sender_manager import sender_manager
# Import Processors
from src.plugins.processors.event_extractor import event_extractor
from src.plugins.processors.daily_digest import daily_digest
# Import Capabilities
from src.plugins.capabilities.calendar_manager import calendar_manager
# Import Ingestors
from src.plugins.ingestors.telegram_ingestor import telegram_ingestor
from src.plugins.ingestors.gmail_ingestor import gmail_ingestor
from src.plugins.ingestors.discord_ingestor import discord_ingestor
from src.plugins.ingestors.youtube_ingestor import youtube_ingestor
from src.plugins.ingestors.webhook_server import webhook_server
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

async def main():
    logger.info("Initializing AI Executive Assistant Core...")
    
    # Start event bus
    bus_task = asyncio.create_task(event_bus.start())
    
    # Start ingestors (background tasks)
    telegram_task = asyncio.create_task(telegram_ingestor.start())
    gmail_task = asyncio.create_task(gmail_ingestor.start())
    discord_task = asyncio.create_task(discord_ingestor.start())
    youtube_task = asyncio.create_task(youtube_ingestor.start())
    webhook_task = asyncio.create_task(webhook_server.start())
    digest_task = asyncio.create_task(daily_digest.start())
    
    try:
        # Keep main running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        event_bus.stop()
        await bus_task
        telegram_task.cancel()
        gmail_task.cancel()
        discord_task.cancel()
        youtube_task.cancel()
        webhook_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
