# LeadIntel — AI Cold Email Intelligence

## Prerequisites

- Python 3.x installed
- VS Code with integrated terminal
- Valid API keys:
  - **SERP_API_KEY** — from [serpapi.com](https://serpapi.com)
  - **GEMINI_API_KEY** — from [Google AI Studio](https://aistudio.google.com)

---

## One-Time Setup (First Time Only)

Open VS Code terminal (`Ctrl + backtick`) and run:

```powershell
cd c:\Users\Imapro\Desktop\abc\LeadIntel
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install streamlit requests google-generativeai pandas openpyxl
```

---

## Run the Project

Every time you want to run the app, open VS Code terminal and paste:

```powershell
& .\.venv\Scripts\Activate.ps1; python -m streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

Press **Ctrl + C** in the terminal to stop the app.

---

## Project Structure

```
LeadIntel/
├── app.py          # Main application file
├── README.md       # This file
└── .venv/          # Python virtual environment
```

---

## How It Works

1. **Enter Business** — Type a business name and city
2. **AI Scrapes Reviews** — Pulls Google Maps reviews via SerpAPI
3. **Extracts Pain Points** — Gemini AI analyzes sentiment, pain points & praises
4. **Custom Cold Email** — Generates 3 personalized cold email variations

---

## Bulk Analysis

Upload a CSV/Excel file with columns `name` (or `business`) and `city` (or `location`) via the sidebar to analyze multiple businesses at once.

---

Built by **imaPRO** · LeadIntel v1.0
