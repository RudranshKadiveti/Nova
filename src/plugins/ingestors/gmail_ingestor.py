import imaplib
import email
import logging
import asyncio
from email.header import decode_header
from src.core.config import config
from src.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class GmailIngestor:
    def __init__(self):
        # We need an App Password to use IMAP with Gmail
        self.username = config.EMAIL_ADDRESS if hasattr(config, "EMAIL_ADDRESS") else None
        self.password = config.GMAIL_APP_PASSWORD if hasattr(config, "GMAIL_APP_PASSWORD") else None
        self.running = False
        self.last_seen_uid = None

    async def start(self):
        if not self.username or not self.password:
            logger.warning("Gmail credentials missing in .env. Gmail ingestor will not start.")
            return

        self.running = True
        logger.info("Starting Gmail Ingestor...")
        
        while self.running:
            try:
                # Run the blocking IMAP operations in a thread
                new_emails = await asyncio.to_thread(self.fetch_new_emails)
                
                # Publish them from the main thread safely
                if new_emails:
                    for email_data in new_emails:
                        await event_bus.publish("new_message", email_data)
                        
            except Exception as e:
                logger.error(f"Gmail Ingestor error: {e}")
            
            # Poll every 60 seconds
            await asyncio.sleep(60)

    def fetch_new_emails(self):
        emails_found = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.username, self.password)
            mail.select("inbox")

            if self.last_seen_uid is None:
                # First run: get the highest UID and ignore past emails
                status, response = mail.uid('search', None, "ALL")
                if status == "OK" and response[0]:
                    uids = response[0].split()
                    if uids:
                        self.last_seen_uid = int(uids[-1])
                    else:
                        self.last_seen_uid = 0
                else:
                    self.last_seen_uid = 0
                mail.logout()
                return emails_found

            # Search for new UIDs strictly higher than what we've seen
            status, messages = mail.uid('search', None, f"UID {self.last_seen_uid + 1}:*")
            if status != "OK" or not messages[0]:
                mail.logout()
                return emails_found

            for uid_bytes in messages[0].split():
                uid = int(uid_bytes)
                if uid > self.last_seen_uid:
                    self.last_seen_uid = uid
                    
                status, data = mail.uid('fetch', uid_bytes, "(RFC822)")
                if status != "OK":
                    continue
                    
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode sender
                        sender = msg.get("From")
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                            
                        # Extract body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        logger.info(f"New Email from {sender}")
                        
                        emails_found.append({
                            "platform": "gmail",
                            "identifier": sender,
                            "text": f"Subject: {subject}\n\n{body}"
                        })

            mail.logout()
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            
        return emails_found

gmail_ingestor = GmailIngestor()
