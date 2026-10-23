import os
import sys
import time
from polygon import RESTClient

def get_client():
    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        print("Error: POLYGON_API_KEY not found in environment.")
        sys.exit(1)
    return RESTClient(api_key=api_key)

def monitor_level(ticker, target_price, condition="above", interval=60):
    client = get_client()
    print(f"Monitoring {ticker} for price {condition} {target_price}...")
    
    while True:
        try:
            last_trade = client.get_last_trade(ticker)
            current_price = last_trade.price
            print(f"Current price of {ticker}: {current_price}")
            
            if condition == "above" and current_price >= target_price:
                print(f"ALERT: {ticker} hit target level {target_price}!")
                break
            elif condition == "below" and current_price <= target_price:
                print(f"ALERT: {ticker} hit target level {target_price}!")
                break
                
            time.sleep(interval)
        except Exception as e:
            print(f"Error during monitoring: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python price_alert.py <ticker> <target_price> [condition: above/below] [interval_seconds]")
        sys.exit(1)
    
    ticker = sys.argv[1]
    target_price = float(sys.argv[2])
    condition = sys.argv[3] if len(sys.argv) > 3 else "above"
    interval = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    
    monitor_level(ticker, target_price, condition, interval)
