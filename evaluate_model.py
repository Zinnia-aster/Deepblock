import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("model_data/labeled_behavior_log.csv")
model = joblib.load("model_data/model.pkl")

# Prepare input features
X = df[["dst_port", "packet_len", "is_syn"]]

# Map string labels to numeric format
label_map = {"normal": 1, "suspicious": -1}
y_true = df["label"].map(label_map)

# Predict using the model
y_pred = model.predict(X)

print("🧠 Classification Report:\n")
print(classification_report(y_true, y_pred, target_names=["suspicious", "normal"], zero_division=0))

print("\n🔍 Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))
