import os
import requests
import time
from send_telegram_message import send_telegram_message
from dotenv import load_dotenv

STOCK_NAME = "NVDA"
NOTICEABLE_DIFFERENCE = 3

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

load_dotenv()
api_alpha = os.getenv("API_ALPHA")
api_news = os.getenv("API_NEWS")

def get_stockprice():
    params_pricecall = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "NVDA",
        "outputsize": "compact",
        "datatype": "json",
        "apikey": api_alpha,
    }

    response = requests.get(STOCK_ENDPOINT, params=params_pricecall)
    data = response.json()

    last_weekday = list(data["Time Series (Daily)"])[0]
    lw_closing = float(data["Time Series (Daily)"][last_weekday]["4. close"])

    day_before_last_weekday = list(data["Time Series (Daily)"])[1]
    db_lw_closing = float(data["Time Series (Daily)"][day_before_last_weekday]["4. close"])

    closing_price_diff_perc = round(((lw_closing - db_lw_closing) / db_lw_closing) * 100, 2)

    if abs(closing_price_diff_perc) > NOTICEABLE_DIFFERENCE:
        return closing_price_diff_perc
    else:
        return False

def get_news(input_text: int):
    params_newscall = {
        "apiKey": api_news,
        "q": "NVIDIA",
    }

    response_news = requests.get(NEWS_ENDPOINT, params=params_newscall)
    data_news = response_news.json()
    news_top_three = data_news["articles"][0:3]

    diff_stockprice = input_text
    if diff_stockprice > 0:
        print_diff = f"{STOCK_NAME}: 🔺{abs(diff_stockprice)}"
    else:
        print_diff = f"{STOCK_NAME}: 🔻{abs(diff_stockprice)}"

    news_top_three_clean = [(news["title"], news["description"], news["url"]) for news in news_top_three]

    send_telegram_message(print_diff)
    time.sleep(2)
    for title, description, url in news_top_three_clean:
        message = (f"{title}: {description}\n"
                   f"{url}")
        send_telegram_message(message)
        time.sleep(2)

run_analysis = get_stockprice()

if run_analysis:
    get_news(run_analysis)
else:
    pass
