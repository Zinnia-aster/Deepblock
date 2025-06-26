from firewall import packet_handler
from scapy.all import IP, TCP

# Fake packet from BLOCKED IP
packet1 = IP(src="192.168.1.100")/TCP(dport=80)
packet_handler(packet1)

# Fake packet to DISALLOWED PORT
packet2 = IP(src="8.8.8.8")/TCP(dport=9999)
packet_handler(packet2)

# Fake ALLOWED packet
packet3 = IP(src="8.8.8.8")/TCP(dport=443)
packet_handler(packet3)
