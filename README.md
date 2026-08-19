<div align="center">

# 🧰 Toolbox Agent Chat

**A tool-calling AI agent with a live chat UI — built for the Pleximus Inc. AI Hackathon**

Ask it a question, watch it decide which tool to reach for, and see the call — and the result — rendered right in the conversation.

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Gemini API](https://img.shields.io/badge/-Gemini_API-4285F4?style=flat-square&logo=googlegemini&logoColor=white)
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

</div>

---

## 🎥 Demo

| | |
|---|---|
| 🎬 **Full Demo** | [Watch on Google Drive](https://drive.google.com/file/d/1EW8zGfhj2f0OmWg7v04pbGUeSfHQXYaV/view?usp=drive_link) |
| ⚡ **Quick Walkthrough** | [Watch on Google Drive](https://drive.google.com/file/d/1Zo7gpqrgHQ9j_ISKPvZ19uKFjsYVu6IS/view?usp=drive_link) |

> Short on time? Start with the quick walkthrough — the full demo covers everything end to end.

---

## 📖 Overview

Toolbox Agent Chat is a minimal but complete example of **function calling** done right: a Gemini-powered agent that reasons about a user's message, decides whether it needs a tool, calls it, reads the result, and loops until it has a real answer — all visualized live in the chat thread with tool-call chips and result cards.

- **Frontend** — single-file `index.html` (vanilla HTML/CSS/JS, zero build step), rendering the live chat thread with tool-call chips and result cards.
- **Backend** — Flask (`app.py`) driving the tool-calling loop (`agent.py`) against the Gemini API.
- **Tools** — plain Python functions in `tools/`, each paired with a function-calling schema so Gemini knows when to invoke it.

## ✨ Features

- 🔁 **Full tool-calling loop** — chains multiple tool calls in one turn before replying
- 💬 **Live tool-call visualization** — every call and result renders as a chip/card in the chat, not a hidden log
- 🧮 **Safe expression evaluation** — AST-based calculator, no `eval()`
- 🌦️ **Real weather data** — geocodes a city and pulls live conditions from Open-Meteo, no API key required
- ⚖️ **Unit conversion** — length, weight, temperature, with common aliases (`meters`, `kilograms`, `Fahrenheit`, …)
- ✍️ **Text utilities** — word count, char count, case conversion, reverse
- 🚦 **Graceful rate-limit handling** — friendly message instead of a crash on the free Gemini tier

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| LLM | Google Gemini (function calling / tool use) |
| Backend | Python, Flask, flask-cors |
| Frontend | HTML, CSS, vanilla JavaScript |
| External API | Open-Meteo (weather + geocoding, no key required) |

## 🧩 Available Tools

| Tool | What it does |
|---|---|
| `calculate` | Evaluates a math expression (`+ - * / % **`) safely via AST parsing |
| `text_utility` | `word_count`, `char_count`, `uppercase`, `lowercase`, `reverse` on a string |
| `get_weather` | Looks up current temperature, humidity, and wind for a city |
| `convert_units` | Converts between length, weight, or temperature units |

## 🚀 Setup

**Prerequisites:** Python 3.10+, a free [Gemini API key](https://aistudio.google.com)

```bash
# 1. Clone the repo
git clone https://github.com/yawshyarr/pleximus_hackathon.git
cd pleximus_hackathon

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# then edit .env → GEMINI_API_KEY=your-key-here

# 5. Run the backend
python app.py
```

Server starts on `http://localhost:5010`. Confirm it's alive:

```bash
curl http://localhost:5010/health
```

Then open `index.html` directly in your browser — it connects to the running backend automatically.

## 💬 Example Prompts

- *"What's 18% of 245, then round it to the nearest whole number?"*
- *"What's the weather in Tokyo right now?"*
- *"Convert 5 miles to kilometers."*
- *"How many words are in this sentence, and reverse it too."*
- *"Convert 98.6°F to Celsius, then tell me the weather in that same rough climate somewhere in Europe."*

Each of these triggers one or more tool calls you can watch happen live in the chat.

## ✅ Edge Cases Handled

- Division by zero / invalid math expressions
- Unrecognized city names
- Invalid or mismatched unit categories (e.g. converting kg to meters)
- Empty or malformed API responses
- Gemini free-tier rate limits (5 requests/min) — surfaced as a friendly message instead of a 500

## 📁 Project Structure

```
toolbox-agent-chat/
├── app.py              # Flask server — exposes /health and /chat
├── agent.py            # Tool-calling loop against the Gemini API
├── tools/
│   ├── calculator.py
│   ├── text_utility.py
│   ├── weather.py
│   └── unit_converter.py
├── index.html           # Single-file chat frontend
├── requirements.txt
└── .env.example
```

## 👤 Author

**Yash Joshi** — built for the Pleximus Inc. AI Hackathon

<div align="center">

⭐ *If you found this project interesting, consider giving it a star!*

</div>
