import os
import requests

def get_yahoo_data(ticker):
    """Fetches raw market data from Yahoo Finance's backend by mimicking a desktop browser."""
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    price = data['chart']['result'][0]['meta']['regularMarketPrice']
    prev_close = data['chart']['result'][0]['meta']['chartPreviousClose']
    change_percent = ((price - prev_close) / prev_close) * 100
    return price, change_percent

try:
    # 1. Fetch live futures and exchange rate data
    gold_usd, gold_change = get_yahoo_data("GC=F")  # Gold Futures
    silver_usd, _ = get_yahoo_data("SI=F")          # Silver Futures
    usd_inr, _ = get_yahoo_data("INR=X")            # USD to INR Conversion Rate

except Exception as e:
    print(f"Data Fetch Error: {e}")
    exit(1)

# 2. Convert raw USD global prices per Troy Ounce to base INR weights
troy_ounce_g = 31.1034768
gold_10g_base = (gold_usd * usd_inr / troy_ounce_g) * 10
silver_1kg_base = (silver_usd * usd_inr / troy_ounce_g) * 1000

# 3. Apply the 15.5% Indian Market Premium 
india_multiplier = 1.155 
odisha_gold_24k = gold_10g_base * india_multiplier
odisha_silver_1kg = silver_1kg_base * india_multiplier

# Calculate 22K Gold from 24K base
odisha_gold_22k = odisha_gold_24k * (22 / 24)

# 4. Generate Market Mood Analysis and Advice
if gold_change > 0.5:
    market_mood = "🔥 Bullish (Prices are soaring!)"
    advice = "💡 Prices are up today. If you're looking to sell, it's a great window! If buying, consider waiting for a minor dip."
elif gold_change < -0.5:
    market_mood = "📉 Bearish (Prices are dropping!)"
    advice = "🛍️ Gold is on discount today! Excellent time to accumulate for upcoming weddings or long-term savings."
else:
    market_mood = "⚖️ Stable (Consolidating)"
    advice = "⏳ Market is moving sideways. A safe, steady day to execute your planned accumulation strategy."

# 5. Format the Telegram message using your exact layout
message = f"""🌅 *Odishan Metal Bulletin* 🌅

📊 *Market Mood:* {market_mood}

✨ *GOLD (per 10 Grams):*
• 24K Pure Gold: ₹{odisha_gold_24k:,.0f}
• 22K Jewelry Gold: ₹{odisha_gold_22k:,.0f}

🥈 *SILVER (per 1 KG):*
• Chandi Rate: ₹{odisha_silver_1kg:,.0f}

---
🌟 *Today's Insight:* {advice}

_(Calculated via live global spot + standard duties. Retail making charges not included.)_"""

# 6. Broadcast via Telegram Bot API
token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')

if not token or not chat_id:
    print("Error: Missing Telegram credentials in GitHub Secrets.")
    exit(1)

url = f"https://api.telegram.org/bot{token}/sendMessage"

response = requests.post(url, json={
    "chat_id": chat_id, 
    "text": message, 
    "parse_mode": "Markdown"
})

if response.status_code == 200:
    print("Bulletin successfully sent to Telegram!")
else:
    print(f"Telegram Delivery Failure: {response.text}")
