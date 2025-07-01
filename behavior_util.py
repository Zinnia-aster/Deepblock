from scapy.all import IP, TCP
import time
from datetime import datetime
import os
import csv

def extract_behavior_features(packet):
    """Extracts behavior-related features from a packet."""
    features = {}
    if IP in packet:
        features["src_ip"] = packet[IP].src
        features["timestamp"] = time.time()
        features["time_of_day"] = datetime.now().strftime("%H:%M:%S")

    if TCP in packet:
        features["dst_port"] = packet[TCP].dport
        features["packet_len"] = len(packet)
        features["is_syn"] = int(packet[TCP].flags == "S")

    return features

def log_behavior(features, log_path="model_data/behavior_log.csv"):
    """Logs extracted behavior features into a CSV for future training."""
    os.makedirs("model_data", exist_ok=True)
    file_exists = os.path.isfile(log_path)

    with open(log_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=features.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(features)
        print("[+] Behavioral log written:", features)


