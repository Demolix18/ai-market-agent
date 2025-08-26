from typing import List, Dict, Any
from rapidfuzz import fuzz

def cluster_articles(articles: List[Dict[str, Any]], title_threshold: int = 88) -> List[List[Dict[str, Any]]]:
    clusters: List[List[Dict[str, Any]]] = []
    used = [False] * len(articles)

    for i, a in enumerate(articles):
        if used[i]: 
            continue
        group = [a]
        used[i] = True
        for j in range(i+1, len(articles)):
            if used[j]: 
                continue
            b = articles[j]
            tscore = fuzz.token_set_ratio(a.get("title",""), b.get("title",""))
            if tscore >= title_threshold:
                group.append(b)
                used[j] = True
        clusters.append(group)
    return clusters
