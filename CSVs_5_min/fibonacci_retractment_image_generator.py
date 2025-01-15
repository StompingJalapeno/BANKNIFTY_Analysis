import os
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

# Function to calculate Fibonacci Pivot Points
def calculate_fibonacci_pivots(df):
    high = df['high'].max()
    low = df['low'].min()
    close = df['close'].iloc[-1]

    pivot = (high + low + close) / 3
    r1 = pivot + 0.382 * (high - low)
    r2 = pivot + 0.618 * (high - low)
    r3 = pivot + (high - low)
    s1 = pivot - 0.382 * (high - low)
    s2 = pivot - 0.618 * (high - low)
    s3 = pivot - (high - low)

    return {
        "Pivot Point (P)": pivot,
        "R1": r1,
        "R2": r2,
        "R3": r3,
        "S1": s1,
        "S2": s2,
        "S3": s3,
    }

# Folder containing CSV files
folder_path = "."  # Replace with the path to your folder
output_path = "../Fibonacci Retractment Levels Image"

# Ensure the output directory exists
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Iterate over all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Ensure valid date
        df.set_index('date', inplace=True)

        # Print data check
        print(f"Data from {file_name}:")
        print(df.head())

        # Calculate Fibonacci Pivot Points
        fib_levels = calculate_fibonacci_pivots(df)

        # Plot candlestick chart using mplfinance
        fig, axes = mpf.plot(
            df,
            type='candle',
            style='charles',
            title=f"Fibonacci Pivot Points for {file_name}",
            ylabel="Price",
            returnfig=True
        )

        # Overlay Fibonacci Pivot Points
        for i, (label, level) in enumerate(fib_levels.items()):
            axes[0].axhline(y=level, color=f"C{i}", linestyle="--", label=f"{label}: {level:.2f}")

        # Add legend
        axes[0].legend(loc="best", fontsize=10)

        # Save the plot with the same name as the CSV file (replace '.csv' with '.png')
        output_filename = os.path.join(output_path, file_name.replace(".csv", ".png"))
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")
        plt.close(fig)  # Close the figure to free memory

        print(f"Chart saved for {file_name} as {output_filename}")

