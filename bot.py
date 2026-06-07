import os
import requests

try:
    # 1. Fetch live global data using stable public REST APIs
    gold_data = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
    gold_usd = gold_data['price']
    gold_change = gold_data.get('chg', 0)  # Daily price change percentage
    
    silver_data = requests.get("https://api.gold-api.com/price/XAG", timeout=10).json()
    silver_usd = silver_data['price']
    
    fx_data = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10).json()
    usd_inr = fx_data['rates']['INR']

except Exception as e:
    print(f"Data Fetch Error: {e}")
    exit(1)

# 2. Convert to INR per standard Indian weights
troy_ounce_g = 31.1034768
gold_10g_base = (gold_usd * usd_inr / troy_ounce_g) * 10
silver_1kg_base = (silver_usd * usd_inr / troy_ounce_g) * 1000

# 3. Apply Indian Market Premium (~9% to account for India's 6% import duty + 3% GST)
india_multiplier = 1.09 
odisha_gold_24k = gold_10g_base * india_multiplier
odisha_silver_1kg = silver_1kg_base * india_multiplier

# Calculate 22K Gold (Jewelry standard) from the 24K base
odisha_gold_22k = odisha_gold_24k * (22 / 24)

# 4. Creative Element: Generate Market Mood & Smart Advice
if gold_change > 0.5:
    market_mood = "🔥 Bullish (Prices are soaring!)"
    advice = "💡 Prices are up today. If you're looking to sell, it's a great window! If buying, consider waiting for a minor dip."
elif gold_change < -0.5:
    market_mood = "📉 Bearish (Prices are dropping!)"
    advice = "🛍️ Gold is on discount today! Excellent time to accumulate for upcoming weddings or long-term savings."
else:
    market_mood = "⚖️ Stable (Consolidating)"
    advice = "⏳ Market is moving sideways. A safe, steady day to execute your planned accumulation strategy."

# 5. Format the daily text message
message = f"""🌅 *Odishan Metal Bulletin* 🌅

*📊 Market Mood:* {market_mood}

✨ *GOLD (per 10 Grams):*
• *24K Pure Gold:* ₹{odisha_gold_24k:,.0f}
• *22K Jewelry Gold:* ₹{odisha_gold_22k:,.0f}

🥈 *SILVER (per 1 KG):*
• *Chandi Rate:* ₹{odisha_silver_1kg:,.0f}

---
🌟 *Today's Insight:* {advice}

_(Calculated using live global APIs + local structural duties. Excludes retail making charges.)_"""

# 6. Send the text message via Telegram API
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
    print("Message sent successfully!")
else:
    print(f"Telegram Error: {response.text}")
