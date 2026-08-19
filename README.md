
- **Frontend** — single-file `index.html` (vanilla HTML/CSS/JS, zero build step), rendering the live chat thread with tool-call chips and result cards.
- **Backend** — Flask (`app.py`) driving the tool-calling loop (`agent.py`) against the Gemini API.
- **Tools** — plain Python functions in `tools/`, each paired with a function-calling schema so Gemini knows when to invoke it.

## 🛠️ Tech Stack

<div align="left">

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Gemini API](https://img.shields.io/badge/-Gemini_API-4285F4?style=flat-square&logo=googlegemini&logoColor=white)
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

</div>

- **LLM**: Google Gemini 2.5 Flash (function calling / tool use)
- **Backend**: Python, Flask, flask-cors
- **Frontend**: HTML, CSS, vanilla JavaScript
- **External API**: Open-Meteo (weather + geocoding, no key required)

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

Server starts on `http://localhost:5001`. Confirm it's alive:

```bash
curl http://localhost:5001/health
```

Then open `index.html` directly in your browser — it connects to the running backend automatically.

## 💬 Example Prompts
