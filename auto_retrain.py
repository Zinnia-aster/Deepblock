import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

def retrain():
    file_path = "model_data/labeled_behavior_log.csv"
    if not os.path.exists(file_path):
        print("[ERROR] Labeled behavior file not found.")
        return

    print("[INFO] Loading labeled behavior data...")
    data = pd.read_csv(file_path)
    
    non_numeric = ["label", "src_ip", "timestamp", "time_of_day"]
    for col in non_numeric:
        if col in data.columns:
            data = data.drop(columns=col)

    data = data.select_dtypes(include=["number"])
    
    print("[INFO] Training new IsolationForest model...")
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(data)

    joblib.dump(model, "model_data/model.pkl")
    print("[✅] Model retrained and saved to model_data/model.pkl")

if __name__ == "__main__":
    retrain()
