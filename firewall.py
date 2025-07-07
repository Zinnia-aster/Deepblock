from scapy.all import sniff, IP, TCP
import json
import csv
import os
from datetime import datetime
from behavior_util import extract_behavior_features, log_behavior
from auto_blocker import load_blocklist, update_blocklist
from collections import defaultdict
from joblib import load
import numpy as np

ip_log = defaultdict(int)

# Load rules from config
with open('config.json') as f:
    rules = json.load(f)

# Limit size of log file
def limit_log_size(max_lines=1000):
    log_file = 'logs/traffic_log.csv'
    if not os.path.exists(log_file):
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    if len(lines) > max_lines:
        with open(log_file, 'w') as f:
            f.write("timestamp,src_ip,dst_port,decision\n")

# Log each packet's decision
def log_packet(packet, decision):
    with open('logs/traffic_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(), 
            packet[IP].src, 
            packet[TCP].dport, 
            decision
        ])

# Main packet handler
def packet_handler(packet):
    limit_log_size()

    if IP in packet and TCP in packet:
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport

        # Check blocklist
        blocklist = load_blocklist()
        if src_ip in blocklist:
            print(f"[AUTO-BLOCKED] {src_ip} is in blocklist.")
            log_packet(packet, "AUTO-BLOCKED")
            return

        # Rule-based blocking
        if src_ip in rules["block_ips"]:
            print(f"[BLOCKED] Packet from {src_ip} to port {dst_port}")
            log_packet(packet, "BLOCKED")
            return

        if dst_port not in rules["allowed_ports"]:
            print(f"[BLOCKED] Disallowed port {dst_port} from {src_ip}")
            log_packet(packet, "BLOCKED")
            return

        # Allow packet
        print(f"[ALLOWED] {src_ip}:{dst_port}")
        log_packet(packet, "ALLOWED")

        # Extract features and log behavior
        features = extract_behavior_features(packet)
        log_behavior(features)

        # Run anomaly detection if features are valid
        if features:
            try:
                model = load("model_data/model.pkl")
                feature_vector = np.array(list(features.values())).reshape(1, -1)
                prediction = model.predict(feature_vector)  # 1 = normal, -1 = anomaly
                if prediction[0] == -1:
                    print(f"[SUSPICIOUS] {src_ip} flagged by model.")
                    update_blocklist(src_ip, ip_log)
            except Exception as e:
                print(f"[ERROR] Model prediction failed: {e}")
