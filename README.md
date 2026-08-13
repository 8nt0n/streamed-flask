<div align="center">
  <img src="https://raw.githubusercontent.com/8nt0n/streamed/main/src/icon.png" alt="Streamed Icon" width="120" />
  <h1>Streamed</h1>
  <p><b>A painfully simple, lightweight media server for your local network.</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
  [Live Demo](https://streamed-demo.netlify.app/) • [Video Demo](https://www.youtube.com/watch?v=EzZ0E9ARLbg)
</div>

---

![Screenshot](https://raw.githubusercontent.com/8nt0n/8nt0n/refs/heads/main/github%20desc/demo_screenshot.png)

## Overview

Streamed is a ridiculously simple media server that lets you stream your local video hoard from a web browser. No subscriptions, no user accounts, no heavy databases, no nonsense. Just run it, and boom—your questionable anime collection is now wirelessly accessible.

If Plex and Jellyfin feel too bloated for your needs, Streamed is the bare-minimum alternative you've been looking for.

### Why use Streamed?
- 🪶 **Stupidly Lightweight:** No heavy database (uses a simple static `.js` file).
- 🚀 **Instant Setup:** Point it at a folder and go.
- 📱 **Browser-First:** Stream to any device with a modern web browser.
- 🛠️ **Zero Dependencies:** Written in Python/Flask. 

---

## 🚀 Getting Started

### Option 1: Docker (Recommended for Homelabs)
The easiest way to get Streamed running on your home server.

```yaml
version: '3.8'
services:
  streamed:
    image: ghcr.io/8nt0n/streamed:latest # Or build from source
    container_name: streamed
    ports:
      - "5000:5000"
    volumes:
      - /path/to/your/movies:/app/media
    restart: unless-stopped

```

### Option 2: Bare Metal (Python)

If you want to run it directly via Python on Windows, Mac, or Linux:

```bash
git clone https://github.com/8nt0n/streamed.git
cd streamed-flask/

# Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install & Run
pip install -r requirements.txt
flask run --host=0.0.0.0

```

---

## 📁 How to Add Media

Ill write that later 😅

---

## 🛠️ Development & Contributing

Pull requests are highly encouraged!

**A note on `thanks.py`:**
What’s it do? Nothing. It just says:

```text
No problem!

```

Run it after fixing a frustrating bug. It is your emotional support script.

---

## License

MIT. Do what you want. Just don’t blame me if your server catches fire.
