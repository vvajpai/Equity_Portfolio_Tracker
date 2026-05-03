📊 Equity Portfolio Tracker

A Python-based automated system that tracks equity portfolio performance, stores historical market data in Supabase (PostgreSQL), and sends daily email reports.

🚀 Features
📈 Fetch real-time stock data using Yahoo Finance (yfinance)
🗄️ Store portfolio & historical data in Supabase (PostgreSQL)
📊 Calculate daily price and volume changes
🧾 Maintain complete historical stock performance records
📧 Generate HTML email reports for daily portfolio performance
🏦 Automatically skip execution on NSE market holidays
⚙️ Fully automated daily execution pipeline (GitHub Actions ready)

🏗️ Architecture
Portfolio Table (Supabase)
        ↓
Yahoo Finance API (yfinance)
        ↓
Analytics Engine (Pandas)
        ↓
Supabase PostgreSQL (daily_stock_data)
        ↓
Email Report Generator
        ↓
Gmail SMTP Delivery

⚙️ Tech Stack
Python
yFinance
Pandas
Supabase (PostgreSQL)
Requests (REST API)
SMTP (Gmail)
pandas_market_calendars
python-dotenv

📂 Project Structure
app/
│
├── new_main.py                
├── database.py          
├── email_sender.py       
├── market_holidays.py   
├── runner.py             
│
├── .env                  
├── requirements.txt
└── README.md

🗄️ Database

The project uses Supabase PostgreSQL with two main tables:

📌 portfolio

Stores active stocks in the portfolio.

ticker (TEXT, UNIQUE)
active (INT)
created_at (TIMESTAMP)
📌 daily_stock_data

Stores historical stock performance data.

ticker (TEXT)
date (DATE)
close_price (FLOAT)
price_change_pct (FLOAT)
volume_change_pct (FLOAT)
created_at (TIMESTAMP)
UNIQUE (ticker, date)

🔄 Workflow

Load portfolio from Supabase
Fetch latest stock data from Yahoo Finance
Compute price & volume changes
Store results in PostgreSQL (daily_stock_data)
Generate HTML email report
Send daily email to user
Skip execution on NSE holidays

📈 Future Improvements

📊 Streamlit dashboard for portfolio visualization

📄 License

MIT License — free to use and modify
