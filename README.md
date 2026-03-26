# Auto Publisher 🎬🤖

> A fully automated content creation and YouTube publishing engine. Generates educational videos locally — no external AI APIs needed — and uploads them to YouTube on a 2-hour schedule. Built for Ubuntu 22.04.

---

## ✨ What It Does

Auto Publisher runs a complete end-to-end pipeline on a loop:

1. **Picks a random topic** from a 15,000+ topic database across 15 categories
2. **Generates a voiceover** using local TTS (espeak / pyttsx3)
3. **Creates a video** with animated text slides synced to audio (moviepy)
4. **Uploads to YouTube** automatically via Google Data API v3
5. **Repeats every 2 hours** via built-in scheduler — no cron needed

Zero manual intervention after initial setup.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| **15,000+ Topic Database** | Covers cybersecurity, finance, business, tech, health, science, psychology, and more |
| **Local TTS Audio** | Uses espeak (primary) and pyttsx3 (fallback) — no cloud API costs |
| **Auto Video Generation** | Creates 1080p slides with fade effects synced to audio duration |
| **YouTube Auto-Upload** | Uploads with title, description, tags, and category via OAuth2 |
| **Self-Installing** | Auto-detects and installs missing Python dependencies on first run |
| **2-Hour Scheduler** | Built-in loop keeps publishing continuously without cron jobs |

---

## 📋 Prerequisites

- **Ubuntu 22.04** (recommended)
- **Python 3.8+**
- **espeak** (for TTS audio generation)
- **ImageMagick** (for moviepy text rendering)
- **Google Cloud Project** with YouTube Data API v3 enabled
- `client_secrets.json` from Google Cloud Console

### Install System Dependencies

```bash
sudo apt update
sudo apt install -y espeak imagemagick python3-pip
```

---

## 🔑 Google API Setup

Before running, you need YouTube API credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Navigate to **APIs & Services** → **Enable APIs**
4. Search and enable **YouTube Data API v3**
5. Go to **APIs & Services** → **Credentials**
6. Click **Create Credentials** → **OAuth 2.0 Client ID**
7. Select **Desktop App** as application type
8. Download the JSON file and rename it to `client_secrets.json`
9. Place `client_secrets.json` in the same directory as `auto_publisher.py`

---

## 🛠 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vikrantproject/auto-publisher
cd auto-publisher
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your Credentials

Place your `client_secrets.json` in the project root:

```
auto-publisher/
├── auto_publisher.py
├── client_secrets.json     ← place here
├── requirements.txt
└── README.md
```

### 4. Run the Publisher

```bash
python auto_publisher.py
```

On first run, a browser window will open for Google OAuth authorization. After approving, credentials are saved to `token.pickle` for all future runs — no login needed again.

---

## 🎮 How the Pipeline Works

```
Startup
   │
   ▼
Auto-install missing dependencies
   │
   ▼
Load 15,000+ topic database
   │
   ╔══════════════════════════════╗
   ║        EVERY 2 HOURS         ║
   ║                              ║
   ║  1. Pick random topic        ║
   ║  2. Generate TTS audio .wav  ║
   ║  3. Create video slides .mp4 ║
   ║  4. Upload to YouTube        ║
   ║  5. Wait for next cycle      ║
   ╚══════════════════════════════╝
```

---

## 📂 Project Structure

```
auto-publisher/
├── auto_publisher.py       # Main engine — all phases in one script
├── client_secrets.json     # Google OAuth credentials (never commit this)
├── token.pickle            # Auto-generated after first auth (never commit)
├── requirements.txt        # Python dependencies
├── output/                 # Auto-created — stores generated files
│   ├── audio_YYYYMMDD_HHMMSS.wav
│   └── video_YYYYMMDD_HHMMSS.mp4
└── README.md
```

---

## 🗂 Topic Categories

The built-in database covers **15,000+ topics** across these categories:

| Category | Examples |
|---|---|
| Cybersecurity | SQL Injection, Phishing, Zero-day Exploits, Ransomware |
| Finance | Compound Interest, Index Funds, Tax-Advantaged Accounts |
| Business | Cash Flow, Product-Market Fit, Pricing Strategy |
| Technology | AI, Blockchain, Cloud Computing, 5G, Quantum Computing |
| Health | Sleep, Gut Health, Mental Health, Preventive Care |
| Science | CRISPR, Climate Change, Black Holes, Neuroplasticity |
| Personal Development | Growth Mindset, Habit Formation, Emotional Intelligence |
| Cryptocurrency | Bitcoin, Ethereum, DeFi |
| Marketing | Content Marketing, Email Marketing, Social Media |
| Productivity | Pomodoro, Eisenhower Matrix, Getting Things Done |
| Psychology | Cognitive Biases, Dopamine, Neuroplasticity |
| Entrepreneurship | MVP, Bootstrapping, Pivoting |
| Leadership | Servant Leadership, Transformational Leadership |
| Investing | Value Investing, Growth Investing, REITs |

---

## 🚢 Deployment

### Run in Background (Linux)

```bash
nohup python auto_publisher.py > publisher.log 2>&1 &
```

### Run with Screen

```bash
screen -S autopublisher
python auto_publisher.py
# Detach: Ctrl+A then D
# Reattach: screen -r autopublisher
```

### Run with PM2

```bash
pm2 start auto_publisher.py --interpreter python3 --name auto-publisher
pm2 save
pm2 startup
```

---

## ⚙️ Configuration

Tweak these values directly in `auto_publisher.py`:

| Setting | Default | Description |
|---|---|---|
| Upload interval | `2 hours` | How often a new video is published |
| Video resolution | `1920x1080` | Output video dimensions |
| Privacy status | `unlisted` | YouTube visibility (`public`, `private`, `unlisted`) |
| TTS speed | `150 wpm` | Voice speed for audio generation |
| Category ID | `27` | YouTube category (27 = Education) |

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes and legitimate content automation** only. Users are responsible for ensuring all published content complies with [YouTube's Terms of Service](https://www.youtube.com/t/terms) and Community Guidelines. Do not use this tool to publish spam, misleading, or policy-violating content.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

<p align="center">Set it once. Publish forever. 🚀</p>
