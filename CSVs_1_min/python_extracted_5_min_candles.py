import os
import pandas as pd

# Path to the folder containing the CSV files
input_folder = "."
output_folder = "../CSVs_5_min"

# Ensure the output folder exists, if not create it
os.makedirs(output_folder, exist_ok=True)

# Get all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Loop through all CSV files
for file_name in csv_files:
    # Full path to the current file
    file_path = os.path.join(input_folder, file_name)
    
    # Load the CSV file
    df = pd.read_csv(file_path, parse_dates=['date'])
    
    # Filter for January 10th, 2024 only
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'].dt.date == pd.to_datetime('2024-01-10').date()]

    # Skip if there is no data for 10th Jan 2024
    if df.empty:
        print(f"No data for 2024-01-10 in {file_name}, skipping...")
        continue

    # Set 'date' column as the index
    df.set_index('date', inplace=True)

    # Resample data to 5-minute intervals
    resampled_df = df.resample('5T').agg({
        'open': 'first',   # First value in the interval
        'high': 'max',     # Maximum value in the interval
        'low': 'min',      # Minimum value in the interval
        'close': 'last',   # Last value in the interval
        'volume': 'sum'    # Sum of volumes in the interval
    })

    # Drop rows where 'volume' is 0, as no trades occurred during those periods
    resampled_df = resampled_df[resampled_df['volume'] > 0]

    # Define the output path for this file
    output_file_name = f"5min_{file_name}"
    output_path = os.path.join(output_folder, output_file_name)

    # Save the resampled data to CSV
    resampled_df.to_csv(output_path)

    print(f"Resampled data saved to {output_path}")
