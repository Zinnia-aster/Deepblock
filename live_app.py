# live_app.py

import streamlit as st
import pandas as pd
import os
import json
import auto_retrain
from auto_blocker import load_blocklist
from datetime import datetime

st.set_page_config(page_title="🛡️ DeepBlock AI Firewall", layout="wide")

# --- HEADER ---
st.markdown("""
    <h1 style='text-align: center; color: #00ffae;'>🧠 DeepBlock Firewall</h1>
    <h4 style='text-align: center; color: white;'>Creator-Grade. Adaptive. Smartly Dangerous.</h4>
    <hr style="border: 1px solid #00ffae;" />
""", unsafe_allow_html=True)

# --- BLOCKLIST SECTION ---
st.subheader("🚫 Blocked IPs (Auto + Manual)")
blocklist = load_blocklist()

if blocklist:
    formatted_blocklist = []
    for ip, info in blocklist.items():
        time = info.get("timestamp", "Unknown")
        formatted_blocklist.append({
            "🚫 IP Address": ip,
            "📆 Blocked On": time,
            "📍 Type": "Auto" if "auto" in info.get("reason", "").lower() else "Manual"
        })
    st.dataframe(pd.DataFrame(formatted_blocklist), use_container_width=True)
else:
    st.success("✅ No threats currently blocked!")

# --- TRAFFIC LOG ---
st.subheader("📊 Real-Time Traffic Log (Last 50 packets)")

log_file = "logs/traffic_log.csv"
if os.path.exists(log_file):
    df = pd.read_csv(log_file)
    df = df.tail(50)[["timestamp", "src_ip", "dst_port", "decision"]]
    df["decision"] = df["decision"].apply(
        lambda x: f"✅ {x}" if "ALLOW" in x else f"⛔ {x}"
    )
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Traffic log not found.")

# --- RETRAIN SECTION ---
st.subheader("🔄 AI Model Re-Trainer")

if st.button("🧠 Retrain Model with Behavior Log"):
    with st.spinner("Feeding new behavior logs to AI..."):
        try:
            auto_retrain.retrain()
            st.success("🎉 Model updated! Your firewall just got smarter.")
        except Exception as e:
            st.error(f"❌ Failed to retrain: {e}")

# --- INSIGHTS ---
st.subheader("📈 Intelligence Dashboard")
st.markdown("""
> Soon you’ll be able to see:  
- 🧠 Live anomaly graph  
- 🔌 Top targeted ports  
- 🌐 IP heatmap  
- ⏳ Suspicious traffic trends  
""")

st.markdown("---")
st.caption("Built by Priya • Powered by ML • Respect the Firewall ⚡")




