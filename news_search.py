from ddgs import DDGS
from pprint import pprint
import json

def search_duckduckgo_news(
    query="latest ai research",
    max_results=10,
    region="wt-wt",          # Examples: "us-en", "uk-en", "in-en"
    safesearch="moderate",   # "off", "moderate", "strict"
    timelimit=None,          # "d" = day, "w" = week, "m" = month, "y" = year
    backend="api",           # "api" | "html" | "lite"
    max_page=3,              # How many result pages to crawl
    follow_redirects=True,
    delay=1.0,               # Delay between requests
    output="list",           # "list" | "generator"
):
    """
    Flexible wrapper for DDGS news search.
    Modify parameters freely.
    """

    ddg = DDGS()

    results = ddg.news(
        query,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
        backend=backend,
        max_page=max_page,
        follow_redirects=follow_redirects,
        delay=delay,
    )

    # Convert to list if desired
    if output == "list":
        return list(results)

    return results


# Example usage:
if __name__ == "__main__":
    articles = search_duckduckgo_news(
        query="intitle:Chowdhury Nafeez Sarafat",
        max_results=5,
        region="wt-wt",
        safesearch="off",
        timelimit="w",
        backend="html",
        output="list"
    )

    for article in articles:
        pprint(article)
