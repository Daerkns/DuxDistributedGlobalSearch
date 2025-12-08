from ddgs import DDGS
from pprint import pprint

results = DDGS().text("python programming", max_results=5)
pprint(results)