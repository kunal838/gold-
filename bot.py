import os
import requests
import yfinance as yf

# 1. Fetch live global data and currency conversion
gold_usd = yf.Ticker("XAUUSD=X").history(period="1d")['Close'].iloc[-1]
silver_usd = yf.Ticker("XAGUSD=X").history(period="1d")['Close'].iloc[-1]
usd_inr = yf.Ticker("INR=X").history(period="1d")['Close'].iloc[-1]

# 2. Convert to INR per standard Indian weights
troy_ounce_g = 31.1034768
gold_10g_base = (gold_usd * usd_inr / troy_ounce_g) * 10
silver_1kg_base = (silver_usd * usd_inr / troy_ounce_g) * 1000

# 3. Apply Indian Market Premium 
# Adds ~9% to account for India's import duty (6%) and GST (3%) 
# to match local Odisha retail rates.
india_multiplier = 1.09 
odisha_gold_10g = gold_10g_base * india_multiplier
odisha_silver_1kg = silver_1kg_base * india_multiplier

# 4. Format the daily text message
message = f"""🪙 *Bhubaneswar Daily Price Estimate* 🪙

*24K Gold (10g):* ₹{odisha_gold_10g:,.0f}
*Silver (1kg):* ₹{odisha_silver_1kg:,.0f}

_(Calculated with standard duties/GST. Local jewelry store making charges are not included.)_"""

# 5. Send the text message via Telegram API
token = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHAT_ID']

# Note: We switched back to 'sendMessage' instead of 'sendPhoto'
url = f"https://api.telegram.org/bot{token}/sendMessage"

requests.post(url, json={
    "chat_id": chat_id, 
    "text": message, 
    "parse_mode": "Markdown"
})
