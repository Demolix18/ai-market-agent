from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict
from typing import List, Dict, Any, Tuple

def compute_cluster_sentiment(cluster: List[Dict[str, Any]], weight_by_domain: Dict[str, float], default_weight: float):
    analyzer = SentimentIntensityAnalyzer()
    s, w = 0.0, 0.0
    for a in cluster:
        txt = (a.get("title","") + " " + a.get("summary","")).strip()
        vs = analyzer.polarity_scores(txt)
        wd = weight_by_domain.get(a["source"], default_weight)
        s += vs["compound"] * wd
        w += wd
    return (s / w) if w else 0.0

def aggregate_by_symbol(clusters_with_entities: List[Tuple[List[Dict[str, Any]], List[str]]], weight_by_domain: Dict[str, float], default_weight: float):
    pos, neg, reasons = defaultdict(float), defaultdict(float), defaultdict(list)

    for cluster, syms in clusters_with_entities:
        if not syms: continue
        sent = compute_cluster_sentiment(cluster, weight_by_domain, default_weight)
        titles = [a["title"] for a in cluster[:2]]
        reason = "; ".join(titles)[:220]
        for s in syms:
            if sent >= 0:
                pos[s] += sent
            else:
                neg[s] += -sent
            reasons[s].append(reason)

    return pos, neg, reasons

def top_n(d: Dict[str, float], n=5):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]
