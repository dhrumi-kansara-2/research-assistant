import operator
from typing import Annotated, TypedDict 
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

class ResearchState(TypedDict):
    query: str #original user question
    sub_questions: list[str] #planner breaks query into these
    search_results: Annotated[list[str], operator.add] #appends across researcher runs
    draft: str
    critique: str
    final_report: str

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

graph_builder=StateGraph(ResearchState)