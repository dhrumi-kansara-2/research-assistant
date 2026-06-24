import json



'''
temp test file to check full planner to reseracher work flow end to end
'''
from graph import graph
result=graph.invoke({
    "query":"XAI methods in healthcare",
    "sub_questions": [],
    "search_results": [],
    "draft": "",
    "critique": "",
    "final_report":""
},    config={"recursion_limit": 10}  # max 10 node executions
)

print("sub questions")

for q in result["sub_questions"]:
    print("-",q)

print("\nSearch results count:", len(result["search_results"]))
print("\nCritique:")
print(result["critique"])
print("\nFinal report preview:")
print(result["final_report"][:500])

 
#saving result in a text file to see whole output
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("=" * 50 + "\n")
    f.write("QUERY\n")
    f.write("=" * 50 + "\n")
    f.write(result["query"] + "\n\n")

    f.write("=" * 50 + "\n")
    f.write("SUB QUESTIONS\n")
    f.write("=" * 50 + "\n")
    for q in result["sub_questions"]:
        f.write(f" - {q}\n")
    f.write("\n")

    f.write("=" * 50 + "\n")
    f.write("SEARCH RESULTS\n")
    f.write("=" * 50 + "\n")
    for r in result["search_results"]:
        f.write(r + "\n\n")

    f.write("=" * 50 + "\n")
    f.write("DRAFT\n")
    f.write("=" * 50 + "\n")
    f.write(result["draft"] + "\n\n")

    f.write("=" * 50 + "\n")
    f.write("CRITIQUE\n")
    f.write("=" * 50 + "\n")
    f.write(result["critique"] + "\n\n")

    f.write("=" * 50 + "\n")
    f.write("FINAL REPORT\n")
    f.write("=" * 50 + "\n")
    f.write(result["final_report"] + "\n")

print("State saved to output.txt")