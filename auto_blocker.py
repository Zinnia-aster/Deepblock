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

    drop_cols = ["label", "src_ip", "timestamp", "time_of_day"]
    for col in drop_cols:
        if col in data.columns:
            data = data.drop(columns=[col])

    print("[INFO] Training new IsolationForest model...")
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(data)

    joblib.dump(model, "model_data/model.pkl")
    print("✅ Model retrained and saved to model_data/model.pkl")

if __name__ == "__main__":
    retrain()

import json
import os

BLOCKLIST_FILE = "model_data/blocklist.json"

def load_blocklist():
    if os.path.exists(BLOCKLIST_FILE):
        with open(BLOCKLIST_FILE, "r") as f:
            return json.load(f)
    return {}

