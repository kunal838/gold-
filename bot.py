import os
import requests

try:
    # 1. Fetch live global data using stable public REST APIs
    # No API keys required for these endpoints
    gold_data = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
    gold_usd = gold_data['price']
    
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

# 3. Apply Indian Market Premium 
# Adds ~9% to account for India's import duty (6%) and GST (3%) 
# to roughly match local Odisha retail rates.
india_multiplier = 1.09 
odisha_gold_10g = gold_10g_base * india_multiplier
odisha_silver_1kg = silver_1kg_base * india_multiplier

# 4. Format the daily text message
message = f"""🪙 *Bhubaneswar Daily Price Estimate* 🪙

*24K Gold (10g):* ₹{odisha_gold_10g:,.0f}
*Silver (1kg):* ₹{odisha_silver_1kg:,.0f}

_(Calculated using live global APIs + standard duties/GST. Local making charges not included.)_"""

# 5. Send the text message via Telegram API
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
