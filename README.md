# 🛡️ AI Web Watchdog

A smart AI-powered web analysis tool that inspects any webpage and predicts whether it is a phishing/scam, blog, ecommerce, or informational site — with the help of GPT and web scraping.

---

## 🔍 Features

- 🌐 URL-based content scraping (title, description, full text)
- 🧠 GPT-4o powered content analysis
- ⚠️ Phishing detection with confidence score
- 🌍 Language detection
- 🗣️ Tone detection (fear, urgency, etc.)
- 🔎 Domain info extraction (`tldextract`)
- 🛑 Meta description fallback handling
- ✅ Clean React frontend interface

---

## 🛠️ Tech Stack

- **Frontend:** React.js (no Tailwind used)
- **Backend:** Python Flask
- **AI:** OpenAI GPT-4o Mini
- **Web Scraping:** BeautifulSoup + Requests
- **Extra Modules:** `langdetect`, `tldextract`, `flask-cors`

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-web-watchdog.git
cd ai-web-watchdog
