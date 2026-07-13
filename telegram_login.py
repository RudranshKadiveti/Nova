import os
import asyncio
from telethon import TelegramClient
from src.core.config import config
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    api_id = config.TELEGRAM_API_ID
    api_hash = config.TELEGRAM_API_HASH
    
    if not api_id or not api_hash:
        print("Please set TELEGRAM_API_ID and TELEGRAM_API_HASH in your .env file first.")
        return
        
    print("Initializing Telegram Client...")
    print("This will create a 'telegram_session.session' file locally.")
    
    client = TelegramClient('telegram_session', api_id, api_hash)
    
    # start() will prompt for phone and code interactively
    await client.start()
    
    print("\n✅ Successfully authenticated!")
    print("The session file has been created.")
    print("You can now start the main application using: python src/main.py")
    
    # Close gracefully
    await client.disconnect()

if __name__ == '__main__':
    # Use standard run which handles input properly in main thread
    asyncio.run(main())
