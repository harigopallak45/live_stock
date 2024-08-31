import yfinance as yf
import time
import json
import requests

def get_google_stock_price():
    ticker = yf.Ticker("GOOGL")
    # Fetch the last day's data with 1-minute intervals
    data = ticker.history(period='1d', interval='1m')
    
    if data.empty:
        raise ValueError("No data retrieved; ensure that the ticker symbol and interval are correct.")
    
    close_price = data['Close'].iloc[-1]
    volume = data['Volume'].iloc[-1]
    return close_price, volume

def send_data_to_server(price, volume):
    try:
        response = requests.get('http://localhost:8005/trade', params={'data': json.dumps([price, volume])})
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to server: {e}")

if __name__ == "__main__":
    while True:
        try:
            price, volume = get_google_stock_price()
            print(f"Google Stock Price: {price}, Volume: {volume}")
            send_data_to_server(price, volume)
        except Exception as e:
            print(f"Error: {e}")
        
        # Sleep for 60 seconds before fetching the next data point
        time.sleep(60)
