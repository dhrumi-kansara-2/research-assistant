from state import ResearchState
from langgraph.graph import StateGraph, END  
from nodes import planner_node, researcher_node, synthesizer_node, critic_node, report_node 
 
'''router function before graph builder'''
def should_continue(state: ResearchState)->str:
    critique=state["critique"]
    if "APPROVED" in critique:
        return "done"
    return "try_again"

'''
connecting two nodes and defining flow between them
'''
graph_builder=StateGraph(ResearchState)

graph_builder.add_node("planner",planner_node)
graph_builder.add_node("researcher",researcher_node)
graph_builder.add_node("synthesizer",synthesizer_node)
graph_builder.add_node("critic",critic_node)
graph_builder.add_node("report",report_node)


graph_builder.set_entry_point("planner")
graph_builder.add_edge("planner","researcher")
graph_builder.add_edge("researcher","synthesizer")
graph_builder.add_edge("researcher","critic")
graph_builder.add_conditional_edges("critic",should_continue,{"done":"report","try_again":"researcher"})
graph_builder.add_edge("researcher",END)




graph=graph_builder.compile()