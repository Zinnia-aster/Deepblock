# 🛡️ DeepBlock — Intelligent Adaptive AI Firewall

![Status](https://img.shields.io/badge/status-Active-brightgreen)  
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)  
![Machine Learning](https://img.shields.io/badge/AI-IsolationForest-9cf)

---

### 🔥 What is DeepBlock?

**DeepBlock** is a real-time, intelligent firewall built using Python, Machine Learning, and Streamlit.  
It monitors network traffic, learns hacker behavior patterns, and evolves by retraining itself from live behavior logs.

You can think of it as a **self-learning AI security agent** — lightweight, beautiful, and powerful.

---

## 🚀 Features

- 🔒 **Rule-Based & ML-Based Filtering**
- 🤖 **AI-Powered Threat Detection** using IsolationForest
- ⛔ **Automatic IP Blocking** from learned behavior
- 📈 **Live Packet Logging & Decisions**
- 🔁 **Self-Retraining System**
- 🧠 **Beautiful Streamlit UI Dashboard**

---

### 💡 How It Works

- `firewall.py` captures packets using Scapy.
- Packet decisions are made by:
  - Static rules (`config.json`)
  - AI model (`model.pkl`) trained with IsolationForest.
- Features like destination port, packet size, and SYN flag are extracted.
- Logged behaviors go into `model_data/behavior_log.csv`.
- Repeat offenders are automatically blocked via `auto_blocker.py`.
- `auto_retrain.py` retrains the model based on labeled behavior logs.
- A modern **Streamlit UI** (`live_app.py`) shows:
  - Blocked IPs
  - Live traffic decisions
  - One-click retraining

---

## 🧪 Future Ideas

- 🌐 Geo-IP mapping & flag display  
- 📊 Real-time charts for anomaly spikes  
- ☁️ Cloud-hosted dashboard  
- 🖥️ `.exe` version for Windows  
- 💰 Commercial offering for creators/devs  

---

## 🙋‍♀️ Author

**Priyadharshini**  
_Student, AI & Data Science | ML Enthusiast | Builder of Intelligent Tools_  
India 🇮🇳  
→ _“Bringing AI to life with purpose.”_



