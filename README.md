# 📊 Equity Portfolio Tracker

A Python-based automated system that tracks equity portfolio performance, stores historical market data in Supabase (PostgreSQL), and sends daily email reports.

---

## 🚀 Features

- 📈 Fetch real-time stock data using Yahoo Finance (yfinance)
- 🗄️ Store portfolio & historical data in Supabase (PostgreSQL)
- 📊 Calculate daily price and volume changes
- 🧾 Maintain complete historical stock performance records
- 📧 Generate HTML email reports
- 🏦 Skip execution on NSE market holidays
- ⚙️ Fully automated daily pipeline

---

## 🏗️ Architecture

- Portfolio Table (Supabase)
        ↓
- Yahoo Finance API
        ↓
- Pandas Analytics Engine
        ↓
- Supabase PostgreSQL (daily_stock_data)
        ↓
- Email Report Generator
        ↓
- Gmail SMTP

---

## ⚙️ Tech Stack

- Python
- yFinance
- Pandas
- Supabase (PostgreSQL)
- Requests
- SMTP (Gmail)
- pandas_market_calendars
- python-dotenv

---
## 🗄️ Database Schema

### portfolio
- ticker (TEXT, UNIQUE)
- active (INT)
- created_at (TIMESTAMP)

### daily_stock_data
- ticker (TEXT)
- date (DATE)
- close_price (FLOAT)
- price_change_pct (FLOAT)
- volume_change_pct (FLOAT)
- created_at (TIMESTAMP)
- UNIQUE (ticker, date)

---

## 🔄 Workflow

1. Load portfolio from Supabase
2. Fetch stock data from Yahoo Finance
3. Compute analytics
4. Store in PostgreSQL
5. Generate email report
6. Send email
7. Skip holidays

---

## 📈 Future Improvements

- Streamlit dashboard

---

## 📄 License

MIT License
