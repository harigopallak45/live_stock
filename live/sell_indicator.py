import numpy as np
import pandas as pd
import time

def generate_ohlc_data():
    while True:
        # Generate new OHLC data
        timestamp = pd.Timestamp.now()
        open_price = np.random.rand() * 100
        high_price = open_price + (np.random.rand() * 10)
        low_price = open_price - (np.random.rand() * 10)
        close_price = low_price + (np.random.rand() * (high_price - low_price))
        volume = np.random.randint(1, 1000)
        
        # Save the OHLC data to a file
        with open('sell_ohlc_data.csv', 'a') as f:
            f.write(f"{timestamp},{open_price},{high_price},{low_price},{close_price},{volume}\n")
        
        # Sleep for 1 second before generating the next data point
        time.sleep(1)

if __name__ == "__main__":
    generate_ohlc_data()
