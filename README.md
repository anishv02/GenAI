# 🌐 Website Summarizer

An AI-powered website summarizer with a modern React frontend and Flask backend.

## ✨ Features

- 🎨 Modern dark theme UI with glassmorphism effects
- 🤖 AI-powered summarization using Ollama (local) or Groq (cloud)
- 📱 Fully responsive design
- ⚡ Fast and lightweight

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Ollama installed with `gemma3` model

### 1. Clone the repository
```bash
git clone https://github.com/anishv02/GenAI.git
cd GenAI
```

### 2. Setup Backend
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd frontend
npm install
cd ..
```

### 4. Start Ollama
```bash
ollama serve
```

### 5. Run the App
**Terminal 1 - Backend:**
```bash
source .venv/bin/activate
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Open http://localhost:3000 🎉

---

## ☁️ Cloud Deployment Guide

### Step 1: Get a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Go to **API Keys** → **Create API Key**
4. Copy and save your API key

---

### Step 2: Deploy Backend to Render.com (Free)

1. Go to [render.com](https://render.com) and sign up/login
2. Click **New** → **Web Service**
3. Connect your GitHub account and select the `GenAI` repository
4. Configure the service:
   - **Name:** `website-summarizer-api`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn api:app`

5. Add **Environment Variables** (click "Add Environment Variable"):
   - `USE_CLOUD` = `true`
   - `GROQ_API_KEY` = `your_groq_api_key_here`

6. Click **Create Web Service**
7. Wait for deployment (2-3 minutes)
8. Copy your backend URL (e.g., `https://website-summarizer-api.onrender.com`)

---

### Step 3: Deploy Frontend to Vercel (Free)

1. Go to [vercel.com](https://vercel.com) and sign up/login with GitHub
2. Click **Add New** → **Project**
3. Import the `GenAI` repository
4. Configure the project:
   - **Framework Preset:** `Create React App`
   - **Root Directory:** Click **Edit** → Select `frontend`

5. Expand **Environment Variables** and add:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://your-backend-url.onrender.com` (from Step 2)

6. Click **Deploy**
7. Wait for deployment (1-2 minutes)
8. Your app is live! 🎉

---

## 📁 Project Structure

```
GenAI/
├── api.py              # Flask backend API
├── scraper.py          # Web scraper utility
├── requirements.txt    # Python dependencies
├── Procfile            # Render deployment config
├── .gitignore          # Git ignore rules
├── .env                # Local environment variables
└── frontend/           # React application
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── App.js      # Main React component
    │   ├── index.js    # Entry point
    │   └── index.css   # Styles
    ├── package.json
    └── .env.production # Production environment
```

---

## 🔧 Environment Variables

### Backend (.env or Render)
| Variable | Description | Default |
|----------|-------------|---------|
| `USE_CLOUD` | Use cloud API instead of Ollama | `false` |
| `GROQ_API_KEY` | Your Groq API key | - |
| `PORT` | Server port | `5001` |

### Frontend (.env.production or Vercel)
| Variable | Description |
|----------|-------------|
| `REACT_APP_API_URL` | Backend API URL |

---

## 🛠️ Tech Stack

- **Frontend:** React 18, CSS3 (Custom Properties, Flexbox, Grid)
- **Backend:** Flask, Flask-CORS, Gunicorn
- **AI:** Ollama/Gemma3 (local) or Groq/Llama-3.1 (cloud)
- **Scraping:** BeautifulSoup4, Requests

---

## 📄 License

MIT License - feel free to use this project for learning and building!
