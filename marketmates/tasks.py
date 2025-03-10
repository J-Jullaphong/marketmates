from datetime import datetime
from io import StringIO

import pandas as pd
import yfinance as yf
from celery import shared_task
from celery.schedules import crontab
from django.core.cache import cache
from django.conf import settings
from selenium import webdriver

from mysite.celery import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Fetch and Store Market Data Periodically."""
    sender.add_periodic_task(
        crontab(minute='*/10', hour='9-18', day_of_week='1-5'),
        fetch_and_store_market_data.s(),
    )


def fetch_stock_data():
    """Fetch stock data from Yahoo Finance."""
    set_data = yf.Ticker('^SET.BK').history()
    latest_close = set_data['Close'].iloc[-1]
    prev_close = set_data['Close'].iloc[-2] if len(
        set_data) > 1 else latest_close
    percent_change = ((
                                  latest_close - prev_close) / prev_close) * 100 if prev_close != 0 else 0
    return set_data, latest_close, percent_change


def parse_table_data(data):
    """Parse and clean table data from the scraped HTML."""
    df_list = pd.read_html(StringIO(str(data)))
    cleaned_data = []

    for df in df_list:
        df.iloc[:, 0] = df.iloc[:, 0].str.split().str.get(0)
        df.index = df.index + 1
        cleaned_data.append(df)

    return cleaned_data[:4]


@shared_task
def fetch_and_store_market_data():
    """Scrape and store market data."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Remote(command_executor=settings.SELENIUM_REMOTE_URL,
                              options=options)
    try:
        driver.get('https://www.set.or.th/th/market/product/stock/top-ranking')
        data = driver.page_source
    finally:
        driver.quit()

    most_active_value, most_active_volume, top_gainer, top_loser = parse_table_data(
        data)

    set_data, latest_close, percent_change = fetch_stock_data()

    market_data = {
        'most_active_value': most_active_value,
        'most_active_volume': most_active_volume,
        'top_gainer': top_gainer,
        'top_loser': top_loser,
        'most_active_value_columns': most_active_value.columns.tolist(),
        'most_active_volume_columns': most_active_volume.columns.tolist(),
        'top_gainer_columns': top_gainer.columns.tolist(),
        'top_loser_columns': top_loser.columns.tolist(),
        'set_data': set_data,
        'latest_close': latest_close,
        'percent_change': percent_change,
        'last_update': f"{datetime.now():%d/%m/%Y %H:%M}"
    }

    cache.set('market_data', market_data, timeout=None)
    return market_data
