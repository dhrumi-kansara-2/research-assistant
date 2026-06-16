import operator
from typing import Annotated, TypedDict 

class ResearchState(TypedDict):
    query: str #original user question
    sub_questions: list[str] #planner breaks query into these
    search_results: Annotated[list[str], operator.add] #appends across researcher runs
    draft: str
    critique: str
    final_report: str
