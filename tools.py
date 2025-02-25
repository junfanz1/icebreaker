from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    """ Search for LinkedIn or X Profile page"""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res