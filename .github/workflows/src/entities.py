import csv, re
from typing import List, Dict

def load_companies(csv_path: str):
    companies = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            aliases = [a.strip() for a in (row.get("ALIASES") or "").split(";") if a.strip()]
            companies.append({
                "symbol": row["SYMBOL"].strip(),
                "name": row["COMPANY_NAME"].strip(),
                "aliases": aliases
            })
    return companies

def find_mentions(text: str, companies: List[Dict[str, str]]):
    text_low = text.lower()
    hits = []
    for c in companies:
        names = [c["name"]] + c["aliases"]
        for nm in names:
            nm_low = nm.lower()
            if re.search(rf'\b{re.escape(nm_low)}\b', text_low):
                hits.append(c["symbol"])
                break
    return list(sorted(set(hits)))
