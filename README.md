
- **Frontend**: single-file `index.html` (vanilla HTML/CSS/JS, no build step) — renders the chat thread, tool-call chips, and tool result cards live as the agent works.
- **Backend**: Flask (`app.py`) + the tool-calling loop (`agent.py`), talking to the Gemini API.
- **Tools**: plain Python functions in `tools/`, each with a matching function-calling schema so Gemini knows when to invoke them.

## Tech Stack

- **LLM**: Google Gemini 2.5 Flash (function calling / tool use)
- **Backend**: Python, Flask, flask-cors
- **Frontend**: HTML, CSS, vanilla JavaScript
- **External API**: Open-Meteo (weather + geocoding, no key required)

## Setup

**Prerequisites:** Python 3, a free [Gemini API key](https://aistudio.google.com)

1. Clone the repo and enter the project folder
```bash
   git clone https://github.com/yawshyarr/pleximus_hackathon.git
   cd pleximus_hackathon
```

2. Create a virtual environment and install dependencies
```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

3. Add your API key
```bash
   cp .env.example .env
   # then edit .env and set GEMINI_API_KEY=your-key-here
```

4. Run the backend
```bash
   python app.py
```
   Server starts on `http://localhost:5001`. Confirm it's up:
```bash
   curl http://localhost:5001/health
```

5. Open the frontend
   Open `index.html` directly in your browser — it connects to the running backend automatically.

## Example prompts to try

- "What is 12 * (45 + 18)?"
- "What's the weather in Mumbai?"
- "Convert 100 F to Celsius"
- "How many words are in this sentence: Artificial Intelligence is revolutionizing workflows"

## Edge cases handled

- Division by zero / invalid math expressions
- Unrecognized city names
- Invalid or mismatched unit categories (e.g. converting kg to meters)
- Empty or malformed API responses

## Author

Built by Yash Joshi for the Pleximus Inc. AI Hackathon.
