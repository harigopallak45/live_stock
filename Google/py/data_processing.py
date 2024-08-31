import pandas as pd

def load_and_process_data(file_path):
    df = pd.read_csv(file_path)
    # Perform any data processing here
    return df
