import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🔐 Deeplock Firewall Logs Dashboard")

df = pd.read_csv("logs/traffic_log.csv")
st.write("Latest Logs", df.tail(10))

counts = df['decision'].value_counts()
st.bar_chart(counts)

st.line_chart(df['timestamp'].value_counts().sort_index())
