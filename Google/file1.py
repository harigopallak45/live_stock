import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib
import mplcursors


matplotlib.use('TkAgg')

def plot_historical_data():
    """
    Function to read historical stock data from a CSV file and plot the 'Close' prices over time.
    The plot includes an interactive cursor for displaying date and price information on hover.
    """
    # Specify the path to the historical data CSV file
    historical_csv_file_path = './GOOGL.csv'

    # Attempt to read the CSV file, handle possible errors
    try:
        df = pd.read_csv(historical_csv_file_path, parse_dates=['Date'], index_col='Date')
    except FileNotFoundError:
        print(f"File not found: {historical_csv_file_path}")
        return
    except pd.errors.EmptyDataError:
        print("No data in the file")
        return
    except pd.errors.ParserError:
        print("Error parsing the file")
        return

    # Check if the 'Close' column exists in the DataFrame
    if 'Close' not in df.columns:
        print("Column 'Close' not found in the CSV file.")
        return

    # Extract the 'Close' prices from the DataFrame
    close_prices = df['Close']

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the close prices with respect to dates
    line, = ax.plot(df.index, close_prices, label='Historical Close Prices', color='blue')

    # Set x-axis to display dates automatically with proper formatting
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Rotate date labels for better readability
    plt.gcf().autofmt_xdate()

    # Calculate and set dynamic y-axis limits with a margin for better visualization
    min_y = close_prices.min()
    max_y = close_prices.max()
    y_margin = (max_y - min_y) * 0.1
    ax.set_ylim(min_y - y_margin, max_y + y_margin)

    # Add labels, title, legend, and grid
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('Historical Google Stock Price from 2004 to 2022')
    ax.legend()
    ax.grid(True)

    # Add interactive cursor to display date and price on hover
    cursor = mplcursors.cursor(line, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        # sel.target is a tuple with the x and y data coordinates
        date_str = mdates.num2date(sel.target[0]).strftime('%Y-%m-%d')  # Convert date number to string
        price = sel.target[1]
        sel.annotation.set_text(f"{date_str}\n{price:.2f}")

    # Display the plot in a new window
    plt.show()

# Call the function to plot the historical data
if __name__ == "__main__":
    plot_historical_data()
