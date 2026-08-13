<div align="center">
  <img src="https://raw.githubusercontent.com/8nt0n/streamed/main/src/icon.png" alt="Streamed Icon" width="120" />
  <h1>Streamed</h1>
  <p><b>A painfully simple, lightweight media server for YOUR local network.</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
  [Live Demo](https://streamed-demo.netlify.app/) • [Video Demo](https://www.youtube.com/watch?v=EzZ0E9ARLbg)
</div>

---

![Screenshot](https://raw.githubusercontent.com/8nt0n/8nt0n/refs/heads/main/github%20desc/demo_screenshot.png)

## Overview

**Lets you stream your local video hoard from any web browser:** no subscriptions, no 3. party accounts, no nonsense. Just run it, and boom - your questionable anime collection is now wirelessly accessible.

> If Plex and Jellyfin feel too bloated for your needs, Streamed is the bare-minimum alternative you've been looking for.

### Why use Streamed?
1. 🔒 **Privacy first:** No Google Sign-In, no online bs, just your local media collection accesible for you 
2. 🚀 **Instant Setup:** Ready in < 5 minutes
3. 📱 **Compatible af:** Stream to any device with a modern web browser. 

---

## 🚀 Getting Started

### Option 1: Docker (Recommended for Homelabs)
The easiest way to get Streamed running on your home server.

**1. Clone and enter the project:**
```bash
git clone https://github.com/8nt0n/streamed.git
cd streamed
```
**2. Start the server:**
```bash
docker compose up -d --build
```
Thats it - streamed is now up and running on ``http://localhost:5000/``

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
