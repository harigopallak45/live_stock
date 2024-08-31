from data_processing import load_and_process_data
from plotting import plot_stock_data

def main():
    file_path = '../GOOGL.csv'  # Update with your file path
    df = load_and_process_data(file_path)
    plot_stock_data(df)

if __name__ == "__main__":
    main()
