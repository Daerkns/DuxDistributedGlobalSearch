from ddgs import DDGS
from pprint import pprint
import json
import hashlib
import os

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
    delay=2.0,               # Delay between page fetches to avoid rate limiting
    fixed_results=False,     # NEW: Toggle to enable fixed/cached results
    cache_dir=".search_cache"  # Directory to store cached results
):
    """
    A flexible wrapper for DDGS text search with optional result caching.
    
    When fixed_results=True, the function will:
    - Cache search results on first run
    - Return identical cached results on subsequent runs
    - Generate cache key based on search parameters
    
    Modify parameters freely and reuse as a template.
    """
    
    if fixed_results:
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Generate unique cache key from search parameters
        cache_params = {
            "query": query,
            "max_results": max_results,
            "region": region,
            "safesearch": safesearch,
            "timelimit": timelimit,
            "backend": backend
        }
        cache_key = hashlib.md5(
            json.dumps(cache_params, sort_keys=True).encode()
        ).hexdigest()
        
        cache_file = os.path.join(cache_dir, f"{cache_key}.json")
        
        # Try to load from cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_results = json.load(f)
                print(f"[FIXED MODE] Loaded {len(cached_results)} results from cache")
                print(f"[FIXED MODE] Cache file: {cache_file}")
                
                if output == "list":
                    return cached_results
                return iter(cached_results)
        
        # If not cached, fetch and save
        print("[FIXED MODE] No cache found, fetching and caching results...")
        print(f"[FIXED MODE] Cache key: {cache_key}")

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

    # Convert generator → list
    results_list = list(results)
    
    # Save to cache if fixed_results is enabled
    if fixed_results:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(results_list, f, indent=2, ensure_ascii=False)
        print(f"[FIXED MODE] Cached {len(results_list)} results to {cache_file}")

    # Return based on output format
    if output == "list":
        return results_list

    return iter(results_list)

# Example use:
if __name__ == "__main__":
    # Example 1: Fixed results mode (will cache on first run)
    print("=" * 60)
    print("EXAMPLE 1: Fixed Results Mode (ON)")
    print("=" * 60)
    data = search_duckduckgo(
        query="intitle:Manjur Mahamud Datasoft",
        max_results=10,
        region="wt-wt",
        safesearch="off",
        timelimit="m",
        backend="auto",
        output="list",
        fixed_results=True  # Toggle ON for fixed results
    )

    for item in data:
        pprint(item)
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("Run this script again to see cached results loaded!")
    print("Delete '.search_cache' folder to refresh results.")
    print("=" * 60)
    
    # Example 2: Normal mode (always fetches fresh results)
    # Uncomment below to test normal mode:
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Normal Mode (OFF)")
    print("=" * 60)
    data = search_duckduckgo(
        query="intitle:Manjur Mahamud Datasoft",
        max_results=10,
        region="wt-wt",
        safesearch="off",
        timelimit="m",
        backend="auto",
        output="list",
        fixed_results=False  # Toggle OFF for fresh results
    )
    
    for item in data:
        pprint(item)
        print("-" * 40)
    """