import logging
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from groq import Groq
from src.core.config import config
from src.core.database import SessionLocal
from src.core.models import Event
from src.plugins.capabilities.notifier import notifier

logger = logging.getLogger(__name__)

class DailyDigest:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        # Schedule it at 10:00 AM every day
        self.scheduler.add_job(self.generate_briefing, CronTrigger(hour=10, minute=0))

    async def start(self):
        self.scheduler.start()
        logger.info("Daily Digest Scheduled for 10:00 AM every day.")

    async def generate_briefing(self):
        logger.info("Generating Daily Morning Briefing...")
        db = SessionLocal()
        try:
            # Get events parsed in the last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            recent_events = db.query(Event).filter(Event.created_at >= yesterday).all()
            
            if not recent_events:
                logger.info("No new events in the past 24 hours to brief.")
                return

            # Format data for the LLM
            data_dump = "Here are the events I intercepted in the last 24 hours:\n"
            for e in recent_events:
                data_dump += f"- Title: {e.title}, Location: {e.location}, Status: {e.status}\n"

            prompt = f"""
You are a highly efficient Executive Assistant. 
Summarize the following intercepted events from the past 24 hours into a 2-3 sentence morning briefing for the user.
Keep it extremely concise, professional, and conversational.
Do not use markdown formatting, just plain text suitable for a notification.

{data_dump}
"""
            api_key = config.GEMINI_API_KEY
            if not api_key:
                logger.error("No API key for Groq. Cannot generate digest.")
                return

            client = Groq(api_key=api_key)
            
            # Using llama-3.3-70b-versatile for standard text generation
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a concise Executive Assistant."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3
            )
            
            briefing = chat_completion.choices[0].message.content.strip()
            
            # Fire the OS Notification!
            notifier.send_notification(
                title="Morning Briefing ☀️",
                msg=briefing
            )
            logger.info("Morning Briefing delivered.")

        except Exception as e:
            logger.error(f"Failed to generate daily digest: {e}")
        finally:
            db.close()

# Instantiate to attach it to the event loop on import
daily_digest = DailyDigest()
