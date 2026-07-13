import json
import logging
import os
from groq import Groq
from src.core.config import config
from src.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class EventExtractor:
    def __init__(self):
        event_bus.subscribe("process_event", self.extract_event)
        # We are using GEMINI_API_KEY from config since the user put the Groq key there
        self.api_key = config.GEMINI_API_KEY
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("API key not set. Event extraction will be disabled.")
        
    async def extract_event(self, data: dict):
        if not self.client:
            logger.error("API key not set. Cannot extract event.")
            return

        text = data.get("text")
        sender_id = data.get("sender_id")
        platform = data.get("platform")

        schema_instruction = '''
Return ONLY a valid JSON object matching this exact structure:
{
    "is_event": true or false,
    "title": "Title of the event (or null if missing)",
    "start_time": "Start time in English (or null if missing)",
    "end_time": "End time in English (or null if missing)",
    "location": "Location or meeting link (or null if missing)"
}
'''

        prompt = f"""
Analyze the following message from {platform}. 
Determine if this message contains a concrete schedule, meeting, event, or appointment.
CRITICAL RULES:
1. DO NOT invent, hallucinate, or guess any details.
2. If a detail (like location or end time) is NOT explicitly mentioned in the text, you MUST set it to null.
3. If the message is just a general statement and not a calendar event, set "is_event" to false.

{schema_instruction}

Message: "{text}"
"""

        try:
            # We use llama-3.3-70b-versatile which supports structured JSON output
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a strict, precise JSON data extraction assistant. You only extract exact facts from the provided text. You never hallucinate data."
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0,
                response_format={"type": "json_object"},
            )
            
            response_text = chat_completion.choices[0].message.content
            result = json.loads(response_text)
            
            if result.get("is_event"):
                logger.info(f"Event extracted via Groq: {result.get('title')}")
                await event_bus.publish("event_extracted", {
                    "sender_id": sender_id,
                    "event_details": result
                })
            else:
                logger.info("Message processed via Groq but no event found.")
                
        except Exception as e:
            logger.error(f"Error extracting event using Groq: {e}")

event_extractor = EventExtractor()
