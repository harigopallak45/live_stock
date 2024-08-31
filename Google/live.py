import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import datetime as dt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
import mplcursors  # For interactive cursor

# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Balance')
scat_buy = ax.scatter([], [], color='green', label='Buy', marker='^')
scat_sell = ax.scatter([], [], color='red', label='Sell', marker='v')

# Initialize data storage
data = {
    'timestamps': [],
    'balances': [],
    'buy_points': {'timestamp': [], 'balance': []},
    'sell_points': {'timestamp': [], 'balance': []}
}

# Function to set the appropriate x-axis intervals
def adjust_xaxis_intervals():
    time_elapsed = (data['timestamps'][-1] - data['timestamps'][0]).total_seconds()

    if time_elapsed <= 10:
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
    elif time_elapsed <= 20:
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=5))
    elif time_elapsed <= 30:
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))
    elif time_elapsed <= 60:
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=15))
    elif time_elapsed <= 120:
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=30))
    elif time_elapsed <= 300:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
    elif time_elapsed <= 600:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=2))
    elif time_elapsed <= 900:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=3))
    elif time_elapsed <= 1800:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    elif time_elapsed <= 3600:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    elif time_elapsed <= 5400:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
    else:
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))

# Initialize plot limits
def init():
    ax.set_xlim(dt.datetime.now(), dt.datetime.now() + dt.timedelta(seconds=20))
    return line, scat_buy, scat_sell

# Update function for animation
def update(frame):
    # Fetch live data
    try:
        response = requests.get(f'http://localhost:8005/trade?data={json.dumps([close[frame], volume[frame]])}')
        response.raise_for_status()
        requested = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return line, scat_buy, scat_sell
    
    # Parse the data
    timestamp = dt.datetime.now()
    balance = requested['balance']
    action = requested['action']
    
    # Update data storage
    data['timestamps'].append(timestamp)
    data['balances'].append(balance)
    
    if action == 'buy':
        data['buy_points']['timestamp'].append(timestamp)
        data['buy_points']['balance'].append(balance)
    elif action == 'sell':
        data['sell_points']['timestamp'].append(timestamp)
        data['sell_points']['balance'].append(balance)
    
    # Update plot data
    line.set_data(mdates.date2num(data['timestamps']), data['balances'])
    if data['buy_points']['timestamp']:
        scat_buy.set_offsets(np.column_stack((mdates.date2num(data['buy_points']['timestamp']), data['buy_points']['balance'])))
    if data['sell_points']['timestamp']:
        scat_sell.set_offsets(np.column_stack((mdates.date2num(data['sell_points']['timestamp']), data['sell_points']['balance'])))
    
    # Adjust x-axis limits dynamically
    ax.set_xlim(data['timestamps'][0], max(data['timestamps']) + dt.timedelta(seconds=5))
    
    # Dynamic y-axis adjustment
    current_min = min(data['balances'])
    current_max = max(data['balances'])
    ax.set_ylim(current_min - 50, current_max + 50)
    
    # Adjust x-axis intervals
    adjust_xaxis_intervals()
    
    return line, scat_buy, scat_sell

# Sample data for the example (replace with your actual data)
close = [50 + i * 0.1 for i in range(200)]
volume = [1000 + i * 10 for i in range(200)]

# Create animation
ani = FuncAnimation(fig, update, frames=range(200), init_func=init, blit=False, repeat=False, interval=1000)

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

# Enable interactive cursor
cursor = mplcursors.cursor(hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(
    f'Time: {mdates.num2date(sel.target[0]).strftime("%Y-%m-%d %H:%M:%S")}\nBalance: {sel.target[1]:.2f}'))

# Show plot
plt.show()
