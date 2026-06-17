from state import ResearchState
from langgraph.graph import StateGraph, END  
from nodes import planner_node, researcher_node 
 
graph_builder=StateGraph(ResearchState)

'''
connecting two nodes and defining flow between them
'''

graph_builder.add_node("planner",planner_node)
graph_builder.add_node("researcher",researcher_node)
graph_builder.set_entry_point("planner")
graph_builder.add_edge("planner","researcher")
graph_builder.add_edge("researcher",END)

graph=graph_builder.compile()