import logging
import asyncio
from googleapiclient.discovery import build
import os
from src.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class YouTubeIngestor:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        # List of channel IDs to monitor
        self.channel_ids = os.getenv("YOUTUBE_CHANNEL_IDS", "").split(",")
        self.running = False

    async def start(self):
        if not self.api_key or not self.channel_ids or self.channel_ids == [""]:
            logger.warning("YouTube API Key or Channel IDs missing in .env. YouTube ingestor will not start.")
            return

        self.running = True
        logger.info("Starting YouTube Ingestor...")
        
        while self.running:
            try:
                await asyncio.to_thread(self.check_livestreams)
            except Exception as e:
                logger.error(f"YouTube Ingestor error: {e}")
            
            # Poll every 15 minutes to save quota
            await asyncio.sleep(900)

    def check_livestreams(self):
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        
        for channel_id in self.channel_ids:
            channel_id = channel_id.strip()
            if not channel_id:
                continue
                
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                eventType="upcoming",
                type="video",
                maxResults=5
            )
            response = request.execute()
            
            for item in response.get("items", []):
                title = item["snippet"]["title"]
                channel_title = item["snippet"]["channelTitle"]
                video_id = item["id"]["videoId"]
                
                # Fetch video details to get exact scheduled start time
                video_request = youtube.videos().list(
                    part="liveStreamingDetails",
                    id=video_id
                )
                video_response = video_request.execute()
                
                if not video_response["items"]:
                    continue
                    
                scheduled_start = video_response["items"][0]["liveStreamingDetails"].get("scheduledStartTime")
                link = f"https://youtube.com/watch?v={video_id}"
                
                logger.info(f"Upcoming Livestream found: {title} by {channel_title}")
                
                text = f"Upcoming YouTube Livestream: '{title}' by {channel_title}. Scheduled for {scheduled_start}. Link: {link}"
                
                asyncio.run_coroutine_threadsafe(
                    event_bus.publish("new_message", {
                        "platform": "youtube",
                        "identifier": channel_title,
                        "text": text
                    }),
                    asyncio.get_running_loop()
                )

youtube_ingestor = YouTubeIngestor()
