import pandas as pd
import numpy as np
import os

def transform_data(input_csv, output_csv):
    """
    Reads raw transaction data from input_csv, applies data cleaning and feature engineering,
    and saves the transformed data to output_csv.
    Additional features:
      - Log transformation of the 'Amount' column.
      - Normalization of the 'Time' column.
    Assumes the dataset has columns 'Time', 'V1'..'V28', 'Amount', 'Class'.
    """
    df = pd.read_csv(input_csv)
    df.fillna(method="ffill", inplace=True)
    
    # Create a log-transformed Amount column.
    if "Amount" in df.columns:
        df["Log_Amount"] = np.log1p(df["Amount"])
    
    # Normalize 'Time' (e.g., scale between 0 and 1).
    if "Time" in df.columns:
        df["Time_norm"] = (df["Time"] - df["Time"].min()) / (df["Time"].max() - df["Time"].min())
    
    # Save the transformed data.
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Transformed data saved to {output_csv}.")
    return df

if __name__ == "__main__":
    input_csv = "data/raw_transactions.csv"
    output_csv = "data/transformed_data.csv"
    transform_data(input_csv, output_csv)
