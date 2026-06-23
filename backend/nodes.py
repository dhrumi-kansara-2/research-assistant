
from langchain_core.messages import HumanMessage, SystemMessage
from state import ResearchState
from tools import search_duckduckgo
from llm import llm
import time
from prompts import PLANNER_PROMPT, SYNTHESIZER_PROMPT, CRITIC_PROMPT, REPORT_PROMPT

'''
planner_node: take user's raw query and break it into 3-5 focused sub questions
'''
def planner_node(state: ResearchState) -> dict:
    time.sleep(5)
    query=state['query']
    messages=[
        SystemMessage(content=PLANNER_PROMPT),
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
    time.sleep(5)
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
    time.sleep(15)       # wait before hitting LLM again
    search_results="\n\n".join(state["search_results"])
    search_results=search_results[:1500] 
    messages=[
        SystemMessage(content=SYNTHESIZER_PROMPT),
        HumanMessage(content=f"Original query: {state['query']}\n\nSearch results:\n{search_results}")
    ]
    response=llm.invoke(messages)
    # print("------------------------------")
    # print("synthesizer node: ")
    # print(response.content)
    # print("------------------------------")
    return {"draft": response.content}

'''
critic_node: reads the draft and decides if it's good enough or if the researcher needs to run again to fill gaps
'''
# MAX_RESEARCH_LOOPS = 2
def critic_node(state: ResearchState) -> dict:
    time.sleep(5)
    # print('------------------------------')
    # print('critic node',state['draft'])
    # print('------------------------------')
    messages = [
        SystemMessage(content=CRITIC_PROMPT),
        HumanMessage(content=f"Draft:\n{state['draft'][:500]}")
    ]
    response = llm.invoke(messages)
    return {"critique": response.content}

'''
report_node: final step. Takes the draft and polishes it into clean, cited, structured final report
'''
def report_node(state: ResearchState)->dict:
    time.sleep(5)
    messages=[
        SystemMessage(content=REPORT_PROMPT),
        HumanMessage(content=f"""Query: {state['query']}
        Draft to polish:
        {state['draft']}

        Critique received: {state['critique']}

        Remember: write ONLY about the query topic above.""")
    ]
    response=llm.invoke(messages)
    print("----------------------------")
    print("final_report",response.content)
    print("----------------------------")

    return {"final_report":response.content}
