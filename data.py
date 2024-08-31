import yfinance as yf
import pandas as pd
import math
from tqdm import tqdm
import pickle
import numpy as np
import random
from multiprocessing import Pool

pd.options.mode.chained_assignment = None  # Disable chained assignment warning

# List of tickers to fetch data for
tickers = ['TSLA', 'AAPL', 'MSFT', 'U', 'CCL', 'TD', 'SPY', 'FB', 'V', 'DIS', 
           'CNR', 'HD', 'UNH', 'MCD', 'MMM', 'ATVI', 'ADBE', 'AMD', 'GOOG', 
           'AMZN', 'AXP', 'BAC', 'BA', 'CVX', 'C', 'KO', 'DOW', 'GM', 'GILD', 
           'INTC', 'MA', 'NVDA', 'TXN', 'XRX', 'RY.TO', 'CP.TO', 'TRI.TO', 
           'ATD-B.TO', 'L.TO', 'DOL.TO', 'BB.TO', 'DOO.TO', 'WEED.TO', 
           'SNC.TO', 'SHOP', 'SU.TO', 'CM.TO', 'TD.TO', 'ENB.TO', 'APHA.TO', 
           'XIU.TO', 'AC.TO']

# Dictionary to store raw data
raws = {}

print('Downloading Data')

# Fetching historical data for each ticker
for ticker in tqdm(tickers):
    t = yf.Ticker(ticker)
    t_data = t.history(period='10y', interval='1d')
    raws[ticker] = t_data

print('Done')

# Dropping unnecessary columns
col_d = {}  # Dictionary to store cleaned data
for ticker in tickers:
    raw = raws[ticker]
    col_d[ticker] = raw.drop(columns=['Dividends', 'Stock Splits'])

# Function to standardize data and create sequences
def z_score(df, f1, f2, f3):
    df['DayOfWeek'] = [i.dayofweek for i in df.index]  # Adding DayOfWeek as a feature
    for column in df.columns:
        std = df[column].std()
        mean = df[column].mean()
        df[column] = (df[column] - mean) / std if std != 0 else 0
        if column == 'Close':
            f1 = (f1 - mean) / std if std != 0 else 0
            f2 = (f2 - mean) / std if std != 0 else 0
            f3 = (f3 - mean) / std if std != 0 else 0
    nan_flag = df.isnull().values.any() or math.isnan(f1) or math.isnan(f2) or math.isnan(f3)
    return df.values, f1, f2, f3, nan_flag

# Function to convert dataframe into sequences
def sequencify(df):
    s1, s2, s3 = [], [], []
    dropped = 0
    for i in range(len(df.index) - 13):
        sequence, f1, f2, f3, nan_flag = z_score(df.iloc[i:i+10], df['Close'].iloc[i+10], df['Close'].iloc[i+11], df['Close'].iloc[i+12])
        if nan_flag:
            dropped += 1
        else:
            s1.append([sequence, f1])
            s2.append([sequence, f2])
            s3.append([sequence, f3])
    return [s1, s2, s3, dropped]

print('Generating sequences. This may take a while...')

# Using multiprocessing to speed up sequence generation
a1, a2, a3 = [], [], []
dropped = 0
with Pool(8) as pool:
    results = pool.imap_unordered(sequencify, list(col_d.values()))
    for res in results:
        a1.append(res[0])
        a2.append(res[1])
        a3.append(res[2])
        dropped += res[3]

print(f'Done! Dropped {dropped} sequences containing NaN')

print('Separating and shuffling sequences')

train1, test1 = [], []
train2, test2 = [], []
train3, test3 = [], []

# Test to train ratio
RATIO = 0.05

# Splitting and shuffling data
for hist in a1:
    split = math.floor(len(hist) * RATIO)
    train1.extend(hist[:-split])
    test1.extend(hist[-split:])
for hist in a2:
    split = math.floor(len(hist) * RATIO)
    train2.extend(hist[:-split])
    test2.extend(hist[-split:])
for hist in a3:
    split = math.floor(len(hist) * RATIO)
    train3.extend(hist[:-split])
    test3.extend(hist[-split:])

random.shuffle(train1)
random.shuffle(train2)
random.shuffle(train3)
random.shuffle(test1)
random.shuffle(test2)
random.shuffle(test3)

print('Done')

# Function to save sequences to CSV files
def save_sequences_to_csv(sequences, filename_prefix):
    for i, seq in enumerate(sequences):
        df = pd.DataFrame(seq[0].reshape(10, -1), columns=['Open', 'High', 'Low', 'Close', 'Volume', 'DayOfWeek'])
        df['FutureClose'] = seq[1]
        df.to_csv(f'./data/{filename_prefix}_sequence_{i}.csv', index=False)

# Saving train and test sequences to CSV files
save_sequences_to_csv(train1, 'train1')
save_sequences_to_csv(test1, 'test1')
save_sequences_to_csv(train2, 'train2')
save_sequences_to_csv(test2, 'test2')
save_sequences_to_csv(train3, 'train3')
save_sequences_to_csv(test3, 'test3')

print('Done saving data to CSV files!')
