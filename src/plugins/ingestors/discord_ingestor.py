import logging
import asyncio
import discord
import os
from src.core.config import config
from src.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class DiscordIngestor:
    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.client = discord.Client(intents=discord.Intents.default())

        @self.client.event
        async def on_message(message):
            # Ignore messages from the bot itself
            if message.author == self.client.user:
                return

            logger.info(f"New Discord message from {message.author}")
            
            await event_bus.publish("new_message", {
                "platform": "discord",
                "identifier": f"{message.author.name}#{message.author.discriminator}",
                "text": message.content
            })

    async def start(self):
        if not self.token:
            logger.warning("Discord Bot Token missing in .env. Discord ingestor will not start.")
            return

        logger.info("Starting Discord Ingestor...")
        try:
            await self.client.start(self.token)
        except Exception as e:
            logger.error(f"Error starting Discord Ingestor: {e}")

discord_ingestor = DiscordIngestor()
