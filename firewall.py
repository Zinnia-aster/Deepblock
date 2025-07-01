from scapy.all import sniff, IP, TCP
import json
import csv
import os
from datetime import datetime
from behavior_util import extract_behavior_features, log_behavior


with open('config.json') as f:
    rules = json.load(f)

def limit_log_size(max_lines=1000):
    log_file = 'logs/traffic_log.csv'
    if not os.path.exists(log_file):
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    if len(lines) > max_lines:
        with open(log_file, 'w') as f:
            f.write("timestamp,src_ip,dst_port,decision\n")

def log_packet(packet, decision):
    with open('logs/traffic_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(), 
            packet[IP].src, 
            packet[TCP].dport, 
            decision
        ])

def packet_handler(packet):
    limit_log_size() 


    if IP in packet and TCP in packet:
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport

        if src_ip in rules["block_ips"]:
            print(f"[BLOCKED] Packet from {src_ip} to port {dst_port}")
            log_packet(packet, "BLOCKED")
            return

        if dst_port not in rules["allowed_ports"]:
            print(f"[BLOCKED] Disallowed port {dst_port} from {src_ip}")
            log_packet(packet, "BLOCKED")
            return

        print(f"[ALLOWED] {src_ip}:{dst_port}")
        log_packet(packet, "ALLOWED")

        features = extract_behavior_features(packet)
        log_behavior(features)



def limit_log_size(max_lines=1000):
    log_file = 'logs/traffic_log.csv'
    if not os.path.exists(log_file):
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    if len(lines) > max_lines:
        with open(log_file, 'w') as f:
            f.write("timestamp,src_ip,dst_port,decision\n")  # reset log
