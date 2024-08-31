import pandas as pd

# Read the CSV file
df = pd.read_csv(r'realtime-agent\AMD.csv')

# Extract required columns
df = df[['Date', 'Close', 'Open', 'High', 'Low', 'Volume']]

# Calculate the Change % column
df['Change %'] = df['Close'].pct_change() * 100

# Rename columns
df.columns = ['Date', 'Price', 'Open', 'High', 'Low', 'Vol.', 'Change %']

# Save the DataFrame to a new CSV file
df.to_csv('new_data_format.csv', index=False)

print("Conversion completed. New CSV file saved as 'new_data_format.csv'")
