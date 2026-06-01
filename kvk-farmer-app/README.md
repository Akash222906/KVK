# 🌾 KVK Krishak Seva — Farmer Advisory System

AI-powered farm advisory app for West Bengal farmers with crop recommendations, PDF reports, chatbot (KrishiBot), voice assistant, market prices, and government schemes.

---

## 🚀 Steps to Run

### 1. Get a Free Groq API Key
- Go to https://console.groq.com
- Sign up → API Keys → Create Key (starts with `gsk_...`)

---

### 2. Start the Backend

**Mac / Linux:**
```bash
cd kvk-farmer-app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt --only-binary=:all:
cp .env.example .env
# Open .env and paste your GROQ_API_KEY
python app.py
```

**Windows (PowerShell):**
```powershell
cd kvk-farmer-app\backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt --only-binary=:all:
copy .env.example .env
notepad .env    # paste your GROQ_API_KEY, save
python app.py
```

> If you get a PowerShell execution policy error:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

✅ Backend starts at http://localhost:5000 and auto-trains ML models on first run (~30–60 sec).

---

### 3. Start the Frontend

Open a **new terminal**:
```bash
cd kvk-farmer-app/frontend
npm install
npm start
```

✅ App opens at http://localhost:3000

---

### 🐳 OR Run with Docker (One Command)
```bash
cd kvk-farmer-app
echo "GROQ_API_KEY=gsk_your_key_here" > .env
docker-compose up --build
```

---

## 🌟 Features

| Feature | Details |
|---------|---------|
| 🤖 KrishiBot AI | Groq LLaMA 3.3 70B · English + Bengali + Hindi |
| 🎙️ Voice Assistant | Speech-to-Text input + Text-to-Speech output |
| 🌾 Crop Recommendation | Random Forest ML · Trained on WB crop data |
| 📦 Yield Prediction | Gradient Boosting Regressor |
| 🐛 Pest Risk Assessment | Rule-based agronomic engine |
| 📄 PDF Farm Reports | ReportLab — weather, ML, market, schemes |
| 📈 Market Prices | 8 crops · MSP vs market price + trends |
| 🏛️ Govt Schemes | PM-KISAN, Krishak Bandhu, KCC, PMFBY, PM-KUSUM |
| 🗺️ District Support | All 20 West Bengal districts |

---

## 🏗️ Project Structure

```
kvk-farmer-app/
├── backend/
│   ├── app.py                  # Main Flask app
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── data.py             # /api/data/* 
│   │   ├── report.py           # /api/report/*
│   │   └── chatbot.py          # /api/chat/*
│   └── services/
│       ├── ml_service.py       # ML models
│       ├── data_service.py     # Weather, market, schemes
│       └── report_service.py   # PDF builder
└── frontend/
    ├── package.json
    └── src/
        ├── App.js
        ├── index.css
        ├── services/api.js
        └── pages/
            ├── Dashboard.js
            ├── ReportGenerator.js
            ├── Chatbot.js       # With voice assistant
            ├── MarketPrices.js
            └── Schemes.js
```

---

## ⚠️ Common Fixes

| Error | Fix |
|-------|-----|
| `numpy` install fails | `pip install numpy --only-binary=:all:` |
| `source` not recognized (Windows) | Use `venv\Scripts\Activate.ps1` |
| Chatbot shows `(fallback)` | Set `GROQ_API_KEY` in `.env` and restart backend |
| Port 5000 in use | `netstat -ano \| findstr :5000` then `taskkill /PID <n> /F` |
| `groq` proxies error | `pip install groq --upgrade --no-cache-dir` |
| Python 3.13 numpy error | Use Python 3.11: `py -3.11 -m venv venv` |

---

## 📞 Support
Contact your nearest **Krishi Vigyan Kendra (KVK)** office or visit **icar.org.in**
