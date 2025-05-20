# NVIDIA Stock Alert & News Telegram Bot

This Python project monitors NVIDIA (NVDA) stock price changes and sends Telegram alerts with related news when significant price movements occur.

---

## Features

- Fetches daily stock prices from [Alpha Vantage API](https://www.alphavantage.co/)
- Detects notable price changes (default threshold ±3%)
- Retrieves the top 3 recent news articles about NVIDIA from [NewsAPI](https://newsapi.org/)
- Sends notifications via Telegram bot with retries and error handling
- Uses environment variables to manage API keys and tokens securely

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/nvda-stock-alert.git
cd nvda-stock-alert
```
### 2. Create a .env file in the project root with the following variables:
```bash
api_alpha=YOUR_ALPHA_VANTAGE_API_KEY
api_news=YOUR_NEWSAPI_API_KEY
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
CHAT_ID=YOUR_TELEGRAM_CHAT_ID
```
Replace the placeholders with your actual API keys and Telegram bot credentials.
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

Run the main script to check stock price changes and receive news alerts on Telegram:
```bash
python your_script.py
```

---


## File Overview
### `your_script.py`

- Fetches daily closing prices for NVDA. 
- Compares the last two days’ closing prices. 
- If the price change exceeds the threshold (±3%), fetches related news. 
- Sends the alert and news to your Telegram chat.

### `send_telegram_message.py`

- Handles sending messages to Telegram with retries and exponential backoff:

```python
import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing BOT_TOKEN or CHAT_ID in environment.")
        return

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    retries = 3

    for attempt in range(retries):
        try:
            response = requests.post(telegram_url, data=payload, timeout=5)
            response.raise_for_status()
            print("Message sent successfully.")
            return
        except Exception as e:
            print(f"Error: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("Failed after retries.")
```

### `requirements.txt`
```bash
requests
python-dotenv
```

---


## Customization
- Modify STOCK_NAME and NOTICEABLE_DIFFERENCE in the main script to monitor different stocks or adjust sensitivity. 
- Update the .env file with your own API keys and Telegram credentials. 
- Extend the script with scheduling (e.g., cron jobs) or logging for production use.

---


## License
This project is licensed under the MIT License.

Feel free to open issues or submit pull requests for improvements!
