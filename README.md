# AI Market Agent (Nightly, 10 PM IST)

This repo fetches Indian markets news from Google News RSS (for Moneycontrol, ET Markets, Mint, Business Standard, NSE), clusters similar stories, maps them to companies, scores sentiment, and emails a nightly report.

### How it works
1. Fetch headlines from Google News RSS (~36h).
2. Normalize + store in SQLite.
3. Cluster near-duplicates.
4. Map to companies (from `data/companies_master.csv`).
5. Score sentiment (positive/negative).
6. Email you **Top 5 positive** + **Top 5 negative** stocks.

### Setup
1. Get a Gmail **App Password** (16 characters).
2. Add GitHub repo **Secrets**:
   - `SMTP_USER` = your Gmail
   - `SMTP_PASS` = your Gmail App Password
   - `EMAIL_TO`  = where to receive reports
3. Done — workflow runs daily at **10 PM IST**.

### Optional
- Add Telegram bot secrets for instant notifications.
- Edit `src/config.py` to change sources.
- Add more companies in `data/companies_master.csv`.
