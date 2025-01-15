import pandas as pd
import gzip
import os

# Specify the directory path containing your .parquet.gz files
directory_path = "."

# Iterate over all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".parquet.gz"):
        # Construct the full file path
        file_path = os.path.join(directory_path, filename)
        
        # Read the Parquet file
        data = pd.read_parquet(file_path)
        
        # Construct the output CSV file path
        csv_filename = filename.replace(".parquet.gz", ".csv")
        csv_file_path = os.path.join(directory_path, csv_filename)
        
        # Write the data to a CSV file
        data.to_csv(csv_file_path, index=False)
        
        print(f"Converted {filename} to {csv_filename}")
