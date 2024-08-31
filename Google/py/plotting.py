import matplotlib.pyplot as plt

def plot_stock_data(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Data')
    plt.legend()
    plt.show()
