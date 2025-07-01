import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load data
data_path = "model_data/behavior_log.csv"
df = pd.read_csv(data_path)
features = df[["dst_port", "packet_len", "is_syn"]]

# Train Isolation Forest
model = IsolationForest(
    n_estimators=100,
    contamination=0.1,  
    random_state=42
)
model.fit(features)

# Save the model
os.makedirs("model_data", exist_ok=True)
joblib.dump(model, "model_data/model.pkl")
print("✅ Model trained & saved as model_data/model.pkl")
