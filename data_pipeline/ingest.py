import os
import pandas as pd
import kagglehub
import zipfile

def download_fraud_data():
    """
    Downloads the Credit Card Fraud Detection dataset from Kaggle using kagglehub.
    Expects the dataset "mlg-ulb/creditcardfraud". The expected CSV file is "creditcard.csv".
    After downloading and extraction, the file is renamed to "raw_transactions.csv".
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    raw_csv_path = os.path.join(data_dir, "raw_transactions.csv")
    
    if os.path.exists(raw_csv_path):
        print(f"Data file already exists at {raw_csv_path}")
        return raw_csv_path

    print("Downloading dataset from Kaggle...")
    dataset_path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    print("Dataset downloaded to:", dataset_path)
    
    if dataset_path.endswith(".zip"):
        with zipfile.ZipFile(dataset_path, "r") as zip_ref:
            zip_ref.extractall(data_dir)
        print("Extracted dataset to", data_dir)
        os.remove(dataset_path)
        dataset_folder = data_dir
    else:
        dataset_folder = dataset_path

    extracted_csv = os.path.join(dataset_folder, "creditcard.csv")
    if not os.path.exists(extracted_csv):
        raise FileNotFoundError("Expected CSV file 'creditcard.csv' not found.")
    
    os.rename(extracted_csv, raw_csv_path)
    print(f"Renamed dataset file to {raw_csv_path}")
    return raw_csv_path

def ingest_data():
    """
    Ingest raw transaction data from the CSV file.
    Downloads data if not available.
    Returns a Pandas DataFrame with basic cleaning.
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    raw_csv_path = os.path.join(data_dir, "raw_transactions.csv")
    
    if not os.path.exists(raw_csv_path):
        raw_csv_path = download_fraud_data()
    
    df = pd.read_csv(raw_csv_path)
    df.fillna(method="ffill", inplace=True)
    return df

if __name__ == "__main__":
    df = ingest_data()
    print("Preview of ingested data:")
    print(df.head())
