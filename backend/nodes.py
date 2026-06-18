
from langchain_core.messages import HumanMessage, SystemMessage
from state import ResearchState
from tools import search_duckduckgo
from llm import llm
import time

'''
planner_node: take user's raw query and break it into 3-5 focused sub questions
'''
def planner_node(state: ResearchState) -> dict:
    query=state['query']
    messages=[
        SystemMessage(content="You are a research planner. Break the user query into exactly 2 sub-questions. Return them as a numbered list. Nothing else."),
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

'''
synthesizer_node: reads all the raw results the Researcher collected and mergers them into one coherent draft report
'''
def synthesizer_node(state: ResearchState)->dict:
    search_results="\n\n".join(state["search_results"])
    time.sleep(15)       # wait before hitting LLM again
    messages=[
        SystemMessage(content="You are a research writer. Synthesize the search results into a coherent, well structured draft report. Include key findings and cite the URLs as sources."),
        HumanMessage(content=f"Original query: {state['query']}\n\nSearch results:\n{search_results}")
    ]
    response=llm.invoke(messages)
    return {"draft": response.content}

'''
critic_node: reads the draft and decides if it's good enough or if the researcher needs to run again to fill gaps
'''

def critic_node(state: ResearchState)->dict:
    message=[
        SystemMessage(content="""You are a research critique. Review the draft report and check for:
                      1. Missing information or gaps.
                      2. Unsupported claims.
                      3. Areas needing more research

                      if the graph is good enough reply with exactly: APPROVED
                      if it needs more research reply with: NEEDS_RESEARCH: <specific gap>"""),
        HumanMessage(content=f"Draft report:\n{state['draft']}")
    ]
    response=llm.invoke(message)
    return {"critique_node":response.content}

'''
report_node: final step. Takes the draft and polishes it into clean, cited, structured final report
'''
def report_node(state: ResearchState)->dict:
    messages=[
        SystemMessage(content="""You are an academic research editor.
        Write a concise research paper with these sections:

        # Title
        ## Abstract (100 words max)
        ## 1. Introduction (100 words max)
        ## 2. Key Findings (bullet points only)
        ## 3. Conclusion (100 words max)
        ## References (URLs only)

        Be concise. No fluff. Stick to word limits strictly."""),
        HumanMessage(content=f"""Query: {state['query']}
        Draft: {state['draft']}
        Crituqe: {state['critique']} 
        """)
    ]
    response=llm.invoke(messages)
    return {"final_report":response.content}
