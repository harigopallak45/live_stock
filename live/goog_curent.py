import requests
import time
from datetime import datetime

def fetch_stock_data(api_key, symbol, date):
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{date}/{date}?adjusted=true&sort=asc&limit=120&apiKey={api_key}'
    response = requests.get(url)
    try:
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    except ValueError as val_err:
        print(f'Error decoding JSON: {val_err}')
    return None

def main():
    # Your Polygon.io API key
    api_key = 'xIjgd5kIAllKlWlXS9_rNzZtYkq7iLcb'
    
    # Symbol for the stock (AAPL for Apple Inc.)
    symbol = 'GOOG'
    
    # Date for fetching data (January 9, 2023)
    date = "01.01.2024"
    
    while True:
        # Fetch stock data
        stock_data = fetch_stock_data(api_key, symbol, date)
        
        # Check if data is fetched successfully
        if stock_data:
            print(f"Aggregated Daily Stock Data for {symbol} on {date}:")
            for index, data_point in enumerate(stock_data['results']):
                print(f"Data Point {index + 1}:")
                print(f"  Timestamp: {data_point['t']}")
                print(f"  Open Price: {data_point['o']}")
                print(f"  Close Price: {data_point['c']}")
                print(f"  High Price: {data_point['h']}")
                print(f"  Low Price: {data_point['l']}")
                print(f"  Volume: {data_point['v']}")
                print()
        else:
            print("Failed to fetch stock data.")
        
        # Wait for 5 seconds before making the next request
        time.sleep(1)

if __name__ == "__main__":
    main()
