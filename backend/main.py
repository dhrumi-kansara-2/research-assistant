from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from graph import graph
import json


app=FastAPI(title="Research Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str


async def research_stream(query: str):
    initial_state={
        "query":query,
        "sub_questions":[],
        "search_results":[],
        "draft":[],
        "critique":[],
        "final_report":[], 
    }
    for chunk in graph.stream(initial_state, config={"recursion_limit":10}):
        node_name=list(chunk.keys())[0]
        node_data=chunk[node_name]
        payload={"node":node_name,"data":node_data}
        yield f"data: {json.dumps(payload)}\n\n"

@app.post("/research")
async def research(request: ResearchRequest):
    return StreamingResponse(
        research_stream(request.query),
        media_type="text/event-stream"
    )


@app.get("/research")
async def research_get(query: str=""):
    if not query.strip():
        return {"error": "Query can not be empty"}
    return StreamingResponse(
        research_stream(query),
        media_type="text/event-stream"
    )