import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Example DataFrame
df = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100),
    'Close': np.random.randn(100).cumsum()
})
forecast_series = pd.Series(data=np.random.randn(30).cumsum(), index=pd.date_range(start='2023-05-01', periods=30))

# Plot historical and forecasted data
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Close'], label='Historical Close Prices', color='blue')
plt.plot(forecast_series.index, forecast_series, label='Predicted Close Prices', linestyle='--', color='red')

# Plot Buy/Sell signals (example)
buy_signals = df['Close'] > df['Close'].rolling(window=5).mean()  # Example condition
sell_signals = df['Close'] < df['Close'].rolling(window=5).mean()  # Example condition
plt.scatter(df['Date'][buy_signals], df['Close'][buy_signals], marker='^', color='green', label='Buy Signal', s=100)  # Green up-triangle for buy signals
plt.scatter(df['Date'][sell_signals], df['Close'][sell_signals], marker='v', color='red', label='Sell Signal', s=100)  # Red down-triangle for sell signals

# Set x-axis major ticks to automatic date locator
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Formatting the x-axis for better readability
plt.gcf().autofmt_xdate()  # Rotate date labels for better readability

# Calculate dynamic y-axis limits
min_y = min(df['Close'].min(), forecast_series.min())
max_y = max(df['Close'].max(), forecast_series.max())
y_margin = (max_y - min_y) * 0.1  # Add margin for better visualization
plt.ylim(min_y - y_margin, max_y + y_margin)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Google Stock Price with Buy/Sell Signals')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
