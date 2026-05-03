

import pandas as pd
import pandas_market_calendars as mcal

_holiday_cache = {}

def get_holiday_set(year):
    if year in _holiday_cache:
        return _holiday_cache[year]

    start = f'{year}-01-01'
    end = f'{year}-12-31'

    nse = mcal.get_calendar('NSE')
    schedule = nse.schedule(start_date=start, end_date=end)

    trading_days = schedule.index.tz_localize(None)
    all_days = pd.date_range(start=start, end=end, freq='D')

    holidays = all_days.difference(trading_days)

    holiday_set = set(holidays)

    _holiday_cache[year] = holiday_set  # cache it

    return holiday_set