import sys
import pickle
import numpy as np

def predict(model_path, features):
    # Convert features to numpy array.
    features = np.array(features, dtype=np.float32).reshape(1, -1)
    
    # Load model.
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Get fraud probability.
    probability = model.predict_proba(features)[0][1]
    return probability

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python predict.py model_path feature1 feature2 ...")
    else:
        model_path = sys.argv[1]
        features = list(map(float, sys.argv[2:]))
        prob = predict(model_path, features)
        print("Fraud Probability:", prob)
