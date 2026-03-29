# 📈 AI-Powered Indian Stock Market Analyzer
### ET AI Hackathon 2026 — Problem Statement 6: AI for the Indian Investor

> Turning live NSE data into actionable, money-making decisions for 14 crore+ Indian retail investors.

---

## 🚀 Live Demo
> Run locally using the steps below

**GitHub:** https://github.com/NAREN-105/ET-GEN-AI

---

## 🧠 Problem It Solves
India has 14 crore+ demat accounts, but most retail investors are:
- Reacting to tips and rumors
- Unable to read technical charts
- Missing corporate filings and signals
- Making decisions on gut feel

This app gives every Indian investor **professional-grade AI analysis** — free, simple, and in plain English.

---

## ✨ Features
| Feature | Description |
|---|---|
| 📊 Live NSE Data | Real-time prices for 8 major Indian stocks via yfinance |
| 📉 Technical Indicators | RSI, MACD, 200-Day Moving Average — auto calculated |
| 🤖 AI Analysis | LLaMA 3.3 70B gives BUY/SELL/HOLD signals in plain English |
| 💬 AI Chat Assistant | Ask anything about the stock — instant AI answers |
| 🌙 Dark Theme UI | Clean, professional interface built with Streamlit |
| 📈 Price Chart | 1-year interactive chart with 200 DMA overlay |

---

## 🛠️ Tech Stack
```
Frontend     → Streamlit
Data Source  → yfinance (Yahoo Finance API)
AI / LLM     → Groq API + LLaMA 3.3 70B
Indicators   → ta (Python Technical Analysis library)
Charts       → Plotly
Secrets      → Streamlit Secrets Manager
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/NAREN-105/ET-GEN-AI.git
cd ET-GEN-AI
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your FREE Groq API Key
- Go to https://console.groq.com
- Sign up → API Keys → Create API Key
- Copy the key

### 4. Add your API key
Create a file: `.streamlit/secrets.toml`
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📦 Requirements
```
streamlit
yfinance
ta
groq
plotly
```

---

## 🏗️ How It Works
```
User selects stock
       ↓
yfinance fetches 1 year of live NSE data
       ↓
ta library calculates RSI + MACD + 200 DMA
       ↓
Groq LLaMA 3.3 70B generates AI analysis
       ↓
Streamlit displays chart + metrics + AI signal
       ↓
User can chat with AI for follow-up questions
```

---

## 📊 Stocks Covered
- Reliance Industries
- TCS
- HDFC Bank
- Infosys
- Wipro
- ICICI Bank
- Kotak Mahindra Bank
- Bajaj Finance

---

## 🎯 AI Output Format
Every stock analysis includes:
1. **WHAT IS HAPPENING** — 2-line simple summary
2. **SIGNAL** — STRONG BUY / BUY / HOLD / CAUTION / AVOID
3. **WHY** — 3 bullet point reasons
4. **RISK LEVEL** — Low / Medium / High
5. **SIMPLE ADVICE** — 1-line actionable tip

---

## 🔮 Future Roadmap
- [ ] 50+ NSE stocks coverage
- [ ] Portfolio tracker
- [ ] Price alerts via WhatsApp/Email
- [ ] News sentiment analysis
- [ ] Mobile app (Android/iOS)
- [ ] Tamil & Hindi language support

---

## 👨‍💻 Built For
**ET AI Hackathon 2026** — Problem Statement 6: AI for the Indian Investor  
Built with ❤️ for India's retail investors
