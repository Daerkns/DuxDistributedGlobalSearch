from ddgs import DDGS
from pprint import pprint
import json

def search_duckduckgo(
    query="python programming",
    max_results=10,
    region="wt-wt",          # World-wide; examples: "us-en", "uk-en", "in-en"
    safesearch="moderate",   # "off", "moderate", "strict"
    timelimit=None,          # Possible: "d", "w", "m", "y"
    backend="api",           # "api", "html", or "lite"
    max_page=3,              # How many pages to iterate through
    output="dict",           # "dict" or "list"
    follow_redirects=True,
    delay=2.0                # Delay between page fetches to avoid rate limiting
):
    """
    A flexible wrapper for DDGS text search.
    Modify parameters freely and reuse as a template.
    """

    ddg = DDGS()

    # You can add or remove kwargs depending on your needs
    results = ddg.text(
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

    # Convert generator → list or return raw generator
    if output == "list":
        return list(results)

    return results

# Example use:
if __name__ == "__main__":
    data = search_duckduckgo(
        query="intitle:Manjur Mahamud Datasoft",
        max_results=10,
        region="wt-wt",
        safesearch="off",
        timelimit="m",
        backend="auto",
        output="list"
    )

    for item in data:
        pprint(item)