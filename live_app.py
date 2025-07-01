import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

st.set_page_config(page_title="DeepBlock AI Firewall", layout="wide")

st.title("🛡️ DeepBlock AI Firewall Dashboard")

# Load behavior log
behavior_path = "model_data/behavior_log.csv"
model_path = "model_data/model.pkl"

if not os.path.exists(behavior_path) or not os.path.exists(model_path):
    st.error("❌ Missing required files: behavior_log.csv or model.pkl")
    st.stop()

df = pd.read_csv(behavior_path)

# Load trained model
model = joblib.load(model_path)

# Prepare features
features = df[["dst_port", "packet_len", "is_syn"]]

# Predict
df["prediction"] = model.predict(features)
df["prediction"] = df["prediction"].map({1: "normal", -1: "suspicious"})

# Optional: show risk level (anomaly score)
df["risk_score"] = model.decision_function(features)
df["risk_level"] = pd.cut(df["risk_score"], bins=[-float('inf'), -0.2, 0.1, float('inf')],
                          labels=["⚠️ High", "🟡 Medium", "🟢 Low"])

# Convert timestamp if available
if "timestamp" in df.columns:
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s', errors="coerce")
    except:
        pass

# Show latest logs
st.subheader("📋 Latest Traffic Logs")
st.dataframe(df.tail(10), use_container_width=True)

# Count chart
st.subheader("📊 Traffic Type Count")
st.bar_chart(df["prediction"].value_counts())

# Risk breakdown
st.subheader("📈 Risk Level Distribution")
st.bar_chart(df["risk_level"].value_counts())

# Timeline of suspicious activity
if "timestamp" in df.columns:
    st.subheader("⏱️ Suspicious Activity Over Time")
    suspicious_time = df[df["prediction"] == "suspicious"]
    time_chart = suspicious_time.groupby("timestamp").size()
    st.line_chart(time_chart)

# Download option
st.download_button("⬇️ Download full behavior log", data=df.to_csv(index=False), file_name="behavior_log_with_predictions.csv")



