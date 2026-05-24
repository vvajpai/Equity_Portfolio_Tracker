from new_main import top_movers
from database_supa import add_stock, get_portfolio, save_daily_stock_data, remove_stock
from email_sender import send_email
from market_holidays import get_holiday_set
import pandas as pd

def run_daily_job():
    print("Running daily stock analysis...\n")

    portfolio = get_portfolio()

    if not portfolio:
        print("Portfolio empty. Run setup first.")
        return

    try:
        df_raw, df_display = top_movers(portfolio)
    except Exception as e:
        print(f"Analysis failed: {e}")
        return

    if df_raw is None or df_raw.empty:
        print("No stock data generated.")
        return

    saved = save_daily_stock_data(df_raw)

    if saved:
        print("Data saved successfully")
    else:
        print("Failed to save data")
        return

    print("Sending email report...")
    send_email(df_display)

    print("Daily job completed\n")


if __name__ == "__main__":

    today = pd.Timestamp.today().normalize()
    year = today.year

    holiday_set = get_holiday_set(year)

    if today in holiday_set:
        print("Market Closed (holiday/weekend)")
        send_email("Market is closed today (holiday/weekend). No stock data collected.")
    else:

        run_daily_job()
