from datetime import datetime, timedelta
from .config import (
    IST, LOOKBACK_HOURS, NEWS_DOMAINS, 
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_TO,
    ENABLE_TELEGRAM, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    DB_PATH, WEIGHT_BY_DOMAIN, DEFAULT_DOMAIN_WEIGHT
)
from . import db
from .sources.google_news import fetch_for_domain
from .normalize import clean_text
from .dedupe import cluster_articles
from .entities import load_companies, find_mentions
from .score import aggregate_by_symbol, top_n
from .report import build_report_html, build_report_text
from .notify.emailer import send_email
from .notify.telegram import send_telegram

def main():
    # Current time in IST
    now_ist = datetime.now(IST)
    since_ist = now_ist - timedelta(hours=LOOKBACK_HOURS)

    # Database connection
    conn = db.get_conn(DB_PATH)
    db.init_db(conn)

    # 1. Ingest articles
    all_articles = []
    for dom in NEWS_DOMAINS:
        try:
            arts = fetch_for_domain(dom)
            for a in arts:
                a.summary = clean_text(a.summary)
                all_articles.append({
                    "source": a.source,
                    "url": a.url,
                    "title": a.title,
                    "published_at": a.published_at.isoformat(timespec="seconds"),
                    "summary": a.summary,
                    "raw_text": a.raw_text or ""
                })
        except Exception:
            continue
    db.insert_articles(conn, all_articles)

    # 2. Fetch only recent ones
    recent = db.fetch_recent_articles(conn, since_ist.isoformat(timespec="seconds"))
    if not recent:
        print("No recent articles found.")
        return

    # 3. Cluster near-duplicates
    clusters = cluster_articles(recent, title_threshold=88)

    # 4. Map clusters to companies
    companies = load_companies("data/companies_master.csv")
    clusters_with_entities = []
    for cl in clusters:
        bag = " ".join([(c.get("title","") + " " + c.get("summary","")) for c in cl])
        syms = find_mentions(bag, companies)
        clusters_with_entities.append((cl, syms))

    # 5. Compute sentiment scores
    pos, neg, reasons = aggregate_by_symbol(clusters_with_entities, WEIGHT_BY_DOMAIN, DEFAULT_DOMAIN_WEIGHT)
    top_pos = top_n(pos, 5)
    top_neg = top_n(neg, 5)

    # 6. Build report
    date_str = now_ist.strftime("%Y-%m-%d %H:%M IST")
    html = build_report_html(date_str, top_pos, top_neg, reasons)
    txt  = build_report_text(date_str, top_pos, top_neg, reasons)

    # 7. Send notifications
    subject = f"Daily Market Impact — {date_str}"
    if SMTP_USER and SMTP_PASS and EMAIL_TO:
        send_email(SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_TO, subject, html, txt)
        print("✅ Email sent.")
    else:
        print("⚠️ Email not configured. Check SMTP_USER, SMTP_PASS, EMAIL_TO secrets.")

    if ENABLE_TELEGRAM and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        send_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, txt[:4000])
        print("✅ Telegram sent.")

if __name__ == "__main__":
    main()
