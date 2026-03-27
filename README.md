# :stethoscope: HealthCheck AI — Symptom Checker

An AI-powered healthcare symptom checker that runs entirely on your local machine. Describe your symptoms and get educational insights on possible conditions and recommended next steps.

> :warning: **Disclaimer:** This tool is for educational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

## Features

- **AI Symptom Analysis** — Describe symptoms in natural language and receive possible conditions with explanations
- **Recommended Next Steps** — Get guidance on whether to see a doctor, visit urgent care, or try at-home care
- **Query History** — All past queries are saved locally in SQLite for reference
- **Fully Local** — Runs on your machine using Ollama + Llama 3.2. No API keys, no cloud, no data leaving your computer
- **Clean UI** — Professional single-page frontend with responsive design

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | [Ollama](https://ollama.com) + Llama 3.2 (local) |
| Backend | Python, FastAPI, httpx |
| Database | SQLite (via aiosqlite) |
| Frontend | Vanilla HTML/CSS/JS |

## Project Structure

```
├── backend/
│   ├── main.py          # FastAPI app, routes, CORS
│   ├── llm.py           # Ollama LLM integration
│   └── database.py      # SQLite query storage
├── frontend/
│   └── index.html       # Single-file UI (inline CSS/JS)
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcheck-ai.git
cd healthcheck-ai
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama & Pull the Model

**macOS (Homebrew):**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Then start the Ollama server and download the model:

```bash
# Start Ollama (keep this running in its own terminal)
ollama serve

# In a new terminal, pull the Llama 3.2 model (~2GB download)
ollama pull llama3.2
```

### 4. Start the Backend

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 5. Open the Frontend

```bash
open frontend/index.html
```

Or just double-click `frontend/index.html` in your file explorer to open it in your browser.

### 6. Use It

1. Type your symptoms in the text box (e.g. "headache, fever for 2 days, sore throat")
2. Click **Analyze Symptoms**
3. Wait 10-15 seconds for the AI response
4. View possible conditions and recommended next steps
5. Click **Load History** to see your past queries

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/check` | Analyze symptoms — send `{"symptoms": "your text"}` |
| GET | `/api/history` | Retrieve past queries |

### Example API Call

```bash
curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "headache and fever for 2 days"}'
```

## Configuration

You can customize the model by setting environment variables in a `.env` file:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.2` | Model to use (try `llama3.1`, `mistral`, etc.) |
| `DB_PATH` | `symptom_checker.db` | SQLite database file path |

## License

MIT
