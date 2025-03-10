import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pushover credentials
TOKEN = os.getenv("PUSHOVER_TOKEN")
USER_KEY = os.getenv("PUSHOVER_USER_KEY")
DEVICE_NAME = os.getenv("PUSHOVER_DEVICE_NAME")
SOUND = "echo"

# Dexscreener API details
CHAIN_ID = "sonic"
PAIR_ADDRESS = "0x66af3655e14a045f1742b3c9544553ef7915ed35"
TARGET_PRICE_LOW = 172.9  # Set your price alert
TARGET_PRICE_HIGH = 177.6

# File to store alert state
STATE_FILE = "alert_state.json"

def send_notification(price, symbol):
    """Send price alert via Pushover"""
    print(f"🚨 Sending notification: {price} | {symbol}!")
    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": TOKEN,
        "user": USER_KEY,
        "device": DEVICE_NAME,
        "sound": SOUND,
        "message": f"🚨 Price Alert: {price} | {symbol}!",
        "priority": 2,
        "expire": 3600,
        "retry": 30,
        "title": f"🚨 Price Alert: {price} | {symbol}!"
    })
    print(f"Pushover response: {response.json()}")

def load_state():
    """Load last alert state from file"""
    if not os.path.exists(STATE_FILE):
        # Create the file with default state if it doesn't exist
        save_state({"alert_triggered": False})
        return {"alert_triggered": False}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"alert_triggered": False}  # Reset state if file is corrupted

def save_state(state):
    """Save alert state to file"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def check_price():
    """Fetch price from Dexscreener and trigger alert if needed"""
    state = load_state()
    
    url = f"https://api.dexscreener.com/latest/dex/pairs/{CHAIN_ID}/{PAIR_ADDRESS}"
    response = requests.get(url).json()
    price = float(response['pairs'][0]['priceNative'])

    print(price, TARGET_PRICE_HIGH, TARGET_PRICE_LOW, price >= TARGET_PRICE_HIGH or price <= TARGET_PRICE_LOW, state["alert_triggered"])

    if price >= TARGET_PRICE_HIGH or price <= TARGET_PRICE_LOW:
        if not state["alert_triggered"]:
            send_notification(price, response['pairs'][0]['baseToken']['symbol'])
            state["alert_triggered"] = True  # Mark alert as triggered
            save_state(state)
    else:
        if state["alert_triggered"]:
            state["alert_triggered"] = False  # Reset if price is back in range AND helpful when setting new price ranges (as the state resets by itself on next run)
            save_state(state)
            print("Reset alert triggered")

if __name__ == "__main__":
    check_price()
