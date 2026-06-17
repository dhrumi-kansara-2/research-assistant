from ddgs import DDGS

def search_duckduckgo(query: str, max_results: int=5)->list[str]:
    results=[]
    with DDGS() as ddgs:
        for r in ddgs.text(query,max_results=max_results):
            snippet = f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}"
            results.append(snippet)
    return results