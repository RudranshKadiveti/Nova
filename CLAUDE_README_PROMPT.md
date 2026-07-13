# Prompt for Claude to Generate README.md

Hey Claude, please generate a highly professional, engaging, and detailed `README.md` for my GitHub repository called **Nova**.

## Project Context
Nova is an **Omni-Channel AI Executive Assistant** built in Python. Its goal is to passively listen to my communication channels, intercept scheduling requests or meetings, parse them intelligently using LLMs, and push them to my Google Calendar, all while aggressively protecting my privacy.

## Tech Stack
- **Language**: Python 3.10+
- **Database**: SQLite (SQLAlchemy ORM)
- **AI/LLM**: Groq API (Llama-3.3-70b-versatile)
- **Integrations**: Telegram (`telethon`), Discord (`discord.py`), Gmail (IMAP), Zoom/WhatsApp (FastAPI Webhooks), Google Calendar (OAuth2).
- **OS Notifications**: `winotify` for native Windows 10/11 Toast Notifications.
- **Background Jobs**: `apscheduler` for cron tasks.

## Key Features to Highlight
1. **Multi-Channel Ingestion**: It simultaneously listens to Telegram, Discord DMs, Gmail, and Webhooks.
2. **Interactive Gatekeeper**: To prevent spam, any message from an unknown sender triggers a native Windows Notification on my desktop with an "Approve" or "Ignore" button. It only processes their data if I click Approve!
3. **Smart Event Extraction**: Uses Groq (Llama 3) with strict JSON schema instructions to extract event title, start time, end time, and location, dropping hallucinations.
4. **Google Calendar Sync**: Pushes extracted events directly to Google Calendar.
5. **Conflict Detection**: Checks Google Calendar before adding an event and fires an urgent notification if I am double-booked.
6. **Morning Briefing**: A cron job runs every day at 10:00 AM, summarizes all intercepted events from the last 24 hours, and pushes a daily digest to my desktop via a notification.

## Instructions for README
Please structure the README with:
- A catchy title and badges.
- A high-level overview.
- A diagram or bulleted list of the Architecture (Ingestors -> Event Bus -> LLM Processor -> Capabilities/Calendar).
- Setup Instructions (requires setting up `.env` with `GEMINI_API_KEY`, `TELEGRAM_API_ID`, `DISCORD_BOT_TOKEN`, `EMAIL_ADDRESS`, `GMAIL_APP_PASSWORD` and getting a `credentials.json` for Google Calendar OAuth).
- A section linking to the `ROADMAP.md` for future features (like Task Extraction).

Make it sound cutting-edge, professional, and easy to understand!
