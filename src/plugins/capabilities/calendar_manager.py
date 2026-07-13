import logging
import os
import dateparser
from datetime import datetime, timezone
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.core.event_bus import event_bus
from src.core.database import SessionLocal
from src.core.models import Event

logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class CalendarManager:
    def __init__(self):
        self.creds = None
        self.service = None
        self.setup_google_calendar()
        event_bus.subscribe("event_extracted", self.sync_event)

    def setup_google_calendar(self):
        """Authenticates with Google Calendar and builds the service."""
        try:
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists('credentials.json'):
                        logger.warning("credentials.json not found! Google Calendar syncing is disabled.")
                        return
                    
                    logger.info("Waiting for Google Calendar OAuth Login...")
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
                    
            self.service = build('calendar', 'v3', credentials=self.creds)
            logger.info("Google Calendar Service successfully initialized!")
            
        except Exception as e:
            logger.error(f"Failed to setup Google Calendar: {e}")

    def parse_datetime(self, time_str: str) -> str:
        """Parses a natural language time string into an RFC3339 formatted string."""
        if not time_str:
            return None
        try:
            # Parse the time string relative to now, assuming local timezone
            dt = dateparser.parse(time_str)
            if not dt:
                return None
            
            # If naive, localize to local timezone (we'll just use UTC for safety or assume local)
            if dt.tzinfo is None:
                # Get local timezone dynamically or fallback to UTC
                local_tz = datetime.now().astimezone().tzinfo
                dt = dt.replace(tzinfo=local_tz)
                
            return dt.isoformat()
        except Exception as e:
            logger.error(f"Date parsing failed for '{time_str}': {e}")
            return None

    async def sync_event(self, data: dict):
        sender_id = data.get("sender_id")
        details = data.get("event_details", {})
        
        title = details.get("title")
        raw_start = details.get("start_time")
        raw_end = details.get("end_time")
        location = details.get("location")
        
        if not title or not raw_start:
            logger.warning("Event missing title or start_time, skipping sync.")
            return
            
        start_time_iso = self.parse_datetime(raw_start)
        if not start_time_iso:
            logger.warning(f"Could not parse start time '{raw_start}', skipping sync.")
            return
            
        end_time_iso = self.parse_datetime(raw_end)
        dt_start = datetime.fromisoformat(start_time_iso)
        
        # Determine dt_end safely
        dt_end = None
        if end_time_iso:
            try:
                dt_end = datetime.fromisoformat(end_time_iso)
            except ValueError:
                pass
                
        # If no valid end time or end time is before/equal to start time, default to 1 hour after start
        if not dt_end or dt_end <= dt_start:
            from datetime import timedelta
            dt_end = dt_start + timedelta(hours=1)
            
        end_time_iso = dt_end.isoformat()

        logger.info(f"Syncing event '{title}' scheduled for {start_time_iso} to Calendar...")
        
        db = SessionLocal()
        try:
            # Duplicate Detection Strategy
            # Check if an event with the exact title and start time from this sender already exists
            existing_event = db.query(Event).filter(
                Event.sender_id == sender_id,
                Event.title == title
            ).first()
            
            if existing_event:
                logger.info(f"Event '{title}' already exists in DB! Skipping duplicate sync.")
                return

            # Conflict Detection Strategy via Google Calendar API
            conflict_found = False
            if self.service:
                try:
                    events_result = self.service.events().list(
                        calendarId='primary', 
                        timeMin=start_time_iso,
                        timeMax=end_time_iso, 
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()
                    
                    conflicts = events_result.get('items', [])
                    if conflicts:
                        conflict_title = conflicts[0].get('summary', 'Busy')
                        conflict_found = True
                        logger.warning(f"Conflict detected! You already have '{conflict_title}' scheduled.")
                        
                        from src.plugins.capabilities.notifier import notifier
                        notifier.send_notification(
                            title="Schedule Conflict Detected! ⚠️",
                            msg=f"Tried to add '{title}' but you already have '{conflict_title}' at this time."
                        )
                except Exception as e:
                    logger.error(f"Failed to check conflicts: {e}")

            # Push to Google Calendar (Even if conflict, we'll add it but maybe mark as tentative, or just add it normally since the user is warned)
            event_link = None
            if self.service:
                event_body = {
                    'summary': f"[CONFLICT] {title}" if conflict_found else title,
                    'location': location,
                    'start': {
                        'dateTime': start_time_iso,
                    },
                    'end': {
                        'dateTime': end_time_iso,
                    }
                }
                
                created_event = self.service.events().insert(calendarId='primary', body=event_body).execute()
                event_link = created_event.get('htmlLink')
                logger.info(f"Event successfully synced to Google Calendar: {event_link}")
                
                if not conflict_found:
                    from src.plugins.capabilities.notifier import notifier
                    notifier.send_notification(
                        title="New Event Synced 📅",
                        msg=f"'{title}' has been added to your Google Calendar."
                    )
            else:
                logger.warning("Google Calendar service not initialized. Saving to DB only.")

            # Save to Local Database
            new_event = Event(
                sender_id=sender_id,
                title=title,
                location=location,
                status="synced" if self.service else "pending_sync"
            )
            db.add(new_event)
            db.commit()
            
            logger.info("Event successfully saved locally.")
            
        except Exception as e:
            logger.error(f"Failed to sync event: {e}")
            db.rollback()
        finally:
            db.close()

calendar_manager = CalendarManager()
