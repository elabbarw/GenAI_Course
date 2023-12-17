# RAG - DuckDuckGo
from duckduckgo_search import DDGS
from gptrim import trim

def search_internet(query):
    """
    Use Duckduck go Search
    """
    
    count = 5
    result_text=''
    with DDGS() as ddgs:
        search_results = [r for r in ddgs.text(query, max_results=count)]
        for result in search_results:
            title = result.get('title', '')
            snippet = result.get('body', '')
            url = result.get('href', '')
            result_text += f'Title: {title}\nSnippet: {snippet}\nURL: {url}\n\n'

        search_prompt = f"""
        Based on the internet search results provided in <>, provide an answer to the query [] if it is relevant along with a source URL. \
        If there are no internet search results or if they are not relevant then say \"Please try again.\"\
        
        context:<{trim(result_text)}>
        query:[{query}]
        """

        return {"role":"system","content": search_prompt}

