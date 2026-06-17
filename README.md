# Research Assistant

A mutli-agent research assitant built with LangGraph, Groq(Llama 3), DuckDuckGo Search, FastAPI, and React

## How it works

1. **Planner**: breaks the query into 3-5 focused sub-questions
2. **Resarcher**: searches DuckDuckGo for sub-question
3. **Sythesizer**: merges all findings into a coherent draft
4. **Critic**: evalute the draft and loops back if gaps are found
5. **Report**: returns a final card, structured report


## Tech stack

| Layer | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq API (Llama 3 8b) |
| Search | DuckDuckGo (no API key) |
| Backend | FastAPI + SSE streaming |
| Frontend | React + Tailwind |
| Tracing | LangSmith (free tier) |

## Project structure

``` 
research-assistant/

├── backend/
│   ├── graph.py       # StateGraph, node wiring, edge logic
│   ├── nodes.py       # all 5 agent node functions
│   ├── tools.py       # DuckDuckGo search wrapper
│   ├── main.py        # FastAPI /research streaming endpoint
│   └── prompts.py     # system prompts for each agent
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
├── .env.example
└── requirements.txt
```

## Running the backend
```bash
cd backend
pip install -r requirements.txt
python graph.py
\
```

 