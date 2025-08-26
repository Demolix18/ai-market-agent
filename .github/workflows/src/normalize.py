import re
from typing import Optional

def clean_text(s: Optional[str]) -> str:
    if not s:
        return ""
    s = re.sub(r'<[^>]+>', ' ', s)  # strip HTML
    s = s.replace('\xa0', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:4000]
