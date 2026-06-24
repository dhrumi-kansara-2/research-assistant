# Research Assistant

A multi-agent research assistant built with LangGraph, Groq (Llama 3), DuckDuckGo, FastAPI, and React.

## How it works

A user query passes through 5 autonomous agents:

1. **Planner** — breaks the query into 2 focused sub-questions
2. **Researcher** — searches DuckDuckGo for each sub-question
3. **Synthesizer** — merges findings into a draft report
4. **Critic** — reviews the draft, loops back if gaps found
5. **Report** — produces a final structured research paper
 

## Tech Stack

| Layer | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq API (llama-3.3-70b-versatile) |
| Search | DuckDuckGo (no API key needed) |
| Backend | FastAPI + SSE streaming |
| Frontend | React + Vite + Tailwind CSS |
| Tracing | LangSmith (free tier) |

## Project Structure

```
research-assistant/
├── backend/
│   ├── state.py        # ResearchState TypedDict
│   ├── llm.py          # ChatGroq instance
│   ├── tools.py        # DuckDuckGo search wrapper
│   ├── nodes.py        # all 5 agent node functions
│   ├── graph.py        # StateGraph wiring and edges
│   ├── prompts.py      # system prompts for each agent
│   └── main.py         # FastAPI /research streaming endpoint
├── frontend/
│   └── src/
│       └── App.jsx     # React UI with EventSource streaming
├── .env.example
└── requirements.txt
```

## Setup

### Backend

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/research-assistant.git
cd research-assistant
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

4. Get your API keys:
   - Groq → https://console.groq.com
   - LangSmith → https://smith.langchain.com

5. Start the backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the dev server:
```bash
npm run dev
```

3. Open http://localhost:5173 in your browser

## Environment Variables

```bash
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=research-assistant
```

## API

| Method | Route | Description |
|---|---|---|
| GET | `/research?query=...` | Streams agent progress as SSE |
| GET | `/docs` | Auto-generated API documentation |