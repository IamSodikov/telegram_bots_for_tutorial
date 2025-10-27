import wikipedia

def search_wiki(search_query: str)-> str:
    wiki_result = wikipedia.search(search_query)
    summary_result = wikipedia.summary(wiki_result[0], sentences = 10)
    return summary_result
