from scapy.all import ARP, Ether, srp
import time
from datetime import datetime

# Replace this with your network's IP range
IP_RANGE = "192.168.56.0/24"

def scan_network():
    arp = ARP(pdst=IP_RANGE)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]
    devices = {rcv.hwsrc.lower() for _, rcv in result}
    return devices

def check_wifi_presence(mac_address, duration=6, interval=60):
    """
    Checks for a specific MAC address every `interval` seconds for `duration` minutes.
    Displays and logs presence at each check.
    """
    mac_address = mac_address.lower()
    success_count = 0

    for i in range(duration):
        print(f"[SCAN {i+1}/{duration}] Scanning at {datetime.now().strftime('%H:%M:%S')}...")
        devices = scan_network()

        if mac_address in devices:
            print(f"✅ {mac_address} is PRESENT on the network.")
            success_count += 1
        else:
            print(f"❌ {mac_address} is ABSENT on the network.")

        if i < duration - 1:
            time.sleep(interval)

    print(f"[SUMMARY] {mac_address} was present {success_count}/{duration} times.")

    return success_count == duration
