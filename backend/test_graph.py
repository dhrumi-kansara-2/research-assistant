'''
temp test file to check full planner to reseracher work flow end to end
'''
from graph import graph
result=graph.invoke({
    "query":"What is the impact of AI on healtcare?",
    "sub_questions": [],
    "search_results": [],
    "draft": "",
    "critique": "",
    "final_report":""
})

print("sub questions")

for q in result["sub_questions"]:
    print("-",q)

print("\nSearch results count:", len(result["search_results"]))
print("\nCritique:")
print(result["critique"])
print("\nFinal report preview:")
print(result["final_report"][:500])