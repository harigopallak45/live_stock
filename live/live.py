import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation

# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Balance')  # Blue line for balance
scat_buy = ax.scatter([], [], color='green', label='Buy', marker='^')
scat_sell = ax.scatter([], [], color='red', label='Sell', marker='v')

# Lists to store the data
timestamps = []
balances = []
buy_points = {'timestamp': [], 'balance': []}
sell_points = {'timestamp': [], 'balance': []}

# Initialize plot
def init():
    ax.set_xlim(dt.datetime.now(), dt.datetime.now() + dt.timedelta(seconds=20))
    ax.set_ylim(5800, 6200)  # Adjust this based on expected balance range
    return line, scat_buy, scat_sell

# Update plot with new data
def update(frame):
    global timestamps, balances, buy_points, sell_points

    # Fetch live data
    response = requests.get('http://localhost:8005/trade?data=' + json.dumps([close[frame], volume[frame]]))
    requested = response.json()
    
    # Parse the data
    timestamp = dt.datetime.now()
    balance = requested['balance']
    action = requested['action']

    # Append data to lists
    timestamps.append(timestamp)
    balances.append(balance)
    
    if action == 'buy':
        buy_points['timestamp'].append(timestamp)
        buy_points['balance'].append(balance)
    elif action == 'sell':
        sell_points['timestamp'].append(timestamp)
        sell_points['balance'].append(balance)
    
    # Update plot data
    line.set_data(mdates.date2num(timestamps), balances)
    if buy_points['timestamp']:
        scat_buy.set_offsets(np.column_stack((mdates.date2num(buy_points['timestamp']), buy_points['balance'])))
    if sell_points['timestamp']:
        scat_sell.set_offsets(np.column_stack((mdates.date2num(sell_points['timestamp']), sell_points['balance'])))
    
    # Adjust x-axis limits
    ax.set_xlim(min(timestamps), max(timestamps) + dt.timedelta(seconds=5))
    
    return line, scat_buy, scat_sell

# Sample data for the example (replace with your actual data)
close = [50 + i * 0.1 for i in range(200)]
volume = [1000 + i * 10 for i in range(200)]

# Create animation
ani = FuncAnimation(fig, update, frames=range(200), init_func=init, blit=True, repeat=False, interval=1000)

# Adding titles and labels
plt.title('Live Stock Balance Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Balance')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Format the x-axis to show datetime values
ax.xaxis_date()
fig.autofmt_xdate()

# Show plot
plt.show()
