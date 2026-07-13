<div align="center">

# 🪐 Nova
### Your Omni-Channel AI Executive Assistant

*Nova quietly listens across your inbox and chats, catches anything that sounds like a meeting, and puts it on your calendar — before you even open the app.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama--3.3--70b-F55036?style=for-the-badge&logo=meta&logoColor=white)](https://groq.com/)
[![Google Calendar](https://img.shields.io/badge/Google%20Calendar-OAuth2-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white)](https://developers.google.com/calendar)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#-license)
[![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)](./ROADMAP.md)

[![SQLite](https://img.shields.io/badge/DB-SQLite%20%2B%20SQLAlchemy-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Telethon-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://docs.telethon.dev/)
[![Discord](https://img.shields.io/badge/Discord-discord.py-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![Gmail](https://img.shields.io/badge/Gmail-IMAP-EA4335?style=flat-square&logo=gmail&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/Webhooks-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Windows](https://img.shields.io/badge/Notifications-winotify-0078D6?style=flat-square&logo=windows&logoColor=white)](#)

</div>

---

## 🌟 Overview

**Nova** is a privacy-first, self-hosted executive assistant that runs quietly in the background of your life. It plugs into the channels you already use — Telegram, Discord, Gmail, Zoom, WhatsApp — and uses an LLM to figure out, in real time, whether a message is actually a scheduling request. If it is, Nova extracts the details, checks your calendar for conflicts, and syncs the event automatically, no copy-pasting required.

What makes Nova different from a generic "AI calendar bot" is that it's built around **consent and control** first. Nova never silently processes a stranger's message — an **Interactive Gatekeeper** pops up a native Windows notification asking you to Approve or Ignore before any unknown sender's content is touched by the LLM.

> 💡 **TL;DR** — Nova is the assistant that reads your messages so you don't have to, and only acts on people you've said "yes" to.

---

## ✨ Key Features

| Feature | What it does |
|---|---|
| 📥 **Multi-Channel Ingestion** | Simultaneously listens to Telegram, Discord DMs, Gmail (IMAP), and a Webhook Server (Zoom / WhatsApp) |
| 🚦 **Interactive Gatekeeper** | Unknown senders trigger a native Windows 10/11 toast notification with **Approve** / **Ignore** — nothing is processed without your say-so |
| 🧠 **Smart Event Extraction** | Groq's `Llama-3.3-70b-versatile` parses messages against a strict JSON schema to pull out title, start/end time, and location — hallucination-resistant by design |
| 📅 **Google Calendar Sync** | Extracted events are pushed straight into your calendar via OAuth2, no manual entry |
| ⚠️ **Double-Booking Detection** | Cross-checks your calendar before inserting an event and fires an urgent alert if you're already busy |
| ☀️ **Morning Briefing** | Every day at 10:00 AM, a cron job digests everything intercepted in the last 24 hours into one clean desktop notification |

---

## 🏗️ Architecture

Nova is built as a simple, linear pipeline: messages come in from many places, get funneled through a single decision point, get understood by an LLM, and finally trigger real-world actions.

```
┌─────────────────────────────────────────────────────────┐
│                      INGESTORS                          │
│                                                           │
│   Telegram      Discord       Gmail        Webhook       │
│  (Telethon)   (discord.py)    (IMAP)   (Zoom / WhatsApp) │
│      │             │             │             │         │
│      └─────────────┴──────┬──────┴─────────────┘         │
└──────────────────────────┼───────────────────────────────┘
                            ▼
                 ┌────────────────────┐
                 │  EVENT BUS / CORE   │
                 │                     │
                 │  Interactive        │
                 │  Gatekeeper         │───▶ 🔔 Windows Toast
                 │  (known/unknown     │      (Approve / Ignore)
                 │  sender check)      │
                 └──────────┬──────────┘
                            ▼ (approved messages only)
                 ┌────────────────────┐
                 │   LLM PROCESSOR     │
                 │                     │
                 │  Groq API           │
                 │  Llama-3.3-70b      │
                 │  → strict JSON      │
                 │    schema parsing   │
                 └──────────┬──────────┘
                            ▼
                 ┌────────────────────┐
                 │    CAPABILITIES     │
                 │                     │
                 │  • Google Calendar  │
                 │    Sync (OAuth2)    │
                 │  • Conflict / Double│
                 │    Booking Check    │
                 │  • Morning Briefing │
                 │    (10:00 AM cron)  │
                 │  • SQLite Event Log │
                 └────────────────────┘
```

**Flow in words:** every ingestor normalizes incoming messages into a common format → the core checks the sender against a whitelist (prompting you via notification if they're unknown) → approved messages go to Groq's Llama 3.3 70B for structured extraction → valid events are checked against your calendar for conflicts, logged to SQLite, and synced to Google Calendar.

---

## 🧰 Tech Stack

- **Language**: Python 3.10+
- **Database**: SQLite via SQLAlchemy ORM
- **AI / LLM**: [Groq API](https://groq.com/) — `llama-3.3-70b-versatile`
- **Integrations**: Telegram (`telethon`), Discord (`discord.py`), Gmail (IMAP), Zoom/WhatsApp (FastAPI webhooks), Google Calendar (OAuth2)
- **OS Notifications**: `winotify` (native Windows 10/11 toast notifications)
- **Background Jobs**: `apscheduler`

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- Windows 10/11 (required for native toast notifications via `winotify`)
- A [Groq API key](https://console.groq.com/keys)
- A Telegram API ID/Hash ([my.telegram.org](https://my.telegram.org))
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) enabled
- A Google Cloud project with the **Calendar API** enabled and OAuth2 credentials downloaded

### 2. Clone the repository

```bash
git clone https://github.com/<your-username>/nova.git
cd nova
```

### 3. Set up a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux (notifications will need an alternative on non-Windows)
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
# --- LLM ---
GROQ_API_KEY=your_groq_api_key_here

# --- Telegram ---
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash

# --- Discord ---
DISCORD_BOT_TOKEN=your_discord_bot_token

# --- Gmail (IMAP) ---
EMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# --- Webhook Server (Zoom / WhatsApp) ---
WEBHOOK_PORT=8000
```

### 6. Set up Google Calendar OAuth2

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and create/select a project.
2. Enable the **Google Calendar API**.
3. Create OAuth 2.0 credentials (Desktop App type).
4. Download the file and save it as **`credentials.json`** in the project root.
5. On first run, Nova will open a browser window for you to authorize access — this generates a local `token.json` for future runs.

### 7. Run Nova

```bash
python main.py
```

Or, if you're using the CLI tool for management tasks (whitelist, viewing logged events, etc.):

```bash
python cli.py
```

---

## ⚙️ Configuration Notes

- **Whitelist / Gatekeeper**: unknown senders are held for approval via a Windows toast notification. Approved senders are remembered so you're only asked once.
- **Morning Briefing**: fires automatically at 10:00 AM local time via `apscheduler` — no setup required beyond keeping Nova running.
- **Conflict Detection**: runs before every calendar insert; you'll get a distinct "you're double-booked" notification if a conflict is found.

---

## 🗺️ Roadmap

Nova is under active development. Planned features include Google Tasks / action-item syncing, a full web dashboard, Slack & Microsoft Teams ingestion, domain-based auto-approval, and automatic meeting agenda generation.

📄 **See the full plan in [`ROADMAP.md`](./ROADMAP.md)**

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues) or open a PR.

## 📄 License

This project is licensed under the **MIT License** — see the [`LICENSE`](./LICENSE) file for details.

---

<div align="center">

*Built to protect your time and your inbox — quietly, one message at a time.* ✨

</div>
