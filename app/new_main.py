import yfinance as yf
import pandas as pd 
import logging 
import warnings

# Suppressing the logs/warnings to have clean output 

logging.getLogger('yfinance').setLevel(logging.CRITICAL)
warnings.filterwarnings('ignore')

def top_movers(stocks):
    stock_data = yf.download(stocks, period = '7d', interval = '1d', progress= False)
    
    # Checking if all the entered stock ticker is Invalid
    
    if stock_data.empty or 'Close' not in stock_data:   
        raise Exception('Invalid Stock Symbols')
    
    closing_data = stock_data["Close"]
    today_close = closing_data.iloc[-1]
    yesterday_close = closing_data.iloc[-2]
    
    price_change = today_close - yesterday_close
    percent_price_change = (price_change/yesterday_close) * 100
    
    volume_data = stock_data['Volume']
    today_volume = volume_data.iloc[-1]
    yesterday_volume = volume_data.iloc[-2]
    
    volume_change = today_volume - yesterday_volume
    percent_volume_change = (volume_change/yesterday_volume) * 100
    
    # print(type(percent_price_change)) 
    
    # ++++++++++++++++++++++++++++++++++++ RAW DATA ++++++++++++++++++++++++++++
    
    result = []
    for stock in percent_price_change.index:
        result.append({
            'symbol': stock,
            'today_close': round(today_close[stock], 2),
            'percent_price_change': round(percent_price_change[stock], 2),
            'percent_volume_change': round(percent_volume_change[stock], 2)
        })
        
    df_raw = pd.DataFrame(result)
    
    df_raw_sorted = df_raw.sort_values(by='percent_price_change', ascending=False, na_position = 'last')
    
    # ++++++++++++++++++++++++++++++++++++ End ++++++++++++++++++++++++++++++++++
    
    # ++++++++++++++++++++++++++++++++ Formatted Data ++++++++++++++++++++++++++++
    
    df_display = df_raw_sorted.copy()
    
    df_display["percent_price_change"] = df_display["percent_price_change"].apply(
        lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")

    df_display["percent_volume_change"] = df_display["percent_volume_change"].apply(
        lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")

    df_display["today_close"] = df_display["today_close"].apply(
        lambda x: f"₹{x:.2f}" if pd.notna(x) else "N/A")

    return df_raw, df_display