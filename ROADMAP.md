# Nova - AI Executive Assistant Roadmap

## Currently Implemented
- **Omni-Channel Ingestion**: Telegram, Discord, Gmail (IMAP), and Webhook Server (Zoom/WhatsApp).
- **AI Event Extraction**: Powered by Groq API (Llama 3 70B) with strict JSON schema parsing to extract meeting titles, times, and locations.
- **Google Calendar Syncing**: Full OAuth2 integration to automatically sync extracted events.
- **Interactive Gatekeeper**: Native Windows 10/11 Notifications that ask for permission before processing messages from unknown senders. 
- **Double Booking Prevention**: Checks Google Calendar for conflicts before adding new events and alerts the user.
- **Morning Briefing**: Automated 10:00 AM daily digest of all events intercepted in the last 24 hours.

## Future Implementations / Planned Features
1. **Task & Action Item Extraction (Google Tasks Sync)**
   - *Status*: Postponed.
   - *Description*: Expand the Groq extraction prompt to look for To-Dos and Action Items (e.g., "Book a flight on 30th Nov") instead of just calendar meetings, and sync them to Google Tasks or Notion.

2. **Full UI Dashboard**
   - *Status*: Pending.
   - *Description*: Replace the `cli.py` with a lightweight local web dashboard (e.g., FastAPI + React) to visually manage the whitelist, view the event database, and configure rules.

3. **Slack / Microsoft Teams Ingestion**
   - *Status*: Pending.
   - *Description*: Expand the `webhook_server.py` to natively support Slack Events API and MS Teams webhooks for enterprise use.

4. **Domain-Based Auto-Approval**
   - *Status*: Pending.
   - *Description*: Allow whitelisting of entire domains (e.g., `@google.com`) so any coworker from that domain automatically bypasses the Interactive Gatekeeper.

5. **Meeting Context / Agenda Generation**
   - *Status*: Pending.
   - *Description*: Automatically append a generated meeting agenda or context summary into the Google Calendar Event description based on the conversation history.
