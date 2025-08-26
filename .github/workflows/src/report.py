from typing import Dict, List

def build_report_html(date_str: str, top_pos: List, top_neg: List, reasons: Dict[str, List[str]]):
    def block(title, items):
        html = f"<h2>{title}</h2><ol>"
        for sym, score in items:
            bullets = "".join(f"<li>{r}</li>" for r in reasons.get(sym, [])[:3])
            html += f"<li><strong>{sym}</strong> — {score:.2f}<ul>{bullets}</ul></li>"
        html += "</ol>"
        return html

    return f"""
    <html><body>
    <h1>Daily Market Impact — {date_str}</h1>
    {block("Top 5 Positive", top_pos)}
    {block("Top 5 Negative", top_neg)}
    </body></html>
    """

def build_report_text(date_str: str, top_pos: List, top_neg: List, reasons: Dict[str, List[str]]):
    def block(title, items):
        out = [title]
        for sym, score in items:
            Rs = reasons.get(sym, [])[:3]
            out.append(f"- {sym} — {score:.2f}")
            for r in Rs:
                out.append(f"  • {r}")
        return "\n".join(out)

    txt = f"Daily Market Impact — {date_str}\n\n"
    txt += block("Top 5 Positive", top_pos) + "\n\n"
    txt += block("Top 5 Negative", top_neg) + "\n"
    return txt
