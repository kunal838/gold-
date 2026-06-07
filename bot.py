import yfinance as yf
import requests
import os

# Fetch global spot prices in INR
# XAUINR=X is Gold to INR, XAGINR=X is Silver to INR
gold = yf.Ticker("XAUINR=X").history(period="1d")['Close'].iloc[-1]
silver = yf.Ticker("XAGINR=X").history(period="1d")['Close'].iloc[-1]

# Convert from Troy Ounce to Indian standard weights
troy_ounce_g = 31.1034768
gold_10g = (gold / troy_ounce_g) * 10
silver_1kg = (silver / troy_ounce_g) * 1000

# Format your daily message
message = f"""🪙 *Daily Price Update* 🪙

*Gold (10g):* ₹{gold_10g:,.2f}
*Silver (1kg):* ₹{silver_1kg:,.2f}

_(Based on global spot prices - local Jharsuguda rates may vary slightly based on making charges and taxes)_"""

# Send via Telegram API
token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']
url = f"https://api.telegram.org/bot{token}/sendMessage"

requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
