from firewall import packet_handler
from scapy.all import sniff

print("🛡️ Deeplock is ACTIVE — Monitoring your network...\n")
sniff(filter="tcp", prn=packet_handler, store=0)
