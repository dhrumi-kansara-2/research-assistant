
from langchain_core.messages import HumanMessage, SystemMessage
from state import ResearchState
from tools import search_duckduckgo
from llm import llm

'''
planner_node: take user's raw query and break it into 3-5 focused sub questions
'''
def planner_node(state: ResearchState) -> dict:
    query=state['query']
    messages=[
        SystemMessage(content="You are a research planner. Break the user query into exactly 3 sub-questions. Return them as a numbered list. Nothing else."),
        HumanMessage(content=f"Query: {query}")
    ]
    response=llm.invoke(messages)
    lines=response.content.strip().split("\n")
    sub_questions=[l.split(".",1)[-1] for l in lines if l.strip()]
    return {"sub_questions":sub_questions}

'''
researcher_node: takes every sub-question the planner produced and searches DuckDuckGo for each one
'''

def researcher_node(state: ResearchState) -> dict:
    sub_questions=state['sub_questions']
    all_results=[]
    for question in sub_questions:
        results=search_duckduckgo(question, max_results=5)
        all_results.extend(results)
    return {"search_results":all_results}