import pandas as pd
import pickle
from sklearn.metrics import classification_report

def evaluate_model(model_path, test_csv):
    # Load model.
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Load test data.
    df = pd.read_csv(test_csv)
    X_test = df.drop(columns=["Class"])
    y_test = df["Class"]
    
    # Predict and evaluate.
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("Evaluation Report:")
    print(report)
    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python evaluate.py model_path test_csv")
    else:
        model_path = sys.argv[1]
        test_csv = sys.argv[2]
        evaluate_model(model_path, test_csv)
