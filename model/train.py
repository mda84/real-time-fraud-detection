import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

def train_model(csv_file, model_output="model/fraud_model.pkl"):
    # Read the preprocessed data.
    df = pd.read_csv(csv_file)
    
    # Assume the target column is "Class" (0: non-fraud, 1: fraud).
    X = df.drop(columns=["Class"])
    y = df["Class"]
    
    # Split the data.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a logistic regression model.
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    
    # Evaluate on test data.
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("Classification Report:")
    print(report)
    
    # Save the model.
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    with open(model_output, "wb") as f:
        pickle.dump(clf, f)
    print(f"Model saved to {model_output}.")
    
    return clf

if __name__ == "__main__":
    csv_file = "data/transformed_data.csv"
    train_model(csv_file)
